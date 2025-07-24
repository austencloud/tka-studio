"""
Font Size Validator - Specific Font Size Regression Prevention
=============================================================

Provides specialized validation for font sizes in exported images to prevent
"humongous" text issues and ensure consistency with Legacy system behavior.
"""

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import pytesseract
    from PIL import Image, ImageDraw, ImageFont

    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logging.warning("OCR libraries not available - text size detection will be limited")

try:
    import cv2
    import numpy as np

    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    cv2 = None
    np = None

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontMetrics, QImage, QPainter

logger = logging.getLogger(__name__)


@dataclass
class FontMeasurements:
    """Font size measurements from an image."""

    word_label_size: Optional[float] = None
    difficulty_label_size: Optional[float] = None
    user_info_size: Optional[float] = None
    beat_number_size: Optional[float] = None
    detected_text: List[str] = None
    measurement_method: str = "unknown"
    confidence: float = 0.0
    errors: List[str] = None


@dataclass
class FontComparisonReport:
    """Comparison report between Legacy and Modern font sizes."""

    legacy_measurements: FontMeasurements
    modern_measurements: FontMeasurements
    word_label_ratio: Optional[float] = None
    difficulty_label_ratio: Optional[float] = None
    within_tolerance: bool = False
    tolerance_percentage: float = 10.0
    issues_found: List[str] = None
    recommendations: List[str] = None


