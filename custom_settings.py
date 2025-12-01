import re
from pathlib import Path
from typing import Dict, List, Tuple


class CustomSettings:
    def __init__(self, config):
        self.config = config

    def _get_base_dir(self, package_info: Dict[str, str]) -> Path:
        """Get base directory for the package"""
        base_dir = self.config.euroscope_docs

        if self.config.use_subdirs:
            base_dir = base_dir / package_info["fir"]

        return base_dir

    def apply_all_settings(self, package_info: Dict[str, str]):
        """Apply all custom settings for the package"""
        print("⚙️  Applying custom settings...")

        fir_code = package_info["fir"]
        base_dir = self._get_base_dir(package_info)

        # Apply your custom settings here!

        # ========================================
        # GENERAL SETTINGS (All FIRs)
        # ========================================

        # Set VCCS Mini position for all profiles
        self.update_all_profiles(
            base_dir, {"TsVccsMiniControlX": "2421", "TsVccsMiniControlY": "26"}
        )

        # Special VCCS position for TWR profiles
        self.update_profiles(base_dir, "*TWR*.prf", {"TsVccsMiniControlX": "2361"})

        # ========================================
        # FIR-SPECIFIC SETTINGS
        # ========================================

        if fir_code == "EDGG":
            self._apply_edgg_settings(base_dir)
        elif fir_code == "EDMM":
            self._apply_edmm_settings(base_dir)
        elif fir_code == "EDWW":
            self._apply_edww_settings(base_dir)
        elif fir_code == "EDXX":
            self._apply_edxx_settings(base_dir)
        elif fir_code == "EXCXO":
            self._apply_excxo_settings(base_dir)

        print(f"   ✓ Applied custom settings for {fir_code}")

    # ============================================================================
    # FIR-SPECIFIC SETTINGS - CUSTOMIZE THESE AS NEEDED
    # ============================================================================

    def _apply_edgg_settings(self, base_dir: Path):
        # ===== EDGG Main Radar Screen =====
        self.update_file(
            base_dir / "EDGG/Settings/EDGG/EDGG_Screen.txt",
            {
                "m_ScreenNumber": "0",
                "m_ScreenPosition": "0",
                "m_ScreenMaximized": "0",
                "m_MetarListX": "1431",
                "m_MetarListY": "44",
                "m_ControllerListX": "2425",
                "m_ControllerListY": "44",
            },
        )

        # ===== EDGG TopSky Settings =====
        self.update_file(
            base_dir / "EDGG/Plugins/Topsky/EDGG/TopSkySettings.txt",
            {
                "Window_ASM": "0,80,120,570,300",
                "Window_QNHTL": "0,1637,551",
                "Window_CARD": "0,1565,755",
                "Window_LFUNCFP": "0,1570,44",
                "Window_CPDLC_Current": "0,0,650",
                "Window_CPDLC_Setting": "1,0,471",
            },
            delimiter="=",
        )

        # ===== EDGG Plugin Settings - Hide Traffic Management Lists =====
        self.replace_in_file(
            base_dir / "EDGG/Settings/EDGG/EDGG_Plugins.txt",
            r"TopSky plugin:ACList/Traffic Management List 1/m_Visible:1",
            "TopSky plugin:ACList/Traffic Management List 1/m_Visible:0",
        )
        self.replace_in_file(
            base_dir / "EDGG/Settings/EDGG/EDGG_Plugins.txt",
            r"TopSky plugin:ACList/Traffic Management List 2/m_Visible:1",
            "TopSky plugin:ACList/Traffic Management List 2/m_Visible:0",
        )

        # ===== EDUU Screen Settings =====
        self.update_file(
            base_dir / "EDGG/Settings/EDUU/EDUU_Screen.txt",
            {"m_ScreenNumber": "0", "m_ScreenPosition": "0", "m_ScreenMaximized": "0"},
        )

        # ===== EDYY Screen Settings =====
        self.update_file(
            base_dir / "EDGG/Settings/EDYY/EDYY_Screen.txt",
            {"m_ScreenNumber": "0", "m_ScreenPosition": "0", "m_ScreenMaximized": "0"},
        )

        # ===== PHX (Tower) Screen Settings =====
        self.update_file(
            base_dir / "EDGG/Settings/PHX/PHX_Screen.txt",
            {
                "m_ScreenMaximized": "0",
                "m_MetarListX": "713",
                "m_MetarListY": "45",
                "m_VoiceListX": "1857",
                "m_VoiceListY": "381",
                "m_ControllerListX": "712",
                "m_ControllerListY": "77",
            },
        )

        # ===== PHX Symbology Night Settings =====
        self.update_file(
            base_dir / "EDGG/Settings/PHX/PHX_Symbology_Night.txt",
            {
                "Datablock:AC list background": "0:3.2:0:0:7",
                "Other:list header": "11447982:3.5:0:0:7",
                "Controller:normal": "16777215:3.5:0:0:7",
                "Controller:breaking": "4227327:3.5:0:0:7",
                "Controller:timeout": "255:4.0:0:0:7",
                "Metar:normal": "11447982:3.5:0:0:7",
                "Metar:modified": "33023:3.5:0:0:7",
                "Metar:timeout": "255:3.5:0:0:7",
                "Other:freetext": "8454143:3.5:0:1:7",
                "Chat:background": "0:3.5:0:0:7",
                "Chat:name normal": "10790052:3.5:0:0:7",
                "Chat:name unread": "16777215:3.5:0:0:7",
            },
        )

        # ===== EDGG Departure List Settings =====
        self.update_file(
            base_dir / "EDGG/Settings/EDGG/EDGG_DepartureList.txt", {"m_X": "712"}
        )

        # ===== PHX Startup List Settings =====
        self.update_file(
            base_dir / "EDGG/Settings/PHX/PHX_StartupList.txt", {"m_Visible": "0"}
        )

        # ===== Traffic Management List Positions =====
        self.replace_in_file(
            base_dir / "EDGG/Settings/EDGG/EDGG_Plugins.txt",
            r"Traffic Management List 1/m_X:\d+",
            "Traffic Management List 1/m_X:0",
        )
        self.replace_in_file(
            base_dir / "EDGG/Settings/EDGG/EDGG_Plugins.txt",
            r"Traffic Management List 1/m_Y:\d+",
            "Traffic Management List 1/m_Y:1005",
        )
        self.replace_in_file(
            base_dir / "EDGG/Settings/EDGG/EDGG_Plugins.txt",
            r"Traffic Management List 2/m_X:\d+",
            "Traffic Management List 2/m_X:368",
        )
        self.replace_in_file(
            base_dir / "EDGG/Settings/EDGG/EDGG_Plugins.txt",
            r"Traffic Management List 2/m_Y:\d+",
            "Traffic Management List 2/m_Y:1005",
        )

        # ===== General Settings - Set active airports by sectors =====
        self.update_file(
            base_dir / "EDGG/Settings/EDGG/EDGG_General.txt",
            {"SET_SetActiveAptBySectors": "1"},
        )

        # ===== Fix ATIS URL =====
        self.replace_in_profiles(
            base_dir,
            "EDGG_*.prf",
            [(r"&atistype=.{3}&", "&"), (r"&depfreq=", "&atistype=&depfreq=")],
        )

        self.replace_in_file(
            base_dir / "EDGG/Settings/EDGG/EDGG_General.txt", r"&atistype=.{3}&", "&"
        )
        self.replace_in_file(
            base_dir / "EDGG/Settings/EDGG/EDGG_General.txt",
            r"&depfreq=",
            "&atistype=&depfreq=",
        )

        # ===== GRP Plugin Settings =====
        grp_maps_file = base_dir / "EDGG/Plugins/GRP/TWR_PHX_NIGHT/GRpluginMaps.txt"
        if grp_maps_file.exists():
            try:
                with open(grp_maps_file, "r", encoding="iso-8859-1") as f:
                    content = f.read()

                # Disable Leadin Lines for EDDL
                content = re.sub(
                    r"(MAP:Leadin Lines\s+AIRPORT:EDDL\s+FOLDER:Airport Layout\s+ACTIVE:)1",
                    r"\g<1>0",
                    content,
                    flags=re.MULTILINE,
                )

                # Disable Checkpoint labels for EDDL
                content = re.sub(
                    r"(MAP:Checkpoints\s+AIRPORT:EDDL\s+FOLDER:Labels\s+ACTIVE:)1",
                    r"\g<1>0",
                    content,
                    flags=re.MULTILINE,
                )

                # Disable EDDL Stand labels
                content = re.sub(
                    r"(MAP:Stands\s+AIRPORT:EDDL\s+FOLDER:Labels\s+ACTIVE:)1",
                    r"\g<1>0",
                    content,
                    flags=re.MULTILINE,
                )

                # Disable EDDL Area labels
                content = re.sub(
                    r"(MAP:Areas\s+AIRPORT:EDDL\s+FOLDER:Labels\s+ACTIVE:)1",
                    r"\g<1>0",
                    content,
                    flags=re.MULTILINE,
                )

                with open(grp_maps_file, "w", encoding="iso-8859-1") as f:
                    f.write(content)

                print(f"      ✓ Updated GRP plugin maps - disabled EDDL features")

            except Exception as e:
                print(f"      ⚠️  Error updating GRP plugin maps: {e}")

        # ===== TopSky Maps - Add ACTIVE runway conditions for EDDL downwind patterns =====
        topsky_maps_file = base_dir / "EDGG/Plugins/Topsky/EDGG/TopSkyMaps.txt"
        if topsky_maps_file.exists():
            try:
                with open(topsky_maps_file, "r", encoding="iso-8859-1") as f:
                    content = f.read()

                content = re.sub(
                    r"(MAP:DOWNWIND 05\s+COLOR:standard\s+FOLDER:EDDL\s+)(ZOOM:)",
                    r"\1ACTIVE:RWY:ARR:EDDL05L:DEP:*\nACTIVE:RWY:ARR:EDDL05R:DEP:*\n\2",
                    content,
                    flags=re.MULTILINE,
                )

                content = re.sub(
                    r"(MAP:DOWNWIND 23\s+COLOR:standard\s+FOLDER:EDDL\s+)(ZOOM:)",
                    r"\1ACTIVE:RWY:ARR:EDDL23R:DEP:*\nACTIVE:RWY:ARR:EDDL23L:DEP:*\n\2",
                    content,
                    flags=re.MULTILINE,
                )

                with open(topsky_maps_file, "w", encoding="iso-8859-1") as f:
                    f.write(content)

                print(
                    f"      ✓ Updated TopSky maps - added ACTIVE runway conditions for EDDL downwind patterns"
                )

            except Exception as e:
                print(f"      ⚠️  Error updating Langen TopSky maps: {e}")

        topsky_maps_file = base_dir / "EDGG/Plugins/Topsky/TWR_PHX_NIGHT/TopSkyMaps.txt"
        if topsky_maps_file.exists():
            try:
                with open(topsky_maps_file, "r", encoding="iso-8859-1") as f:
                    content = f.read()

                # remove urban area from all tower profiles
                content = re.sub(
                    r"(MAP:Urban Area\s+FOLDER:Topography\s+ASRDATA:PHOENIX\s+LAYER:-4\s+)ACTIVE:ID:\*:DFC,DFGW,DFGC,DFGE,DFGI,DFG,DFTC,DFTS,DFTN,DFTW,DFAN,DFAS,DFANT,DFAST:\*:\*\s+AND_ACTIVE:ID:\*:DLC,DLGE,DLGW,DLT,DLA,DLAT,DLD,BOT:\*:\*\s+AND_ACTIVE:ID:\*:DKC,DKG,DKT,DKA,DKAT,NOR:\*:\*(\s+COLOR:)",
                    r"\1ACTIVE:0\2",
                    content,
                    flags=re.MULTILINE,
                )

                # remove highway from all tower profiles
                content = re.sub(
                    r"(MAP:Highways\s+FOLDER:Topography\s+ASRDATA:PHOENIX\s+LAYER:-2\s+COLOR:topo_road\s+STYLE:Solid:1\s+)ACTIVE:ID:\*:DFC,DFGW,DFGC,DFGE,DFGI,DFG,DFTC,DFTS,DFTN,DFTW,DFAN,DFAS,DFANT,DFAST:\*:\*\s+AND_ACTIVE:ID:\*:DLC,DLGE,DLGW,DLT,DLA,DLAT,DLD,BOT:\*:\*\s+AND_ACTIVE:ID:\*:DKC,DKG,DKT,DKA,DKAT,NOR:\*:\*(\s+COORD:)",
                    r"\1ACTIVE:0\2",
                    content,
                    flags=re.MULTILINE,
                )

                with open(topsky_maps_file, "w", encoding="iso-8859-1") as f:
                    f.write(content)

                print(
                    f"      ✓ Updated TopSky maps for TWR PHX - removed urban area and highway"
                )

            except Exception as e:
                print(f"      ⚠️  Error updating TWR TopSky maps: {e}")

    def _apply_edmm_settings(self, base_dir: Path):
        """EDMM-specific settings - modify as you like!"""

        # Screen settings
        self.update_file(
            base_dir / "EDMM/Settings/iCAS2/Screen.txt",
            {
                "m_ScreenNumber": "0",
                "m_ScreenPosition": "0",
                "m_ScreenMaximized": "0",
                "m_MetarListX": "1431",
                "m_MetarListY": "45",
                "m_ControllerListX": "1574",
                "m_ControllerListY": "45",
            },
        )

        self.update_file(
            base_dir / "EDMM/Settings/TWR_PHX/Screen.txt",
            {
                "m_ScreenNumber": "0",
                "m_ScreenPosition": "0",
                "m_ScreenMaximized": "0",
                "m_MetarListX": "1431",
                "m_MetarListY": "45",
                "m_ControllerListX": "1574",
                "m_ControllerListY": "45",
            },
        )
        
        self._update_edmm_twr_night_recent_files(base_dir)

    def _apply_edww_settings(self, base_dir: Path):
        """EDWW-specific settings - modify as you like!"""
        

        screen_files = [
            "EDWW/Settings/Settings EDWW/SCREEN.txt",
            "EDWW/Settings/Settings EDUU/SCREEN.txt",
            "EDWW/Settings/Settings EDYY/SCREEN.txt",
            "EDWW/Settings/Settings PHX/SCREEN.txt",
        ]

        for screen_file in screen_files:
            self.update_file(
                base_dir / screen_file,
                {
                    "m_ScreenNumber": "0",
                    "m_ScreenPosition": "0",
                    "m_ScreenMaximized": "0",
                },
            )

        # Additional EDWW-specific settings
        self.update_file(
            base_dir / "EDWW/Settings/Settings EDWW/SCREEN.txt",
            {
                "m_MetarListX": "713",
                "m_MetarListY": "45",
                "m_VoiceListX": "1857",
                "m_VoiceListY": "381",
                "m_ControllerListX": "712",
                "m_ControllerListY": "77",
            },
        )

        # ===== PHX Symbology Night Settings =====
        self.update_file(
            base_dir / "EDWW/Settings/Settings PHX/SYMBOLOGY NIGHT.txt",
            {
                "Datablock:AC list background": "0:3.2:0:0:7",
                "Other:list header": "11447982:3.5:0:0:7",
                "Controller:normal": "16777215:3.5:0:0:7",
                "Controller:breaking": "4227327:3.5:0:0:7",
                "Controller:timeout": "255:4.0:0:0:7",
                "Metar:normal": "11447982:3.5:0:0:7",
                "Metar:modified": "33023:3.5:0:0:7",
                "Metar:timeout": "255:3.5:0:0:7",
                "Other:freetext": "8454143:3.5:0:1:7",
                "Chat:background": "0:3.5:0:0:7",
                "Chat:name normal": "10790052:3.5:0:0:7",
                "Chat:name unread": "16777215:3.5:0:0:7",
            },
        )

        # ===== EDWW Departure List Settings =====
        self.update_file(
            base_dir / "EDWW/Settings/Settings PHX/DEP.txt",
            {
                "m_X": "0",
                "m_Y": "45",
            },
        )

        # TopSky window positions
        self.update_file(
            base_dir / "EDWW/Plugins/TOPSKY EDWW/TopSkySettings.txt",
            {
                "Window_ASM": "0,80,120,570,300",
                "Window_QNHTL": "0,1637,551",
                "Window_CARD": "0,1565,755",
                "Window_LFUNCFP": "0,1570,44",
                "Window_CPDLC_Current": "0,0,650",
                "Window_CPDLC_Setting": "1,0,471",
            },
            delimiter="=",
        )
        
        self._update_edww_twr_night_recent_files(base_dir)

    def _apply_edxx_settings(self, base_dir: Path):
        """EDXX (FIS) specific settings - modify as you like!"""

        # Screen settings
        self.update_file(
            base_dir / "EDXX/Settings/Screen.txt",
            {
                "m_ScreenNumber": "0",
                "m_ScreenPosition": "0",
                "m_ScreenMaximized": "0",
                "m_MetarListX": "1431",
                "m_MetarListY": "44",
                "m_ControllerListX": "2425",
                "m_ControllerListY": "44",
            },
        )

        # Update airport name color and size
        self.update_file(
            base_dir / "EDXX/Settings/Symbology.txt",
            {"Airports:name": "11053224:3.5:0:0:1"},
        )

        # TopSky window positions
        self.update_file(
            base_dir / "EDXX/Plugins/TopSky/TopSkySettings.txt",
            {"Window_QNHTL": "0,1422,974", "Window_FlightPlanSelect": "3,500,45"},
            delimiter="=",
        )

    def _apply_excxo_settings(self, base_dir: Path):
        """EXCXO-specific settings - modify as you like!"""

        self.update_file(
            base_dir / "EXCXO/Settings/Screen Layout.txt",
            {
                "m_ScreenNumber": "0",
                "m_ScreenPosition": "0",
                "m_ScreenMaximized": "0",
                "m_ControllerListX": "3281",
                "m_ControllerListY": "45",
            },
        )
        
    def _update_edww_twr_night_recent_files(self, base_dir: Path):
        if self.config.use_subdirs:
            twr_night_profile = base_dir / "EDWW FIR - TWR PHX NIGHT.prf"
        else:
            twr_night_profile = base_dir / "EDWW/EDWW FIR - TWR PHX NIGHT.prf"
        
        if not twr_night_profile.exists():
            print("      ⚠️  EDWW TWR Night profile not found")
            return

        try:
            with open(twr_night_profile, "r", encoding="iso-8859-1") as f:
                lines = f.readlines()

            # Find and remove existing RecentFiles entries
            filtered_lines = [line for line in lines if not line.startswith("RecentFiles\t")]

            # Add new RecentFiles entries at the end
            new_recent_files = [
                "RecentFiles\tRecent1\t\\EDWW\\ASR\\EDWW-TWR.asr\n",
                "RecentFiles\tRecent2\t\\EDWW\\ASR\\EDDB_GND.asr\n",
                "RecentFiles\tRecent3\t\\EDWW\\ASR\\EDDH_GND.asr\n"
            ]
            
            filtered_lines.extend(new_recent_files)

            with open(twr_night_profile, "w", encoding="iso-8859-1") as f:
                f.writelines(filtered_lines)

            print(f"      ✓ Updated recent files in EDWW TWR Night profile")

        except Exception as e:
            print(f"      ⚠️  Error updating EDWW TWR Night recent files: {e}")

    def _update_edmm_twr_night_recent_files(self, base_dir: Path):
        if self.config.use_subdirs:
            twr_night_profile = base_dir / "TWR_PHX_NIGHT.prf"
        else:
            twr_night_profile = base_dir / "EDMM/TWR_PHX_NIGHT.prf"
        
        if not twr_night_profile.exists():
            print("      ⚠️  EDMM TWR PHX Night profile not found")
            return

        try:
            with open(twr_night_profile, "r", encoding="iso-8859-1") as f:
                lines = f.readlines()

            # Find and remove existing RecentFiles entries
            filtered_lines = [line for line in lines if not line.startswith("RecentFiles\t")]

            # Add new RecentFiles entries at the end
            new_recent_files = [
                "RecentFiles\tRecent1\t\\EDMM\\ASR\\TWR_PHX\\EDDM_GND.asr\n",
                "RecentFiles\tRecent2\t\\EDMM\\ASR\\TWR_PHX\\ALL_EDMM_TWR.asr\n"
            ]
            
            filtered_lines.extend(new_recent_files)

            with open(twr_night_profile, "w", encoding="iso-8859-1") as f:
                f.writelines(filtered_lines)

            print(f"      ✓ Updated recent files in EDMM TWR PHX Night profile")

        except Exception as e:
            print(f"      ⚠️  Error updating EDMM TWR PHX Night recent files: {e}")


    # ============================================================================
    # HELPER METHODS - USE THESE TO CREATE CUSTOMIZATIONS
    # ============================================================================

    def update_file(
        self, file_path: Path, updates: Dict[str, str], delimiter: str = ":"
    ):
        """
        Update a settings file with new values

        Args:
            file_path: Path to the file to update
            updates: Dictionary of {setting_name: new_value}
            delimiter: Character that separates setting from value (':' or '=')

        Example:
            self.update_file(base_dir / "MyFIR/Settings/Screen.txt", {
                'm_ScreenNumber': '1',
                'm_MetarListX': '1500'
            })
        """
        if not file_path.exists():
            return

        try:
            with open(file_path, "r", encoding="iso-8859-1") as f:
                content = f.read()

            for setting, value in updates.items():
                pattern = rf"^{re.escape(setting)}{re.escape(delimiter)}.+$"
                replacement = f"{setting}{delimiter}{value}"
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

            with open(file_path, "w", encoding="iso-8859-1") as f:
                f.write(content)

            print(f"      ✓ Updated {len(updates)} settings in {file_path.name}")

        except Exception as e:
            print(f"      ⚠️  Error updating {file_path.name}: {e}")

    def update_profiles(self, base_dir: Path, pattern: str, updates: Dict[str, str]):
        """
        Update profile files (.prf) with new settings

        Args:
            base_dir: Base directory to search in
            pattern: File pattern to match (e.g., "*.prf", "*TWR*.prf", "EDGG_*.prf")
            updates: Dictionary of {setting_name: new_value}

        Example:
            self.update_profiles(base_dir, "*TWR*.prf", {
                'TsVccsMiniControlX': '1327'
            })
        """
        files_updated = 0
        for prf_file in base_dir.rglob(pattern):
            for setting, value in updates.items():
                self.replace_in_file(
                    prf_file, rf"{re.escape(setting)}\t.+", f"{setting}\t{value}"
                )
            files_updated += 1

        if files_updated > 0:
            print(
                f"      ✓ Updated {len(updates)} settings in {files_updated} profile files"
            )

    def update_all_profiles(self, base_dir: Path, updates: Dict[str, str]):
        """Update all .prf files with settings - convenience method"""
        self.update_profiles(base_dir, "*.prf", updates)

    def replace_in_profiles(
        self, base_dir: Path, pattern: str, replacements: List[Tuple[str, str]]
    ):
        """
        Apply regex replacements to profile files

        Args:
            base_dir: Base directory to search in
            pattern: File pattern to match
            replacements: List of (regex_pattern, replacement) tuples

        Example:
            self.replace_in_profiles(base_dir, "EDGG_*.prf", [
                (r'&atistype=.{3}&', '&'),
                (r'&depfreq=', '&atistype=&depfreq=')
            ])
        """
        files_updated = 0
        for prf_file in base_dir.rglob(pattern):
            for regex_pattern, replacement in replacements:
                self.replace_in_file(prf_file, regex_pattern, replacement)
            files_updated += 1

        if files_updated > 0:
            print(
                f"      ✓ Applied {len(replacements)} replacements to {files_updated} profile files"
            )

    def replace_in_file(self, file_path: Path, pattern: str, replacement: str):
        """
        Apply a regex replacement to any file

        Args:
            file_path: Path to the file
            pattern: Regex pattern to find
            replacement: Text to replace with

        Example:
            self.replace_in_file(my_file, r'old_text', 'new_text')
        """
        if not file_path.exists():
            return

        try:
            with open(file_path, "r", encoding="iso-8859-1") as f:
                content = f.read()

            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

            if new_content != content:
                with open(file_path, "w", encoding="iso-8859-1") as f:
                    f.write(new_content)

        except Exception as e:
            print(f"      ⚠️  Error updating {file_path.name}: {e}")

