"""
Beat data converters for TKA API.
Handles conversion between BeatData and BeatAPI models.
"""

import logging
from typing import Optional

from domain.models.core_models import BeatData

from ..models import BeatAPI
from .motion_converters import api_to_domain_motion, domain_to_api_motion

logger = logging.getLogger(__name__)


def domain_to_api_beat(beat: BeatData) -> BeatAPI:
    """
    Convert domain BeatData to API BeatAPI.

    Args:
        beat: Domain beat data to convert

    Returns:
        BeatAPI: Converted API beat model

    Raises:
        ValueError: If beat data is invalid or conversion fails
    """
    try:
        blue_motion = None
        if beat.blue_motion:
            blue_motion = domain_to_api_motion(beat.blue_motion)

        red_motion = None
        if beat.red_motion:
            red_motion = domain_to_api_motion(beat.red_motion)

        return BeatAPI(
            id=beat.id,
            beat_number=beat.beat_number,
            letter=beat.letter,
            duration=beat.duration,
            blue_motion=blue_motion,
            red_motion=red_motion,
            blue_reversal=beat.blue_reversal,
            red_reversal=beat.red_reversal,
            is_blank=beat.is_blank,
            metadata=beat.metadata,
        )
    except Exception as e:
        logger.error(f"Failed to convert domain beat to API: {e}")
        raise ValueError(f"Invalid beat data for API conversion: {e}")


def api_to_domain_beat(api_beat: BeatAPI) -> BeatData:
    """
    Convert API BeatAPI to domain BeatData.

    Args:
        api_beat: API beat data to convert

    Returns:
        BeatData: Converted domain beat model

    Raises:
        ValueError: If API data is invalid or conversion fails
    """
    try:
        blue_motion = None
        if api_beat.blue_motion:
            blue_motion = api_to_domain_motion(api_beat.blue_motion)

        red_motion = None
        if api_beat.red_motion:
            red_motion = api_to_domain_motion(api_beat.red_motion)

        return BeatData(
            id=api_beat.id,
            beat_number=api_beat.beat_number,
            letter=api_beat.letter,
            duration=api_beat.duration,
            blue_motion=blue_motion,
            red_motion=red_motion,
            blue_reversal=api_beat.blue_reversal,
            red_reversal=api_beat.red_reversal,
            is_blank=api_beat.is_blank,
            metadata=api_beat.metadata or {},
        )
    except Exception as e:
        logger.error(f"Failed to convert API beat to domain: {e}")
        raise ValueError(f"Invalid API beat data for domain conversion: {e}")


def validate_beat_data(beat: BeatData) -> bool:
    """
    Validate beat data for consistency.

    Args:
        beat: Beat data to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Basic validation checks
        if beat.beat_number < 1:
            return False
        if beat.duration <= 0:
            return False
        if not beat.letter or len(beat.letter) != 1:
            return False
        if beat.id is None or beat.id == "":
            return False
        return True
    except Exception:
        return False


def validate_api_beat_data(beat: BeatAPI) -> bool:
    """
    Validate API beat data for consistency.

    Args:
        beat: API beat data to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Basic validation checks
        if beat.beat_number < 1:
            return False
        if beat.duration <= 0:
            return False
        if not beat.letter or len(beat.letter) != 1:
            return False
        if beat.id is None or beat.id == "":
            return False
        return True
    except Exception:
        return False
