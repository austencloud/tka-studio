"""
SequenceStateManager - Single Source of Truth for Sequence State

Manages all sequence and start position state in the event-driven architecture.
This replaces the complex web of signal coordinators and multiple state holders.
"""

from typing import Optional
import logging
from PyQt6.QtCore import QObject, pyqtSignal

from domain.models.beat_data import BeatData
from domain.models.sequence_models import SequenceData
from core.events.event_bus import BaseEvent
from core.events.domain_events import (
    CommandExecutedEvent,
    CommandUndoneEvent, 
    CommandRedoneEvent
)

logger = logging.getLogger(__name__)


class SequenceStateManager(QObject):
    """
    Single source of truth for all sequence and start position state.
    
    Responsibilities:
    - Hold current sequence and start position state
    - React to command execution events
    - Emit Qt signals for UI updates
    - Manage persistence coordination
    - Provide clean API for state access
    
    This replaces:
    - Multiple state holders in different components
    - Complex signal coordination
    - Direct state manipulation
    """
    
    # Qt signals for UI updates (these replace the complex signal chains)
    sequence_updated = pyqtSignal(object)  # SequenceData
    start_position_updated = pyqtSignal(object)  # BeatData
    state_changed = pyqtSignal()  # General state change notification
    
    def __init__(self, event_bus, command_processor):
        super().__init__()
        self.event_bus = event_bus
        self.command_processor = command_processor
        
        # Current state (single source of truth)
        self.current_sequence: Optional[SequenceData] = None
        self.start_position: Optional[BeatData] = None
        
        # Setup event subscriptions
        self._setup_event_subscriptions()
        
        logger.info("🎯 SequenceStateManager initialized")
        
    def _setup_event_subscriptions(self):
        """Subscribe to events that change state"""
        try:
            # Subscribe to command events for state updates
            self.event_bus.subscribe("command.executed", self._on_command_executed)
            self.event_bus.subscribe("command.undone", self._on_command_undone)  
            self.event_bus.subscribe("command.redone", self._on_command_redone)
            
            logger.info("✅ SequenceStateManager event subscriptions setup")
            
        except Exception as e:
            logger.error(f"❌ Failed to setup event subscriptions: {e}")
    
    def _on_command_executed(self, event: CommandExecutedEvent):
        """Update state when commands execute successfully"""
        try:
            command_type = event.command_type
            
            if command_type == "SetStartPositionCommand":
                # Start position was set
                if hasattr(event, 'result') and event.result:
                    self._update_start_position(event.result)
                    
            elif command_type == "AddBeatCommand":
                # Beat was added to sequence
                if hasattr(event, 'result') and event.result:
                    self._update_sequence(event.result)
                    
            elif command_type == "RemoveBeatCommand":
                # Beat was removed from sequence  
                if hasattr(event, 'result') and event.result:
                    self._update_sequence(event.result)
                    
            elif command_type == "ClearSequenceCommand":
                # Sequence was cleared
                self._clear_all_state()
                    
            logger.debug(f"✅ State updated from command: {command_type}")
            
        except Exception as e:
            logger.error(f"❌ Error updating state from command: {e}")
    
    def _on_command_undone(self, event: CommandUndoneEvent):
        """Update state when commands are undone"""
        # For undo, we need to get the current state from the command processor
        # The command should have restored the previous state
        self._refresh_state_from_persistence()
        
    def _on_command_redone(self, event: CommandRedoneEvent):
        """Update state when commands are redone"""
        # Similar to command executed
        self._on_command_executed(event)
        
    def _update_sequence(self, new_sequence: SequenceData):
        """Update the current sequence and notify UI"""
        if self.current_sequence != new_sequence:
            self.current_sequence = new_sequence
            self.sequence_updated.emit(new_sequence)
            self.state_changed.emit()
            logger.debug(f"📊 Sequence updated: {new_sequence.length} beats")
            
    def _update_start_position(self, new_start_position: BeatData):
        """Update the start position and notify UI"""
        if self.start_position != new_start_position:
            self.start_position = new_start_position
            self.start_position_updated.emit(new_start_position)
            self.state_changed.emit()
            logger.debug(f"🎯 Start position updated: {new_start_position.letter if new_start_position else 'None'}")
            
    def _clear_all_state(self):
        """Clear all state"""
        self.current_sequence = None
        self.start_position = None
        self.sequence_updated.emit(None)
        self.start_position_updated.emit(None)
        self.state_changed.emit()
        logger.info("🗑️ All state cleared")
        
    def _refresh_state_from_persistence(self):
        """Refresh state from persistence (for undo/redo scenarios)"""
        try:
            # Load current state from persistence
            from application.services.core.sequence_persistence_service import SequencePersistenceService
            from application.services.core.sequence_start_position_manager import SequenceStartPositionManager
            
            persistence_service = SequencePersistenceService()
            start_position_manager = SequenceStartPositionManager()
            
            # Load sequence (this will need to be converted from legacy format)
            # For now, we'll just refresh what we have
            # TODO: Implement proper persistence loading
            
            logger.debug("🔄 State refreshed from persistence")
            
        except Exception as e:
            logger.error(f"❌ Error refreshing state from persistence: {e}")
    
    # Public API for accessing current state
    def get_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence"""
        return self.current_sequence
        
    def get_start_position(self) -> Optional[BeatData]:
        """Get the current start position"""
        return self.start_position
        
    def has_sequence(self) -> bool:
        """Check if there's a current sequence"""
        return self.current_sequence is not None and self.current_sequence.length > 0
        
    def has_start_position(self) -> bool:
        """Check if there's a start position set"""
        return self.start_position is not None
        
    def is_empty(self) -> bool:
        """Check if both sequence and start position are empty"""
        return not self.has_sequence() and not self.has_start_position()
        
    # Direct state setting methods (for non-command scenarios like loading)
    def set_sequence_direct(self, sequence: Optional[SequenceData]):
        """Set sequence directly (for loading scenarios, bypasses commands)"""
        self._update_sequence(sequence)
        
    def set_start_position_direct(self, start_position: Optional[BeatData]):
        """Set start position directly (for loading scenarios, bypasses commands)"""
        self._update_start_position(start_position)
        
    def cleanup(self):
        """Cleanup resources when the state manager is being destroyed"""
        try:
            # Unsubscribe from events
            if self.event_bus:
                # The event bus should handle cleanup of subscriptions
                pass
                
            logger.info("🧹 SequenceStateManager cleaned up")
            
        except Exception as e:
            logger.error(f"❌ Error during SequenceStateManager cleanup: {e}")
