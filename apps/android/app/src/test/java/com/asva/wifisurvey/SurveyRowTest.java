package com.asva.wifisurvey;
import org.junit.Test;
import static org.junit.Assert.*;

public class SurveyRowTest {
    @Test public void pseudonymsAreStableOnlyWithinSurvey() {
        String a = SurveyRow.apId("one", "aa:bb:cc:dd:ee:ff");
        assertEquals(a, SurveyRow.apId("one", "aa:bb:cc:dd:ee:ff"));
        assertNotEquals(a, SurveyRow.apId("two", "aa:bb:cc:dd:ee:ff"));
        assertFalse(a.contains("aa:bb"));
    }
    @Test public void csvEscapesUserLabels() {
        String row = SurveyRow.csv("2026-01-01T12:00:00Z", "Room, \"A\"", 1, 2, "ap-1", 2412, -60);
        assertTrue(row.contains("\"Room, \"\"A\"\"\""));
        assertTrue(row.endsWith(",measured,android-wifi-scan-v1\n"));
    }
    @Test(expected = IllegalArgumentException.class) public void invalidPositionRejected() {
        SurveyRow.csv("2026-01-01T12:00:00Z", "ground", Double.NaN, 2, "ap-1", 2412, -60);
    }
    @Test(expected = IllegalArgumentException.class) public void sentinelRssiRejected() {
        SurveyRow.csv("2026-01-01T12:00:00Z", "ground", 1, 2, "ap-1", 2412, 0);
    }
}
