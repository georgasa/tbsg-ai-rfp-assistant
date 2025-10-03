#!/bin/bash

# Temenos RAG Client Android App Build Script

echo "🚀 Building Temenos RAG Client Android App..."
echo "================================================"

# Check if we're in the right directory
if [ ! -f "settings.gradle" ]; then
    echo "❌ Error: Please run this script from the android-app directory"
    exit 1
fi

# Check if Java is available
if ! command -v java &> /dev/null; then
    echo "❌ Error: Java is not installed or not in PATH"
    exit 1
fi

# Check if Android SDK is available
if [ -z "$ANDROID_HOME" ]; then
    echo "⚠️  Warning: ANDROID_HOME is not set"
    echo "   Make sure Android SDK is installed and ANDROID_HOME is set"
fi

echo "📱 Building debug APK..."
./gradlew assembleDebug

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "📦 APK location: app/build/outputs/apk/debug/app-debug.apk"
    echo ""
    echo "📋 To install on device:"
    echo "   adb install app/build/outputs/apk/debug/app-debug.apk"
    echo ""
    echo "📋 To run in Android Studio:"
    echo "   android-studio ."
else
    echo "❌ Build failed!"
    exit 1
fi 