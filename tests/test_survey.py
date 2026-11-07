from dataclasses import replace

import pytest

from wifi_analyzer.demo import demo_samples
from wifi_analyzer.survey import FIELDS, read_csv, write_csv


def test_roundtrip_preserves_quoted_labels_and_evidence(tmp_path):
    samples = [replace(demo_samples()[0], floor='Room, "A"\nupstairs')]
    path = tmp_path / "survey.csv"
    write_csv(samples, path)
    assert read_csv(path) == samples


@pytest.mark.parametrize(
    "changes",
    [
        {"rssi_dbm": 0},
        {"rssi_dbm": -128},
        {"x_m": float("nan")},
        {"y_m": float("inf")},
        {"evidence": "real-ish"},
        {"schema_version": "2"},
        {"floor": " "},
        {"frequency_mhz": 0},
        {"timestamp_utc": "2026-01-01T12:00:00"},
        {"timestamp_utc": "2026-01-01T12:00:00+01:00"},
    ],
)
def test_invalid_samples_rejected(changes):
    with pytest.raises(ValueError):
        replace(demo_samples()[0], **changes)


def test_android_export_contract(tmp_path):
    # Same numeric/quoted serialization used by SurveyRow.java.
    path = tmp_path / "android.csv"
    path.write_text(
        ",".join(FIELDS)
        + "\n"
        + '1,"2026-01-01T12:00:00Z","Room, ""A""",1.0,2.0,"ap-1",2412,-60,measured,android-wifi-scan-v1\n'
    )
    sample = read_csv(path)[0]
    assert (sample.floor, sample.x_m, sample.rssi_dbm, sample.evidence) == (
        'Room, "A"',
        1,
        -60,
        "measured",
    )


@pytest.mark.parametrize(
    "body",
    [
        "",
        ",".join(FIELDS) + "\n",
        ",".join(FIELDS) + "\n1,2026-01-01T12:00:00Z,ground,nan,0,ap,2412,-60,measured,phone\n",
        ",".join(FIELDS) + "\n1,2026-01-01T12:00:00Z,ground,0,0,ap,2412,-60,measured\n",
    ],
)
def test_invalid_csv_fails_closed(tmp_path, body):
    path = tmp_path / "invalid.csv"
    path.write_text(body)
    with pytest.raises(ValueError):
        read_csv(path)
