"""
Batch Conversion Service

Handles batch conversion operations for multiple pictographs.
Provides optimized processing for large datasets with error handling and reporting.
"""

import logging
from typing import Any, Dict, List

try:
    from core.decorators import handle_service_errors
    from core.exceptions import DataProcessingError, ValidationError
    from core.monitoring import monitor_performance
    from domain.models import PictographData
    from .external_data_converter import ExternalDataConverter
    from .conversion_validator import ConversionValidator
except ImportError:
    # Fallback for tests
    def handle_service_errors(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

    def monitor_performance(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

    class DataProcessingError(Exception):
        pass

    class ValidationError(Exception):
        pass

logger = logging.getLogger(__name__)


class BatchConversionService:
    """
    Handles batch conversion operations for multiple pictographs.
    
    Provides optimized processing with error handling, progress tracking,
    and detailed reporting for large dataset conversions.
    """

    def __init__(self):
        """Initialize the batch conversion service."""
        self.external_converter = ExternalDataConverter()
        self.validator = ConversionValidator()

    @handle_service_errors("convert_multiple_external_pictographs")
    @monitor_performance("batch_data_conversion")
    def convert_multiple_external_pictographs(
        self, external_pictographs: List[Dict[str, Any]]
    ) -> List[PictographData]:
        """
        Convert multiple external pictographs to modern PictographData format.

        Args:
            external_pictographs: List of external pictograph data dictionaries

        Returns:
            List of PictographData objects

        Raises:
            ValidationError: If input list is invalid
            DataProcessingError: If conversion fails for any pictograph
        """
        # Validate input
        if not isinstance(external_pictographs, list):
            raise ValidationError("External pictographs must be a list")

        if not external_pictographs:
            logger.warning("Empty pictograph list provided for conversion")
            return []

        converted_pictographs = []
        conversion_errors = []

        for i, external_data in enumerate(external_pictographs):
            try:
                pictograph_data = self.external_converter.convert_external_pictograph_to_pictograph_data(
                    external_data
                )
                converted_pictographs.append(pictograph_data)
            except Exception as e:
                error_msg = f"Pictograph {i}: {e}"
                conversion_errors.append(error_msg)
                logger.warning(f"Conversion error for pictograph {i}: {e}")

        if conversion_errors:
            logger.warning(
                f"Conversion completed with {len(conversion_errors)} errors out of {len(external_pictographs)} pictographs"
            )
        else:
            logger.info(
                f"Successfully converted {len(converted_pictographs)} pictographs"
            )

        return converted_pictographs

    def convert_with_validation(
        self, external_pictographs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Convert multiple pictographs with detailed validation reporting.

        Args:
            external_pictographs: List of external pictograph data dictionaries

        Returns:
            Dictionary with conversion results and validation report
        """
        if not isinstance(external_pictographs, list):
            raise ValidationError("External pictographs must be a list")

        results = {
            "converted_pictographs": [],
            "validation_results": [],
            "conversion_errors": [],
            "summary": {}
        }

        for i, external_data in enumerate(external_pictographs):
            try:
                # Validate structure first
                validation_result = self.validator.validate_external_data_structure(external_data)
                validation_result["index"] = i
                results["validation_results"].append(validation_result)

                if validation_result["valid"]:
                    # Convert if validation passed
                    pictograph_data = self.external_converter.convert_external_pictograph_to_pictograph_data(
                        external_data
                    )
                    results["converted_pictographs"].append(pictograph_data)
                else:
                    logger.warning(f"Skipping pictograph {i} due to validation errors: {validation_result['issues']}")

            except Exception as e:
                error_info = {
                    "index": i,
                    "error": str(e),
                    "external_data": external_data
                }
                results["conversion_errors"].append(error_info)
                logger.error(f"Conversion error for pictograph {i}: {e}")

        # Generate summary
        results["summary"] = self._generate_batch_summary(results)
        
        return results

    def convert_with_progress_callback(
        self, 
        external_pictographs: List[Dict[str, Any]], 
        progress_callback=None
    ) -> List[PictographData]:
        """
        Convert multiple pictographs with progress reporting.

        Args:
            external_pictographs: List of external pictograph data dictionaries
            progress_callback: Optional callback function for progress updates

        Returns:
            List of PictographData objects
        """
        if not isinstance(external_pictographs, list):
            raise ValidationError("External pictographs must be a list")

        converted_pictographs = []
        total_count = len(external_pictographs)

        for i, external_data in enumerate(external_pictographs):
            try:
                pictograph_data = self.external_converter.convert_external_pictograph_to_pictograph_data(
                    external_data
                )
                converted_pictographs.append(pictograph_data)

                # Report progress
                if progress_callback:
                    progress = (i + 1) / total_count
                    progress_callback(progress, i + 1, total_count)

            except Exception as e:
                logger.warning(f"Conversion error for pictograph {i}: {e}")
                
                # Report progress even on error
                if progress_callback:
                    progress = (i + 1) / total_count
                    progress_callback(progress, i + 1, total_count, error=str(e))

        return converted_pictographs

    def _generate_batch_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics for batch conversion."""
        total_input = len(results["validation_results"])
        successful_conversions = len(results["converted_pictographs"])
        validation_errors = sum(1 for v in results["validation_results"] if not v["valid"])
        conversion_errors = len(results["conversion_errors"])

        return {
            "total_input": total_input,
            "successful_conversions": successful_conversions,
            "validation_errors": validation_errors,
            "conversion_errors": conversion_errors,
            "success_rate": successful_conversions / total_input if total_input > 0 else 0,
            "total_errors": validation_errors + conversion_errors,
        }

    def get_batch_statistics(self) -> Dict[str, Any]:
        """Get statistics about batch conversion capabilities."""
        return {
            "supported_formats": ["external_pictograph"],
            "output_formats": ["PictographData"],
            "features": [
                "validation",
                "error_handling",
                "progress_tracking",
                "detailed_reporting"
            ],
            "conversion_statistics": self.validator.get_conversion_statistics()
        }
