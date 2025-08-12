"""
Sequence Operation Service Interfaces

Interface definitions for sequence operation services following TKA's clean architecture.
These interfaces handle sequence manipulation, validation, and transformation operations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IBeatFactory(ABC):
    """Interface for beat factory operations."""

    @abstractmethod
    def create_beat(self, beat_config: dict[str, Any]) -> Any:
        """
        Create beat from configuration.

        Args:
            beat_config: Configuration dictionary for beat

        Returns:
            Beat object

        Note:
            Web implementation: Creates beat data structure for client-side
        """

    @abstractmethod
    def create_start_position_beat(self, start_position: Any) -> Any:
        """
        Create beat for start position.

        Args:
            start_position: Start position data

        Returns:
            Start position beat object

        Note:
            Web implementation: Creates initial beat state
        """

    @abstractmethod
    def clone_beat(self, beat: Any) -> Any:
        """
        Clone existing beat.

        Args:
            beat: Beat to clone

        Returns:
            Cloned beat object

        Note:
            Web implementation: Deep copy of beat data
        """

    @abstractmethod
    def validate_beat(self, beat: Any) -> tuple[bool, list[str]]:
        """
        Validate beat object.

        Args:
            beat: Beat to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """

    @abstractmethod
    def get_beat_types(self) -> list[str]:
        """
        Get available beat types.

        Returns:
            List of supported beat types

        Note:
            Web implementation: Returns client-side beat type definitions
        """


class ISequenceLoader(ABC):
    """Interface for sequence loading operations."""

    @abstractmethod
    def load_sequence(self, sequence_id: str) -> Any | None:
        """
        Load sequence by ID.

        Args:
            sequence_id: Unique sequence identifier

        Returns:
            Sequence object or None if not found

        Note:
            Web implementation: Loads from server, localStorage, or IndexedDB
        """

    @abstractmethod
    def load_sequence_from_file(self, file_path: str) -> Any | None:
        """
        Load sequence from file.

        Args:
            file_path: Path to sequence file

        Returns:
            Sequence object or None if load failed

        Note:
            Web implementation: Handles File API or drag-and-drop
        """

    @abstractmethod
    def load_sequence_from_data(self, sequence_data: dict[str, Any]) -> Any | None:
        """
        Load sequence from raw data.

        Args:
            sequence_data: Raw sequence data dictionary

        Returns:
            Sequence object or None if invalid data

        Note:
            Web implementation: Validates and constructs sequence client-side
        """

    @abstractmethod
    def validate_sequence_format(self, data: Any) -> tuple[bool, list[str]]:
        """
        Validate sequence data format.

        Args:
            data: Sequence data to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """

    @abstractmethod
    def get_supported_formats(self) -> list[str]:
        """
        Get supported sequence file formats.

        Returns:
            List of supported file extensions

        Note:
            Web implementation: Returns formats supported by browser
        """


class ISequenceBeatOperations(ABC):
    """Interface for sequence beat operation services."""

    @abstractmethod
    def add_beat(self, sequence: Any, beat: Any, position: int | None = None) -> Any:
        """
        Add beat to sequence.

        Args:
            sequence: Sequence to modify
            beat: Beat to add
            position: Optional position to insert at (append if None)

        Returns:
            Modified sequence

        Note:
            Web implementation: Updates sequence state immutably
        """

    @abstractmethod
    def remove_beat(self, sequence: Any, beat_index: int) -> Any:
        """
        Remove beat from sequence.

        Args:
            sequence: Sequence to modify
            beat_index: Index of beat to remove

        Returns:
            Modified sequence

        Note:
            Web implementation: Creates new sequence without specified beat
        """

    @abstractmethod
    def move_beat(self, sequence: Any, from_index: int, to_index: int) -> Any:
        """
        Move beat within sequence.

        Args:
            sequence: Sequence to modify
            from_index: Current position of beat
            to_index: Target position for beat

        Returns:
            Modified sequence

        Note:
            Web implementation: Reorders beats in sequence
        """

    @abstractmethod
    def replace_beat(self, sequence: Any, beat_index: int, new_beat: Any) -> Any:
        """
        Replace beat in sequence.

        Args:
            sequence: Sequence to modify
            beat_index: Index of beat to replace
            new_beat: New beat to insert

        Returns:
            Modified sequence

        Note:
            Web implementation: Updates sequence with new beat
        """

    @abstractmethod
    def duplicate_beat(self, sequence: Any, beat_index: int) -> Any:
        """
        Duplicate beat in sequence.

        Args:
            sequence: Sequence to modify
            beat_index: Index of beat to duplicate

        Returns:
            Modified sequence with duplicated beat

        Note:
            Web implementation: Clones beat and inserts copy
        """

    @abstractmethod
    def swap_beats(self, sequence: Any, index1: int, index2: int) -> Any:
        """
        Swap two beats in sequence.

        Args:
            sequence: Sequence to modify
            index1: Index of first beat
            index2: Index of second beat

        Returns:
            Modified sequence with swapped beats

        Note:
            Web implementation: Exchanges beat positions
        """


class ISequenceDictionaryManager(ABC):
    """Interface for sequence dictionary management operations."""

    @abstractmethod
    def add_sequence_to_dictionary(self, sequence: Any, word: str) -> bool:
        """
        Add sequence to dictionary with word.

        Args:
            sequence: Sequence to add
            word: Word associated with sequence

        Returns:
            True if added successfully

        Note:
            Web implementation: Stores in local dictionary cache
        """

    @abstractmethod
    def get_sequence_by_word(self, word: str) -> Any | None:
        """
        Get sequence by associated word.

        Args:
            word: Word to look up

        Returns:
            Sequence object or None if not found

        Note:
            Web implementation: Retrieves from local dictionary cache
        """

    @abstractmethod
    def get_word_by_sequence(self, sequence: Any) -> str | None:
        """
        Get word associated with sequence.

        Args:
            sequence: Sequence to look up

        Returns:
            Associated word or None if not found

        Note:
            Web implementation: Reverse lookup in dictionary
        """

    @abstractmethod
    def remove_from_dictionary(self, word: str) -> bool:
        """
        Remove entry from dictionary.

        Args:
            word: Word to remove

        Returns:
            True if removed successfully

        Note:
            Web implementation: Removes from local dictionary cache
        """

    @abstractmethod
    def get_dictionary_words(self) -> list[str]:
        """
        Get all words in dictionary.

        Returns:
            List of dictionary words

        Note:
            Web implementation: Returns cached dictionary keys
        """

    @abstractmethod
    def calculate_difficulty(self, sequence: Any) -> int:
        """
        Calculate sequence difficulty level.

        Args:
            sequence: Sequence to analyze

        Returns:
            Difficulty level (1-10)

        Note:
            Web implementation: Client-side difficulty calculation
        """

    @abstractmethod
    def search_dictionary(self, search_term: str) -> list[str]:
        """
        Search dictionary for matching words.

        Args:
            search_term: Term to search for

        Returns:
            List of matching words

        Note:
            Web implementation: Fuzzy search in local dictionary
        """


class ISequenceGenerator(ABC):
    """Interface for sequence generation operations."""

    @abstractmethod
    def generate_random_sequence(
        self, length: int, constraints: dict[str, Any] | None = None
    ) -> Any:
        """
        Generate random sequence.

        Args:
            length: Number of beats in sequence
            constraints: Optional generation constraints

        Returns:
            Generated sequence

        Note:
            Web implementation: Client-side sequence generation
        """

    @abstractmethod
    def generate_variation(self, base_sequence: Any, variation_type: str) -> Any:
        """
        Generate variation of existing sequence.

        Args:
            base_sequence: Base sequence to vary
            variation_type: Type of variation to apply

        Returns:
            Varied sequence

        Note:
            Web implementation: Applies variations client-side
        """

    @abstractmethod
    def generate_from_pattern(self, pattern: str) -> Any:
        """
        Generate sequence from pattern.

        Args:
            pattern: Pattern string to generate from

        Returns:
            Generated sequence

        Note:
            Web implementation: Pattern-based generation
        """

    @abstractmethod
    def get_generation_parameters(self) -> dict[str, Any]:
        """
        Get available generation parameters.

        Returns:
            Dictionary of generation parameters and their constraints

        Note:
            Web implementation: Returns client-side generation options
        """


class ISequenceStartPositionManager(ABC):
    """Interface for sequence start position management operations."""

    @abstractmethod
    def set_start_position(self, sequence: Any, start_position: Any) -> Any:
        """
        Set start position for sequence.

        Args:
            sequence: Sequence to modify
            start_position: Start position data

        Returns:
            Modified sequence with new start position

        Note:
            Web implementation: Updates sequence start state
        """

    @abstractmethod
    def get_start_position(self, sequence: Any) -> Any | None:
        """
        Get start position from sequence.

        Args:
            sequence: Sequence to examine

        Returns:
            Start position data or None if not set

        Note:
            Web implementation: Extracts start position from sequence
        """

    @abstractmethod
    def validate_start_position(
        self, start_position: Any, sequence: Any
    ) -> tuple[bool, list[str]]:
        """
        Validate start position for sequence.

        Args:
            start_position: Start position to validate
            sequence: Sequence context

        Returns:
            Tuple of (is_valid, error_messages)
        """

    @abstractmethod
    def get_available_start_positions(self) -> list[Any]:
        """
        Get available start position options.

        Returns:
            List of available start positions

        Note:
            Web implementation: Returns predefined start position options
        """


class ISequenceTransformer(ABC):
    """Interface for sequence transformation operations."""

    @abstractmethod
    def mirror_sequence(self, sequence: Any, axis: str = "vertical") -> Any:
        """
        Mirror sequence along axis.

        Args:
            sequence: Sequence to mirror
            axis: Mirror axis ("vertical", "horizontal")

        Returns:
            Mirrored sequence

        Note:
            Web implementation: Transforms sequence coordinates
        """

    @abstractmethod
    def rotate_sequence(self, sequence: Any, degrees: float) -> Any:
        """
        Rotate sequence.

        Args:
            sequence: Sequence to rotate
            degrees: Rotation angle in degrees

        Returns:
            Rotated sequence

        Note:
            Web implementation: Applies rotation transformation
        """

    @abstractmethod
    def scale_sequence(self, sequence: Any, scale_factor: float) -> Any:
        """
        Scale sequence.

        Args:
            sequence: Sequence to scale
            scale_factor: Scaling factor

        Returns:
            Scaled sequence

        Note:
            Web implementation: Scales sequence dimensions
        """

    @abstractmethod
    def reverse_sequence(self, sequence: Any) -> Any:
        """
        Reverse sequence order.

        Args:
            sequence: Sequence to reverse

        Returns:
            Reversed sequence

        Note:
            Web implementation: Reverses beat order
        """

    @abstractmethod
    def interpolate_beats(
        self, sequence: Any, start_index: int, end_index: int, num_interpolated: int
    ) -> Any:
        """
        Interpolate beats between two positions.

        Args:
            sequence: Sequence to modify
            start_index: Starting beat index
            end_index: Ending beat index
            num_interpolated: Number of beats to interpolate

        Returns:
            Sequence with interpolated beats

        Note:
            Web implementation: Creates smooth transitions between beats
        """


class ISequenceValidator(ABC):
    """Interface for sequence validation operations."""

    @abstractmethod
    def validate_sequence(self, sequence: Any) -> tuple[bool, list[str]]:
        """
        Validate complete sequence.

        Args:
            sequence: Sequence to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """

    @abstractmethod
    def validate_beat_transitions(self, sequence: Any) -> tuple[bool, list[str]]:
        """
        Validate transitions between beats.

        Args:
            sequence: Sequence to validate

        Returns:
            Tuple of (transitions_valid, error_messages)
        """

    @abstractmethod
    def validate_sequence_consistency(self, sequence: Any) -> tuple[bool, list[str]]:
        """
        Validate sequence internal consistency.

        Args:
            sequence: Sequence to validate

        Returns:
            Tuple of (is_consistent, error_messages)
        """

    @abstractmethod
    def check_sequence_completeness(self, sequence: Any) -> tuple[bool, list[str]]:
        """
        Check if sequence is complete.

        Args:
            sequence: Sequence to check

        Returns:
            Tuple of (is_complete, missing_elements)
        """

    @abstractmethod
    def get_validation_rules(self) -> list[dict[str, Any]]:
        """
        Get available validation rules.

        Returns:
            List of validation rule definitions

        Note:
            Web implementation: Returns client-side validation rules
        """

    @abstractmethod
    def validate_with_custom_rules(
        self, sequence: Any, rules: list[dict[str, Any]]
    ) -> tuple[bool, list[str]]:
        """
        Validate sequence with custom rules.

        Args:
            sequence: Sequence to validate
            rules: Custom validation rules

        Returns:
            Tuple of (is_valid, error_messages)
        """


class IOptionLoader(ABC):
    """Interface for option loading operations."""

    @abstractmethod
    def load_options(self, criteria: dict[str, Any]) -> list[Any]:
        """Load options based on criteria."""

    @abstractmethod
    def get_available_options(self, context: str) -> list[Any]:
        """Get available options for context."""

    @abstractmethod
    def validate_option_criteria(self, criteria: dict[str, Any]) -> bool:
        """Validate option loading criteria."""


class ISequenceOptionService(ABC):
    """Interface for sequence option services."""

    @abstractmethod
    def get_sequence_options(self, sequence_state: Any) -> list[Any]:
        """Get options for sequence state."""

    @abstractmethod
    def filter_options_by_continuity(
        self, options: list[Any], last_beat: Any
    ) -> list[Any]:
        """Filter options to maintain sequence continuity."""

    @abstractmethod
    def validate_option_continuity(self, option: Any, last_beat: Any) -> bool:
        """Validate if option maintains continuity."""


class ISequenceStateTracker(ABC):
    """Interface for sequence state tracking operations."""

    @abstractmethod
    def get_current_sequence(self) -> Any | None:
        """Get current sequence."""

    @abstractmethod
    def set_current_sequence(self, sequence: Any) -> None:
        """Set current sequence."""

    @abstractmethod
    def get_sequence_state(self) -> dict[str, Any]:
        """Get complete sequence state."""

    @abstractmethod
    def track_state_change(self, change_type: str, data: Any) -> None:
        """Track state change."""
