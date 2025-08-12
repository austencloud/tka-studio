"""
Letter Determination Domain Models

Domain models for letter determination results and comparison contexts.
These provide type-safe, immutable representations of letter determination operations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..enums import Letter


@dataclass(frozen=True)
class LetterDeterminationResult:
    """
    Immutable result of a letter determination operation.

    Provides detailed information about the determination process,
    including confidence, strategy used, and any warnings.
    """

    letter: Letter | None
    confidence: float
    strategy_used: str
    attributes_compared: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate result after initialization."""
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(
                f"Confidence must be between 0.0 and 1.0, got: {self.confidence}"
            )

        if self.letter is not None and self.confidence == 0.0:
            raise ValueError("Cannot have a letter result with zero confidence")

    @property
    def is_successful(self) -> bool:
        """Check if letter determination was successful."""
        return self.letter is not None

    @property
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0

    def with_warning(self, warning: str) -> LetterDeterminationResult:
        """Create a new result with an additional warning."""
        from dataclasses import replace

        new_warnings = [*list(self.warnings), warning]
        return replace(self, warnings=new_warnings)

    @classmethod
    def success(
        cls,
        letter: Letter,
        confidence: float,
        strategy: str,
        attributes: dict[str, Any] | None = None,
    ) -> LetterDeterminationResult:
        """Create a successful determination result."""
        return cls(
            letter=letter,
            confidence=confidence,
            strategy_used=strategy,
            attributes_compared=attributes or {},
            warnings=[],
        )

    @classmethod
    def failure(cls, strategy: str, reason: str | None = None) -> LetterDeterminationResult:
        """Create a failed determination result."""
        warnings = [reason] if reason else []
        return cls(
            letter=None,
            confidence=0.0,
            strategy_used=strategy,
            attributes_compared={},
            warnings=warnings,
        )


@dataclass(frozen=True)
class MotionComparisonContext:
    """
    Context information for motion comparison operations.

    Controls various aspects of how motions are compared,
    including handling of special cases like direction inversion.
    """

    swap_prop_rot_dir: bool = False
    direction_inversion_enabled: bool = True
    prefloat_matching_enabled: bool = True
    strict_orientation_matching: bool = False
    tolerance_threshold: float = 0.001

    def __post_init__(self):
        """Validate context after initialization."""
        if not (0.0 <= self.tolerance_threshold <= 1.0):
            raise ValueError(
                f"Tolerance threshold must be between 0.0 and 1.0, got: {self.tolerance_threshold}"
            )

    @property
    def is_strict_matching(self) -> bool:
        """Check if strict matching mode is enabled."""
        return (
            self.strict_orientation_matching
            and not self.swap_prop_rot_dir
            and self.tolerance_threshold < 0.01
        )

    def with_prop_rot_dir_swap(self, enabled: bool = True) -> MotionComparisonContext:
        """Create context with prop rotation direction swapping."""
        from dataclasses import replace

        return replace(self, swap_prop_rot_dir=enabled)

    def with_strict_matching(self, enabled: bool = True) -> MotionComparisonContext:
        """Create context with strict matching enabled."""
        from dataclasses import replace

        return replace(
            self,
            strict_orientation_matching=enabled,
            prefloat_matching_enabled=not enabled,
            tolerance_threshold=0.0 if enabled else 0.001,
        )

    @classmethod
    def default(cls) -> MotionComparisonContext:
        """Create default comparison context."""
        return cls()

    @classmethod
    def strict(cls) -> MotionComparisonContext:
        """Create strict comparison context."""
        return cls(
            swap_prop_rot_dir=False,
            direction_inversion_enabled=False,
            prefloat_matching_enabled=False,
            strict_orientation_matching=True,
            tolerance_threshold=0.0,
        )

    @classmethod
    def legacy_compatible(cls) -> MotionComparisonContext:
        """Create context that matches legacy system behavior."""
        return cls(
            swap_prop_rot_dir=False,
            direction_inversion_enabled=True,
            prefloat_matching_enabled=True,
            strict_orientation_matching=False,
            tolerance_threshold=0.001,
        )


@dataclass(frozen=True)
class AttributeComparisonResult:
    """
    Result of comparing motion attributes between two pictographs.

    Provides detailed breakdown of which attributes matched and which didn't.
    """

    locations_match: bool
    orientations_match: bool
    motion_types_match: bool
    prop_rot_dirs_match: bool
    prefloat_attributes_match: bool
    overall_match: bool

    # Detailed comparison data
    differences: dict[str, Any] = field(default_factory=dict)
    transformations_applied: list[str] = field(default_factory=list)

    @property
    def match_score(self) -> float:
        """Calculate a match score between 0.0 and 1.0."""
        matches = [
            self.locations_match,
            self.orientations_match,
            self.motion_types_match,
            self.prop_rot_dirs_match,
            self.prefloat_attributes_match,
        ]
        return sum(matches) / len(matches)

    @property
    def has_transformations(self) -> bool:
        """Check if any transformations were applied during comparison."""
        return len(self.transformations_applied) > 0

    def with_transformation(self, transformation: str) -> AttributeComparisonResult:
        """Create result with additional transformation recorded."""
        from dataclasses import replace

        new_transformations = [*list(self.transformations_applied), transformation]
        return replace(self, transformations_applied=new_transformations)

    @classmethod
    def perfect_match(cls) -> AttributeComparisonResult:
        """Create a perfect match result."""
        return cls(
            locations_match=True,
            orientations_match=True,
            motion_types_match=True,
            prop_rot_dirs_match=True,
            prefloat_attributes_match=True,
            overall_match=True,
        )

    @classmethod
    def no_match(cls, differences: dict[str, Any] | None = None) -> AttributeComparisonResult:
        """Create a no match result."""
        return cls(
            locations_match=False,
            orientations_match=False,
            motion_types_match=False,
            prop_rot_dirs_match=False,
            prefloat_attributes_match=False,
            overall_match=False,
            differences=differences or {},
        )
