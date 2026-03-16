"""No-op logging helpers for click-dummy mode."""

from __future__ import annotations

from typing import Any


def log_event(*_args: Any, **_kwargs: Any) -> None:
    return None
