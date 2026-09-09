#!/bin/bash

echo "Building Discode Android APK..."
echo "================================"
echo ""

# Check if we're in the right directory
if [ ! -f "app/build.gradle" ]; then
    echo "Error: Please run this script from the project root directory"
    echo "Usage: ./build_apk.sh"
    exit 1
fi

# Check for Java
if ! command -v java &> /dev/null; then
    echo "Error: Java is not installed"
    echo "Please install Java JDK 17 or later"
    exit 1
fi

# Check for Android SDK
if [ -z "$ANDROID_HOME" ]; then
    echo "Error: ANDROID_HOME is not set"
    echo "Please set ANDROID_HOME to your Android SDK path"
    exit 1
fi

# Create releases directory
mkdir -p app/releases

# Build debug APK
echo "Building debug APK..."
cd app
./gradlew assembleDebug --no-daemon --stacktrace

if [ $? -eq 0 ]; then
    # Copy debug APK to releases
    if [ -f "app/build/outputs/apk/debug/app-debug.apk" ]; then
        cp app/build/outputs/apk/debug/app-debug.apk ../releases/
        echo "✓ Debug APK built: app/releases/app-debug.apk"
    fi
else
    echo "✗ Debug APK build failed"
    exit 1
fi

echo ""
echo "================================"
echo "Build complete!"
echo ""
echo "APK location: app/releases/app-debug.apk"
echo ""
echo "To build a release APK for distribution:"
echo "1. Create a keystore: keytool -genkey -v -keystore discode.keystore -alias discode -keyalg RSA -keysize 2048 -validity 10000"
echo "2. Run: ./gradlew assembleRelease"
echo "3. The signed APK will be in app/build/outputs/apk/release/"
