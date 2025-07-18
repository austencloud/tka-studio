"""
Visual Testing for Thumbnail Sizing - Modern Browse Tab

This test actually runs the TKA application and measures thumbnail heights
to ensure they properly accommodate their image content.
"""

import sys
import time
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QFrame
from PyQt6.QtCore import QTimer, Qt, QSize
from PyQt6.QtGui import QPixmap, QScreen
from PyQt6.QtTest import QTest

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
sys.path.insert(
    0, str(Path(__file__).parent.parent.parent / "src" / "desktop" / "modern")
)

from main import TKAApplication
from src.presentation.tabs.browse.components.sequence_browser_panel import (
    SequenceBrowserPanel,
)


@dataclass
class ThumbnailMeasurement:
    """Measurement data for a single thumbnail."""

    sequence_id: str
    word: str
    container_width: int
    container_height: int
    image_width: int
    image_height: int
    content_height: int  # Height of all content (word + image + info)
    is_height_adequate: bool
    height_ratio: float  # content_height / container_height
    has_clipping: bool


class ThumbnailSizingTester:
    """Visual tester for thumbnail sizing in the modern browse tab."""

    def __init__(self):
        self.app = None
        self.main_window = None
        self.browse_panel = None
        self.measurements: List[ThumbnailMeasurement] = []
        self.test_results = {}

    def setup_application(self) -> bool:
        """Setup the TKA application for testing."""
        try:
            # Create application if it doesn't exist
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
            else:
                self.app = QApplication.instance()

            # Create main application window
            self.main_window = TKAApplication()
            self.main_window.show()

            # Wait for window to be ready
            QTest.qWait(2000)

            return True

        except Exception as e:
            print(f"Failed to setup application: {e}")
            return False

    def navigate_to_browse_tab(self) -> bool:
        """Navigate to the browse tab and load sequences."""
        try:
            # Find and click the browse tab
            browse_tab = self._find_widget_by_text(self.main_window, "Browse")
            if not browse_tab:
                print("Could not find Browse tab")
                return False

            # Click the browse tab
            QTest.mouseClick(browse_tab, Qt.MouseButton.LeftButton)
            QTest.qWait(1000)

            # Find the sequence browser panel
            self.browse_panel = self._find_widget_by_type(
                self.main_window, SequenceBrowserPanel
            )
            if not self.browse_panel:
                print("Could not find SequenceBrowserPanel")
                return False

            print("Successfully navigated to browse tab")
            return True

        except Exception as e:
            print(f"Failed to navigate to browse tab: {e}")
            return False

    def load_test_sequences(self) -> bool:
        """Load sequences for testing."""
        try:
            # Trigger sequence loading by applying default filters
            if hasattr(self.browse_panel, "show_sequences") and hasattr(
                self.browse_panel, "current_sequences"
            ):
                # Wait for sequences to load
                QTest.qWait(3000)

                if len(self.browse_panel.current_sequences) == 0:
                    print("No sequences loaded - trying to trigger loading...")
                    # Try to trigger loading by emulating filter application
                    # This might need adjustment based on actual UI flow
                    return False

                print(f"Loaded {len(self.browse_panel.current_sequences)} sequences")
                return True
            else:
                print("Browse panel does not have expected methods")
                return False

        except Exception as e:
            print(f"Failed to load test sequences: {e}")
            return False

    def measure_thumbnails(self) -> List[ThumbnailMeasurement]:
        """Measure all visible thumbnails."""
        measurements = []

        if not self.browse_panel:
            print("No browse panel available for measurement")
            return measurements

        try:
            # Wait for thumbnails to render
            QTest.qWait(2000)

            # Find all thumbnail widgets
            thumbnails = self._find_thumbnail_widgets()

            print(f"Found {len(thumbnails)} thumbnail widgets")

            for i, thumbnail in enumerate(thumbnails):
                measurement = self._measure_single_thumbnail(thumbnail, i)
                if measurement:
                    measurements.append(measurement)

            self.measurements = measurements
            return measurements

        except Exception as e:
            print(f"Failed to measure thumbnails: {e}")
            return measurements

    def _measure_single_thumbnail(
        self, thumbnail: QWidget, index: int
    ) -> Optional[ThumbnailMeasurement]:
        """Measure a single thumbnail widget."""
        try:
            # Get container dimensions
            container_size = thumbnail.size()
            container_width = container_size.width()
            container_height = container_size.height()

            # Find child widgets
            layout = thumbnail.layout()
            if not layout:
                print(f"Thumbnail {index} has no layout")
                return None

            # Extract components
            word_label = None
            image_label = None
            info_label = None

            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    if isinstance(widget, QLabel):
                        # Determine widget type by font or style
                        font = widget.font()
                        if font.bold():
                            word_label = widget
                        elif widget.styleSheet().startswith(
                            "background: rgba(0, 0, 0, 0.2)"
                        ):
                            image_label = widget
                        else:
                            info_label = widget

            if not word_label:
                print(f"Thumbnail {index} missing word label")
                return None

            # Get sequence info
            sequence_word = word_label.text()
            sequence_id = f"seq_{index}"  # Fallback ID

            # Measure image dimensions
            image_width = 0
            image_height = 0
            if image_label:
                image_size = image_label.size()
                image_width = image_size.width()
                image_height = image_size.height()

            # Calculate content height
            content_height = 0
            if word_label:
                content_height += word_label.height()
            if image_label:
                content_height += image_label.height()
            if info_label:
                content_height += info_label.height()

            # Add spacing (5px between components according to code)
            content_height += 2 * 5  # 2 spacings

            # Add margins (10px top and bottom according to code)
            content_height += 20

            # Check if height is adequate
            is_height_adequate = container_height >= content_height
            height_ratio = content_height / max(container_height, 1)
            has_clipping = height_ratio > 1.0

            measurement = ThumbnailMeasurement(
                sequence_id=sequence_id,
                word=sequence_word,
                container_width=container_width,
                container_height=container_height,
                image_width=image_width,
                image_height=image_height,
                content_height=content_height,
                is_height_adequate=is_height_adequate,
                height_ratio=height_ratio,
                has_clipping=has_clipping,
            )

            print(f"Measured thumbnail {index}: {sequence_word}")
            print(f"  Container: {container_width}x{container_height}")
            print(f"  Image: {image_width}x{image_height}")
            print(f"  Content Height: {content_height}")
            print(f"  Height Adequate: {is_height_adequate}")
            print(f"  Height Ratio: {height_ratio:.2f}")

            return measurement

        except Exception as e:
            print(f"Failed to measure thumbnail {index}: {e}")
            return None

    def _find_thumbnail_widgets(self) -> List[QWidget]:
        """Find all thumbnail widgets in the browse panel."""
        thumbnails = []

        if not self.browse_panel:
            return thumbnails

        try:
            # The thumbnails are stored in thumbnail_widgets list
            if hasattr(self.browse_panel, "thumbnail_widgets"):
                thumbnails = self.browse_panel.thumbnail_widgets
            else:
                # Fallback: search for QFrame widgets with the right styling
                thumbnails = self._find_widgets_by_type(self.browse_panel, QFrame)
                # Filter for thumbnail frames
                thumbnails = [
                    t
                    for t in thumbnails
                    if "rgba(255, 255, 255, 0.1)" in t.styleSheet()
                ]

        except Exception as e:
            print(f"Error finding thumbnail widgets: {e}")

        return thumbnails

    def analyze_results(self) -> Dict:
        """Analyze measurement results and provide recommendations."""
        if not self.measurements:
            return {"error": "No measurements available"}

        # Calculate statistics
        total_thumbnails = len(self.measurements)
        adequate_height_count = sum(
            1 for m in self.measurements if m.is_height_adequate
        )
        clipping_count = sum(1 for m in self.measurements if m.has_clipping)

        # Height ratio statistics
        height_ratios = [m.height_ratio for m in self.measurements]
        avg_height_ratio = sum(height_ratios) / len(height_ratios)
        max_height_ratio = max(height_ratios)
        min_height_ratio = min(height_ratios)

        # Container size statistics
        container_heights = [m.container_height for m in self.measurements]
        avg_container_height = sum(container_heights) / len(container_heights)

        # Content height statistics
        content_heights = [m.content_height for m in self.measurements]
        avg_content_height = sum(content_heights) / len(content_heights)

        results = {
            "summary": {
                "total_thumbnails": total_thumbnails,
                "adequate_height_count": adequate_height_count,
                "adequate_height_percentage": (adequate_height_count / total_thumbnails)
                * 100,
                "clipping_count": clipping_count,
                "clipping_percentage": (clipping_count / total_thumbnails) * 100,
            },
            "height_analysis": {
                "avg_height_ratio": avg_height_ratio,
                "max_height_ratio": max_height_ratio,
                "min_height_ratio": min_height_ratio,
                "avg_container_height": avg_container_height,
                "avg_content_height": avg_content_height,
                "height_deficit": max(0, avg_content_height - avg_container_height),
            },
            "problematic_thumbnails": [
                {
                    "word": m.word,
                    "container_height": m.container_height,
                    "content_height": m.content_height,
                    "height_ratio": m.height_ratio,
                    "deficit": m.content_height - m.container_height,
                }
                for m in self.measurements
                if m.has_clipping
            ],
            "recommendations": self._generate_recommendations(),
        }

        self.test_results = results
        return results

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on measurements."""
        recommendations = []

        if not self.measurements:
            return ["No measurements available for analysis"]

        # Check clipping issues
        clipping_count = sum(1 for m in self.measurements if m.has_clipping)
        if clipping_count > 0:
            recommendations.append(
                f"⚠️ {clipping_count} thumbnails have content clipping"
            )

        # Check height ratios
        height_ratios = [m.height_ratio for m in self.measurements]
        avg_ratio = sum(height_ratios) / len(height_ratios)

        if avg_ratio > 1.1:
            recommendations.append(
                "📏 Container heights are too small - increase minimum height"
            )
        elif avg_ratio > 1.05:
            recommendations.append(
                "📐 Container heights are marginally small - consider slight increase"
            )
        elif avg_ratio < 0.7:
            recommendations.append(
                "📦 Container heights may be too large - consider reducing for better layout"
            )
        else:
            recommendations.append("✅ Container heights are appropriate")

        # Check for consistency
        max_ratio = max(height_ratios)
        min_ratio = min(height_ratios)
        if max_ratio - min_ratio > 0.3:
            recommendations.append(
                "🔧 Large variation in height ratios - consider dynamic sizing"
            )

        return recommendations

    def save_results(self, filename: str = "thumbnail_sizing_results.json") -> bool:
        """Save test results to file."""
        try:
            results_file = Path(__file__).parent / filename

            # Convert measurements to dict for JSON serialization
            measurements_dict = [
                {
                    "sequence_id": m.sequence_id,
                    "word": m.word,
                    "container_width": m.container_width,
                    "container_height": m.container_height,
                    "image_width": m.image_width,
                    "image_height": m.image_height,
                    "content_height": m.content_height,
                    "is_height_adequate": m.is_height_adequate,
                    "height_ratio": m.height_ratio,
                    "has_clipping": m.has_clipping,
                }
                for m in self.measurements
            ]

            full_results = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "measurements": measurements_dict,
                "analysis": self.test_results,
            }

            with open(results_file, "w") as f:
                json.dump(full_results, f, indent=2)

            print(f"Results saved to {results_file}")
            return True

        except Exception as e:
            print(f"Failed to save results: {e}")
            return False

    def run_full_test(self) -> bool:
        """Run the complete visual test."""
        print("🔍 Starting TKA Thumbnail Sizing Visual Test")
        print("=" * 50)

        # Setup application
        print("1. Setting up application...")
        if not self.setup_application():
            print("❌ Failed to setup application")
            return False
        print("✅ Application setup complete")

        # Navigate to browse tab
        print("2. Navigating to browse tab...")
        if not self.navigate_to_browse_tab():
            print("❌ Failed to navigate to browse tab")
            return False
        print("✅ Browse tab loaded")

        # Load test sequences
        print("3. Loading test sequences...")
        if not self.load_test_sequences():
            print("❌ Failed to load test sequences")
            return False
        print("✅ Test sequences loaded")

        # Measure thumbnails
        print("4. Measuring thumbnails...")
        measurements = self.measure_thumbnails()
        if not measurements:
            print("❌ No measurements collected")
            return False
        print(f"✅ Measured {len(measurements)} thumbnails")

        # Analyze results
        print("5. Analyzing results...")
        results = self.analyze_results()
        print("✅ Analysis complete")

        # Save results
        print("6. Saving results...")
        if self.save_results():
            print("✅ Results saved")
        else:
            print("⚠️ Failed to save results")

        # Print summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)

        if "summary" in results:
            summary = results["summary"]
            print(f"Total Thumbnails: {summary['total_thumbnails']}")
            print(
                f"Adequate Height: {summary['adequate_height_count']} ({summary['adequate_height_percentage']:.1f}%)"
            )
            print(
                f"Clipping Issues: {summary['clipping_count']} ({summary['clipping_percentage']:.1f}%)"
            )

        if "height_analysis" in results:
            height = results["height_analysis"]
            print(f"Average Height Ratio: {height['avg_height_ratio']:.2f}")
            print(f"Average Container Height: {height['avg_container_height']:.0f}px")
            print(f"Average Content Height: {height['avg_content_height']:.0f}px")
            if height["height_deficit"] > 0:
                print(f"Height Deficit: {height['height_deficit']:.0f}px")

        if "recommendations" in results:
            print("\n💡 RECOMMENDATIONS:")
            for rec in results["recommendations"]:
                print(f"  {rec}")

        return True

    def cleanup(self):
        """Clean up resources."""
        if self.main_window:
            self.main_window.close()
        if self.app:
            self.app.quit()

    # Helper methods
    def _find_widget_by_text(self, parent: QWidget, text: str) -> Optional[QWidget]:
        """Find a widget containing specific text."""
        for child in parent.findChildren(QWidget):
            if hasattr(child, "text") and child.text() == text:
                return child
        return None

    def _find_widget_by_type(
        self, parent: QWidget, widget_type: type
    ) -> Optional[QWidget]:
        """Find a widget of specific type."""
        widgets = parent.findChildren(widget_type)
        return widgets[0] if widgets else None

    def _find_widgets_by_type(
        self, parent: QWidget, widget_type: type
    ) -> List[QWidget]:
        """Find all widgets of specific type."""
        return parent.findChildren(widget_type)


def main():
    """Main test function."""
    tester = ThumbnailSizingTester()

    try:
        success = tester.run_full_test()

        if success:
            print("\n🎉 Visual test completed successfully!")
            print("Check thumbnail_sizing_results.json for detailed results")
        else:
            print("\n❌ Visual test failed")

    except KeyboardInterrupt:
        print("\n⏸️ Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
    finally:
        tester.cleanup()


if __name__ == "__main__":
    main()
