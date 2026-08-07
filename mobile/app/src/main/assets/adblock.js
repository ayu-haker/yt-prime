(
function () {
  "use strict";
  if (window.__ytprimeAdBlock) return;
  window.__ytprimeAdBlock = true;
  var css = "ytd-display-ad-renderer{ display:none !important; }ytd-in-feed-ad-layout-renderer{ display:none !important; }ytd-promoted-sparkles-web-renderer{ display:none !important; }ytd-video-masthead-ad-v3-renderer{ display:none !important; }ytd-banner-promo-renderer{ display:none !important; }ytd-statement-banner-renderer{ display:none !important; }ytd-ad-slot-renderer{ display:none !important; }ytd-companion-slot-renderer{ display:none !important; }ytd-player-legacy-desktop-watch-ads-renderer{ display:none !important; }ytd-search-pyv-renderer{ display:none !important; }ytd-rich-item[is-ad]{ display:none !important; }ytd-video-renderer[is-ad]{ display:none !important; }.ytp-ad-player-overlay{ display:none !important; }.ytp-ad-module{ display:none !important; }.ytp-ad-image-overlay{ display:none !important; }.ytp-ad-overlay-container{ display:none !important; }.ytp-ad-text-overlay{ display:none !important; }.ytp-ad-text-overlay-container{ display:none !important; }.ytp-ad-progress-bar{ display:none !important; }.ytp-ad-preview-container{ display:none !important; }.ytp-ad-skip-button-container{ display:none !important; }.ytp-ad-skip-button{ display:none !important; }.ytp-ad-skip-button-modern{ display:none !important; }#player-ads{ display:none !important; }#masthead-ad{ display:none !important; }";
  var skip = ".ytp-ad-skip-button,.ytp-ad-skip-button-modern,.ytp-ad-overlay-close-button,.ytp-ad-skip-button-slot";
  var adQuery = "ytd-display-ad-renderer,ytd-in-feed-ad-layout-renderer,ytd-promoted-sparkles-web-renderer,ytd-video-masthead-ad-v3-renderer,ytd-banner-promo-renderer,ytd-statement-banner-renderer,ytd-ad-slot-renderer,ytd-companion-slot-renderer,ytd-player-legacy-desktop-watch-ads-renderer,ytd-search-pyv-renderer,ytd-rich-item[is-ad],ytd-video-renderer[is-ad],.ytp-ad-player-overlay,.ytp-ad-module,.ytp-ad-image-overlay,.ytp-ad-overlay-container,.ytp-ad-text-overlay,.ytp-ad-text-overlay-container,.ytp-ad-progress-bar,.ytp-ad-preview-container,.ytp-ad-skip-button-container,.ytp-ad-skip-button,.ytp-ad-skip-button-modern,#player-ads,#masthead-ad";
  var style = document.createElement("style");
  style.setAttribute("type", "text/css");
  style.appendChild(document.createTextNode(css));
  (document.head || document.documentElement).appendChild(style);
  function hideAds() {
    document.querySelectorAll(adQuery).forEach(function (el) {
      if (el && el.parentNode) el.remove();
    });
  }
  function clickSkip() {
    var list = skip.split(",");
    for (var i = 0; i < list.length; i++) {
      var el = document.querySelector(list[i]);
      if (el) {
        el.click();
        el.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      }
    }
  }
  function sweep() { hideAds(); clickSkip(); }
  var observer = new MutationObserver(sweep);
  function start() {
    sweep();
    observer.observe(document.documentElement, { childList: true, subtree: true });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else { start(); }
  setInterval(sweep, 2000);
})();
