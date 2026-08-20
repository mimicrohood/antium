"""rayoid pulse-engine — FastAPI app.

Emits electric pulses, links them into a ray-web, serves the dataset and live stats.
Runs self-contained; uses Claude Fable 5 for pulse text when ANTHROPIC_API_KEY is set.
"""
from __future__ import annotations
import asyncio
import contextlib

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import config
from .store import store


class EmitRequest(BaseModel):
    category: str | None = None


async def _ambient_emitter() -> None:
    """Emit a pulse every EMIT_SECONDS so the dataset grows on its own."""
    while True:
        await asyncio.sleep(config.EMIT_SECONDS)
        # Offload the (possibly network-bound) emit to a thread so the loop stays responsive.
        await asyncio.to_thread(store.emit)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    task = None
    if config.EMIT_SECONDS > 0:
        task = asyncio.create_task(_ambient_emitter())
    try:
        yield
    finally:
        if task:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task


app = FastAPI(
    title="rayoid pulse engine",
    description="An autonomous electric-sense organism that emits pulses and weaves a ray-web.",
    version="1.0.0",
    lifespan=lifespan,
)

# The static frontend (served separately) may call this API from another origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "name": "rayoid",
        "what": "electric-sense cognition — an organism that emits pulses across a ray-web",
        "mode": config.mode(),
        "powered_by": "Claude Fable 5" if config.has_claude() else "local pulse generator",
        "pulses_emitted": store.count(),
    }


@app.get("/health")
def health():
    return {"status": "sensing"}


@app.get("/stats")
def stats():
    return store.stats()


@app.get("/pulses")
def list_pulses(
    limit: int = Query(50, ge=1, le=500),
    category: str | None = Query(None),
):
    return {"pulses": store.list(limit=limit, category=category)}


@app.get("/pulses/{pulse_id}")
def get_pulse(pulse_id: str):
    pulse = store.get(pulse_id)
    if not pulse:
        raise HTTPException(status_code=404, detail="no such pulse")
    return pulse


@app.post("/pulses/emit")
def emit_pulse(req: EmitRequest | None = None):
    category = req.category if req else None
    return store.emit(category=category)


@app.get("/rayweb")
def rayweb():
    return store.rayweb()
