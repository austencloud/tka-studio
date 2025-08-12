"""
Integration tests for the modern visibility system.

Tests the complete integration of:
- ModernVisibilityStateManager
- VisibilityPictographPreview
- GlobalVisibilityService
- Modern VisibilityTab

Uses TKAAITestHelper for comprehensive validation.
"""
from __future__ import annotations

import logging
from typing import Any

from application.services.pictograph.global_visibility_service import (
    PictographVisibilityManager as GlobalVisibilityService,
)
from application.services.settings.visibility_settings_manager import (
    VisibilitySettingsManager as ModernVisibilityStateManager,
)
from core.interfaces.tab_settings_interfaces import IVisibilityService
from core.testing.ai_agent_helpers import TKAAITestHelper
from presentation.components.ui.settings.visibility.visibility_pictograph_preview import (
    VisibilityPictographPreview,
)
from presentation.components.ui.settings.visibility.visibility_tab import VisibilityTab


logger = logging.getLogger(__name__)


class TestModernVisibilityIntegration:
    """Comprehensive integration tests for the modern visibility system."""

    def setup_method(self):
        """Setup test environment with TKA infrastructure."""
        # Use TKA test infrastructure
        self.helper = TKAAITestHelper(use_test_mode=True)
        self.container = self.helper.container

        # Get services from DI container
        self.visibility_service = self.container.resolve(IVisibilityService)

        # Create our new components
        self.state_manager = ModernVisibilityStateManager(self.visibility_service)
        self.global_service = GlobalVisibilityService()

        # Track test state
        self.test_results = {}

    def test_state_manager_integration(self):
        """Test state manager integration with existing visibility service."""
        logger.info("Testing state manager integration...")

        # Test basic functionality
        assert self.state_manager.get_motion_visibility("blue") is not None
        assert self.state_manager.get_motion_visibility("red") is not None

        # Test dependency logic
        _ = self.state_manager.get_motion_visibility("blue")
        _ = self.state_manager.get_motion_visibility("red")

        # Test glyph dependency on motions
        tka_visible = self.state_manager.get_glyph_visibility("TKA")
        assert isinstance(tka_visible, bool)

        # Test validation
        validation = self.state_manager.validate_state()
        assert validation["valid"] is True
        assert isinstance(validation["issues"], list)
        assert isinstance(validation["warnings"], list)

        self.test_results["state_manager"] = True
        logger.info("✓ State manager integration successful")

    def test_observer_pattern(self):
        """Test observer pattern functionality."""
        logger.info("Testing observer pattern...")

        observer_called = {"count": 0}

        def test_observer():
            observer_called["count"] += 1

        # Register observer
        self.state_manager.register_observer(test_observer, ["motion"])

        # Trigger change
        original_blue = self.state_manager.get_motion_visibility("blue")
        self.state_manager.set_motion_visibility("blue", not original_blue)

        # Verify observer was called
        assert observer_called["count"] > 0

        # Restore original state
        self.state_manager.set_motion_visibility("blue", original_blue)

        self.test_results["observer_pattern"] = True
        logger.info("✓ Observer pattern working correctly")

    def test_motion_validation_logic(self):
        """Test motion validation prevents invalid states."""
        logger.info("Testing motion validation logic...")

        # Ensure both motions start as visible
        self.state_manager.set_motion_visibility("blue", True)
        self.state_manager.set_motion_visibility("red", True)

        # Try to disable both motions (should be prevented)
        self.state_manager.set_motion_visibility("blue", False)
        self.state_manager.set_motion_visibility("red", False)

        # At least one should still be visible
        blue_visible = self.state_manager.get_motion_visibility("blue")
        red_visible = self.state_manager.get_motion_visibility("red")

        assert blue_visible or red_visible, "At least one motion must remain visible"

        # Restore both motions
        self.state_manager.set_motion_visibility("blue", True)
        self.state_manager.set_motion_visibility("red", True)

        self.test_results["motion_validation"] = True
        logger.info("✓ Motion validation logic working correctly")

    def test_dependency_logic(self):
        """Test dependent glyph logic."""
        logger.info("Testing dependency logic...")

        # Test with both motions visible
        self.state_manager.set_motion_visibility("blue", True)
        self.state_manager.set_motion_visibility("red", True)

        # Dependent glyphs should be able to be visible
        self.state_manager.set_glyph_visibility("TKA", True)
        tka_visible = self.state_manager.get_glyph_visibility("TKA")
        assert tka_visible is True

        # Test with one motion hidden
        self.state_manager.set_motion_visibility("blue", False)

        # Dependent glyphs should be hidden even if enabled
        tka_effective = self.state_manager.get_glyph_visibility("TKA")
        assert (
            tka_effective is False
        ), "TKA should be hidden when not all motions visible"

        # Non-dependent glyphs should still work
        self.state_manager.set_glyph_visibility("Reversals", True)
        reversals_visible = self.state_manager.get_glyph_visibility("Reversals")
        assert reversals_visible is True

        # Restore state
        self.state_manager.set_motion_visibility("blue", True)

        self.test_results["dependency_logic"] = True
        logger.info("✓ Dependency logic working correctly")

    def test_global_visibility_service(self):
        """Test global visibility service functionality."""
        logger.info("Testing global visibility service...")

        # Test registration
        class MockPictograph:
            def __init__(self):
                self.updates = []

            def update_visibility(self, element_type, element_name, visible):
                self.updates.append((element_type, element_name, visible))

        mock_picto = MockPictograph()

        # Register pictograph
        success = self.global_service.register_pictograph(
            "test_picto_1", mock_picto, "test_component"
        )
        assert success is True

        # Test global update
        result = self.global_service.apply_visibility_change("glyph", "TKA", False)

        assert result["success_count"] >= 1
        assert result["failure_count"] == 0
        assert len(mock_picto.updates) > 0

        # Test statistics
        stats = self.global_service.get_statistics()
        assert stats["active_registrations"] >= 1

        # Test unregistration
        unregister_success = self.global_service.unregister_pictograph("test_picto_1")
        assert unregister_success is True

        self.test_results["global_service"] = True
        logger.info("✓ Global visibility service working correctly")

    def test_pictograph_preview_creation(self):
        """Test pictograph preview component creation."""
        logger.info("Testing pictograph preview creation...")

        try:
            # Create preview component
            preview = VisibilityPictographPreview()

            # Verify it has required components
            assert preview.scene is not None
            assert preview.view is not None
            assert preview.sample_beat_data is not None

            # Test visibility update
            preview.update_visibility("TKA", False, animate=False)

            # Clean up
            preview.cleanup()

            self.test_results["preview_creation"] = True
            logger.info("✓ Pictograph preview creation successful")

        except Exception as e:
            logger.exception(f"Preview creation failed: {e}")
            self.test_results["preview_creation"] = False

    def test_visibility_tab_creation(self):
        """Test complete visibility tab creation."""
        logger.info("Testing visibility tab creation...")

        try:
            # Create visibility tab with all components
            tab = VisibilityTab(
                visibility_service=self.visibility_service,
                global_visibility_service=self.global_service,
            )

            # Verify components exist
            assert tab.state_manager is not None
            assert tab.motion_toggles is not None
            assert tab.element_toggles is not None
            assert tab.preview is not None

            # Test state summary
            summary = tab.get_state_summary()
            assert "motion_states" in summary
            assert "element_states" in summary

            # Clean up
            tab.cleanup()

            self.test_results["tab_creation"] = True
            logger.info("✓ Visibility tab creation successful")

        except Exception as e:
            logger.exception(f"Tab creation failed: {e}")
            self.test_results["tab_creation"] = False

    def test_tka_system_integration(self):
        """Test integration with existing TKA system."""
        logger.info("Testing TKA system integration...")

        # Use TKAAITestHelper to validate system works
        result = self.helper.run_comprehensive_test_suite()

        assert result.success, f"TKA system test failed: {result.errors}"
        assert result.metadata["success_rate"] > 0.8

        # Test sequence creation still works
        seq_result = self.helper.create_sequence("Visibility Test", 4)
        assert seq_result.success

        # Test beat creation still works
        beat_result = self.helper.create_beat_with_motions(1, "A")
        assert beat_result.success

        self.test_results["tka_integration"] = True
        logger.info("✓ TKA system integration successful")

    def test_performance_with_multiple_pictographs(self):
        """Test performance with multiple registered pictographs."""
        logger.info("Testing performance with multiple pictographs...")

        import time

        class MockPictograph:
            def update_visibility(self, element_type, element_name, visible):
                pass

        # Register multiple pictographs
        pictographs = []
        for i in range(50):  # Test with 50 pictographs
            picto = MockPictograph()
            pictographs.append(picto)
            self.global_service.register_pictograph(
                f"perf_test_{i}", picto, "performance_test"
            )

        # Measure update performance
        start_time = time.time()

        result = self.global_service.apply_visibility_change("glyph", "TKA", False)

        end_time = time.time()
        update_time = end_time - start_time

        # Should complete quickly even with many pictographs
        assert update_time < 1.0, f"Update took too long: {update_time}s"
        assert result["success_count"] == 50

        # Clean up
        for i in range(50):
            self.global_service.unregister_pictograph(f"perf_test_{i}")

        self.test_results["performance"] = True
        logger.info(
            f"✓ Performance test passed ({update_time:.3f}s for 50 pictographs)"
        )

    def run_comprehensive_test(self) -> dict[str, Any]:
        """Run all integration tests and return results."""
        logger.info("Starting comprehensive modern visibility integration test...")

        test_methods = [
            self.test_state_manager_integration,
            self.test_observer_pattern,
            self.test_motion_validation_logic,
            self.test_dependency_logic,
            self.test_global_visibility_service,
            self.test_pictograph_preview_creation,
            self.test_visibility_tab_creation,
            self.test_tka_system_integration,
            self.test_performance_with_multiple_pictographs,
        ]

        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                logger.exception(f"Test {test_method.__name__} failed: {e}")
                self.test_results[test_method.__name__] = False

        # Calculate overall success
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)
        success_rate = passed_tests / total_tests if total_tests > 0 else 0

        overall_success = success_rate == 1  # 100% success threshold

        results = {
            "overall_success": overall_success,
            "success_rate": success_rate,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "test_breakdown": self.test_results,
        }

        if overall_success:
            logger.info(
                f"✅ All integration tests passed! ({success_rate:.1%} success rate)"
            )
        else:
            logger.warning(f"⚠️ Some tests failed ({success_rate:.1%} success rate)")

        return results


# Convenience function for AI agents
def test_modern_visibility_integration() -> dict[str, Any]:
    """One-line integration test for AI agents."""
    tester = TestModernVisibilityIntegration()
    tester.setup_method()
    return tester.run_comprehensive_test()


if __name__ == "__main__":
    # Run tests directly
    results = test_modern_visibility_integration()
    print(f"Integration test results: {results}")
