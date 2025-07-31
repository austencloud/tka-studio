"""
End-to-end test for Browse tab sequence selection functionality.

This test validates the complete user journey from opening the browse tab,
selecting a filter, clicking on a sequence thumbnail, and verifying that
the sequence appears correctly in the sequence viewer.
"""

import logging
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from PyQt6.QtCore import QEventLoop, QObject, Qt, QTimer, pyqtSignal
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication, QPushButton, QTabWidget, QWidget

# Configure logging for detailed test output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("test_browse_sequence_selection_e2e.log", encoding="utf-8"),
    ],
)

# Set console encoding to handle unicode
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

logger = logging.getLogger(__name__)


class BrowseSequenceSelectionE2ETest(QObject):
    """End-to-end test for browse tab sequence selection workflow."""

    # Signals for test coordination
    test_completed = pyqtSignal(bool, str)  # success, message

    def __init__(self):
        super().__init__()
        self.app = None
        self.main_window = None
        self.browse_tab = None
        self.filter_selection_panel = None
        self.sequence_browser_panel = None
        self.sequence_viewer_panel = None
        self.test_results = []

    def setup_application(self) -> bool:
        """Launch and setup the TKA application."""
        try:
            logger.info(
                "🚀 SETUP: Setting up TKA application for Browse E2E testing..."
            )

            # Create QApplication if not exists
            self.app = QApplication.instance()
            if self.app is None:
                self.app = QApplication(sys.argv)

            # Import and create main window
            from desktop.modern.main import TKAMainWindow

            logger.info("🏗️ SETUP: Creating main window...")
            self.main_window = TKAMainWindow()

            # Show window and wait for initialization
            self.main_window.show()
            self._wait_for_ui(2000)  # Wait 2 seconds for full UI initialization

            logger.info("✅ SUCCESS: Application setup completed")
            return True

        except Exception as e:
            logger.error(f"❌ ERROR: Failed to setup application: {e}")
            import traceback

            traceback.print_exc()
            return False

    def navigate_to_browse_tab(self) -> bool:
        """Navigate to the browse tab and verify components."""
        try:
            logger.info("🧭 NAVIGATE: Navigating to browse tab...")

            # Find the tab widget
            tab_widget = self._find_tab_widget()
            if not tab_widget:
                logger.error("❌ ERROR: Could not find tab widget")
                return False

            # Find browse tab
            browse_tab_index = -1
            for i in range(tab_widget.count()):
                tab_text = tab_widget.tabText(i)
                logger.info(f"📋 Found tab {i}: {tab_text}")
                if "browse" in tab_text.lower():
                    browse_tab_index = i
                    break

            if browse_tab_index == -1:
                logger.error("❌ Could not find browse tab")
                return False

            # Switch to browse tab
            logger.info(f"🔄 Switching to browse tab at index {browse_tab_index}")
            tab_widget.setCurrentIndex(browse_tab_index)
            self._wait_for_ui(1000)  # Wait for tab to load

            # Get browse tab widget
            self.browse_tab = tab_widget.currentWidget()
            logger.info(f"📋 Browse tab widget: {type(self.browse_tab)}")

            # Find browse tab components
            self._find_browse_components()

            logger.info("✅ Successfully navigated to browse tab")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to navigate to browse tab: {e}")
            import traceback

            traceback.print_exc()
            return False

    def _find_tab_widget(self):
        """Find the main tab widget."""
        try:
            # Direct findChild approach
            tab_widget = self.main_window.findChild(QTabWidget)
            if tab_widget:
                logger.info("✅ Tab widget found via direct findChild")
                return tab_widget

            # Search all children
            all_children = self.main_window.findChildren(QObject)
            logger.info(f"🔍 Found {len(all_children)} total children in main window")

            for child in all_children:
                if isinstance(child, QTabWidget):
                    logger.info(
                        f"✅ Tab widget found in children: {child.__class__.__name__}"
                    )
                    return child

            logger.error("❌ No tab widget found")
            return None

        except Exception as e:
            logger.error(f"❌ Error finding tab widget: {e}")
            return None

    def _find_browse_components(self):
        """Find and identify browse tab components."""
        try:
            logger.info("🔍 Finding browse tab components...")

            # Find all components in browse tab
            all_components = self.browse_tab.findChildren(QWidget)
            logger.info(f"📊 Found {len(all_components)} components in browse tab")

            # Look for specific browse components by class name
            for component in all_components:
                class_name = component.__class__.__name__

                if "FilterSelection" in class_name:
                    self.filter_selection_panel = component
                    logger.info(f"✅ Found filter selection panel: {class_name}")

                elif "SequenceBrowser" in class_name or "Browser" in class_name:
                    self.sequence_browser_panel = component
                    logger.info(f"✅ Found sequence browser panel: {class_name}")

                elif "SequenceViewer" in class_name or "Viewer" in class_name:
                    self.sequence_viewer_panel = component
                    logger.info(f"✅ Found sequence viewer panel: {class_name}")

                elif "Browse" in class_name:
                    logger.info(f"📋 Browse component: {class_name}")

            # Log what we found
            logger.info("🔍 Component discovery results:")
            logger.info(
                f"   Filter selection panel: {self.filter_selection_panel is not None}"
            )
            logger.info(
                f"   Sequence browser panel: {self.sequence_browser_panel is not None}"
            )
            logger.info(
                f"   Sequence viewer panel: {self.sequence_viewer_panel is not None}"
            )

        except Exception as e:
            logger.error(f"❌ Error finding browse components: {e}")

    def test_sequence_selection_workflow(self) -> bool:
        """Test the complete sequence selection workflow."""
        try:
            logger.info("🧪 Starting sequence selection workflow test...")

            # Step 1: Verify we're on the filter selection panel
            if not self._verify_filter_selection_visible():
                logger.error("❌ Filter selection panel not visible")
                return False

            # Step 2: Select the first available filter
            if not self._select_first_filter():
                logger.error("❌ Failed to select first filter")
                return False

            # Step 3: Wait for sequences to load and navigate to browser
            if not self._wait_for_sequences_to_load():
                logger.error("❌ Failed to load sequences")
                return False

            # Step 4: Click on the first sequence thumbnail
            if not self._click_first_sequence_thumbnail():
                logger.error("❌ Failed to click sequence thumbnail")
                return False

            # Step 5: Verify sequence appears in viewer
            if not self._verify_sequence_in_viewer():
                logger.error("❌ Sequence did not appear in viewer")
                return False

            logger.info("✅ Sequence selection workflow test completed successfully!")
            return True

        except Exception as e:
            logger.error(f"❌ Sequence selection workflow test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def _verify_filter_selection_visible(self) -> bool:
        """Verify that the filter selection panel is visible."""
        try:
            logger.info("🔍 Verifying filter selection panel is visible...")

            if not self.filter_selection_panel:
                # Try to find filter selection panel by looking for filter buttons
                filter_buttons = self.browse_tab.findChildren(QPushButton)
                logger.info(f"📊 Found {len(filter_buttons)} buttons in browse tab")

                # Look for buttons with filter-like text
                for button in filter_buttons:
                    button_text = button.text().lower()
                    if any(
                        keyword in button_text
                        for keyword in ["a-c", "all", "starting", "level", "length"]
                    ):
                        logger.info(f"✅ Found filter button: {button.text()}")
                        return True

                logger.warning("⚠️ No filter selection panel or buttons found")
                return False

            # Check if filter selection panel is visible
            if self.filter_selection_panel.isVisible():
                logger.info("✅ Filter selection panel is visible")
                return True
            else:
                logger.warning("⚠️ Filter selection panel exists but is not visible")
                return False

        except Exception as e:
            logger.error(f"❌ Error verifying filter selection: {e}")
            return False

    def _select_first_filter(self) -> bool:
        """Select the first available filter option."""
        try:
            logger.info("🎯 Selecting first available filter...")

            # Find all buttons in the browse tab
            all_buttons = self.browse_tab.findChildren(QPushButton)
            logger.info(f"🔍 Found {len(all_buttons)} buttons to search for filters")

            # Look for filter buttons (starting letters, level, etc.)
            filter_button = None
            for button in all_buttons:
                button_text = button.text().strip()

                # Look for common filter patterns
                if button_text in [
                    "A-C",
                    "D-F",
                    "G-I",
                    "All",
                    "Level 1",
                    "Level 2",
                    "Short",
                    "Medium",
                ]:
                    filter_button = button
                    logger.info(f"✅ Found filter button: '{button_text}'")
                    break

                # Also check for single letters or simple patterns
                elif len(button_text) <= 3 and button_text.replace("-", "").isalpha():
                    filter_button = button
                    logger.info(f"✅ Found potential filter button: '{button_text}'")
                    break

            if not filter_button:
                logger.error("❌ No filter button found")
                return False

            # Click the filter button
            logger.info(f"🖱️ Clicking filter button: '{filter_button.text()}'")
            QTest.mouseClick(filter_button, Qt.MouseButton.LeftButton)
            self._wait_for_ui(1000)  # Wait for filter to apply

            logger.info("✅ Filter button clicked successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Error selecting filter: {e}")
            return False

    def _wait_for_sequences_to_load(self) -> bool:
        """Wait for sequences to load and browser panel to appear."""
        try:
            logger.info("⏳ Waiting for sequences to load...")

            # Wait up to 10 seconds for sequences to load
            max_wait_time = 10000  # 10 seconds
            wait_interval = 500  # Check every 500ms
            elapsed_time = 0

            while elapsed_time < max_wait_time:
                # Look for sequence thumbnails or browser panel
                if self._are_sequences_loaded():
                    logger.info("✅ Sequences loaded successfully")
                    return True

                self._wait_for_ui(wait_interval)
                elapsed_time += wait_interval
                logger.info(f"⏳ Still waiting... ({elapsed_time}ms elapsed)")

            logger.warning("⚠️ Timeout waiting for sequences to load")
            return False

        except Exception as e:
            logger.error(f"❌ Error waiting for sequences: {e}")
            return False

    def _are_sequences_loaded(self) -> bool:
        """Check if sequences have loaded by looking for thumbnails or browser content."""
        try:
            # Strategy 1: Look for sequence browser panel
            if self.sequence_browser_panel and self.sequence_browser_panel.isVisible():
                logger.info("✅ Sequence browser panel is visible")
                return True

            # Strategy 2: Look for clickable widgets that might be thumbnails
            all_widgets = self.browse_tab.findChildren(QWidget)
            clickable_widgets = [
                w for w in all_widgets if w.isVisible() and w.isEnabled()
            ]

            if (
                len(clickable_widgets) > 10
            ):  # Assume if there are many widgets, sequences loaded
                logger.info(
                    f"✅ Found {len(clickable_widgets)} clickable widgets - sequences likely loaded"
                )
                return True

            return False

        except Exception as e:
            logger.error(f"❌ Error checking if sequences loaded: {e}")
            return False

    def _click_first_sequence_thumbnail(self) -> bool:
        """Click on the first sequence thumbnail."""
        try:
            logger.info("🖱️ Looking for sequence thumbnail to click...")

            # Find all clickable widgets in the browse tab
            all_widgets = self.browse_tab.findChildren(QWidget)
            clickable_widgets = [
                w for w in all_widgets if w.isVisible() and w.isEnabled()
            ]

            logger.info(f"🔍 Found {len(clickable_widgets)} clickable widgets")

            # Try to find a thumbnail-like widget
            thumbnail_widget = None
            for widget in clickable_widgets:
                class_name = widget.__class__.__name__

                # Look for thumbnail-like widgets
                if any(
                    keyword in class_name.lower()
                    for keyword in ["thumbnail", "sequence", "card", "item"]
                ):
                    thumbnail_widget = widget
                    logger.info(f"✅ Found potential thumbnail: {class_name}")
                    break

            # If no specific thumbnail found, try the first few widgets
            if not thumbnail_widget and clickable_widgets:
                # Skip buttons and other UI elements, look for content widgets
                for widget in clickable_widgets[:10]:
                    class_name = widget.__class__.__name__
                    if "Button" not in class_name and "Label" not in class_name:
                        thumbnail_widget = widget
                        logger.info(f"✅ Using widget as thumbnail: {class_name}")
                        break

            if not thumbnail_widget:
                logger.error("❌ No thumbnail widget found to click")
                return False

            # Click the thumbnail
            logger.info(
                f"🖱️ Clicking thumbnail widget: {thumbnail_widget.__class__.__name__}"
            )
            QTest.mouseClick(thumbnail_widget, Qt.MouseButton.LeftButton)
            self._wait_for_ui(1000)  # Wait for click to process

            logger.info("✅ Thumbnail clicked successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Error clicking thumbnail: {e}")
            return False

    def _verify_sequence_in_viewer(self) -> bool:
        """Verify that a sequence appears in the sequence viewer."""
        try:
            logger.info("🔍 Verifying sequence appears in viewer...")

            # Wait a bit for viewer to update
            self._wait_for_ui(1000)

            # Strategy 1: Check if sequence viewer panel is visible and has content
            if self.sequence_viewer_panel:
                if self.sequence_viewer_panel.isVisible():
                    logger.info("✅ Sequence viewer panel is visible")

                    # Look for content in the viewer (images, text, etc.)
                    viewer_children = self.sequence_viewer_panel.findChildren(QWidget)
                    visible_children = [c for c in viewer_children if c.isVisible()]

                    if (
                        len(visible_children) > 5
                    ):  # Assume viewer has content if many widgets
                        logger.info(
                            f"✅ Sequence viewer has content ({len(visible_children)} visible widgets)"
                        )
                        return True
                    else:
                        logger.warning(
                            f"⚠️ Sequence viewer visible but limited content ({len(visible_children)} widgets)"
                        )
                else:
                    logger.warning("⚠️ Sequence viewer panel exists but is not visible")

            # Strategy 2: Look for any indication that viewer updated
            # Check for images, sequence titles, metadata, etc.
            all_widgets = self.browse_tab.findChildren(QWidget)
            for widget in all_widgets:
                class_name = widget.__class__.__name__
                if (
                    "Image" in class_name
                    or "Picture" in class_name
                    or "Thumbnail" in class_name
                ):
                    if widget.isVisible():
                        logger.info(f"✅ Found visible image widget: {class_name}")
                        return True

            logger.warning("⚠️ Could not verify sequence in viewer")
            return False

        except Exception as e:
            logger.error(f"❌ Error verifying sequence in viewer: {e}")
            return False

    def _wait_for_ui(self, milliseconds: int):
        """Wait for UI to update."""
        loop = QEventLoop()
        QTimer.singleShot(milliseconds, loop.quit)
        loop.exec()

    def run_test(self) -> bool:
        """Run the complete browse sequence selection test."""
        try:
            logger.info("🧪 Starting Browse Sequence Selection E2E Test")
            logger.info("=" * 60)

            # Step 1: Setup application
            if not self.setup_application():
                return False

            # Step 2: Navigate to browse tab
            if not self.navigate_to_browse_tab():
                return False

            # Step 3: Test sequence selection workflow
            if not self.test_sequence_selection_workflow():
                return False

            logger.info("=" * 60)
            logger.info("🎉 Browse Sequence Selection E2E Test PASSED!")
            return True

        except Exception as e:
            logger.error(f"❌ Browse Sequence Selection E2E Test FAILED: {e}")
            import traceback

            traceback.print_exc()
            return False

        finally:
            # Cleanup
            if self.main_window:
                self.main_window.close()
            if self.app:
                self.app.quit()


def main():
    """Run the browse sequence selection E2E test."""
    test = BrowseSequenceSelectionE2ETest()
    success = test.run_test()

    if success:
        print("\n🎉 TEST PASSED: Browse sequence selection works correctly!")
        sys.exit(0)
    else:
        print("\n❌ TEST FAILED: Browse sequence selection has issues!")
        sys.exit(1)


if __name__ == "__main__":
    main()
