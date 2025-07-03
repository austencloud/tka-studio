"""
TKA Application Configuration

Centralized configuration system to replace scattered config patterns.
Provides immutable configuration objects with dependency injection support.

USAGE:
    from core.config.app_config import create_app_config, AppConfig
    
    # Create configuration
    config_result = create_app_config()
    if config_result.is_success():
        app_config = config_result.value
        # Use app_config.positioning.default_grid_mode, etc.
    
    # Inject into DI container
    container.register_singleton(AppConfig, lambda: config_result.value)
"""

import os
from dataclasses import dataclass
from typing import Optional

from core.types.result import Result, AppError, ErrorType, success, failure, app_error
from core.config.data_config import DataConfig, create_data_config


@dataclass(frozen=True)
class PositioningConfig:
    """Configuration for positioning services."""
    default_grid_mode: str = "diamond"
    enable_special_placements: bool = True
    quadrant_adjustment_enabled: bool = True
    default_adjustment_fallback: bool = True
    enable_directional_tuples: bool = True
    
    def validate(self) -> Result[bool, AppError]:
        """Validate positioning configuration."""
        valid_grid_modes = ["diamond", "box"]
        if self.default_grid_mode not in valid_grid_modes:
            return failure(app_error(
                ErrorType.CONFIG_ERROR,
                f"Invalid grid mode: {self.default_grid_mode}",
                {"valid_modes": valid_grid_modes, "provided": self.default_grid_mode}
            ))
        
        return success(True)


@dataclass(frozen=True)
class UIConfig:
    """Configuration for UI components."""
    default_screen: str = "secondary"
    enable_animations: bool = True
    background_type: str = "aurora"
    theme: str = "dark"
    enable_debug_borders: bool = False
    
    def validate(self) -> Result[bool, AppError]:
        """Validate UI configuration."""
        valid_screens = ["primary", "secondary", "auto"]
        if self.default_screen not in valid_screens:
            return failure(app_error(
                ErrorType.CONFIG_ERROR,
                f"Invalid screen setting: {self.default_screen}",
                {"valid_screens": valid_screens, "provided": self.default_screen}
            ))
        
        valid_backgrounds = ["aurora", "solid", "gradient", "none"]
        if self.background_type not in valid_backgrounds:
            return failure(app_error(
                ErrorType.CONFIG_ERROR,
                f"Invalid background type: {self.background_type}",
                {"valid_types": valid_backgrounds, "provided": self.background_type}
            ))
        
        return success(True)


@dataclass(frozen=True)
class LoggingConfig:
    """Configuration for logging."""
    level: str = "INFO"
    enable_file_logging: bool = True
    enable_console_logging: bool = True
    log_dir: str = "logs"
    max_file_size_mb: int = 10
    backup_count: int = 5
    
    def validate(self) -> Result[bool, AppError]:
        """Validate logging configuration."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.level not in valid_levels:
            return failure(app_error(
                ErrorType.CONFIG_ERROR,
                f"Invalid log level: {self.level}",
                {"valid_levels": valid_levels, "provided": self.level}
            ))
        
        if self.max_file_size_mb <= 0:
            return failure(app_error(
                ErrorType.CONFIG_ERROR,
                f"Invalid max file size: {self.max_file_size_mb}MB",
                {"provided": self.max_file_size_mb}
            ))
        
        return success(True)


@dataclass(frozen=True)
class AppConfig:
    """Main application configuration."""
    data_config: DataConfig
    positioning: PositioningConfig
    ui: UIConfig
    logging: LoggingConfig
    
    def validate(self) -> Result[bool, AppError]:
        """Validate entire application configuration."""
        # Validate data config
        data_result = self.data_config.validate_paths()
        if data_result.is_failure():
            return data_result
        
        # Validate positioning config
        positioning_result = self.positioning.validate()
        if positioning_result.is_failure():
            return positioning_result
        
        # Validate UI config
        ui_result = self.ui.validate()
        if ui_result.is_failure():
            return ui_result
        
        # Validate logging config
        logging_result = self.logging.validate()
        if logging_result.is_failure():
            return logging_result
        
        return success(True)
    
    @classmethod
    def from_environment(cls) -> Result["AppConfig", AppError]:
        """Load configuration from environment variables and defaults."""
        # Create data configuration
        data_result = create_data_config()
        if data_result.is_failure():
            return failure(data_result.error)
        
        # Create positioning config from environment
        positioning = PositioningConfig(
            default_grid_mode=os.environ.get("TKA_DEFAULT_GRID_MODE", "diamond"),
            enable_special_placements=os.environ.get("TKA_ENABLE_SPECIAL_PLACEMENTS", "true").lower() == "true",
            quadrant_adjustment_enabled=os.environ.get("TKA_QUADRANT_ADJUSTMENT", "true").lower() == "true",
            default_adjustment_fallback=os.environ.get("TKA_DEFAULT_FALLBACK", "true").lower() == "true",
            enable_directional_tuples=os.environ.get("TKA_DIRECTIONAL_TUPLES", "true").lower() == "true"
        )
        
        # Create UI config from environment
        ui = UIConfig(
            default_screen=os.environ.get("TKA_DEFAULT_SCREEN", "secondary"),
            enable_animations=os.environ.get("TKA_ENABLE_ANIMATIONS", "true").lower() == "true",
            background_type=os.environ.get("TKA_BACKGROUND_TYPE", "aurora"),
            theme=os.environ.get("TKA_THEME", "dark"),
            enable_debug_borders=os.environ.get("TKA_DEBUG_BORDERS", "false").lower() == "true"
        )
        
        # Create logging config from environment
        logging_config = LoggingConfig(
            level=os.environ.get("TKA_LOG_LEVEL", "INFO"),
            enable_file_logging=os.environ.get("TKA_FILE_LOGGING", "true").lower() == "true",
            enable_console_logging=os.environ.get("TKA_CONSOLE_LOGGING", "true").lower() == "true",
            log_dir=os.environ.get("TKA_LOG_DIR", "logs"),
            max_file_size_mb=int(os.environ.get("TKA_MAX_LOG_SIZE_MB", "10")),
            backup_count=int(os.environ.get("TKA_LOG_BACKUP_COUNT", "5"))
        )
        
        config = cls(
            data_config=data_result.value,
            positioning=positioning,
            ui=ui,
            logging=logging_config
        )
        
        # Validate the complete configuration
        validation_result = config.validate()
        if validation_result.is_failure():
            return failure(validation_result.error)
        
        return success(config)


def create_app_config(
    data_config: Optional[DataConfig] = None,
    positioning_config: Optional[PositioningConfig] = None,
    ui_config: Optional[UIConfig] = None,
    logging_config: Optional[LoggingConfig] = None
) -> Result[AppConfig, AppError]:
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
            data_result = create_data_config()
            if data_result.is_failure():
                return failure(data_result.error)
            data_config = data_result.value
        
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
            logging=logging_config
        )
        
        # Validate the configuration
        validation_result = config.validate()
        if validation_result.is_failure():
            return failure(validation_result.error)
        
        return success(config)
        
    except Exception as e:
        return failure(app_error(
            ErrorType.CONFIG_ERROR,
            f"Failed to create app config: {e}",
            cause=e
        ))
