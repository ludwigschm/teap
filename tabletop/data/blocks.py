"""Helpers for loading tabletop block and card configuration data."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Dict, List, Tuple

from tabletop.data.config import CARD_COMBINATIONS_DIR, CARD_DIR


def load_blocks() -> List[Dict[str, Any]]:
    """Load only block 1 for the conference click-dummy."""

    path = CARD_COMBINATIONS_DIR / "Paare1.csv"
    rounds = load_csv_rounds(path)
    return [
        {
            "index": 1,
            "label": "Block 1",
            "csv": path.name,
            "csv_path": path,
            "path": path,
            "rounds": rounds,
            "payout": False,
            "practice": False,
        }
    ]


def load_csv_rounds(path: Path) -> List[Dict[str, Any]]:
    rounds: List[Dict[str, Any]] = []
    try:
        with open(path, newline="", encoding="utf-8") as fp:
            rows = list(csv.reader(fp))
    except (FileNotFoundError, Exception):
        return rounds

    def parse_cards(row: List[str], start: int, end: int) -> Tuple[int, int]:
        values: List[int] = []
        for idx in range(start, min(end, len(row))):
            cell = (row[idx] or "").strip()
            if not cell:
                continue
            try:
                values.append(int(float(cell)))
            except ValueError:
                continue
            if len(values) == 2:
                break
        if len(values) < 2:
            raise ValueError("Zu wenige Karten")
        return tuple(values[:2])  # type: ignore[return-value]

    start_idx = 0
    if rows:
        try:
            parse_cards(rows[0], 2, 6)
            parse_cards(rows[0], 7, 11)
        except Exception:
            start_idx = 1

    for row in rows[start_idx:]:
        if not row or all((cell or "").strip() == "" for cell in row):
            continue
        try:
            vp1_cards = parse_cards(row, 2, 6)
            vp2_cards = parse_cards(row, 7, 11)
        except Exception:
            continue

        rounds.append({"vp1": vp1_cards, "vp2": vp2_cards})

    return rounds


def value_to_card_path(value: Any) -> str:
    fallback = CARD_DIR / "back.png"
    try:
        number = int(value)
    except (TypeError, ValueError):
        return str(fallback)
    path = CARD_DIR / f"{number}.png"
    return str(path) if path.exists() else str(fallback)


__all__ = ["load_blocks", "load_csv_rounds", "value_to_card_path"]
