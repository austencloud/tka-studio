"""
External Data Converter

Handles conversion of external pictograph data to modern PictographData format.
Focused on the core conversion logic without dependencies on other conversion types.
"""

import logging
from typing import Any, Dict, Optional

try:
    from core.decorators import handle_service_errors
    from core.exceptions import DataProcessingError, ValidationError
    from core.monitoring import monitor_performance
    from domain.models import GlyphData, PictographData
    from .glyph_data_service import GlyphDataService
    from .motion_attribute_converter import MotionAttributeConverter
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
        def __init__(self, message: str, data_type: Optional[str] = None, processing_stage: Optional[str] = None):
            super().__init__(message)
            self.data_type = data_type
            self.processing_stage = processing_stage

    class ValidationError(Exception):
        def __init__(self, message: str, field: Optional[str] = None, value: Any = None):
            super().__init__(message)
            self.field = field
            self.value = value

logger = logging.getLogger(__name__)


class ExternalDataConverter:
    """
    Converts external pictograph data to modern PictographData format.
    
    Focused solely on external data to PictographData conversion,
    following single responsibility principle.
    """

    def __init__(self):
        """Initialize the external data converter."""
        self.glyph_data_service = GlyphDataService()
        self.motion_converter = MotionAttributeConverter()

    @handle_service_errors("convert_external_pictograph_to_pictograph_data")
    @monitor_performance("external_data_conversion")
    def convert_external_pictograph_to_pictograph_data(
        self, external_data: Dict[str, Any]
    ) -> PictographData:
        """
        Convert external pictograph data to modern PictographData format.

        Args:
            external_data: External pictograph data dictionary

        Returns:
            PictographData object with converted motion information

        Raises:
            DataProcessingError: If required data is missing or invalid
            ValidationError: If data format is invalid
        """
        # Validate input data
        if not isinstance(external_data, dict):
            raise ValidationError("External data must be a dictionary")

        if not external_data:
            raise ValidationError("External data cannot be empty")

        try:
            # Extract basic information
            letter = external_data.get("letter", "Unknown")
            start_pos = external_data.get("start_pos", "unknown")
            end_pos = external_data.get("end_pos", "unknown")

            # Convert blue motion attributes
            blue_attrs = external_data.get("blue_attributes", {})
            blue_motion = self.motion_converter.convert_motion_attributes(blue_attrs, "blue")

            # Convert red motion attributes
            red_attrs = external_data.get("red_attributes", {})
            red_motion = self.motion_converter.convert_motion_attributes(red_attrs, "red")

            # Create arrows from motion data
            from domain.models.pictograph_models import ArrowData, GridData

            arrows = {}
            if blue_motion:
                arrows["blue"] = ArrowData(motion_data=blue_motion, color="blue")
            if red_motion:
                arrows["red"] = ArrowData(motion_data=red_motion, color="red")

            # Create initial PictographData object
            pictograph_data = PictographData(
                grid_data=GridData(),  # Default grid data
                arrows=arrows,
                letter=letter,
                start_position=start_pos,
                end_position=end_pos,
                metadata={
                    "source": "external_conversion",
                },
            )

            # Generate glyph data using the glyph data service
            glyph_data = self._generate_glyph_data(pictograph_data)

            # Return final PictographData object with glyph data
            return pictograph_data.update(glyph_data=glyph_data)

        except (ValidationError, DataProcessingError):
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            logger.error(
                f"Failed to convert external data to PictographData: {e}",
                extra={"external_data": external_data},
            )
            raise DataProcessingError(
                f"Data conversion failed: {e}",
                data_type="external_pictograph",
                processing_stage="conversion",
            ) from e

    def _generate_glyph_data(
        self, pictograph_data: PictographData
    ) -> Optional[GlyphData]:
        """
        Generate glyph data for the pictograph data using the glyph data service.

        Args:
            pictograph_data: The pictograph data to generate glyph data for

        Returns:
            GlyphData object or None if no glyphs needed
        """
        try:
            # Use the glyph data service directly with pictograph data
            return self.glyph_data_service.determine_glyph_data(pictograph_data)
        except Exception as e:
            logger.warning(f"Failed to generate glyph data: {e}")
            return None

    def validate_external_data(self, external_data: Dict[str, Any]) -> bool:
        """
        Validate external data format.

        Args:
            external_data: External data to validate

        Returns:
            True if valid, False otherwise
        """
        if not isinstance(external_data, dict):
            return False

        if not external_data:
            return False

        # Check for required fields
        required_fields = ["letter"]
        for field in required_fields:
            if field not in external_data:
                return False

        return True

    def get_supported_fields(self) -> list:
        """Get list of supported external data fields."""
        return [
            "letter",
            "start_pos",
            "end_pos",
            "blue_attributes",
            "red_attributes",
        ]
