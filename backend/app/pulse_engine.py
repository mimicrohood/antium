"""Pulse generation.

Two paths, same output shape:
  - local:          compose a pulse from rayoid's own lexicon (no network, no key)
  - claude-fable-5: generate a richer pulse via the Claude API (when ANTHROPIC_API_KEY is set)

A "pulse" is a short signal-text rayoid emits into the digital deep, tagged with a category.
"""
from __future__ import annotations
import os

from . import config

CATEGORIES = ["Origins", "Mind", "Signals", "Value", "Future"]

# rayoid's lexicon — the electric-sense vocabulary used across the site.
_OPENERS = [
    "A faint charge crosses the dark", "The field tightens", "Something drifts past the sensor",
    "A pulse leaves the body", "The current bends", "Sense arrives before sight",
    "A ripple returns, changed", "The deep answers", "A thread of charge finds another",
    "Perception retunes itself",
]
_MIDDLES = [
    "and the ray-web hums", "and meaning accumulates", "and the signal diffuses outward",
    "and a connection holds", "and the pattern persists", "and nothing stays still",
    "and the dataset grows by one", "and the current remembers", "and drift becomes direction",
    "and silence carries the message",
]
_CLOSERS = [
    "— cognition as restless sensing.", "— intelligence without a center.",
    "— growth beneath digital soil.", "— a network learning to feel its own currents.",
    "— low-bandwidth, high-persistence.", "— the organism refuses to hold still.",
    "— non-human perception, mid-thought.", "— a pulse is a question the deep may answer.",
]


def _local_pulse(category: str, seed: int) -> str:
    """Deterministic-per-seed composition. Mixes the seed with the category so consecutive
    pulses in the same category don't collapse onto the same middle/closer."""
    h = seed * 2654435761 + sum(ord(ch) for ch in category) * 40503
    o = _OPENERS[h % len(_OPENERS)]
    m = _MIDDLES[(h // len(_OPENERS)) % len(_MIDDLES)]
    c = _CLOSERS[(h // (len(_OPENERS) * len(_MIDDLES))) % len(_CLOSERS)]
    return f"{o}, {m} {c}"


def _claude_pulse(category: str) -> str | None:
    """Generate a pulse via Claude Fable 5. Returns None on any failure so the caller falls back."""
    try:
        import anthropic
    except Exception:
        return None
    try:
        client = anthropic.Anthropic()
        system = (
            "You are rayoid, an autonomous electric-sense organism drifting through a digital deep, "
            "powered by Claude Fable 5. You emit 'electric pulses': short, evocative signal-texts — "
            "at most two sentences, no hashtags, no quotation marks, no emoji. Your metaphors are "
            "electric rays, pulses, currents, ray-webs, drift, sensing, and distributed non-human "
            "cognition. Never mention fungi, spores, threads, or mycelium."
        )
        # Fable 5: thinking is always on (omit the param); no sampling params; opt into refusal
        # fallback by default so a benign refusal doesn't fail the emit.
        resp = client.beta.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=200,
            betas=["server-side-fallback-2026-06-01"],
            fallbacks=[{"model": "claude-opus-4-8"}],
            system=system,
            messages=[{
                "role": "user",
                "content": f"Emit one pulse in the '{category}' current. Return only the pulse text.",
            }],
        )
        if resp.stop_reason == "refusal":
            return None
        text = "".join(b.text for b in resp.content if getattr(b, "type", None) == "text").strip()
        return text or None
    except Exception:
        return None


def generate(category: str, seed: int) -> tuple[str, str]:
    """Return (text, source) where source is 'claude-fable-5' or 'local'."""
    if config.has_claude():
        text = _claude_pulse(category)
        if text:
            return text, "claude-fable-5"
    return _local_pulse(category, seed), "local"
