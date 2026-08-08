package org.ytprime.ytprime;

import android.content.Context;
import android.content.SharedPreferences;
import android.net.Uri;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Local watch history. Stores every video the user opens in the WebView
 * (id, url, page title, timestamp) in SharedPreferences as JSON, newest
 * first, deduplicated by video id.
 */
public class HistoryStore {

    private static final String PREFS = "ytprime_history";
    private static final String KEY = "items";
    private static final int MAX_ITEMS = 200;

    private final SharedPreferences prefs;

    public static final class Entry {
        public final String id;
        public final String url;
        public final String title;
        public final long ts;

        Entry(String id, String url, String title, long ts) {
            this.id = id;
            this.url = url;
            this.title = title;
            this.ts = ts;
        }
    }

    public HistoryStore(Context context) {
        prefs = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
    }

    public void add(String url, String title) {
        String id = videoIdFromUrl(url);
        if (id == null) {
            return;
        }
        Map<String, Entry> map = loadMap();
        map.put(id, new Entry(id, url, cleanTitle(title), System.currentTimeMillis()));
        List<Entry> list = new ArrayList<>(map.values());
        list.sort((a, b) -> Long.compare(b.ts, a.ts));
        while (list.size() > MAX_ITEMS) {
            list.remove(list.size() - 1);
        }
        save(list);
    }

    public List<Entry> list() {
        List<Entry> list = new ArrayList<>(loadMap().values());
        list.sort((a, b) -> Long.compare(b.ts, a.ts));
        return list;
    }

    public void clear() {
        prefs.edit().remove(KEY).apply();
    }

    private Map<String, Entry> loadMap() {
        Map<String, Entry> map = new LinkedHashMap<>();
        try {
            JSONArray arr = new JSONArray(prefs.getString(KEY, "[]"));
            for (int i = 0; i < arr.length(); i++) {
                JSONObject o = arr.getJSONObject(i);
                map.put(o.getString("id"), new Entry(
                        o.getString("id"),
                        o.optString("url"),
                        o.optString("title", "Untitled"),
                        o.optLong("ts")));
            }
        } catch (Exception ignored) {
            // corrupted storage -> start over
        }
        return map;
    }

    private void save(List<Entry> list) {
        JSONArray arr = new JSONArray();
        for (Entry e : list) {
            try {
                JSONObject o = new JSONObject();
                o.put("id", e.id);
                o.put("url", e.url);
                o.put("title", e.title);
                o.put("ts", e.ts);
                arr.put(o);
            } catch (Exception ignored) {
                // skip entry
            }
        }
        prefs.edit().putString(KEY, arr.toString()).apply();
    }

    static String videoIdFromUrl(String url) {
        try {
            Uri uri = Uri.parse(url);
            String host = uri.getHost();
            String path = uri.getPath();
            String v = uri.getQueryParameter("v");
            if ("youtu.be".equals(host) && path != null && path.length() > 1) {
                return path.substring(1);
            }
            if (v != null && !v.isEmpty()) {
                return v;
            }
            if (path != null && path.startsWith("/shorts/") && path.length() > 8) {
                return path.substring(8);
            }
        } catch (Exception ignored) {
            // not a URL
        }
        return null;
    }

    static String cleanTitle(String title) {
        if (title == null) {
            return "Untitled";
        }
        String s = title.trim();
        if (s.endsWith(" - YouTube")) {
            s = s.substring(0, s.length() - " - YouTube".length());
        }
        return s.isEmpty() ? "Untitled" : s;
    }
}
