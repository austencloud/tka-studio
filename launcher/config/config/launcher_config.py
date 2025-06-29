#!/usr/bin/env python3
"""
Launcher Configuration - Settings and Preferences
================================================

Configuration management for the TKA Fluent Launcher including:
- Window geometry and positioning
- Theme and appearance settings
- Application preferences
- Dual-mode configuration

Architecture:
- JSON-based configuration storage
- Type-safe configuration classes
- Automatic migration and validation
"""

import json
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from PyQt6.QtCore import QRect

logger = logging.getLogger(__name__)


@dataclass
class WindowConfig:
    """Window geometry and positioning configuration."""

    width: int = 1200  # 50% of typical 1920px screen width
    height: int = 800  # 50% of typical 1600px screen height
    x: Optional[int] = None
    y: Optional[int] = None
    maximized: bool = False
    mode: str = "window"  # "window" or "docked"


@dataclass
class ThemeConfig:
    """Theme and appearance configuration."""

    theme: str = "dark"  # "dark" or "light"
    accent_color: str = "blue"
    transparency: float = 0.95
    animations_enabled: bool = True
    glassmorphism_enabled: bool = True


@dataclass
class ApplicationConfig:
    """Application behavior configuration."""

    auto_refresh: bool = True
    show_categories: bool = True
    search_delay_ms: int = 300
    launch_timeout_seconds: int = 30
    remember_selection: bool = True
    last_selected_app: Optional[str] = None


@dataclass
class LauncherConfiguration:
    """Complete launcher configuration."""

    version: str = "3.0.0"
    window: WindowConfig = None
    theme: ThemeConfig = None
    application: ApplicationConfig = None

    def __post_init__(self):
        """Initialize default values if None."""
        if self.window is None:
            object.__setattr__(self, "window", WindowConfig())
        if self.theme is None:
            object.__setattr__(self, "theme", ThemeConfig())
        if self.application is None:
            object.__setattr__(self, "application", ApplicationConfig())


