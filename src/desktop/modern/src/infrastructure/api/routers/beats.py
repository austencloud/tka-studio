"""
Beat Management Router

Handles all beat-related operations including adding, updating, and removing beats.
"""

import logging
from typing import Optional

from application.services.core.sequence_management_service import (
    SequenceManagementService,
)
from core.commands import CommandProcessor
from core.monitoring import monitor_performance
from fastapi import APIRouter, Depends, HTTPException

from ..converters.beat_converters import api_to_domain_beat, domain_to_api_beat
from ..dependencies import get_command_processor, get_sequence_service
from ..models import BeatAPI, CommandResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Beats"])


@router.post("/sequences/{sequence_id}/beats", response_model=CommandResponse)
@monitor_performance("api_add_beat")
async def add_beat(
    sequence_id: str,
    beat: BeatAPI,
    position: int,
    command_processor: CommandProcessor = Depends(get_command_processor),
    sequence_service: SequenceManagementService = Depends(get_sequence_service),
):
    """Add a beat to a sequence at the specified position."""
    try:
        # Convert API beat to domain beat
        domain_beat = api_to_domain_beat(beat)

        # Get current sequence
        current_sequence = sequence_service.get_sequence_by_id(sequence_id)
        if not current_sequence:
            raise HTTPException(
                status_code=404, detail=f"Sequence {sequence_id} not found"
            )

        # Add beat using command processor for undo support
        updated_sequence = sequence_service.add_beat(
            current_sequence, domain_beat, position
        )

        # Save updated sequence
        sequence_service.save_sequence(updated_sequence)

        logger.info(f"Added beat to sequence {sequence_id} at position {position}")

        return CommandResponse(
            success=True,
            message=f"Beat added to sequence at position {position}",
            command_id=f"add_beat_{sequence_id}_{position}",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to add beat to sequence {sequence_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to add beat")


@router.put("/sequences/{sequence_id}/beats/{beat_id}", response_model=BeatAPI)
@monitor_performance("api_update_beat")
async def update_beat(
    sequence_id: str,
    beat_id: str,
    beat_update: BeatAPI,
    sequence_service: SequenceManagementService = Depends(get_sequence_service),
):
    """Update an existing beat in a sequence."""
    try:
        # Get current sequence
        current_sequence = sequence_service.get_sequence_by_id(sequence_id)
        if not current_sequence:
            raise HTTPException(
                status_code=404, detail=f"Sequence {sequence_id} not found"
            )

        # Find beat by ID
        beat_index = None
        for i, beat in enumerate(current_sequence.beats):
            if beat.id == beat_id:
                beat_index = i
                break

        if beat_index is None:
            raise HTTPException(
                status_code=404, detail=f"Beat {beat_id} not found in sequence"
            )

        # Convert API beat to domain beat
        domain_beat = api_to_domain_beat(beat_update)

        # Update beat in sequence
        new_beats = list(current_sequence.beats)
        new_beats[beat_index] = domain_beat
        updated_sequence = current_sequence.update(beats=new_beats)

        # Save updated sequence
        sequence_service.save_sequence(updated_sequence)

        logger.info(f"Updated beat {beat_id} in sequence {sequence_id}")

        # Return updated beat
        return domain_to_api_beat(domain_beat)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update beat {beat_id} in sequence {sequence_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update beat")


@router.delete(
    "/sequences/{sequence_id}/beats/{beat_id}", response_model=CommandResponse
)
@monitor_performance("api_remove_beat")
async def remove_beat(
    sequence_id: str,
    beat_id: str,
    sequence_service: SequenceManagementService = Depends(get_sequence_service),
):
    """Remove a beat from a sequence."""
    try:
        # Get current sequence
        current_sequence = sequence_service.get_sequence_by_id(sequence_id)
        if not current_sequence:
            raise HTTPException(
                status_code=404, detail=f"Sequence {sequence_id} not found"
            )

        # Find beat by ID
        beat_index = None
        for i, beat in enumerate(current_sequence.beats):
            if beat.id == beat_id:
                beat_index = i
                break

        if beat_index is None:
            raise HTTPException(
                status_code=404, detail=f"Beat {beat_id} not found in sequence"
            )

        # Remove beat from sequence
        updated_sequence = sequence_service.remove_beat(current_sequence, beat_index)

        # Save updated sequence
        sequence_service.save_sequence(updated_sequence)

        logger.info(f"Removed beat {beat_id} from sequence {sequence_id}")

        return CommandResponse(
            success=True,
            message=f"Beat {beat_id} removed from sequence",
            command_id=f"remove_beat_{sequence_id}_{beat_id}",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Failed to remove beat {beat_id} from sequence {sequence_id}: {e}"
        )
        raise HTTPException(status_code=500, detail="Failed to remove beat")
