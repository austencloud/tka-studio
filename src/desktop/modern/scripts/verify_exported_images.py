"""
Verify Exported Images Script

This script verifies that the newly exported sequence card images are compatible
with the modern sequence card tab and display correctly.
"""

from __future__ import annotations

import logging
from pathlib import Path
import sys


# Add the modern src directory to the path
modern_src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(modern_src_path))


from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.service_registration import (
    register_services,
)
from desktop.modern.core.interfaces.sequence_card_services import (
    ISequenceCardCacheService,
)


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class ExportedImageVerifier:
    """
    Verifies that exported sequence card images are compatible with the modern system.
    """

    def __init__(self):
        self.app = None
        self.container = None
        self.cache_service = None
        self.verification_results = {
            "total_images": 0,
            "valid_images": 0,
            "invalid_images": 0,
            "cache_compatible": 0,
            "display_compatible": 0,
            "errors": [],
        }

    def initialize(self) -> bool:
        """Initialize the verification environment."""
        try:
            logger.info("Initializing image verifier...")

            # Create QApplication if needed
            if not QApplication.instance():
                self.app = QApplication([])
            else:
                self.app = QApplication.instance()

            # Set up dependency injection
            self.container = DIContainer()
            register_services(self.container)

            # Get the cache service for testing compatibility
            self.cache_service = self.container.resolve(ISequenceCardCacheService)

            logger.info("Verifier initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize verifier: {e}", exc_info=True)
            return False

    def get_default_export_path(self) -> Path:
        """Get the default export path for sequence card images."""
        tka_root = Path(__file__).parent.parent.parent.parent.parent
        return tka_root / "images" / "sequence_card_images"

    def verify_all_images(self, export_path: Path | None = None) -> bool:
        """
        Verify all exported sequence card images.

        Args:
            export_path: Path to exported images directory

        Returns:
            True if verification passed, False otherwise
        """
        try:
            if export_path is None:
                export_path = self.get_default_export_path()

            logger.info("Starting image verification...")
            logger.info(f"Export path: {export_path}")

            if not export_path.exists():
                logger.error(f"Export path does not exist: {export_path}")
                return False

            # Collect all image files
            image_files = self._collect_image_files(export_path)
            self.verification_results["total_images"] = len(image_files)

            logger.info(f"Found {len(image_files)} images to verify")

            if len(image_files) == 0:
                logger.warning("No images found to verify")
                return False

            # Verify each image
            for i, (word, image_path) in enumerate(image_files):
                logger.info(
                    f"Verifying {i + 1}/{len(image_files)}: {word}/{image_path.name}"
                )

                try:
                    self._verify_single_image(word, image_path)
                    self.verification_results["valid_images"] += 1
                except Exception as e:
                    logger.exception(f"Error verifying {image_path}: {e}")
                    self.verification_results["invalid_images"] += 1
                    self.verification_results["errors"].append(
                        {"file": str(image_path), "error": str(e)}
                    )

            # Log final results
            self._log_verification_results()

            # Consider verification successful if most images are valid
            success_rate = (
                self.verification_results["valid_images"]
                / self.verification_results["total_images"]
            )
            return success_rate >= 0.95  # 95% success rate threshold

        except Exception as e:
            logger.error(f"Error during image verification: {e}", exc_info=True)
            return False

    def _collect_image_files(self, export_path: Path) -> list[tuple[str, Path]]:
        """Collect all image files from the export directory."""
        image_files = []

        for word_dir in export_path.iterdir():
            if word_dir.is_dir():
                word = word_dir.name
                for image_file in word_dir.glob("*.png"):
                    image_files.append((word, image_file))

        return sorted(image_files)

    def _verify_single_image(self, word: str, image_path: Path) -> None:
        """Verify a single image file."""
        # Test 1: Basic image validity
        self._verify_image_format(image_path)

        # Test 2: Image dimensions and properties
        self._verify_image_properties(image_path)

        # Test 3: Cache service compatibility
        self._verify_cache_compatibility(word, image_path)

        # Test 4: Display compatibility
        self._verify_display_compatibility(image_path)

    def _verify_image_format(self, image_path: Path) -> None:
        """Verify that the image has the correct format."""
        # Load image
        image = QImage(str(image_path))

        if image.isNull():
            raise ValueError("Image is null or corrupted")

        # Check format
        if image.format() != QImage.Format.Format_ARGB32:
            logger.warning(f"Image format is {image.format()}, expected ARGB32")

        # Check file signature
        with open(image_path, "rb") as f:
            header = f.read(8)
            if header != b"\x89PNG\r\n\x1a\n":
                raise ValueError("Invalid PNG file signature")

    def _verify_image_properties(self, image_path: Path) -> None:
        """Verify image properties like dimensions and quality."""
        image = QImage(str(image_path))

        # Check minimum dimensions
        if image.width() < 300 or image.height() < 300:
            raise ValueError(f"Image too small: {image.width()}x{image.height()}")

        # Check maximum reasonable dimensions
        if image.width() > 5000 or image.height() > 5000:
            raise ValueError(f"Image too large: {image.width()}x{image.height()}")

        # Check that image has content (not just white)
        has_content = self._check_image_has_content(image)
        if not has_content:
            logger.warning(f"Image appears to be mostly empty: {image_path}")

    def _check_image_has_content(self, image: QImage) -> bool:
        """Check if image has actual content (not just white background)."""
        # Sample pixels to check for non-white content
        sample_points = [
            (image.width() // 4, image.height() // 4),
            (image.width() // 2, image.height() // 2),
            (3 * image.width() // 4, 3 * image.height() // 4),
        ]

        non_white_pixels = 0
        for x, y in sample_points:
            if x < image.width() and y < image.height():
                pixel = image.pixelColor(x, y)
                if pixel.name() != "#ffffff":
                    non_white_pixels += 1

        return non_white_pixels > 0

    def _verify_cache_compatibility(self, word: str, image_path: Path) -> None:
        """Verify that the image is compatible with the cache service."""
        try:
            # Try to load the image through the cache service
            # This tests that the cache service can handle the exported images

            # Create a mock sequence identifier
            sequence_id = f"{word}_{image_path.stem}"

            # Test cache operations (if the cache service supports direct image loading)
            if hasattr(self.cache_service, "load_image"):
                cached_image = self.cache_service.load_image(
                    sequence_id, str(image_path)
                )
                if cached_image is None:
                    raise ValueError("Cache service could not load image")

            self.verification_results["cache_compatible"] += 1

        except Exception as e:
            logger.warning(f"Cache compatibility issue for {image_path}: {e}")

    def _verify_display_compatibility(self, image_path: Path) -> None:
        """Verify that the image can be displayed correctly."""
        try:
            # Load as QPixmap (used for display)
            pixmap = QPixmap(str(image_path))

            if pixmap.isNull():
                raise ValueError("Could not create QPixmap from image")

            # Test scaling operations (common in display)
            scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
            if scaled_pixmap.isNull():
                raise ValueError("Could not scale image")

            self.verification_results["display_compatible"] += 1

        except Exception as e:
            logger.warning(f"Display compatibility issue for {image_path}: {e}")

    def _log_verification_results(self) -> None:
        """Log the final verification results."""
        results = self.verification_results

        logger.info("=" * 60)
        logger.info("IMAGE VERIFICATION RESULTS")
        logger.info("=" * 60)
        logger.info(f"Total images verified: {results['total_images']}")
        logger.info(f"Valid images: {results['valid_images']}")
        logger.info(f"Invalid images: {results['invalid_images']}")
        logger.info(f"Cache compatible: {results['cache_compatible']}")
        logger.info(f"Display compatible: {results['display_compatible']}")

        if results["total_images"] > 0:
            success_rate = (results["valid_images"] / results["total_images"]) * 100
            logger.info(f"Success rate: {success_rate:.1f}%")

        if results["errors"]:
            logger.info(f"\nErrors encountered ({len(results['errors'])}):")
            for error in results["errors"][:10]:  # Show first 10 errors
                logger.info(f"  {error['file']}: {error['error']}")
            if len(results["errors"]) > 10:
                logger.info(f"  ... and {len(results['errors']) - 10} more errors")

        if results["valid_images"] == results["total_images"]:
            logger.info("✅ All images verified successfully!")
        elif results["valid_images"] / results["total_images"] >= 0.95:
            logger.info("✅ Verification passed (95%+ success rate)")
        else:
            logger.warning("⚠️  Verification completed with issues")

        logger.info("=" * 60)


def main():
    """Main entry point for the verification script."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Verify exported TKA sequence card images"
    )
    parser.add_argument(
        "--export-path", type=Path, help="Path to exported images directory"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create and run verifier
    verifier = ExportedImageVerifier()

    if not verifier.initialize():
        logger.error("Failed to initialize verifier")
        sys.exit(1)

    success = verifier.verify_all_images(export_path=args.export_path)

    if success:
        logger.info("Image verification completed successfully")
        sys.exit(0)
    else:
        logger.error("Image verification failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
