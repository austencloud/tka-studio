"""
TKA Application Configuration

Centralized configuration system to replace scattered config patterns.
Provides immutable configuration objects with dependency injection support.

USAGE:
    from desktop.modern.core.config.app_config import create_app_config, AppConfig

    # Create configuration
    try:
        app_config = create_app_config()
        # Use app_config.positioning.default_grid_mode, etc.
    except Exception as e:
        logger.error(f"Failed to create config: {e}")

    # Inject into DI container
    container.register_singleton(AppConfig, lambda: app_config)
"""

from __future__ import annotations

from dataclasses import dataclass
import os

# Result pattern removed - using simple exceptions
from desktop.modern.core.config.data_config import DataConfig, create_data_config


@dataclass(frozen=True)
class PositioningConfig:
    """Configuration for positioning services."""

    default_grid_mode: str = "diamond"
    enable_special_placements: bool = True
    quadrant_adjustment_enabled: bool = True
    default_adjustment_fallback: bool = True
    enable_directional_tuples: bool = True

    def validate(self) -> bool:
        """Validate positioning configuration."""
        valid_grid_modes = ["diamond", "box"]
        if self.default_grid_mode not in valid_grid_modes:
            raise ValueError(f"Invalid grid mode: {self.default_grid_mode}")

        return True


@dataclass(frozen=True)
class UIConfig:
    """Configuration for UI components."""

    default_screen: str = "secondary"
    enable_animations: bool = True
    background_type: str = "aurora"
    theme: str = "dark"
    enable_debug_borders: bool = False

    def validate(self) -> bool:
        """Validate UI configuration."""
        valid_screens = ["primary", "secondary", "auto"]
        if self.default_screen not in valid_screens:
            raise ValueError(f"Invalid screen setting: {self.default_screen}")

        valid_backgrounds = ["aurora", "solid", "gradient", "none"]
        if self.background_type not in valid_backgrounds:
            raise ValueError(f"Invalid background type: {self.background_type}")

        return True


@dataclass(frozen=True)
class LoggingConfig:
    """Configuration for logging."""

    level: str = "INFO"
    enable_file_logging: bool = True
    enable_console_logging: bool = True
    log_dir: str = "logs"
    max_file_size_mb: int = 10
    backup_count: int = 5

    def validate(self) -> bool:
        """Validate logging configuration."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.level not in valid_levels:
            raise ValueError(f"Invalid log level: {self.level}")

        if self.max_file_size_mb <= 0:
            raise ValueError(f"Invalid max file size: {self.max_file_size_mb}MB")

        return True


@dataclass(frozen=True)
class AppConfig:
    """Main application configuration."""

    data_config: DataConfig
    positioning: PositioningConfig
    ui: UIConfig
    logging: LoggingConfig

    def validate(self) -> bool:
        """Validate entire application configuration."""
        # Validate data config
        self.data_config.validate_paths()

        # Validate positioning config
        self.positioning.validate()

        # Validate UI config
        self.ui.validate()

        # Validate logging config
        self.logging.validate()

        return True

    @classmethod
    def from_environment(cls) -> AppConfig:
        """Load configuration from environment variables and defaults."""
        # Create data configuration
        data_config = create_data_config()

        # Create positioning config from environment
        positioning = PositioningConfig(
            default_grid_mode=os.environ.get("TKA_DEFAULT_GRID_MODE", "diamond"),
            enable_special_placements=os.environ.get(
                "TKA_ENABLE_SPECIAL_PLACEMENTS", "true"
            ).lower()
            == "true",
            quadrant_adjustment_enabled=os.environ.get(
                "TKA_QUADRANT_ADJUSTMENT", "true"
            ).lower()
            == "true",
            default_adjustment_fallback=os.environ.get(
                "TKA_DEFAULT_FALLBACK", "true"
            ).lower()
            == "true",
            enable_directional_tuples=os.environ.get(
                "TKA_DIRECTIONAL_TUPLES", "true"
            ).lower()
            == "true",
        )

        # Create UI config from environment
        ui = UIConfig(
            default_screen=os.environ.get("TKA_DEFAULT_SCREEN", "secondary"),
            enable_animations=os.environ.get("TKA_ENABLE_ANIMATIONS", "true").lower()
            == "true",
            background_type=os.environ.get("TKA_BACKGROUND_TYPE", "aurora"),
            theme=os.environ.get("TKA_THEME", "dark"),
            enable_debug_borders=os.environ.get("TKA_DEBUG_BORDERS", "false").lower()
            == "true",
        )

        # Create logging config from environment
        logging_config = LoggingConfig(
            level=os.environ.get("TKA_LOG_LEVEL", "INFO"),
            enable_file_logging=os.environ.get("TKA_FILE_LOGGING", "true").lower()
            == "true",
            enable_console_logging=os.environ.get("TKA_CONSOLE_LOGGING", "true").lower()
            == "true",
            log_dir=os.environ.get("TKA_LOG_DIR", "logs"),
            max_file_size_mb=int(os.environ.get("TKA_MAX_LOG_SIZE_MB", "10")),
            backup_count=int(os.environ.get("TKA_LOG_BACKUP_COUNT", "5")),
        )

        config = cls(
            data_config=data_config,
            positioning=positioning,
            ui=ui,
            logging=logging_config,
        )

        # Validate the complete configuration
        config.validate()

        return config


def create_app_config(
    data_config: DataConfig | None = None,
    positioning_config: PositioningConfig | None = None,
    ui_config: UIConfig | None = None,
    logging_config: LoggingConfig | None = None,
) -> AppConfig:
    """
    Create application configuration with optional overrides.

    Args:
        data_config: Optional data configuration override
        positioning_config: Optional positioning configuration override
        ui_config: Optional UI configuration override
        logging_config: Optional logging configuration override

    Returns:
        Result containing AppConfig or AppError
    """
    try:
        # Use provided configs or create defaults
        if data_config is None:
            data_config = create_data_config()

        if positioning_config is None:
            positioning_config = PositioningConfig()

        if ui_config is None:
            ui_config = UIConfig()

        if logging_config is None:
            logging_config = LoggingConfig()

        config = AppConfig(
            data_config=data_config,
            positioning=positioning_config,
            ui=ui_config,
            logging=logging_config,
        )

        # Validate the configuration
        config.validate()

        return config

    except Exception as e:
        raise RuntimeError(f"Failed to create app config: {e}") from e
