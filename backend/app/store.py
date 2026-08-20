"""Persistent store for pulses + the ray-web + homepage stats.

Thread-safe (a lock guards mutation) so the ambient emitter and HTTP handlers can share it.
Pulses persist to data/pulses.json; the ray-web is derived, not stored.
"""
from __future__ import annotations
import json
import threading
from datetime import date, datetime, timezone

from . import config, pulse_engine

_lock = threading.Lock()


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class Store:
    def __init__(self) -> None:
        self._pulses: list[dict] = []
        self._seq = 0
        self._load()

    # ---- persistence ----
    def _load(self) -> None:
        if config.PULSES_FILE.exists():
            try:
                data = json.loads(config.PULSES_FILE.read_text(encoding="utf-8"))
                self._pulses = data.get("pulses", [])
                self._seq = data.get("seq", len(self._pulses))
            except Exception:
                self._pulses, self._seq = [], 0

    def _save(self) -> None:
        config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        payload = {"seq": self._seq, "pulses": self._pulses}
        config.PULSES_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- emission ----
    def emit(self, category: str | None = None) -> dict:
        with _lock:
            self._seq += 1
            seq = self._seq
            cat = category if category in pulse_engine.CATEGORIES else \
                pulse_engine.CATEGORIES[seq % len(pulse_engine.CATEGORIES)]
            text, source = pulse_engine.generate(cat, seq)
            pulse = {
                "id": f"pulse-{seq:06d}",
                "seq": seq,
                "category": cat,
                "text": text,
                "source": source,
                "emitted_at": _now_iso(),
            }
            self._pulses.append(pulse)
            self._save()
            return pulse

    # ---- reads ----
    def list(self, limit: int = 50, category: str | None = None) -> list[dict]:
        with _lock:
            items = self._pulses
            if category:
                items = [p for p in items if p["category"] == category]
            return list(reversed(items[-limit:]))

    def get(self, pulse_id: str) -> dict | None:
        with _lock:
            for p in self._pulses:
                if p["id"] == pulse_id:
                    return {**p, "links": self._links_for(p)}
            return None

    def count(self) -> int:
        with _lock:
            return len(self._pulses)

    # ---- ray-web ----
    def _links_for(self, pulse: dict) -> list[str]:
        """A pulse resonates with the most recent earlier pulses that share its category."""
        earlier = [p for p in self._pulses if p["seq"] < pulse["seq"] and p["category"] == pulse["category"]]
        return [p["id"] for p in earlier[-2:]]

    def rayweb(self) -> dict:
        with _lock:
            nodes = [{"id": p["id"], "category": p["category"], "seq": p["seq"]} for p in self._pulses]
            edges = []
            for p in self._pulses:
                for target in self._links_for(p):
                    edges.append({"from": p["id"], "to": target})
            return {"nodes": nodes, "edges": edges}

    # ---- stats (drive the homepage counters) ----
    def stats(self) -> dict:
        with _lock:
            n = len(self._pulses)
            genesis = date.fromisoformat(config.GENESIS)
            days_online = max(1, (date.today() - genesis).days)
            by_cat = {c: 0 for c in pulse_engine.CATEGORIES}
            for p in self._pulses:
                by_cat[p["category"]] = by_cat.get(p["category"], 0) + 1
            last = self._pulses[-1]["emitted_at"] if self._pulses else None
            return {
                "pulses_emitted": n,
                "days_online": days_online,
                "always_sensing": "24/7",
                "open_source": "100%",
                "ray_web_size": n,
                "by_category": by_cat,
                "last_pulse_at": last,
            }


store = Store()
