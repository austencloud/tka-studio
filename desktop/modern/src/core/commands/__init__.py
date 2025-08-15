"""
Command System Module
====================

Provides command pattern implementation for undo/redo functionality
and event-driven architecture.
"""
from __future__ import annotations

try:
    from .command_system import CommandProcessor, ICommand
    
    COMMANDS_AVAILABLE = True
except ImportError:
    COMMANDS_AVAILABLE = False
    CommandProcessor = None
    ICommand = None

__all__ = ["CommandProcessor", "ICommand", "COMMANDS_AVAILABLE"]
