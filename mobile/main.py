"""yt-prime mobile: ad-free YouTube in an Android WebView.

Built with Buildozer (python-for-android). On Android, a native WebView is
attached to the activity via pyjnius and the ad-block content script is
evaluated on a timer. On the desktop it just shows a hint label.
"""

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label

from adblock import build_content_script

HOME = "https://www.youtube.com/"


def _autoclass():
    try:
        from jnius import autoclass

        return autoclass
    except Exception:
        return None


class YtPrimeApp(App):
    title = "yt-prime"

    def build(self):
        autoclass = _autoclass()
        if autoclass is None:
            return Label(
                text="yt-prime\nRun on Android to open YouTube",
                halign="center",
                valign="middle",
            )
        self._init_webview(autoclass)
        Clock.schedule_interval(self._sweep, 2.0)
        Window.bind(on_keyboard=self._on_key)
        return Label()  # placeholder; the native WebView covers the screen

    def _init_webview(self, autoclass):
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        WebView = autoclass("android.webkit.WebView")
        WebViewClient = autoclass("android.webkit.WebViewClient")
        LayoutParams = autoclass("android.view.ViewGroup$LayoutParams")

        activity = PythonActivity.mActivity
        webview = WebView(activity)
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setMediaPlaybackRequiresUserGesture(False)
        settings.setUseWideViewPort(True)
        webview.setWebViewClient(WebViewClient())
        params = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        activity.addContentView(webview, params)
        webview.loadUrl(HOME)
        self.webview = webview

    def _sweep(self, _dt):
        webview = getattr(self, "webview", None)
        if webview is None:
            return
        try:
            webview.evaluateJavascript(build_content_script(), None)
        except Exception:
            pass

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
        except Exception:
            pass
        return False


if __name__ == "__main__":
    YtPrimeApp().run()
