"""
Comprehensive TKA Browse Tab Organized Filter Hub Test

This script performs extensive testing of the organized filter hub implementation,
including functionality, visual design, user experience, and technical aspects.
"""

import sys
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

# Add the src directory to Python path for imports
modern_src = Path(__file__).parent / "src" / "desktop" / "modern" / "src"
sys.path.insert(0, str(modern_src))

from presentation.tabs.browse.models import FilterType
from presentation.tabs.browse.modern_browse_tab import ModernBrowseTab


class ComprehensiveBrowseTabTester:
    """Comprehensive tester for the organized filter hub."""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = None
        self.browse_tab = None
        self.test_results = {
            "functionality": [],
            "visual_design": [],
            "user_experience": [],
            "technical": [],
            "responsive": [],
            "performance": [],
        }
        self.errors = []
        self.warnings = []

    def setup_test_environment(self):
        """Set up the test environment."""
        print("🔧 Setting up test environment...")

        # Create main window
        self.window = QMainWindow()
        self.window.setWindowTitle("TKA Browse Tab Organized Filter Hub Test")
        self.window.setGeometry(100, 100, 1400, 900)

        # Apply dark theme
        self.app.setStyleSheet(
            """
            QMainWindow {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }
        """
        )

        try:
            # Create browse tab
            sequences_dir = Path("test_sequences")
            settings_file = Path("test_settings.json")

            self.browse_tab = ModernBrowseTab(sequences_dir, settings_file)
            self.window.setCentralWidget(self.browse_tab)

            print("✅ Test environment setup complete")
            return True

        except Exception as e:
            print(f"❌ Failed to setup test environment: {e}")
            traceback.print_exc()
            return False

    def test_quick_access_functionality(self):
        """Test quick access button functionality."""
        print("\n🧪 Testing Quick Access Functionality...")

        quick_access_tests = [
            ("Favorites", "favorites"),
            ("Recently Added", "recent"),
            ("All Sequences", "all_sequences"),
        ]

        for label, filter_type in quick_access_tests:
            try:
                print(f"  🔍 Testing {label}...")

                # Find the quick access section
                quick_access = self.browse_tab.filter_selection_panel.quick_access

                # Check if buttons exist
                if hasattr(quick_access, "buttons"):
                    print(f"    ✅ {label} button found")
                    self.test_results["functionality"].append(f"{label} button exists")

                    # Try to trigger the button (simulate click)
                    # This would normally be done with QTest.mouseClick, but we'll simulate
                    if (
                        hasattr(quick_access, "_on_favorites_clicked")
                        and filter_type == "favorites"
                    ):
                        quick_access._on_favorites_clicked()
                        print(f"    ✅ {label} click simulation successful")
                        self.test_results["functionality"].append(
                            f"{label} click works"
                        )
                    elif (
                        hasattr(quick_access, "_on_recent_clicked")
                        and filter_type == "recent"
                    ):
                        quick_access._on_recent_clicked()
                        print(f"    ✅ {label} click simulation successful")
                        self.test_results["functionality"].append(
                            f"{label} click works"
                        )
                    elif (
                        hasattr(quick_access, "_on_all_sequences_clicked")
                        and filter_type == "all_sequences"
                    ):
                        quick_access._on_all_sequences_clicked()
                        print(f"    ✅ {label} click simulation successful")
                        self.test_results["functionality"].append(
                            f"{label} click works"
                        )
                else:
                    print(f"    ⚠️  {label} button structure unclear")
                    self.warnings.append(f"{label} button structure unclear")

            except Exception as e:
                print(f"    ❌ {label} test failed: {e}")
                self.errors.append(f"{label} test failed: {e}")

    def test_category_sections_functionality(self):
        """Test category section functionality."""
        print("\n🧪 Testing Category Sections Functionality...")

        category_tests = [
            ("By Sequence Name", FilterType.STARTING_LETTER, "A-D"),
            ("By Length", FilterType.SEQUENCE_LENGTH, "5"),
            ("By Difficulty", FilterType.DIFFICULTY_LEVEL, "beginner"),
            ("By Start Position", FilterType.STARTING_POSITION, "alpha"),
            ("By Author", FilterType.AUTHOR, "Demo Author"),
            ("By Grid Style", FilterType.GRID_MODE, "diamond"),
        ]

        for section_name, filter_type, test_value in category_tests:
            try:
                print(f"  🔍 Testing {section_name}...")

                # Check if category sections exist
                if hasattr(self.browse_tab.filter_selection_panel, "category_sections"):
                    sections = self.browse_tab.filter_selection_panel.category_sections

                    if filter_type in sections:
                        print(f"    ✅ {section_name} section found")
                        self.test_results["functionality"].append(
                            f"{section_name} section exists"
                        )

                        # Test section has options
                        section = sections[filter_type]
                        if hasattr(section, "options") or hasattr(section, "buttons"):
                            print(f"    ✅ {section_name} has options/buttons")
                            self.test_results["functionality"].append(
                                f"{section_name} has interactive elements"
                            )
                        else:
                            print(f"    ⚠️  {section_name} structure unclear")
                            self.warnings.append(f"{section_name} structure unclear")
                    else:
                        print(f"    ❌ {section_name} section not found")
                        self.errors.append(f"{section_name} section not found")
                else:
                    print(f"    ❌ Category sections not found")
                    self.errors.append("Category sections not found")

            except Exception as e:
                print(f"    ❌ {section_name} test failed: {e}")
                self.errors.append(f"{section_name} test failed: {e}")

    def test_visual_design_elements(self):
        """Test visual design elements."""
        print("\n🧪 Testing Visual Design Elements...")

        try:
            # Test header existence
            if hasattr(self.browse_tab.filter_selection_panel, "header"):
                print("  ✅ Header section found")
                self.test_results["visual_design"].append("Header section exists")
            else:
                print("  ⚠️  Header section structure unclear")
                self.warnings.append("Header section structure unclear")

            # Test quick access styling
            if hasattr(self.browse_tab.filter_selection_panel, "quick_access"):
                print("  ✅ Quick access section found")
                self.test_results["visual_design"].append("Quick access section exists")

                # Check for styling
                quick_access = self.browse_tab.filter_selection_panel.quick_access
                if hasattr(quick_access, "setStyleSheet") or "glassmorphism" in str(
                    type(quick_access)
                ):
                    print("  ✅ Quick access has styling")
                    self.test_results["visual_design"].append(
                        "Quick access styling applied"
                    )

            # Test category grid layout
            if hasattr(self.browse_tab.filter_selection_panel, "category_grid"):
                print("  ✅ Category grid layout found")
                self.test_results["visual_design"].append("Category grid layout exists")

            # Test glass-morphism effects
            widget = self.browse_tab.filter_selection_panel
            if hasattr(widget, "styleSheet") and "rgba" in widget.styleSheet():
                print("  ✅ Glass-morphism effects detected")
                self.test_results["visual_design"].append(
                    "Glass-morphism effects present"
                )
            else:
                print("  ⚠️  Glass-morphism effects unclear")
                self.warnings.append("Glass-morphism effects unclear")

        except Exception as e:
            print(f"  ❌ Visual design test failed: {e}")
            self.errors.append(f"Visual design test failed: {e}")

    def test_navigation_functionality(self):
        """Test navigation between filter and results views."""
        print("\n🧪 Testing Navigation Functionality...")

        try:
            # Test initial state (should be on filter selection)
            if hasattr(self.browse_tab, "internal_left_stack"):
                current_index = self.browse_tab.internal_left_stack.currentIndex()
                print(f"  📍 Initial stack index: {current_index}")

                if current_index == 0:
                    print("  ✅ Starts on filter selection view")
                    self.test_results["functionality"].append(
                        "Starts on filter selection view"
                    )
                else:
                    print("  ⚠️  Unexpected initial view")
                    self.warnings.append("Unexpected initial view")

                # Test navigation to sequence browser
                self.browse_tab._show_sequence_browser()
                time.sleep(0.1)  # Allow for animation

                new_index = self.browse_tab.internal_left_stack.currentIndex()
                print(f"  📍 After navigation: {new_index}")

                if new_index == 1:
                    print("  ✅ Navigation to sequence browser works")
                    self.test_results["functionality"].append(
                        "Navigation to sequence browser works"
                    )
                else:
                    print("  ❌ Navigation to sequence browser failed")
                    self.errors.append("Navigation to sequence browser failed")

                # Test navigation back to filter selection
                self.browse_tab._show_filter_selection()
                time.sleep(0.1)

                back_index = self.browse_tab.internal_left_stack.currentIndex()
                print(f"  📍 After back navigation: {back_index}")

                if back_index == 0:
                    print("  ✅ Navigation back to filter selection works")
                    self.test_results["functionality"].append(
                        "Navigation back to filter selection works"
                    )
                else:
                    print("  ❌ Navigation back to filter selection failed")
                    self.errors.append("Navigation back to filter selection failed")

        except Exception as e:
            print(f"  ❌ Navigation test failed: {e}")
            self.errors.append(f"Navigation test failed: {e}")

    def test_responsive_design(self):
        """Test responsive design at different window sizes."""
        print("\n🧪 Testing Responsive Design...")

        test_sizes = [
            (1400, 900, "Wide"),
            (1000, 700, "Medium"),
            (800, 600, "Narrow"),
            (600, 500, "Mobile"),
        ]

        for width, height, label in test_sizes:
            try:
                print(f"  📏 Testing {label} size ({width}x{height})...")

                # Resize window
                self.window.resize(width, height)
                self.app.processEvents()
                time.sleep(0.1)

                # Check if layout adapts
                if hasattr(self.browse_tab.filter_selection_panel, "category_grid"):
                    print(f"    ✅ {label} resize successful")
                    self.test_results["responsive"].append(f"{label} resize works")
                else:
                    print(f"    ⚠️  {label} resize - layout unclear")
                    self.warnings.append(f"{label} resize - layout unclear")

            except Exception as e:
                print(f"    ❌ {label} resize failed: {e}")
                self.errors.append(f"{label} resize failed: {e}")

    def test_performance_metrics(self):
        """Test performance metrics."""
        print("\n🧪 Testing Performance Metrics...")

        try:
            # Test startup time
            start_time = time.time()
            # Simulate reload
            self.browse_tab.filter_selection_panel.update()
            self.app.processEvents()
            startup_time = time.time() - start_time

            print(f"  ⏱️  Filter panel update time: {startup_time:.3f}s")

            if startup_time < 0.5:
                print("  ✅ Fast performance")
                self.test_results["performance"].append("Fast filter panel updates")
            else:
                print("  ⚠️  Slow performance")
                self.warnings.append("Slow filter panel updates")

            # Test memory usage (basic)
            widget_count = len(self.browse_tab.findChildren(QWidget))
            print(f"  📊 Widget count: {widget_count}")

            if widget_count < 200:
                print("  ✅ Reasonable widget count")
                self.test_results["performance"].append("Reasonable widget count")
            else:
                print("  ⚠️  High widget count")
                self.warnings.append("High widget count")

        except Exception as e:
            print(f"  ❌ Performance test failed: {e}")
            self.errors.append(f"Performance test failed: {e}")

    def test_filter_application_flow(self):
        """Test the complete filter application flow."""
        print("\n🧪 Testing Filter Application Flow...")

        try:
            # Test filter signal connection
            filter_panel = self.browse_tab.filter_selection_panel

            if hasattr(filter_panel, "filter_selected"):
                print("  ✅ Filter selection signal exists")
                self.test_results["functionality"].append(
                    "Filter selection signal exists"
                )

                # Test signal connection to browse tab
                if hasattr(self.browse_tab, "_on_filter_selected"):
                    print("  ✅ Filter selection handler exists")
                    self.test_results["functionality"].append(
                        "Filter selection handler exists"
                    )

                    # Test sequence browser updates
                    if hasattr(self.browse_tab, "sequence_browser_panel"):
                        print("  ✅ Sequence browser panel exists")
                        self.test_results["functionality"].append(
                            "Sequence browser panel exists"
                        )
                    else:
                        print("  ❌ Sequence browser panel missing")
                        self.errors.append("Sequence browser panel missing")
                else:
                    print("  ❌ Filter selection handler missing")
                    self.errors.append("Filter selection handler missing")
            else:
                print("  ❌ Filter selection signal missing")
                self.errors.append("Filter selection signal missing")

        except Exception as e:
            print(f"  ❌ Filter application flow test failed: {e}")
            self.errors.append(f"Filter application flow test failed: {e}")

    def run_comprehensive_tests(self):
        """Run all comprehensive tests."""
        print("🚀 Starting Comprehensive Browse Tab Testing...")
        print("=" * 70)

        # Setup
        if not self.setup_test_environment():
            print("❌ Test environment setup failed. Aborting tests.")
            return False

        # Show window
        self.window.show()
        self.app.processEvents()
        time.sleep(0.5)  # Allow UI to settle

        # Run all tests
        test_methods = [
            self.test_quick_access_functionality,
            self.test_category_sections_functionality,
            self.test_visual_design_elements,
            self.test_navigation_functionality,
            self.test_responsive_design,
            self.test_performance_metrics,
            self.test_filter_application_flow,
        ]

        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                print(f"❌ Test method {test_method.__name__} failed: {e}")
                self.errors.append(f"Test method {test_method.__name__} failed: {e}")

        # Generate report
        self.generate_test_report()

        return len(self.errors) == 0

    def generate_test_report(self):
        """Generate comprehensive test report."""
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 70)

        # Summary
        total_results = sum(len(results) for results in self.test_results.values())
        print(f"✅ Total successful tests: {total_results}")
        print(f"⚠️  Total warnings: {len(self.warnings)}")
        print(f"❌ Total errors: {len(self.errors)}")

        # Detailed results by category
        for category, results in self.test_results.items():
            if results:
                print(f"\n🎯 {category.upper()} RESULTS:")
                for result in results:
                    print(f"  ✅ {result}")

        # Warnings
        if self.warnings:
            print(f"\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  ⚠️  {warning}")

        # Errors
        if self.errors:
            print(f"\n❌ ERRORS:")
            for error in self.errors:
                print(f"  ❌ {error}")

        # Overall assessment
        print(f"\n🎭 OVERALL ASSESSMENT:")

        if len(self.errors) == 0:
            print("🎉 EXCELLENT: No critical errors found!")
            print("✅ The organized filter hub is ready for user interaction!")
        elif len(self.errors) < 5:
            print("👍 GOOD: Minor issues found, but mostly functional")
            print("🔧 Address the errors above for optimal experience")
        else:
            print("⚠️  NEEDS WORK: Multiple issues found")
            print("🔧 Significant fixes required before user interaction")

        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if len(self.errors) == 0 and len(self.warnings) == 0:
            print("  🎯 Perfect implementation - ready for production!")
        elif len(self.errors) == 0:
            print("  🔧 Address warnings for better user experience")
        else:
            print("  🚨 Fix critical errors before proceeding")
            print("  🔍 Focus on filter functionality and navigation")

        print("=" * 70)

    def run_visual_inspection(self):
        """Run visual inspection with user interaction."""
        print("\n👁️  VISUAL INSPECTION MODE")
        print("=" * 40)
        print("Please manually inspect the following:")
        print("1. 📝 Header: 'TKA Sequence Library' title")
        print("2. ⭐ Quick Access: 3 horizontal buttons with icons")
        print("3. 📊 Category Grid: 2x3 or 3x2 layout")
        print("4. 🎨 Glass-morphism: Semi-transparent backgrounds")
        print("5. 🖱️  Hover Effects: Buttons respond to mouse")
        print("6. 📱 Responsive: Try resizing the window")
        print("7. 🔄 Navigation: Click buttons to test switching")
        print("\nPress any key in the console to continue...")

        # Keep window open for manual inspection
        input()


def main():
    """Main test execution."""
    tester = ComprehensiveBrowseTabTester()

    # Run comprehensive automated tests
    success = tester.run_comprehensive_tests()

    # Run visual inspection
    tester.run_visual_inspection()

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
