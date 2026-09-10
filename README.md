# EuroScope AIRAC Updater

A modular Python tool for automatically updating EuroScope AIRAC packages with **completely customizable** preferences and user settings.

## Features

- **Auto-download** packages for supported FIRs
- **Automatic backup** of existing configurations
- **Profile updates** with VATSIM credentials and preferences
- **Customizable settings** - no hardcoded preferences!
- **JSON-based configuration** - easy to edit and share
- **NavData integration** for Navigraph users
- **Modular design** - easy to extend with new FIRs and settings

## Philosophy: Your Setup, Your Way

Every setting is configurable via JSON files. Don't like the default screen positions? Change them. Want different List positions? Configure them. Need custom file modifications? Add them. 

The script provides intelligent defaults but respects your choices completely.

## Supported FIRs

- **EDGG** - Germany (Full Package)
- **EDMM** - Munich (Full Package)  
- **EDWW** - Bremen (Full Package)
- **EDXX** - Germany FIS
- **EXCXO** - Shanwick Oceanic
- **BIRD** - Iceland
- **LPPO** - Portugal

## Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```pip install -r requirements.txt```

## First-Time Setup

1. **Run the script** for the first time to create the configuration file:
   ```
   python main.py EDGG
   ```

3. **Edit the generated `config.ini`** with your settings:
   ```ini
   [LOGIN]
   cid = 1234567
   password = your_password
   name = Your Name
   rating = 3 # S1=1, S2=2, S3=3, C1=4, C3=5
   initials = ABC
   hoppie = your_hoppie_code
   
   [PATHS]
   download_dir = C:\Users\YourName\Downloads
   euroscope_docs = C:\Users\YourName\AppData\Roaming\EuroScope
   # ... etc
   ```

## Usage

### Basic Usage

```bash
# Auto-download and install EDGG package
python main.py EDGG

# Install from existing ZIP file
python main.py EDGG-Full-Package_20250613220519-241301-0016.zip

# Use custom config file
python main.py EDGG -c my_config.ini
```

### Advanced Options

```bash
# Skip backup creation
python main.py EDGG --no-backup

# Dry run (show what would be done without making changes)
python main.py EDGG --dry-run

# Help
python main.py --help
```

## Configuration File

The `config.ini` file contains all your personal settings:

### [PATHS] Section
- `download_dir` - Where packages are downloaded
- `euroscope_docs` - EuroScope documents directory  
- `euroscope_app` - EuroScope application directory
- `backup_dir` - Where backups are stored
- `navdata_dir` - NavData directory (for Navigraph users)
- `custom_files_dir` - Custom files to copy

### [LOGIN] Section
- `cid` - Your VATSIM ID
- `password` - Your VATSIM password
- `name` - Your real name
- `rating` - Your controller rating (1=S1, 2=S2, 3=S3, etc.)
- `initials` - Your initials for observer callsign
- `hoppie` - Your Hoppie code for CPDLC

### [SETTINGS] Section
- `text_size` - Text size for displays (optional)

### [VCCS] Section
- Voice communication settings (optional)

### [OPTIONS] Section
- `use_subdirs` - Use subdirectories for each package
- `use_custom_files` - Copy custom files
- `delete_package` - Delete package after installation

## Custom Settings System

The script uses a simple, direct Python-based custom settings system. **You write simple Python code to customize whatever you want!**

### How It Works

1. **Open `custom_settings.py`**
2. **Find your FIR section** (e.g., `_apply_edgg_settings`)
3. **Modify, add, or comment out** settings as you like
4. **Use the helper methods** to make any changes you want

### Example: Customize EDGG Settings

```python
def _apply_edgg_settings(self, base_dir: Path):
    # Change screen to monitor 1 instead of 0
    self.update_file(base_dir / "EDGG/Settings/EDGG/EDGG_Screen.txt", {
        'm_ScreenNumber': '1',  # Changed from '0' to '1'
        'm_ScreenPosition': '6',
        'm_MetarListX': '1500'  # Moved METAR list
    })
    
    # Don't want TopSky window changes? Just comment them out:
    # self.update_file(base_dir / "EDGG/Plugins/Topsky/...", {...})
```

### Helper Methods

```python
# Update any settings file
self.update_file(file_path, {'setting': 'value'})

# Update all profile files  
self.update_all_profiles(base_dir, {'TsVccsMiniControlX': '1600'})

# Update specific profiles only
self.update_profiles(base_dir, "*TWR*.prf", {'setting': 'value'})

# Find and replace text
self.replace_in_file(file_path, r'old_text', 'new_text')

# Add lines at the end of a file
self.add_lines_to_file(file_path, ['line1', 'line2',])

# Add lines only if they aren't already there (safe to re-run each AIRAC)
self.add_lines_if_missing(file_path, ['Plugin:KeyA:1', 'Plugin:KeyB:2'])

# Copy files around
self.copy_file(source_file, target_file)
```

### Adding a New FIR

1. **Add your method**:
```python
def _apply_myfir_settings(self, base_dir: Path):
    self.update_file(base_dir / "MYFIR/Settings/Screen.txt", {
        'm_ScreenNumber': '0',
        'm_ScreenPosition': '6'
    })
```

2. **Register it**:
```python
elif fir_code == 'MYFIR':
    self._apply_myfir_settings(base_dir)
```

### Want No Customizations?

Just comment out everything in your FIR's section or set the method to `pass`:

```python
def _apply_edgg_settings(self, base_dir: Path):
    pass  # No customizations
```
## What Gets Updated

The script automatically updates:

### Always Updated:
- VATSIM login credentials  
- Observer callsign
- Hoppie code for CPDLC
- NavData files (if available)
- Custom files (if enabled)

### Configurable via Custom Settings:
- ⚙️ **Screen positions and layout** - Completely customizable per FIR
- ⚙️ **VCCS settings** - Voice communication positions  
- ⚙️ **Text sizes** - If configured in settings
- ⚙️ **Window positions** - TopSky, METAR lists, controller lists, etc.
- ⚙️ **FIR-specific preferences** - ATIS URLs, sector settings, etc.
- ⚙️ **Any file modification** - Regex replacements, value updates, etc.

If you don't like any setting, just disable it or change it in the JSON files.

## License

This tool is provided as-is for the VATSIM community. Use at your own risk and always backup your EuroScope configuration before using.
