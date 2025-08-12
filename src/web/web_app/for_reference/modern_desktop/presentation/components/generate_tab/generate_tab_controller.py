"""
Generation Tab Controller - Modern Implementation

Coordinates between the GeneratePanel UI and the generation services.
Handles user interactions and manages the generation workflow.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtWidgets import QMessageBox

from desktop.modern.core.interfaces.generation_services import (
    GenerationMode,
    IGenerationService,
    ISequenceConfigurationService,
)
from desktop.modern.domain.models.generation_models import (
    GenerationConfig,
    GenerationResult,
    GenerationState,
)


if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer
    from desktop.modern.presentation.components.generate_tab.generate_panel import (
        GeneratePanel,
    )

logger = logging.getLogger(__name__)


class GenerateTabController(QObject):
    """
    Controller for the Generate Tab.

    Coordinates between the UI and generation services, handling user interactions
    and managing the generation workflow with proper error handling.
    """

    # Signals for communication with other components
    generation_completed = pyqtSignal(GenerationResult)
    config_changed = pyqtSignal(GenerationConfig)
    error_occurred = pyqtSignal(str)

    def __init__(self, container: DIContainer, parent: QObject | None = None):
        super().__init__(parent)
        self.container = container

        # Initialize services
        self._initialize_services()

        # Initialize state
        self._current_state = GenerationState(
            config=self.config_service.get_current_config()
        )

        # UI reference (set later)
        self._generate_panel: GeneratePanel | None = None

        # Timer for UI updates
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._update_ui_state)
        self._update_timer.setSingleShot(True)

    def _initialize_services(self) -> None:
        """Initialize required services from the container."""
        try:
            self.generation_service = self.container.resolve(IGenerationService)
            self.config_service = self.container.resolve(ISequenceConfigurationService)

            logger.info("✅ Generation tab controller services initialized")

        except Exception as e:
            logger.exception(f"❌ Failed to initialize generation services: {e!s}")
            # Create mock services as fallback
            self._create_fallback_services()

    def _create_fallback_services(self) -> None:
        """Create fallback services if dependency injection fails."""
        logger.error("Failed to resolve generation services from DI container")
        raise RuntimeError(
            "Generation services not available - check service registration"
        )

    def set_generate_panel(self, panel: GeneratePanel) -> None:
        """
        Set the generate panel and connect signals.

        Args:
            panel: Generate panel UI component
        """
        self._generate_panel = panel

        # Connect panel signals to controller methods
        panel.generate_requested.connect(self.handle_generate_request)
        panel.auto_complete_requested.connect(self.handle_auto_complete_request)
        panel.config_changed.connect(self.handle_config_change)

        # Set initial panel state
        panel.set_state(self._current_state)

        logger.info("✅ Generate panel connected to controller")

    def handle_generate_request(self, config: GenerationConfig) -> None:
        """
        Handle generation request from the UI.

        Args:
            config: Generation configuration from UI
        """
        try:
            logger.info(
                f"Generation requested: {config.mode.value}, length={config.length}"
            )

            # Update state to show generation in progress
            self._current_state = self._current_state.start_generation()
            self._update_ui_if_available()

            # Perform generation based on mode
            if config.mode == GenerationMode.FREEFORM:
                result = self.generation_service.generate_freeform_sequence(config)
            elif config.mode == GenerationMode.CIRCULAR:
                result = self.generation_service.generate_circular_sequence(config)
            else:
                raise ValueError(f"Unknown generation mode: {config.mode}")

            # Update state with result
            self._current_state = self._current_state.with_result(result)
            self._update_ui_if_available()

            # Emit completion signal
            self.generation_completed.emit(result)

            if result.success:
                logger.info("✅ Generation completed successfully")
                self._show_success_message()
            else:
                logger.error(f"❌ Generation failed: {result.error_message}")
                self._show_error_message(result.error_message)

        except Exception as e:
            logger.error(f"❌ Generation request failed: {e!s}", exc_info=True)

            # Create error result
            error_result = GenerationResult(
                success=False, error_message=f"Generation failed: {e!s}"
            )

            self._current_state = self._current_state.with_result(error_result)
            self._update_ui_if_available()
            self._show_error_message(str(e))
            self.error_occurred.emit(str(e))

    def handle_auto_complete_request(self) -> None:
        """Handle auto-complete request from the UI."""
        try:
            logger.info("Auto-complete requested")

            # Update state to show generation in progress
            self._current_state = self._current_state.start_generation()
            self._update_ui_if_available()

            # Get current sequence (placeholder - would get from sequence manager)
            current_sequence = []  # TODO: Get from sequence manager

            # Perform auto-completion
            result = self.generation_service.auto_complete_sequence(current_sequence)

            # Update state with result
            self._current_state = self._current_state.with_result(result)
            self._update_ui_if_available()

            # Emit completion signal
            self.generation_completed.emit(result)

            if result.success:
                logger.info("✅ Auto-completion completed successfully")
            else:
                logger.error(f"❌ Auto-completion failed: {result.error_message}")
                self._show_error_message(result.error_message)

        except Exception as e:
            logger.error(f"❌ Auto-complete request failed: {e!s}", exc_info=True)
            self._show_error_message(str(e))

    def handle_config_change(self, config: GenerationConfig) -> None:
        """
        Handle configuration change from the UI.

        Args:
            config: Updated configuration
        """
        try:
            # Update configuration service
            config_dict = {
                "mode": config.mode,
                "length": config.length,
                "level": config.level,
                "turn_intensity": config.turn_intensity,
                "grid_mode": config.grid_mode,
                "prop_continuity": config.prop_continuity,
                "letter_types": config.letter_types,
                "slice_size": config.slice_size,
                "cap_type": config.cap_type,
            }

            self.config_service.update_config(config_dict)

            # Update state
            self._current_state = self._current_state.with_config(config)

            # Emit config change signal
            self.config_changed.emit(config)

            logger.debug(f"Configuration updated: {config.mode.value}")

        except Exception as e:
            logger.error(f"❌ Config update failed: {e!s}", exc_info=True)

    def save_config_as_preset(self, name: str) -> None:
        """
        Save current configuration as a preset.

        Args:
            name: Preset name
        """
        try:
            self.config_service.save_config_as_preset(name)
            logger.info(f"✅ Configuration saved as preset: {name}")

        except Exception as e:
            logger.exception(f"❌ Failed to save preset: {e!s}")
            self._show_error_message(f"Failed to save preset: {e!s}")

    def load_config_preset(self, name: str) -> None:
        """
        Load a configuration preset.

        Args:
            name: Preset name
        """
        try:
            config = self.config_service.load_config_preset(name)
            self._current_state = self._current_state.with_config(config)
            self._update_ui_if_available()

            logger.info(f"✅ Configuration preset loaded: {name}")

        except Exception as e:
            logger.exception(f"❌ Failed to load preset: {e!s}")
            self._show_error_message(f"Failed to load preset: {e!s}")

    def get_preset_names(self) -> list[str]:
        """Get list of available preset names."""
        try:
            return self.config_service.get_preset_names()
        except Exception as e:
            logger.exception(f"❌ Failed to get preset names: {e!s}")
            return []

    def _update_ui_if_available(self) -> None:
        """Update UI if panel is available."""
        if self._generate_panel:
            self._generate_panel.set_state(self._current_state)

    def _update_ui_state(self) -> None:
        """Timer callback for UI state updates."""
        self._update_ui_if_available()

    def _show_success_message(self) -> None:
        """Show success message to user."""
        # In a full implementation, this might show a toast notification
        # or update a status bar. For now, we'll just log it.
        logger.info("Generation completed successfully!")

    def _show_error_message(self, message: str) -> None:
        """
        Show error message to user.

        Args:
            message: Error message to display
        """
        if self._generate_panel:
            # Show error dialog
            msg_box = QMessageBox(self._generate_panel)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Generation Error")
            msg_box.setText("Generation failed")
            msg_box.setDetailedText(message)
            msg_box.exec()
