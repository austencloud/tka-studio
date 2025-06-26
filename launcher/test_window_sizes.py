#!/usr/bin/env python3
"""
Test script to verify the 3-row layout works at different window sizes.
"""

import sys
import logging
from pathlib import Path

# Add launcher to path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from launcher_window import TKAModernWindow
from tka_integration import TKAIntegrationService

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_window_size(width, height):
    """Test the launcher at a specific window size."""
    logger.info(f"🧪 Testing window size: {width}x{height}")

    # Create TKA integration
    tka_integration = TKAIntegrationService()

    # Create launcher window
    window = TKAModernWindow(tka_integration)

    # Set specific window size
    window.resize(width, height)
    window.show()

    # Schedule size analysis after layout is complete
    QTimer.singleShot(1000, lambda: analyze_layout(window, width, height))
    QTimer.singleShot(2000, QApplication.quit)


def analyze_layout(window, expected_width, expected_height):
    """Analyze the layout at the current window size."""
    logger.info(f"📊 Layout Analysis for {expected_width}x{expected_height}:")

    # Get the application grid
    app_grid = window.app_grid
    if not app_grid:
        logger.error("❌ Application grid not found")
        return

    # Check scroll area dimensions
    scroll_area = app_grid.scroll_area
    scroll_widget = app_grid.scroll_widget

    viewport_size = scroll_area.viewport().size()
    widget_size = scroll_widget.size()

    logger.info(
        f"   Scroll Area Viewport: {viewport_size.width()}x{viewport_size.height()}"
    )
    logger.info(f"   Scroll Widget: {widget_size.width()}x{widget_size.height()}")

    # Check if content fits without scrolling
    fits_horizontally = widget_size.width() <= viewport_size.width()
    fits_vertically = widget_size.height() <= viewport_size.height()

    if fits_horizontally and fits_vertically:
        logger.info("✅ Content fits perfectly without scrolling")
    else:
        logger.warning(f"⚠️  Content overflow detected:")
        if not fits_horizontally:
            logger.warning(
                f"   Horizontal overflow: {widget_size.width() - viewport_size.width()}px"
            )
        if not fits_vertically:
            logger.warning(
                f"   Vertical overflow: {widget_size.height() - viewport_size.height()}px"
            )


def main():
    """Test multiple window sizes."""
    app = QApplication(sys.argv)

    # Test different window sizes
    test_sizes = [
        (800, 600),  # Small window
        (1200, 800),  # Medium window
        (1600, 1000),  # Large window
        (600, 400),  # Very small window
    ]

    for width, height in test_sizes:
        logger.info(f"\n{'='*50}")
        test_window_size(width, height)
        app.exec()
        logger.info(f"{'='*50}\n")


if __name__ == "__main__":
    main()
