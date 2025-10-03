@echo off
echo 🚀 Building Temenos RAG Client Android App...
echo ================================================

REM Check if we're in the right directory
if not exist "settings.gradle" (
    echo ❌ Error: Please run this script from the android-app directory
    pause
    exit /b 1
)

REM Check if Java is available
java -version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Java is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Android SDK is available
if "%ANDROID_HOME%"=="" (
    echo ⚠️  Warning: ANDROID_HOME is not set
    echo    Make sure Android SDK is installed and ANDROID_HOME is set
)

echo 📱 Building debug APK...
call gradlew.bat assembleDebug

if errorlevel 1 (
    echo ❌ Build failed!
    pause
    exit /b 1
) else (
    echo ✅ Build successful!
    echo 📦 APK location: app\build\outputs\apk\debug\app-debug.apk
    echo.
    echo 📋 To install on device:
    echo    adb install app\build\outputs\apk\debug\app-debug.apk
    echo.
    echo 📋 To run in Android Studio:
    echo    android-studio .
)

pause 