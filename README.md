# yt-prime

Ad-free YouTube, on your phone and on your desktop.

A small project with two apps that both wrap the real YouTube web app and
apply a **uBlock-Origin-style ad blocker** (block ad networks, strip ad DOM,
auto-click skip buttons):

| App | Platform | Built with | How to get it |
|-----|----------|------------|---------------|
| **Mobile** | Android | Python — Kivy + Buildozer (python-for-android) | Install the APK from **GitHub Releases** |
| **Desktop** | Windows/Linux | Python — PySide6 QtWebEngine | `pip install -r requirements.txt && python main.py` |

Both are **pure Python**. The APK is compiled from the Kivy app in `mobile/`
by CI on every `v*` tag — no Android Studio or Java needed.

---

## 📱 Mobile app (Android)

An installable APK that opens YouTube full-screen in an Android WebView
(with a desktop-site toggle in the menu) and continuously removes ads.

### Install

1. Grab `ytprime-*.apk` from the latest **Release** on GitHub — or directly
   from `dist/` in this repo.
2. Open it on your phone → allow "install from unknown sources" → Install.
3. Open **yt-prime**, log in, watch — ads gone.

No Play Store, no root, no accounts, and the app itself is ~25 MB.

### In-app menu

- **Refresh** — reload the page.
- **Ad-block: ON/OFF** — toggle the filter on the fly (takes effect on reload).
- **Desktop site: ON/OFF** — switch the desktop YouTube layout in the phone.

### How it blocks ads

- Injected stylesheet hides every known ad element
  (`ytd-display-ad-renderer`, `ytd-in-feed-ad-layout-renderer`, player
  overlays, masthead/promoted cards…).
- A `MutationObserver` + 2 s sweep strips ad nodes as YouTube adds them and
  **auto-clicks the skip button** for residual in-player ads.

Filter lists live in `mobile/adblock.py`.

### Build it yourself

```bash
pip install buildozer
cd mobile
buildozer -v android debug        # needs Docker or the p4a toolchain
# APK appears in mobile/bin/
```

CI builds it for `arm64-v8a` and `armeabi-v7a` (Android 8.0+).

---

## 🖥 Desktop app

A phone-sized portrait window (~430×860, resizable) around the full desktop
YouTube site, with the same ad blocker at the network *and* DOM level.

```bash
cd desktop
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

- **Network blocking** — drops requests to ad networks
  (`doubleclick.net`, `googlesyndication.com`, `googleadservices.com`) and
  kills in-player video ads (`googlevideo.com` URLs with `ad_signature`);
  blocked count + reason shows in the status bar.
- **Cosmetic blocking** — injected stylesheet + MutationObserver removes ad
  elements and auto-clicks skip.
- **Persistent login** — your YouTube account survives restarts.

WSL note: `sudo apt install libxkbfile1`, and if you have no GPU:
`QTWEBENGINE_CHROMIUM_FLAGS="--disable-gpu --no-sandbox"`.

---

## Tests

```bash
python -m pytest -q     # 10 tests
```

- Desktop: ad-network blocking, googlevideo `ad_signature`, allow-list
  behaviour, content-script selectors.
- Mobile: content-script builder validity + selector coverage.

## Repository layout

```
yt-prime/
├── desktop/             PySide6 desktop app
│   ├── main.py
│   ├── requirements.txt
│   └── ytprime/         adblock/ (rules, blocker, scripts), window, browser
├── mobile/              Kivy + Buildozer Android app
│   ├── main.py          WebView + periodic ad-script injection
│   ├── adblock.py       Filter lists + content script (testable)
│   └── buildozer.spec
├── tests/               shared test suite
├── .github/workflows/release.yml   Builds the APK on v* tags → Release
└── desktop/tests/       desktop filter tests
```
