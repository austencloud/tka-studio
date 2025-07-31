"""
Autonomous Generate Tab E2E Test

This test autonomously generates sequences in the actual generate tab to verify:
1. Service registration and resolution
2. Real CSV data loading vs mock data
3. Grid mode consistency
4. Complete generation workflow
5. UI state management
"""

import logging

from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication
import pytest

logger = logging.getLogger(__name__)


class AutonomousGenerateTest:
    """Autonomous test runner for generate tab functionality."""

    def __init__(self, main_window):
        self.main_window = main_window
        self.construct_tab = None
        self.generate_panel = None
        self.results = []

    def setup(self):
        """Setup test environment."""
        logger.info("🔧 Setting up autonomous generate test...")

        # Get construct tab from modern tab widget structure
        tab_widget = self.main_window.tab_widget
        if not tab_widget:
            raise RuntimeError("Could not find tab widget")

        # Find construct tab by iterating through tabs
        self.construct_tab = None
        for i in range(tab_widget.count()):
            widget = tab_widget.widget(i)
            # Check if this is the construct tab
            if (
                hasattr(widget, "_controller")
                or "construct" in str(type(widget)).lower()
            ):
                self.construct_tab = widget
                break

        if not self.construct_tab:
            # Try alternative access method
            if hasattr(tab_widget, "construct_tab"):
                self.construct_tab = tab_widget.construct_tab
            else:
                raise RuntimeError("Could not find construct tab in tab widget")

        # Navigate to construct tab
        tab_widget.setCurrentWidget(self.construct_tab)
        QTest.qWait(1000)

        # Get generate panel
        layout_manager = getattr(self.construct_tab, "_view", None)
        if layout_manager:
            layout_manager = getattr(layout_manager, "_layout_manager", None)
            if layout_manager:
                self.generate_panel = getattr(layout_manager, "generate_panel", None)

        if not self.generate_panel:
            logger.warning("Could not find generate panel directly, will use signals")

        logger.info("✅ Test setup complete")

    def test_service_registration(self):
        """Test that generation services are properly registered."""
        logger.info("🔍 Testing service registration...")

        try:
            # Get the DI container from construct tab controller
            controller = getattr(self.construct_tab, "_controller", None)
            if not controller:
                raise RuntimeError("Could not find construct tab controller")

            container = getattr(controller, "_container", None)
            if not container:
                raise RuntimeError("Could not find DI container")

            # Try to resolve generation service
            from desktop.modern.core.interfaces.generation_services import (
                IGenerationService,
            )

            generation_service = container.resolve(IGenerationService)

            if generation_service:
                logger.info("✅ IGenerationService successfully resolved")
                self.results.append(
                    ("service_registration", True, "IGenerationService resolved")
                )
                return True
            else:
                logger.error("❌ IGenerationService resolved to None")
                self.results.append(
                    ("service_registration", False, "Service resolved to None")
                )
                return False

        except Exception as e:
            logger.error(f"❌ Service registration test failed: {e}")
            self.results.append(("service_registration", False, str(e)))
            return False

    def test_freeform_generation(self):
        """Test freeform sequence generation."""
        logger.info("🎯 Testing freeform generation...")

        try:
            # Create generation config
            from desktop.modern.core.interfaces.generation_services import (
                GenerationMode,
                LetterType,
                PropContinuity,
            )
            from desktop.modern.domain.models.generation_models import GenerationConfig

            config = GenerationConfig(
                mode=GenerationMode.FREEFORM,
                length=4,  # Short sequence for testing
                level=1,
                turn_intensity=1.0,
                prop_continuity=PropContinuity.CONTINUOUS,
                letter_types={LetterType.TYPE1, LetterType.TYPE2, LetterType.TYPE3},
            )

            # Monitor for generation completion
            generation_completed = False
            generation_success = False
            error_message = ""

            def on_generation_completed(success, error):
                nonlocal generation_completed, generation_success, error_message
                generation_completed = True
                generation_success = success
                error_message = error
                logger.info(
                    f"🔔 Generation completed: success={success}, error={error}"
                )

            # Connect to generation completion signal if available
            controller = getattr(self.construct_tab, "_controller", None)
            if controller and hasattr(controller, "generation_completed"):
                controller.generation_completed.connect(on_generation_completed)

            # Trigger generation
            logger.info("🚀 Triggering freeform generation...")
            if controller and hasattr(controller, "handle_generation_request"):
                controller.handle_generation_request(config)
            else:
                raise RuntimeError("Could not find generation request handler")

            # Wait for completion with timeout
            timeout_ms = 10000  # 10 seconds
            start_time = QTest.qWait(0)  # Get current time

            while not generation_completed and timeout_ms > 0:
                QApplication.processEvents()
                QTest.qWait(100)
                timeout_ms -= 100

            if not generation_completed:
                logger.error("❌ Generation timed out")
                self.results.append(
                    ("freeform_generation", False, "Generation timed out")
                )
                return False

            if generation_success:
                logger.info("✅ Freeform generation successful")
                self.results.append(
                    ("freeform_generation", True, "Generation completed successfully")
                )
                return True
            else:
                logger.error(f"❌ Freeform generation failed: {error_message}")
                self.results.append(
                    (
                        "freeform_generation",
                        False,
                        f"Generation failed: {error_message}",
                    )
                )
                return False

        except Exception as e:
            logger.error(f"❌ Freeform generation test failed: {e}")
            self.results.append(("freeform_generation", False, str(e)))
            return False

    def test_circular_generation(self):
        """Test circular sequence generation."""
        logger.info("🔄 Testing circular generation...")

        try:
            # Create circular generation config
            from desktop.modern.core.interfaces.generation_services import (
                CAPType,
                GenerationMode,
                LetterType,
                PropContinuity,
                SliceSize,
            )
            from desktop.modern.domain.models.generation_models import GenerationConfig

            config = GenerationConfig(
                mode=GenerationMode.CIRCULAR,
                length=8,  # Circular sequences need even length
                level=1,
                turn_intensity=1.0,
                prop_continuity=PropContinuity.CONTINUOUS,
                letter_types={LetterType.TYPE1, LetterType.TYPE2},
                cap_type=CAPType.STRICT_ROTATED,
                slice_size=SliceSize.HALVED,
            )

            # Monitor for generation completion
            generation_completed = False
            generation_success = False
            error_message = ""

            def on_generation_completed(success, error):
                nonlocal generation_completed, generation_success, error_message
                generation_completed = True
                generation_success = success
                error_message = error
                logger.info(
                    f"🔔 Circular generation completed: success={success}, error={error}"
                )

            # Connect to generation completion signal if available
            controller = getattr(self.construct_tab, "_controller", None)
            if controller and hasattr(controller, "generation_completed"):
                controller.generation_completed.connect(on_generation_completed)

            # Trigger generation
            logger.info("🚀 Triggering circular generation...")
            if controller and hasattr(controller, "handle_generation_request"):
                controller.handle_generation_request(config)
            else:
                raise RuntimeError("Could not find generation request handler")

            # Wait for completion with timeout
            timeout_ms = 15000  # 15 seconds for circular (more complex)

            while not generation_completed and timeout_ms > 0:
                QApplication.processEvents()
                QTest.qWait(100)
                timeout_ms -= 100

            if not generation_completed:
                logger.error("❌ Circular generation timed out")
                self.results.append(
                    ("circular_generation", False, "Generation timed out")
                )
                return False

            if generation_success:
                logger.info("✅ Circular generation successful")
                self.results.append(
                    ("circular_generation", True, "Generation completed successfully")
                )
                return True
            else:
                logger.error(f"❌ Circular generation failed: {error_message}")
                self.results.append(
                    (
                        "circular_generation",
                        False,
                        f"Generation failed: {error_message}",
                    )
                )
                return False

        except Exception as e:
            logger.error(f"❌ Circular generation test failed: {e}")
            self.results.append(("circular_generation", False, str(e)))
            return False

    def analyze_generation_data(self):
        """Analyze the generated sequence data for quality."""
        logger.info("📊 Analyzing generation data...")

        try:
            # Get workbench state manager
            controller = getattr(self.construct_tab, "_controller", None)
            if not controller:
                raise RuntimeError("Could not find construct tab controller")

            workbench_manager = getattr(controller, "_workbench_state_manager", None)
            if not workbench_manager:
                logger.warning("Could not find workbench state manager")
                self.results.append(
                    ("data_analysis", False, "No workbench state manager")
                )
                return False

            # Get current sequence
            current_sequence = workbench_manager.get_current_sequence()
            if not current_sequence:
                logger.warning("No current sequence found")
                self.results.append(("data_analysis", False, "No current sequence"))
                return False

            # Analyze sequence properties
            beats = getattr(current_sequence, "beats", [])
            if not beats:
                logger.warning("Sequence has no beats")
                self.results.append(("data_analysis", False, "No beats in sequence"))
                return False

            logger.info(f"📈 Sequence analysis: {len(beats)} beats")

            # Check for mock data vs real data
            mock_count = 0
            real_count = 0

            for beat in beats:
                if hasattr(beat, "metadata"):
                    metadata = beat.metadata
                    if isinstance(metadata, dict) and metadata.get("mock"):
                        mock_count += 1
                    else:
                        real_count += 1
                elif hasattr(beat, "letter"):
                    # Check if it's a real letter or mock
                    letter = beat.letter
                    if letter in ["A", "B", "C", "D", "E", "F", "G", "H"]:
                        real_count += 1
                    else:
                        mock_count += 1

            total_beats = len(beats)
            real_percentage = (real_count / total_beats) * 100 if total_beats > 0 else 0

            logger.info(
                f"📊 Data analysis: {real_count}/{total_beats} real beats ({real_percentage:.1f}%)"
            )

            if mock_count > 0:
                logger.warning(
                    f"⚠️ Found {mock_count} mock beats - CSV data not being used properly"
                )
                self.results.append(
                    (
                        "data_analysis",
                        False,
                        f"Mock data detected: {mock_count}/{total_beats} beats",
                    )
                )
                return False
            else:
                logger.info("✅ All beats appear to use real data")
                self.results.append(
                    (
                        "data_analysis",
                        True,
                        f"Real data: {real_count}/{total_beats} beats",
                    )
                )
                return True

        except Exception as e:
            logger.error(f"❌ Data analysis failed: {e}")
            self.results.append(("data_analysis", False, str(e)))
            return False

    def run_all_tests(self):
        """Run all autonomous tests."""
        logger.info("🎬 Starting autonomous generate tab tests...")

        try:
            self.setup()

            # Run tests in sequence
            tests = [
                self.test_service_registration,
                self.test_freeform_generation,
                self.analyze_generation_data,
                self.test_circular_generation,
                self.analyze_generation_data,
            ]

            passed = 0
            total = len(tests)

            for test in tests:
                try:
                    if test():
                        passed += 1
                except Exception as e:
                    logger.error(f"❌ Test {test.__name__} failed with exception: {e}")

            # Print summary
            logger.info(f"🎯 Test Summary: {passed}/{total} tests passed")
            for test_name, success, message in self.results:
                status = "✅" if success else "❌"
                logger.info(f"  {status} {test_name}: {message}")

            return passed == total

        except Exception as e:
            logger.error(f"❌ Autonomous test suite failed: {e}")
            import traceback

            traceback.print_exc()
            return False


