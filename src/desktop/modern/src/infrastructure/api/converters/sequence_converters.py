"""
Sequence data converters for TKA API.
Handles conversion between SequenceData and SequenceAPI models.
"""

import logging
from typing import List

from domain.models.core_models import SequenceData

from ..models import SequenceAPI
from .beat_converters import api_to_domain_beat, domain_to_api_beat

logger = logging.getLogger(__name__)


def domain_to_api_sequence(sequence: SequenceData) -> SequenceAPI:
    """
    Convert domain SequenceData to API SequenceAPI.

    Args:
        sequence: Domain sequence data to convert

    Returns:
        SequenceAPI: Converted API sequence model

    Raises:
        ValueError: If sequence data is invalid or conversion fails
    """
    try:
        api_beats = []
        for beat in sequence.beats:
            api_beat = domain_to_api_beat(beat)
            api_beats.append(api_beat)

        return SequenceAPI(
            id=sequence.id,
            name=sequence.name,
            word=sequence.word,
            beats=api_beats,
            start_position=sequence.start_position,
            metadata=sequence.metadata,
        )
    except Exception as e:
        logger.error(f"Failed to convert domain sequence to API: {e}")
        raise ValueError(f"Invalid sequence data for API conversion: {e}")


def api_to_domain_sequence(api_seq: SequenceAPI) -> SequenceData:
    """
    Convert API SequenceAPI to domain SequenceData.

    Args:
        api_seq: API sequence data to convert

    Returns:
        SequenceData: Converted domain sequence model

    Raises:
        ValueError: If API data is invalid or conversion fails
    """
    try:
        domain_beats = []
        for api_beat in api_seq.beats:
            domain_beat = api_to_domain_beat(api_beat)
            domain_beats.append(domain_beat)

        return SequenceData(
            id=api_seq.id,
            name=api_seq.name,
            word=api_seq.word,
            beats=domain_beats,
            start_position=api_seq.start_position,
            metadata=api_seq.metadata or {},
        )
    except Exception as e:
        logger.error(f"Failed to convert API sequence to domain: {e}")
        raise ValueError(f"Invalid API sequence data for domain conversion: {e}")


def validate_sequence_data(sequence: SequenceData) -> bool:
    """
    Validate sequence data for consistency.

    Args:
        sequence: Sequence data to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Basic validation checks
        if not sequence.id or sequence.id == "":
            return False
        if not sequence.name or sequence.name.strip() == "":
            return False
        if len(sequence.beats) == 0:
            return False

        # Validate beat numbering is sequential
        for i, beat in enumerate(sequence.beats):
            if beat.beat_number != i + 1:
                return False

        return True
    except Exception:
        return False


def validate_api_sequence_data(sequence: SequenceAPI) -> bool:
    """
    Validate API sequence data for consistency.

    Args:
        sequence: API sequence data to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Basic validation checks
        if not sequence.id or sequence.id == "":
            return False
        if not sequence.name or sequence.name.strip() == "":
            return False
        if len(sequence.beats) == 0:
            return False

        # Validate beat numbering is sequential
        for i, beat in enumerate(sequence.beats):
            if beat.beat_number != i + 1:
                return False

        return True
    except Exception:
        return False


def convert_sequence_batch(sequences: List[SequenceData]) -> List[SequenceAPI]:
    """
    Convert a batch of domain sequences to API format.

    Args:
        sequences: List of domain sequences to convert

    Returns:
        List[SequenceAPI]: List of converted API sequences

    Raises:
        ValueError: If any sequence conversion fails
    """
    try:
        api_sequences = []
        for sequence in sequences:
            api_sequence = domain_to_api_sequence(sequence)
            api_sequences.append(api_sequence)
        return api_sequences
    except Exception as e:
        logger.error(f"Failed to convert sequence batch: {e}")
        raise ValueError(f"Batch conversion failed: {e}")
