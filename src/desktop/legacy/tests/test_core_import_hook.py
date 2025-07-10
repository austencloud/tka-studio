"""
Regression test for core import hook functionality.

Tests that 'from core.*' imports work correctly from any location
in the legacy application without requiring manual path setup.
"""

import os
import sys
import unittest
from importlib import reload
from pathlib import Path

# Add the legacy directory to the path for testing
legacy_path = Path(__file__).parent.parent
sys.path.insert(0, str(legacy_path))


class TestCoreImportHook(unittest.TestCase):
    """Test the core import hook functionality."""

    def setUp(self):
        """Set up test environment."""
        # Ensure the hook is installed
        try:
            from core_import_hook import install_core_import_hook

            install_core_import_hook()
        except ImportError:
            self.skipTest("Core import hook not available")

    def test_glassmorphism_styler_import(self):
        """Test that glassmorphism_styler can be imported via core."""
        try:
            from core.glassmorphism_styler import GlassmorphismStyler

            self.assertIsNotNone(GlassmorphismStyler)
            print(
                "✅ Successfully imported GlassmorphismStyler via 'from core.glassmorphism_styler'"
            )
        except ImportError as e:
            self.fail(f"Failed to import glassmorphism_styler via core: {e}")

    def test_import_from_different_locations(self):
        """Test that core imports work from different file locations."""
        # Save original working directory
        original_cwd = os.getcwd()

        try:
            # Test from various subdirectories
            test_locations = [
                legacy_path / "src" / "main_window",
                legacy_path / "src" / "main_window" / "main_widget",
                legacy_path
                / "src"
                / "main_window"
                / "main_widget"
                / "settings_dialog"
                / "ui"
                / "prop_type",
            ]

            for location in test_locations:
                if location.exists():
                    os.chdir(location)
                    try:
                        # Clear module cache to force re-import
                        if "core.glassmorphism_styler" in sys.modules:
                            del sys.modules["core.glassmorphism_styler"]

                        from core.glassmorphism_styler import GlassmorphismStyler

                        self.assertIsNotNone(GlassmorphismStyler)
                        print(f"✅ Successfully imported from {location}")
                    except ImportError as e:
                        self.fail(f"Failed to import from {location}: {e}")

        finally:
            # Restore original working directory
            os.chdir(original_cwd)

    def test_prop_button_functionality(self):
        """Test that the actual prop_button file can import and function."""
        try:
            # Add the src directory to path
            src_path = legacy_path / "src"
            if str(src_path) not in sys.path:
                sys.path.insert(0, str(src_path))

            # Try to import the prop_button module
            from main_window.main_widget.settings_dialog.ui.prop_type.prop_button import (
                PropButton,
            )

            self.assertIsNotNone(PropButton)
            print(
                "✅ Successfully imported PropButton (which depends on core.glassmorphism_styler)"
            )

        except ImportError as e:
            self.fail(f"Failed to import PropButton: {e}")

    def test_hook_installation(self):
        """Test that the hook is properly installed in the import system."""
        from core_import_hook import CoreImportFinder

        # Check if our finder is in the meta_path
        finder_installed = any(
            isinstance(finder, CoreImportFinder) for finder in sys.meta_path
        )
        self.assertTrue(
            finder_installed, "CoreImportFinder should be installed in sys.meta_path"
        )
        print("✅ Core import hook is properly installed in import system")

    def test_hook_finds_correct_core(self):
        """Test that the hook finds the correct core directory."""
        from core_import_hook import CoreImportFinder

        finder = CoreImportFinder()
        core_dirs = finder.core_directories

        # Should find at least one core directory
        self.assertGreater(len(core_dirs), 0, "Should find at least one core directory")

        # Should find the settings_dialog core directory specifically
        settings_core = any(
            "settings_dialog" in str(core_dir) for core_dir in core_dirs
        )
        self.assertTrue(settings_core, "Should find settings_dialog core directory")
        print(
            f"✅ Found {len(core_dirs)} core directories including settings_dialog/core"
        )


def run_core_import_regression_test():
    """Run the regression test and return results."""
    print("🧪 Running Core Import Hook Regression Test")
    print("=" * 50)

    try:
        # Create test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(TestCoreImportHook)

        # Run tests with detailed output
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        # Summary
        print("\n" + "=" * 50)
        if result.wasSuccessful():
            print("🎉 ALL TESTS PASSED - Core import hook working correctly!")
            print(f"✅ Ran {result.testsRun} tests successfully")
            return True
        else:
            print("❌ SOME TESTS FAILED")
            print(f"❌ Failures: {len(result.failures)}")
            print(f"❌ Errors: {len(result.errors)}")
            return False

    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_core_import_regression_test()
    sys.exit(0 if success else 1)
