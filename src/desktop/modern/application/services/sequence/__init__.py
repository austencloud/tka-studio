"""
Sequence Services - Clean Architecture Implementation

This package provides focused, single-responsibility services for sequence operations:

📋 Core Services:
- SequenceOrchestrator: Main business operations coordinator
- SequenceTransformer: Workbench transformations
- SequenceValidator: Validation rules and integrity checks
- SequenceRepository: CRUD operations and data access

💾 Infrastructure:
- SequencePersister: JSON save/load operations (renamed from persistence_service)
- SequenceStateTracker: Event-driven state management (renamed from state_manager)
- SequenceGenerator: Generation algorithms (already existed)

✅ Benefits of This Architecture:
- Single Responsibility Principle: Each service has one clear purpose
- No more 700+ line "god services"
- Clear separation of concerns
- Easier testing and maintenance
- Framework-agnostic business logic
"""

# Core microservices - CLEAN MICROSERVICES ARCHITECTURE
from shared.application.services.sequence.beat_factory import BeatFactory
from shared.application.services.sequence.sequence_dictionary_manager import (
    SequenceDictionaryManager,
)
from shared.application.services.sequence.sequence_generator import (
    SequenceGenerator,
    SequenceType,
)

# Infrastructure services
from shared.application.services.sequence.sequence_persister import SequencePersister
from shared.application.services.sequence.sequence_repository import (
    RepositoryError,
    SequenceRepository,
)

# Focused services
from shared.application.services.sequence.sequence_transformer import (
    SequenceTransformer,
    WorkbenchOperation,
)
from shared.application.services.sequence.sequence_validator import (
    SequenceValidator,
    ValidationError,
)

from .loader import SequenceLoader
from .sequence_beat_operations import SequenceBeatOperations
from .sequence_start_position_manager import SequenceStartPositionManager
from .sequence_state_tracker import SequenceStateTracker

# Legacy orchestration (DEPRECATED - use SequenceCoordinator instead)
# from .sequence_orchestrator import ISequenceOrchestratorSignals, SequenceOrchestrator


# Legacy import - SequenceManager is deprecated, use SequenceOrchestrator instead


__all__ = [
    # CLEAN MICROSERVICES ARCHITECTURE
    # Core microservices - inject these directly into components that need them
    "SequenceBeatOperations",
    "SequenceStartPositionManager",
    "SequenceLoader",
    "SequenceDictionaryManager",
    # Beat operations
    "BeatFactory",
    # Focused services
    "SequenceTransformer",
    "WorkbenchOperation",
    "SequenceValidator",
    "ValidationError",
    "SequenceRepository",
    "RepositoryError",
    # "IStorageAdapter",  # Removed - doesn't exist
    # Infrastructure
    "SequencePersister",
    "SequenceStateTracker",
    "SequenceGenerator",
    "SequenceType",
]
