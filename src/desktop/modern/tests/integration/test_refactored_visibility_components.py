#!/usr/bin/env python3
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Validate refactored visibility components maintain all functionality
PERMANENT: Ensure component decomposition preserves architectural contracts
AUTHOR: @ai-agent
"""

import logging
import time
from typing import Any, Dict, Optional

import pytest
from application.services.pictograph.global_visibility_service import (
    PictographVisibilityManager as GlobalVisibilityService,
)
from application.services.pictograph.visibility_state_manager import (
    VisibilityStateManager as ModernVisibilityStateManager,
)
from core.application.application_factory import ApplicationFactory
from core.interfaces.tab_settings_interfaces import IVisibilityService
from core.testing.ai_agent_helpers import TKAAITestHelper
from presentation.components.ui.settings.components import ElementToggle, MotionToggle
from presentation.components.ui.settings.visibility.components import (
    DependencyWarning,
    ElementVisibilitySection,
    MotionControlsSection,
    VisibilityPreviewSection,
)

# Import refactored components
from presentation.components.ui.settings.visibility.visibility_tab import VisibilityTab

logger = logging.getLogger(__name__)


@pytest.mark.specification
@pytest.mark.critical
class TestRefactoredVisibilityComponents:
    """
    PERMANENT specification tests for refactored visibility components.

    Validates that component decomposition maintains all existing functionality
    while improving architectural organization and following TKA patterns.
    """

    def setup_method(self):
        """Setup test environment with TKA infrastructure."""
        # Use TKA test infrastructure
        self.helper = TKAAITestHelper(use_test_mode=True)
        self.container = self.helper.container

        # Get services from DI container
        self.visibility_service = self.container.resolve(IVisibilityService)

        # Create services
        self.state_manager = ModernVisibilityStateManager(self.visibility_service)
        self.global_service = GlobalVisibilityService()

        # Track test results
        self.test_results = {}

        logger.info("Test environment setup complete")

    def test_motion_toggle_component_contract(self):
        """PERMANENT: MotionToggle must maintain color coding and state management."""
        # Test blue motion toggle
        blue_toggle = MotionToggle("blue")
        assert blue_toggle.get_color() == "blue"
        assert blue_toggle.get_is_active() is True  # Default active
        assert blue_toggle.text() == "Blue Motion"

        # Test red motion toggle
        red_toggle = MotionToggle("red")
        assert red_toggle.get_color() == "red"
        assert red_toggle.get_is_active() is True
        assert red_toggle.text() == "Red Motion"

        # Test state changes
        blue_toggle.set_active(False)
        assert blue_toggle.get_is_active() is False
        assert blue_toggle.isChecked() is False

        self.test_results["motion_toggle_contract"] = True
        logger.info("✓ MotionToggle component contract validated")

    def test_element_toggle_component_contract(self):
        """PERMANENT: ElementToggle must maintain dependency awareness."""
        # Test independent element
        independent_toggle = ElementToggle("Reversals", "Show reversal indicators")
        assert independent_toggle.get_is_dependent() is False
        assert independent_toggle.isEnabled() is True

        # Test dependent element
        dependent_toggle = ElementToggle("TKA", "Show TKA symbols")
        dependent_toggle.set_dependent(True)
        assert dependent_toggle.get_is_dependent() is True

        # Test motion dependency
        dependent_toggle.set_motions_visible(False)
        assert dependent_toggle.isEnabled() is False

        dependent_toggle.set_motions_visible(True)
        assert dependent_toggle.isEnabled() is True

        self.test_results["element_toggle_contract"] = True
        logger.info("✓ ElementToggle component contract validated")

    def test_motion_controls_section_contract(self):
        """PERMANENT: MotionControlsSection must coordinate motion toggles."""
        section = MotionControlsSection(self.visibility_service, self.state_manager)

        # Verify component creation
        assert section.motion_toggles is not None
        assert len(section.motion_toggles) == 2
        assert "blue" in section.motion_toggles
        assert "red" in section.motion_toggles

        # Test state retrieval
        motion_states = section.get_motion_states()
        assert isinstance(motion_states, dict)
        assert "blue" in motion_states
        assert "red" in motion_states

        # Test signal emission (mock test)
        signal_emitted = False

        def mock_handler(color, visible):
            nonlocal signal_emitted
            signal_emitted = True

        section.motion_visibility_changed.connect(mock_handler)
        section._on_motion_visibility_changed("blue", False)
        assert signal_emitted is True

        self.test_results["motion_controls_contract"] = True
        logger.info("✓ MotionControlsSection contract validated")

    def test_element_visibility_section_contract(self):
        """PERMANENT: ElementVisibilitySection must manage element dependencies."""
        section = ElementVisibilitySection(self.visibility_service, self.state_manager)

        # Verify component creation
        assert section.element_toggles is not None
        assert len(section.element_toggles) > 0

        # Test expected elements
        expected_elements = [
            "TKA",
            "Reversals",
            "VTG",
            "Elemental",
            "Positions",
            "Non-radial_points",
        ]
        for element in expected_elements:
            assert element in section.element_toggles

        # Test dependency management
        dependent_elements = section.get_dependent_elements()
        assert isinstance(dependent_elements, dict)
        assert dependent_elements["TKA"] is True  # TKA should be dependent
        assert (
            dependent_elements["Reversals"] is False
        )  # Reversals should be independent

        # Test motion dependency update
        section.update_motion_dependency(False)
        tka_toggle = section.element_toggles["TKA"]
        assert tka_toggle.isEnabled() is False

        section.update_motion_dependency(True)
        assert tka_toggle.isEnabled() is True

        self.test_results["element_visibility_contract"] = True
        logger.info("✓ ElementVisibilitySection contract validated")

    def test_visibility_preview_section_contract(self):
        """PERMANENT: VisibilityPreviewSection must manage preview updates."""
        section = VisibilityPreviewSection()

        # Verify component creation
        assert section.preview is not None
        preview_widget = section.get_preview_widget()
        assert preview_widget is not None

        # Test signal emission
        signal_emitted = False

        def mock_handler():
            nonlocal signal_emitted
            signal_emitted = True

        section.preview_updated.connect(mock_handler)
        section._on_preview_updated()
        assert signal_emitted is True

        # Test cleanup
        section.cleanup()

        self.test_results["preview_section_contract"] = True
        logger.info("✓ VisibilityPreviewSection contract validated")

    def test_dependency_warning_contract(self):
        """PERMANENT: DependencyWarning must show/hide based on motion state."""
        warning = DependencyWarning()

        # Initially hidden
        assert warning.isVisible() is False

        # Test visibility control
        warning.set_visible(True)
        assert warning.isVisible() is True

        warning.set_visible(False)
        assert warning.isVisible() is False

        # Test motion state update
        warning.update_warning_state(False)  # Not all motions visible
        assert warning.isVisible() is True

        warning.update_warning_state(True)  # All motions visible
        assert warning.isVisible() is False

        self.test_results["dependency_warning_contract"] = True
        logger.info("✓ DependencyWarning contract validated")

    def test_main_visibility_tab_coordinator_contract(self):
        """PERMANENT: Main VisibilityTab must coordinate all components."""
        tab = VisibilityTab(
            visibility_service=self.visibility_service,
            global_visibility_service=self.global_service,
        )

        # Verify component coordination
        assert tab.motion_section is not None
        assert tab.element_section is not None
        assert tab.preview_section is not None
        assert tab.dependency_warning is not None

        # Test state summary
        summary = tab.get_state_summary()
        assert isinstance(summary, dict)
        assert "motion_states" in summary
        assert "element_states" in summary
        assert "dependency_warning_visible" in summary
        assert "state_manager_validation" in summary

        # Test signal coordination
        signal_emitted = False

        def mock_handler(element_type, visible):
            nonlocal signal_emitted
            signal_emitted = True

        tab.visibility_changed.connect(mock_handler)
        tab._on_motion_visibility_changed("blue", False)
        assert signal_emitted is True

        # Test cleanup
        tab.cleanup()

        self.test_results["main_tab_coordinator_contract"] = True
        logger.info("✓ Main VisibilityTab coordinator contract validated")

    def test_tka_system_integration_preserved(self):
        """PERMANENT: Refactored components must preserve TKA system integration."""
        # Use TKAAITestHelper to validate system still works
        result = self.helper.run_comprehensive_test_suite()

        assert result.success, f"TKA system test failed: {result.errors}"
        assert result.metadata["success_rate"] > 0.8

        # Test sequence creation still works
        seq_result = self.helper.create_sequence("Refactored Visibility Test", 4)
        assert seq_result.success

        # Test beat creation still works
        beat_result = self.helper.create_beat_with_motions(1, "A")
        assert beat_result.success

        # Test pictograph operations still work
        picto_result = self.helper.test_pictograph_from_beat()
        assert picto_result.success

        self.test_results["tka_integration_preserved"] = True
        logger.info("✓ TKA system integration preserved after refactoring")

    def test_architectural_compliance(self):
        """PERMANENT: Components must follow TKA architectural patterns."""
        # Test dependency injection usage
        tab = VisibilityTab(
            visibility_service=self.visibility_service,
            global_visibility_service=self.global_service,
        )

        # Verify services are injected, not instantiated directly
        assert tab.visibility_service is self.visibility_service
        assert tab.global_visibility_service is self.global_service
        assert tab.state_manager is not None

        # Verify component composition
        assert isinstance(tab.motion_section, MotionControlsSection)
        assert isinstance(tab.element_section, ElementVisibilitySection)
        assert isinstance(tab.preview_section, VisibilityPreviewSection)
        assert isinstance(tab.dependency_warning, DependencyWarning)

        # Verify signal-based communication
        assert hasattr(tab.motion_section, "motion_visibility_changed")
        assert hasattr(tab.element_section, "element_visibility_changed")
        assert hasattr(tab.preview_section, "preview_updated")

        self.test_results["architectural_compliance"] = True
        logger.info("✓ Architectural compliance validated")

    def test_performance_characteristics(self):
        """PERMANENT: Refactored components must maintain performance."""
        start_time = time.time()

        # Create multiple tabs to test performance
        tabs = []
        for i in range(5):
            tab = VisibilityTab(
                visibility_service=self.visibility_service,
                global_visibility_service=self.global_service,
            )
            tabs.append(tab)

        creation_time = time.time() - start_time

        # Should create 5 tabs in under 1 second
        assert creation_time < 1.0, f"Tab creation too slow: {creation_time:.2f}s"

        # Test state retrieval performance
        start_time = time.time()
        for tab in tabs:
            summary = tab.get_state_summary()
            assert summary is not None

        retrieval_time = time.time() - start_time
        assert retrieval_time < 0.5, f"State retrieval too slow: {retrieval_time:.2f}s"

        # Cleanup
        for tab in tabs:
            tab.cleanup()

        self.test_results["performance_characteristics"] = True
        logger.info("✓ Performance characteristics validated")

    def run_comprehensive_refactoring_test(self) -> Dict[str, Any]:
        """Run all refactoring validation tests."""
        logger.info("Starting comprehensive refactoring validation...")

        test_methods = [
            self.test_motion_toggle_component_contract,
            self.test_element_toggle_component_contract,
            self.test_motion_controls_section_contract,
            self.test_element_visibility_section_contract,
            self.test_visibility_preview_section_contract,
            self.test_dependency_warning_contract,
            self.test_main_visibility_tab_coordinator_contract,
            self.test_tka_system_integration_preserved,
            self.test_architectural_compliance,
            self.test_performance_characteristics,
        ]

        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                logger.error(f"Test {test_method.__name__} failed: {e}")
                self.test_results[test_method.__name__] = False

        success_count = sum(1 for result in self.test_results.values() if result)
        total_count = len(self.test_results)
        success_rate = success_count / total_count if total_count > 0 else 0

        logger.info(
            f"Refactoring validation complete: {success_count}/{total_count} tests passed"
        )

        return {
            "overall_success": success_rate >= 0.9,
            "success_rate": success_rate,
            "test_results": self.test_results,
            "tests_passed": success_count,
            "total_tests": total_count,
        }


# Convenience function for quick validation
def validate_refactored_visibility_components() -> Dict[str, Any]:
    """Quick validation of refactored visibility components."""
    test_instance = TestRefactoredVisibilityComponents()
    test_instance.setup_method()
    return test_instance.run_comprehensive_refactoring_test()


if __name__ == "__main__":
    # Run tests directly
    result = validate_refactored_visibility_components()
    print(
        f"Refactoring validation: {'✅ PASSED' if result['overall_success'] else '❌ FAILED'}"
    )
    print(f"Success rate: {result['success_rate']:.1%}")
    print(f"Tests: {result['tests_passed']}/{result['total_tests']}")

    if not result["overall_success"]:
        print("\nFailed tests:")
        for test_name, passed in result["test_results"].items():
            if not passed:
                print(f"  - {test_name}")

    exit(0 if result["overall_success"] else 1)
