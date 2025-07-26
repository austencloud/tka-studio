"""
Workbench State Service - Clean interface for workbench data access

This replaces the clumsy workbench_getter/workbench_setter pattern with a proper service.
"""

from abc import ABC, abstractmethod
from typing import Optional, Protocol, runtime_checkable

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


@runtime_checkable
class WorkbenchProtocol(Protocol):
    """Protocol defining what we need from a workbench."""
    
    def get_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence from the workbench."""
        ...
    
    def set_sequence(self, sequence: SequenceData) -> None:
        """Set the sequence in the workbench."""
        ...
    
    def get_start_position_data(self) -> Optional[BeatData]:
        """Get the start position data."""
        ...
    
    def set_start_position_data(self, start_position: BeatData, position_key: str) -> None:
        """Set the start position data."""
        ...


class IWorkbenchStateService(ABC):
    """Interface for workbench state access."""
    
    @abstractmethod
    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence."""
        ...
    
    @abstractmethod
    def set_current_sequence(self, sequence: SequenceData) -> None:
        """Set the current sequence."""
        ...
    
    @abstractmethod
    def get_start_position(self) -> Optional[BeatData]:
        """Get the start position data."""
        ...
    
    @abstractmethod
    def set_start_position(self, start_position: BeatData, position_key: str) -> None:
        """Set the start position data."""
        ...
    
    @abstractmethod
    def is_workbench_available(self) -> bool:
        """Check if workbench is available and ready."""
        ...


class WorkbenchStateService(IWorkbenchStateService):
    """
    Concrete implementation of workbench state service.
    
    This service provides a clean, typed interface for accessing workbench state
    instead of passing around getter/setter functions.
    """
    
    def __init__(self):
        self._workbench: Optional[WorkbenchProtocol] = None
        self._sequence_change_callbacks = []
        self._start_position_change_callbacks = []
    
    def set_workbench(self, workbench: WorkbenchProtocol) -> None:
        """Set the workbench instance (dependency injection)."""
        self._workbench = workbench
    
    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence from workbench."""
        if not self._workbench:
            return None
        return self._workbench.get_sequence()
    
    def set_current_sequence(self, sequence: SequenceData) -> None:
        """Set the current sequence in workbench."""
        if not self._workbench:
            raise RuntimeError("Workbench not available")
        
        self._workbench.set_sequence(sequence)
        
        # Notify callbacks
        for callback in self._sequence_change_callbacks:
            callback(sequence)
    
    def get_start_position(self) -> Optional[BeatData]:
        """Get the start position data from workbench."""
        if not self._workbench:
            return None
        return self._workbench.get_start_position_data()
    
    def set_start_position(self, start_position: BeatData, position_key: str) -> None:
        """Set the start position in workbench."""
        if not self._workbench:
            raise RuntimeError("Workbench not available")
        
        self._workbench.set_start_position_data(start_position, position_key)
        
        # Notify callbacks
        for callback in self._start_position_change_callbacks:
            callback(start_position, position_key)
    
    def is_workbench_available(self) -> bool:
        """Check if workbench is available."""
        return self._workbench is not None
    
    def add_sequence_change_callback(self, callback):
        """Add callback for sequence changes."""
        self._sequence_change_callbacks.append(callback)
    
    def add_start_position_change_callback(self, callback):
        """Add callback for start position changes."""
        self._start_position_change_callbacks.append(callback)
    
    def remove_sequence_change_callback(self, callback):
        """Remove sequence change callback."""
        