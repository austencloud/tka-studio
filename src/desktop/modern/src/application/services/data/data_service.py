"""
TKA Data Service

Clean, dependency-injectable data service to replace the singleton DataPathHandler.
Uses Result types for proper error handling and configuration injection.

USAGE:
    from core.config.data_config import create_data_config
    from application.services.data.data_service import DataService
    
    # Create configuration
    config_result = create_data_config()
    if config_result.is_success():
        data_service = DataService(config_result.value)
        
        # Load data with proper error handling
        diamond_result = data_service.load_diamond_dataset()
        if diamond_result.is_success():
            df = diamond_result.value
        else:
            logger.error(f"Failed to load diamond data: {diamond_result.error}")
"""

import logging
from typing import Dict, Any
import pandas as pd

from core.types.result import Result, AppError, ErrorType, success, failure, app_error
from core.config.data_config import DataConfig

logger = logging.getLogger(__name__)


class DataService:
    """
    Clean data service with dependency injection and proper error handling.
    
    Replaces the singleton DataPathHandler with a focused, testable service.
    """

    def __init__(self, config: DataConfig):
        """
        Initialize with data configuration.
        
        Args:
            config: Data configuration with validated paths
        """
        self.config = config

    def load_diamond_dataset(self) -> Result[pd.DataFrame, AppError]:
        """
        Load diamond pictograph dataset with error handling.
        
        Returns:
            Result containing DataFrame or AppError
        """
        try:
            if not self.config.diamond_csv_path.exists():
                return failure(app_error(
                    ErrorType.FILE_SYSTEM_ERROR,
                    f"Diamond CSV file not found: {self.config.diamond_csv_path}",
                    {"path": str(self.config.diamond_csv_path)}
                ))
            
            df = pd.read_csv(self.config.diamond_csv_path)
            
            if df.empty:
                return failure(app_error(
                    ErrorType.DATA_ERROR,
                    "Diamond CSV file is empty",
                    {"path": str(self.config.diamond_csv_path), "shape": df.shape}
                ))
            
            logger.info(f"Loaded diamond dataset: {df.shape[0]} rows, {df.shape[1]} columns")
            return success(df)
            
        except pd.errors.EmptyDataError:
            return failure(app_error(
                ErrorType.DATA_ERROR,
                "Diamond CSV file contains no data",
                {"path": str(self.config.diamond_csv_path)}
            ))
        except pd.errors.ParserError as e:
            return failure(app_error(
                ErrorType.DATA_ERROR,
                f"Failed to parse diamond CSV: {e}",
                {"path": str(self.config.diamond_csv_path)},
                e
            ))
        except Exception as e:
            return failure(app_error(
                ErrorType.FILE_SYSTEM_ERROR,
                f"Failed to load diamond dataset: {e}",
                {"path": str(self.config.diamond_csv_path)},
                e
            ))

    def load_box_dataset(self) -> Result[pd.DataFrame, AppError]:
        """
        Load box pictograph dataset with error handling.
        
        Returns:
            Result containing DataFrame or AppError
        """
        try:
            if not self.config.box_csv_path.exists():
                return failure(app_error(
                    ErrorType.FILE_SYSTEM_ERROR,
                    f"Box CSV file not found: {self.config.box_csv_path}",
                    {"path": str(self.config.box_csv_path)}
                ))
            
            df = pd.read_csv(self.config.box_csv_path)
            
            if df.empty:
                return failure(app_error(
                    ErrorType.DATA_ERROR,
                    "Box CSV file is empty",
                    {"path": str(self.config.box_csv_path), "shape": df.shape}
                ))
            
            logger.info(f"Loaded box dataset: {df.shape[0]} rows, {df.shape[1]} columns")
            return success(df)
            
        except pd.errors.EmptyDataError:
            return failure(app_error(
                ErrorType.DATA_ERROR,
                "Box CSV file contains no data",
                {"path": str(self.config.box_csv_path)}
            ))
        except pd.errors.ParserError as e:
            return failure(app_error(
                ErrorType.DATA_ERROR,
                f"Failed to parse box CSV: {e}",
                {"path": str(self.config.box_csv_path)},
                e
            ))
        except Exception as e:
            return failure(app_error(
                ErrorType.FILE_SYSTEM_ERROR,
                f"Failed to load box dataset: {e}",
                {"path": str(self.config.box_csv_path)},
                e
            ))

    def load_combined_dataset(self) -> Result[pd.DataFrame, AppError]:
        """
        Load and combine both diamond and box datasets.
        
        Returns:
            Result containing combined DataFrame or AppError
        """
        try:
            # Load diamond dataset
            diamond_result = self.load_diamond_dataset()
            if diamond_result.is_failure():
                return failure(diamond_result.error)
            
            diamond_df = diamond_result.value
            
            # Load box dataset (optional)
            box_result = self.load_box_dataset()
            if box_result.is_failure():
                # Box dataset is optional - just use diamond if box fails
                logger.warning(f"Box dataset not available: {box_result.error}")
                return success(diamond_df)
            
            box_df = box_result.value
            
            # Combine datasets
            combined_df = pd.concat([diamond_df, box_df], ignore_index=True)
            
            logger.info(f"Combined dataset: {combined_df.shape[0]} rows, {combined_df.shape[1]} columns")
            return success(combined_df)
            
        except Exception as e:
            return failure(app_error(
                ErrorType.DATA_ERROR,
                f"Failed to combine datasets: {e}",
                {
                    "diamond_path": str(self.config.diamond_csv_path),
                    "box_path": str(self.config.box_csv_path)
                },
                e
            ))

    def validate_data_files(self) -> Result[Dict[str, Any], AppError]:
        """
        Validate data files and return status information.
        
        Returns:
            Result containing status dict or AppError
        """
        try:
            status = {
                "diamond_exists": self.config.diamond_csv_path.exists(),
                "box_exists": self.config.box_csv_path.exists(),
                "diamond_path": str(self.config.diamond_csv_path),
                "box_path": str(self.config.box_csv_path),
                "data_dir": str(self.config.data_dir),
                "data_dir_exists": self.config.data_dir.exists(),
            }
            
            # Add file sizes if files exist
            if status["diamond_exists"]:
                status["diamond_size_bytes"] = self.config.diamond_csv_path.stat().st_size
            
            if status["box_exists"]:
                status["box_size_bytes"] = self.config.box_csv_path.stat().st_size
            
            return success(status)
            
        except Exception as e:
            return failure(app_error(
                ErrorType.FILE_SYSTEM_ERROR,
                f"Failed to validate data files: {e}",
                {
                    "diamond_path": str(self.config.diamond_csv_path),
                    "box_path": str(self.config.box_csv_path)
                },
                e
            ))

    def get_data_config(self) -> DataConfig:
        """Get the current data configuration."""
        return self.config

    def reload_config(self, new_config: DataConfig) -> Result[bool, AppError]:
        """
        Reload with new configuration.
        
        Args:
            new_config: New data configuration
            
        Returns:
            Result indicating success or failure
        """
        try:
            # Validate new configuration
            validation_result = new_config.validate_paths()
            if validation_result.is_failure():
                return failure(validation_result.error)
            
            self.config = new_config
            logger.info(f"Reloaded data service with new config: {new_config.data_dir}")
            return success(True)
            
        except Exception as e:
            return failure(app_error(
                ErrorType.CONFIG_ERROR,
                f"Failed to reload config: {e}",
                {"new_data_dir": str(new_config.data_dir)},
                e
            ))