def add_lines_to_file(self, file_path: Path, lines_to_add):
    """
    Add lines at the end of any file
    Args:
        file_path: Path to the file
        lines_to_add: The lines you want to add
    Example:
        self.add_lines_to_file(file_path, ['line1', 'line2',])
    """
    if not file_path.exists():
        return

    try:
        with open(file_path, "a", encoding="iso-8859-1") as f:
            f.write("\n")
            for line in lines_to_add:
                f.write(line + "\n")

        print(f"      ✓ Added {len(lines_to_add)} lines in {file_path.name}")

    except Exception as e:
        print(f"      ⚠️  Error updating {file_path.name}: {e}")


def copy_file(self, source: Path, target: Path):
    """Copy a file - useful for custom file operations"""
    try:
        import shutil

        shutil.copy2(source, target)
        print(f"      ✓ Copied {source.name} to {target}")
    except Exception as e:
        print(f"      ⚠️  Error copying {source.name}: {e}")


# ================================================================================
# ADDING YOUR OWN CUSTOMIZATIONS
# ================================================================================
"""
To add custom settings for a new FIR or modify existing ones:

1. Add a new method like _apply_myfir_settings(self, base_dir)
2. Call it from apply_all_settings() 
3. Use the helper methods to make changes

Example for a new FIR:

def _apply_myfir_settings(self, base_dir: Path):
    # Update screen settings
    self.update_file(base_dir / "MYFIR/Settings/Screen.txt", {
        'm_ScreenNumber': '1',
        'm_ScreenPosition': '6'
    })
    
    # Update all profiles
    self.update_all_profiles(base_dir, {
        'TsVccsMiniControlX': '1600'
    })
    
    # Custom regex replacements
    self.replace_in_profiles(base_dir, "MYFIR_*.prf", [
        (r'old_pattern', 'new_text')
    ])
    
    # Copy custom files
    custom_file = Path("my_custom_file.txt")
    if custom_file.exists():
        self.copy_file(custom_file, base_dir / "MYFIR/MyFile.txt")

Then add to apply_all_settings():
elif fir_code == 'MYFIR':
    self._apply_myfir_settings(base_dir)

HELPER METHODS SUMMARY:

update_file(file_path, updates, delimiter=':')
    - Update colon or equals delimited files
    - e.g., update_file(screen_file, {'m_ScreenNumber': '1'})

update_profiles(base_dir, pattern, updates)  
    - Update .prf files matching pattern
    - e.g., update_profiles(base_dir, "*TWR*.prf", {'Setting': 'Value'})

update_all_profiles(base_dir, updates)
    - Update all .prf files
    - e.g., update_all_profiles(base_dir, {'TsVccsMiniControlX': '1529'})

replace_in_profiles(base_dir, pattern, replacements)
    - Apply regex replacements to profiles
    - e.g., replace_in_profiles(base_dir, "*.prf", [('old', 'new')])

replace_in_file(file_path, pattern, replacement)
    - Apply regex replacement to any file
    - e.g., replace_in_file(my_file, r'pattern', 'replacement')

copy_file(source, target)
    - Copy files around
    - e.g., copy_file(custom_file, target_location)
"""
