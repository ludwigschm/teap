"""No-op round CSV logging for click-dummy mode."""

from __future__ import annotations

from typing import Any


def init_round_log(*_args: Any, **_kwargs: Any) -> None:
    return None


def write_round_log(*_args: Any, **_kwargs: Any) -> None:
    return None


def flush_round_log(*_args: Any, **_kwargs: Any) -> None:
    return None


def close_round_log(*_args: Any, **_kwargs: Any) -> None:
    return None


def round_log_action_label(*_args: Any, **_kwargs: Any) -> str:
    return ""
