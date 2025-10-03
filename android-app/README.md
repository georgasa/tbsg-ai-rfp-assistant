# Temenos RAG Client - Android App

## Overview
This Android application provides a user-friendly interface for interacting with the Temenos RAG (Retrieval-Augmented Generation) API. Users can ask questions about Temenos products and receive AI-powered responses.

## Features
- **Multi-region support**: Global, MEA, and Americas regions
- **Category-based model selection**: Generic, Technology, and Functionality categories
- **Context-aware queries**: Optional context input for more specific responses
- **Connection testing**: Verify API connectivity before sending queries
- **Response management**: Copy and clear responses
- **Conversation history**: Local storage of previous conversations

## Installation

### For Development
1. Clone the repository
2. Open the project in Android Studio
3. Build and run on an emulator or physical device

### For Testing
The debug APK is located at:
```
android-app/app/build/outputs/apk/debug/app-debug.apk
```

### Installation on Device
1. Enable "Install from unknown sources" in your device settings
2. Transfer the APK to your device
3. Open the APK file to install

### Installation on Emulator
```bash
cd android-app
./gradlew installDebug
```

## Recent Fixes (Latest Update)
- **Fixed app crash on startup**: Added proper error handling and exception catching
- **Resolved theme issues**: Fixed theme name mismatches in AndroidManifest.xml
- **Updated deprecated listeners**: Replaced deprecated ChipGroup listeners with modern alternatives
- **Enhanced error logging**: Added comprehensive error logging for debugging

## API Configuration
The app uses shared configuration with the Python script. API settings are defined in `SharedConfig.kt`:
- Base URL: `https://tbsg.temenos.com/api/v1.0`
- JWT Token: Configured for authentication
- Timeout: 30 seconds

## Usage
1. **Test Connection**: Verify API connectivity
2. **Select Region**: Choose Global, MEA, or Americas
3. **Choose Category**: Select from Generic, Technology, or Functionality options
4. **Enter Question**: Type your question about Temenos products
5. **Add Context** (optional): Provide additional context for more specific responses
6. **Send Query**: Submit your question to the RAG API
7. **View Response**: See the AI-generated answer with metadata

## Technical Details
- **Minimum SDK**: 24 (Android 7.0)
- **Target SDK**: 34 (Android 14)
- **Architecture**: MVVM with Repository pattern
- **Database**: Room for local conversation storage
- **Networking**: Retrofit with OkHttp
- **UI**: Material Design 3 components

## Troubleshooting
If the app crashes on startup:
1. Check that all required permissions are granted
2. Verify internet connectivity
3. Ensure the API configuration is correct
4. Check the logcat for detailed error messages

## Dependencies
- AndroidX Core KTX
- Material Design 3
- Retrofit for API calls
- Room for database
- Coroutines for async operations
- OkHttp for networking

## Building
```bash
# Build debug APK
./gradlew assembleDebug

# Install on connected device/emulator
./gradlew installDebug

# Build release APK
./gradlew assembleRelease
```

## License
This project is proprietary to Temenos. 