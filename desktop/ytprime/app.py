"""Application bootstrap."""

import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWebEngineWidgets import QWebEngineView  # noqa: F401 (loads QtWebEngine)

from .adblock.blocker import RequestBlocker
from .window import MainWindow


def run(argv: list[str] | None = None) -> int:
    QCoreApplication.setOrganizationName("yt-prime")
    QCoreApplication.setApplicationName("yt-prime")

    from PySide6.QtWidgets import QApplication

    app = QApplication(argv if argv is not None else sys.argv)
    blocker = RequestBlocker()
    window = MainWindow(blocker)
    window.show()
    return app.exec()
