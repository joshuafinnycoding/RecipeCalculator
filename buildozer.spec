[app]

# (str) Title of your application
title = Recipe Calculator

# (str) Package name
package.name = recipecalculator

# (str) Package domain (needed for android/ios packaging)
package.domain = org.recipecalculator

# (source.dir) Source code directory containing main.py
source.dir = .

# (list) Source includes patterns, let empty to include all the files in source.dir
# includes patterns are separated by ' '
#source.include_patterns = assets/*,images/*.png

# (list) List of inclusions using pattern matching
#source.include_exts = py,png,jpg,kv,atlas

# Version
version = 0.1

# Requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,android

# Supported orientations
orientation = portrait

# Fullscreen or not
fullscreen = 0

# Android specific
[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# Path to build artifact storage, absolute or relative to spec file
build_dir = .buildozer

# Path to build output (i.e. where the built apk will be)
bin_dir = ./bin

# Allow running the build command without fully installing Buildozer
# before, this is useful for testing
#android.skip_update = False

# Specify the Python for android API to build against
android.api = 31

# Specify the Android NDK version to use
android.ndk = 25c

# Specify the Android SDK version to use
android.sdk = 34

# Specify the Android build tools version
android.build_tools_version = 34.0.0

# Whether or not to warn on release keys
android.release_artifact = apk

# Target Android API
android.target_api = 34

# Minimum API
android.minapi = 21

# Default orientation
android.orientation = portrait

# Permissions
android.permissions = INTERNET,ACCESS_FINE_LOCATION,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Features
android.features = android.hardware.usb.host

# The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# Presplash
#p4a.hook = patches/0001-custom-setup.patch

# Include requirements (python and libraries) in the apk
android.entrypoint = org.kivy.android.PythonActivity
