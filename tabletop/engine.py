"""Minimal engine types for the click-dummy UI."""

from __future__ import annotations

from enum import Enum
from typing import Any


class Phase(Enum):
    WAITING_START = "WAITING_START"
    DEALING = "DEALING"
    SIGNAL_WAIT = "SIGNAL_WAIT"
    CALL_WAIT = "CALL_WAIT"
    REVEAL_SCORE = "REVEAL_SCORE"


class EventLogger:
    """No-op logger kept for compatibility with the view layer."""

    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        pass

    def log_event(self, *_args: Any, **_kwargs: Any) -> None:
        return None

    def close(self) -> None:
        return None
