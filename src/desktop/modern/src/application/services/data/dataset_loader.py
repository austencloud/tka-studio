"""
Dataset Loader

Handles loading and caching of CSV pictograph datasets.
Focused solely on data access and file I/O operations.
"""

import logging
from typing import Optional

import pandas as pd
from infrastructure.data_path_handler import DataPathHandler

logger = logging.getLogger(__name__)


class DatasetLoader:
    """
    Loads and caches CSV pictograph datasets.
    
    Responsible for:
    - Loading diamond and box datasets from CSV files
    - Caching loaded datasets in memory
    - Validating dataset availability
    - Providing dataset status information
    """

    def __init__(self):
        """Initialize the dataset loader."""
        self._data_handler = DataPathHandler()
        self._diamond_dataset: Optional[pd.DataFrame] = None
        self._box_dataset: Optional[pd.DataFrame] = None
        self._combined_dataset: Optional[pd.DataFrame] = None
        self._datasets_loaded = False

    def load_datasets(self) -> None:
        """Load the diamond and box pictograph datasets."""
        if self._datasets_loaded:
            return  # Already loaded

        try:
            logger.info("Loading pictograph datasets...")
            
            # Load individual datasets
            self._diamond_dataset = self._data_handler.load_diamond_dataset()
            self._box_dataset = self._data_handler.load_box_dataset()

            # Create combined dataset
            self._create_combined_dataset()

            # Validate and report status
            self._validate_and_report_status()
            
            self._datasets_loaded = True
            logger.info("Pictograph datasets loaded successfully")

        except Exception as e:
            logger.error(f"Error loading datasets: {e}")
            self._create_empty_datasets()
            self._datasets_loaded = True  # Mark as loaded even if failed to prevent retries

    def _create_combined_dataset(self) -> None:
        """Create combined dataset from diamond and box datasets."""
        datasets_to_combine = []
        
        if self._diamond_dataset is not None and not self._diamond_dataset.empty:
            datasets_to_combine.append(self._diamond_dataset)
            
        if self._box_dataset is not None and not self._box_dataset.empty:
            datasets_to_combine.append(self._box_dataset)

        if datasets_to_combine:
            self._combined_dataset = pd.concat(datasets_to_combine, ignore_index=True)
        else:
            self._combined_dataset = pd.DataFrame()

    def _validate_and_report_status(self) -> None:
        """Validate data files and report status."""
        status = self._data_handler.validate_data_files()
        
        if not status["diamond_exists"]:
            logger.warning(f"Diamond dataset not found: {status['diamond_path']}")
        else:
            logger.info(f"Diamond dataset loaded: {len(self._diamond_dataset) if self._diamond_dataset is not None else 0} entries")
            
        if not status["box_exists"]:
            logger.warning(f"Box dataset not found: {status['box_path']}")
        else:
            logger.info(f"Box dataset loaded: {len(self._box_dataset) if self._box_dataset is not None else 0} entries")

    def _create_empty_datasets(self) -> None:
        """Create empty datasets as fallback."""
        self._diamond_dataset = pd.DataFrame()
        self._box_dataset = pd.DataFrame()
        self._combined_dataset = pd.DataFrame()

    def get_diamond_dataset(self) -> Optional[pd.DataFrame]:
        """
        Get the diamond dataset.
        
        Returns:
            Diamond dataset DataFrame or None if not available
        """
        if not self._datasets_loaded:
            self.load_datasets()
        return self._diamond_dataset

    def get_box_dataset(self) -> Optional[pd.DataFrame]:
        """
        Get the box dataset.
        
        Returns:
            Box dataset DataFrame or None if not available
        """
        if not self._datasets_loaded:
            self.load_datasets()
        return self._box_dataset

    def get_combined_dataset(self) -> Optional[pd.DataFrame]:
        """
        Get the combined dataset.
        
        Returns:
            Combined dataset DataFrame or None if not available
        """
        if not self._datasets_loaded:
            self.load_datasets()
        return self._combined_dataset

    def get_dataset_by_mode(self, grid_mode: str) -> Optional[pd.DataFrame]:
        """
        Get dataset by grid mode.
        
        Args:
            grid_mode: "diamond" or "box"
            
        Returns:
            Appropriate dataset or None if not available
        """
        if not self._datasets_loaded:
            self.load_datasets()
            
        if grid_mode == "diamond":
            return self._diamond_dataset
        elif grid_mode == "box":
            return self._box_dataset
        else:
            logger.warning(f"Unknown grid mode: {grid_mode}")
            return None

    def is_dataset_available(self, grid_mode: str) -> bool:
        """
        Check if a dataset is available and not empty.
        
        Args:
            grid_mode: "diamond" or "box"
            
        Returns:
            True if dataset is available and not empty
        """
        dataset = self.get_dataset_by_mode(grid_mode)
        return dataset is not None and not dataset.empty

    def get_dataset_info(self) -> dict:
        """
        Get information about loaded datasets.
        
        Returns:
            Dictionary with dataset statistics
        """
        if not self._datasets_loaded:
            self.load_datasets()

        return {
            "diamond_loaded": self._diamond_dataset is not None and not self._diamond_dataset.empty,
            "box_loaded": self._box_dataset is not None and not self._box_dataset.empty,
            "diamond_entries": len(self._diamond_dataset) if self._diamond_dataset is not None else 0,
            "box_entries": len(self._box_dataset) if self._box_dataset is not None else 0,
            "total_entries": len(self._combined_dataset) if self._combined_dataset is not None else 0,
            "datasets_loaded": self._datasets_loaded,
        }

    def reload_datasets(self) -> None:
        """Force reload of all datasets."""
        self._datasets_loaded = False
        self._diamond_dataset = None
        self._box_dataset = None
        self._combined_dataset = None
        self.load_datasets()

    def clear_cache(self) -> None:
        """Clear cached datasets to free memory."""
        self._diamond_dataset = None
        self._box_dataset = None
        self._combined_dataset = None
        self._datasets_loaded = False
        logger.info("Dataset cache cleared")
