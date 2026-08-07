"""Ad-blocking subsystem.

Filter logic (rules, scripts) is Qt-free and unit-testable without a
display; the Qt request interceptor is imported lazily by callers.
"""

from .rules import Ruleset, block_decision
from .scripts import CONTENT_SCRIPT, CSS_INJECT, CSS_SELECTORS, SKIP_SELECTORS

__all__ = [
    "Ruleset",
    "block_decision",
    "CONTENT_SCRIPT",
    "CSS_INJECT",
    "CSS_SELECTORS",
    "SKIP_SELECTORS",
]
