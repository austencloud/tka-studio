"""
TKA Data Configuration

Provides clean, dependency-injectable data configuration to replace the singleton DataPathHandler.
Uses Result types for proper error handling.

USAGE:
    from core.config.data_config import create_data_config, DataConfig
    
    # Create configuration
    config_result = create_data_config()
    if config_result.is_success():
        config = config_result.value
        # Use config.diamond_csv_path, etc.
    else:
        logger.error(f"Config error: {config_result.error}")
        
    # Inject into services
    class DataService:
        def __init__(self, config: DataConfig):
            self.config = config
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from core.types.result import Result, AppError, ErrorType, success, failure, app_error


@dataclass(frozen=True)
class DataConfig:
    """Immutable data configuration for TKA."""
    data_dir: Path
    diamond_csv_path: Path
    box_csv_path: Path
    
    def validate_paths(self) -> Result[bool, AppError]:
        """Validate that all required paths exist."""
        if not self.data_dir.exists():
            return failure(app_error(
                ErrorType.CONFIG_ERROR,
                f"Data directory not found: {self.data_dir}",
                {"attempted_path": str(self.data_dir)}
            ))
        
        if not self.diamond_csv_path.exists():
            return failure(app_error(
                ErrorType.DATA_ERROR,
                f"Diamond CSV not found: {self.diamond_csv_path}",
                {"path": str(self.diamond_csv_path)}
            ))
        
        # Box CSV is optional - don't fail if missing
        if not self.box_csv_path.exists():
            # Just log a warning, don't fail
            pass
            
        return success(True)
    
    def get_status(self) -> dict:
        """Get status of all data files."""
        return {
            "diamond_exists": self.diamond_csv_path.exists(),
            "box_exists": self.box_csv_path.exists(),
            "diamond_path": str(self.diamond_csv_path),
            "box_path": str(self.box_csv_path),
            "data_dir": str(self.data_dir),
        }


def create_data_config(base_path: Optional[Path] = None) -> Result[DataConfig, AppError]:
    """
    Create data configuration with simple, predictable logic.
    
    Args:
        base_path: Optional base path for data directory. If None, uses environment or default.
        
    Returns:
        Result containing DataConfig or AppError
    """
    try:
        if base_path is None:
            # Use environment variable or default
            env_path = os.environ.get("TKA_DATA_DIR")
            if env_path:
                base_path = Path(env_path)
            else:
                # Default: look for data directory relative to project root
                base_path = _find_project_data_dir()
        
        data_dir = base_path.resolve()
        diamond_csv = data_dir / "DiamondPictographDataframe.csv"
        box_csv = data_dir / "BoxPictographDataframe.csv"
        
        config = DataConfig(data_dir, diamond_csv, box_csv)
        
        # Validate the configuration
        validation_result = config.validate_paths()
        if validation_result.is_failure():
            return failure(validation_result.error)
            
        return success(config)
        
    except Exception as e:
        return failure(app_error(
            ErrorType.CONFIG_ERROR,
            f"Failed to create data config: {e}",
            {"base_path": str(base_path) if base_path else "None"},
            e
        ))


def _find_project_data_dir() -> Path:
    """
    Find the project data directory using simple upward search.
    
    Returns:
        Path to data directory
    """
    # Start from this file and search upward
    current_path = Path(__file__).resolve().parent
    
    # Search upward for TKA project root
    while current_path.parent != current_path:  # Not at filesystem root
        # Look for data directory at this level
        potential_data = current_path / "data"
        if potential_data.exists() and (potential_data / "DiamondPictographDataframe.csv").exists():
            return potential_data
            
        # Check if this is the TKA root directory
        if current_path.name == "TKA":
            return current_path / "data"
            
        current_path = current_path.parent
    
    # Fallback: use current working directory + data
    return Path.cwd() / "data"


def create_data_config_from_env() -> Result[DataConfig, AppError]:
    """Create data configuration from environment variables only."""
    env_path = os.environ.get("TKA_DATA_DIR")
    if not env_path:
        return failure(app_error(
            ErrorType.CONFIG_ERROR,
            "TKA_DATA_DIR environment variable not set",
            {"available_env_vars": [k for k in os.environ.keys() if "TKA" in k]}
        ))
    
    return create_data_config(Path(env_path))


def create_data_config_with_fallback() -> DataConfig:
    """
    Create data configuration with fallback to defaults.
    
    This is for cases where you need a config and can't handle Result types.
    Logs errors but doesn't fail.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    result = create_data_config()
    if result.is_success():
        return result.value
    
    # Log the error and create a fallback config
    logger.warning(f"Failed to create data config: {result.error}")
    
    # Create minimal fallback config
    fallback_data_dir = Path.cwd() / "data"
    fallback_data_dir.mkdir(exist_ok=True)
    
    return DataConfig(
        data_dir=fallback_data_dir,
        diamond_csv_path=fallback_data_dir / "DiamondPictographDataframe.csv",
        box_csv_path=fallback_data_dir / "BoxPictographDataframe.csv"
    )
