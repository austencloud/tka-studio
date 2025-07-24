"""
Image Comparator - Pixel-Perfect Legacy vs Modern Comparison
===========================================================

Provides comprehensive image comparison capabilities for detecting visual
regressions between Legacy and Modern image export systems.
"""

import logging
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("PIL/Pillow not available - some image comparison features will be limited")

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    logging.warning("OpenCV not available - template matching features will be limited")

from PyQt6.QtGui import QImage, QColor
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)


@dataclass
class ComparisonResult:
    """Result of image comparison."""
    images_match: bool
    pixel_difference_count: int
    total_pixels: int
    difference_percentage: float
    max_color_difference: int
    average_color_difference: float
    dimension_match: bool
    legacy_dimensions: Tuple[int, int]
    modern_dimensions: Tuple[int, int]
    difference_map_path: Optional[str] = None
    errors: List[str] = None
    warnings: List[str] = None


@dataclass
class RegionComparison:
    """Comparison result for a specific region."""
    region_name: str
    matches: bool
    difference_percentage: float
    bounding_box: Tuple[int, int, int, int]  # x, y, width, height


class ImageComparator:
    """
    Pixel-perfect Legacy vs Modern image comparison.
    
    Provides comprehensive comparison capabilities including pixel-level analysis,
    dimension validation, and difference visualization.
    """
    
    def __init__(self, tolerance_percentage: float = 0.1):
        """
        Initialize the image comparator.
        
        Args:
            tolerance_percentage: Acceptable difference percentage (0.0 to 100.0)
        """
        self.tolerance_percentage = tolerance_percentage
        self.difference_threshold = 10  # Color difference threshold (0-255)
    
    def compare_images_pixel_perfect(self, legacy_path: str, modern_path: str, 
                                   output_diff_path: Optional[str] = None) -> ComparisonResult:
        """
        Compare two images pixel by pixel for exact matching.
        
        Args:
            legacy_path: Path to legacy system export
            modern_path: Path to modern system export
            output_diff_path: Optional path to save difference visualization
            
        Returns:
            ComparisonResult with detailed comparison information
        """
        errors = []
        warnings = []
        
        try:
            # Load images
            legacy_img = self._load_image(legacy_path)
            modern_img = self._load_image(modern_path)
            
            if legacy_img is None:
                errors.append(f"Failed to load legacy image: {legacy_path}")
            if modern_img is None:
                errors.append(f"Failed to load modern image: {modern_path}")
            
            if errors:
                return ComparisonResult(
                    images_match=False,
                    pixel_difference_count=0,
                    total_pixels=0,
                    difference_percentage=100.0,
                    max_color_difference=255,
                    average_color_difference=255.0,
                    dimension_match=False,
                    legacy_dimensions=(0, 0),
                    modern_dimensions=(0, 0),
                    errors=errors
                )
            
            # Check dimensions
            legacy_dims = (legacy_img.width(), legacy_img.height())
            modern_dims = (modern_img.width(), modern_img.height())
            dimension_match = legacy_dims == modern_dims
            
            if not dimension_match:
                warnings.append(f"Dimension mismatch: Legacy {legacy_dims} vs Modern {modern_dims}")
            
            # Perform pixel comparison
            if PIL_AVAILABLE:
                result = self._compare_with_pil(legacy_img, modern_img, output_diff_path)
            else:
                result = self._compare_with_qt(legacy_img, modern_img)
            
            # Update result with dimension information
            result.dimension_match = dimension_match
            result.legacy_dimensions = legacy_dims
            result.modern_dimensions = modern_dims
            result.warnings = warnings
            
            # Determine if images match within tolerance
            result.images_match = (
                result.difference_percentage <= self.tolerance_percentage and
                dimension_match
            )
            
            logger.info(f"Image comparison completed: {result.difference_percentage:.2f}% difference")
            return result
            
        except Exception as e:
            logger.error(f"Image comparison failed: {e}")
            return ComparisonResult(
                images_match=False,
                pixel_difference_count=0,
                total_pixels=0,
                difference_percentage=100.0,
                max_color_difference=255,
                average_color_difference=255.0,
                dimension_match=False,
                legacy_dimensions=(0, 0),
                modern_dimensions=(0, 0),
                errors=[f"Comparison failed: {e}"]
            )
    
    def compare_regions(self, legacy_path: str, modern_path: str, 
                       regions: Dict[str, Tuple[int, int, int, int]]) -> List[RegionComparison]:
        """
        Compare specific regions of two images.
        
        Args:
            legacy_path: Path to legacy image
            modern_path: Path to modern image
            regions: Dictionary of region_name -> (x, y, width, height)
            
        Returns:
            List of RegionComparison results
        """
        results = []
        
        try:
            legacy_img = self._load_image(legacy_path)
            modern_img = self._load_image(modern_path)
            
            if not legacy_img or not modern_img:
                logger.error("Failed to load images for region comparison")
                return results
            
            for region_name, (x, y, width, height) in regions.items():
                try:
                    # Extract regions
                    legacy_region = legacy_img.copy(x, y, width, height)
                    modern_region = modern_img.copy(x, y, width, height)
                    
                    # Compare regions
                    if PIL_AVAILABLE:
                        comparison = self._compare_with_pil(legacy_region, modern_region)
                    else:
                        comparison = self._compare_with_qt(legacy_region, modern_region)
                    
                    matches = comparison.difference_percentage <= self.tolerance_percentage
                    
                    results.append(RegionComparison(
                        region_name=region_name,
                        matches=matches,
                        difference_percentage=comparison.difference_percentage,
                        bounding_box=(x, y, width, height)
                    ))
                    
                except Exception as e:
                    logger.error(f"Failed to compare region '{region_name}': {e}")
                    results.append(RegionComparison(
                        region_name=region_name,
                        matches=False,
                        difference_percentage=100.0,
                        bounding_box=(x, y, width, height)
                    ))
            
        except Exception as e:
            logger.error(f"Region comparison failed: {e}")
        
        return results
    
    def _load_image(self, image_path: str) -> Optional[QImage]:
        """Load an image from file path."""
        try:
            path = Path(image_path)
            if not path.exists():
                logger.error(f"Image file does not exist: {image_path}")
                return None
            
            image = QImage(str(path))
            if image.isNull():
                logger.error(f"Failed to load image: {image_path}")
                return None
            
            return image
            
        except Exception as e:
            logger.error(f"Error loading image {image_path}: {e}")
            return None
    
    def _compare_with_pil(self, legacy_img: QImage, modern_img: QImage, 
                         output_diff_path: Optional[str] = None) -> ComparisonResult:
        """Compare images using PIL/Pillow for enhanced analysis."""
        try:
            # Convert QImage to PIL Image
            legacy_pil = self._qimage_to_pil(legacy_img)
            modern_pil = self._qimage_to_pil(modern_img)
            
            # Ensure same size for comparison
            if legacy_pil.size != modern_pil.size:
                # Resize to match legacy dimensions
                modern_pil = modern_pil.resize(legacy_pil.size, Image.Resampling.LANCZOS)
            
            # Calculate difference
            diff = ImageChops.difference(legacy_pil, modern_pil)
            
            # Convert to numpy for analysis
            diff_array = np.array(diff)
            legacy_array = np.array(legacy_pil)
            
            # Calculate statistics
            total_pixels = diff_array.size // diff_array.shape[-1] if len(diff_array.shape) > 2 else diff_array.size
            
            # Calculate color differences
            if len(diff_array.shape) == 3:  # Color image
                color_diff = np.sqrt(np.sum(diff_array ** 2, axis=2))
            else:  # Grayscale
                color_diff = diff_array
            
            different_pixels = np.sum(color_diff > self.difference_threshold)
            max_diff = np.max(color_diff)
            avg_diff = np.mean(color_diff)
            
            difference_percentage = (different_pixels / total_pixels) * 100
            
            # Save difference map if requested
            diff_map_path = None
            if output_diff_path:
                diff_map_path = self._save_difference_map(diff, output_diff_path)
            
            return ComparisonResult(
                images_match=difference_percentage <= self.tolerance_percentage,
                pixel_difference_count=int(different_pixels),
                total_pixels=int(total_pixels),
                difference_percentage=float(difference_percentage),
                max_color_difference=int(max_diff),
                average_color_difference=float(avg_diff),
                dimension_match=legacy_pil.size == modern_pil.size,
                legacy_dimensions=legacy_pil.size,
                modern_dimensions=modern_pil.size,
                difference_map_path=diff_map_path
            )
            
        except Exception as e:
            logger.error(f"PIL comparison failed: {e}")
            return self._compare_with_qt(legacy_img, modern_img)
    
    def _compare_with_qt(self, legacy_img: QImage, modern_img: QImage) -> ComparisonResult:
        """Compare images using Qt native methods."""
        try:
            # Ensure same format
            legacy_img = legacy_img.convertToFormat(QImage.Format.Format_ARGB32)
            modern_img = modern_img.convertToFormat(QImage.Format.Format_ARGB32)
            
            # Get dimensions
            width = min(legacy_img.width(), modern_img.width())
            height = min(legacy_img.height(), modern_img.height())
            
            different_pixels = 0
            total_pixels = width * height
            max_diff = 0
            total_diff = 0
            
            # Compare pixel by pixel
            for y in range(height):
                for x in range(width):
                    legacy_color = QColor(legacy_img.pixel(x, y))
                    modern_color = QColor(modern_img.pixel(x, y))
                    
                    # Calculate color difference
                    r_diff = abs(legacy_color.red() - modern_color.red())
                    g_diff = abs(legacy_color.green() - modern_color.green())
                    b_diff = abs(legacy_color.blue() - modern_color.blue())
                    
                    color_diff = max(r_diff, g_diff, b_diff)
                    total_diff += color_diff
                    
                    if color_diff > self.difference_threshold:
                        different_pixels += 1
                    
                    max_diff = max(max_diff, color_diff)
            
            difference_percentage = (different_pixels / total_pixels) * 100 if total_pixels > 0 else 0
            avg_diff = total_diff / total_pixels if total_pixels > 0 else 0
            
            return ComparisonResult(
                images_match=difference_percentage <= self.tolerance_percentage,
                pixel_difference_count=different_pixels,
                total_pixels=total_pixels,
                difference_percentage=difference_percentage,
                max_color_difference=max_diff,
                average_color_difference=avg_diff,
                dimension_match=legacy_img.size() == modern_img.size(),
                legacy_dimensions=(legacy_img.width(), legacy_img.height()),
                modern_dimensions=(modern_img.width(), modern_img.height())
            )
            
        except Exception as e:
            logger.error(f"Qt comparison failed: {e}")
            raise
    
    def _qimage_to_pil(self, qimage: QImage) -> Image.Image:
        """Convert QImage to PIL Image."""
        if not PIL_AVAILABLE:
            raise ImportError("PIL not available")
        
        # Convert to ARGB32 format
        qimage = qimage.convertToFormat(QImage.Format.Format_ARGB32)
        
        width = qimage.width()
        height = qimage.height()
        
        # Get image data
        ptr = qimage.bits()
        ptr.setsize(qimage.sizeInBytes())
        arr = np.array(ptr).reshape(height, width, 4)  # ARGB
        
        # Convert ARGB to RGB
        rgb_arr = arr[:, :, [2, 1, 0]]  # BGR to RGB
        
        return Image.fromarray(rgb_arr, 'RGB')
    
    def _save_difference_map(self, diff_image: Image.Image, output_path: str) -> str:
        """Save difference map visualization."""
        try:
            # Enhance difference visibility
            enhanced_diff = diff_image.point(lambda x: x * 3)  # Amplify differences
            enhanced_diff.save(output_path)
            logger.debug(f"Difference map saved to: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to save difference map: {e}")
            return None
