"""Versioned CSV contract shared by the Android collector and Python tools."""

from __future__ import annotations

import csv
import math
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

FIELDS = (
    "schema_version",
    "timestamp_utc",
    "floor",
    "x_m",
    "y_m",
    "ap_id",
    "frequency_mhz",
    "rssi_dbm",
    "evidence",
    "source",
)


@dataclass(frozen=True)
class Sample:
    timestamp_utc: str
    floor: str
    x_m: float
    y_m: float
    ap_id: str
    frequency_mhz: int
    rssi_dbm: float
    evidence: str
    source: str
    schema_version: str = "1"

    def __post_init__(self) -> None:
        if self.schema_version != "1":
            raise ValueError("unsupported schema_version")
        timestamp = datetime.fromisoformat(self.timestamp_utc.replace("Z", "+00:00"))
        offset = timestamp.utcoffset()
        if offset is None or offset.total_seconds() != 0:
            raise ValueError("timestamp_utc must have a UTC offset")
        if not all(math.isfinite(v) for v in (self.x_m, self.y_m, self.rssi_dbm)):
            raise ValueError("coordinates and RSSI must be finite")
        if not -127 <= self.rssi_dbm < 0:
            raise ValueError("RSSI must be in [-127, 0) dBm; zero is not a measurement")
        if not 2300 <= self.frequency_mhz <= 7125:
            raise ValueError("only 2.4/5/6 GHz survey frequencies are supported")
        if not all(v.strip() for v in (self.floor, self.ap_id, self.source)):
            raise ValueError("floor, ap_id and source are required")
        if self.evidence not in {"measured", "synthetic"}:
            raise ValueError("evidence must be measured or synthetic")


def read_csv(path: str | Path) -> list[Sample]:
    """Read strict schema v1; do not silently drop invalid observations."""
    samples = []
    with Path(path).open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != list(FIELDS):
            raise ValueError(f"expected CSV columns in order: {','.join(FIELDS)}")
        for line, row in enumerate(reader, 2):
            try:
                if None in row or any(v is None for v in row.values()):
                    raise ValueError("wrong number of columns")
                samples.append(
                    Sample(
                        timestamp_utc=row["timestamp_utc"],
                        floor=row["floor"],
                        x_m=float(row["x_m"]),
                        y_m=float(row["y_m"]),
                        ap_id=row["ap_id"],
                        frequency_mhz=int(row["frequency_mhz"]),
                        rssi_dbm=float(row["rssi_dbm"]),
                        evidence=row["evidence"],
                        source=row["source"],
                        schema_version=row["schema_version"],
                    )
                )
            except (ValueError, TypeError) as exc:
                raise ValueError(f"{path}: row {line}: {exc}") from exc
    if not samples:
        raise ValueError("survey contains no samples")
    return samples


def write_csv(samples: list[Sample], path: str | Path) -> None:
    with Path(path).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(asdict(sample) for sample in samples)
