"""
Repeated measurements and unsupported regions
==================================================

Synthetic values demonstrate median aggregation and a limited interpolation
radius. The middle gap stays unknown, even though two sides were surveyed.
Duplicate positions are aggregated before interpolation so repeatedly sampling
one location cannot overwhelm nearby positions solely through sample count.
"""

import matplotlib.pyplot as plt

from wifi_analyzer.report import plot_group
from wifi_analyzer.survey import Sample

samples = [
    Sample(
        "2026-01-01T12:00:00Z",
        "room",
        x,
        y,
        "demo-ap",
        2412,
        level,
        "synthetic",
        "illustrative-repeats",
    )
    for x, y, level in [(0, 0, -50), (0, 0, -60), (0, 5, -60), (25, 0, -80), (25, 5, -85)]
]
plot_group(samples, radius_m=6)
plt.show()
