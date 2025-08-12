"""
Music Player Component

Component for music playback controls including play, pause, stop,
and seek functionality for acts.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.core.interfaces.write_services import IWriteTabCoordinator


logger = logging.getLogger(__name__)


class MusicPlayerComponent(QFrame):
    """
    Music player component with playback controls.

    Provides play, pause, stop, and seek functionality for act music.
    """

    play_requested = pyqtSignal()
    pause_requested = pyqtSignal()
    stop_requested = pyqtSignal()
    seek_requested = pyqtSignal(float)  # position in seconds

    def __init__(self, coordinator: IWriteTabCoordinator, parent: QWidget = None):
        super().__init__(parent)

        self.coordinator = coordinator
        self.duration = 0.0
        self.position = 0.0
        self.is_playing = False
        self.is_seeking = False  # Flag to prevent feedback during seeking

        # Timer for updating position
        self.position_timer = QTimer()
        self.position_timer.timeout.connect(self._update_position)
        self.position_timer.setInterval(100)  # Update every 100ms

        self._setup_ui()
        self._setup_styling()
        self._connect_signals()

        # Initially disabled
        self.setEnabled(False)

    def _setup_ui(self):
        """Setup the music player UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(6)

        # Top row: Title and status
        title_layout = QHBoxLayout()

        self.title_label = QLabel("🎵 Music Player")
        self.title_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        title_layout.addWidget(self.title_label)

        title_layout.addStretch()

        self.status_label = QLabel("No music loaded")
        self.status_label.setFont(QFont("Segoe UI", 9))
        title_layout.addWidget(self.status_label)

        layout.addLayout(title_layout)

        # Position slider
        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.setMinimum(0)
        self.position_slider.setMaximum(1000)  # Use 1000 steps for smooth seeking
        self.position_slider.setValue(0)
        self.position_slider.setEnabled(False)
        layout.addWidget(self.position_slider)

        # Time labels and controls
        controls_layout = QHBoxLayout()

        # Time display
        time_layout = QHBoxLayout()
        self.current_time_label = QLabel("0:00")
        self.current_time_label.setFont(QFont("Segoe UI", 9))
        time_layout.addWidget(self.current_time_label)

        time_layout.addWidget(QLabel("/"))

        self.total_time_label = QLabel("0:00")
        self.total_time_label.setFont(QFont("Segoe UI", 9))
        time_layout.addWidget(self.total_time_label)

        controls_layout.addLayout(time_layout)

        controls_layout.addStretch()

        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(4)

        self.play_button = QPushButton("▶")
        self.play_button.setFixedSize(32, 28)
        self.play_button.setFont(QFont("Segoe UI", 10))
        button_layout.addWidget(self.play_button)

        self.pause_button = QPushButton("⏸")
        self.pause_button.setFixedSize(32, 28)
        self.pause_button.setFont(QFont("Segoe UI", 10))
        self.pause_button.setEnabled(False)
        button_layout.addWidget(self.pause_button)

        self.stop_button = QPushButton("⏹")
        self.stop_button.setFixedSize(32, 28)
        self.stop_button.setFont(QFont("Segoe UI", 10))
        button_layout.addWidget(self.stop_button)

        controls_layout.addLayout(button_layout)

        layout.addLayout(controls_layout)

        # Set fixed height
        self.setFixedHeight(85)

    def _setup_styling(self):
        """Setup music player styling."""
        self.setStyleSheet("""
            MusicPlayerComponent {
                background: rgba(40, 40, 50, 0.9);
                border: 1px solid rgba(80, 80, 100, 0.4);
                border-radius: 6px;
            }
            QPushButton {
                background: rgba(70, 130, 180, 0.8);
                border: 1px solid rgba(100, 150, 200, 0.6);
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(80, 140, 190, 0.9);
            }
            QPushButton:pressed {
                background: rgba(60, 120, 170, 0.9);
            }
            QPushButton:disabled {
                background: rgba(60, 60, 70, 0.5);
                border-color: rgba(80, 80, 90, 0.3);
                color: rgba(255, 255, 255, 0.4);
            }
            QSlider::groove:horizontal {
                border: 1px solid rgba(80, 80, 100, 0.5);
                height: 6px;
                background: rgba(60, 60, 70, 0.8);
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: rgba(100, 150, 200, 0.9);
                border: 1px solid rgba(80, 120, 160, 0.8);
                width: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: rgba(120, 170, 220, 0.9);
            }
            QSlider::sub-page:horizontal {
                background: rgba(100, 150, 200, 0.7);
                border-radius: 3px;
            }
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
                border: none;
            }
        """)

    def _connect_signals(self):
        """Connect internal signals."""
        self.play_button.clicked.connect(self._on_play_clicked)
        self.pause_button.clicked.connect(self._on_pause_clicked)
        self.stop_button.clicked.connect(self._on_stop_clicked)

        self.position_slider.sliderPressed.connect(self._on_seek_start)
        self.position_slider.sliderReleased.connect(self._on_seek_end)
        self.position_slider.valueChanged.connect(self._on_slider_moved)

    def _on_play_clicked(self):
        """Handle play button click."""
        self.play_requested.emit()

    def _on_pause_clicked(self):
        """Handle pause button click."""
        self.pause_requested.emit()

    def _on_stop_clicked(self):
        """Handle stop button click."""
        self.stop_requested.emit()

    def _on_seek_start(self):
        """Handle start of seeking."""
        self.is_seeking = True
        self.position_timer.stop()

    def _on_seek_end(self):
        """Handle end of seeking."""
        self.is_seeking = False

        # Calculate seek position
        if self.duration > 0:
            position = (self.position_slider.value() / 1000.0) * self.duration
            self.seek_requested.emit(position)

        # Resume position updates if playing
        if self.is_playing:
            self.position_timer.start()

    def _on_slider_moved(self, value):
        """Handle slider movement during seeking."""
        if self.is_seeking and self.duration > 0:
            # Update time display during seeking
            position = (value / 1000.0) * self.duration
            self.current_time_label.setText(self._format_time(position))

    def set_music_loaded(self, filename: str, duration: float):
        """Set music as loaded with given filename and duration."""
        self.duration = duration
        self.position = 0.0

        self.status_label.setText(f"♪ {filename}")
        self.status_label.setStyleSheet("color: rgba(100, 200, 100, 0.9);")

        self.total_time_label.setText(self._format_time(duration))
        self.current_time_label.setText("0:00")

        self.position_slider.setEnabled(duration > 0)
        self.position_slider.setValue(0)

        self.setEnabled(True)
        self._update_button_states()

        logger.info(f"Music loaded: {filename} (duration: {duration:.1f}s)")

    def set_music_unloaded(self):
        """Set music as unloaded."""
        self.duration = 0.0
        self.position = 0.0
        self.is_playing = False

        self.status_label.setText("No music loaded")
        self.status_label.setStyleSheet("color: rgba(255, 255, 255, 0.6);")

        self.total_time_label.setText("0:00")
        self.current_time_label.setText("0:00")

        self.position_slider.setEnabled(False)
        self.position_slider.setValue(0)

        self.position_timer.stop()
        self.setEnabled(False)

    def set_playing(self, playing: bool):
        """Set playing state."""
        self.is_playing = playing

        if playing:
            self.position_timer.start()
        else:
            self.position_timer.stop()

        self._update_button_states()

    def set_position(self, position: float):
        """Set current playback position."""
        self.position = position

        if not self.is_seeking:
            self.current_time_label.setText(self._format_time(position))

            if self.duration > 0:
                slider_value = int((position / self.duration) * 1000)
                self.position_slider.setValue(slider_value)

    def _update_position(self):
        """Update position from coordinator."""
        try:
            current_pos = self.coordinator.get_music_position()
            self.set_position(current_pos)

            # Check if music is still playing
            if self.is_playing and not self.coordinator.is_music_playing():
                self.set_playing(False)

        except Exception as e:
            logger.exception(f"Failed to update music position: {e}")

    def _update_button_states(self):
        """Update button enable/disable states."""
        has_music = self.duration > 0

        self.play_button.setEnabled(has_music and not self.is_playing)
        self.pause_button.setEnabled(has_music and self.is_playing)
        self.stop_button.setEnabled(has_music)

    def _format_time(self, seconds: float) -> str:
        """Format seconds as MM:SS."""
        seconds = max(seconds, 0)

        minutes = int(seconds // 60)
        seconds = int(seconds % 60)

        return f"{minutes}:{seconds:02d}"
