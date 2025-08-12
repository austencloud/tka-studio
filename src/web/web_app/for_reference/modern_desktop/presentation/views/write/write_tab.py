"""
Write Tab

Modern write tab implementation that combines act browsing, editing,
and music player functionality in a unified interface.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.write_services import ActData, IWriteTabCoordinator
from desktop.modern.presentation.components.write.act_browser_component import (
    ActBrowserComponent,
)
from desktop.modern.presentation.components.write.act_sheet_component import (
    ActSheetComponent,
)
from desktop.modern.presentation.components.write.music_player_component import (
    MusicPlayerComponent,
)


logger = logging.getLogger(__name__)


class WriteTab(QWidget):
    """
    Main write tab for creating and editing acts.

    Provides comprehensive act management including:
    - Browsing existing acts
    - Creating new acts
    - Editing act content (sequences, metadata)
    - Music playback integration
    - Saving and loading functionality
    """

    # Signals for main application
    error_occurred = pyqtSignal(str)
    act_saved = pyqtSignal(str)  # file path

    def __init__(self, container: DIContainer, parent: QWidget = None):
        super().__init__(parent)

        self.container = container
        self.coordinator: Optional[IWriteTabCoordinator] = None

        self._setup_coordinator()
        self._setup_ui()
        self._connect_signals()

        logger.info("Write tab initialized")

    def _setup_coordinator(self):
        """Setup the write tab coordinator."""
        try:
            self.coordinator = self.container.resolve(IWriteTabCoordinator)
            logger.info("Write tab coordinator resolved successfully")
        except Exception as e:
            logger.error(f"Failed to resolve write tab coordinator: {e}")
            self.error_occurred.emit(f"Failed to initialize Write Tab: {e}")

    def _setup_ui(self):
        """Setup the write tab UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Top toolbar
        toolbar_layout = QHBoxLayout()

        self.new_act_button = QPushButton("📄 New Act")
        self.new_act_button.setMinimumHeight(32)
        toolbar_layout.addWidget(self.new_act_button)

        self.save_act_button = QPushButton("💾 Save")
        self.save_act_button.setMinimumHeight(32)
        self.save_act_button.setEnabled(False)
        toolbar_layout.addWidget(self.save_act_button)

        self.save_as_button = QPushButton("💾 Save As...")
        self.save_as_button.setMinimumHeight(32)
        self.save_as_button.setEnabled(False)
        toolbar_layout.addWidget(self.save_as_button)

        toolbar_layout.addStretch()

        layout.addLayout(toolbar_layout)

        # Main content splitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        if self.coordinator:
            # Act browser (left side)
            self.act_browser = ActBrowserComponent(self.coordinator)
            self.act_browser.setMinimumWidth(250)
            main_splitter.addWidget(self.act_browser)

            # Right side container
            right_container = QWidget()
            right_layout = QVBoxLayout(right_container)
            right_layout.setContentsMargins(0, 0, 0, 0)
            right_layout.setSpacing(8)

            # Act sheet (main editing area)
            self.act_sheet = ActSheetComponent(self.coordinator)
            right_layout.addWidget(self.act_sheet, 1)

            # Music player (bottom of right side)
            self.music_player = MusicPlayerComponent(self.coordinator)
            right_layout.addWidget(self.music_player)

            main_splitter.addWidget(right_container)

        else:
            # Error fallback
            self._create_error_fallback(main_splitter)

        # Set splitter proportions (25% browser, 75% editor)
        main_splitter.setSizes([250, 750])
        layout.addWidget(main_splitter, 1)

    def _create_error_fallback(self, parent):
        """Create error fallback UI when coordinator fails."""
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont
        from PyQt6.QtWidgets import QLabel

        error_widget = QWidget()
        error_layout = QVBoxLayout(error_widget)
        error_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        error_label = QLabel(
            "⚠️ Write Tab Error\n\nFailed to initialize write tab services"
        )
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Medium))
        error_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                background: rgba(40, 40, 40, 0.3);
                border: 2px dashed rgba(255, 100, 100, 0.5);
                border-radius: 10px;
                padding: 40px;
                margin: 20px;
            }
        """)

        error_layout.addWidget(error_label)
        parent.addWidget(error_widget)

    def _connect_signals(self):
        """Connect signals between components."""
        if not self.coordinator:
            return

        try:
            # Toolbar signals
            self.new_act_button.clicked.connect(self._on_new_act)
            self.save_act_button.clicked.connect(self._on_save_act)
            self.save_as_button.clicked.connect(self._on_save_as_act)

            # Act browser signals
            self.act_browser.act_selected.connect(self._on_act_selected)

            # Act sheet signals
            self.act_sheet.act_info_changed.connect(self._on_act_info_changed)
            self.act_sheet.music_load_requested.connect(self._on_load_music)
            self.act_sheet.sequence_remove_requested.connect(self._on_remove_sequence)

            # Music player signals
            self.music_player.play_requested.connect(self._on_play_music)
            self.music_player.pause_requested.connect(self._on_pause_music)
            self.music_player.stop_requested.connect(self._on_stop_music)
            self.music_player.seek_requested.connect(self._on_seek_music)

            # Coordinator signals
            signals = self.coordinator.get_signals()
            signals.act_loaded.connect(self._on_act_loaded)
            signals.act_saved.connect(self._on_act_saved_signal)
            signals.act_created.connect(self._on_act_created)
            signals.music_loaded.connect(self._on_music_loaded)
            signals.playback_started.connect(self._on_playback_started)
            signals.playback_paused.connect(self._on_playback_paused)
            signals.playback_stopped.connect(self._on_playback_stopped)

        except Exception as e:
            logger.error(f"Failed to connect write tab signals: {e}")

    def _on_new_act(self):
        """Handle new act creation."""
        try:
            if not self.coordinator:
                return

            # Check if current act has unsaved changes
            if self.coordinator.is_current_act_modified():
                reply = QMessageBox.question(
                    self,
                    "Unsaved Changes",
                    "Current act has unsaved changes. Create new act anyway?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No,
                )
                if reply != QMessageBox.StandardButton.Yes:
                    return

            new_act = self.coordinator.create_new_act()
            self.act_sheet.set_act(new_act)
            self._update_button_states()

            logger.info("Created new act")

        except Exception as e:
            logger.error(f"Failed to create new act: {e}")
            self.error_occurred.emit(f"Failed to create new act: {e}")

    def _on_save_act(self):
        """Handle act saving."""
        try:
            if not self.coordinator:
                return

            success = self.coordinator.save_current_act()
            if not success:
                QMessageBox.warning(
                    self,
                    "Save Failed",
                    "Failed to save the current act. Please try again.",
                )

        except Exception as e:
            logger.error(f"Failed to save act: {e}")
            self.error_occurred.emit(f"Failed to save act: {e}")

    def _on_save_as_act(self):
        """Handle save as functionality."""
        try:
            if not self.coordinator:
                return

            current_act = self.coordinator.get_current_act()
            if not current_act:
                return

            # Get save location from user
            acts_dir = self.coordinator.act_data_service.get_acts_directory()
            default_name = f"{current_act.name}.json"

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Act As",
                str(acts_dir / default_name),
                "Act Files (*.json);;All Files (*)",
            )

            if file_path:
                success = self.coordinator.save_current_act(Path(file_path))
                if not success:
                    QMessageBox.warning(
                        self,
                        "Save Failed",
                        f"Failed to save act to {file_path}. Please try again.",
                    )

        except Exception as e:
            logger.error(f"Failed to save act as: {e}")
            self.error_occurred.emit(f"Failed to save act as: {e}")

    def _on_act_selected(self, file_path: str):
        """Handle act selection from browser."""
        try:
            if not self.coordinator:
                return

            # Check if current act has unsaved changes
            if self.coordinator.is_current_act_modified():
                reply = QMessageBox.question(
                    self,
                    "Unsaved Changes",
                    "Current act has unsaved changes. Load new act anyway?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No,
                )
                if reply != QMessageBox.StandardButton.Yes:
                    return

            success = self.coordinator.load_act_from_file(Path(file_path))
            if not success:
                QMessageBox.warning(
                    self, "Load Failed", f"Failed to load act from {file_path}."
                )

        except Exception as e:
            logger.error(f"Failed to load act: {e}")
            self.error_occurred.emit(f"Failed to load act: {e}")

    def _on_act_info_changed(self, name: str, description: str):
        """Handle act info changes."""
        try:
            if not self.coordinator:
                return

            self.coordinator.update_current_act_info(name, description)
            self._update_button_states()

        except Exception as e:
            logger.error(f"Failed to update act info: {e}")

    def _on_load_music(self):
        """Handle music loading request."""
        try:
            if not self.coordinator:
                return

            # Get music file from user
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Music File",
                "",
                "Audio Files (*.mp3 *.wav *.ogg *.mid *.midi);;All Files (*)",
            )

            if file_path:
                success = self.coordinator.load_music_for_current_act(Path(file_path))
                if not success:
                    QMessageBox.warning(
                        self,
                        "Music Load Failed",
                        f"Failed to load music file: {Path(file_path).name}",
                    )

        except Exception as e:
            logger.error(f"Failed to load music: {e}")
            self.error_occurred.emit(f"Failed to load music: {e}")

    def _on_remove_sequence(self, position: int):
        """Handle sequence removal."""
        try:
            if not self.coordinator:
                return

            reply = QMessageBox.question(
                self,
                "Remove Sequence",
                f"Remove sequence #{position + 1} from the act?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                success = self.coordinator.remove_sequence_from_current_act(position)
                if success:
                    self.act_sheet.refresh_sequences()
                    self._update_button_states()

        except Exception as e:
            logger.error(f"Failed to remove sequence: {e}")

    def _on_play_music(self):
        """Handle music play."""
        try:
            if self.coordinator:
                self.coordinator.play_music()
        except Exception as e:
            logger.error(f"Failed to play music: {e}")

    def _on_pause_music(self):
        """Handle music pause."""
        try:
            if self.coordinator:
                self.coordinator.pause_music()
        except Exception as e:
            logger.error(f"Failed to pause music: {e}")

    def _on_stop_music(self):
        """Handle music stop."""
        try:
            if self.coordinator:
                self.coordinator.stop_music()
        except Exception as e:
            logger.error(f"Failed to stop music: {e}")

    def _on_seek_music(self, position: float):
        """Handle music seek."""
        try:
            if self.coordinator:
                self.coordinator.set_music_position(position)
        except Exception as e:
            logger.error(f"Failed to seek music: {e}")

    def _on_act_loaded(self, act: ActData):
        """Handle act loaded signal."""
        self.act_sheet.set_act(act)
        self._update_button_states()

    def _on_act_saved_signal(self, file_path: str):
        """Handle act saved signal."""
        self.act_saved.emit(file_path)
        self._update_button_states()
        self.act_browser.refresh()  # Refresh browser to show updated act

    def _on_act_created(self, act: ActData):
        """Handle act created signal."""
        self.act_sheet.set_act(act)
        self._update_button_states()

    def _on_music_loaded(self, file_path: str):
        """Handle music loaded signal."""
        try:
            filename = Path(file_path).name
            duration = (
                self.coordinator.get_music_duration() if self.coordinator else 0.0
            )
            self.music_player.set_music_loaded(filename, duration)
        except Exception as e:
            logger.error(f"Failed to handle music loaded signal: {e}")

    def _on_playback_started(self):
        """Handle playback started signal."""
        self.music_player.set_playing(True)

    def _on_playback_paused(self):
        """Handle playback paused signal."""
        self.music_player.set_playing(False)

    def _on_playback_stopped(self):
        """Handle playback stopped signal."""
        self.music_player.set_playing(False)

    def _update_button_states(self):
        """Update toolbar button states."""
        if not self.coordinator:
            return

        has_act = self.coordinator.get_current_act() is not None
        is_modified = self.coordinator.is_current_act_modified()

        self.save_act_button.setEnabled(has_act and is_modified)
        self.save_as_button.setEnabled(has_act)

    def add_sequence_to_current_act(self, sequence_data):
        """
        Add a sequence to the current act.

        This method provides external interface for other tabs
        (like Construct tab) to add sequences to the current act.
        """
        try:
            if not self.coordinator:
                logger.warning("No coordinator available to add sequence")
                return False

            success = self.coordinator.add_sequence_to_current_act(sequence_data)
            if success:
                self.act_sheet.refresh_sequences()
                self._update_button_states()
                logger.info("Successfully added sequence to current act")
                return True
            logger.warning("Failed to add sequence to current act")
            return False

        except Exception as e:
            logger.error(f"Failed to add sequence to current act: {e}")
            return False

    def refresh(self):
        """Refresh the write tab content."""
        try:
            if self.act_browser:
                self.act_browser.refresh()

            if self.coordinator:
                current_act = self.coordinator.get_current_act()
                self.act_sheet.set_act(current_act)

        except Exception as e:
            logger.error(f"Failed to refresh write tab: {e}")

    def cleanup(self):
        """Clean up resources when tab is closed."""
        try:
            if self.coordinator:
                self.coordinator.cleanup()
            logger.info("Write tab cleanup completed")
        except Exception as e:
            logger.error(f"Error during write tab cleanup: {e}")

    def __del__(self):
        """Cleanup when tab is destroyed."""
        self.cleanup()
