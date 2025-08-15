"""
Command System Implementation
============================

Provides command pattern with undo/redo support for TKA application.
"""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar('T')

logger = logging.getLogger(__name__)


class ICommand(ABC, Generic[T]):
    """Interface for commands with undo/redo support."""
    
    @property
    @abstractmethod
    def command_id(self) -> str:
        """Unique identifier for this command."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of the command."""
        pass
    
    @abstractmethod
    def can_execute(self) -> bool:
        """Check if command can be executed."""
        pass
    
    @abstractmethod
    def can_undo(self) -> bool:
        """Check if command can be undone."""
        pass
    
    @abstractmethod
    def execute(self) -> T:
        """Execute the command and return result."""
        pass
    
    @abstractmethod
    def undo(self) -> T:
        """Undo the command and return previous state."""
        pass


class CommandProcessor:
    """
    Command processor with undo/redo stack management.
    
    Handles command execution, undo/redo operations, and maintains
    command history for the application.
    """
    
    def __init__(self, event_bus: Any = None):
        """
        Initialize command processor.
        
        Args:
            event_bus: Optional event bus for command notifications
        """
        self.event_bus = event_bus
        self._undo_stack: list[ICommand] = []
        self._redo_stack: list[ICommand] = []
        self._max_history = 100  # Limit history to prevent memory issues
        
        logger.debug("CommandProcessor initialized")
    
    def execute_command(self, command: ICommand[T]) -> T | None:
        """
        Execute a command and add it to the undo stack.
        
        Args:
            command: Command to execute
            
        Returns:
            Result of command execution
        """
        if not command.can_execute():
            logger.warning(f"Command cannot be executed: {command.description}")
            return None
        
        try:
            result = command.execute()
            
            # Add to undo stack if command supports undo
            if command.can_undo():
                self._undo_stack.append(command)
                
                # Limit stack size
                if len(self._undo_stack) > self._max_history:
                    self._undo_stack.pop(0)
                
                # Clear redo stack when new command is executed
                self._redo_stack.clear()
            
            # Emit event if event bus is available
            if self.event_bus and hasattr(self.event_bus, 'emit'):
                try:
                    from desktop.modern.src.core.events.domain_events import CommandExecutedEvent
                    event = CommandExecutedEvent(
                        command_id=command.command_id,
                        description=command.description,
                        result=result
                    )
                    self.event_bus.emit(event)
                except ImportError:
                    pass  # Event system not available
            
            logger.debug(f"Command executed: {command.description}")
            return result
            
        except Exception as e:
            logger.exception(f"Command execution failed: {command.description}: {e}")
            return None
    
    def undo(self) -> Any:
        """
        Undo the last command.
        
        Returns:
            Result of undo operation
        """
        if not self.can_undo():
            logger.warning("No commands to undo")
            return None
        
        command = self._undo_stack.pop()
        
        try:
            result = command.undo()
            self._redo_stack.append(command)
            
            # Emit event if event bus is available
            if self.event_bus and hasattr(self.event_bus, 'emit'):
                try:
                    from desktop.modern.src.core.events.domain_events import CommandUndoneEvent
                    event = CommandUndoneEvent(
                        command_id=command.command_id,
                        description=command.description,
                        result=result
                    )
                    self.event_bus.emit(event)
                except ImportError:
                    pass  # Event system not available
            
            logger.debug(f"Command undone: {command.description}")
            return result
            
        except Exception as e:
            logger.exception(f"Command undo failed: {command.description}: {e}")
            # Put command back on undo stack if undo failed
            self._undo_stack.append(command)
            return None
    
    def redo(self) -> Any:
        """
        Redo the last undone command.
        
        Returns:
            Result of redo operation
        """
        if not self.can_redo():
            logger.warning("No commands to redo")
            return None
        
        command = self._redo_stack.pop()
        
        try:
            result = command.execute()
            self._undo_stack.append(command)
            
            # Emit event if event bus is available
            if self.event_bus and hasattr(self.event_bus, 'emit'):
                try:
                    from desktop.modern.src.core.events.domain_events import CommandRedoneEvent
                    event = CommandRedoneEvent(
                        command_id=command.command_id,
                        description=command.description,
                        result=result
                    )
                    self.event_bus.emit(event)
                except ImportError:
                    pass  # Event system not available
            
            logger.debug(f"Command redone: {command.description}")
            return result
            
        except Exception as e:
            logger.exception(f"Command redo failed: {command.description}: {e}")
            # Put command back on redo stack if redo failed
            self._redo_stack.append(command)
            return None
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return len(self._undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return len(self._redo_stack) > 0
    
    def get_undo_description(self) -> str | None:
        """Get description of the command that would be undone."""
        if self.can_undo():
            return self._undo_stack[-1].description
        return None
    
    def get_redo_description(self) -> str | None:
        """Get description of the command that would be redone."""
        if self.can_redo():
            return self._redo_stack[-1].description
        return None
    
    def clear_history(self) -> None:
        """Clear all command history."""
        self._undo_stack.clear()
        self._redo_stack.clear()
        logger.debug("Command history cleared")
    
    def get_history_info(self) -> dict[str, Any]:
        """Get information about command history."""
        return {
            "undo_count": len(self._undo_stack),
            "redo_count": len(self._redo_stack),
            "can_undo": self.can_undo(),
            "can_redo": self.can_redo(),
            "undo_description": self.get_undo_description(),
            "redo_description": self.get_redo_description(),
        }
