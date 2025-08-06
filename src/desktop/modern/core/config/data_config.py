"""
TKA Data Configuration

Provides clean, dependency-injectable data configuration to replace the singleton DataPathHandler.
Uses Result types for proper error handling.

USAGE:
    from desktop.modern.core.config.data_config import create_data_config, DataConfig

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

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


# Removed Result pattern - using simple exceptions instead


@dataclass(frozen=True)
class DataConfig:
    """Immutable data configuration for TKA."""

    data_dir: Path
    diamond_csv_path: Path
    box_csv_path: Path

    def validate_paths(self) -> None:
        """
        Validate that all required paths exist.

        Raises:
            FileNotFoundError: If required data directory or files don't exist
        """
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")

        if not self.diamond_csv_path.exists():
            raise FileNotFoundError(f"Diamond CSV not found: {self.diamond_csv_path}")

        # Box CSV is optional - don't fail if missing
        if not self.box_csv_path.exists():
            # Just log a warning, don't fail
            pass

    def get_status(self) -> dict:
        """Get status of all data files."""
        return {
            "diamond_exists": self.diamond_csv_path.exists(),
            "box_exists": self.box_csv_path.exists(),
            "diamond_path": str(self.diamond_csv_path),
            "box_path": str(self.box_csv_path),
            "data_dir": str(self.data_dir),
        }


def create_data_config(
    base_path: Path | None = None,
) -> DataConfig:
    """
    Create data configuration with simple, predictable logic.

    Args:
        base_path: Optional base path for data directory. If None, uses environment or default.

    Returns:
        DataConfig instance

    Raises:
        FileNotFoundError: If data directory or required files don't exist
        ValueError: If configuration is invalid
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
        config.validate_paths()  # Will raise exception if invalid

        return config

    except Exception as e:
        raise ValueError(f"Failed to create data config: {e}") from e


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
        if (
            potential_data.exists()
            and (potential_data / "DiamondPictographDataframe.csv").exists()
        ):
            return potential_data

        # Check if this is the TKA root directory
        if current_path.name == "TKA":
            return current_path / "data"

        current_path = current_path.parent

    # Fallback: use current working directory + data
    return Path.cwd() / "data"
