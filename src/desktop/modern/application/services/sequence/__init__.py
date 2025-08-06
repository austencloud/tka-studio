"""
Sequence Services - Focused Services for Beat Operations

This package contains the refactored services that replaced the SequenceBeatOperations God Object:

- BeatCreationService: Creating new beats from pictographs
- BeatSequenceService: Sequence manipulation operations
- SequenceWordCalculator: Word calculation from sequences
- SequencePersistenceAdapter: Save/load operations
- BeatOperationCoordinator: Orchestrates the focused services

REFACTORING COMPLETE: 21KB God Object broken into focused 2-5KB services!
"""

from __future__ import annotations

from .beat_creation_service import BeatCreationService
from .beat_operation_coordinator import BeatOperationCoordinator
from .beat_sequence_service import BeatSequenceService

# Backward compatibility - export the coordinator as the main service
from .sequence_beat_operations import SequenceBeatOperations
from .sequence_persistence_adapter import SequencePersistenceAdapter
from .sequence_word_calculator import SequenceWordCalculator


__all__ = [
    "BeatCreationService",
    "BeatOperationCoordinator",
    "BeatSequenceService",
    "SequenceBeatOperations",  # Backward compatibility
    "SequencePersistenceAdapter",
    "SequenceWordCalculator",
]
