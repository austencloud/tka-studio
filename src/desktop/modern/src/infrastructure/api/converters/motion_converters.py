"""
Motion data converters for TKA API.
Handles conversion between MotionData and MotionAPI models.
"""

import logging
from typing import Optional

from domain.models.core_models import (
    Location,
    MotionData,
    MotionType,
    RotationDirection,
)

from ..models import LocationAPI, MotionAPI, MotionTypeAPI, RotationDirectionAPI

logger = logging.getLogger(__name__)


def domain_to_api_motion(motion: MotionData) -> MotionAPI:
    """
    Convert domain MotionData to API MotionAPI.

    Args:
        motion: Domain motion data to convert

    Returns:
        MotionAPI: Converted API motion model

    Raises:
        ValueError: If motion data is invalid or conversion fails
    """
    try:
        return MotionAPI(
            motion_type=MotionTypeAPI(motion.motion_type.value),
            prop_rot_dir=RotationDirectionAPI(motion.prop_rot_dir.value),
            start_loc=LocationAPI(motion.start_loc.value),
            end_loc=LocationAPI(motion.end_loc.value),
            turns=motion.turns,
            start_ori=motion.start_ori.value if motion.start_ori else "in",
            end_ori=motion.end_ori.value if motion.end_ori else "in",
        )
    except Exception as e:
        logger.error(f"Failed to convert domain motion to API: {e}")
        raise ValueError(f"Invalid motion data for API conversion: {e}")


def api_to_domain_motion(motion: MotionAPI) -> MotionData:
    """
    Convert API MotionAPI to domain MotionData.

    Args:
        motion: API motion data to convert

    Returns:
        MotionData: Converted domain motion model

    Raises:
        ValueError: If API data is invalid or conversion fails
    """
    try:
        return MotionData(
            motion_type=MotionType(motion.motion_type.value),
            prop_rot_dir=RotationDirection(motion.prop_rot_dir.value),
            start_loc=Location(motion.start_loc.value),
            end_loc=Location(motion.end_loc.value),
            turns=motion.turns,
            start_ori=motion.start_ori.value if motion.start_ori else "in",
            end_ori=motion.end_ori.value if motion.end_ori else "in",
        )
    except Exception as e:
        logger.error(f"Failed to convert API motion to domain: {e}")
        raise ValueError(f"Invalid API motion data for domain conversion: {e}")


def validate_motion_data(motion: MotionData) -> bool:
    """
    Validate motion data for consistency.

    Args:
        motion: Motion data to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Basic validation checks
        if motion.turns < 0:
            return False
        if not motion.motion_type or not motion.prop_rot_dir:
            return False
        if not motion.start_loc or not motion.end_loc:
            return False
        return True
    except Exception:
        return False


def validate_api_motion_data(motion: MotionAPI) -> bool:
    """
    Validate API motion data for consistency.

    Args:
        motion: API motion data to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Basic validation checks
        if motion.turns < 0:
            return False
        if not motion.motion_type or not motion.prop_rot_dir:
            return False
        if not motion.start_loc or not motion.end_loc:
            return False
        return True
    except Exception:
        return False
