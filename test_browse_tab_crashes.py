"""
Browse Tab Crash Detector

Script to identify and fix crashes in the Modern Browse Tab.
This will help us find the exact issues causing crashes during user interaction.
"""

import sys
import traceback
from pathlib import Path

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

# Add src to path
sys.path.append(str(Path(__file__).parent / "src" / "desktop" / "modern" / "src"))

from presentation.tabs.browse.models import FilterType
from presentation.tabs.browse.modern_browse_tab import ModernBrowseTab


class BrowseTabCrashDetector:
    """Detect and report crashes in browse tab interactions."""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.temp_dir = Path(__file__).parent.parent / "temp"
        self.temp_dir.mkdir(exist_ok=True)

        # Create temporary files
        self.sequences_dir = self.temp_dir / "sequences"
        self.sequences_dir.mkdir(exist_ok=True)

        self.settings_file = self.temp_dir / "settings.json"
        self.settings_file.write_text('{"filter_type": null, "filter_value": null}')

        self.browse_tab = None
        self.crash_count = 0

    def test_initialization(self):
        """Test browse tab initialization."""
        print("🧪 Testing browse tab initialization...")
        try:
            self.browse_tab = ModernBrowseTab(self.sequences_dir, self.settings_file)
            print("✅ Browse tab initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Crash during initialization: {e}")
            traceback.print_exc()
            self.crash_count += 1
            return False

    def test_filter_button_clicks(self):
        """Test clicking all filter buttons."""
        if not self.browse_tab:
            return False

        print("🧪 Testing filter button clicks...")

        filter_types = [
            FilterType.ALL_SEQUENCES,
            FilterType.STARTING_LETTER,
            FilterType.CONTAINS_LETTERS,
            FilterType.SEQUENCE_LENGTH,
            FilterType.DIFFICULTY_LEVEL,
            FilterType.STARTING_POSITION,
            FilterType.AUTHOR,
            FilterType.FAVORITES,
            FilterType.MOST_RECENT,
            FilterType.GRID_MODE,
        ]

        for filter_type in filter_types:
            try:
                print(f"  🔍 Testing {filter_type.value}...")
                self.browse_tab.filter_selection_panel._on_filter_button_clicked(
                    filter_type
                )
                print(f"  ✅ {filter_type.value} clicked successfully")
            except Exception as e:
                print(f"  ❌ Crash when clicking {filter_type.value}: {e}")
                traceback.print_exc()
                self.crash_count += 1

        return self.crash_count == 0

    def test_navigation_switching(self):
        """Test navigation stack switching."""
        if not self.browse_tab:
            return False

        print("🧪 Testing navigation switching...")

        try:
            # Test switching to sequence browser
            print("  🔄 Switching to sequence browser...")
            self.browse_tab._show_sequence_browser()
            print("  ✅ Switched to sequence browser")

            # Test switching back to filter selection
            print("  🔄 Switching back to filter selection...")
            self.browse_tab._show_filter_selection()
            print("  ✅ Switched back to filter selection")

            return True
        except Exception as e:
            print(f"  ❌ Crash during navigation switching: {e}")
            traceback.print_exc()
            self.crash_count += 1
            return False

    def test_filter_service_operations(self):
        """Test browse service operations."""
        if not self.browse_tab:
            return False

        print("🧪 Testing browse service operations...")

        try:
            # Test loading sequences
            print("  📚 Loading sequences...")
            sequences = self.browse_tab.browse_service.load_sequences()
            print(f"  ✅ Loaded {len(sequences)} sequences")

            # Test applying filters
            filter_types = [FilterType.ALL_SEQUENCES, FilterType.STARTING_LETTER]
            for filter_type in filter_types:
                print(f"  🔍 Testing filter: {filter_type.value}...")
                filtered = self.browse_tab.browse_service.apply_filter(
                    filter_type, None
                )
                print(
                    f"  ✅ Filter {filter_type.value} returned {len(filtered)} sequences"
                )

            return True
        except Exception as e:
            print(f"  ❌ Crash during service operations: {e}")
            traceback.print_exc()
            self.crash_count += 1
            return False

    def test_ui_components(self):
        """Test UI component operations."""
        if not self.browse_tab:
            return False

        print("🧪 Testing UI components...")

        try:
            # Test filter selection panel
            print("  🎛️ Testing filter selection panel...")
            filter_panel = self.browse_tab.filter_selection_panel
            assert filter_panel is not None
            print("  ✅ Filter selection panel OK")

            # Test sequence browser panel
            print("  🖥️ Testing sequence browser panel...")
            browser_panel = self.browse_tab.sequence_browser_panel
            assert browser_panel is not None
            print("  ✅ Sequence browser panel OK")

            # Test sequence viewer panel
            print("  👁️ Testing sequence viewer panel...")
            viewer_panel = self.browse_tab.sequence_viewer_panel
            assert viewer_panel is not None
            print("  ✅ Sequence viewer panel OK")

            return True
        except Exception as e:
            print(f"  ❌ Crash during UI component testing: {e}")
            traceback.print_exc()
            self.crash_count += 1
            return False

    def test_resize_handling(self):
        """Test resize event handling."""
        if not self.browse_tab:
            return False

        print("🧪 Testing resize handling...")

        try:
            # Test different window sizes
            test_sizes = [(800, 600), (1200, 800), (400, 300)]

            for width, height in test_sizes:
                print(f"  📏 Testing resize to {width}x{height}...")
                self.browse_tab.resize(width, height)
                self.browse_tab.filter_selection_panel.resize(width // 2, height)
                print(f"  ✅ Resize to {width}x{height} OK")

            return True
        except Exception as e:
            print(f"  ❌ Crash during resize handling: {e}")
            traceback.print_exc()
            self.crash_count += 1
            return False

    def run_all_tests(self):
        """Run all crash detection tests."""
        print("🚀 Starting Browse Tab Crash Detection...")
        print("=" * 50)

        # Run all tests
        tests = [
            self.test_initialization,
            self.test_ui_components,
            self.test_filter_service_operations,
            self.test_filter_button_clicks,
            self.test_navigation_switching,
            self.test_resize_handling,
        ]

        passed = 0
        total = len(tests)

        for test in tests:
            if test():
                passed += 1
            print()

        print("=" * 50)
        print(f"🏁 Tests completed: {passed}/{total} passed")
        print(f"💥 Total crashes detected: {self.crash_count}")

        if self.crash_count == 0:
            print("🎉 No crashes detected! Browse tab is stable.")
        else:
            print("⚠️  Crashes detected. Browse tab needs fixes.")

        return self.crash_count == 0


if __name__ == "__main__":
    detector = BrowseTabCrashDetector()
    success = detector.run_all_tests()

    if success:
        print("\n🎯 Browse tab is ready for user interaction!")
    else:
        print("\n🔧 Browse tab needs fixes before user interaction.")

    sys.exit(0 if success else 1)
