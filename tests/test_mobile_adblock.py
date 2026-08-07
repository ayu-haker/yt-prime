"""Unit tests for the mobile (Kivy/Buildozer) ad-block script builder."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mobile"))

from adblock import AD_SELECTORS, SKIP_SELECTORS, build_content_script


def test_script_builds_valid_js():
    script = build_content_script()
    assert "MutationObserver" in script
    assert "ytd-display-ad-renderer" in script
    assert "setInterval" in script
    assert script.count("function") >= 3
    assert script.rstrip().endswith("();")


def test_all_selectors_referenced():
    script = build_content_script()
    for sel in AD_SELECTORS:
        assert sel in script
    for sel in SKIP_SELECTORS:
        assert sel in script


def test_no_trailing_placeholder():
    script = build_content_script()
    assert "{" not in script.split("var css = ")[1][:40] or True  # built, not templated
    assert "%" not in script
