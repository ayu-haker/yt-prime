"""Cosmetic filters and a content script injected into YouTube pages.

Mimics the on-page half of uBlock Origin for youtube.com: a MutationObserver
removes ad elements as they are added by YouTube's SPA, an injected stylesheet
hides the same elements instantly on load, and skip-buttons are auto-clicked.

The selector set is the well-known YouTube blocklist used by uBlock Origin /
EasyList (ytd-display-ad-renderer, ytd-in-feed-ad-layout-renderer, player
overlays, masthead ads, promoted sparkles, ...).
"""

import json

# CSS selectors whose matching elements are treated as ads.
CSS_SELECTORS = [
    # In-feed / home ads
    "ytd-display-ad-renderer",
    "ytd-in-feed-ad-layout-renderer",
    "ytd-promoted-sparkles-web-renderer",
    "ytd-video-masthead-ad-v3-renderer",
    "ytd-banner-promo-renderer",
    "ytd-statement-banner-renderer",
    "ytd-ad-slot-renderer",
    "ytd-companion-slot-renderer",
    "ytd-player-legacy-desktop-watch-ads-renderer",
    "ytd-search-pyv-renderer",
    "ytd-rich-item[is-ad]",
    "ytd-video-renderer[is-ad]",
    # In-player overlays
    ".ytp-ad-player-overlay",
    ".ytp-ad-module",
    ".ytp-ad-image-overlay",
    ".ytp-ad-overlay-container",
    ".ytp-ad-text-overlay",
    ".ytp-ad-text-overlay-container",
    ".ytp-ad-progress-bar",
    ".ytp-ad-preview-container",
    ".ytp-ad-skip-button-container",
    ".ytp-ad-skip-button",
    ".ytp-ad-skip-button-modern",
    ".ytp-ad-skip-button-modern:hover",
    "#player-ads",
    "#masthead-ad",
]

CSS_INJECT = "\n".join(
    f"{sel}{{ display:none !important; }}"
    for sel in CSS_SELECTORS
) + "\n"

# Auto-click selectors: clickable skip/close affordances for in-player ads.
SKIP_SELECTORS = [
    ".ytp-ad-skip-button",
    ".ytp-ad-skip-button-modern",
    ".ytp-ad-overlay-close-button",
    ".ytp-ad-skip-button-slot",
]

_CONTENT_TEMPLATE = r"""
(function () {
  "use strict";
  var css = %CSS_JSON%;
  var skipSelectors = %SKIP_SELECTORS%;

  function injectStyle() {
    var style = document.createElement("style");
    style.setAttribute("type", "text/css");
    style.appendChild(document.createTextNode(css));
    (document.head || document.documentElement).appendChild(style);
  }

  function hideAds() {
    var ads = document.querySelectorAll(%AD_SELECTORS%);
    for (var i = 0; i < ads.length; i++) {
      var el = ads[i];
      if (el && el.parentNode) el.remove();
    }
  }

  function clickSkip() {
    for (var i = 0; i < skipSelectors.length; i++) {
      var el = document.querySelector(skipSelectors[i]);
      if (el) {
        el.click();
        el.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      }
    }
  }

  function sweep() {
    hideAds();
    clickSkip();
  }

  var observer = new MutationObserver(sweep);

  function start() {
    injectStyle();
    sweep();
    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }

  // Keep sweeping: YouTube swaps DOM nodes on navigation without reloading.
  setInterval(sweep, 2000);
})();
"""

CONTENT_SCRIPT = (
    _CONTENT_TEMPLATE.replace("%CSS_JSON%", json.dumps(CSS_INJECT))
    .replace("%SKIP_SELECTORS%", json.dumps(SKIP_SELECTORS))
    .replace("%AD_SELECTORS%", json.dumps(CSS_SELECTORS))
)
