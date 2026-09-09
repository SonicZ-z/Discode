# Discode Android App

This is the Android app version of the Discode Discord Bot Manager. It allows you to create, manage, and control Discord bots directly from your Android device.

## Features

- Create and manage multiple Discord bots
- Add custom commands to each bot
- Create and manage plugins
- Start/stop bots with one tap
- View bot status and information
- Clean, modern Material Design UI

## Building the APK

### Prerequisites

- Android Studio (latest version)
- Java JDK 17 or later
- Android SDK with API 34

### Steps

1. Open Android Studio
2. Click "Open an Existing Project"
3. Navigate to the `app` folder in this repository
4. Wait for Gradle to sync
5. Click "Build" > "Build Bundle(s) / APK(s)" > "Build APK"
6. Once built, the APK will be in `app/build/outputs/apk/debug/`

### Building Release APK

To build a signed release APK:

1. Generate a keystore file (if you don't have one):
   ```bash
   keytool -genkey -v -keystore discode-release.keystore -alias discode -keyalg RSA -keysize 2048 -validity 10000
   ```

2. Create a `keystore.properties` file in the `app` directory with:
   ```properties
   storePassword=yourpassword
   keyPassword=yourpassword
   keyAlias=discode
   storeFile=discode-release.keystore
   ```

3. In Android Studio:
   - Click "Build" > "Generate Signed Bundle / APK"
   - Select "APK"
   - Choose your keystore
   - Enter passwords
   - Select "release" build type
   - Click "Finish"

4. The signed APK will be in `app/release/`

## App Structure

```
app/
├── src/
│   └── main/
│       ├── java/com/discode/app/
│       │   ├── MainActivity.java      # Main menu
│       │   ├── BotActivity.java       # Bot management
│       │   ├── CommandActivity.java   # Command management
│       │   ├── PluginActivity.java     # Plugin management
│       │   ├── SettingsActivity.java   # App settings
│       │   ├── AboutActivity.java      # About page with credits
│       │   ├── BotConfig.java          # Bot configuration model
│       │   ├── BotCommand.java         # Command model
│       │   └── AppDatabase.java        # Local database using SharedPreferences
│       └── res/
│           ├── layout/                 # All activity layouts
│           ├── drawable/               # Icons and backgrounds
│           └── values/                 # Strings, colors, styles
└── build.gradle                        # App build configuration
```

## Activities

### MainActivity
The main dashboard with buttons to access:
- Bots Manager
- Commands Manager
- Plugins Manager
- Settings
- About

### BotActivity
Manage your Discord bots:
- View list of all bots
- Create new bots
- Edit existing bots
- Start/stop bots
- Delete bots
- Access bot-specific commands

### CommandActivity
Manage commands for a specific bot:
- View all commands
- Add new commands
- Edit existing commands
- Delete commands

### PluginActivity
Manage plugins:
- View all plugins
- Create new plugins
- View plugin code
- Delete plugins

### SettingsActivity
App settings:
- Set default bot

### AboutActivity
Information about the app including:
- Version
- Description
- Credits

## Credits

- **SonicZ-z**: Original code and concept creator
- **Vibe Code**: Android app development, fixing errors, and improvements

## License

MIT License - see the LICENSE file in the parent directory for details.
