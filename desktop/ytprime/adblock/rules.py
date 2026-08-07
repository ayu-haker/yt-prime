"""Ad-block filter rules.

A curated, YouTube-focused rule set inspired by uBlock Origin / EasyList
filter lists. Pure Python so it can be unit-tested without a display.

Rule types:
  - blocked_domains:  host equals rule, or is a subdomain of it
  - blocked_host_substrings: host contains the rule substring
  - url_keywords:     full URL contains the substring (narrowed by host when
                      `on_hosts` is given)
"""

from dataclasses import dataclass, field

# Third-party ad / tracking / telemetry domains.
BLOCKED_DOMAINS = {
    "doubleclick.net",
    "googleadservices.com",
    "googlesyndication.com",
    "pagead2.googlesyndication.com",
    "google-analytics.com",
    "googletagmanager.com",
    "adservice.google.com",
    "adsystem.com",
    "adform.net",
    "adnxs.com",
    "taboola.com",
    "outbrain.com",
}

# Host substrings that mark an ad/tracker request anywhere.
BLOCKED_HOST_SUBSTRINGS = {
    "doubleclick",
    "googlesyndication",
    "googleadservices",
}

# URL substrings that identify ad traffic on specific hosts.
# Ordered: more specific rules first (the first match wins).
BLOCKED_URL_KEYWORDS = [
    # Video ads served from the same googlevideo.com player backend carry an
    # ad_signature parameter; blocking them kills pre/mid-roll video ads.
    ("googlevideo.com", "ad_signature"),
    ("googlevideo.com", "ad_"),
    ("youtube.com", "/pagead/"),
    ("youtube.com", "youtubei/v1/ad_break"),
]

# Justifications shown in the block log / debug UI.
DOMAIN_REASONS = {
    "doubleclick.net": "Google ad network",
    "googleadservices.com": "Google ad services",
    "googlesyndication.com": "AdSense / syndication",
    "pagead2.googlesyndication.com": "AdSense / syndication",
    "google-analytics.com": "Analytics (optional to block)",
    "googletagmanager.com": "Tag manager / telemetry",
    "adservice.google.com": "Ad delivery",
    "adsystem.com": "Ad network",
    "adform.net": "Ad network",
    "adnxs.com": "Ad network (AppNexus)",
    "taboola.com": "Native ads",
    "outbrain.com": "Native ads",
}


@dataclass
class Ruleset:
    """Container of ad-blocking rules with a single match query."""

    domains: set = field(default_factory=lambda: set(BLOCKED_DOMAINS))
    host_substrings: set = field(default_factory=lambda: set(BLOCKED_HOST_SUBSTRINGS))
    url_keywords: list = field(default_factory=lambda: list(BLOCKED_URL_KEYWORDS))

    def blocked(self, host: str, full_url: str) -> str | None:
        """Return the matching rule name, or None if the URL is allowed.

        host and full_url must be lower-cased by the caller.
        """
        if not host:
            return None
        for rule in self.domains:
            if host == rule or host.endswith("." + rule):
                return DOMAIN_REASONS.get(rule, rule)
        for sub in self.host_substrings:
            if sub in host:
                return f"host contains '{sub}'"
        for (on_host, keyword) in self.url_keywords:
            if on_host in host and keyword in full_url:
                return f"'{keyword}' on {on_host}"
        return None


def block_decision(host: str, full_url: str, ruleset: Ruleset | None = None) -> str | None:
    """Lower-case convenience wrapper around :meth:`Ruleset.blocked`."""
    ruleset = ruleset or Ruleset()
    return ruleset.blocked(host.lower(), full_url.lower())
