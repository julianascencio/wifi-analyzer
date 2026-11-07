Phone collection
=====================

Why Android first
----------------------
Android exposes nearby access-point RSSI through WifiManager. Ordinary browser
apps do not provide this scan API, so a native collector is included under
``apps/android``. Apple documents that iOS has no general-purpose Wi-Fi scanning
API; an iOS equivalent is not promised.

The initial app uses manual X/Y coordinates because GPS is often unsuitable for
room-scale positioning. It does not auto-discover a floor plan or estimate
position from signal strength. Record one floor/zone at a time with a consistent
origin. Scan while standing still; label another building as a distinct zone
unless its coordinates share the same origin.

Build and install
----------------------
Use JDK 17, Android SDK 35 and Gradle 8.11.1 (AGP 8.9.2)::

    cd apps/android
    gradle :app:testDebugUnitTest :app:lintDebug :app:assembleDebug
    adb install -r app/build/outputs/apk/debug/app-debug.apk

Alternatively download ``wifi-survey-debug-apk`` from the PR's successful
Android workflow, unzip it and install on a test device. This is a development
APK, not a store release. The repo does not contain a Gradle wrapper; CI installs
the specified Gradle version using setup-gradle.

Use
--------
1. Enable Wi-Fi and system Location. Grant **precise location** when requested.
   The OS requires it for scans even though this app does not collect GPS.
2. Enter a floor/zone and X/Y in metres from your chosen origin.
3. Tap Record and stay still. Only successful, fresh observations are saved.
4. Move to another marked point and repeat. Android normally limits foreground
   requests to four scans per two minutes; rejected scans are not fabricated.
5. Export CSV through Android's document picker; move it to your computer.
6. Run ``wifi-analyzer report surveys/wifi-survey.csv``.

Collection is foreground and user-triggered. Going to the background cancels
pending acquisition but preserves saved rows. The app saves privately on device,
with no Internet permission, GPS reads or SSID storage. AP IDs are salted SHA-256
pseudonyms, stable within the stored survey; clearing the survey resets them.
These are not a guarantee of anonymity. A new survey requires a fresh export
before clearing if the old data is needed. Clearing removes the app's copy only,
not previously exported files. No automatic speed test or cloud backend exists.

Physical-device acceptance checklist
-----------------------------------------
* Deny permission: a clear explanation appears without a crash.
* Grant approximate only: precise permission is still requested.
* Disable system Location/Wi-Fi: failed scans do not append cached data.
* Scan at two positions: export includes the entered coordinates and fresh timestamps.
* Trigger throttling: the failure is shown and no fake rows are saved.
* Background/rotate during acquisition: pending scan cancels, saved data survives.
* Close/reopen, export, cancel export, clear survey and repeat.
* Import the CSV on Python and compare AP counts and RSSI with the phone's capture.

These checks require an actual phone and have not been completed by CI.

References
---------------
* `Android scanning and limits <https://developer.android.com/develop/connectivity/wifi/wifi-scan>`_
* `Apple Wi-Fi API overview <https://developer.apple.com/documentation/technotes/tn3111-ios-wifi-api-overview>`_
