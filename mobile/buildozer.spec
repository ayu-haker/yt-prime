[app]

title = yt-prime
package.name = ytprime
package.domain = org.ytprime

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
source.include_patterns = icon.png

version = 1.0.0
requirements = python3,kivy

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/icon.png

# Android
android.api = 34
android.minapi = 21
android.ndk = 25b
android.build_tools = 34.0.0
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True
android.permissions = INTERNET

# iOS is not supported by this project.
ios.codesign.debug = automatic

[buildozer]

log_level = 2
warn_on_root = 1
