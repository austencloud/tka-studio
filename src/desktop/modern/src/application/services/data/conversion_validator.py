"""
Conversion Validator

Handles validation of data conversions and provides conversion statistics.
Ensures data integrity during conversion processes.
"""

import logging
from typing import Any, Dict

try:
    from core.decorators import handle_service_errors
    from core.exceptions import ValidationError
    from domain.models import BeatData
    from .motion_attribute_converter import MotionAttributeConverter
except ImportError:
    # Fallback for tests
    def handle_service_errors(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

    class ValidationError(Exception):
        def __init__(self, message: str, field: str = None, value: Any = None):
            super().__init__(message)
            self.field = field
            self.value = value

logger = logging.getLogger(__name__)


class ConversionValidator:
    """
    Validates data conversions and provides conversion statistics.
    
    Ensures data integrity and provides insights into conversion processes.
    """

    def __init__(self):
        """Initialize the conversion validator."""
        self.motion_converter = MotionAttributeConverter()

    @handle_service_errors("validate_conversion")
    def validate_conversion(
        self, external_data: Dict[str, Any], beat_data: BeatData
    ) -> Dict[str, Any]:
        """
        Validate that conversion preserved all important data.

        Args:
            external_data: Original external data
            beat_data: Converted BeatData

        Returns:
            Dictionary with validation results including 'valid', 'issues', and 'total_issues'

        Raises:
            ValidationError: If input parameters are invalid
        """
        # Validate inputs
        if not isinstance(external_data, dict):
            raise ValidationError("External data must be a dictionary")
        if not isinstance(beat_data, BeatData):
            raise ValidationError("Beat data must be a BeatData instance")

        issues = []

        # Check letter preservation
        if external_data.get("letter") != beat_data.letter:
            issues.append(
                f"Letter mismatch: {external_data.get('letter')} → {beat_data.letter}"
            )

        # Check position preservation (stored in metadata)
        if external_data.get("start_pos") != beat_data.metadata.get("start_pos"):
            issues.append(
                f"Start position mismatch: {external_data.get('start_pos')} → {beat_data.metadata.get('start_pos')}"
            )

        if external_data.get("end_pos") != beat_data.metadata.get("end_pos"):
            issues.append(
                f"End position mismatch: {external_data.get('end_pos')} → {beat_data.metadata.get('end_pos')}"
            )

        # Check motion type preservation
        blue_attrs = external_data.get("blue_attributes", {})
        if blue_attrs.get("motion_type") and beat_data.blue_motion:
            motion_type_mapping = self.motion_converter.get_motion_type_mapping()
            expected_motion_type = motion_type_mapping.get(
                blue_attrs["motion_type"].lower()
            )
            if (
                expected_motion_type
                and expected_motion_type != beat_data.blue_motion.motion_type
            ):
                issues.append(
                    f"Blue motion type mismatch: {blue_attrs['motion_type']} → {beat_data.blue_motion.motion_type}"
                )

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "total_issues": len(issues),
        }

    def get_conversion_statistics(self) -> Dict[str, Any]:
        """Get statistics about available conversions."""
        motion_types = self.motion_converter.get_motion_type_mapping()
        rotation_directions = self.motion_converter.get_rotation_direction_mapping()
        locations = self.motion_converter.get_location_mapping()
        hand_motion_types = self.motion_converter.get_hand_motion_type_mapping()
        
        return {
            "motion_types": list(motion_types.keys()),
            "rotation_directions": list(rotation_directions.keys()),
            "locations": list(locations.keys()),
            "hand_motion_types": list(hand_motion_types.keys()),
            "total_mappings": len(motion_types) + len(rotation_directions) + len(locations) + len(hand_motion_types),
            "mapping_details": {
                "motion_type_count": len(motion_types),
                "rotation_direction_count": len(rotation_directions),
                "location_count": len(locations),
                "hand_motion_type_count": len(hand_motion_types),
            }
        }

    def validate_external_data_structure(self, external_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the structure of external data.

        Args:
            external_data: External data to validate

        Returns:
            Dictionary with validation results
        """
        issues = []
        warnings = []

        # Check basic structure
        if not isinstance(external_data, dict):
            issues.append("External data must be a dictionary")
            return {"valid": False, "issues": issues, "warnings": warnings}

        if not external_data:
            issues.append("External data cannot be empty")

        # Check required fields
        required_fields = ["letter"]
        for field in required_fields:
            if field not in external_data:
                issues.append(f"Missing required field: {field}")

        # Check optional but important fields
        optional_fields = ["start_pos", "end_pos", "blue_attributes", "red_attributes"]
        for field in optional_fields:
            if field not in external_data:
                warnings.append(f"Missing optional field: {field}")

        # Validate motion attributes structure
        for color in ["blue", "red"]:
            attr_key = f"{color}_attributes"
            if attr_key in external_data:
                attrs = external_data[attr_key]
                if not isinstance(attrs, dict):
                    issues.append(f"{attr_key} must be a dictionary")
                else:
                    # Check motion attribute fields
                    motion_fields = ["motion_type", "start_loc", "end_loc", "start_ori", "end_ori", "prop_rot_dir"]
                    for field in motion_fields:
                        if field not in attrs:
                            warnings.append(f"Missing {color} motion field: {field}")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "total_issues": len(issues),
            "total_warnings": len(warnings),
        }

    def get_validation_summary(self, validation_results: list) -> Dict[str, Any]:
        """
        Get summary of multiple validation results.

        Args:
            validation_results: List of validation result dictionaries

        Returns:
            Summary dictionary with aggregated statistics
        """
        total_validations = len(validation_results)
        valid_count = sum(1 for result in validation_results if result.get("valid", False))
        total_issues = sum(result.get("total_issues", 0) for result in validation_results)
        total_warnings = sum(result.get("total_warnings", 0) for result in validation_results)

        return {
            "total_validations": total_validations,
            "valid_count": valid_count,
            "invalid_count": total_validations - valid_count,
            "success_rate": valid_count / total_validations if total_validations > 0 else 0,
            "total_issues": total_issues,
            "total_warnings": total_warnings,
            "average_issues_per_validation": total_issues / total_validations if total_validations > 0 else 0,
        }
