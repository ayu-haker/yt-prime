"""Qt-side glue that turns the ruleset into enforced blocking."""

from PySide6.QtCore import Signal, QObject
from PySide6.QtWebEngineCore import QWebEngineUrlRequestInterceptor

from .rules import Ruleset, block_decision


class RequestBlocker(QWebEngineUrlRequestInterceptor):
    """Blocks ad/tracker requests before they reach the network.

    'blocked' is emitted with the reason whenever a request is dropped.
    """

    blocked = Signal(str, str)

    def __init__(self, ruleset: Ruleset | None = None, parent: QObject | None = None):
        super().__init__(parent)
        self._ruleset = ruleset or Ruleset()

    def interceptRequest(self, info) -> None:
        url = info.requestUrl()
        host = url.host()
        full = url.toString()
        reason = block_decision(host, full, self._ruleset)
        if reason is not None:
            self.blocked.emit(host, reason)
            info.block(True)
