"""
Option Configuration Service - Pure Configuration Management

Manages configuration and business rules without UI dependencies.
Extracted from hardcoded values in presentation components.
"""

from desktop.modern.presentation.components.option_picker.types.letter_types import (
    LetterType,
)


class OptionConfigurationService:
    """
    Pure service for option picker configuration management.

    No Qt dependencies - manages business rules and configuration.
    """

    def __init__(self):
        """Initialize with default configuration values."""
        self._config = {
            # Pool configuration - OPTIMIZED: Reduced from 50 to 36 to match actual usage
            "total_max_pictographs": 36,  # 16+8+8+2+1+1 = 36 total (corrected calculation)
            # Performance configuration
            "debounce_delay_ms": 50,
            "performance_logging_threshold_ms": 100,
            # Layout configuration
            "column_count": 8,
            "spacing": 3,
            "min_frame_size": 60,
            "border_ratio": 0.015,
            # Section grouping
            "groupable_types": [LetterType.TYPE4, LetterType.TYPE5, LetterType.TYPE6],
            "individual_types": [LetterType.TYPE1, LetterType.TYPE2, LetterType.TYPE3],
        }

    def get_max_pictographs_per_section(self, letter_type: LetterType) -> int:
        """
        Get maximum pictographs for a specific letter type.

        Pure business rule - no Qt dependencies.
        """
        # Customized per type based on actual requirements
        type_limits = {
            LetterType.TYPE1: 16,  # Type1 has 16 pictographs
            LetterType.TYPE2: 8,  # Type2 has 8 pictographs
            LetterType.TYPE3: 8,  # Type3 has 8 pictographs
            LetterType.TYPE4: 2,  # Grouped sections can be smaller
            LetterType.TYPE5: 1,
            LetterType.TYPE6: 1,
        }
        return type_limits.get(letter_type, self._config["max_pictographs_per_section"])

    def get_total_max_pictographs(self) -> int:
        """Get total maximum pictographs across all sections."""
        return self._config["total_max_pictographs"]

    def get_debounce_delay(self) -> int:
        """Get debounce delay for refresh operations in milliseconds."""
        return self._config["debounce_delay_ms"]

    def get_performance_threshold(self) -> int:
        """Get performance logging threshold in milliseconds."""
        return self._config["performance_logging_threshold_ms"]

    def get_layout_config(self) -> dict[str, int]:
        """Get layout configuration values."""
        return {
            "column_count": self._config["column_count"],
            "spacing": self._config["spacing"],
            "min_frame_size": self._config["min_frame_size"],
        }

    def get_sizing_config(self) -> dict[str, float]:
        """Get sizing calculation configuration."""
        return {
            "border_ratio": self._config["border_ratio"],
            "min_frame_size": self._config["min_frame_size"],
        }

    def is_groupable_type(self, letter_type: LetterType) -> bool:
        """
        Check if letter type should be grouped with others.

        Pure business rule - no Qt dependencies.
        """
        return letter_type in self._config["groupable_types"]

    def is_individual_type(self, letter_type: LetterType) -> bool:
        """
        Check if letter type should be displayed individually.

        Pure business rule - no Qt dependencies.
        """
        return letter_type in self._config["individual_types"]

    def get_groupable_types(self) -> list:
        """Get list of letter types that should be grouped."""
        return self._config["groupable_types"].copy()

    def get_individual_types(self) -> list:
        """Get list of letter types that should be individual."""
        return self._config["individual_types"].copy()

    def update_config(self, config_updates: dict[str, any]) -> None:
        """
        Update configuration values.

        Validates updates before applying them.
        """
        try:
            for key, value in config_updates.items():
                if key in self._config:
                    # Basic validation
                    if isinstance(value, type(self._config[key])):
                        self._config[key] = value
                        print(f"✅ [CONFIG] Updated {key} to {value}")
                    else:
                        print(
                            f"❌ [CONFIG] Invalid type for {key}: expected {type(self._config[key])}, got {type(value)}"
                        )
                else:
                    print(f"❌ [CONFIG] Unknown configuration key: {key}")
        except Exception as e:
            print(f"❌ [CONFIG] Error updating configuration: {e}")

    def get_section_config(self, letter_type: LetterType) -> dict[str, any]:
        """
        Get complete configuration for a specific letter type section.

        Returns all relevant configuration for section setup.
        """
        return {
            "is_groupable": self.is_groupable_type(letter_type),
            "column_count": self._config["column_count"],
            "spacing": self._config["spacing"],
            "debounce_delay": self._config["debounce_delay_ms"],
        }

    def validate_pool_size(self, requested_size: int) -> bool:
        """
        Validate that requested pool size is reasonable.

        Pure validation logic - no Qt dependencies.
        """
        try:
            return requested_size > 0 and requested_size <= 1000  # Sanity check
        except Exception:
            return False

    def get_all_config(self) -> dict[str, any]:
        """Get complete configuration dictionary (read-only copy)."""
        return self._config.copy()

    def reset_to_defaults(self) -> None:
        """Reset all configuration to default values."""
        self.__init__()
        print("✅ [CONFIG] Reset to default configuration")
