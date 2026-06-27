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
# We try several paths in priority order so the data persists across HF
# Space rebuilds whenever a persistent volume is available:
#   1. /data   — HF Spaces persistent storage mount (set via Space settings
#                → Storage → connect a Dataset). Survives every rebuild.
#   2. HF_HOME / XDG_CACHE_HOME — Gradio's writable home (may persist
#                depending on Space config).
#   3. demo/custom_sizes.json  — fallback that lives inside the git repo;
#                survives only if the user commits it manually.
#   4. /tmp     — last-resort scratch (lost on rebuild, only good for
#                the current session).
def _candidate_paths():
    paths = []
    # 1. HF Space persistent storage (the one we really want)
    if os.path.isdir("/data"):
        paths.append("/data/custom_sizes.json")
    # 2. Writable home cache
    home = os.environ.get("HF_HOME") or os.path.expanduser("~/.cache/huggingface")
    if home and os.access(os.path.dirname(home) or home, os.W_OK):
        paths.append(os.path.join(home, "retoka_custom_sizes.json"))
    # 3. Local file (committed in git; safe across same commit, not across rebuilds)
    paths.append(_STORE_PATH)
    # 4. tmpfs fallback (session-only)
    paths.append("/tmp/retoka_custom_sizes.json")
    return paths

_STORE_PATH = os.path.join(_HERE, "custom_sizes.json")
_LOCK = threading.Lock()
_ACTIVE_PATH = None  # set on first successful load/write

# Bump this whenever the defaults in ``demo/assets/size_list_ES.csv`` change.
# Any stored overrides that don't match this version are silently discarded
# on next read, so the new CSV defaults take effect immediately after deploy.
CSV_VERSION = 5


def _resolve_path() -> str:
    """Pick the first candidate path we can actually write to.
    Caches the result in module state so we don't re-probe every call."""
    global _ACTIVE_PATH
    if _ACTIVE_PATH is not None:
        return _ACTIVE_PATH
    for path in _candidate_paths():
        parent = os.path.dirname(path)
        try:
            os.makedirs(parent, exist_ok=True)
            # Probe writability with a touch
            with open(path, "a"):
                pass
            _ACTIVE_PATH = path
            return path
        except OSError:
            continue
    # Last-resort: in-process dict; nothing persistent but at least no crash
    _ACTIVE_PATH = None
    return None


def _load() -> Dict[str, list]:
    """Read the JSON file from the first available persistent path.
    Returns empty dict if no path is writable, or if the stored version
    doesn't match ``CSV_VERSION`` (in which case stored overrides are
    discarded so the latest CSV defaults take effect)."""
    path = _resolve_path()
    if path is None or not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        # Version check: if the file was written with an older CSV_VERSION
        # we silently drop it so new CSV defaults win. This makes deploys of
        # updated defaults work without manual intervention.
        if data.get("__version__", 0) != CSV_VERSION:
            return {}
        return data
    except (OSError, json.JSONDecodeError):
        return {}


def _save(data: Dict[str, list]) -> bool:
    """Atomically write the JSON file to the first available persistent
    path. Returns True on success, False if no writable path exists.
    Always stamps the current ``CSV_VERSION`` into the file so future
    version mismatches can be detected."""
    path = _resolve_path()
    if path is None:
        return False
    try:
        payload = dict(data)
        payload["__version__"] = CSV_VERSION
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
        return True
    except OSError:
        return False


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
    was actually written to a persistent path (False if no writable
    path exists on this deployment)."""
    with _LOCK:
        data = _load()
        data[display_key] = [h, w, head_ratio, head_height, top_dist]
        return _save(data)


def reset_profile(display_key: str) -> bool:
    """Remove the custom override so the size falls back to its CSV
    default. Returns True if the file was actually modified."""
    with _LOCK:
        data = _load()
        if display_key in data:
            del data[display_key]
            return _save(data)
    return False


def has_custom(display_key: str) -> bool:
    with _LOCK:
        data = _load()
    return display_key in data


def list_custom() -> Dict[str, list]:
    """Snapshot of every size that has a custom override."""
    with _LOCK:
        return dict(_load())


def active_path() -> str:
    """Which storage path the next read/write will hit. Useful for
    diagnostics in the UI (showing the user where their data lives)."""
    return _resolve_path() or "(no writable path found)"