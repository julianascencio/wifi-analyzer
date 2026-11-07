"""Offline figures and machine-readable reports without third-party upload."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from .analysis import estimate_grid, summarize
from .survey import Sample


def plot_group(samples: list[Sample], *, radius_m: float = 8) -> Any:
    """Plot observations over an estimated surface; grey means unsupported."""
    xs = [s.x_m for s in samples]
    ys = [s.y_m for s in samples]
    x, y = np.meshgrid(np.linspace(min(xs), max(xs), 101), np.linspace(min(ys), max(ys), 61))
    z = estimate_grid(samples, x, y, radius_m=radius_m)
    fig, ax = plt.subplots(figsize=(10, 5), layout="constrained")
    ax.set_facecolor("#d9dfe5")
    # Degenerate surveys remain point maps, not artificial 2D surfaces.
    if min(xs) != max(xs) and min(ys) != max(ys):
        ax.pcolormesh(x, y, z, cmap="viridis", vmin=-95, vmax=-35, shading="auto")
    points = ax.scatter(
        xs,
        ys,
        c=[s.rssi_dbm for s in samples],
        cmap="viridis",
        vmin=-95,
        vmax=-35,
        edgecolors="white",
        linewidths=0.5,
        s=28,
    )
    first = samples[0]
    ax.set(
        title=f"{first.evidence.upper()} observations | {first.ap_id} | {first.frequency_mhz} MHz"
        f"\n{first.floor}: estimated IDW background; grey = unknown",
        xlabel="Local x (m)",
        ylabel="Local y (m)",
    )
    ax.set_aspect("equal", adjustable="datalim")
    fig.colorbar(points, ax=ax, label="Received signal (dBm)")
    return fig


def make_report(samples: list[Sample], output: Path, *, radius_m: float = 8) -> None:
    output.mkdir(parents=True, exist_ok=True)
    summaries = summarize(samples)
    for row in summaries:
        selected = [
            s
            for s in samples
            if (s.floor, s.ap_id, s.frequency_mhz, s.evidence)
            == (row["floor"], row["ap_id"], row["frequency_mhz"], row["evidence"])
        ]
        # Untrusted labels must never become filesystem paths.
        key = json.dumps([row[k] for k in ("floor", "ap_id", "frequency_mhz", "evidence")])
        filename = "map-" + hashlib.sha256(key.encode()).hexdigest()[:16] + ".png"
        fig = plot_group(selected, radius_m=radius_m)
        fig.savefig(output / filename, dpi=150)
        plt.close(fig)
        row["map"] = filename
    report = {
        "schema_version": "1",
        "radius_m": radius_m,
        "groups": summaries,
        "limitations": [
            "RSSI is not throughput or backhaul quality.",
            "IDW is an estimate; walls and unsampled regions are not resolved.",
            "Sample fractions are not area coverage percentages.",
        ],
    }
    (output / "summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
