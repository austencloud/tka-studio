"""
Write Services Dependency Injection Registration

Registers all write tab services with the DI container following
the established patterns for service registration.
"""

from __future__ import annotations

import logging

from desktop.modern.application.services.write.act_data_service import ActDataService
from desktop.modern.application.services.write.act_editing_service import (
    ActEditingService,
)
from desktop.modern.application.services.write.act_layout_service import (
    ActLayoutService,
)
from desktop.modern.application.services.write.music_player_service import (
    MusicPlayerService,
)
from desktop.modern.application.services.write.write_tab_coordinator import (
    WriteTabCoordinator,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.write_services import (
    IActDataService,
    IActEditingService,
    IActLayoutService,
    IMusicPlayerService,
    IWriteTabCoordinator,
)
from desktop.modern.presentation.views.write import WriteTab


logger = logging.getLogger(__name__)


def register_write_services(container: DIContainer) -> None:
    """
    Register all write tab services with the DI container.

    Args:
        container: DI container to register services with
    """
    try:
        # Core data and editing services (singleton for state consistency)
        container.register_singleton(IActDataService, ActDataService)
        container.register_singleton(IActEditingService, ActEditingService)
        container.register_singleton(IActLayoutService, ActLayoutService)

        # Music player service (singleton to maintain playback state)
        container.register_singleton(IMusicPlayerService, MusicPlayerService)

        # Write tab coordinator (factory to inject all dependencies)
        container.register_factory(
            IWriteTabCoordinator,
            lambda: WriteTabCoordinator(
                act_data_service=container.resolve(IActDataService),
                music_player_service=container.resolve(IMusicPlayerService),
                act_editing_service=container.resolve(IActEditingService),
                act_layout_service=container.resolve(IActLayoutService),
            ),
        )

        # Main write tab (factory to inject container)
        container.register_factory(WriteTab, lambda: WriteTab(container))

        logger.info("Write services registered successfully")

    except Exception as e:
        logger.error(f"Failed to register write services: {e}")
        raise


def validate_write_service_registration(container: DIContainer) -> bool:
    """
    Validate that all write services are properly registered and can be resolved.

    Args:
        container: DI container to validate

    Returns:
        True if all services can be resolved, False otherwise
    """
    try:
        logger.info("Validating write service registration...")

        # Test core service resolution
        act_data_service = container.resolve(IActDataService)
        act_editing_service = container.resolve(IActEditingService)
        act_layout_service = container.resolve(IActLayoutService)
        music_player_service = container.resolve(IMusicPlayerService)

        # Test coordinator resolution
        coordinator = container.resolve(IWriteTabCoordinator)

        # Test main component resolution (skip in headless environments)
        try:
            write_tab = container.resolve(WriteTab)
        except Exception as e:
            if "QApplication" in str(e):
                logger.warning("Skipping UI component test in headless environment")
                write_tab = None
            else:
                raise

        # Verify services have expected interfaces
        services_to_check = [
            (act_data_service, IActDataService),
            (act_editing_service, IActEditingService),
            (act_layout_service, IActLayoutService),
            (music_player_service, IMusicPlayerService),
            (coordinator, IWriteTabCoordinator),
        ]

        for service, interface in services_to_check:
            if not isinstance(service, interface):
                logger.error(f"Service {service} does not implement {interface}")
                return False

        # Test basic functionality
        # Test act data service
        acts_dir = act_data_service.get_acts_directory()
        logger.info(f"Acts directory: {acts_dir}")

        # Test layout calculations
        cols, rows = act_layout_service.calculate_grid_dimensions(10)
        logger.info(f"Grid dimensions for 10 sequences: {cols}x{rows}")

        # Test music player availability
        is_available = music_player_service.is_available()
        logger.info(f"Music player available: {is_available}")

        # Test coordinator basic operations
        test_act = coordinator.create_new_act()
        logger.info(f"Created test act: {test_act.name}")

        logger.info("Write service registration validation completed successfully")
        return True

    except Exception as e:
        logger.error(f"Write service registration validation failed: {e}")
        return False


def get_write_service_dependencies() -> dict:
    """
    Get information about write service dependencies for documentation.

    Returns:
        Dictionary describing service dependencies
    """
    return {
        "core_services": {
            IActDataService.__name__: {
                "implementation": ActDataService.__name__,
                "dependencies": [],
                "description": "Manages act data persistence and file operations",
            },
            IActEditingService.__name__: {
                "implementation": ActEditingService.__name__,
                "dependencies": [],
                "description": "Provides act editing operations (add/remove sequences, etc.)",
            },
            IActLayoutService.__name__: {
                "implementation": ActLayoutService.__name__,
                "dependencies": [],
                "description": "Calculates layout dimensions and positioning for acts",
            },
            IMusicPlayerService.__name__: {
                "implementation": MusicPlayerService.__name__,
                "dependencies": ["pygame (optional)"],
                "description": "Provides music playback functionality using pygame",
            },
        },
        "coordination_services": {
            IWriteTabCoordinator.__name__: {
                "implementation": WriteTabCoordinator.__name__,
                "dependencies": [
                    IActDataService.__name__,
                    IMusicPlayerService.__name__,
                    IActEditingService.__name__,
                    IActLayoutService.__name__,
                ],
                "description": "Orchestrates all write tab functionality and UI coordination",
            },
        },
        "external_dependencies": [
            "pygame for music playback (optional - will fallback gracefully)",
            "PyQt6 for UI components",
            "pathlib for modern path handling",
            "json for act data serialization",
        ],
        "features": {
            "act_management": "Create, load, save, and edit acts",
            "sequence_editing": "Add, remove, and organize sequences in acts",
            "music_integration": "Load and play music files with acts",
            "file_persistence": "JSON-based act storage and retrieval",
            "layout_calculation": "Automatic grid layout for sequence display",
            "ui_components": "Modern UI with browsing, editing, and playback controls",
        },
    }
