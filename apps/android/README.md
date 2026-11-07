# Android survey collector

Native Java Android app for user-triggered RSSI surveys. Android 8+; SDK 35,
JDK 17, Gradle 8.11.1 and Android Gradle Plugin 8.9.2.

```bash
cd apps/android
gradle :app:testDebugUnitTest :app:lintDebug :app:assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Open this directory in Android Studio or use the pinned Gradle version above.
No wrapper is included. The GitHub Actions Android job builds a debug APK artifact.
See [the complete phone guide](../../docs/mobile.rst) for permissions, survey
steps, exports, privacy behavior and physical-device acceptance checks.

Manual coordinates are required. Wi-Fi sensing, floor-plan reconstruction,
background recording and on-phone heatmaps are not implemented. Automated build
and JVM checks do not establish real-device radio behavior.
