# Contributor guidance

Keep domain validation, acquisition, analysis and presentation separate. Read the
README and docs/methods.rst before extending numerical methods. Preserve schema
compatibility or explicitly version it. Never commit private surveys, SSIDs,
raw BSSIDs, credentials or real property coordinates to examples.

Every new method needs an evidence/assumptions section, meaningful tests and a
runnable example where useful. Label synthetic, measured and estimated values.
Do not infer Mbps, wall geometry or CSI from ordinary RSSI. Do not combine floors,
APs, frequencies or evidence classes silently. Run Ruff, mypy, pytest, package and
Sphinx builds; Android changes also need lint, JVM tests and an APK build.
Keep PRs focused and leave them open for review unless asked to merge.
