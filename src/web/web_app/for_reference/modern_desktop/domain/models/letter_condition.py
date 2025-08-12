"""
Letter Condition Enum - Legacy Compatible

This module provides the letter condition classifications used by the legacy system
for placement key generation and pictograph validation.
"""

from __future__ import annotations

from enum import Enum


class LetterCondition(Enum):
    """Letter condition classifications from legacy system."""

    PRO = "pro"
    ANTI = "anti"
    DASH = "dash"
    HAS_STATIC = "static"
    ALPHA_ENDING = "alpha_ending"
    BETA_ENDING = "beta_ending"
    GAMMA_ENDING = "gamma_ending"
    ALPHA_STARTING = "alpha_starting"
    BETA_STARTING = "beta_starting"
    GAMMA_STARTING = "gamma_starting"
    FOUR_VARIATIONS = "four_variations"
    EIGHT_VARIATIONS = "eight_variations"
    SIXTEEN_VARIATIONS = "sixteen_variations"
    HYBRID = "hybrid"
    NON_HYBRID = "non_hybrid"
    TYPE1_HYBRID = "type1_hybrids"
    TYPE1_NON_HYBRID = "type1_non_hybrids"
    TYPE1 = "type1"
    TYPE2 = "type2"
    TYPE3 = "type3"
    TYPE4 = "type4"
    TYPE5 = "type5"
    TYPE6 = "type6"
