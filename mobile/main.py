"""yt-prime mobile: ad-free YouTube in an Android WebView.

Built with Buildozer (python-for-android). On Android, a native WebView is
attached to the activity via pyjnius and the ad-block content script is
evaluated on a timer. On the desktop it just shows a hint label.

Every startup step is logged to ytprime.log (in the app files dir, or
/sdcard/Download when writable) and any failure during WebView setup is
shown on screen so it can be reported.
"""

import os
import traceback

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label

try:
    from adblock import build_content_script
except Exception:
    build_content_script = None

HOME = "https://www.youtube.com/"
LOG_FILENAME = "ytprime.log"


def _log_path():
    candidates = []
    try:
        from jnius import autoclass

        activity = autoclass("org.kivy.android.PythonActivity").mActivity
        candidates.append(activity.getFilesDir().getAbsolutePath())
        try:
            download = os.path.join(
                autoclass("android.os.Environment")
                .getExternalStoragePublicDirectory(
                    autoclass("android.os.Environment").DIRECTORY_DOWNLOADS
                )
                .getAbsolutePath(),
                "ytprime",
            )
            candidates.append(download)
        except Exception:
            pass
    except Exception:
        pass
    candidates.append(os.getcwd())
    for base in candidates:
        try:
            path = os.path.join(base, LOG_FILENAME)
            os.makedirs(base, exist_ok=True)
            with open(path, "a"):
                pass
            return path
        except Exception:
            continue
    return os.path.join(os.getcwd(), LOG_FILENAME)


def _append_log(message):
    try:
        with open(_log_path(), "a") as handle:
            handle.write(message + "\n")
    except Exception:
        pass


def _autoclass():
    try:
        from jnius import autoclass

        return autoclass
    except Exception as exc:
        _append_log("jnius import failed: %r" % (exc,))
        return None


def _fail_label(text):
    label = Label(text=text, halign="center", valign="middle")
    label.bind(size=label.setter("text_size"))
    return label


class YtPrimeApp(App):
    title = "yt-prime"

    def build(self):
        _append_log("== yt-prime start ==")
        autoclass = _autoclass()
        if autoclass is None:
            return _fail_label("yt-prime\nRun on Android to open YouTube")
        try:
            self._init_webview(autoclass)
        except Exception:
            trace = traceback.format_exc()
            _append_log("webview init failed:\n" + trace)
            return _fail_label("WebView init failed:\n\n" + trace)
        Clock.schedule_interval(self._sweep, 2.0)
        try:
            Window.bind(on_keyboard=self._on_key)
        except Exception as exc:
            _append_log("Window.bind(on_keyboard) failed: %r" % (exc,))
        self._heartbeat = 0
        return Label()  # placeholder; the native WebView covers the screen

    def _init_webview(self, autoclass):
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        activity = PythonActivity.mActivity
        _append_log("PythonActivity OK")

        WebView = autoclass("android.webkit.WebView")
        WebViewClient = autoclass("android.webkit.WebViewClient")
        LayoutParams = autoclass("android.view.ViewGroup$LayoutParams")
        _append_log("webview classes loaded")

        webview = WebView(activity)
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setMediaPlaybackRequiresUserGesture(False)
        settings.setUseWideViewPort(True)
        webview.setWebViewClient(WebViewClient())
        _append_log("webview configured")

        params = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        activity.addContentView(webview, params)
        _append_log("webview attached")

        webview.loadUrl(HOME)
        self.webview = webview
        _append_log("url loaded: " + HOME)

    def _sweep(self, _dt):
        self._heartbeat = getattr(self, "_heartbeat", 0) + 1
        if self._heartbeat % 15 == 0:
            _append_log("alive (sweep %d)" % self._heartbeat)
        webview = getattr(self, "webview", None)
        if webview is None or build_content_script is None:
            return
        try:
            webview.evaluateJavascript(build_content_script(), None)
        except Exception as exc:
            _append_log("evaluateJavascript failed: %r" % (exc,))

    def _on_key(self, _window, key, _scancode, _codepoint, _modifiers):
        if key != 27:  # Android back button
            return False
        webview = getattr(self, "webview", None)
        if webview is None:
            return False
        try:
            if webview.canGoBack():
                webview.goBack()
                return True
        except Exception as exc:
            _append_log("back handler failed: %r" % (exc,))
        return False


if __name__ == "__main__":
    YtPrimeApp().run()