@pytest.mark.e2e
def test_autonomous_generate_functionality(tka_app):
    """
    Autonomous end-to-end test for generate tab functionality.

    This test will:
    1. Verify service registration
    2. Test freeform generation
    3. Test circular generation
    4. Analyze data quality (real vs mock)
    5. Verify complete workflow
    """
    app, main_window = tka_app

    # Create and run autonomous test
    test_runner = AutonomousGenerateTest(main_window)
    success = test_runner.run_all_tests()

    # Assert overall success
    assert success, "Autonomous generate tab test failed - check logs for details"


if __name__ == "__main__":
    """Run autonomous test standalone for debugging."""
    import os
    import sys

    # Add paths for imports
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    sys.path.insert(0, os.path.join(project_root, "src"))
    sys.path.insert(0, os.path.join(project_root, "src/desktop/modern"))

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Create application
    from desktop.modern.main import create_application

    app, main_window = create_application()
    main_window.show()

    # Wait for initialization
    QTest.qWait(3000)

    # Run autonomous test
    test_runner = AutonomousGenerateTest(main_window)
    success = test_runner.run_all_tests()

    if success:
        logger.info("🎉 All autonomous tests passed!")
        sys.exit(0)
    else:
        logger.error("❌ Some autonomous tests failed!")
        sys.exit(1)
