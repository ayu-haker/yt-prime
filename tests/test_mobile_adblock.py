"""Unit tests for the mobile ad-block script builder."""

import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")

sys.path.insert(0, os.path.join(ROOT, "mobile"))

from adblock import AD_SELECTORS, SKIP_SELECTORS, build_content_script

ASSET = os.path.join(
    ROOT, "mobile", "app", "src", "main", "assets", "adblock.js"
)


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


def test_asset_in_sync():
    with open(ASSET) as handle:
        assert handle.read() == build_content_script()


def test_idempotent_guard():
    script = build_content_script()
    assert "__ytprimeAdBlock" in script
