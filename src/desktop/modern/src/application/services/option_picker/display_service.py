"""
Option Picker Display Service

Pure service for handling option picker display management.
Extracted from OptionPicker to follow single responsibility principle.

This service handles:
- Display manager coordination
- Section creation and updates
- Beat display updates
- Section visibility management

Uses dependency injection and follows TKA's clean architecture.
"""

import logging
from typing import List, Dict, Any, Callable
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from core.interfaces.option_picker_services import (
    IOptionPickerDisplayService,
)
from domain.models.core_models import BeatData

logger = logging.getLogger(__name__)


class OptionPickerDisplayService(IOptionPickerDisplayService):
    """
    Pure service for option picker display management.

    Coordinates display operations without any business logic.
    Provides clean interface for display updates.
    """

    def __init__(self):
        """Initialize the display service."""
        self.display_manager: Any = None
        self.sections_container: QWidget = None
        self.sections_layout: QVBoxLayout = None
        self.pool_manager: Any = None
        self.size_provider: Callable = None

    def initialize_display(
        self,
        sections_container: QWidget,
        sections_layout: QVBoxLayout,
        pool_manager: Any,
        size_provider: Callable,
    ) -> None:
        """
        Initialize the display components.

        Args:
            sections_container: Container for sections
            sections_layout: Layout for sections
            pool_manager: Pictograph pool manager
            size_provider: Function to provide size information
        """
        try:
            self.sections_container = sections_container
            self.sections_layout = sections_layout
            self.pool_manager = pool_manager
            self.size_provider = size_provider

            # Create display manager
            from presentation.components.option_picker.services.layout.display_service import (
                OptionPickerDisplayManager,
            )

            self.display_manager = OptionPickerDisplayManager(
                sections_container,
                sections_layout,
                pool_manager,
                size_provider,
            )

            logger.debug("Display service initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing display: {e}")
            raise

    def create_sections(self) -> None:
        """Create display sections for beat options."""
        try:
            if not self.display_manager:
                logger.warning("Display manager not initialized")
                return

            self.display_manager.create_sections()
            logger.debug("Display sections created")

        except Exception as e:
            logger.error(f"Error creating sections: {e}")
            raise

    def update_beat_display(self, beat_options: List[BeatData]) -> None:
        """
        Update the display with new beat options.

        Args:
            beat_options: List of beat data to display
        """
        try:
            if not self.display_manager:
                logger.warning("Display manager not initialized")
                return

            self.display_manager.update_beat_display(beat_options)
            logger.debug(f"Updated beat display with {len(beat_options)} options")

        except Exception as e:
            logger.error(f"Error updating beat display: {e}")

    def ensure_sections_visible(self) -> None:
        """Ensure all sections are visible after updates."""
        try:
            if not self.display_manager:
                logger.warning("Display manager not initialized")
                return

            sections = self.display_manager.get_sections()
            for section in sections.values():
                if hasattr(section, "pictograph_container"):
                    section.pictograph_container.setVisible(True)

            logger.debug("Ensured sections are visible")

        except Exception as e:
            logger.error(f"Error ensuring sections visible: {e}")

    def resize_sections(self) -> None:
        """Resize sections to fit current container."""
        try:
            if not self.display_manager:
                logger.warning("Display manager not initialized")
                return

            # Resize bottom row sections to proper 1/3 width
            if hasattr(self.display_manager, "resize_bottom_row_sections"):
                self.display_manager.resize_bottom_row_sections()

            logger.debug("Resized sections")

        except Exception as e:
            logger.error(f"Error resizing sections: {e}")

    def get_sections(self) -> Dict[str, Any]:
        """
        Get current display sections.

        Returns:
            Dictionary of section name to section widget
        """
        try:
            if not self.display_manager:
                logger.warning("Display manager not initialized")
                return {}

            return self.display_manager.get_sections()

        except Exception as e:
            logger.error(f"Error getting sections: {e}")
            return {}

    def resize_all_frames(self) -> None:
        """Resize all pictograph frames."""
        try:
            if not self.pool_manager:
                logger.warning("Pool manager not available")
                return

            if hasattr(self.pool_manager, "resize_all_frames"):
                self.pool_manager.resize_all_frames()

            logger.debug("Resized all frames")

        except Exception as e:
            logger.error(f"Error resizing frames: {e}")

    def refresh_display(self) -> None:
        """Refresh the entire display."""
        try:
            if not self.display_manager:
                logger.warning("Display manager not initialized")
                return

            # Get current sections and refresh them
            sections = self.get_sections()
            for _, section in sections.items():
                if hasattr(section, "refresh"):
                    section.refresh()

            logger.debug("Refreshed display")

        except Exception as e:
            logger.error(f"Error refreshing display: {e}")

    def clear_display(self) -> None:
        """Clear all displayed content."""
        try:
            if not self.display_manager:
                logger.warning("Display manager not initialized")
                return

            # Clear beat display
            self.update_beat_display([])

            logger.debug("Cleared display")

        except Exception as e:
            logger.error(f"Error clearing display: {e}")

    def get_display_info(self) -> Dict[str, Any]:
        """
        Get information about the current display state.

        Returns:
            Dictionary with display information
        """
        try:
            sections = self.get_sections()

            return {
                "display_manager_initialized": self.display_manager is not None,
                "sections_count": len(sections),
                "section_names": list(sections.keys()),
                "sections_container_available": self.sections_container is not None,
                "sections_layout_available": self.sections_layout is not None,
                "pool_manager_available": self.pool_manager is not None,
                "size_provider_available": self.size_provider is not None,
            }

        except Exception as e:
            logger.error(f"Error getting display info: {e}")
            return {
                "display_manager_initialized": False,
                "sections_count": 0,
                "section_names": [],
                "error": str(e),
            }

    def validate_display_components(self) -> bool:
        """
        Validate that all display components are properly initialized.

        Returns:
            True if all components are valid
        """
        try:
            if not self.display_manager:
                logger.warning("Display manager not initialized")
                return False

            if not self.sections_container:
                logger.warning("Sections container not available")
                return False

            if not self.sections_layout:
                logger.warning("Sections layout not available")
                return False

            if not self.pool_manager:
                logger.warning("Pool manager not available")
                return False

            return True

        except Exception as e:
            logger.error(f"Error validating display components: {e}")
            return False

    def cleanup(self) -> None:
        """Clean up display resources."""
        try:
            if self.display_manager and hasattr(self.display_manager, "cleanup"):
                self.display_manager.cleanup()

            self.display_manager = None
            self.sections_container = None
            self.sections_layout = None
            self.pool_manager = None
            self.size_provider = None

            logger.debug("Display service cleaned up")

        except Exception as e:
            logger.error(f"Error during display cleanup: {e}")

    def set_section_visibility(self, section_name: str, visible: bool) -> None:
        """
        Set visibility of a specific section.

        Args:
            section_name: Name of the section
            visible: Whether section should be visible
        """
        try:
            sections = self.get_sections()
            if section_name in sections:
                section = sections[section_name]
                if hasattr(section, "setVisible"):
                    section.setVisible(visible)
                    logger.debug(f"Set section {section_name} visibility to {visible}")
                else:
                    logger.warning(
                        f"Section {section_name} doesn't support visibility control"
                    )
            else:
                logger.warning(f"Section {section_name} not found")

        except Exception as e:
            logger.error(f"Error setting section visibility: {e}")

    def get_section_count(self) -> int:
        """
        Get the number of display sections.

        Returns:
            Number of sections
        """
        try:
            sections = self.get_sections()
            return len(sections)

        except Exception as e:
            logger.error(f"Error getting section count: {e}")
            return 0
