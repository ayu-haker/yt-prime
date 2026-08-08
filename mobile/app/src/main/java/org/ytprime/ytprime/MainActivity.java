package org.ytprime.ytprime;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.webkit.CookieManager;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

public class MainActivity extends Activity {

    private static final String HOME = "https://www.youtube.com/";
    private static final String MOBILE_UA =
            "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 "
            + "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36";
    private static final String DESKTOP_UA =
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            + "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36";

    private static final long REINJECT_MS = 2000;

    private WebView webView;
    private boolean adBlockEnabled = true;
    private boolean desktopSite = false;
    private boolean destroyed = false;
    private String contentScript = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        contentScript = readAsset("adblock.js");

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);
        settings.setSupportMultipleWindows(false);
        settings.setUserAgentString(MOBILE_UA);

        CookieManager.getInstance().setAcceptCookie(true);
        CookieManager.getInstance().setAcceptThirdPartyCookies(webView, true);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return false;  // keep all navigation (incl. Google sign-in) inside the WebView
            }

            @Override
            @SuppressWarnings("deprecation")
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return false;
            }

            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                String url = request.getUrl().toString();
                if (adBlockEnabled && isAdUrl(url)) {
                    return emptyResponse();
                }
                return super.shouldInterceptRequest(view, request);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                injectAdBlock();
            }
        });

        webView.postDelayed(reinject, REINJECT_MS);
        webView.loadUrl(HOME);
    }

    private final Runnable reinject = new Runnable() {
        @Override
        public void run() {
            if (webView != null && !destroyed) {
                injectAdBlock();
                webView.postDelayed(this, REINJECT_MS);
            }
        }
    };

    private void injectAdBlock() {
        if (!adBlockEnabled || contentScript.isEmpty()) {
            return;
        }
        try {
            webView.evaluateJavascript(contentScript, null);
        } catch (Exception ignored) {
            // page mid-navigation; next sweep will handle it
        }
    }

    private static boolean isAdUrl(String url) {
        String u = url.toLowerCase();
        return u.contains("doubleclick.net")
                || u.contains("googlesyndication.com")
                || u.contains("googleadservices.com")
                || u.contains("adservice.google.com")
                || (u.contains("googlevideo.com") && u.contains("ad_signature"));
    }

    private static WebResourceResponse emptyResponse() {
        return new WebResourceResponse(
                "text/plain", "UTF-8", new ByteArrayInputStream(new byte[0]));
    }

    private String readAsset(String name) {
        try {
            InputStream in = getAssets().open(name);
            BufferedReader reader = new BufferedReader(
                    new InputStreamReader(in, StandardCharsets.UTF_8));
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                sb.append(line).append('\n');
            }
            reader.close();
            return sb.toString();
        } catch (Exception e) {
            return "";
        }
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onDestroy() {
        destroyed = true;
        if (webView != null) {
            webView.removeCallbacks(reinject);
            webView.destroy();
        }
        super.onDestroy();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main_menu, menu);
        return true;
    }

    @Override
    public boolean onPrepareOptionsMenu(Menu menu) {
        MenuItem ad = menu.findItem(R.id.action_adblock);
        if (ad != null) {
            ad.setChecked(adBlockEnabled);
        }
        MenuItem desk = menu.findItem(R.id.action_desktop);
        if (desk != null) {
            desk.setChecked(desktopSite);
        }
        return super.onPrepareOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if (id == R.id.action_refresh) {
            webView.reload();
            return true;
        }
        if (id == R.id.action_adblock) {
            adBlockEnabled = !adBlockEnabled;
            webView.reload();
            return true;
        }
        if (id == R.id.action_desktop) {
            desktopSite = !desktopSite;
            applyUserAgent();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    private void applyUserAgent() {
        WebSettings settings = webView.getSettings();
        settings.setUserAgentString(desktopSite ? DESKTOP_UA : MOBILE_UA);
        webView.reload();
    }
}
