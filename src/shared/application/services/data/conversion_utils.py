"""
Conversion Utilities

Data conversion operations implemented as a service class.
"""

from typing import Any

from desktop.modern.core.interfaces.data_builder_services import IConversionUtils


class ConversionUtils(IConversionUtils):
    """Service class for data conversion operations."""

    def extract_end_position_from_position_key(self, position_key: str) -> str:
        """
        Extract the actual end position from a position key like 'beta5_beta5'.

        Args:
            position_key: Position key in format "start_end" or just "position"

        Returns:
            The end position part of the key
        """
        # Position keys are in format "start_end", we want the end part
        if "_" in position_key:
            parts = position_key.split("_")
            if len(parts) == 2:
                return parts[1]  # Return the end position part

        # Fallback: if no underscore, assume it's already the position
        return position_key

    # Interface implementation methods
    def convert_coordinates(
        self, coords: tuple[float, float], from_system: str, to_system: str
    ) -> tuple[float, float]:
        """Convert coordinates between systems (interface implementation)."""
        x, y = coords

        # Simple coordinate system conversions
        if from_system == "screen" and to_system == "grid":
            # Convert screen coordinates to grid coordinates
            # This is a simplified implementation
            grid_x = x / 100.0  # Assuming 100 pixels per grid unit
            grid_y = y / 100.0
            return (grid_x, grid_y)

        elif from_system == "grid" and to_system == "screen":
            # Convert grid coordinates to screen coordinates
            screen_x = x * 100.0
            screen_y = y * 100.0
            return (screen_x, screen_y)

        elif from_system == "relative" and to_system == "absolute":
            # Convert relative coordinates (0-1) to absolute
            # Assuming a default canvas size of 800x600
            abs_x = x * 800.0
            abs_y = y * 600.0
            return (abs_x, abs_y)

        elif from_system == "absolute" and to_system == "relative":
            # Convert absolute coordinates to relative (0-1)
            rel_x = x / 800.0
            rel_y = y / 600.0
            return (rel_x, rel_y)

        # If no conversion needed or unknown systems, return as-is
        return coords

    def convert_units(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert units between measurement systems (interface implementation)."""
        if from_unit == to_unit:
            return value

        # Length conversions
        if from_unit == "px" and to_unit == "em":
            return value / 16.0  # Assuming 16px = 1em
        elif from_unit == "em" and to_unit == "px":
            return value * 16.0
        elif from_unit == "px" and to_unit == "rem":
            return value / 16.0  # Assuming 16px = 1rem
        elif from_unit == "rem" and to_unit == "px":
            return value * 16.0

        # Angle conversions
        elif from_unit == "degrees" and to_unit == "radians":
            return value * 3.14159 / 180.0
        elif from_unit == "radians" and to_unit == "degrees":
            return value * 180.0 / 3.14159

        # Time conversions
        elif from_unit == "ms" and to_unit == "s":
            return value / 1000.0
        elif from_unit == "s" and to_unit == "ms":
            return value * 1000.0

        # If conversion not supported, return original
        return value

    def normalize_data_format(self, data: Any, target_format: str) -> Any:
        """Normalize data to target format (interface implementation)."""
        if target_format == "json":
            # Convert data to JSON-serializable format
            if hasattr(data, "__dict__"):
                return data.__dict__
            elif isinstance(data, (list, tuple)):
                return [
                    self.normalize_data_format(item, target_format) for item in data
                ]
            elif isinstance(data, dict):
                return {
                    k: self.normalize_data_format(v, target_format)
                    for k, v in data.items()
                }
            else:
                return data

        elif target_format == "string":
            # Convert data to string representation
            return str(data)

        elif target_format == "dict":
            # Convert data to dictionary format
            if hasattr(data, "__dict__"):
                return data.__dict__
            elif isinstance(data, (list, tuple)):
                return {str(i): item for i, item in enumerate(data)}
            else:
                return {"value": data}

        # If format not supported, return original
        return data

    def convert_color_format(self, color: str, from_format: str, to_format: str) -> str:
        """
        Convert color between formats.

        Args:
            color: Color value to convert
            from_format: Source format (hex, rgb, hsl, etc.)
            to_format: Target format

        Returns:
            Converted color value
        """
        # Simple implementation - for now just return the original color
        # This can be expanded later if color conversion is actually needed
        return color

    def convert_units(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert between different units.

        Args:
            value: Value to convert
            from_unit: Source unit
            to_unit: Target unit

        Returns:
            Converted value
        """
        # Simple implementation - for now just return the original value
        # This can be expanded later if unit conversion is actually needed
        return value


# Convenience function for backward compatibility
def extract_end_position_from_position_key(position_key: str) -> str:
    """Backward compatibility function."""
    utils = ConversionUtils()
    return utils.extract_end_position_from_position_key(position_key)
