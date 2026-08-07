"""Unit tests for the ad-block filter engine (no Qt/display needed)."""

from ytprime.adblock.rules import Ruleset, block_decision


def test_blocks_ad_networks():
    assert block_decision("googleads.g.doubleclick.net", "https://googleads.g.doubleclick.net/pagead/id") == "Google ad network"
    assert block_decision("pagead2.googlesyndication.com", "https://pagead2.googlesyndication.com/activeview") == "AdSense / syndication"
    assert block_decision("securepubads.g.doubleclick.net", "https://securepubads.g.doubleclick.net/gpt/pubads_impl.js") is not None


def test_allows_google_content():
    assert block_decision("www.youtube.com", "https://www.youtube.com/watch?v=abc") is None
    assert block_decision("rr4---sn.youtube.com", "https://rr4---sn.youtube.com/videoplayback?video=xyz") is None
    assert block_decision("www.google.com", "https://www.google.com/") is None


def test_blocks_googlevideo_ad_signature():
    assert block_decision(
        "rr5---sn.googlevideo.com",
        "https://rr5---sn.googlevideo.com/videoplayback?ad_signature=XYZ&itag=18",
    ) == "'ad_signature' on googlevideo.com"


def test_blocks_youtube_pagead_path():
    assert block_decision(
        "www.youtube.com", "https://www.youtube.com/pagead/viewthroughconversion"
    ) is not None


def test_custom_ruleset_override():
    ruleset = Ruleset(domains={"myads.test"}, host_substrings=set(), url_keywords=set())
    assert ruleset.blocked("cdn.myads.test", "https://cdn.myads.test/x.js") == "myads.test"
    assert ruleset.blocked("www.youtube.com", "https://www.youtube.com/watch?v=x") is None


def test_empty_host():
    assert block_decision("", "file:///tmp/a.html") is None


def test_scripts_contain_known_selectors():
    from ytprime.adblock.scripts import CONTENT_SCRIPT, CSS_INJECT, CSS_SELECTORS

    assert "ytd-display-ad-renderer" in CSS_SELECTORS
    assert "ytd-display-ad-renderer{ display:none !important; }" in CSS_INJECT
    assert "MutationObserver" in CONTENT_SCRIPT
    assert ".ytp-ad-skip-button" in CONTENT_SCRIPT
