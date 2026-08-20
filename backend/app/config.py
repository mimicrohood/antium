"""Runtime configuration, resolved from environment variables."""
import os
from pathlib import Path

# Where the growing pulse dataset lives (gitignored).
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PULSES_FILE = DATA_DIR / "pulses.json"

# rayoid's genesis — day 0 of "Days Online". Fixed so the counter is stable across restarts.
# Matches the project's public launch framing.
GENESIS = "2026-08-19"

# Ambient emission cadence, in seconds. 0 disables the background emitter (emit-on-demand only).
EMIT_SECONDS = int(os.environ.get("RAYOID_EMIT_SECONDS", "20"))

# Claude Fable 5 is used for pulse generation only when a key is present.
# The model id matches the site's "Tech Support: Claude Fable 5".
CLAUDE_MODEL = "claude-fable-5"


def has_claude() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def mode() -> str:
    return "claude-fable-5" if has_claude() else "local"
