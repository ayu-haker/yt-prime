"""Ad-block rules + content script for the mobile (native Android WebView) app.

Pure Python (no Android imports) so it can be unit-tested on the desktop.
The produced script is evaluated in the WebView on page load and on a timer;
it is written to app/src/main/assets/adblock.js so the native app ships it.
"""

AD_SELECTORS = [
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
    "#player-ads",
    "#masthead-ad",
]

SKIP_SELECTORS = [
    ".ytp-ad-skip-button",
    ".ytp-ad-skip-button-modern",
    ".ytp-ad-overlay-close-button",
    ".ytp-ad-skip-button-slot",
]


def _js(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def build_content_script() -> str:
    """JS that hides YouTube ad DOM + auto-clicks skip buttons."""
    css = "".join(f"{sel}{{ display:none !important; }}" for sel in AD_SELECTORS)
    ad_query = ",".join(AD_SELECTORS)
    skip_query = ",".join(SKIP_SELECTORS)
    return f"""(
function () {{
  "use strict";
  if (window.__ytprimeAdBlock) return;
  window.__ytprimeAdBlock = true;
  var css = {_js(css)};
  var skip = "{skip_query}";
  var adQuery = {_js(ad_query)};
  var style = document.createElement("style");
  style.setAttribute("type", "text/css");
  style.appendChild(document.createTextNode(css));
  (document.head || document.documentElement).appendChild(style);
  function hideAds() {{
    document.querySelectorAll(adQuery).forEach(function (el) {{
      if (el && el.parentNode) el.remove();
    }});
  }}
  function clickSkip() {{
    var list = skip.split(",");
    for (var i = 0; i < list.length; i++) {{
      var el = document.querySelector(list[i]);
      if (el) {{
        el.click();
        el.dispatchEvent(new MouseEvent("click", {{ bubbles: true }}));
      }}
    }}
  }}
  function sweep() {{ hideAds(); clickSkip(); }}
  var observer = new MutationObserver(sweep);
  function start() {{
    sweep();
    observer.observe(document.documentElement, {{ childList: true, subtree: true }});
  }}
  if (document.readyState === "loading") {{
    document.addEventListener("DOMContentLoaded", start);
  }} else {{ start(); }}
  setInterval(sweep, 2000);
}})();
"""


def write_asset(path: str) -> None:
    """Write the content script to an asset file shipped inside the APK."""
    with open(path, "w") as handle:
        handle.write(build_content_script())
