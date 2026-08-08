package org.ytprime.ytprime;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class HistoryActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        HistoryStore history = new HistoryStore(this);
        final List<HistoryStore.Entry> entries = history.list();

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);

        TextView heading = new TextView(this);
        heading.setText("Watch history");
        heading.setTextSize(22);
        heading.setPadding(20, 28, 20, 8);
        root.addView(heading);

        if (entries.isEmpty()) {
            TextView empty = new TextView(this);
            empty.setText("No videos watched yet.\nVideos you open will appear here.");
            empty.setTextSize(16);
            empty.setPadding(20, 24, 20, 8);
            root.addView(empty);
            setContentView(root);
            return;
        }

        ArrayAdapter<HistoryStore.Entry> adapter =
                new ArrayAdapter<HistoryStore.Entry>(
                        this, android.R.layout.simple_list_item_2,
                        android.R.id.text1, entries) {
                    @Override
                    public View getView(int position, View convertView, ViewGroup parent) {
                        View v = super.getView(position, convertView, parent);
                        HistoryStore.Entry e = getItem(position);
                        TextView t1 = v.findViewById(android.R.id.text1);
                        TextView t2 = v.findViewById(android.R.id.text2);
                        t1.setText(e.title);
                        t2.setText(formatTime(e.ts));
                        return v;
                    }
                };

        ListView list = new ListView(this);
        list.setAdapter(adapter);
        list.setOnItemClickListener((parent, v, position, id) -> {
            HistoryStore.Entry e = entries.get(position);
            Intent data = new Intent();
            data.putExtra("url", e.url);
            setResult(RESULT_OK, data);
            finish();
        });
        root.addView(list);
        setContentView(root);
    }

    private static String formatTime(long ts) {
        return new SimpleDateFormat("dd MMM, HH:mm", Locale.getDefault()).format(new Date(ts));
    }
}
