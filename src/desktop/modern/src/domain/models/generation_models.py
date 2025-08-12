"""
Domain models for Modern Generate Tab.

These immutable data classes represent the core business entities
for sequence generation, following Modern's clean architecture principles.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING


# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from desktop.modern.core.interfaces.generation_services import (
        CAPType,
        GenerationMetadata,
        GenerationMode,
        LetterType,
        PropContinuity,
        SliceSize,
    )


@dataclass(frozen=True)
class GenerationConfig:
    """Immutable configuration for sequence generation"""

    mode: GenerationMode = None
    length: int = 16
    level: int = 1
    turn_intensity: float = 1.0
    prop_continuity: PropContinuity = None
    letter_types: set[LetterType] | None = None
    slice_size: SliceSize = None
    cap_type: CAPType | None = None
    start_position_key: str | None = None

    def __post_init__(self):
        # Set defaults if None
        if self.mode is None:
            object.__setattr__(self, "mode", GenerationMode.FREEFORM)
        if self.prop_continuity is None:
            object.__setattr__(self, "prop_continuity", PropContinuity.CONTINUOUS)
        if self.slice_size is None:
            object.__setattr__(self, "slice_size", SliceSize.HALVED)
        if self.cap_type is None:
            object.__setattr__(self, "cap_type", CAPType.STRICT_ROTATED)
        if self.letter_types is None:
            object.__setattr__(
                self,
                "letter_types",
                {
                    LetterType.TYPE1,
                    LetterType.TYPE2,
                    LetterType.TYPE3,
                    LetterType.TYPE4,
                    LetterType.TYPE5,
                    LetterType.TYPE6,
                },
            )

    def with_updates(self, **kwargs) -> GenerationConfig:
        """Create a new config with updated values"""
        return replace(self, **kwargs)

    def is_valid(self) -> bool:
        """Check if configuration is valid"""
        return (
            4 <= self.length <= 32
            and 1 <= self.level <= 6
            and 0.5 <= self.turn_intensity <= 3.0
            and self.letter_types is not None
            and len(self.letter_types) > 0
        )


@dataclass(frozen=True)
class GenerationResult:
    """Result of a sequence generation operation"""

    success: bool
    sequence_data: list[dict] | None = None
    start_position_data: dict | None = None
    metadata: GenerationMetadata | None = None
    error_message: str | None = None
    warnings: list[str] | None = None

    def __post_init__(self):
        if self.warnings is None:
            object.__setattr__(self, "warnings", [])


@dataclass(frozen=True)
class GenerationState:
    """Current state of the generation UI"""

    config: GenerationConfig
    is_generating: bool = False
    last_result: GenerationResult | None = None
    validation_errors: list[str] | None = None

    def __post_init__(self):
        if self.validation_errors is None:
            object.__setattr__(self, "validation_errors", [])

    def with_config(self, config: GenerationConfig) -> GenerationState:
        """Create new state with updated config"""
        return replace(self, config=config)

    def with_result(self, result: GenerationResult) -> GenerationState:
        """Create new state with generation result"""
        return replace(self, last_result=result, is_generating=False)

    def start_generation(self) -> GenerationState:
        """Create new state marking generation as started"""
        return replace(self, is_generating=True)