class LauncherConfig:
    """
    Configuration manager for TKA Fluent Launcher.

    Handles loading, saving, and validation of launcher settings
    with automatic migration and sensible defaults.
    """

    def __init__(self, config_file: Optional[Path] = None):
        """Initialize configuration manager."""
        self.config_file = config_file or self._get_default_config_path()
        self.config = self._load_configuration()

        logger.info(f"📋 Configuration loaded from: {self.config_file}")

    def _get_default_config_path(self) -> Path:
        """Get the default configuration file path."""
        # Use launcher directory for config file
        launcher_dir = Path(__file__).parent
        return launcher_dir / "config" / "launcher_config.json"

    def _load_configuration(self) -> LauncherConfiguration:
        """Load configuration from file with fallback to defaults."""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Validate and migrate if needed
                config = self._validate_and_migrate(data)
                logger.info("✅ Configuration loaded successfully")
                return config
            else:
                logger.info("📋 No config file found, using defaults")
                return self._create_default_configuration()

        except Exception as e:
            logger.warning(f"⚠️ Failed to load config, using defaults: {e}")
            return self._create_default_configuration()

    def _create_default_configuration(self) -> LauncherConfiguration:
        """Create default configuration."""
        return LauncherConfiguration(
            window=WindowConfig(), theme=ThemeConfig(), application=ApplicationConfig()
        )

    def _validate_and_migrate(self, data: Dict[str, Any]) -> LauncherConfiguration:
        """Validate and migrate configuration data."""
        try:
            # Check version and migrate if needed
            version = data.get("version", "1.0.0")
            if version != "3.0.0":
                data = self._migrate_configuration(data, version)

            # Create configuration objects with validation
            window_config = WindowConfig(**data.get("window", {}))
            theme_config = ThemeConfig(**data.get("theme", {}))
            app_config = ApplicationConfig(**data.get("application", {}))

            return LauncherConfiguration(
                window=window_config,
                theme=theme_config,
                application=app_config,
                version="3.0.0",
            )

        except Exception as e:
            logger.warning(f"⚠️ Configuration validation failed: {e}")
            return self._create_default_configuration()

    def _migrate_configuration(
        self, data: Dict[str, Any], from_version: str
    ) -> Dict[str, Any]:
        """Migrate configuration from older versions."""
        logger.info(f"🔄 Migrating configuration from {from_version} to 3.0.0")

        # Add migration logic here as needed
        # For now, just ensure required structure exists
        migrated = {
            "window": data.get("window", {}),
            "theme": data.get("theme", {}),
            "application": data.get("application", {}),
            "version": "3.0.0",
        }

        return migrated

    def save_configuration(self):
        """Save current configuration to file."""
        try:
            # Ensure config directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)

            # Convert to dictionary
            config_dict = asdict(self.config)

            # Save to file
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)

            logger.info("💾 Configuration saved successfully")

        except Exception as e:
            logger.error(f"❌ Failed to save configuration: {e}")

    # Convenience methods for accessing configuration

    def get_window_geometry(self) -> QRect:
        """Get window geometry as QRect."""
        w = self.config.window
        if w.x is not None and w.y is not None:
            return QRect(w.x, w.y, w.width, w.height)
        else:
            # Return default centered position (will be calculated by launcher)
            return QRect(0, 0, w.width, w.height)

    def set_window_geometry(self, rect: QRect):
        """Set window geometry from QRect."""
        self.config.window.x = rect.x()
        self.config.window.y = rect.y()
        self.config.window.width = rect.width()
        self.config.window.height = rect.height()

    def get_theme_name(self) -> str:
        """Get current theme name."""
        return self.config.theme.theme

    def set_theme_name(self, theme: str):
        """Set theme name."""
        self.config.theme.theme = theme

    def get_accent_color(self) -> str:
        """Get accent color."""
        return self.config.theme.accent_color

    def set_accent_color(self, color: str):
        """Set accent color."""
        self.config.theme.accent_color = color

    def is_animations_enabled(self) -> bool:
        """Check if animations are enabled."""
        return self.config.theme.animations_enabled

    def set_animations_enabled(self, enabled: bool):
        """Enable or disable animations."""
        self.config.theme.animations_enabled = enabled

    def is_glassmorphism_enabled(self) -> bool:
        """Check if glassmorphism effects are enabled."""
        return self.config.theme.glassmorphism_enabled

    def set_glassmorphism_enabled(self, enabled: bool):
        """Enable or disable glassmorphism effects."""
        self.config.theme.glassmorphism_enabled = enabled

    def get_window_mode(self) -> str:
        """Get window mode (window/docked)."""
        return self.config.window.mode

    def set_window_mode(self, mode: str):
        """Set window mode."""
        if mode in ("window", "docked"):
            self.config.window.mode = mode
        else:
            logger.warning(f"⚠️ Invalid window mode: {mode}")

    def is_auto_refresh_enabled(self) -> bool:
        """Check if auto refresh is enabled."""
        return self.config.application.auto_refresh

    def set_auto_refresh_enabled(self, enabled: bool):
        """Enable or disable auto refresh."""
        self.config.application.auto_refresh = enabled

    def get_last_selected_app(self) -> Optional[str]:
        """Get last selected application ID."""
        return self.config.application.last_selected_app

    def set_last_selected_app(self, app_id: Optional[str]):
        """Set last selected application ID."""
        self.config.application.last_selected_app = app_id

    def get_search_delay(self) -> int:
        """Get search delay in milliseconds."""
        return self.config.application.search_delay_ms

    def get_launch_timeout(self) -> int:
        """Get launch timeout in seconds."""
        return self.config.application.launch_timeout_seconds

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self.config)

    def update_from_dict(self, data: Dict[str, Any]):
        """Update configuration from dictionary."""
        try:
            # Update individual sections
            if "window" in data:
                for key, value in data["window"].items():
                    if hasattr(self.config.window, key):
                        setattr(self.config.window, key, value)

            if "theme" in data:
                for key, value in data["theme"].items():
                    if hasattr(self.config.theme, key):
                        setattr(self.config.theme, key, value)

            if "application" in data:
                for key, value in data["application"].items():
                    if hasattr(self.config.application, key):
                        setattr(self.config.application, key, value)

            logger.info("✅ Configuration updated from dictionary")

        except Exception as e:
            logger.error(f"❌ Failed to update configuration: {e}")

    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self.config = self._create_default_configuration()
        logger.info("🔄 Configuration reset to defaults")
