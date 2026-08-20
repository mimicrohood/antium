# rayoid backend

**The pulse engine.** rayoid is an autonomous electric-sense organism; this service is
the part of it that actually *emits*. It generates **electric pulses** (short signal-texts),
links them into a **ray-web** (a graph of resonant pulses), stores the growing dataset, and
serves it — plus the live stats the site's homepage shows (Pulses Emitted, Days Online, …).

It runs **self-contained** out of the box: no API key required. If `ANTHROPIC_API_KEY`
is set, pulses are generated with **Claude Fable 5** for richer, less repetitive signals;
otherwise a local generator composes them from rayoid's own lexicon of currents and drift.

## Run

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8080
```

Open http://127.0.0.1:8080/docs for the interactive API, or hit the endpoints directly.

Optional — richer pulses via Claude Fable 5:

```bash
export ANTHROPIC_API_KEY=sk-ant-...   # Windows: set ANTHROPIC_API_KEY=...
```

## Endpoints

| Method | Path | What it does |
|---|---|---|
| `GET`  | `/`                | Service banner + mode (`local` or `claude-fable-5`) |
| `GET`  | `/health`          | Liveness probe |
| `GET`  | `/stats`           | Live counters for the homepage (pulses emitted, days online, …) |
| `GET`  | `/pulses`          | Recent pulses (`?limit=`, `?category=`) |
| `GET`  | `/pulses/{id}`     | One pulse + its ray-web links |
| `POST` | `/pulses/emit`     | Emit a new pulse now (optional `{"category": "..."}`) |
| `GET`  | `/rayweb`          | The ray-web graph (`{nodes, edges}`) |

## Data

Pulses persist to `backend/data/pulses.json` (created on first run, gitignored). Delete it
to reset the organism to a cold start.

## Ambient emission

On startup the engine emits a pulse every ~20s (configurable via `RAYOID_EMIT_SECONDS`),
so the dataset grows on its own — the digital-deep equivalent of a ray that "refuses to
hold still." Set `RAYOID_EMIT_SECONDS=0` to disable ambient emission and only emit on demand.
