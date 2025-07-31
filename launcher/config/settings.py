"""
Settings management for TKA Unified Launcher.
Enhanced with state persistence and smart initialization.
"""

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Optional


@dataclass
class LauncherSettings:
    """Launcher configuration settings with enhanced state persistence."""

    # UI Settings
    launch_mode: str = "docked"  # "window" or "docked" - default to docked
    window_width: int = 1000
    window_height: int = 700
    window_x: Optional[int] = None
    window_y: Optional[int] = None
    target_screen_index: int = 0  # Which screen to use (0 = primary)
    last_window_geometry: Optional[dict[str, int]] = None  # x, y, width, height

    # Docked Mode Settings
    dock_position: str = "left"  # "left", "right", "top", "bottom"
    dock_screen: int = 0  # Screen index (0 = primary, 1 = secondary, etc.)
    dock_width: int = 110  # Optimized dock width
    dock_offset_ratio: float = 0.0  # Position ratio along screen edge (0 = top/left)
    dock_auto_hide: bool = False
    dock_icon_size: int = 48
    dock_last_geometry: Optional[dict[str, int]] = None  # Store last dock position

    # Behavior Settings
    auto_start_docked: bool = True  # Start in dock mode by default
    confirm_dangerous_actions: bool = True
    show_tooltips: bool = True
    enable_animations: bool = True

    # Theme Settings
    theme: str = "auto"  # "light", "dark", "auto"
    accent_color: str = "#6366f1"
    font_family: str = "Inter"
    font_size: int = 10

    # Advanced Settings
    log_level: str = "INFO"
    enable_debug_mode: bool = False
    auto_save_settings: bool = True
    check_for_updates: bool = True


class SettingsManager:
    """Manages launcher settings persistence with enhanced state management."""

    def __init__(self, settings_path: Optional[Path] = None):
        if settings_path is None:
            settings_path = Path.home() / ".tka" / "launcher_settings.json"
        self.settings_path = settings_path
        self.settings = LauncherSettings()
        self.load_settings()

    def load_settings(self):
        """Load settings from file."""
        if self.settings_path.exists():
            try:
                with open(self.settings_path, encoding="utf-8") as f:
                    data = json.load(f)

                # Update settings with loaded data
                for key, value in data.items():
                    if hasattr(self.settings, key):
                        setattr(self.settings, key, value)

            except Exception as e:
                print(f"⚠️ Failed to load settings: {e}")
                # Keep default settings

    def save_settings(self):
        """Save current settings to file."""
        try:
            self.settings_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(asdict(self.settings), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Failed to save settings: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return getattr(self.settings, key, default)

    def set(self, key: str, value: Any):
        """Set a setting value."""
        if hasattr(self.settings, key):
            setattr(self.settings, key, value)
            if self.settings.auto_save_settings:
                self.save_settings()

    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.settings = LauncherSettings()
        self.save_settings()

    def save_window_state(
        self, geometry: dict[str, int], mode: str, screen_index: int = 0
    ):
        """Save current window state for restoration."""
        if mode == "window":
            self.set("last_window_geometry", geometry)
            self.set("window_x", geometry.get("x"))
            self.set("window_y", geometry.get("y"))
            self.set("window_width", geometry.get("width"))
            self.set("window_height", geometry.get("height"))
        elif mode == "docked":
            self.set("dock_last_geometry", geometry)
            self.set("dock_screen", screen_index)

        self.set("launch_mode", mode)
        self.set("target_screen_index", screen_index)
        self.save_settings()

    def get_window_state(self) -> dict[str, Any]:
        """Get saved window state for restoration."""
        return {
            "mode": self.get("launch_mode", "docked"),
            "window_geometry": self.get("last_window_geometry"),
            "dock_geometry": self.get("dock_last_geometry"),
            "target_screen": self.get("target_screen_index", 0),
            "dock_screen": self.get("dock_screen", 0),
            "dock_width": self.get("dock_width", 110),
        }

    def should_restore_to_docked(self) -> bool:
        """Check if launcher should start in docked mode."""
        return self.get("launch_mode", "docked") == "docked"
