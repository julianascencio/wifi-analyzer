Methods, evidence and limitations
======================================

Received power
-------------------
RSSI is the receiver's reported power estimate in dBm. Android's ScanResult.level
uses these units. Devices have different calibration, antenna patterns and
orientations: compare surveys with the same device and a consistent posture.
No instrument calibration has been performed for this project.

The summary reports minimum, maximum and median observed RSSI, sample count,
unique-position count and fraction of samples below -75 dBm. This threshold is
an illustrative screening value, not a universal service requirement. Sample
fractions are not percentages of property area. Repeated scans affect summary
statistics; the map first collapses repeats at each position to their median.

Spatial estimates
----------------------
For a selected floor, AP, centre frequency and evidence type, the map estimates
RSSI in logarithmic dBm space using inverse-distance weights:

.. math::

   \hat r(x) = \frac{\sum_i r_i / d_i^2}{\sum_i 1 / d_i^2}

Only observations within a user-selected radius (default 8 m) contribute. An
exact observation location returns its median. Outside the coordinate bounding
box or without any neighbour inside the radius the result is unknown (grey).
This is a descriptive visual interpolation choice, not a physical power sum.
The bounding box is not a surveyed polygon: unsampled holes within the radius
can still receive estimates. There is no wall-aware masking or uncertainty
interval. Narrow/collinear surveys cannot establish two-dimensional coverage.
For single-axis surveys the report renders observation points only.

Synthetic 50 m case
------------------------
The four source locations, -38 dBm reference, exponent 2.4 and 12 dB obstacle
penalty are arbitrary illustrative assumptions. There is no measured wall loss,
calibrated antenna pattern, simulated airtime or extender backhaul model. The
case demonstrates analysis mechanics, not expected real-world performance.

What these data cannot establish
-------------------------------------
RSSI alone cannot quantify throughput, packet loss, interference/channel load,
noise floor, roaming reliability or the extender's upstream link. Absence from
a scan is not recorded as zero power or proven disconnection. Map each AP
separately; the strongest advertised signal need not deliver the best Internet.
CSI sensing needs compatible hardware, firmware and a separate validated model;
this project does not implement human tracking or room reconstruction.

Sources
------------
* `Android ScanResult reference <https://developer.android.com/reference/android/net/wifi/ScanResult>`_
  defines the received-power level, frequency and monotonic observation timestamp.
* `Android Wi-Fi scanning overview <https://developer.android.com/develop/connectivity/wifi/wifi-scan>`_
  documents permissions, freshness and throttling.
* `NIST Wi-Fi sensing research <https://www.nist.gov/publications/ieee-80211bf-enabling-widespread-adoption-wi-fi-sensing>`_
  describes sensing as a separate use of wireless measurements.

Validation status
----------------------
Automated tests check schema rejection, CSV interoperability, group isolation,
exact-position and symmetric IDW cases, duplicate handling, unknown regions and
end-to-end CLI behavior. Android CI compiles the app and checks lint/serialization.
No on-site measurements, RF calibration or physical-phone acceptance results
are supplied in this initial version. AI assisted development; inspect evidence
and validate on your own hardware before relying on conclusions.
