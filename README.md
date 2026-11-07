# Wi-Fi Analyzer

**Created by [ASVA Consulting](https://asvaconsulting.com)** · Source-available, noncommercial

Reproducible Wi-Fi received-power surveys, analysis and maps. Inspired by
[OrbitalPV](https://github.com/julianascencio/orbital-pv): a modular Python library,
runnable examples, a Sphinx/PyData gallery, explicit evidence and automated checks.

## First working workflow

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e '.[dev,docs]'
wifi-analyzer demo --output outputs/demo
# After exporting a real survey from the Android app:
wifi-analyzer report surveys/wifi-survey.csv --output outputs/my-survey --radius-m 8
```

The demo writes a **synthetic** 50 m property survey, four PNG maps and a JSON
summary linking each AP to its map. It models one router and three extenders only
as illustrative signal sources. It is not a measurement of any actual property.
No network connection, router credentials or hardware is needed for the demo.

## Android companion included

[`apps/android`](apps/android/README.md) is a native Android 8+ survey collector.
Enter floor/zone and local X/Y coordinates, record a fresh scan, then export CSV.
The app keeps observations locally between launches. It has no Internet permission,
stores no SSID names, and uses salted AP pseudonyms. Review exports before sharing:
positions and pseudonyms remain potentially sensitive.

The `Android` CI job builds a debug APK artifact and runs lint and JVM tests.
Physical-phone acceptance checks are documented; hardware behavior is not verified
by those checks. No Play Store release is claimed. iOS and automatic positioning
are not implemented.

## What it does / limits

- Strict versioned CSV import/export with UTC time, position, AP, frequency, RSSI and provenance.
- Summary statistics separated by floor, AP, frequency and measured/synthetic evidence.
- Sample maps with bounded inverse-distance interpolation; repeated positions use median RSSI.
- Two offline runnable gallery examples, CLI and a documented Python API.
- Android user-triggered scans with permission, throttling, freshness and export handling.

RSSI is received power in dBm, **not Mbps, transmit power or backhaul quality**.
Nearby AP scan results do not prove a device was connected to that AP. No speed,
packet-loss, noise-floor, channel-utilization or extender-uplink measurements are
invented from RSSI. Interpolation does not discover walls or guarantee coverage.
Wi-Fi CSI sensing and LiDAR-like reconstruction are separate future research work.

## Structure

| Path | Purpose |
|---|---|
| `src/wifi_analyzer/` | Survey schema, analytics, mapping, CLI |
| `apps/android/` | Native survey acquisition and CSV export |
| `examples/` | Runnable, documented gallery cases |
| `tests/` | Schema, numerical, isolation and CLI regression tests |
| `docs/` | Methods, limitations, mobile workflow, API and roadmap |
| `.github/workflows/` | Python, Android, documentation and optional Pages checks |

## Development and gallery

```bash
ruff check .
ruff format --check .
mypy src/wifi_analyzer
pytest
python -m build
MPLBACKEND=Agg sphinx-build -W --keep-going -b html docs docs/_build/html
```

Open `docs/_build/html/index.html`. The documentation workflow uploads a preview
artifact for PRs. After merge, enable GitHub Pages with **GitHub Actions** as its
source and set repository variable `ENABLE_PAGES=true` to opt into deployment.
No Pages configuration or published package is assumed.

## Evidence and licensing

AI assisted this implementation. Tests establish software behavior, not field
accuracy. Synthetic demos and measured observations are kept distinct. See
[methods](docs/methods.rst), [mobile](docs/mobile.rst), and [roadmap](docs/roadmap.rst).

Original code and docs use the same **ASVA Noncommercial Software License 1.0**
as the reference repository. Commercial use requires separate written permission.
This is source-available, not OSI open source. Dependencies and third-party
materials retain their own terms. See [LICENSE](LICENSE) and [LICENSING.md](LICENSING.md).
