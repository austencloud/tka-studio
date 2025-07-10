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

from .sequence_generator import SequenceGenerator, SequenceType
from .sequence_manager import SequenceManager

# Core orchestration
from .sequence_orchestrator import ISequenceOrchestratorSignals, SequenceOrchestrator

# Infrastructure services
from .sequence_persister import SequencePersister
from .sequence_repository import IStorageAdapter, RepositoryError, SequenceRepository
from .sequence_state_tracker import SequenceStateTracker

# Focused services
from .sequence_transformer import SequenceTransformer, WorkbenchOperation
from .sequence_validator import SequenceValidator, ValidationError

__all__ = [
    # Core orchestration
    "SequenceOrchestrator",
    "ISequenceOrchestratorSignals",
    "SequenceManager",
    # Focused services
    "SequenceTransformer",
    "WorkbenchOperation",
    "SequenceValidator",
    "ValidationError",
    "SequenceRepository",
    "RepositoryError",
    "IStorageAdapter",
    # Infrastructure
    "SequencePersister",
    "SequenceStateTracker",
    "SequenceGenerator",
    "SequenceType",
]
