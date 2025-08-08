"""
Interface definitions for Modern Generate Tab services.

These interfaces define the contracts for generation-related services,
following Modern's dependency injection and clean architecture patterns.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional


if TYPE_CHECKING:
    from desktop.modern.domain.models.generation_models import (
        GenerationConfig,
        GenerationResult,
    )


class GenerationMode(Enum):
    FREEFORM = "freeform"
    CIRCULAR = "circular"


class PropContinuity(Enum):
    CONTINUOUS = "continuous"
    RANDOM = "random"


class LetterType(Enum):
    TYPE1 = "Type1"  # Dual-Shift: A-V
    TYPE2 = "Type2"  # Shift: W,X,Y,Z,Σ,Δ,θ,Ω
    TYPE3 = "Type3"  # Cross-Shift: W-,X-,Y-,Z-,Σ-,Δ-,θ-,Ω-
    TYPE4 = "Type4"  # Dash: Φ,Ψ,Λ
    TYPE5 = "Type5"  # Dual-Dash: Φ-,Ψ-,Λ-
    TYPE6 = "Type6"  # Static: α,β,Γ


class SliceSize(Enum):
    QUARTERED = "quartered"
    HALVED = "halved"


class CAPType(Enum):
    STRICT_ROTATED = "strict_rotated"
    STRICT_MIRRORED = "strict_mirrored"
    STRICT_SWAPPED = "strict_swapped"
    STRICT_COMPLEMENTARY = "strict_complementary"
    SWAPPED_COMPLEMENTARY = "swapped_complementary"
    ROTATED_COMPLEMENTARY = "rotated_complementary"
    MIRRORED_SWAPPED = "mirrored_swapped"
    MIRRORED_COMPLEMENTARY = "mirrored_complementary"
    ROTATED_SWAPPED = "rotated_swapped"
    MIRRORED_ROTATED = "mirrored_rotated"
    MIRRORED_COMPLEMENTARY_ROTATED = "mirrored_complementary_rotated"


@dataclass(frozen=True)
class GenerationMetadata:
    generation_time_ms: int
    algorithm_used: str
    parameters_hash: str
    warnings: Optional[list[str]] = None


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    errors: Optional[list[str]] = None
    warnings: Optional[list[str]] = None
    suggestions: Optional[list[str]] = None


class IGenerationService(ABC):
    @abstractmethod
    def generate_freeform_sequence(self, config: GenerationConfig) -> GenerationResult:
        pass

    @abstractmethod
    def generate_circular_sequence(self, config: GenerationConfig) -> GenerationResult:
        pass

    @abstractmethod
    def auto_complete_sequence(self, current_sequence: Any) -> GenerationResult:
        pass

    @abstractmethod
    def validate_generation_parameters(
        self, config: GenerationConfig
    ) -> ValidationResult:
        pass


class ISequenceConfigurationService(ABC):
    @abstractmethod
    def get_current_config(self) -> GenerationConfig:
        pass

    @abstractmethod
    def update_config(self, updates: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def save_config_as_preset(self, name: str) -> None:
        pass

    @abstractmethod
    def load_config_preset(self, name: str) -> GenerationConfig:
        pass

    @abstractmethod
    def get_default_config(self) -> GenerationConfig:
        pass

    @abstractmethod
    def get_preset_names(self) -> list[str]:
        pass


class IGenerationValidationService(ABC):
    @abstractmethod
    def validate_length(self, length: int, mode: GenerationMode) -> ValidationResult:
        pass

    @abstractmethod
    def validate_level(self, level: int, length: int) -> ValidationResult:
        pass

    @abstractmethod
    def validate_turn_intensity(self, intensity: float, level: int) -> ValidationResult:
        pass

    @abstractmethod
    def validate_letter_combination(
        self, letters: set[LetterType], mode: GenerationMode
    ) -> ValidationResult:
        pass

    @abstractmethod
    def validate_complete_config(self, config: GenerationConfig) -> ValidationResult:
        pass


class IGenerationHistoryService(ABC):
    @abstractmethod
    def record_generation(
        self, config: GenerationConfig, result: GenerationResult
    ) -> None:
        pass

    @abstractmethod
    def get_recent_configs(self, limit: int = 10) -> list[GenerationConfig]:
        pass

    @abstractmethod
    def get_generation_stats(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def clear_history(self) -> None:
        pass


class ITurnIntensityManager(ABC):
    """Interface for turn intensity management operations."""

    @abstractmethod
    def calculate_turn_intensity(self, sequence_data: Any, level: int) -> float:
        """
        Calculate turn intensity for sequence.

        Args:
            sequence_data: Sequence data to analyze
            level: Difficulty level

        Returns:
            Calculated turn intensity value

        Note:
            Web implementation: Client-side turn calculation
        """

    @abstractmethod
    def apply_turn_intensity(self, sequence_data: Any, intensity: float) -> Any:
        """
        Apply turn intensity to sequence.

        Args:
            sequence_data: Sequence to modify
            intensity: Turn intensity to apply

        Returns:
            Modified sequence with applied intensity

        Note:
            Web implementation: Updates sequence turn properties
        """

    @abstractmethod
    def get_intensity_range(self, level: int) -> tuple[float, float]:
        """
        Get valid intensity range for level.

        Args:
            level: Difficulty level

        Returns:
            Tuple of (min_intensity, max_intensity)

        Note:
            Web implementation: Returns level-appropriate ranges
        """

    @abstractmethod
    def validate_intensity(self, intensity: float, level: int) -> bool:
        """
        Validate turn intensity for level.

        Args:
            intensity: Turn intensity to validate
            level: Difficulty level

        Returns:
            True if intensity is valid for level
        """

    @abstractmethod
    def get_recommended_intensity(self, level: int) -> float:
        """
        Get recommended turn intensity for level.

        Args:
            level: Difficulty level

        Returns:
            Recommended turn intensity

        Note:
            Web implementation: Returns level-optimized intensity
        """
