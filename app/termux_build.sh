#!/bin/bash

echo "=========================================="
echo "  Discode Android APK - Termux Builder"
echo "=========================================="
echo ""

# Check if running in Termux
if [ ! -d "$PREFIX" ]; then
    echo "Error: This script is for Termux only!"
    exit 1
fi

echo "[*] Checking dependencies..."

# Install required packages
pkg install -y openjdk-17 wget unzip

# Set JAVA_HOME
if [ ! -d "$PREFIX/opt/openjdk-17" ]; then
    echo "Error: Java 17 not found"
    exit 1
fi

export JAVA_HOME=$PREFIX/opt/openjdk-17

# Download Android SDK tools
echo "[*] Downloading Android SDK tools..."

SDK_DIR=$HOME/android-sdk
mkdir -p $SDK_DIR

if [ ! -d "$SDK_DIR/cmdline-tools" ]; then
    wget -q -O /tmp/sdk-tools.zip https://dl.google.com/android/repository/commandlinetools-linux-10406996_latest.zip
    unzip -q /tmp/sdk-tools.zip -d $SDK_DIR
    mv $SDK_DIR/cmdline-tools $SDK_DIR/cmdline-tools-latest
    rm /tmp/sdk-tools.zip
fi

export ANDROID_HOME=$SDK_DIR
export ANDROID_SDK_ROOT=$SDK_DIR

# Set up PATH
export PATH=$PATH:$SDK_DIR/cmdline-tools-latest/bin

echo "[*] Setting up Android SDK..."

# Accept licenses
mkdir -p $SDK_DIR/licenses
cp /workspace/github__SonicZ-z__Discode/app/licenses/* $SDK_DIR/licenses/ 2>/dev/null || true

# Install SDK packages
echo "[*] Installing SDK packages (this may take a while)..."
sdkmanager --install "platform-tools" "platforms;android-34" "build-tools;34.0.0" "extras;android;m2repository" "extras;google;m2repository" <<< 'y'

if [ $? -ne 0 ]; then
    echo "Error: Failed to install SDK packages"
    echo "Try running: sdkmanager --list to see available packages"
    exit 1
fi

echo "[*] SDK setup complete!"
echo ""

# Build the APK
echo "[*] Building APK..."
cd /workspace/github__SonicZ-z__Discode/app

# Create local.properties
cat > local.properties <<EOF
sdk.dir=$SDK_DIR
EOF

# Build debug APK
./gradlew assembleDebug --no-daemon --stacktrace --warning-mode none

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "  ✓ APK Build Successful!"
    echo "=========================================="
    echo ""
    
    # Copy APK to releases
    mkdir -p ../releases
    if [ -f "app/build/outputs/apk/debug/app-debug.apk" ]; then
        cp app/build/outputs/apk/debug/app-debug.apk ../releases/
        ls -lh ../releases/app-debug.apk
        echo ""
        echo "APK saved to: /workspace/github__SonicZ-z__Discode/releases/app-debug.apk"
    fi
    
    echo ""
    echo "To install on your device:"
    echo "  termux-download -d /workspace/github__SonicZ-z__Discode/releases/app-debug.apk"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "  ✗ APK Build Failed!"
    echo "=========================================="
    echo ""
    echo "Check the error messages above."
    echo "Make sure you have enough storage space."
    exit 1
fi
