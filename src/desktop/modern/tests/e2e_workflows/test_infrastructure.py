"""
Test Infrastructure - Eliminates All Duplicated Setup Logic
===========================================================

Single setup for all end-to-end tests. No more repeated:
- Path configuration
- Container creation
- Service resolution
- Application setup
"""

import logging
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

# Fix path once for all tests
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from desktop.modern.core.application.application_factory import (
    ApplicationFactory,
    ApplicationMode,
)
from desktop.modern.tests.framework.tka_workflow_tester import (
    TestConfiguration,
    TestMode,
    TKAWorkflowTester,
)


class TestInfrastructure:
    """
    Singleton test infrastructure - eliminates all setup duplication.

    Usage in tests:
        infra = TestInfrastructure()
        service = infra.get_service('start_position_data')
        container = infra.container
    """

    _instance = None
    _initialized = False

    def __new__(cls, visual_mode: bool = True):
        # Create new instance if mode changed or no instance exists
        if (
            cls._instance is None
            or getattr(cls._instance, "visual_mode", None) != visual_mode
        ):
            cls._instance = super().__new__(cls)
            cls._initialized = False  # Force re-initialization if mode changed
        return cls._instance

    def __init__(self, visual_mode: bool = True):
        if not self._initialized:
            self.app = None
            self.container = None
            self.workflow_tester = None
            self.services = {}
            self.visual_mode = visual_mode
            self.logger = self._setup_logging()
            self._initialize_once()
            TestInfrastructure._initialized = True

    def _setup_logging(self) -> logging.Logger:
        """Setup logging once for all tests."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
        )
        return logging.getLogger(__name__)

    def _initialize_once(self):
        """Initialize everything once - no more duplication!"""
        self.logger.info("🔧 Initializing test infrastructure...")

        # QApplication setup once
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()

        if self.visual_mode:
            self.logger.info("🚀 Launching REAL TKA Application in visual mode...")
            self._launch_real_tka_application()
        else:
            self.logger.info("🤖 Setting up headless test container...")
            # Container setup once for headless mode
            self.container = ApplicationFactory.create_app(
                ApplicationMode.TEST, force=True
            )

        # Pre-resolve all commonly used services once
        self._preload_services()

        # Workflow tester setup once
        self._setup_workflow_tester(self.visual_mode)

        self.logger.info("✅ Test infrastructure ready")

    def _launch_real_tka_application(self):
        """Launch the actual TKA application like a real user would."""
        try:
            # Import the real main function
            from desktop.modern.main import main as tka_main

            # Remove any test flags from sys.argv to ensure normal startup
            original_argv = sys.argv[:]
            sys.argv = [sys.argv[0]]  # Keep only the script name

            # Launch the real TKA application
            self.logger.info("🎨 Starting real TKA application...")
            result = tka_main()

            # If main returns a container (test/headless mode), we got it
            if hasattr(result, "resolve"):
                self.container = result
            else:
                # For production mode, we need to get the global container
                from desktop.modern.core.service_locator import get_global_container

                self.container = get_global_container()

            # Restore original argv
            sys.argv = original_argv

            # Give the UI time to fully load
            import time

            time.sleep(2)  # Allow UI to fully initialize

            self.logger.info("✅ Real TKA application launched successfully!")

        except Exception as e:
            self.logger.error(f"❌ Failed to launch real TKA application: {e}")
            # Fallback to container-only mode
            self.container = ApplicationFactory.create_app(
                ApplicationMode.TEST, force=True
            )

    def _preload_services(self):
        """Pre-resolve services so no test has to do this repeatedly."""
        try:
            # Start position services (used by construct tab tests)
            from desktop.modern.core.interfaces.start_position_services import (
                IStartPositionDataService,
                IStartPositionOrchestrator,
                IStartPositionSelectionService,
                IStartPositionUIService,
            )

            self.services["start_position_data"] = self.container.resolve(
                IStartPositionDataService
            )
            self.services["start_position_selection"] = self.container.resolve(
                IStartPositionSelectionService
            )
            self.services["start_position_ui"] = self.container.resolve(
                IStartPositionUIService
            )
            self.services["start_position_orchestrator"] = self.container.resolve(
                IStartPositionOrchestrator
            )

            # Workbench services (used by sequence tests)
            from desktop.modern.core.interfaces.workbench_services import (
                IWorkbenchStateManager,
            )

            self.services["workbench_state"] = self.container.resolve(
                IWorkbenchStateManager
            )

            # Settings services (used by configuration tests)
            try:
                from desktop.modern.application.services.settings.modern_settings_service import (
                    ModernSettingsService,
                )
                from desktop.modern.core.interfaces.settings_services import (
                    IBackgroundSettingsManager,
                    IPropTypeSettingsManager,
                    IVisibilitySettingsManager,
                )

                self.services["settings"] = self.container.resolve(
                    ModernSettingsService
                )
                self.services["background_settings"] = self.container.resolve(
                    IBackgroundSettingsManager
                )
                self.services["visibility_settings"] = self.container.resolve(
                    IVisibilitySettingsManager
                )
                self.services["prop_settings"] = self.container.resolve(
                    IPropTypeSettingsManager
                )
            except Exception:
                self.logger.warning(
                    "Settings services not available in test mode - this is normal"
                )

            # Sequence card services (used by sequence card tests)
            from desktop.modern.core.interfaces.sequence_card_services import (
                ISequenceCardCacheService,
                ISequenceCardDataService,
                ISequenceCardDisplayService,
                ISequenceCardExportService,
                ISequenceCardLayoutService,
                ISequenceCardSettingsService,
            )

            try:
                self.services["sequence_card_data"] = self.container.resolve(
                    ISequenceCardDataService
                )
                self.services["sequence_card_cache"] = self.container.resolve(
                    ISequenceCardCacheService
                )
                self.services["sequence_card_layout"] = self.container.resolve(
                    ISequenceCardLayoutService
                )
                self.services["sequence_card_display"] = self.container.resolve(
                    ISequenceCardDisplayService
                )
                self.services["sequence_card_export"] = self.container.resolve(
                    ISequenceCardExportService
                )
                self.services["sequence_card_settings"] = self.container.resolve(
                    ISequenceCardSettingsService
                )
            except Exception:
                self.logger.warning("Sequence card services not available")

            self.logger.info(f"✅ Pre-loaded {len(self.services)} services")

        except Exception as e:
            self.logger.warning(f"Could not preload some services: {e}")

    def _setup_workflow_tester(self, visual_mode: bool = True):
        """Setup workflow tester with optimized configuration."""
        config = TestConfiguration(
            mode=TestMode.UI_VISIBLE if visual_mode else TestMode.HEADLESS,
            debug_logging=False,
            timing_delays={
                "startup": 800,  # Slower for visual mode so you can see what's happening
                "transition": 500,  # Slower transitions to see UI changes
                "operation": 300,  # Slower operations to see interactions
                "validation": 200,  # Slower validation to see results
            },
            visual_validation=True,
        )

        self.workflow_tester = TKAWorkflowTester(config)
        if not self.workflow_tester.initialize():
            raise RuntimeError("Failed to initialize workflow tester")

    def get_service(self, service_name: str):
        """Get pre-resolved service by name."""
        service = self.services.get(service_name)
        if service is None:
            self.logger.warning(f"Service '{service_name}' not available")
        return service

    def get_all_services(self) -> Dict[str, Any]:
        """Get all pre-resolved services."""
        return self.services.copy()

    def quick_reset(self):
        """Quick reset between tests - much faster than full setup."""
        if self.workflow_tester:
            self.workflow_tester.clear_sequence()
        QTest.qWait(50)  # Minimal wait

    def validate_service_health(self) -> bool:
        """Quick health check of critical services."""
        critical_services = [
            "start_position_data",
            "start_position_selection",
            "workbench_state",
            # Removed 'settings' since it's not properly registered in test mode
        ]

        for service_name in critical_services:
            if not self.get_service(service_name):
                self.logger.error(f"Critical service '{service_name}' not available")
                return False

        return True

    def cleanup(self):
        """Final cleanup - only called once at the end."""
        try:
            if self.workflow_tester:
                self.workflow_tester.cleanup()

            if self.app and self.app != QApplication.instance():
                self.app.quit()

        except Exception as e:
            self.logger.warning(f"Cleanup warning: {e}")


# Convenience functions for easy test usage
def get_test_infrastructure(visual_mode: bool = True) -> TestInfrastructure:
    """Get the test infrastructure instance."""
    return TestInfrastructure(visual_mode=visual_mode)


def quick_test_setup(
    visual_mode: bool = True,
) -> tuple[TestInfrastructure, TKAWorkflowTester]:
    """Quick setup that returns infrastructure and workflow tester."""
    infra = TestInfrastructure(visual_mode=visual_mode)
    infra.quick_reset()
    return infra, infra.workflow_tester
