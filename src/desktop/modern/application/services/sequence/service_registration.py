"""
Service Registration for Focused Beat Services

Provides registration helpers for the new focused services that replaced SequenceBeatOperations.
This ensures proper dependency injection setup for the refactored architecture.
"""

from __future__ import annotations

from desktop.modern.core.dependency_injection.di_container import DIContainer

from .beat_creation_service import BeatCreationService
from .beat_operation_coordinator import BeatOperationCoordinator
from .beat_sequence_service import BeatSequenceService
from .sequence_persistence_adapter import SequencePersistenceAdapter
from .sequence_word_calculator import SequenceWordCalculator


def register_focused_beat_services(container: DIContainer) -> None:
    """
    Register all focused beat services in the DI container.

    Args:
        container: The DI container to register services in
    """
    print("🔧 [SERVICE_REGISTRATION] Registering focused beat services...")

    # Register focused services as singletons
    container.register_singleton(BeatCreationService, BeatCreationService)
    container.register_singleton(BeatSequenceService, BeatSequenceService)
    container.register_singleton(SequenceWordCalculator, SequenceWordCalculator)
    container.register_singleton(SequencePersistenceAdapter, SequencePersistenceAdapter)

    # Register coordinator with dependencies
    container.register_factory(
        BeatOperationCoordinator,
        lambda: BeatOperationCoordinator(
            beat_creator=container.resolve(BeatCreationService),
            sequence_service=container.resolve(BeatSequenceService),
            word_calculator=container.resolve(SequenceWordCalculator),
            persistence=container.resolve(SequencePersistenceAdapter),
        ),
    )

    print("✅ [SERVICE_REGISTRATION] Focused beat services registered successfully")


def register_legacy_beat_operations_adapter(container: DIContainer) -> None:
    """
    Register the legacy SequenceBeatOperations adapter for backward compatibility.

    Args:
        container: The DI container to register services in
    """
    from .sequence_beat_operations import SequenceBeatOperations

    print("🔧 [SERVICE_REGISTRATION] Registering legacy beat operations adapter...")

    # Register the adapter that uses focused services internally
    container.register_factory(
        SequenceBeatOperations,
        lambda: SequenceBeatOperations(),  # Uses default coordinator internally
    )

    print("✅ [SERVICE_REGISTRATION] Legacy beat operations adapter registered")


def verify_service_registration(container: DIContainer) -> bool:
    """
    Verify that all focused services are properly registered and resolvable.

    Args:
        container: The DI container to verify

    Returns:
        True if all services are properly registered, False otherwise
    """
    print("🔍 [SERVICE_VERIFICATION] Verifying focused service registration...")

    services_to_verify = [
        BeatCreationService,
        BeatSequenceService,
        SequenceWordCalculator,
        SequencePersistenceAdapter,
        BeatOperationCoordinator,
    ]

    try:
        for service_type in services_to_verify:
            service_instance = container.resolve(service_type)
            if service_instance is None:
                print(
                    f"❌ [SERVICE_VERIFICATION] Failed to resolve {service_type.__name__}"
                )
                return False
            print(
                f"✅ [SERVICE_VERIFICATION] {service_type.__name__} resolved successfully"
            )

        print("✅ [SERVICE_VERIFICATION] All focused services verified successfully")
        return True

    except Exception as e:
        print(f"❌ [SERVICE_VERIFICATION] Error verifying services: {e}")
        return False
