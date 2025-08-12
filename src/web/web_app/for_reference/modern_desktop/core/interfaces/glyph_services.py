"""
Glyph Service Interfaces

Interface definitions for glyph-related services following TKA's clean architecture.
These interfaces define contracts for glyph data processing, generation, and management
that must behave identically across desktop and web platforms.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from desktop.modern.domain.models import (
    BeatData,
    ElementalType,
    GlyphData,
    LetterType,
    PictographData,
    VTGMode,
)


class IGlyphDataService(ABC):
    """Interface for glyph data determination and processing operations."""

    @abstractmethod
    def determine_glyph_data(self, beat_data: BeatData) -> GlyphData:
        """
        Determine complete glyph data from beat information.

        Args:
            beat_data: Beat data containing pictograph and motion information

        Returns:
            Complete glyph data with all classifications

        Note:
            Web implementation: Same classification logic, different data structures
        """

    @abstractmethod
    def get_vtg_mode(self, pictograph_data: PictographData) -> VTGMode:
        """
        Determine VTG mode from pictograph data.

        Args:
            pictograph_data: Pictograph data to analyze

        Returns:
            VTG mode (VTG1, VTG2, or VTG3)

        Note:
            Web implementation: Same logic, may use different motion data access
        """

    @abstractmethod
    def get_elemental_type(self, pictograph_data: PictographData) -> ElementalType:
        """
        Determine elemental type from pictograph data.

        Args:
            pictograph_data: Pictograph data to analyze

        Returns:
            Elemental type (Air, Earth, Fire, Water)

        Note:
            Web implementation: Same classification rules across platforms
        """

    @abstractmethod
    def get_letter_type(self, letter: str) -> LetterType:
        """
        Get letter type from letter string.

        Args:
            letter: Letter string (A-Z, Σ, Δ, θ, Ω)

        Returns:
            Letter type (TYPE1, TYPE2, TYPE3)

        Note:
            Web implementation: Static mapping, can be shared configuration
        """

    @abstractmethod
    def get_letter_type_map(self) -> dict[str, LetterType]:
        """
        Get complete mapping from letters to letter types.

        Returns:
            Dictionary mapping letters to their types

        Note:
            Web implementation: Static data, can be shared JSON configuration
        """

    @abstractmethod
    def validate_glyph_data(self, glyph_data: GlyphData) -> bool:
        """
        Validate glyph data consistency.

        Args:
            glyph_data: Glyph data to validate

        Returns:
            True if valid, False otherwise

        Note:
            Web implementation: Same validation rules across platforms
        """

    @abstractmethod
    def get_glyph_characteristics(self, glyph_data: GlyphData) -> dict[str, Any]:
        """
        Get characteristics of a glyph based on its data.

        Args:
            glyph_data: Glyph data to analyze

        Returns:
            Dictionary of glyph characteristics

        Note:
            Web implementation: Same characteristic definitions
        """

    @abstractmethod
    def is_reversible_glyph(self, glyph_data: GlyphData) -> bool:
        """
        Check if a glyph is reversible.

        Args:
            glyph_data: Glyph data to check

        Returns:
            True if reversible, False otherwise

        Note:
            Web implementation: Same reversibility rules
        """

    @abstractmethod
    def get_glyph_complexity_score(self, glyph_data: GlyphData) -> float:
        """
        Calculate complexity score for a glyph.

        Args:
            glyph_data: Glyph data to score

        Returns:
            Complexity score (0.0 to 1.0)

        Note:
            Web implementation: Same scoring algorithm
        """


class IGlyphGenerationService(ABC):
    """Interface for glyph generation operations."""

    @abstractmethod
    def generate_glyph(self, specifications: dict[str, Any]) -> GlyphData:
        """
        Generate a glyph based on specifications.

        Args:
            specifications: Dictionary of glyph specifications

        Returns:
            Generated glyph data

        Note:
            Web implementation: Same generation logic, different randomization
        """

    @abstractmethod
    def generate_glyph_sequence(
        self, length: int, constraints: dict[str, Any]
    ) -> list[GlyphData]:
        """
        Generate a sequence of glyphs with constraints.

        Args:
            length: Length of sequence to generate
            constraints: Dictionary of generation constraints

        Returns:
            List of generated glyph data

        Note:
            Web implementation: Same sequence generation logic
        """

    @abstractmethod
    def validate_glyph_sequence(
        self, glyphs: list[GlyphData]
    ) -> tuple[bool, list[str]]:
        """
        Validate a sequence of glyphs for consistency.

        Args:
            glyphs: List of glyph data to validate

        Returns:
            Tuple of (is_valid, error_messages)

        Note:
            Web implementation: Same validation rules
        """

    @abstractmethod
    def get_generation_constraints(self) -> dict[str, Any]:
        """
        Get available generation constraints.

        Returns:
            Dictionary of constraint definitions

        Note:
            Web implementation: Static constraints, can be shared configuration
        """

    @abstractmethod
    def apply_generation_filter(
        self, glyphs: list[GlyphData], filter_criteria: dict[str, Any]
    ) -> list[GlyphData]:
        """
        Apply filter criteria to a list of glyphs.

        Args:
            glyphs: List of glyph data to filter
            filter_criteria: Dictionary of filter criteria

        Returns:
            Filtered list of glyph data

        Note:
            Web implementation: Same filtering logic
        """

    @abstractmethod
    def get_generation_statistics(self) -> dict[str, Any]:
        """
        Get statistics about generation operations.

        Returns:
            Dictionary of generation statistics

        Note:
            Web implementation: Same statistical calculations
        """


class IGlyphClassificationService(ABC):
    """Interface for glyph classification operations."""

    @abstractmethod
    def classify_by_vtg_mode(
        self, glyphs: list[GlyphData]
    ) -> dict[VTGMode, list[GlyphData]]:
        """
        Classify glyphs by VTG mode.

        Args:
            glyphs: List of glyph data to classify

        Returns:
            Dictionary mapping VTG modes to glyph lists

        Note:
            Web implementation: Same classification logic
        """

    @abstractmethod
    def classify_by_elemental_type(
        self, glyphs: list[GlyphData]
    ) -> dict[ElementalType, list[GlyphData]]:
        """
        Classify glyphs by elemental type.

        Args:
            glyphs: List of glyph data to classify

        Returns:
            Dictionary mapping elemental types to glyph lists

        Note:
            Web implementation: Same classification logic
        """

    @abstractmethod
    def classify_by_letter_type(
        self, glyphs: list[GlyphData]
    ) -> dict[LetterType, list[GlyphData]]:
        """
        Classify glyphs by letter type.

        Args:
            glyphs: List of glyph data to classify

        Returns:
            Dictionary mapping letter types to glyph lists

        Note:
            Web implementation: Same classification logic
        """

    @abstractmethod
    def get_classification_statistics(self, glyphs: list[GlyphData]) -> dict[str, Any]:
        """
        Get classification statistics for a list of glyphs.

        Args:
            glyphs: List of glyph data to analyze

        Returns:
            Dictionary of classification statistics

        Note:
            Web implementation: Same statistical calculations
        """

    @abstractmethod
    def find_similar_glyphs(
        self,
        target_glyph: GlyphData,
        candidates: list[GlyphData],
        threshold: float = 0.8,
    ) -> list[GlyphData]:
        """
        Find glyphs similar to a target glyph.

        Args:
            target_glyph: Target glyph to find similarities for
            candidates: List of candidate glyphs
            threshold: Similarity threshold (0.0 to 1.0)

        Returns:
            List of similar glyphs

        Note:
            Web implementation: Same similarity algorithm
        """

    @abstractmethod
    def calculate_glyph_similarity(self, glyph1: GlyphData, glyph2: GlyphData) -> float:
        """
        Calculate similarity score between two glyphs.

        Args:
            glyph1: First glyph
            glyph2: Second glyph

        Returns:
            Similarity score (0.0 to 1.0)

        Note:
            Web implementation: Same similarity calculation
        """


class IGlyphRenderingService(ABC):
    """Interface for glyph rendering and visualization operations."""

    @abstractmethod
    def render_glyph(self, glyph_data: GlyphData, size: tuple[int, int]) -> Any:
        """
        Render a glyph to a visual representation.

        Args:
            glyph_data: Glyph data to render
            size: Size tuple (width, height)

        Returns:
            Rendered glyph (platform-specific format)

        Note:
            Web implementation: Canvas/SVG rendering instead of PyQt6
        """

    @abstractmethod
    def render_glyph_sequence(
        self, glyphs: list[GlyphData], layout: dict[str, Any]
    ) -> Any:
        """
        Render a sequence of glyphs with layout.

        Args:
            glyphs: List of glyph data to render
            layout: Layout configuration

        Returns:
            Rendered sequence (platform-specific format)

        Note:
            Web implementation: CSS Grid/Flexbox layout instead of PyQt6
        """

    @abstractmethod
    def get_glyph_bounds(self, glyph_data: GlyphData) -> tuple[int, int, int, int]:
        """
        Get bounding box for a glyph.

        Args:
            glyph_data: Glyph data to get bounds for

        Returns:
            Bounding box (x, y, width, height)

        Note:
            Web implementation: getBoundingClientRect() equivalent
        """

    @abstractmethod
    def export_glyph_image(
        self, glyph_data: GlyphData, file_path: str, format: str = "PNG"
    ) -> bool:
        """
        Export glyph as image file.

        Args:
            glyph_data: Glyph data to export
            file_path: Output file path
            format: Image format (PNG, JPEG, etc.)

        Returns:
            True if successful, False otherwise

        Note:
            Web implementation: Blob download instead of direct file writing
        """

    @abstractmethod
    def get_supported_formats(self) -> list[str]:
        """
        Get supported image formats for export.

        Returns:
            List of supported format names

        Note:
            Web implementation: May differ from desktop due to browser support
        """


class IGlyphCacheService(ABC):
    """Interface for glyph caching operations."""

    @abstractmethod
    def cache_glyph(self, key: str, glyph_data: GlyphData) -> None:
        """
        Cache glyph data with a key.

        Args:
            key: Cache key
            glyph_data: Glyph data to cache

        Note:
            Web implementation: IndexedDB or localStorage caching
        """

    @abstractmethod
    def get_cached_glyph(self, key: str) -> Optional[GlyphData]:
        """
        Get cached glyph data by key.

        Args:
            key: Cache key

        Returns:
            Cached glyph data or None if not found

        Note:
            Web implementation: IndexedDB or localStorage retrieval
        """

    @abstractmethod
    def clear_cache(self) -> None:
        """
        Clear all cached glyph data.

        Note:
            Web implementation: Clear IndexedDB or localStorage
        """

    @abstractmethod
    def get_cache_statistics(self) -> dict[str, Any]:
        """
        Get cache usage statistics.

        Returns:
            Dictionary of cache statistics

        Note:
            Web implementation: Storage API quota information
        """

    @abstractmethod
    def is_cached(self, key: str) -> bool:
        """
        Check if glyph is cached.

        Args:
            key: Cache key

        Returns:
            True if cached, False otherwise
        """
