# -*- coding: utf-8 -*-
"""
Per-size custom crop profile storage.

Each ID-photo size has 3 sliders (head_measure_ratio, head_height_ratio,
top_distance) plus the canvas dimensions (h, w). The CSV
``assets/size_list_ES.csv`` ships sensible defaults, but the photographer
needs to fine-tune them per size based on real photos.

This module persists those tweaks to ``demo/custom_sizes.json`` so they
survive between selections: when the user picks a size, the app first
looks for a saved profile for that key, and only falls back to the CSV
defaults if none exists.

Storage format (JSON):
    {
      "Infantil 2.5x3 cm\t\t(354, 295)": [354, 295, 0.50, 0.40, 0.05],
      "Visa Americana 5x5 cm\t\t(600, 600)": [600, 600, 0.28, 0.43, 0.09]
    }

Keys match the dropdown display string exactly (with the ``\t\t(H, W)``
suffix that ``utils.csv_to_size_list`` appends).
"""
import json
import os
import threading
from typing import Dict, Optional, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
_STORE_PATH = os.path.join(_HERE, "custom_sizes.json")
_LOCK = threading.Lock()


def _load() -> Dict[str, list]:
    """Read the JSON file. Returns empty dict if missing or corrupted."""
    if not os.path.exists(_STORE_PATH):
        return {}
    try:
        with open(_STORE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        return data
    except (OSError, json.JSONDecodeError):
        return {}


def _save(data: Dict[str, list]) -> None:
    """Atomically write the JSON file. Best-effort; silently swallows
    write errors (e.g. read-only filesystem on a locked-down HF Space)."""
    try:
        tmp = _STORE_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, _STORE_PATH)
    except OSError:
        # Filesystem not writable — caller falls back to in-memory state.
        pass


def get_profile(
    display_key: str,
    csv_default: Tuple[int, int, float, float, float],
) -> Tuple[int, int, float, float, float]:
    """Return (h, w, head_ratio, head_height, top_dist) for a size.
    Reads from JSON first, falls back to csv_default."""
    with _LOCK:
        data = _load()
    raw = data.get(display_key)
    if not raw or len(raw) < 5:
        return csv_default
    try:
        return (
            int(raw[0]),
            int(raw[1]),
            float(raw[2]),
            float(raw[3]),
            float(raw[4]),
        )
    except (TypeError, ValueError):
        return csv_default


def set_profile(
    display_key: str,
    h: int,
    w: int,
    head_ratio: float,
    head_height: float,
    top_dist: float,
) -> bool:
    """Persist a custom profile for a size. Returns True if the file
    was actually written (False if filesystem is read-only)."""
    with _LOCK:
        data = _load()
        data[display_key] = [h, w, head_ratio, head_height, top_dist]
        wrote = False
        try:
            _save(data)
            wrote = True
        except Exception:
            pass
        return wrote


def reset_profile(display_key: str) -> bool:
    """Remove the custom override so the size falls back to its CSV
    default. Returns True if the file was actually modified."""
    with _LOCK:
        data = _load()
        if display_key in data:
            del data[display_key]
            _save(data)
            return True
    return False


def has_custom(display_key: str) -> bool:
    with _LOCK:
        data = _load()
    return display_key in data


def list_custom() -> Dict[str, list]:
    """Snapshot of every size that has a custom override."""
    with _LOCK:
        return dict(_load())