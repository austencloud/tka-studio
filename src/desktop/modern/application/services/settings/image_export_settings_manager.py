"""
Image Export Settings Manager Implementation

Implements image export settings management with format validation,
quality presets, and QSettings persistence.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import QObject, QSettings, pyqtSignal


logger = logging.getLogger(__name__)


class ImageExportSettingsManager(QObject):
    """
    Implementation of image export settings management using QSettings.

    Features:
    - Multiple format support with validation
    - Quality presets for common use cases
    - Dimension management with aspect ratio preservation
    - Scale factor support for high-DPI exports
    - Background inclusion options
    - Format-specific optimizations
    """

    export_format_changed = pyqtSignal(str)  # format_name
    export_quality_changed = pyqtSignal(int)  # quality
    export_dimensions_changed = pyqtSignal(int, int)  # width, height

    # Supported export formats
    SUPPORTED_FORMATS = ["PNG", "JPEG", "SVG", "PDF", "TIFF", "BMP"]

    # Default export settings
    DEFAULT_FORMAT = "PNG"
    DEFAULT_QUALITY = 95
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080
    DEFAULT_SCALE_FACTOR = 1.0
    DEFAULT_INCLUDE_BACKGROUND = True

    # Quality presets
    QUALITY_PRESETS = {
        "Maximum": 100,
        "High": 95,
        "Good": 85,
        "Medium": 75,
        "Low": 60,
        "Minimum": 40,
    }

    # Common dimension presets
    DIMENSION_PRESETS = {
        "HD (1280x720)": (1280, 720),
        "Full HD (1920x1080)": (1920, 1080),
        "4K (3840x2160)": (3840, 2160),
        "Square HD (1080x1080)": (1080, 1080),
        "Instagram (1080x1080)": (1080, 1080),
        "YouTube Thumbnail (1280x720)": (1280, 720),
        "Print Letter (2550x3300)": (2550, 3300),
        "Print A4 (2480x3508)": (2480, 3508),
    }

    def __init__(self, settings: QSettings):
        super().__init__()
        self.settings = settings
        logger.debug("Initialized ImageExportSettingsManager")

    def get_export_format(self) -> str:
        """
        Get the current export format.

        Returns:
            Export format name (e.g., "PNG", "JPEG")
        """
        try:
            format_name = self.settings.value(
                "export/format", self.DEFAULT_FORMAT, type=str
            )

            # Validate format
            if format_name not in self.SUPPORTED_FORMATS:
                logger.warning(
                    f"Invalid export format: {format_name}, using {self.DEFAULT_FORMAT}"
                )
                return self.DEFAULT_FORMAT

            return format_name

        except Exception as e:
            logger.error(f"Failed to get export format: {e}")
            return self.DEFAULT_FORMAT

    def set_export_format(self, format_name: str) -> bool:
        """
        Set the export format.

        Args:
            format_name: Export format to set

        Returns:
            True if successful, False if invalid format
        """
        try:
            if format_name not in self.SUPPORTED_FORMATS:
                logger.warning(f"Unsupported export format: {format_name}")
                return False

            old_format = self.get_export_format()

            self.settings.setValue("export/format", format_name)
            self.settings.sync()

            # Emit change event if format actually changed
            if old_format != format_name:
                self.export_format_changed.emit(format_name)
                logger.info(f"Export format changed from {old_format} to {format_name}")

            return True

        except Exception as e:
            logger.error(f"Failed to set export format {format_name}: {e}")
            return False

    def get_supported_formats(self) -> list[str]:
        """
        Get list of supported export formats.

        Returns:
            List of supported format names
        """
        return self.SUPPORTED_FORMATS.copy()

    def get_export_quality(self) -> int:
        """
        Get export quality (0-100).

        Returns:
            Export quality percentage
        """
        try:
            quality = self.settings.value(
                "export/quality", self.DEFAULT_QUALITY, type=int
            )

            # Clamp to valid range
            quality = max(0, min(100, quality))

            return quality

        except Exception as e:
            logger.error(f"Failed to get export quality: {e}")
            return self.DEFAULT_QUALITY

    def set_export_quality(self, quality: int) -> bool:
        """
        Set export quality (0-100).

        Args:
            quality: Quality percentage (0-100)

        Returns:
            True if successful, False if invalid quality
        """
        try:
            if not (0 <= quality <= 100):
                logger.warning(f"Invalid export quality: {quality} (must be 0-100)")
                return False

            old_quality = self.get_export_quality()

            self.settings.setValue("export/quality", quality)
            self.settings.sync()

            # Emit change event if quality actually changed
            if old_quality != quality:
                self.export_quality_changed.emit(quality)
                logger.debug(f"Export quality changed from {old_quality} to {quality}")

            return True

        except Exception as e:
            logger.error(f"Failed to set export quality {quality}: {e}")
            return False

    def get_export_dimensions(self) -> tuple[int, int]:
        """
        Get export dimensions (width, height).

        Returns:
            Tuple of (width, height) in pixels
        """
        try:
            width = self.settings.value("export/width", self.DEFAULT_WIDTH, type=int)
            height = self.settings.value("export/height", self.DEFAULT_HEIGHT, type=int)

            # Ensure positive dimensions
            width = max(1, width)
            height = max(1, height)

            return (width, height)

        except Exception as e:
            logger.error(f"Failed to get export dimensions: {e}")
            return (self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)

    def set_export_dimensions(self, width: int, height: int) -> bool:
        """
        Set export dimensions.

        Args:
            width: Width in pixels
            height: Height in pixels

        Returns:
            True if successful, False if invalid dimensions
        """
        try:
            if width <= 0 or height <= 0:
                logger.warning(
                    f"Invalid export dimensions: {width}x{height} (must be positive)"
                )
                return False

            # Check for reasonable limits (avoid memory issues)
            max_dimension = 32768  # 32K pixels
            if width > max_dimension or height > max_dimension:
                logger.warning(
                    f"Export dimensions too large: {width}x{height} (max {max_dimension})"
                )
                return False

            old_dimensions = self.get_export_dimensions()

            self.settings.setValue("export/width", width)
            self.settings.setValue("export/height", height)
            self.settings.sync()

            # Emit change event if dimensions actually changed
            if old_dimensions != (width, height):
                self.export_dimensions_changed.emit(width, height)
                logger.info(
                    f"Export dimensions changed from {old_dimensions[0]}x{old_dimensions[1]} to {width}x{height}"
                )

            return True

        except Exception as e:
            logger.error(f"Failed to set export dimensions {width}x{height}: {e}")
            return False

    def get_include_background(self) -> bool:
        """
        Get whether to include background in export.

        Returns:
            True if background should be included, False otherwise
        """
        try:
            return self.settings.value(
                "export/include_background", self.DEFAULT_INCLUDE_BACKGROUND, type=bool
            )
        except Exception as e:
            logger.error(f"Failed to get include background setting: {e}")
            return self.DEFAULT_INCLUDE_BACKGROUND

    def set_include_background(self, include: bool) -> None:
        """
        Set whether to include background in export.

        Args:
            include: Whether to include background
        """
        try:
            old_include = self.get_include_background()

            self.settings.setValue("export/include_background", include)
            self.settings.sync()

            if old_include != include:
                logger.debug(f"Include background changed to {include}")

        except Exception as e:
            logger.error(f"Failed to set include background {include}: {e}")

    def get_scale_factor(self) -> float:
        """
        Get the scale factor for export.

        Returns:
            Scale factor (typically 1.0 for normal size)
        """
        try:
            scale = self.settings.value(
                "export/scale_factor", self.DEFAULT_SCALE_FACTOR, type=float
            )

            # Ensure positive scale factor
            scale = max(0.1, scale)

            return scale

        except Exception as e:
            logger.error(f"Failed to get scale factor: {e}")
            return self.DEFAULT_SCALE_FACTOR

    def set_scale_factor(self, scale: float) -> bool:
        """
        Set the scale factor for export.

        Args:
            scale: Scale factor (must be positive)

        Returns:
            True if successful, False if invalid scale
        """
        try:
            if scale <= 0:
                logger.warning(f"Invalid scale factor: {scale} (must be positive)")
                return False

            # Check for reasonable limits
            if scale > 10.0:
                logger.warning(f"Scale factor too large: {scale} (max 10.0)")
                return False

            old_scale = self.get_scale_factor()

            self.settings.setValue("export/scale_factor", scale)
            self.settings.sync()

            if old_scale != scale:
                logger.debug(f"Scale factor changed from {old_scale} to {scale}")

            return True

        except Exception as e:
            logger.error(f"Failed to set scale factor {scale}: {e}")
            return False

    def get_quality_presets(self) -> dict[str, int]:
        """
        Get available quality presets.

        Returns:
            Dictionary mapping preset names to quality values
        """
        return self.QUALITY_PRESETS.copy()

    def apply_quality_preset(self, preset_name: str) -> bool:
        """
        Apply a quality preset.

        Args:
            preset_name: Name of the preset to apply

        Returns:
            True if successful, False if invalid preset
        """
        try:
            if preset_name not in self.QUALITY_PRESETS:
                logger.warning(f"Unknown quality preset: {preset_name}")
                return False

            quality = self.QUALITY_PRESETS[preset_name]
            return self.set_export_quality(quality)

        except Exception as e:
            logger.error(f"Failed to apply quality preset {preset_name}: {e}")
            return False

    def get_dimension_presets(self) -> dict[str, tuple[int, int]]:
        """
        Get available dimension presets.

        Returns:
            Dictionary mapping preset names to (width, height) tuples
        """
        return self.DIMENSION_PRESETS.copy()

    def apply_dimension_preset(self, preset_name: str) -> bool:
        """
        Apply a dimension preset.

        Args:
            preset_name: Name of the preset to apply

        Returns:
            True if successful, False if invalid preset
        """
        try:
            if preset_name not in self.DIMENSION_PRESETS:
                logger.warning(f"Unknown dimension preset: {preset_name}")
                return False

            width, height = self.DIMENSION_PRESETS[preset_name]
            return self.set_export_dimensions(width, height)

        except Exception as e:
            logger.error(f"Failed to apply dimension preset {preset_name}: {e}")
            return False

    def get_format_recommendations(self, format_name: str = None) -> dict[str, str]:
        """
        Get recommendations for optimal settings for a format.

        Args:
            format_name: Format to get recommendations for (uses current if None)

        Returns:
            Dictionary of recommendations
        """
        try:
            if format_name is None:
                format_name = self.get_export_format()

            recommendations = {
                "PNG": {
                    "quality": "Not applicable (lossless)",
                    "use_case": "Graphics with transparency, screenshots",
                    "background": "Optional (supports transparency)",
                },
                "JPEG": {
                    "quality": "85-95 for high quality, 75-85 for web",
                    "use_case": "Photos, complex images without transparency",
                    "background": "Recommended (no transparency support)",
                },
                "SVG": {
                    "quality": "Not applicable (vector)",
                    "use_case": "Scalable graphics, web use",
                    "background": "Optional (supports transparency)",
                },
                "PDF": {
                    "quality": "Not applicable (vector)",
                    "use_case": "Print, documentation",
                    "background": "Recommended for print",
                },
                "TIFF": {
                    "quality": "95-100 for archival",
                    "use_case": "Archival, professional printing",
                    "background": "Optional (supports transparency)",
                },
                "BMP": {
                    "quality": "Not applicable (uncompressed)",
                    "use_case": "Simple graphics, legacy compatibility",
                    "background": "Recommended (limited transparency)",
                },
            }

            return recommendations.get(format_name, {})

        except Exception as e:
            logger.error(f"Failed to get format recommendations for {format_name}: {e}")
            return {}

    def reset_to_defaults(self) -> None:
        """
        Reset all export settings to defaults.
        """
        try:
            self.set_export_format(self.DEFAULT_FORMAT)
            self.set_export_quality(self.DEFAULT_QUALITY)
            self.set_export_dimensions(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)
            self.set_scale_factor(self.DEFAULT_SCALE_FACTOR)
            self.set_include_background(self.DEFAULT_INCLUDE_BACKGROUND)

            logger.info("Reset all export settings to defaults")

        except Exception as e:
            logger.error(f"Failed to reset export settings: {e}")
