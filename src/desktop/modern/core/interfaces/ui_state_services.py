"""
UI State Management Service Interfaces

Interface definitions for UI state management services following TKA's clean architecture.
These interfaces define contracts for UI state operations, thumbnail generation,
and state persistence that must work identically across desktop and web platforms.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.enums import LetterType, MotionType
from desktop.modern.domain.models.sequence_data import SequenceData


class UIMode(Enum):
    """UI operation modes."""

    BROWSER = "browser"
    CONSTRUCTOR = "constructor"
    ADVANCED = "advanced"


class IOptionPickerStateManager(ABC):
    """Interface for option picker state management operations."""

    @abstractmethod
    def get_current_options(self) -> dict[str, Any]:
        """
        Get current option picker options.

        Returns:
            Dictionary of current options

        Note:
            Web implementation: Retrieved from component state
        """

    @abstractmethod
    def set_current_options(self, options: dict[str, Any]) -> None:
        """
        Set current option picker options.

        Args:
            options: Options dictionary to set

        Note:
            Web implementation: Updates component state and triggers re-render
        """

    @abstractmethod
    def get_selected_option(self) -> Optional[str]:
        """
        Get currently selected option.

        Returns:
            Selected option key or None if none selected
        """

    @abstractmethod
    def set_selected_option(self, option_key: str) -> None:
        """
        Set currently selected option.

        Args:
            option_key: Option key to select

        Note:
            Web implementation: Updates selection state and UI
        """

    @abstractmethod
    def get_option_visibility(self, option_key: str) -> bool:
        """
        Get visibility state of an option.

        Args:
            option_key: Option key to check

        Returns:
            True if visible, False otherwise
        """

    @abstractmethod
    def set_option_visibility(self, option_key: str, visible: bool) -> None:
        """
        Set visibility state of an option.

        Args:
            option_key: Option key to set visibility for
            visible: Visibility state

        Note:
            Web implementation: Updates display state and re-renders
        """

    @abstractmethod
    def get_option_filters(self) -> dict[str, Any]:
        """
        Get current option filters.

        Returns:
            Dictionary of active filters

        Note:
            Web implementation: Retrieved from filter state
        """

    @abstractmethod
    def set_option_filters(self, filters: dict[str, Any]) -> None:
        """
        Set option filters.

        Args:
            filters: Filters dictionary to apply

        Note:
            Web implementation: Updates filter state and refreshes options
        """

    @abstractmethod
    def reset_to_defaults(self) -> None:
        """
        Reset option picker to default state.

        Note:
            Web implementation: Restores default state and re-renders
        """

    @abstractmethod
    def get_state_snapshot(self) -> dict[str, Any]:
        """
        Get snapshot of current state.

        Returns:
            Dictionary containing complete state

        Note:
            Web implementation: Serializable state for persistence
        """

    @abstractmethod
    def restore_state_snapshot(self, snapshot: dict[str, Any]) -> None:
        """
        Restore state from snapshot.

        Args:
            snapshot: State snapshot to restore

        Note:
            Web implementation: Restores state and re-renders
        """


class IThumbnailGenerator(ABC):
    """Interface for thumbnail generation operations."""

    @abstractmethod
    def generate_beat_thumbnail(
        self, beat_data: BeatData, size: tuple[int, int]
    ) -> bytes:
        """
        Generate thumbnail image for beat data.

        Args:
            beat_data: Beat data to generate thumbnail for
            size: Thumbnail size (width, height)

        Returns:
            Thumbnail image as bytes

        Note:
            Web implementation: Uses Canvas API or WebGL for rendering
        """

    @abstractmethod
    def generate_sequence_thumbnail(
        self, sequence: SequenceData, size: tuple[int, int]
    ) -> bytes:
        """
        Generate thumbnail image for sequence data.

        Args:
            sequence: Sequence data to generate thumbnail for
            size: Thumbnail size (width, height)

        Returns:
            Thumbnail image as bytes

        Note:
            Web implementation: Uses Canvas API for sequence overview
        """

    @abstractmethod
    def generate_motion_thumbnail(
        self, motion_type: MotionType, size: tuple[int, int]
    ) -> bytes:
        """
        Generate thumbnail for motion type.

        Args:
            motion_type: Motion type to generate thumbnail for
            size: Thumbnail size (width, height)

        Returns:
            Thumbnail image as bytes

        Note:
            Web implementation: Uses Canvas API or SVG rendering
        """

    @abstractmethod
    def generate_letter_thumbnail(
        self, letter_type: LetterType, size: tuple[int, int]
    ) -> bytes:
        """
        Generate thumbnail for letter type.

        Args:
            letter_type: Letter type to generate thumbnail for
            size: Thumbnail size (width, height)

        Returns:
            Thumbnail image as bytes

        Note:
            Web implementation: Uses Canvas API or SVG rendering
        """

    @abstractmethod
    def get_thumbnail_cache_stats(self) -> dict[str, Any]:
        """
        Get thumbnail cache statistics.

        Returns:
            Dictionary of cache statistics

        Note:
            Web implementation: May use browser storage for caching
        """

    @abstractmethod
    def clear_thumbnail_cache(self) -> None:
        """
        Clear thumbnail cache.

        Note:
            Web implementation: Clears browser storage cache
        """

    @abstractmethod
    def set_thumbnail_quality(self, quality: float) -> None:
        """
        Set thumbnail generation quality.

        Args:
            quality: Quality value (0.0 to 1.0)

        Note:
            Web implementation: Affects Canvas rendering quality
        """


class IMainWindowStateManager(ABC):
    """Interface for main window state management operations."""

    @abstractmethod
    def get_window_state(self) -> dict[str, Any]:
        """
        Get current window state.

        Returns:
            Dictionary of window state

        Note:
            Web implementation: Returns viewport and UI state
        """

    @abstractmethod
    def set_window_state(self, state: dict[str, Any]) -> None:
        """
        Set window state.

        Args:
            state: State dictionary to apply

        Note:
            Web implementation: Updates UI layout and viewport
        """

    @abstractmethod
    def get_active_panel(self) -> Optional[str]:
        """
        Get currently active panel.

        Returns:
            Active panel name or None if none active
        """

    @abstractmethod
    def set_active_panel(self, panel_name: str) -> None:
        """
        Set active panel.

        Args:
            panel_name: Panel name to activate

        Note:
            Web implementation: Updates UI to show active panel
        """

    @abstractmethod
    def get_panel_visibility(self, panel_name: str) -> bool:
        """
        Get panel visibility state.

        Args:
            panel_name: Panel name to check

        Returns:
            True if visible, False otherwise
        """

    @abstractmethod
    def set_panel_visibility(self, panel_name: str, visible: bool) -> None:
        """
        Set panel visibility state.

        Args:
            panel_name: Panel name to set visibility for
            visible: Visibility state

        Note:
            Web implementation: Updates UI display state
        """

    @abstractmethod
    def get_ui_mode(self) -> UIMode:
        """
        Get current UI mode.

        Returns:
            Current UI mode
        """

    @abstractmethod
    def set_ui_mode(self, mode: UIMode) -> None:
        """
        Set UI mode.

        Args:
            mode: UI mode to set

        Note:
            Web implementation: Updates UI layout and available controls
        """

    @abstractmethod
    def save_window_layout(self, layout_name: str) -> bool:
        """
        Save current window layout.

        Args:
            layout_name: Name for saved layout

        Returns:
            True if saved successfully, False otherwise

        Note:
            Web implementation: Saves to browser storage
        """

    @abstractmethod
    def load_window_layout(self, layout_name: str) -> bool:
        """
        Load a saved window layout.

        Args:
            layout_name: Name of layout to load

        Returns:
            True if loaded successfully, False otherwise

        Note:
            Web implementation: Loads from browser storage
        """

    @abstractmethod
    def get_available_layouts(self) -> list[str]:
        """
        Get list of available layouts.

        Returns:
            List of layout names

        Note:
            Web implementation: Retrieved from browser storage
        """


class IDialogStateManager(ABC):
    """Interface for dialog state management operations."""

    @abstractmethod
    def show_dialog(
        self, dialog_id: str, data: Optional[dict[str, Any]] = None
    ) -> None:
        """
        Show a dialog.

        Args:
            dialog_id: ID of dialog to show
            data: Optional data to pass to dialog

        Note:
            Web implementation: Shows modal or updates UI state
        """

    @abstractmethod
    def hide_dialog(self, dialog_id: str) -> None:
        """
        Hide a dialog.

        Args:
            dialog_id: ID of dialog to hide

        Note:
            Web implementation: Hides modal or updates UI state
        """

    @abstractmethod
    def is_dialog_visible(self, dialog_id: str) -> bool:
        """
        Check if a dialog is visible.

        Args:
            dialog_id: ID of dialog to check

        Returns:
            True if visible, False otherwise
        """

    @abstractmethod
    def get_dialog_data(self, dialog_id: str) -> Optional[dict[str, Any]]:
        """
        Get data for a dialog.

        Args:
            dialog_id: ID of dialog to get data for

        Returns:
            Dialog data or None if not found
        """

    @abstractmethod
    def set_dialog_data(self, dialog_id: str, data: dict[str, Any]) -> None:
        """
        Set data for a dialog.

        Args:
            dialog_id: ID of dialog to set data for
            data: Data to set

        Note:
            Web implementation: Updates dialog component state
        """

    @abstractmethod
    def get_dialog_result(self, dialog_id: str) -> Optional[Any]:
        """
        Get result from a dialog.

        Args:
            dialog_id: ID of dialog to get result from

        Returns:
            Dialog result or None if no result
        """

    @abstractmethod
    def set_dialog_result(self, dialog_id: str, result: Any) -> None:
        """
        Set result for a dialog.

        Args:
            dialog_id: ID of dialog to set result for
            result: Result to set

        Note:
            Web implementation: Updates dialog state and may trigger callbacks
        """

    @abstractmethod
    def get_active_dialogs(self) -> list[str]:
        """
        Get list of active dialog IDs.

        Returns:
            List of active dialog IDs
        """


class IProgressStateManager(ABC):
    """Interface for progress state management operations."""

    @abstractmethod
    def start_progress(
        self, operation_id: str, total_steps: int, description: str
    ) -> None:
        """
        Start a progress operation.

        Args:
            operation_id: ID for the operation
            total_steps: Total number of steps
            description: Human-readable description

        Note:
            Web implementation: Shows progress UI component
        """

    @abstractmethod
    def update_progress(
        self, operation_id: str, current_step: int, step_description: str = ""
    ) -> None:
        """
        Update progress for an operation.

        Args:
            operation_id: ID of the operation
            current_step: Current step number
            step_description: Optional description of current step

        Note:
            Web implementation: Updates progress UI component
        """

    @abstractmethod
    def complete_progress(self, operation_id: str) -> None:
        """
        Complete a progress operation.

        Args:
            operation_id: ID of the operation

        Note:
            Web implementation: Hides progress UI component
        """

    @abstractmethod
    def cancel_progress(self, operation_id: str) -> None:
        """
        Cancel a progress operation.

        Args:
            operation_id: ID of the operation

        Note:
            Web implementation: Hides progress UI and may trigger cleanup
        """

    @abstractmethod
    def get_progress_status(self, operation_id: str) -> Optional[dict[str, Any]]:
        """
        Get status of a progress operation.

        Args:
            operation_id: ID of the operation

        Returns:
            Progress status dictionary or None if not found
        """

    @abstractmethod
    def get_active_operations(self) -> list[str]:
        """
        Get list of active operation IDs.

        Returns:
            List of active operation IDs
        """
