"""Main window: phone-sized portrait frame around the YouTube web app."""

from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from .browser import BrowserView
from .adblock.blocker import RequestBlocker
from .config import HOME_URL, MIN_HEIGHT, MIN_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH

YOUTUBE_PREFIX = "youtube.com"


class MainWindow(QMainWindow):
    def __init__(self, blocker: RequestBlocker):
        super().__init__()
        self.setWindowTitle("yt-prime — YouTube (ad-free)")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(MIN_WIDTH, MIN_HEIGHT)

        self.browser = BrowserView(blocker, self)
        self.browser.urlChanged.connect(self._on_url_changed)

        self._bar = self._build_toolbar()
        self._status = QStatusBar(self)
        self.setStatusBar(self._status)
        blocker.blocked.connect(
            lambda host, reason: self._status.showMessage(
                f"blocked {host} ({reason})", 3000
            )
        )

        central = QWidget(self)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._bar)
        layout.addWidget(self.browser, 1)
        self.setCentralWidget(central)

        self.browser.setUrl(QUrl(HOME_URL))

    def _build_toolbar(self) -> QWidget:
        bar = QWidget(self)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        back = QPushButton("◀", bar)
        back.setToolTip("Back")
        back.clicked.connect(self.browser.back)

        fwd = QPushButton("▶", bar)
        fwd.setToolTip("Forward")
        fwd.clicked.connect(self.browser.forward)

        reload = QPushButton("⟳", bar)
        reload.setToolTip("Reload")
        reload.clicked.connect(self.browser.reload)

        home = QPushButton("⌂", bar)
        home.setToolTip("YouTube Home")
        home.clicked.connect(lambda: self.browser.setUrl(QUrl(HOME_URL)))

        self._address = QLineEdit(HOME_URL, bar)
        self._address.setPlaceholderText("Search or paste a YouTube link…")
        self._address.returnPressed.connect(self._go)

        for widget in (back, fwd, reload, home):
            layout.addWidget(widget)
        layout.addWidget(self._address, 1)
        return bar

    def _go(self):
        text = self._address.text().strip()
        if not text:
            return
        if not text.startswith("http://") and not text.startswith("https://"):
            url = f"https://www.{YOUTUBE_PREFIX}/results?search_query={_quote(text)}"
        else:
            url = text
        self.browser.setUrl(QUrl(url))

    def _on_url_changed(self, url: QUrl):
        self._address.setText(url.toString())


def _quote(text: str) -> str:
    from urllib.parse import quote

    return quote(text)
