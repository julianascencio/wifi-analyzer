Quick start
================

From a checkout, install Python 3.11 or newer and run::

    python -m pip install -e '.[dev,docs]'
    wifi-analyzer demo --output outputs/demo

Inspect ``summary.json`` and its linked PNG files. All demo observations are
synthetic. To use your own data, follow the Android collection guide and run::

    wifi-analyzer report surveys/wifi-survey.csv --output outputs/survey

The CSV's exact columns, in order, are::

    schema_version,timestamp_utc,floor,x_m,y_m,ap_id,frequency_mhz,rssi_dbm,evidence,source

Example illustrative row (not a real measurement)::

    1,2026-01-01T12:00:00Z,ground,5,10,demo-ap,2412,-65,synthetic,manual-example

Use schema version ``1``, UTC timestamps with an offset or Z, local coordinates
in metres relative to a documented origin, RSSI in dBm, and centre frequency in
MHz. Evidence must be ``measured`` or ``synthetic``. Measured means an observation,
not independently calibrated truth. Source identifies the acquisition method.
Empty input, missing columns, nonfinite values and zero RSSI are rejected.
Positions must share one coordinate origin per floor/zone and survey; do not
merge independently positioned surveys without explicit coordinate alignment.

Keep private surveys in the ignored ``surveys/`` directory. Exported positions
and pseudonyms may identify a property: do not publish them by default.
