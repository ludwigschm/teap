"""No-op async bridge for click-dummy mode."""

from __future__ import annotations

from typing import Any, Callable


def enqueue(callable_obj: Callable[..., Any], *_args: Any, **_kwargs: Any) -> None:
    try:
        callable_obj()
    except Exception:
        return None
