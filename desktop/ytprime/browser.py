"""Browser view + persistent profile with the ad-block stack attached."""

from PySide6.QtCore import QUrl, Signal
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineScript
from PySide6.QtWebEngineWidgets import QWebEngineView

from .adblock import CONTENT_SCRIPT
from .adblock.blocker import RequestBlocker
from .config import COSMETIC_FILTERS, NETWORK_FILTERS, PROFILE_DIR


def _make_profile(blocker: RequestBlocker) -> QWebEngineProfile:
    profile = QWebEngineProfile(PROFILE_DIR)  # persistent: keeps YouTube login
    if NETWORK_FILTERS:
        profile.setUrlRequestInterceptor(blocker)
    if COSMETIC_FILTERS:
        # Inject a stylesheet + MutationObserver that removes ad elements and
        # auto-clicks skip buttons, continuously (works in Qt6, no
        # StyleSheetWorld support needed).
        js = QWebEngineScript()
        js.setName("ytprime-content")
        js.setSourceCode(CONTENT_SCRIPT)
        js.setInjectionPoint(QWebEngineScript.DocumentReady)
        js.setWorldId(QWebEngineScript.MainWorld)
        js.setRunsOnSubFrames(True)
        profile.scripts().insert(js)
    return profile


class BrowserView(QWebEngineView):
    """QWebEngineView wired to a persistent, ad-blocked profile."""

    def __init__(self, blocker: RequestBlocker, parent=None):
        super().__init__(parent)
        self.setPage(QWebEnginePage(_make_profile(blocker), self))
