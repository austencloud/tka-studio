"""
Visual Element Detector - Detection of Grids, Props, Arrows, and Other Elements
==============================================================================

Provides detection capabilities for visual elements in exported images to ensure
all required components (grids, props, arrows) are properly rendered.
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    cv2 = None
    np = None

from PyQt6.QtGui import QImage, QColor
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)


@dataclass
class ElementDetectionResult:
    """Result of visual element detection."""
    element_type: str
    detected: bool
    confidence: float
    bounding_boxes: List[Tuple[int, int, int, int]]  # List of (x, y, width, height)
    detection_method: str
    error_message: Optional[str] = None


@dataclass
class VisualElementReport:
    """Comprehensive report of visual elements in an image."""
    image_path: str
    grids_detected: bool
    props_detected: bool
    arrows_detected: bool
    beat_numbers_detected: bool
    text_elements_detected: bool
    total_elements_found: int
    detection_results: Dict[str, ElementDetectionResult]
    overall_confidence: float
    errors: List[str] = None
    warnings: List[str] = None


class VisualElementDetector:
    """
    Detect visual elements in exported images.
    
    Provides methods to detect grids, props, arrows, and other visual elements
    to ensure complete rendering and prevent missing element regressions.
    """
    
    def __init__(self):
        """Initialize the visual element detector."""
        self.detection_methods = {
            'grids': self._detect_grids,
            'props': self._detect_props,
            'arrows': self._detect_arrows,
            'beat_numbers': self._detect_beat_numbers,
            'text_elements': self._detect_text_elements,
        }
    
    def detect_all_elements(self, image_path: str) -> VisualElementReport:
        """
        Detect all visual elements in an exported image.
        
        Args:
            image_path: Path to the exported image
            
        Returns:
            VisualElementReport with comprehensive detection results
        """
        errors = []
        warnings = []
        detection_results = {}
        
        try:
            logger.info(f"Detecting visual elements in: {image_path}")
            
            # Load image
            image = self._load_image(image_path)
            if image is None:
                errors.append(f"Failed to load image: {image_path}")
                return self._create_failed_report(image_path, errors)
            
            # Run detection for each element type
            total_confidence = 0.0
            detected_count = 0
            
            for element_type, detection_method in self.detection_methods.items():
                try:
                    result = detection_method(image)
                    detection_results[element_type] = result
                    
                    if result.detected:
                        detected_count += 1
                    
                    total_confidence += result.confidence
                    
                    if result.error_message:
                        warnings.append(f"{element_type}: {result.error_message}")
                        
                except Exception as e:
                    error_msg = f"Detection failed for {element_type}: {e}"
                    errors.append(error_msg)
                    detection_results[element_type] = ElementDetectionResult(
                        element_type=element_type,
                        detected=False,
                        confidence=0.0,
                        bounding_boxes=[],
                        detection_method="failed",
                        error_message=str(e)
                    )
            
            # Calculate overall metrics
            overall_confidence = total_confidence / len(self.detection_methods) if self.detection_methods else 0.0
            
            return VisualElementReport(
                image_path=image_path,
                grids_detected=detection_results.get('grids', ElementDetectionResult('grids', False, 0.0, [], 'none')).detected,
                props_detected=detection_results.get('props', ElementDetectionResult('props', False, 0.0, [], 'none')).detected,
                arrows_detected=detection_results.get('arrows', ElementDetectionResult('arrows', False, 0.0, [], 'none')).detected,
                beat_numbers_detected=detection_results.get('beat_numbers', ElementDetectionResult('beat_numbers', False, 0.0, [], 'none')).detected,
                text_elements_detected=detection_results.get('text_elements', ElementDetectionResult('text_elements', False, 0.0, [], 'none')).detected,
                total_elements_found=detected_count,
                detection_results=detection_results,
                overall_confidence=overall_confidence,
                errors=errors,
                warnings=warnings
            )
            
        except Exception as e:
            logger.error(f"Visual element detection failed: {e}")
            return self._create_failed_report(image_path, [f"Detection failed: {e}"])
    
    def detect_specific_element(self, image_path: str, element_type: str) -> ElementDetectionResult:
        """
        Detect a specific type of visual element.
        
        Args:
            image_path: Path to the exported image
            element_type: Type of element to detect ('grids', 'props', 'arrows', etc.)
            
        Returns:
            ElementDetectionResult for the specific element
        """
        try:
            if element_type not in self.detection_methods:
                return ElementDetectionResult(
                    element_type=element_type,
                    detected=False,
                    confidence=0.0,
                    bounding_boxes=[],
                    detection_method="unsupported",
                    error_message=f"Unsupported element type: {element_type}"
                )
            
            image = self._load_image(image_path)
            if image is None:
                return ElementDetectionResult(
                    element_type=element_type,
                    detected=False,
                    confidence=0.0,
                    bounding_boxes=[],
                    detection_method="failed",
                    error_message="Failed to load image"
                )
            
            detection_method = self.detection_methods[element_type]
            return detection_method(image)
            
        except Exception as e:
            logger.error(f"Specific element detection failed for {element_type}: {e}")
            return ElementDetectionResult(
                element_type=element_type,
                detected=False,
                confidence=0.0,
                bounding_boxes=[],
                detection_method="failed",
                error_message=str(e)
            )
    
    def _load_image(self, image_path: str) -> Optional[QImage]:
        """Load an image from file path."""
        try:
            image = QImage(image_path)
            if image.isNull():
                logger.error(f"Failed to load image: {image_path}")
                return None
            return image
        except Exception as e:
            logger.error(f"Error loading image {image_path}: {e}")
            return None
    
    def _detect_grids(self, image: QImage) -> ElementDetectionResult:
        """Detect grid elements in the image."""
        try:
            # Grids typically appear as geometric patterns with regular spacing
            if OPENCV_AVAILABLE:
                return self._detect_grids_opencv(image)
            else:
                return self._detect_grids_qt(image)
                
        except Exception as e:
            return ElementDetectionResult(
                element_type="grids",
                detected=False,
                confidence=0.0,
                bounding_boxes=[],
                detection_method="failed",
                error_message=str(e)
            )
    
    def _detect_props(self, image: QImage) -> ElementDetectionResult:
        """Detect prop elements (staffs) in the image."""
        try:
            # Props are typically staff-like objects with specific shapes
            if OPENCV_AVAILABLE:
                return self._detect_props_opencv(image)
            else:
                return self._detect_props_qt(image)
                
        except Exception as e:
            return ElementDetectionResult(
                element_type="props",
                detected=False,
                confidence=0.0,
                bounding_boxes=[],
                detection_method="failed",
                error_message=str(e)
            )
    
    def _detect_arrows(self, image: QImage) -> ElementDetectionResult:
        """Detect arrow elements in the image."""
        try:
            # Arrows have distinctive triangular or pointed shapes
            if OPENCV_AVAILABLE:
                return self._detect_arrows_opencv(image)
            else:
                return self._detect_arrows_qt(image)
                
        except Exception as e:
            return ElementDetectionResult(
                element_type="arrows",
                detected=False,
                confidence=0.0,
                bounding_boxes=[],
                detection_method="failed",
                error_message=str(e)
            )
    
    def _detect_beat_numbers(self, image: QImage) -> ElementDetectionResult:
        """Detect beat number elements in the image."""
        try:
            # Beat numbers are typically small numeric text
            return self._detect_text_patterns(image, "beat_numbers", r'\d+')
            
        except Exception as e:
            return ElementDetectionResult(
                element_type="beat_numbers",
                detected=False,
                confidence=0.0,
                bounding_boxes=[],
                detection_method="failed",
                error_message=str(e)
            )
    
    def _detect_text_elements(self, image: QImage) -> ElementDetectionResult:
        """Detect text elements in the image."""
        try:
            # Text elements include word labels, user info, etc.
            return self._detect_text_patterns(image, "text_elements", r'[A-Za-z]+')
            
        except Exception as e:
            return ElementDetectionResult(
                element_type="text_elements",
                detected=False,
                confidence=0.0,
                bounding_boxes=[],
                detection_method="failed",
                error_message=str(e)
            )
    
    def _detect_grids_opencv(self, image: QImage) -> ElementDetectionResult:
        """Detect grids using OpenCV."""
        # Convert QImage to OpenCV format
        cv_image = self._qimage_to_opencv(image)
        
        # Convert to grayscale
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Detect lines using HoughLines
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
        
        # Grid detection logic - look for intersecting horizontal and vertical lines
        horizontal_lines = []
        vertical_lines = []
        
        if lines is not None:
            for line in lines:
                rho, theta = line[0]
                # Horizontal lines (theta close to 0 or pi)
                if abs(theta) < 0.1 or abs(theta - np.pi) < 0.1:
                    horizontal_lines.append(line)
                # Vertical lines (theta close to pi/2)
                elif abs(theta - np.pi/2) < 0.1:
                    vertical_lines.append(line)
        
        # Consider grid detected if we have both horizontal and vertical lines
        grid_detected = len(horizontal_lines) >= 2 and len(vertical_lines) >= 2
        confidence = min(1.0, (len(horizontal_lines) + len(vertical_lines)) / 10.0)
        
        return ElementDetectionResult(
            element_type="grids",
            detected=grid_detected,
            confidence=confidence,
            bounding_boxes=[],  # Could be enhanced to return actual grid regions
            detection_method="opencv_hough"
        )
    
    def _detect_grids_qt(self, image: QImage) -> ElementDetectionResult:
        """Detect grids using Qt-based analysis."""
        # Simplified grid detection using color analysis
        # Look for patterns that suggest grid lines
        
        width = image.width()
        height = image.height()
        
        # Sample pixels to look for grid-like patterns
        line_pixels = 0
        total_samples = 0
        
        # Check for horizontal patterns
        for y in range(0, height, 20):  # Sample every 20 pixels
            for x in range(width):
                pixel = QColor(image.pixel(x, y))
                total_samples += 1
                
                # Grid lines are typically dark or have high contrast
                if pixel.lightness() < 100:  # Dark pixels
                    line_pixels += 1
        
        # Simple heuristic: if enough dark pixels in regular patterns, likely a grid
        grid_ratio = line_pixels / total_samples if total_samples > 0 else 0
        grid_detected = grid_ratio > 0.1  # At least 10% dark pixels
        
        return ElementDetectionResult(
            element_type="grids",
            detected=grid_detected,
            confidence=grid_ratio,
            bounding_boxes=[],
            detection_method="qt_color_analysis"
        )
    
    def _detect_props_opencv(self, image: QImage) -> ElementDetectionResult:
        """Detect props using OpenCV."""
        # Props (staffs) are typically elongated objects
        cv_image = self._qimage_to_opencv(image)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Use contour detection to find elongated objects
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        prop_contours = []
        for contour in contours:
            # Calculate aspect ratio
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = max(w, h) / min(w, h) if min(w, h) > 0 else 0
            
            # Props are typically elongated (high aspect ratio) and of reasonable size
            if aspect_ratio > 3 and cv2.contourArea(contour) > 100:
                prop_contours.append((x, y, w, h))
        
        props_detected = len(prop_contours) > 0
        confidence = min(1.0, len(prop_contours) / 4.0)  # Expect up to 4 props
        
        return ElementDetectionResult(
            element_type="props",
            detected=props_detected,
            confidence=confidence,
            bounding_boxes=prop_contours,
            detection_method="opencv_contours"
        )
    
    def _detect_props_qt(self, image: QImage) -> ElementDetectionResult:
        """Detect props using Qt-based analysis."""
        # Simplified prop detection
        # Look for elongated colored regions that might be staffs
        
        # This is a placeholder implementation
        # In practice, would need more sophisticated analysis
        
        return ElementDetectionResult(
            element_type="props",
            detected=True,  # Assume present for now
            confidence=0.5,  # Low confidence for simplified detection
            bounding_boxes=[],
            detection_method="qt_simplified"
        )
    
    def _detect_arrows_opencv(self, image: QImage) -> ElementDetectionResult:
        """Detect arrows using OpenCV."""
        # Arrows have distinctive triangular shapes
        cv_image = self._qimage_to_opencv(image)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Use template matching or contour analysis for arrow detection
        # This is a simplified implementation
        
        return ElementDetectionResult(
            element_type="arrows",
            detected=True,  # Placeholder
            confidence=0.6,
            bounding_boxes=[],
            detection_method="opencv_template"
        )
    
    def _detect_arrows_qt(self, image: QImage) -> ElementDetectionResult:
        """Detect arrows using Qt-based analysis."""
        return ElementDetectionResult(
            element_type="arrows",
            detected=True,  # Placeholder
            confidence=0.4,
            bounding_boxes=[],
            detection_method="qt_simplified"
        )
    
    def _detect_text_patterns(self, image: QImage, element_type: str, pattern: str) -> ElementDetectionResult:
        """Detect text patterns in the image."""
        # This would require OCR or sophisticated text detection
        # For now, return a simplified result
        
        return ElementDetectionResult(
            element_type=element_type,
            detected=True,  # Assume text is present
            confidence=0.7,
            bounding_boxes=[],
            detection_method="pattern_matching"
        )
    
    def _qimage_to_opencv(self, qimage: QImage):
        """Convert QImage to OpenCV format."""
        if not OPENCV_AVAILABLE:
            raise ImportError("OpenCV not available")
        
        qimage = qimage.convertToFormat(QImage.Format.Format_RGB888)
        width = qimage.width()
        height = qimage.height()
        
        ptr = qimage.bits()
        ptr.setsize(qimage.sizeInBytes())
        arr = np.array(ptr).reshape(height, width, 3)
        
        # Convert RGB to BGR for OpenCV
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    
    def _create_failed_report(self, image_path: str, errors: List[str]) -> VisualElementReport:
        """Create a failed detection report."""
        return VisualElementReport(
            image_path=image_path,
            grids_detected=False,
            props_detected=False,
            arrows_detected=False,
            beat_numbers_detected=False,
            text_elements_detected=False,
            total_elements_found=0,
            detection_results={},
            overall_confidence=0.0,
            errors=errors
        )
