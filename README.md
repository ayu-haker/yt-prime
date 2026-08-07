# yt-prime

Ad-free YouTube, on your phone and on your desktop.

Two apps that both wrap the real YouTube web app and apply a
**uBlock-Origin-style ad blocker** (strip ad DOM, block ad networks,
auto-click skip buttons):

| App | Platform | Built with | How to get it |
|-----|----------|------------|---------------|
| **Mobile** | Android 5.0+ | Python — Kivy + Buildozer | **Download the ready APK** (below) |
| **Desktop** | Windows/Linux | Python — PySide6 QtWebEngine | `pip install -r requirements.txt && python main.py` |

Both are **pure Python**. The Android APK is compiled from the Kivy app in
`mobile/` by CI on every `v*` tag — no Android Studio or Java needed.

---

## 📥 Download the APK

Grab `ytprime-1.0.0-arm64-v8a-debug.apk` (~21 MB):

- **Direct:** [`dist/ytprime-1.0.0-arm64-v8a-debug.apk`](dist/ytprime-1.0.0-arm64-v8a-debug.apk)
- **Release:** [github.com/ayu-haker/yt-prime/releases/latest](https://github.com/ayu-haker/yt-prime/releases/latest)

Then, on your phone:
1. Tap the downloaded `.apk` file.
2. Allow **"install from unknown sources"** when asked.
3. Open **yt-prime**, log in, watch — ads gone.

> The APK lives directly in `dist/` so you never need to wait on a
> build/release page. New builds land there automatically on every tag.

---

## 📱 Mobile app (Android)

An installable APK that opens YouTube full-screen in an Android WebView
(with a desktop-site toggle in the menu) and continuously removes ads.
No Play Store, no root, no account required.

### In-app menu

- **Refresh** — reload the page.
- **Ad-block: ON/OFF** — toggle the filter on the fly (takes effect on reload).
- **Desktop site: ON/OFF** — switch the desktop YouTube layout in the phone.

### How it blocks ads

- An injected stylesheet hides every known ad element
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

CI builds `arm64-v8a` automatically on every `v*` tag
(`.github/workflows/release.yml`).

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
├── dist/                Ready-to-install APK (official release)
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
