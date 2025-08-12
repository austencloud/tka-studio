"""
TKA Data Service

Clean, dependency-injectable data service to replace the singleton DataPathHandler.
Uses simple exceptions for error handling and configuration injection.
"""

import logging
from typing import Any

import pandas as pd

from desktop.modern.core.config.data_config import DataConfig
from desktop.modern.core.interfaces.data_services import IDataManager

logger = logging.getLogger(__name__)


class DataManager(IDataManager):
    """
    Clean data service with dependency injection support.

    Replaces the singleton DataPathHandler with a configurable service.
    """

    def __init__(self, config: DataConfig):
        """
        Initialize the data service.

        Args:
            config: Data configuration object
        """
        self.config = config
        self._diamond_dataset = None
        self._box_dataset = None
        logger.info(f"Data service initialized with config: {config.data_dir}")

    def load_diamond_dataset(self) -> pd.DataFrame:
        """Load diamond pictograph dataset with error handling."""
        if self._diamond_dataset is None:
            try:
                self._diamond_dataset = pd.read_csv(self.config.diamond_csv_path)
                logger.info("Diamond dataset loaded successfully")
            except FileNotFoundError:
                logger.error(
                    f"Diamond dataset not found at {self.config.diamond_csv_path}"
                )
                raise
            except Exception as e:
                logger.error(f"Error loading diamond dataset: {e}")
                raise
        return self._diamond_dataset

    def load_box_dataset(self) -> pd.DataFrame:
        """Load box pictograph dataset with error handling."""
        if self._box_dataset is None:
            try:
                self._box_dataset = pd.read_csv(self.config.box_csv_path)
                logger.info("Box dataset loaded successfully")
            except FileNotFoundError:
                logger.error(f"Box dataset not found at {self.config.box_csv_path}")
                raise
            except Exception as e:
                logger.error(f"Error loading box dataset: {e}")
                raise
        return self._box_dataset

    def load_combined_dataset(self) -> pd.DataFrame:
        """Load and combine both diamond and box datasets."""
        diamond_df = self.load_diamond_dataset()
        box_df = self.load_box_dataset()

        # Add dataset source column
        diamond_df = diamond_df.copy()
        box_df = box_df.copy()
        diamond_df["dataset_source"] = "diamond"
        box_df["dataset_source"] = "box"

        combined = pd.concat([diamond_df, box_df], ignore_index=True)
        logger.info(f"Combined dataset created with {len(combined)} records")
        return combined

    def validate_data_files(self) -> dict[str, Any]:
        """Validate data files and return status information."""
        validation_results = {
            "diamond_csv_exists": self.config.diamond_csv_path.exists(),
            "box_csv_exists": self.config.box_csv_path.exists(),
            "diamond_csv_path": str(self.config.diamond_csv_path),
            "box_csv_path": str(self.config.box_csv_path),
            "errors": [],
        }

        try:
            if validation_results["diamond_csv_exists"]:
                diamond_df = pd.read_csv(self.config.diamond_csv_path)
                validation_results["diamond_record_count"] = len(diamond_df)
            else:
                validation_results["errors"].append(
                    f"Diamond CSV not found: {self.config.diamond_csv_path}"
                )
        except Exception as e:
            validation_results["errors"].append(f"Error reading diamond CSV: {e}")

        try:
            if validation_results["box_csv_exists"]:
                box_df = pd.read_csv(self.config.box_csv_path)
                validation_results["box_record_count"] = len(box_df)
            else:
                validation_results["errors"].append(
                    f"Box CSV not found: {self.config.box_csv_path}"
                )
        except Exception as e:
            validation_results["errors"].append(f"Error reading box CSV: {e}")

        validation_results["is_valid"] = len(validation_results["errors"]) == 0
        return validation_results

    def get_data_config(self) -> DataConfig:
        """Get the current data configuration."""
        return self.config

    def reload_config(self, new_config: DataConfig) -> None:
        """Reload with new configuration."""
        self.config = new_config
        # Clear cached datasets to force reload
        self._diamond_dataset = None
        self._box_dataset = None
        logger.info(f"Reloaded data service with new config: {new_config.data_dir}")

    def get_dataset_info(self) -> dict[str, Any]:
        """Get information about loaded datasets."""
        info = {
            "diamond_loaded": self._diamond_dataset is not None,
            "box_loaded": self._box_dataset is not None,
            "config": {
                "data_dir": str(self.config.data_dir),
                "diamond_csv_path": str(self.config.diamond_csv_path),
                "box_csv_path": str(self.config.box_csv_path),
            },
        }

        if self._diamond_dataset is not None:
            info["diamond_record_count"] = len(self._diamond_dataset)
        if self._box_dataset is not None:
            info["box_record_count"] = len(self._box_dataset)

        return info

    def get_dataset_by_mode(self, grid_mode: str) -> pd.DataFrame:
        """
        Get dataset by grid mode for backward compatibility.

        Args:
            grid_mode: Either 'diamond' or 'box'

        Returns:
            The requested dataset

        Raises:
            ValueError: If grid_mode is not 'diamond' or 'box'
        """
        if grid_mode == "diamond":
            return self.load_diamond_dataset()
        elif grid_mode == "box":
            return self.load_box_dataset()
        else:
            raise ValueError(
                f"Invalid grid_mode: {grid_mode}. Must be 'diamond' or 'box'"
            )