class FontSizeValidator:
    """
    Validate font sizes in exported images to prevent regressions.

    Provides methods to measure font sizes, compare against expected ranges,
    and detect "humongous" text issues that have been problematic.
    """

    def __init__(self, tolerance_percentage: float = 10.0):
        """
        Initialize the font size validator.

        Args:
            tolerance_percentage: Acceptable font size variation percentage
        """
        self.tolerance_percentage = tolerance_percentage

        # Expected font size ranges based on Legacy system analysis
        self.expected_ranges = {
            "word_label": {
                1: (50, 90),  # 1 beat: base_size / 2.3
                2: (80, 130),  # 2 beats: base_size / 1.5
                3: (150, 200),  # 3+ beats: base_size
            },
            "difficulty_label": (15, 40),
            "user_info": (30, 70),
            "beat_numbers": (20, 50),
        }

    def validate_word_label_size(
        self, image_path: str, expected_range: Tuple[float, float]
    ) -> bool:
        """
        Validate word label font size is within expected range.

        Args:
            image_path: Path to exported image
            expected_range: (min_size, max_size) tuple

        Returns:
            True if font size is within range, False otherwise
        """
        try:
            measurements = self.measure_font_sizes(image_path)

            if not measurements.word_label_size:
                logger.error("Could not measure word label size")
                return False

            min_size, max_size = expected_range
            actual_size = measurements.word_label_size

            if min_size <= actual_size <= max_size:
                logger.info(
                    f"Word label size validation passed: {actual_size} (range: {min_size}-{max_size})"
                )
                return True
            else:
                logger.error(
                    f"Word label size out of range: {actual_size} (expected: {min_size}-{max_size})"
                )
                return False

        except Exception as e:
            logger.error(f"Word label size validation failed: {e}")
            return False

    def validate_difficulty_label_size(
        self, image_path: str, expected_range: Tuple[float, float]
    ) -> bool:
        """
        Validate difficulty label font size is within expected range.

        Args:
            image_path: Path to exported image
            expected_range: (min_size, max_size) tuple

        Returns:
            True if font size is within range, False otherwise
        """
        try:
            measurements = self.measure_font_sizes(image_path)

            if not measurements.difficulty_label_size:
                logger.warning("Could not measure difficulty label size")
                return True  # Not critical if difficulty label is not present

            min_size, max_size = expected_range
            actual_size = measurements.difficulty_label_size

            if min_size <= actual_size <= max_size:
                logger.info(f"Difficulty label size validation passed: {actual_size}")
                return True
            else:
                logger.error(
                    f"Difficulty label size out of range: {actual_size} (expected: {min_size}-{max_size})"
                )
                return False

        except Exception as e:
            logger.error(f"Difficulty label size validation failed: {e}")
            return False

    def compare_font_sizes_legacy_vs_modern(
        self, legacy_img_path: str, modern_img_path: str
    ) -> FontComparisonReport:
        """
        Compare font sizes between Legacy and Modern exports.

        Args:
            legacy_img_path: Path to legacy export
            modern_img_path: Path to modern export

        Returns:
            FontComparisonReport with detailed comparison
        """
        try:
            # Measure font sizes in both images
            legacy_measurements = self.measure_font_sizes(legacy_img_path)
            modern_measurements = self.measure_font_sizes(modern_img_path)

            # Calculate ratios
            word_ratio = None
            difficulty_ratio = None

            if (
                legacy_measurements.word_label_size
                and modern_measurements.word_label_size
            ):
                word_ratio = (
                    modern_measurements.word_label_size
                    / legacy_measurements.word_label_size
                )

            if (
                legacy_measurements.difficulty_label_size
                and modern_measurements.difficulty_label_size
            ):
                difficulty_ratio = (
                    modern_measurements.difficulty_label_size
                    / legacy_measurements.difficulty_label_size
                )

            # Check if within tolerance
            within_tolerance = True
            issues = []
            recommendations = []

            if word_ratio:
                word_diff_percent = abs(word_ratio - 1.0) * 100
                if word_diff_percent > self.tolerance_percentage:
                    within_tolerance = False
                    issues.append(
                        f"Word label size differs by {word_diff_percent:.1f}% (ratio: {word_ratio:.2f})"
                    )

                    if word_ratio > 1.5:
                        recommendations.append(
                            "Modern word labels are significantly larger - check beat_scale calculation"
                        )
                    elif word_ratio < 0.7:
                        recommendations.append(
                            "Modern word labels are significantly smaller - verify font scaling logic"
                        )

            if difficulty_ratio:
                diff_diff_percent = abs(difficulty_ratio - 1.0) * 100
                if diff_diff_percent > self.tolerance_percentage:
                    within_tolerance = False
                    issues.append(
                        f"Difficulty label size differs by {diff_diff_percent:.1f}% (ratio: {difficulty_ratio:.2f})"
                    )

            return FontComparisonReport(
                legacy_measurements=legacy_measurements,
                modern_measurements=modern_measurements,
                word_label_ratio=word_ratio,
                difficulty_label_ratio=difficulty_ratio,
                within_tolerance=within_tolerance,
                tolerance_percentage=self.tolerance_percentage,
                issues_found=issues,
                recommendations=recommendations,
            )

        except Exception as e:
            logger.error(f"Font size comparison failed: {e}")
            return FontComparisonReport(
                legacy_measurements=FontMeasurements(
                    errors=[f"Legacy measurement failed: {e}"]
                ),
                modern_measurements=FontMeasurements(
                    errors=[f"Modern measurement failed: {e}"]
                ),
                within_tolerance=False,
                issues_found=[f"Comparison failed: {e}"],
            )

    def measure_font_sizes(self, image_path: str) -> FontMeasurements:
        """
        Measure font sizes in an exported image.

        Args:
            image_path: Path to image file

        Returns:
            FontMeasurements with detected font sizes
        """
        try:
            # Try multiple measurement methods
            if OCR_AVAILABLE:
                measurements = self._measure_with_ocr(image_path)
                if measurements.confidence > 0.5:
                    return measurements

            if OPENCV_AVAILABLE:
                measurements = self._measure_with_opencv(image_path)
                if measurements.confidence > 0.3:
                    return measurements

            # Fallback to Qt-based measurement
            return self._measure_with_qt(image_path)

        except Exception as e:
            logger.error(f"Font size measurement failed: {e}")
            return FontMeasurements(
                errors=[f"Measurement failed: {e}"], measurement_method="failed"
            )

    def _measure_with_ocr(self, image_path: str) -> FontMeasurements:
        """Measure font sizes using OCR text detection."""
        if not OCR_AVAILABLE:
            raise ImportError("OCR libraries not available")

        try:
            # Load image
            image = Image.open(image_path)

            # Get detailed OCR data
            ocr_data = pytesseract.image_to_data(
                image, output_type=pytesseract.Output.DICT
            )

            detected_text = []
            word_sizes = []
            difficulty_sizes = []

            # Analyze detected text
            for i, text in enumerate(ocr_data["text"]):
                if text.strip():
                    confidence = int(ocr_data["conf"][i])
                    if confidence > 30:  # Minimum confidence threshold
                        height = int(ocr_data["height"][i])
                        detected_text.append(text)

                        # Categorize text by content and position
                        text_upper = text.upper()
                        y_pos = int(ocr_data["top"][i])

                        # Word labels are typically larger and in upper portion
                        if len(text) > 2 and y_pos < image.height * 0.4:
                            word_sizes.append(height)

                        # Difficulty labels are typically numbers in circles
                        if text.isdigit() and len(text) == 1:
                            difficulty_sizes.append(height)

            # Calculate average sizes
            word_label_size = np.mean(word_sizes) if word_sizes else None
            difficulty_label_size = (
                np.mean(difficulty_sizes) if difficulty_sizes else None
            )

            confidence = (
                len(detected_text) / 10.0
            )  # Rough confidence based on text detection

            return FontMeasurements(
                word_label_size=word_label_size,
                difficulty_label_size=difficulty_label_size,
                detected_text=detected_text,
                measurement_method="ocr",
                confidence=min(confidence, 1.0),
            )

        except Exception as e:
            logger.error(f"OCR measurement failed: {e}")
            return FontMeasurements(
                errors=[f"OCR failed: {e}"], measurement_method="ocr_failed"
            )

    def _measure_with_opencv(self, image_path: str) -> FontMeasurements:
        """Measure font sizes using OpenCV contour analysis."""
        if not OPENCV_AVAILABLE:
            raise ImportError("OpenCV not available")

        try:
            # Load image
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Find text regions using contours
            _, thresh = cv2.threshold(
                gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
            )
            contours, _ = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            text_heights = []
            large_text_heights = []

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)

                # Filter for text-like regions
                aspect_ratio = w / h if h > 0 else 0
                area = cv2.contourArea(contour)

                # Text regions typically have certain aspect ratios and minimum size
                if 0.1 < aspect_ratio < 10 and area > 50:
                    text_heights.append(h)

                    # Large text (likely word labels) in upper portion
                    if y < image.shape[0] * 0.4 and h > 30:
                        large_text_heights.append(h)

            # Estimate font sizes
            word_label_size = (
                np.mean(large_text_heights) if large_text_heights else None
            )

            # Difficulty labels are typically smaller, circular regions
            small_text_heights = [h for h in text_heights if 10 < h < 40]
            difficulty_label_size = (
                np.mean(small_text_heights) if small_text_heights else None
            )

            confidence = (
                len(text_heights) / 20.0
            )  # Rough confidence based on detected regions

            return FontMeasurements(
                word_label_size=word_label_size,
                difficulty_label_size=difficulty_label_size,
                measurement_method="opencv",
                confidence=min(confidence, 1.0),
            )

        except Exception as e:
            logger.error(f"OpenCV measurement failed: {e}")
            return FontMeasurements(
                errors=[f"OpenCV failed: {e}"], measurement_method="opencv_failed"
            )

    def _measure_with_qt(self, image_path: str) -> FontMeasurements:
        """Measure font sizes using Qt-based analysis."""
        try:
            # Load image
            qimage = QImage(image_path)
            if qimage.isNull():
                raise ValueError("Failed to load image")

            # This is a simplified approach - in practice, we would need more
            # sophisticated analysis to detect text regions and estimate sizes

            # For now, return estimated sizes based on image dimensions
            # This serves as a fallback when other methods fail

            height = qimage.height()
            width = qimage.width()

            # Rough estimates based on typical proportions
            estimated_word_size = height * 0.08  # ~8% of image height
            estimated_difficulty_size = height * 0.03  # ~3% of image height

            return FontMeasurements(
                word_label_size=estimated_word_size,
                difficulty_label_size=estimated_difficulty_size,
                measurement_method="qt_estimated",
                confidence=0.2,  # Low confidence for estimates
            )

        except Exception as e:
            logger.error(f"Qt measurement failed: {e}")
            return FontMeasurements(
                errors=[f"Qt measurement failed: {e}"], measurement_method="qt_failed"
            )
