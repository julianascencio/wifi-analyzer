from dataclasses import replace

import numpy as np
import pytest

from wifi_analyzer.analysis import estimate_grid, summarize
from wifi_analyzer.survey import Sample


def sample(x=0, y=0, rssi=-50):
    return Sample("2026-01-01T12:00:00Z", "room", x, y, "ap", 2412, rssi, "synthetic", "test")


def test_exact_and_symmetric_idw():
    result = estimate_grid(
        [sample(), sample(2, 0, -70)], np.array([0.0, 1.0, 2.0]), np.zeros(3), radius_m=3
    )
    np.testing.assert_allclose(result, [-50, -60, -70])


def test_repeated_locations_use_median_before_weighting():
    rows = [sample(rssi=-40), sample(rssi=-60), sample(2, 0, -70)]
    result = estimate_grid(rows, np.array([0.0, 1.0]), np.zeros(2), radius_m=3)
    np.testing.assert_allclose(result, [-50, -60])


def test_unknown_outside_radius_or_bounds():
    rows = [sample(), sample(20, 0, -80)]
    result = estimate_grid(rows, np.array([-1.0, 10.0, 21.0]), np.zeros(3), radius_m=2)
    assert np.isnan(result).all()


@pytest.mark.parametrize(
    "changes",
    [{"ap_id": "other"}, {"floor": "upstairs"}, {"frequency_mhz": 5180}, {"evidence": "measured"}],
)
def test_groups_never_mixed(changes):
    rows = [sample(), replace(sample(), **changes)]
    assert len(summarize(rows)) == 2
    with pytest.raises(ValueError, match="select exactly"):
        estimate_grid(rows, np.zeros(1), np.zeros(1))


@pytest.mark.parametrize("radius", [0, -1, float("nan"), float("inf")])
def test_bad_radius(radius):
    with pytest.raises(ValueError):
        estimate_grid([sample()], np.zeros(1), np.zeros(1), radius_m=radius)


def test_summary_threshold_not_area():
    result = summarize([sample(rssi=-75), sample(rssi=-80), sample(rssi=-60)])[0]
    assert result["fraction_samples_below_minus75_dbm"] == 1 / 3
    assert result["median_rssi_dbm"] == -75
    assert result["samples"] == 3
    assert result["positions"] == 1
