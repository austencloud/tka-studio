"""
Comprehensive E2E Test for Option Picker Pagination Issue
=========================================================

This test reproduces the specific pagination pattern where selecting the same
start position multiple times in succession produces this exact sequence:
- Load 1: Displays all ~36 options correctly
- Load 2: Displays only first half
- Load 3: Displays only second half
- Load 4: Displays all ~36 options correctly again
- Pattern repeats...

The test uses the existing application factory to create a proper test environment.
"""

import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

# Import application factory for proper initialization
from core.application.application_factory import ApplicationFactory, ApplicationMode
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication, QMainWindow


@dataclass
class OptionLoadResult:
    """Represents the result of an option loading operation."""

    load_number: int
    option_count: int
    sections_with_options: Dict[str, int]  # section_name -> option_count
    timestamp: float
    error_message: Optional[str] = None


class OptionPickerPaginationTester:
    """
    Comprehensive tester for the option picker pagination issue.

    This class creates a realistic test environment and systematically
    reproduces the pagination pattern to identify the root cause.
    """

    def __init__(self):
        self.app: Optional[QApplication] = None
        self.main_window: Optional[QMainWindow] = None
        self.container = None
        self.construct_tab = None
        self.load_results: List[OptionLoadResult] = []

    def initialize(self) -> bool:
        """Initialize the test environment."""
        try:
            print("🚀 [PAGINATION_TEST] Initializing test environment...")

            # Create QApplication if needed
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
            else:
                self.app = QApplication.instance()

            # Create DI container using application factory
            print("🔧 [PAGINATION_TEST] Creating DI container...")
            self.container = ApplicationFactory.create_app(ApplicationMode.TEST)

            # Import and create construct tab
            from presentation.tabs.construct.construct_tab import ConstructTab

            print("🔧 [PAGINATION_TEST] Creating construct tab...")
            self.construct_tab = ConstructTab(container=self.container, parent=None)

            # Create main window
            self.main_window = QMainWindow()
            self.main_window.setWindowTitle("Option Picker Pagination Test")
            self.main_window.setCentralWidget(self.construct_tab)
            self.main_window.resize(1400, 900)
            self.main_window.show()

            # Wait for initialization
            self._wait_for_initialization()

            # Test environment ready for direct UI interaction

            print("✅ [PAGINATION_TEST] Test environment initialized successfully")
            return True

        except Exception as e:
            print(f"❌ [PAGINATION_TEST] Initialization failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    # Container creation now handled by ApplicationFactory

    def _wait_for_initialization(self, timeout_ms: int = 5000) -> None:
        """Wait for the UI to be fully initialized."""
        start_time = time.time()

        while time.time() - start_time < timeout_ms / 1000:
            QApplication.processEvents()

            # Check if construct tab is ready
            if (
                hasattr(self.construct_tab, "layout_manager")
                and self.construct_tab.layout_manager
                and hasattr(self.construct_tab.layout_manager, "start_position_picker")
            ):
                break

            time.sleep(0.1)

        # Additional wait for complete initialization
        QTest.qWait(1000)

    def run_pagination_test(
        self, position_key: str = "alpha1_alpha1", num_loads: int = 6
    ) -> bool:
        """
        Run the pagination test by selecting the same start position multiple times.

        Args:
            position_key: The start position to test with
            num_loads: Number of consecutive loads to perform

        Returns:
            True if the pagination pattern is reproduced, False otherwise
        """
        try:
            print(
                f"🎯 [PAGINATION_TEST] Starting pagination test with position: {position_key}"
            )
            print(f"📊 [PAGINATION_TEST] Will perform {num_loads} consecutive loads")

            # Clear any existing results
            self.load_results.clear()

            # Perform consecutive loads
            for load_num in range(1, num_loads + 1):
                print(f"\n🔄 [PAGINATION_TEST] === LOAD {load_num} ===")

                result = self._perform_single_load(position_key, load_num)
                self.load_results.append(result)

                # Log result
                if result.error_message:
                    print(
                        f"❌ [PAGINATION_TEST] Load {load_num} failed: {result.error_message}"
                    )
                else:
                    print(
                        f"✅ [PAGINATION_TEST] Load {load_num} completed: {result.option_count} options"
                    )
                    self._log_section_details(result)

                # Wait between loads to ensure proper processing
                QTest.qWait(500)

            # Analyze results
            return self._analyze_pagination_pattern()

        except Exception as e:
            print(f"❌ [PAGINATION_TEST] Test execution failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def _perform_single_load(
        self, position_key: str, load_number: int
    ) -> OptionLoadResult:
        """Perform a single load operation and capture the results."""
        try:
            timestamp = time.time()

            # Trigger start position selection
            success = self._select_start_position(position_key)
            if not success:
                return OptionLoadResult(
                    load_number=load_number,
                    option_count=0,
                    sections_with_options={},
                    timestamp=timestamp,
                    error_message="Failed to select start position",
                )

            # Wait for option loading to complete
            QTest.qWait(1000)

            # Count options in the option picker
            option_count, sections_data = self._count_displayed_options()

            return OptionLoadResult(
                load_number=load_number,
                option_count=option_count,
                sections_with_options=sections_data,
                timestamp=timestamp,
            )

        except Exception as e:
            return OptionLoadResult(
                load_number=load_number,
                option_count=0,
                sections_with_options={},
                timestamp=time.time(),
                error_message=str(e),
            )

    def _select_start_position(self, position_key: str) -> bool:
        """Select a start position using the UI."""
        try:
            # Get the start position picker
            if not hasattr(self.construct_tab, "layout_manager"):
                print("❌ [PAGINATION_TEST] Layout manager not found")
                return False

            layout_manager = self.construct_tab.layout_manager
            if not hasattr(layout_manager, "start_position_picker"):
                print("❌ [PAGINATION_TEST] Start position picker not found")
                return False

            start_position_picker = layout_manager.start_position_picker

            # Find the position option widget
            position_option = self._find_position_option(
                start_position_picker, position_key
            )
            if not position_option:
                print(f"❌ [PAGINATION_TEST] Position option {position_key} not found")
                return False

            # Click the position option
            QTest.mouseClick(position_option, Qt.MouseButton.LeftButton)

            # Wait for processing
            QTest.qWait(200)

            print(
                f"✅ [PAGINATION_TEST] Successfully selected position: {position_key}"
            )
            return True

        except Exception as e:
            print(f"❌ [PAGINATION_TEST] Error selecting start position: {e}")
            return False

    def _find_position_option(self, start_position_picker, position_key: str):
        """Find the position option widget for the given position key."""
        try:
            # Navigate through the picker structure to find position options
            if hasattr(start_position_picker, "content"):
                content = start_position_picker.content
                if hasattr(content, "position_options"):
                    for option in content.position_options:
                        if (
                            hasattr(option, "position_key")
                            and option.position_key == position_key
                        ):
                            return option

            print(
                f"❌ [PAGINATION_TEST] Could not find position option for {position_key}"
            )
            return None

        except Exception as e:
            print(f"❌ [PAGINATION_TEST] Error finding position option: {e}")
            return None

    def _count_displayed_options(self) -> Tuple[int, Dict[str, int]]:
        """Count the options currently displayed in the option picker."""
        try:
            total_count = 0
            sections_data = {}

            # Get the option picker
            if not hasattr(self.construct_tab, "layout_manager"):
                return 0, {}

            layout_manager = self.construct_tab.layout_manager
            if not hasattr(layout_manager, "option_picker_manager"):
                return 0, {}

            option_picker_manager = layout_manager.option_picker_manager
            if not hasattr(option_picker_manager, "option_picker"):
                return 0, {}

            option_picker = option_picker_manager.option_picker
            if not hasattr(option_picker, "option_picker_widget"):
                return 0, {}

            option_picker_widget = option_picker.option_picker_widget
            if not hasattr(option_picker_widget, "option_picker_scroll"):
                return 0, {}

            option_picker_scroll = option_picker_widget.option_picker_scroll
            if not hasattr(option_picker_scroll, "sections"):
                return 0, {}

            # Count options in each section
            sections = option_picker_scroll.sections
            for letter_type, section in sections.items():
                if hasattr(section, "pictographs") and section.pictographs:
                    section_count = len(section.pictographs)
                    sections_data[str(letter_type)] = section_count
                    total_count += section_count

            return total_count, sections_data

        except Exception as e:
            print(f"❌ [PAGINATION_TEST] Error counting options: {e}")
            return 0, {}

    def _log_section_details(self, result: OptionLoadResult) -> None:
        """Log detailed section information for a load result."""
        if result.sections_with_options:
            print(f"📋 [PAGINATION_TEST] Section breakdown:")
            for section_name, count in result.sections_with_options.items():
                print(f"   - {section_name}: {count} options")
        else:
            print(f"📋 [PAGINATION_TEST] No sections with options found")

    def _analyze_pagination_pattern(self) -> bool:
        """Analyze the load results to detect the pagination pattern."""
        try:
            print(f"\n📊 [PAGINATION_TEST] === ANALYSIS RESULTS ===")

            if len(self.load_results) < 4:
                print(f"❌ [PAGINATION_TEST] Insufficient data for pattern analysis")
                return False

            # Print summary
            print(f"📈 [PAGINATION_TEST] Load Summary:")
            for result in self.load_results:
                status = "✅" if not result.error_message else "❌"
                print(
                    f"   Load {result.load_number}: {status} {result.option_count} options"
                )

            # Check for the specific pagination pattern
            pattern_detected = self._detect_specific_pattern()

            if pattern_detected:
                print(f"🎯 [PAGINATION_TEST] PAGINATION PATTERN DETECTED!")
                print(f"   - Pattern: Full -> Half -> Half -> Full -> ...")
                return True
            else:
                print(f"✅ [PAGINATION_TEST] No pagination pattern detected")
                return False

        except Exception as e:
            print(f"❌ [PAGINATION_TEST] Error analyzing results: {e}")
            return False

    def _detect_specific_pattern(self) -> bool:
        """Detect the specific pagination pattern described in the issue."""
        try:
            # Get option counts
            counts = [
                result.option_count
                for result in self.load_results
                if not result.error_message
            ]

            if len(counts) < 4:
                return False

            # Expected pattern: high, low, low, high, ...
            # Where "high" is around 36 and "low" is around 18

            # Calculate expected full count (use the maximum as reference)
            full_count = max(counts)
            half_count_threshold = full_count * 0.7  # Allow some variance

            # Check pattern
            for i in range(0, len(counts) - 3, 4):
                # Check 4-load cycle: full, half, half, full
                load1 = counts[i]
                load2 = counts[i + 1] if i + 1 < len(counts) else 0
                load3 = counts[i + 2] if i + 2 < len(counts) else 0
                load4 = counts[i + 3] if i + 3 < len(counts) else 0

                # Check if this matches the pattern
                if (
                    load1 >= half_count_threshold  # Load 1: full
                    and load2 < half_count_threshold  # Load 2: half
                    and load3 < half_count_threshold  # Load 3: half
                    and load4 >= half_count_threshold
                ):  # Load 4: full

                    print(
                        f"🔍 [PAGINATION_TEST] Pattern found in cycle starting at load {i+1}:"
                    )
                    print(f"   Load {i+1}: {load1} (full)")
                    print(f"   Load {i+2}: {load2} (half)")
                    print(f"   Load {i+3}: {load3} (half)")
                    print(f"   Load {i+4}: {load4} (full)")
                    return True

            return False

        except Exception as e:
            print(f"❌ [PAGINATION_TEST] Error detecting pattern: {e}")
            return False

    def cleanup(self) -> None:
        """Clean up test resources."""
        try:
            if self.main_window:
                self.main_window.close()

            if self.app:
                self.app.quit()

        except Exception as e:
            print(f"❌ [PAGINATION_TEST] Cleanup error: {e}")


def main():
    """Run the pagination test."""
    print("🚀 [PAGINATION_TEST] Starting Option Picker Pagination Test")
    print("=" * 60)

    tester = OptionPickerPaginationTester()

    try:
        # Initialize test environment
        if not tester.initialize():
            print("❌ [PAGINATION_TEST] Failed to initialize test environment")
            return False

        # Run the pagination test
        pattern_detected = tester.run_pagination_test(
            position_key="alpha1_alpha1", num_loads=6
        )

        if pattern_detected:
            print("\n🎯 [PAGINATION_TEST] SUCCESS: Pagination issue reproduced!")
            print("   Next step: Add debugging to identify root cause")
        else:
            print("\n✅ [PAGINATION_TEST] No pagination issue detected")
            print("   The issue may be environment-specific or already fixed")

        return pattern_detected

    except Exception as e:
        print(f"❌ [PAGINATION_TEST] Test execution failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        tester.cleanup()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
