Roadmap
============

Implemented foundation
---------------------------
Versioned CSV, native Android foreground survey, offline Python analysis,
AP-specific maps, synthetic gallery, reproducible checks and optional Pages.

Next: field-validated coverage
-----------------------------------
Collect a real 50 m survey; compare repeated observations with one device,
record plan coordinates and label the main router/extenders. Add floor-plan
alignment, surveyed polygons, explicit obstacles and interpolation validation
against held-out positions. Add AP selection and maps inside the phone app.

Next: connection reliability
---------------------------------
Add explicit local-gateway latency/loss and controlled LAN throughput probes.
Record whether traffic uses Wi-Fi or cellular. Keep RF strength, LAN quality,
Internet service quality and extender upstream telemetry as distinct quantities.
Add supported router connectors only after their actual APIs are identified.

Research track: CSI sensing
--------------------------------
Add hardware capability discovery, licensed datasets, calibration protocols and
reproducible baselines before interpreting CSI. Treat presence/motion sensing,
localization and 3D geometry reconstruction as different problems. No claim of
LiDAR-quality maps or generic-router support is made by this roadmap.
