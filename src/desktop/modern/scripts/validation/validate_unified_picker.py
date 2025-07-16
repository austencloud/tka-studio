"""
Validation script for unified start position picker architecture.

This script validates that:
1. Start position services are properly registered in DI container
2. Unified start position picker can be instantiated
3. Basic functionality works correctly
4. Service integration is working

Usage:
    python validate_unified_picker.py
"""

import logging
import sys
from pathlib import Path

# Add the modern src directory to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def setup_logging():
    """Setup logging for validation."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    return logging.getLogger(__name__)


def validate_service_registration():
    """Validate that start position services are properly registered."""
    logger = logging.getLogger(__name__)

    try:
        # Create application factory and container
        from core.application.application_factory import (
            ApplicationFactory,
            ApplicationMode,
        )

        logger.info("Creating application container...")
        container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)

        # Validate start position services are registered
        from core.interfaces.start_position_services import (
            IStartPositionDataService,
            IStartPositionOrchestrator,
            IStartPositionSelectionService,
            IStartPositionUIService,
        )

        services_to_check = [
            (IStartPositionDataService, "StartPositionDataService"),
            (IStartPositionSelectionService, "StartPositionSelectionService"),
            (IStartPositionUIService, "StartPositionUIService"),
            (IStartPositionOrchestrator, "StartPositionOrchestrator"),
        ]

        logger.info("Validating start position service registration...")

        for service_interface, service_name in services_to_check:
            try:
                service = container.resolve(service_interface)
                if service:
                    logger.info(f"✅ {service_name} registered and resolvable")
                else:
                    logger.error(f"❌ {service_name} resolved to None")
                    return False
            except Exception as e:
                logger.error(f"❌ Failed to resolve {service_name}: {e}")
                return False

        return True

    except Exception as e:
        logger.error(f"❌ Failed to validate service registration: {e}")
        return False


def validate_component_creation():
    """Validate that unified component can be created with services."""
    logger = logging.getLogger(__name__)

    try:
        # Import Qt Application
        from PyQt6.QtWidgets import QApplication

        # Create Qt application if not exists
        app = QApplication.instance()
        if not app:
            app = QApplication([])

        # Get container and services
        from application.services.pictograph_pool_manager import PictographPoolManager
        from core.application.application_factory import (
            ApplicationFactory,
            ApplicationMode,
        )
        from core.interfaces.start_position_services import (
            IStartPositionDataService,
            IStartPositionOrchestrator,
            IStartPositionSelectionService,
            IStartPositionUIService,
        )

        container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)

        logger.info("Resolving services for component creation...")

        # Resolve all required services
        pool_manager = container.resolve(PictographPoolManager)
        data_service = container.resolve(IStartPositionDataService)
        selection_service = container.resolve(IStartPositionSelectionService)
        ui_service = container.resolve(IStartPositionUIService)
        orchestrator = container.resolve(IStartPositionOrchestrator)

        logger.info("Creating unified start position picker...")

        # Import and create unified component
        from presentation.components.start_position_picker.start_position_picker import (
            PickerMode,
            UnifiedStartPositionPicker,
        )

        picker = UnifiedStartPositionPicker(
            pool_manager=pool_manager,
            data_service=data_service,
            selection_service=selection_service,
            ui_service=ui_service,
            orchestrator=orchestrator,
            initial_mode=PickerMode.BASIC,
        )

        if picker:
            logger.info("✅ Unified start position picker created successfully")
            logger.info(f"   - Initial mode: {picker.get_current_mode().value}")
            logger.info(f"   - Grid mode: {picker.get_current_grid_mode()}")

            # Test basic functionality
            logger.info("Testing basic functionality...")

            # Test mode switching
            picker.set_mode(PickerMode.ADVANCED)
            if picker.get_current_mode() == PickerMode.ADVANCED:
                logger.info("✅ Mode switching works")
            else:
                logger.error("❌ Mode switching failed")
                return False

            # Test grid mode toggle
            original_grid_mode = picker.get_current_grid_mode()
            picker._toggle_grid_mode()
            new_grid_mode = picker.get_current_grid_mode()

            if original_grid_mode != new_grid_mode:
                logger.info("✅ Grid mode toggle works")
            else:
                logger.error("❌ Grid mode toggle failed")
                return False

            return True
        else:
            logger.error("❌ Failed to create unified start position picker")
            return False

    except Exception as e:
        logger.error(f"❌ Failed to validate component creation: {e}")
        import traceback

        traceback.print_exc()
        return False


def validate_service_functionality():
    """Validate that services provide expected functionality."""
    logger = logging.getLogger(__name__)

    try:
        from core.application.application_factory import (
            ApplicationFactory,
            ApplicationMode,
        )
        from core.interfaces.start_position_services import (
            IStartPositionSelectionService,
            IStartPositionUIService,
        )

        container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)

        logger.info("Testing service functionality...")

        # Test UI service
        ui_service = container.resolve(IStartPositionUIService)

        # Test getting positions
        basic_positions = ui_service.get_positions_for_mode(
            "diamond", is_advanced=False
        )
        advanced_positions = ui_service.get_positions_for_mode(
            "diamond", is_advanced=True
        )

        if len(basic_positions) == 3:
            logger.info("✅ Basic positions count correct (3)")
        else:
            logger.error(f"❌ Basic positions count incorrect: {len(basic_positions)}")
            return False

        if len(advanced_positions) == 16:
            logger.info("✅ Advanced positions count correct (16)")
        else:
            logger.error(
                f"❌ Advanced positions count incorrect: {len(advanced_positions)}"
            )
            return False

        # Test size calculation
        size = ui_service.calculate_option_size(1000, is_advanced=False)
        if isinstance(size, int) and 80 <= size <= 200:
            logger.info(f"✅ Size calculation works: {size}px")
        else:
            logger.error(f"❌ Size calculation failed: {size}")
            return False

        # Test selection service
        selection_service = container.resolve(IStartPositionSelectionService)

        # Test validation
        if selection_service.validate_selection("alpha1_alpha1"):
            logger.info("✅ Position validation works")
        else:
            logger.error("❌ Position validation failed")
            return False

        # Test key extraction
        end_pos = selection_service.extract_end_position_from_key("alpha1_alpha1")
        if end_pos == "alpha1":
            logger.info("✅ End position extraction works")
        else:
            logger.error(f"❌ End position extraction failed: {end_pos}")
            return False

        return True

    except Exception as e:
        logger.error(f"❌ Failed to validate service functionality: {e}")
        return False


def main():
    """Main validation function."""
    logger = setup_logging()

    logger.info("🔍 Starting unified start position picker validation...")
    logger.info("=" * 60)

    # Step 1: Validate service registration
    logger.info("Step 1: Validating service registration...")
    if not validate_service_registration():
        logger.error("❌ Service registration validation FAILED")
        return 1

    # Step 2: Validate service functionality
    logger.info("Step 2: Validating service functionality...")
    if not validate_service_functionality():
        logger.error("❌ Service functionality validation FAILED")
        return 1

    # Step 3: Validate component creation
    logger.info("Step 3: Validating component creation...")
    if not validate_component_creation():
        logger.error("❌ Component creation validation FAILED")
        return 1

    logger.info("=" * 60)
    logger.info("🎉 ALL VALIDATIONS PASSED!")
    logger.info("")
    logger.info("✅ Start position services are properly registered")
    logger.info("✅ Services provide expected functionality")
    logger.info("✅ Unified component can be created and used")
    logger.info("✅ Architecture consolidation successful")
    logger.info("")
    logger.info("The unified start position picker is ready for use!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
