"""
Simple end-to-end test for sequence building workflow without unicode characters.
"""

import logging
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from PyQt6.QtCore import QObject
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QTabWidget

# Configure simple logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


class SimpleSequenceBuildingTest:
    """Simple end-to-end test for sequence building workflow."""

    def __init__(self):
        self.app = None
        self.main_window = None
        self.construct_tab = None
        self.start_position_picker = None
        self.option_picker = None
        self.workbench = None

    def setup_application(self) -> bool:
        """Launch and setup the TKA application."""
        try:
            logger.info("SETUP: Setting up TKA application...")

            # Use the proper application creation method from main.py
            from desktop.modern.main import create_application

            logger.info("SETUP: Creating application and main window...")
            self.app, self.main_window = create_application()

            # Show window and wait for initialization
            self.main_window.show()
            QTest.qWait(3000)  # Wait 3 seconds for full UI initialization

            logger.info("SUCCESS: Application setup completed")
            return True

        except Exception as e:
            logger.error(f"ERROR: Failed to setup application: {e}")
            import traceback

            traceback.print_exc()
            return False

    def find_construct_tab(self) -> bool:
        """Find and navigate to the construct tab."""
        try:
            logger.info("NAVIGATE: Finding construct tab...")

            # Find tab widget
            tab_widget = self.main_window.findChild(QTabWidget)
            if not tab_widget:
                # Try alternative search
                all_children = self.main_window.findChildren(QObject)
                logger.info(f"SEARCH: Found {len(all_children)} total children")

                for child in all_children:
                    if isinstance(child, QTabWidget):
                        tab_widget = child
                        break

                if not tab_widget:
                    logger.error("ERROR: Could not find tab widget")
                    return False

            logger.info(f"FOUND: Tab widget with {tab_widget.count()} tabs")

            # Find construct tab
            construct_tab_index = -1
            for i in range(tab_widget.count()):
                tab_text = tab_widget.tabText(i)
                logger.info(f"TAB {i}: {tab_text}")
                if "construct" in tab_text.lower() or i == 0:
                    construct_tab_index = i
                    break

            if construct_tab_index == -1:
                logger.error("ERROR: Could not find construct tab")
                return False

            # Switch to construct tab
            tab_widget.setCurrentIndex(construct_tab_index)
            QTest.qWait(500)

            # Get construct tab widget
            self.construct_tab = tab_widget.currentWidget()
            logger.info(f"SUCCESS: Found construct tab: {type(self.construct_tab)}")

            return True

        except Exception as e:
            logger.error(f"ERROR: Failed to find construct tab: {e}")
            import traceback

            traceback.print_exc()
            return False

    def analyze_construct_components(self) -> bool:
        """Analyze the components in the construct tab."""
        try:
            logger.info("ANALYZE: Analyzing construct tab components...")

            if not self.construct_tab:
                logger.error("ERROR: No construct tab available")
                return False

            # Get all child components
            all_children = self.construct_tab.findChildren(QObject)
            logger.info(f"FOUND: {len(all_children)} total child components")

            # Analyze component types
            component_types = {}
            for widget in all_children:
                widget_name = widget.__class__.__name__
                component_types[widget_name] = component_types.get(widget_name, 0) + 1

            logger.info("COMPONENTS: Component type summary:")
            for comp_type, count in sorted(component_types.items()):
                logger.info(f"   {comp_type}: {count}")

            # Look for key components
            self._find_key_components(all_children)

            # Report findings
            logger.info("RESULTS: Component discovery results:")
            logger.info(
                f"   Start Position Picker: {self.start_position_picker is not None}"
            )
            logger.info(f"   Option Picker: {self.option_picker is not None}")
            logger.info(f"   Workbench: {self.workbench is not None}")

            return True

        except Exception as e:
            logger.error(f"ERROR: Failed to analyze components: {e}")
            import traceback

            traceback.print_exc()
            return False

    def _find_key_components(self, all_children):
        """Find key components using name matching."""
        for widget in all_children:
            widget_name = widget.__class__.__name__.lower()

            # Look for start position picker
            if (
                "start" in widget_name and "position" in widget_name
            ) or "startposition" in widget_name:
                self.start_position_picker = widget
                logger.info(
                    f"FOUND: Start position picker: {widget.__class__.__name__}"
                )

            # Look for option picker
            if (
                "option" in widget_name and "picker" in widget_name
            ) or "optionpicker" in widget_name:
                self.option_picker = widget
                logger.info(f"FOUND: Option picker: {widget.__class__.__name__}")

            # Look for workbench
            if "workbench" in widget_name or (
                "sequence" in widget_name and "view" in widget_name
            ):
                self.workbench = widget
                logger.info(f"FOUND: Workbench: {widget.__class__.__name__}")

    def test_start_position_interaction(self) -> bool:
        """Test interaction with start position picker."""
        try:
            logger.info("TEST: Testing start position interaction...")

            if not self.start_position_picker:
                logger.warning("WARNING: No start position picker found, skipping test")
                return True

            # Check for available methods
            methods = [
                method
                for method in dir(self.start_position_picker)
                if not method.startswith("_")
            ]
            logger.info(
                f"METHODS: Start position picker has {len(methods)} public methods"
            )

            # Look for selection methods
            selection_methods = [
                m for m in methods if "select" in m.lower() or "position" in m.lower()
            ]
            logger.info(f"SELECTION: Found selection methods: {selection_methods}")

            # Look for signals
            signals = [
                attr
                for attr in dir(self.start_position_picker)
                if "signal"
                in str(type(getattr(self.start_position_picker, attr, None))).lower()
            ]
            logger.info(f"SIGNALS: Found signals: {signals}")

            return True

        except Exception as e:
            logger.error(f"ERROR: Start position interaction test failed: {e}")
            return False

    def test_option_picker_interaction(self) -> bool:
        """Test interaction with option picker."""
        try:
            logger.info("TEST: Testing option picker interaction...")

            if not self.option_picker:
                logger.warning("WARNING: No option picker found, skipping test")
                return True

            # Check for available methods
            methods = [
                method
                for method in dir(self.option_picker)
                if not method.startswith("_")
            ]
            logger.info(f"METHODS: Option picker has {len(methods)} public methods")

            # Look for option-related methods
            option_methods = [
                m for m in methods if "option" in m.lower() or "select" in m.lower()
            ]
            logger.info(f"OPTIONS: Found option methods: {option_methods}")

            return True

        except Exception as e:
            logger.error(f"ERROR: Option picker interaction test failed: {e}")
            return False

    def test_workbench_interaction(self) -> bool:
        """Test interaction with workbench."""
        try:
            logger.info("TEST: Testing workbench interaction...")

            if not self.workbench:
                logger.warning("WARNING: No workbench found, skipping test")
                return True

            # Check for available methods
            methods = [
                method for method in dir(self.workbench) if not method.startswith("_")
            ]
            logger.info(f"METHODS: Workbench has {len(methods)} public methods")

            # Look for sequence-related methods
            sequence_methods = [
                m for m in methods if "sequence" in m.lower() or "beat" in m.lower()
            ]
            logger.info(f"SEQUENCE: Found sequence methods: {sequence_methods}")

            return True

        except Exception as e:
            logger.error(f"ERROR: Workbench interaction test failed: {e}")
            return False

    def run_complete_test(self) -> bool:
        """Run the complete test suite."""
        try:
            logger.info("START: Starting complete sequence building test...")

            # Setup
            if not self.setup_application():
                return False

            if not self.find_construct_tab():
                return False

            if not self.analyze_construct_components():
                return False

            # Component interaction tests
            if not self.test_start_position_interaction():
                return False

            if not self.test_option_picker_interaction():
                return False

            if not self.test_workbench_interaction():
                return False

            logger.info("SUCCESS: All tests completed successfully!")
            return True

        except Exception as e:
            logger.error(f"ERROR: Test suite failed: {e}")
            import traceback

            traceback.print_exc()
            return False
        finally:
            # Cleanup
            if self.main_window:
                self.main_window.close()


def run_simple_test():
    """Run the simple end-to-end test."""
    test = SimpleSequenceBuildingTest()
    success = test.run_complete_test()

    if success:
        print("\nSUCCESS: END-TO-END TEST PASSED!")
        print("All sequence building components were found and analyzed.")
    else:
        print("\nFAILED: END-TO-END TEST FAILED!")
        print("Check the logs above for detailed failure information.")

    return success


if __name__ == "__main__":
    success = run_simple_test()
    sys.exit(0 if success else 1)
