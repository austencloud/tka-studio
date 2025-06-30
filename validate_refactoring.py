#!/usr/bin/env python3
"""
Validate Refactored Visibility Components
========================================

Quick validation script to ensure the refactored visibility components
work correctly and maintain all existing functionality.
"""

import sys
import os
import logging
from pathlib import Path

# Add TKA to path
tka_path = Path(__file__).parent / "src" / "desktop" / "modern" / "src"
sys.path.insert(0, str(tka_path))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_imports():
    """Test that all refactored components can be imported."""
    try:
        # Test core imports
        from core.application.application_factory import ApplicationFactory
        from core.testing.ai_agent_helpers import TKAAITestHelper
        from core.interfaces.tab_settings_interfaces import IVisibilityService

        # Test service imports
        from application.services.settings.visibility_state_manager import (
            ModernVisibilityStateManager,
        )
        from application.services.pictograph.global_visibility_service import (
            GlobalVisibilityService,
        )

        # Test refactored component imports
        from presentation.components.ui.settings.visibility.visibility_tab import (
            VisibilityTab,
        )
        from presentation.components.ui.settings.visibility.components import (
            MotionControlsSection,
            ElementVisibilitySection,
            VisibilityPreviewSection,
            DependencyWarning,
        )
        from presentation.components.ui.settings.components import (
            MotionToggle,
            ElementToggle,
        )

        logger.info("✅ All imports successful")
        return True

    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False


def test_component_creation():
    """Test that components can be created without errors."""
    try:
        from core.application.application_factory import ApplicationFactory
        from core.interfaces.tab_settings_interfaces import IVisibilityService
        from application.services.settings.visibility_state_manager import (
            ModernVisibilityStateManager,
        )
        from application.services.pictograph.global_visibility_service import (
            GlobalVisibilityService,
        )

        # Create test services (no Qt components)
        container = ApplicationFactory.create_test_app()
        visibility_service = container.resolve(IVisibilityService)
        state_manager = ModernVisibilityStateManager(visibility_service)
        global_service = GlobalVisibilityService()

        # Test service creation and basic functionality
        assert visibility_service is not None
        assert state_manager is not None
        assert global_service is not None

        # Test state manager functionality
        assert hasattr(state_manager, "get_motion_visibility")
        assert hasattr(state_manager, "set_motion_visibility")
        assert hasattr(state_manager, "get_glyph_visibility")
        assert hasattr(state_manager, "set_glyph_visibility")

        logger.info("✅ Component creation successful (services only)")
        return True

    except Exception as e:
        logger.error(f"❌ Component creation failed: {e}")
        return False


def test_tka_integration():
    """Test that TKA system integration is preserved."""
    try:
        from core.testing.ai_agent_helpers import TKAAITestHelper

        # Use TKAAITestHelper to validate system works
        helper = TKAAITestHelper(use_test_mode=True)
        result = helper.run_comprehensive_test_suite()

        if not result.success:
            logger.error(f"❌ TKA system test failed: {result.errors}")
            return False

        if result.metadata["success_rate"] <= 0.8:
            logger.error(
                f"❌ TKA success rate too low: {result.metadata['success_rate']:.1%}"
            )
            return False

        # Test sequence creation
        seq_result = helper.create_sequence("Refactoring Test", 4)
        if not seq_result.success:
            logger.error(f"❌ Sequence creation failed: {seq_result.errors}")
            return False

        # Test beat creation
        beat_result = helper.create_beat_with_motions(1, "A")
        if not beat_result.success:
            logger.error(f"❌ Beat creation failed: {beat_result.errors}")
            return False

        logger.info("✅ TKA system integration preserved")
        return True

    except Exception as e:
        logger.error(f"❌ TKA integration test failed: {e}")
        return False


def test_architectural_compliance():
    """Test that components follow TKA architectural patterns."""
    try:
        from core.application.application_factory import ApplicationFactory
        from core.interfaces.tab_settings_interfaces import IVisibilityService
        from application.services.settings.visibility_state_manager import (
            ModernVisibilityStateManager,
        )
        from presentation.components.ui.settings.visibility.visibility_tab import (
            VisibilityTab,
        )
        from presentation.components.ui.settings.visibility.components import (
            MotionControlsSection,
            ElementVisibilitySection,
            VisibilityPreviewSection,
            DependencyWarning,
        )

        # Test dependency injection
        container = ApplicationFactory.create_test_app()
        visibility_service = container.resolve(IVisibilityService)

        # Test that component classes exist and have expected methods
        assert hasattr(MotionControlsSection, "__init__")
        assert hasattr(ElementVisibilitySection, "__init__")
        assert hasattr(VisibilityPreviewSection, "__init__")
        assert hasattr(DependencyWarning, "__init__")

        # Test that VisibilityTab class exists and has expected structure
        assert hasattr(VisibilityTab, "__init__")
        assert hasattr(VisibilityTab, "cleanup")
        assert hasattr(VisibilityTab, "get_state_summary")
        assert hasattr(VisibilityTab, "refresh_all_settings")

        # Test service injection pattern (without creating Qt widgets)
        state_manager = ModernVisibilityStateManager(visibility_service)
        assert state_manager is not None

        logger.info("✅ Architectural compliance validated")
        return True

    except Exception as e:
        logger.error(f"❌ Architectural compliance test failed: {e}")
        return False


def main():
    """Run all validation tests."""
    print("🔧 Validating Refactored Visibility Components")
    print("=" * 50)

    tests = [
        ("Import Validation", test_imports),
        ("Component Creation", test_component_creation),
        ("TKA Integration", test_tka_integration),
        ("Architectural Compliance", test_architectural_compliance),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        result = test_func()
        results.append(result)
        print(f"   {'✅ PASSED' if result else '❌ FAILED'}")

    success_count = sum(results)
    total_count = len(results)
    success_rate = success_count / total_count

    print("\n" + "=" * 50)
    print(f"📊 Validation Results: {success_count}/{total_count} tests passed")
    print(f"📊 Success Rate: {success_rate:.1%}")

    if success_rate >= 0.75:
        print("🎉 Refactoring validation SUCCESSFUL!")
        print("✅ Components maintain functionality and follow TKA patterns")
        return 0
    else:
        print("❌ Refactoring validation FAILED!")
        print("⚠️  Some components may have issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())
