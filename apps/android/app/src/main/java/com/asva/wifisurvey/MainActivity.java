package com.asva.wifisurvey;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.SystemClock;
import android.text.InputType;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.UUID;

/** Foreground, user-triggered survey. Never labels cached scans as new samples. */
public class MainActivity extends Activity {
    private WifiManager wifi;
    private TextView status;
    private EditText floor, x, y;
    private Button scan;
    private boolean pending;
    private long requestedMicros;
    private double scanX, scanY;
    private String scanFloor;
    private final Handler handler = new Handler(Looper.getMainLooper());
    private final Runnable timeout = () -> finishScan("Scan timed out. No samples recorded. Try later.");
    private File survey;
    private SharedPreferences prefs;

    private final BroadcastReceiver receiver = new BroadcastReceiver() {
        @Override public void onReceive(Context context, Intent intent) {
            if (!pending || !WifiManager.SCAN_RESULTS_AVAILABLE_ACTION.equals(intent.getAction())) return;
            if (!intent.getBooleanExtra(WifiManager.EXTRA_RESULTS_UPDATED, false)) {
                finishScan("Scan failed or throttled. No cached results recorded.");
                return;
            }
            try {
                if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                    finishScan("Location permission was revoked. No samples recorded."); return;
                }
                StringBuilder rows = new StringBuilder();
                int count = 0;
                long nowMicros = SystemClock.elapsedRealtimeNanos() / 1000;
                for (ScanResult result : wifi.getScanResults()) {
                    if (result.timestamp < requestedMicros || result.timestamp > nowMicros
                            || result.BSSID == null || result.BSSID.isEmpty()
                            || result.level >= 0 || result.level < -127
                            || result.frequency < 2300 || result.frequency > 7125) continue;
                    String id = SurveyRow.apId(prefs.getString("salt", ""), result.BSSID);
                    String measuredAt = Instant.now().minusMillis((nowMicros - result.timestamp) / 1000).toString();
                    rows.append(SurveyRow.csv(measuredAt, scanFloor, scanX, scanY,
                                             id, result.frequency, result.level));
                    count++;
                }
                if (count > 0) {
                    boolean header = !survey.exists() || survey.length() == 0;
                    try (FileOutputStream out = new FileOutputStream(survey, true)) {
                        if (header) out.write(SurveyRow.HEADER.getBytes(StandardCharsets.UTF_8));
                        out.write(rows.toString().getBytes(StandardCharsets.UTF_8));
                    }
                }
                finishScan("Saved " + count + " fresh AP observations at (" + scanX + ", " + scanY
                    + "). Move to the next point. Export CSV when finished.");
            } catch (SecurityException e) {
                finishScan("Grant precise location permission and enable system Location and Wi-Fi.");
            } catch (IOException e) {
                finishScan("Could not save survey: " + e.getMessage());
            }
        }
    };

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        wifi = (WifiManager) getApplicationContext().getSystemService(WIFI_SERVICE);
        survey = new File(getFilesDir(), "survey.csv");
        prefs = getSharedPreferences("survey", MODE_PRIVATE);
        if (!prefs.contains("salt")) prefs.edit().putString("salt", UUID.randomUUID().toString()).apply();
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(32, 40, 32, 32);
        layout.setOnApplyWindowInsetsListener((v, insets) -> {
            v.setPadding(32, 32 + insets.getSystemWindowInsetTop(), 32, 32 + insets.getSystemWindowInsetBottom());
            return insets;
        });
        TextView heading = new TextView(this);
        heading.setText("Wi-Fi Survey • ASVA\n\nEnter a position in metres from a fixed origin on your plan. "
            + "Stay still during each scan. Position is manual; this app does not map rooms automatically.\n\n"
            + "Precise location permission and system Location are required by Android for Wi-Fi scanning. "
            + "No GPS is collected. No Internet permission or cloud upload. AP identifiers are salted pseudonyms; "
            + "SSID names are not stored. CSV still contains sensitive positions.\n");
        layout.addView(heading);
        floor = field(layout, "Floor / zone", prefs.getString("floor", "ground"), false);
        x = field(layout, "X (metres)", prefs.getString("x", "0"), true);
        y = field(layout, "Y (metres)", prefs.getString("y", "0"), true);
        scan = button(layout, "Record this position", v -> requestScan());
        button(layout, "Export CSV", v -> {
            if (!survey.exists()) { status.setText("Record a scan first."); return; }
            Intent save = new Intent(Intent.ACTION_CREATE_DOCUMENT);
            save.addCategory(Intent.CATEGORY_OPENABLE);
            save.setType("text/csv");
            save.putExtra(Intent.EXTRA_TITLE, "wifi-survey.csv");
            startActivityForResult(save, 2);
        });
        button(layout, "New survey / clear stored data", v -> new AlertDialog.Builder(this)
            .setMessage("Delete stored measurements and reset AP pseudonyms? Export first to keep them.")
            .setNegativeButton("Cancel", null)
            .setPositiveButton("Clear", (dialog, which) -> {
                finishScan("Starting a new survey.");
                if (survey.exists() && !survey.delete()) { status.setText("Could not delete survey."); return; }
                prefs.edit().putString("salt", UUID.randomUUID().toString()).apply();
                status.setText("Stored measurements deleted. New AP pseudonyms will be used.");
            }).show());
        status = new TextView(this);
        status.setText("Ready. Android normally permits four foreground scans per two minutes. "
            + "Existing observations survive closing the app.");
        layout.addView(status);
        ScrollView scroll = new ScrollView(this);
        scroll.addView(layout);
        setContentView(scroll);
    }

    private EditText field(LinearLayout layout, String label, String value, boolean numeric) {
        TextView name = new TextView(this); name.setText(label); layout.addView(name);
        EditText input = new EditText(this); input.setText(value); input.setContentDescription(label);
        input.setSingleLine(true);
        if (numeric) input.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_FLAG_DECIMAL | InputType.TYPE_NUMBER_FLAG_SIGNED);
        layout.addView(input); return input;
    }
    private Button button(LinearLayout layout, String title, View.OnClickListener listener) {
        Button b = new Button(this); b.setText(title); b.setOnClickListener(listener); layout.addView(b); return b;
    }
    @Override protected void onStart() {
        super.onStart();
        // This receiver is exclusively for a protected system broadcast.
        registerReceiver(receiver, new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
    }
    @Override protected void onStop() {
        finishScan("Paused. Any pending scan was cancelled; recorded data remains saved.");
        prefs.edit().putString("floor", floor.getText().toString()).putString("x", x.getText().toString())
            .putString("y", y.getText().toString()).apply();
        unregisterReceiver(receiver);
        super.onStop();
    }
    private void finishScan(String message) {
        pending = false; handler.removeCallbacks(timeout); scan.setEnabled(true); status.setText(message);
    }
    @SuppressWarnings("deprecation")
    private void requestScan() {
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, 1);
            status.setText("Grant precise location, then tap Record again. System Location must also be enabled.");
            return;
        }
        try {
            scanX = Double.parseDouble(x.getText().toString());
            scanY = Double.parseDouble(y.getText().toString());
            scanFloor = floor.getText().toString().trim();
            if (!Double.isFinite(scanX) || !Double.isFinite(scanY) || scanFloor.isEmpty()) throw new NumberFormatException();
        } catch (NumberFormatException e) { status.setText("Enter a floor and finite X/Y coordinates in metres."); return; }
        requestedMicros = SystemClock.elapsedRealtimeNanos() / 1000;
        pending = true; scan.setEnabled(false);
        try {
            if (!wifi.startScan()) { finishScan("Scan rejected: enable Wi-Fi/Location or wait for throttling to clear."); return; }
            status.setText("Scanning. Stay at this position…");
            handler.postDelayed(timeout, 15000);
        } catch (SecurityException e) { finishScan("Precise location permission and system Location are required."); }
    }
    @Override protected void onActivityResult(int request, int result, Intent data) {
        super.onActivityResult(request, result, data);
        if (request != 2 || result != RESULT_OK || data == null || data.getData() == null) return;
        try (FileInputStream input = new FileInputStream(survey);
             OutputStream output = getContentResolver().openOutputStream(data.getData())) {
            if (output == null) throw new IOException("No output stream");
            byte[] buffer = new byte[8192]; int n;
            while ((n = input.read(buffer)) != -1) output.write(buffer, 0, n);
            status.setText("CSV exported. On your computer run: wifi-analyzer report wifi-survey.csv");
        } catch (IOException | SecurityException e) { status.setText("Export failed: " + e.getMessage()); }
    }
}
