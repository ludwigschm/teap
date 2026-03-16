"""No-op cloud bridge for click-dummy mode."""

from __future__ import annotations

from typing import Any


def init_client(*_args: Any, **_kwargs: Any) -> None:
    return None


def push_async(*_args: Any, **_kwargs: Any) -> None:
    return None
