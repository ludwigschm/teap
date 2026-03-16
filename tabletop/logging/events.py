"""No-op event logging for click-dummy mode."""

from __future__ import annotations

from typing import Any


class Events:
    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        pass

    def log_event(self, *_args: Any, **_kwargs: Any) -> None:
        return None

    def close(self) -> None:
        return None
