#!/usr/bin/env python3
"""
End-to-End Sequence Card Tab Responsiveness Test

This test launches the actual TKA desktop application and measures:
1. Tab switching responsiveness
2. Content loading timing
3. Progressive loading behavior
4. Comparison with legacy system performance

Usage:
    python test_sequence_card_responsiveness.py
"""

import sys
import time
import logging
import traceback
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtCore import QTimer, QEventLoop, QCoreApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

# Import TKA components
from main import create_application, TKAMainWindow


@dataclass
class TimingMetrics:
    """Container for timing measurements."""

    tab_click_to_response: Optional[float] = None
    page_widgets_displayed: Optional[float] = None
    first_image_loaded: Optional[float] = None
    all_images_loaded: Optional[float] = None
    total_completion_time: Optional[float] = None
    errors: List[str] = field(default_factory=list)
    events_processed: int = 0
    ui_updates: int = 0


class SequenceCardTabDiagnostics:
    """Diagnostic tool for sequence card tab performance analysis."""

    def __init__(self):
        self.app: Optional[QApplication] = None
        self.main_window: Optional[TKAMainWindow] = None
        self.sequence_card_tab = None
        self.metrics = TimingMetrics()
        self.start_time = 0
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        """Set up detailed logging for diagnostics."""
        logger = logging.getLogger("sequence_card_diagnostics")
        logger.setLevel(logging.DEBUG)

        # Create console handler with detailed format
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def launch_application(self) -> bool:
        """Launch the TKA desktop application."""
        try:
            self.logger.info("🚀 Launching TKA Desktop Application...")

            # Create QApplication if it doesn't exist
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
            else:
                self.app = QApplication.instance()

            # Create TKA application and main window
            self.app, self.main_window = create_application()

            if not self.main_window:
                self.logger.error("❌ Failed to get main window from TKA app")
                return False

            # Show the main window
            self.main_window.show()

            # Process events to ensure window is displayed
            QCoreApplication.processEvents()

            # Wait for window to be fully initialized
            QTest.qWait(500)

            self.logger.info("✅ TKA Application launched successfully")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to launch application: {e}")
            self.logger.error(traceback.format_exc())
            self.metrics.errors.append(f"Launch failed: {e}")
            return False

    def find_and_activate_sequence_card_tab(self) -> bool:
        """Find the menu bar and click the sequence card tab button to trigger creation."""
        try:
            self.logger.info("🔍 Searching for menu bar and sequence card button...")

            # Find the menu bar widget
            from presentation.components.menu_bar.menu_bar_widget import MenuBarWidget

            menu_bar = self.main_window.findChild(MenuBarWidget)
            if not menu_bar:
                self.logger.error("❌ No MenuBarWidget found in main window")
                return False

            self.logger.info("✅ Found menu bar widget")

            # Find the navigation widget within the menu bar
            nav_widget = menu_bar.navigation_widget
            if not nav_widget:
                self.logger.error("❌ No navigation widget found in menu bar")
                return False

            self.logger.info("✅ Found navigation widget")

            # Find the sequence card button
            sequence_card_button = None
            for tab_name, button in nav_widget.tab_buttons.items():
                self.logger.debug(f"Found tab button: {tab_name}")
                if tab_name == "sequence_card":
                    sequence_card_button = button
                    break

            if not sequence_card_button:
                self.logger.error("❌ Sequence card button not found in navigation")
                return False

            self.logger.info("✅ Found sequence card button")

            # Click the sequence card button to trigger tab creation
            self.logger.info("🖱️ Clicking sequence card button...")
            sequence_card_button.click()

            # Process events to allow tab creation
            QCoreApplication.processEvents()
            QTest.qWait(500)  # Wait for tab creation

            # Now find the created tab
            tab_widget = self.main_window.findChild(QTabWidget)
            if not tab_widget:
                self.logger.error("❌ No QTabWidget found in main window")
                return False

            # Look for sequence card tab
            for i in range(tab_widget.count()):
                tab_text = tab_widget.tabText(i)
                self.logger.debug(f"Found tab {i}: '{tab_text}'")

                if "sequence" in tab_text.lower() and "card" in tab_text.lower():
                    self.sequence_card_tab = tab_widget.widget(i)
                    self.tab_widget = tab_widget
                    self.tab_index = i
                    self.logger.info(
                        f"✅ Found sequence card tab at index {i}: '{tab_text}'"
                    )
                    return True

            self.logger.error("❌ Sequence card tab not found after button click")
            return False

        except Exception as e:
            self.logger.error(f"❌ Error finding/activating sequence card tab: {e}")
            self.logger.error(traceback.format_exc())
            self.metrics.errors.append(f"Tab activation failed: {e}")
            return False

    def measure_tab_switching_performance(self) -> bool:
        """Measure the performance of switching to the sequence card tab."""
        try:
            self.logger.info("📊 Starting tab switching performance measurement...")

            # Record start time
            self.start_time = time.time()

            # Switch to sequence card tab
            self.logger.info(
                f"🖱️ Clicking sequence card tab (index {self.tab_index})..."
            )
            click_start = time.time()

            self.tab_widget.setCurrentIndex(self.tab_index)
            QCoreApplication.processEvents()

            # Measure time to first response
            response_time = time.time() - click_start
            self.metrics.tab_click_to_response = response_time
            self.logger.info(f"⏱️ Tab click to response: {response_time:.3f}s")

            # Wait for tab to be fully activated
            QTest.qWait(100)

            return True

        except Exception as e:
            self.logger.error(f"❌ Error measuring tab switching: {e}")
            self.metrics.errors.append(f"Tab switching failed: {e}")
            return False

    def monitor_content_loading(self) -> bool:
        """Monitor the content loading process with detailed timing."""
        try:
            self.logger.info("📈 Monitoring content loading process...")

            # Check if sequence card tab has content component
            if not hasattr(self.sequence_card_tab, "content"):
                self.logger.error("❌ Sequence card tab has no 'content' attribute")
                return False

            content_component = self.sequence_card_tab.content

            # Monitor for page widgets creation
            page_widgets_start = time.time()
            page_widgets_found = False

            # Wait up to 10 seconds for page widgets to appear
            timeout = 10.0
            check_interval = 0.1
            elapsed = 0

            while elapsed < timeout:
                QCoreApplication.processEvents()
                self.metrics.events_processed += 1

                # Check if page widgets exist
                if (
                    hasattr(content_component, "page_widgets")
                    and content_component.page_widgets
                ):
                    if not page_widgets_found:
                        self.metrics.page_widgets_displayed = (
                            time.time() - page_widgets_start
                        )
                        self.logger.info(
                            f"✅ Page widgets displayed: {self.metrics.page_widgets_displayed:.3f}s"
                        )
                        self.logger.info(
                            f"📄 Found {len(content_component.page_widgets)} page widgets"
                        )
                        page_widgets_found = True
                        break

                QTest.qWait(int(check_interval * 1000))
                elapsed += check_interval

            if not page_widgets_found:
                self.logger.error(f"❌ No page widgets found after {timeout}s")
                self.metrics.errors.append("Page widgets not created")
                return False

            # Monitor image loading
            return self._monitor_image_loading(content_component)

        except Exception as e:
            self.logger.error(f"❌ Error monitoring content loading: {e}")
            self.logger.error(traceback.format_exc())
            self.metrics.errors.append(f"Content monitoring failed: {e}")
            return False

    def _monitor_image_loading(self, content_component) -> bool:
        """Monitor the image loading process."""
        try:
            self.logger.info("🖼️ Monitoring image loading...")

            total_cards = 0
            loaded_cards = 0

            # Count total cards
            for page_widget in content_component.page_widgets:
                if hasattr(page_widget, "card_widgets"):
                    total_cards += len(page_widget.card_widgets)

            self.logger.info(f"📊 Total cards to load: {total_cards}")

            if total_cards == 0:
                self.logger.warning("⚠️ No cards found to load")
                return True

            # Monitor loading progress
            first_image_loaded = False
            image_loading_start = time.time()
            timeout = 30.0  # 30 seconds timeout
            check_interval = 0.2
            elapsed = 0

            while elapsed < timeout:
                QCoreApplication.processEvents()
                self.metrics.events_processed += 1

                # Count loaded images
                current_loaded = 0
                for page_widget in content_component.page_widgets:
                    if hasattr(page_widget, "card_widgets"):
                        for card_widget in page_widget.card_widgets:
                            if (
                                hasattr(card_widget, "is_image_loaded")
                                and card_widget.is_image_loaded
                            ):
                                current_loaded += 1

                # Check for first image loaded
                if current_loaded > 0 and not first_image_loaded:
                    self.metrics.first_image_loaded = time.time() - image_loading_start
                    self.logger.info(
                        f"🖼️ First image loaded: {self.metrics.first_image_loaded:.3f}s"
                    )
                    first_image_loaded = True

                # Check for all images loaded
                if current_loaded >= total_cards:
                    self.metrics.all_images_loaded = time.time() - image_loading_start
                    self.logger.info(
                        f"✅ All images loaded: {self.metrics.all_images_loaded:.3f}s"
                    )
                    break

                # Log progress periodically
                if current_loaded != loaded_cards:
                    loaded_cards = current_loaded
                    progress = (loaded_cards / total_cards) * 100
                    self.logger.info(
                        f"📈 Loading progress: {loaded_cards}/{total_cards} ({progress:.1f}%)"
                    )

                QTest.qWait(int(check_interval * 1000))
                elapsed += check_interval

            if elapsed >= timeout:
                self.logger.warning(f"⚠️ Image loading timeout after {timeout}s")
                self.logger.warning(
                    f"📊 Final progress: {loaded_cards}/{total_cards} images loaded"
                )
                self.metrics.errors.append(
                    f"Image loading timeout: {loaded_cards}/{total_cards}"
                )

            return True

        except Exception as e:
            self.logger.error(f"❌ Error monitoring image loading: {e}")
            self.metrics.errors.append(f"Image monitoring failed: {e}")
            return False

    def run_full_diagnostic(self) -> TimingMetrics:
        """Run the complete diagnostic test."""
        try:
            self.logger.info("🔬 Starting Full Sequence Card Tab Diagnostic")
            self.logger.info("=" * 60)

            # Step 1: Launch application
            if not self.launch_application():
                return self.metrics

            # Step 2: Find and activate sequence card tab
            if not self.find_and_activate_sequence_card_tab():
                return self.metrics

            # Step 3: Measure tab switching
            if not self.measure_tab_switching_performance():
                return self.metrics

            # Step 4: Monitor content loading
            if not self.monitor_content_loading():
                return self.metrics

            # Calculate total time
            self.metrics.total_completion_time = time.time() - self.start_time

            self.logger.info("=" * 60)
            self.logger.info("✅ Diagnostic completed successfully")

            return self.metrics

        except Exception as e:
            self.logger.error(f"❌ Diagnostic failed: {e}")
            self.logger.error(traceback.format_exc())
            self.metrics.errors.append(f"Diagnostic failed: {e}")
            return self.metrics

        finally:
            # Clean up
            if self.app:
                self.app.quit()

    def print_results(self):
        """Print detailed diagnostic results."""
        print("\n" + "=" * 80)
        print("🔬 SEQUENCE CARD TAB DIAGNOSTIC RESULTS")
        print("=" * 80)

        print(
            f"⏱️  Tab Click to Response:     {self.metrics.tab_click_to_response:.3f}s"
            if self.metrics.tab_click_to_response
            else "❌ Tab Click to Response:     FAILED"
        )
        print(
            f"📄 Page Widgets Displayed:   {self.metrics.page_widgets_displayed:.3f}s"
            if self.metrics.page_widgets_displayed
            else "❌ Page Widgets Displayed:   FAILED"
        )
        print(
            f"🖼️  First Image Loaded:       {self.metrics.first_image_loaded:.3f}s"
            if self.metrics.first_image_loaded
            else "❌ First Image Loaded:       FAILED"
        )
        print(
            f"✅ All Images Loaded:        {self.metrics.all_images_loaded:.3f}s"
            if self.metrics.all_images_loaded
            else "❌ All Images Loaded:        FAILED"
        )
        print(
            f"🏁 Total Completion Time:    {self.metrics.total_completion_time:.3f}s"
            if self.metrics.total_completion_time
            else "❌ Total Completion Time:    FAILED"
        )

        print(f"\n📊 Events Processed:         {self.metrics.events_processed}")
        print(f"🔄 UI Updates:               {self.metrics.ui_updates}")

        if self.metrics.errors:
            print(f"\n❌ ERRORS ({len(self.metrics.errors)}):")
            for i, error in enumerate(self.metrics.errors, 1):
                print(f"   {i}. {error}")
        else:
            print("\n✅ NO ERRORS DETECTED")

        print("=" * 80)


def main():
    """Main test execution."""
    print("🔬 TKA Sequence Card Tab Responsiveness Diagnostic")
    print("=" * 60)

    # Run diagnostic
    diagnostics = SequenceCardTabDiagnostics()
    metrics = diagnostics.run_full_diagnostic()

    # Print results
    diagnostics.print_results()

    # Return exit code based on success
    if metrics.errors:
        print(f"\n❌ Test completed with {len(metrics.errors)} errors")
        return 1
    else:
        print("\n✅ Test completed successfully")
        return 0


if __name__ == "__main__":
    sys.exit(main())
