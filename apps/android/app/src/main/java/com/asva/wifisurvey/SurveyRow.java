package com.asva.wifisurvey;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/** Pure Java CSV contract; identifiers are pseudonyms, not anonymity guarantees. */
public final class SurveyRow {
    public static final String HEADER = "schema_version,timestamp_utc,floor,x_m,y_m,ap_id,frequency_mhz,rssi_dbm,evidence,source\n";
    private SurveyRow() { }

    public static String apId(String salt, String bssid) {
        try {
            byte[] hash = MessageDigest.getInstance("SHA-256").digest(
                (salt + ":" + bssid).getBytes(StandardCharsets.UTF_8));
            StringBuilder result = new StringBuilder("ap-");
            for (byte b : hash) result.append(String.format(java.util.Locale.ROOT, "%02x", b & 255));
            return result.toString();
        } catch (NoSuchAlgorithmException e) { throw new IllegalStateException(e); }
    }

    private static String quoted(String value) {
        return "\"" + value.replace("\"", "\"\"") + "\"";
    }

    public static String csv(String time, String floor, double x, double y,
                             String ap, int frequency, int rssi) {
        if (!Double.isFinite(x) || !Double.isFinite(y) || floor.trim().isEmpty()
                || rssi >= 0 || rssi < -127 || frequency < 2300 || frequency > 7125) {
            throw new IllegalArgumentException("Invalid survey observation");
        }
        return "1," + quoted(time) + "," + quoted(floor) + "," + x + "," + y + ","
            + quoted(ap) + "," + frequency + "," + rssi + ",measured,android-wifi-scan-v1\n";
    }
}
