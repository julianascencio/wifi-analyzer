"""Deterministic illustrative 50 m survey; never presented as finca measurements."""

import math

from .survey import Sample


def demo_samples() -> list[Sample]:
    samples = []
    for ap_id, ax, ay in (
        ("router", 0, 10),
        ("extender-1", 18, 5),
        ("extender-2", 32, 15),
        ("extender-3", 48, 10),
    ):
        for x in range(0, 51, 5):
            for y in range(0, 21, 5):
                distance = max(1, math.hypot(x - ax, y - ay))
                # Illustrative log-distance curve and arbitrary obstacle loss.
                loss = 12 if (x > 25) != (ax > 25) else 0
                rssi = max(-110, -38 - 24 * math.log10(distance) - loss)
                samples.append(
                    Sample(
                        "2026-01-01T12:00:00Z",
                        "outdoor",
                        x,
                        y,
                        ap_id,
                        5180,
                        rssi,
                        "synthetic",
                        "demo-log-distance-v1",
                    )
                )
    return samples
