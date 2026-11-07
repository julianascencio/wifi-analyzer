"""Descriptive statistics and explicitly estimated, bounded spatial interpolation."""

from __future__ import annotations

import math
from collections import defaultdict
from statistics import median
from typing import Any

import numpy as np
import numpy.typing as npt

from .survey import Sample

Array = npt.NDArray[np.float64]


def _group(sample: Sample) -> tuple[str, str, int, str]:
    return sample.floor, sample.ap_id, sample.frequency_mhz, sample.evidence


def summarize(samples: list[Sample]) -> list[dict[str, Any]]:
    """Summaries per floor/AP/frequency/evidence, never a speed prediction."""
    grouped: dict[tuple[str, str, int, str], list[Sample]] = defaultdict(list)
    for sample in samples:
        grouped[_group(sample)].append(sample)
    return [
        {
            "floor": key[0],
            "ap_id": key[1],
            "frequency_mhz": key[2],
            "evidence": key[3],
            "samples": len(rows),
            "positions": len({(s.x_m, s.y_m) for s in rows}),
            "median_rssi_dbm": median(s.rssi_dbm for s in rows),
            "min_rssi_dbm": min(s.rssi_dbm for s in rows),
            "max_rssi_dbm": max(s.rssi_dbm for s in rows),
            "fraction_samples_below_minus75_dbm": sum(s.rssi_dbm < -75 for s in rows) / len(rows),
        }
        for key, rows in sorted(grouped.items())
    ]


def estimate_grid(samples: list[Sample], x: Array, y: Array, *, radius_m: float = 8) -> Array:
    """IDW (power=2) in dBm. Median repeats first; unknown outside radius/bounds.

    This is visual interpolation, not a propagation model, wall detector or area
    coverage guarantee. Input must be one floor, AP, frequency and evidence type.
    """
    if not samples or len({_group(s) for s in samples}) != 1:
        raise ValueError("select exactly one floor/AP/frequency/evidence group")
    if x.shape != y.shape or not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("grid coordinates must be finite with matching shapes")
    if not math.isfinite(radius_m) or radius_m <= 0:
        raise ValueError("radius_m must be positive and finite")
    locations: dict[tuple[float, float], list[float]] = defaultdict(list)
    for s in samples:
        locations[s.x_m, s.y_m].append(s.rssi_dbm)
    points = np.array(list(locations), dtype=float)
    values = np.array([median(v) for v in locations.values()])
    result = np.full(x.shape, np.nan, dtype=float)
    for index in np.ndindex(x.shape):
        px, py = x[index], y[index]
        if not (
            points[:, 0].min() <= px <= points[:, 0].max()
            and points[:, 1].min() <= py <= points[:, 1].max()
        ):
            continue
        distance = np.hypot(points[:, 0] - px, points[:, 1] - py)
        exact = distance == 0
        nearby = distance <= radius_m
        if exact.any():
            result[index] = values[exact][0]
        elif nearby.any():
            weights = 1 / distance[nearby] ** 2
            result[index] = np.dot(values[nearby], weights) / weights.sum()
    return result
