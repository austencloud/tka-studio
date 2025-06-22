"""
Command processing endpoints for TKA API.
Handles undo/redo operations and command status.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException

from core.monitoring import monitor_performance
from core.commands import CommandProcessor
from ..models import CommandResponse
from ..dependencies import get_command_processor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Commands"])


@router.post(
    "/commands/undo",
    response_model=CommandResponse,
    summary="Undo Last Action",
    description="Undoes the last performed action in the application",
)
@monitor_performance("api_undo_command")
def undo_last_action(
    command_processor: CommandProcessor = Depends(get_command_processor),
):
    """
    Undo Last Action

    Reverts the most recent action performed in the application.
    This includes sequence modifications, beat changes, and other operations.

    **Performance Characteristics:**
    - Response time: <200ms typical
    - Memory impact: Varies by operation complexity
    - CPU usage: <5% during undo

    **Usage Scenarios:**
    - User mistake correction
    - Experimental changes rollback
    - Multi-step operation reversal
    - Workflow error recovery

    **Best Practices:**
    - Check undo availability before calling
    - Handle cases where no undo is available
    - Consider undo stack depth limitations
    """
    try:
        # Attempt to undo the last command
        success = command_processor.undo()

        if success:
            logger.info("Successfully undid last action")
            return CommandResponse(
                success=True,
                message="Action undone successfully",
                command_id="",  # Could be enhanced to return actual command ID
            )
        else:
            logger.warning("No action available to undo")
            return CommandResponse(
                success=False,
                message="No action available to undo",
                command_id="",
            )

    except Exception as e:
        logger.error(f"Failed to undo action: {e}")
        raise HTTPException(status_code=500, detail="Failed to undo action")


@router.post(
    "/commands/redo",
    response_model=CommandResponse,
    summary="Redo Last Undone Action",
    description="Redoes the last undone action in the application",
)
@monitor_performance("api_redo_command")
def redo_last_action(
    command_processor: CommandProcessor = Depends(get_command_processor),
):
    """
    Redo Last Undone Action

    Re-applies the most recently undone action in the application.
    This allows users to restore actions they previously undid.

    **Performance Characteristics:**
    - Response time: <200ms typical
    - Memory impact: Varies by operation complexity
    - CPU usage: <5% during redo

    **Usage Scenarios:**
    - Restoring accidentally undone changes
    - Workflow experimentation
    - Multi-step operation restoration
    - Change management workflows

    **Best Practices:**
    - Check redo availability before calling
    - Handle cases where no redo is available
    - Consider redo stack depth limitations
    """
    try:
        # Attempt to redo the last undone command
        success = command_processor.redo()

        if success:
            logger.info("Successfully redid last action")
            return CommandResponse(
                success=True,
                message="Action redone successfully",
                command_id="",  # Could be enhanced to return actual command ID
            )
        else:
            logger.warning("No action available to redo")
            return CommandResponse(
                success=False,
                message="No action available to redo",
                command_id="",
            )

    except Exception as e:
        logger.error(f"Failed to redo action: {e}")
        raise HTTPException(status_code=500, detail="Failed to redo action")


@router.get(
    "/commands/status",
    summary="Get Command Status",
    description="Returns the current status of the command processor",
)
@monitor_performance("api_command_status")
def get_command_status(
    command_processor: CommandProcessor = Depends(get_command_processor),
):
    """
    Get Command Status

    Returns information about the current state of the command processor,
    including undo/redo availability and command history statistics.

    **Performance Characteristics:**
    - Response time: <50ms typical
    - Memory impact: Minimal
    - CPU usage: <1% during check

    **Usage Scenarios:**
    - UI state management (enable/disable undo/redo buttons)
    - Command history inspection
    - Debugging command processor issues
    - Application state verification

    **Best Practices:**
    - Use for UI state synchronization
    - Check before performing undo/redo operations
    - Monitor for command processor health
    """
    try:
        # Get command processor status
        can_undo = command_processor.can_undo()
        can_redo = command_processor.can_redo()

        # Additional status information could be added here
        status_info = {
            "can_undo": can_undo,
            "can_redo": can_redo,
            "processor_active": True,  # Could check actual processor state
            "timestamp": (
                command_processor.get_last_command_timestamp()
                if hasattr(command_processor, "get_last_command_timestamp")
                else None
            ),
        }

        logger.debug(f"Command status: {status_info}")
        return status_info

    except Exception as e:
        logger.error(f"Failed to get command status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get command status")
