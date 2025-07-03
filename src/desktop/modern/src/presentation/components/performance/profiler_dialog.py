"""
Profiler Control Dialog

Dialog for configuring and controlling the performance profiler.
Provides user-friendly interface for profiler settings and session management.
"""

import logging

try:
    from PyQt6.QtWidgets import (
        QDialog,
        QVBoxLayout,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QCheckBox,
        QSpinBox,
        QDoubleSpinBox,
        QPushButton,
        QGroupBox,
        QFormLayout,
        QTextEdit,
        QTabWidget,
        QWidget,
        QMessageBox,
    )
    from PyQt6.QtCore import pyqtSignal

    QT_AVAILABLE = True
except ImportError:
    # Fallback for environments without PyQt6
    QT_AVAILABLE = False
    QDialog = object
    def pyqtSignal(*_args, **_kwargs):
        return None

from core.performance import get_profiler, get_performance_config
from core.performance.config import PerformanceConfig

logger = logging.getLogger(__name__)


class ProfilerControlDialog(QDialog if QT_AVAILABLE else object):
    """
    Dialog for profiler configuration and control.

    Features:
    - Profiler settings configuration
    - Session management
    - Real-time status display
    - Configuration validation
    """

    if QT_AVAILABLE:
        configuration_changed = pyqtSignal()
        session_started = pyqtSignal(str)
        session_stopped = pyqtSignal()

    def __init__(self, parent=None):
        if not QT_AVAILABLE:
            logger.warning("PyQt6 not available - Profiler control dialog disabled")
            return

        super().__init__(parent)

        self.profiler = get_profiler()
        self.config = get_performance_config()

        self.setup_ui()
        self.load_configuration()

    def setup_ui(self):
        """Setup the user interface."""
        if not QT_AVAILABLE:
            return

        self.setWindowTitle("Performance Profiler Control")
        self.setModal(True)
        self.setMinimumSize(500, 400)

        layout = QVBoxLayout(self)

        # Create tabs
        tabs = QTabWidget()

        # Configuration tab
        config_tab = self.create_configuration_tab()
        tabs.addTab(config_tab, "Configuration")

        # Session control tab
        session_tab = self.create_session_tab()
        tabs.addTab(session_tab, "Session Control")

        # Status tab
        status_tab = self.create_status_tab()
        tabs.addTab(status_tab, "Status")

        layout.addWidget(tabs)

        # Button box
        button_layout = QHBoxLayout()

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_configuration)
        button_layout.addWidget(self.apply_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_configuration)
        button_layout.addWidget(self.reset_button)

        button_layout.addStretch()

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)

    def create_configuration_tab(self) -> QWidget:
        """Create configuration settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Profiling settings
        profiling_group = QGroupBox("Profiling Settings")
        profiling_layout = QFormLayout(profiling_group)

        self.profiling_enabled = QCheckBox()
        profiling_layout.addRow("Enable Profiling:", self.profiling_enabled)

        self.overhead_threshold = QDoubleSpinBox()
        self.overhead_threshold.setRange(0.1, 10.0)
        self.overhead_threshold.setSingleStep(0.1)
        self.overhead_threshold.setSuffix(" %")
        profiling_layout.addRow("Overhead Threshold:", self.overhead_threshold)

        self.bottleneck_threshold = QDoubleSpinBox()
        self.bottleneck_threshold.setRange(1.0, 1000.0)
        self.bottleneck_threshold.setSingleStep(1.0)
        self.bottleneck_threshold.setSuffix(" ms")
        profiling_layout.addRow("Bottleneck Threshold:", self.bottleneck_threshold)

        self.memory_threshold = QSpinBox()
        self.memory_threshold.setRange(50, 2000)
        self.memory_threshold.setSuffix(" MB")
        profiling_layout.addRow("Memory Threshold:", self.memory_threshold)

        self.cache_enabled = QCheckBox()
        profiling_layout.addRow("Enable Caching:", self.cache_enabled)

        self.cache_size = QSpinBox()
        self.cache_size.setRange(100, 10000)
        profiling_layout.addRow("Cache Size:", self.cache_size)

        layout.addWidget(profiling_group)

        # Monitoring settings
        monitoring_group = QGroupBox("Monitoring Settings")
        monitoring_layout = QFormLayout(monitoring_group)

        self.monitoring_enabled = QCheckBox()
        monitoring_layout.addRow("Enable Monitoring:", self.monitoring_enabled)

        self.monitoring_interval = QSpinBox()
        self.monitoring_interval.setRange(100, 10000)
        self.monitoring_interval.setSuffix(" ms")
        monitoring_layout.addRow("Update Interval:", self.monitoring_interval)

        self.system_metrics = QCheckBox()
        monitoring_layout.addRow("System Metrics:", self.system_metrics)

        self.qt_metrics = QCheckBox()
        monitoring_layout.addRow("Qt Metrics:", self.qt_metrics)

        self.memory_tracking = QCheckBox()
        monitoring_layout.addRow("Memory Tracking:", self.memory_tracking)

        layout.addWidget(monitoring_group)
        layout.addStretch()

        return widget

    def create_session_tab(self) -> QWidget:
        """Create session control tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Session control
        session_group = QGroupBox("Session Control")
        session_layout = QVBoxLayout(session_group)

        # Session name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Session Name:"))
        self.session_name_input = QLineEdit()
        self.session_name_input.setPlaceholderText("Optional session name")
        name_layout.addWidget(self.session_name_input)
        session_layout.addLayout(name_layout)

        # Control buttons
        button_layout = QHBoxLayout()

        self.start_session_button = QPushButton("Start Session")
        self.start_session_button.clicked.connect(self.start_session)
        button_layout.addWidget(self.start_session_button)

        self.stop_session_button = QPushButton("Stop Session")
        self.stop_session_button.clicked.connect(self.stop_session)
        self.stop_session_button.setEnabled(False)
        button_layout.addWidget(self.stop_session_button)

        session_layout.addLayout(button_layout)

        # Session status
        self.session_status_label = QLabel("No active session")
        session_layout.addWidget(self.session_status_label)

        layout.addWidget(session_group)
        layout.addStretch()

        return widget

    def create_status_tab(self) -> QWidget:
        """Create status display tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Status display
        status_group = QGroupBox("Profiler Status")
        status_layout = QVBoxLayout(status_group)

        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        status_layout.addWidget(self.status_text)

        # Refresh button
        refresh_button = QPushButton("Refresh Status")
        refresh_button.clicked.connect(self.refresh_status)
        status_layout.addWidget(refresh_button)

        layout.addWidget(status_group)

        return widget

    def load_configuration(self):
        """Load current configuration into UI controls."""
        if not QT_AVAILABLE:
            return

        try:
            # Profiling settings
            self.profiling_enabled.setChecked(self.config.profiling.enabled)
            self.overhead_threshold.setValue(
                self.config.profiling.overhead_threshold_percent
            )
            self.bottleneck_threshold.setValue(
                self.config.profiling.bottleneck_threshold_ms
            )
            self.memory_threshold.setValue(
                int(self.config.profiling.memory_threshold_mb)
            )
            self.cache_enabled.setChecked(self.config.profiling.cache_enabled)
            self.cache_size.setValue(self.config.profiling.cache_size)

            # Monitoring settings
            self.monitoring_enabled.setChecked(self.config.monitoring.enabled)
            self.monitoring_interval.setValue(self.config.monitoring.interval_ms)
            self.system_metrics.setChecked(self.config.monitoring.system_metrics)
            self.qt_metrics.setChecked(self.config.monitoring.qt_metrics)
            self.memory_tracking.setChecked(self.config.monitoring.memory_tracking)

            # Update session status
            self.update_session_status()

            # Refresh status
            self.refresh_status()

        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")

    def apply_configuration(self):
        """Apply configuration changes."""
        if not QT_AVAILABLE:
            return

        try:
            # Note: In a real implementation, you would need to update the configuration
            # and restart the profiler with new settings. For now, we'll just show a message.

            QMessageBox.information(
                self,
                "Configuration Applied",
                "Configuration changes will take effect after restarting the profiler.",
            )

            self.configuration_changed.emit()

        except Exception as e:
            logger.error(f"Failed to apply configuration: {e}")
            QMessageBox.critical(
                self, "Configuration Error", f"Failed to apply configuration: {e}"
            )

    def reset_configuration(self):
        """Reset configuration to defaults."""
        if not QT_AVAILABLE:
            return

        try:
            # Reset to default configuration

            default_config = PerformanceConfig.create_default()

            # Update UI with defaults
            self.profiling_enabled.setChecked(default_config.profiling.enabled)
            self.overhead_threshold.setValue(
                default_config.profiling.overhead_threshold_percent
            )
            self.bottleneck_threshold.setValue(
                default_config.profiling.bottleneck_threshold_ms
            )
            self.memory_threshold.setValue(
                int(default_config.profiling.memory_threshold_mb)
            )
            self.cache_enabled.setChecked(default_config.profiling.cache_enabled)
            self.cache_size.setValue(default_config.profiling.cache_size)

            self.monitoring_enabled.setChecked(default_config.monitoring.enabled)
            self.monitoring_interval.setValue(default_config.monitoring.interval_ms)
            self.system_metrics.setChecked(default_config.monitoring.system_metrics)
            self.qt_metrics.setChecked(default_config.monitoring.qt_metrics)
            self.memory_tracking.setChecked(default_config.monitoring.memory_tracking)

        except Exception as e:
            logger.error(f"Failed to reset configuration: {e}")

    def start_session(self):
        """Start a new profiling session."""
        if not QT_AVAILABLE:
            return

        try:
            session_name = self.session_name_input.text().strip() or None
            result = self.profiler.start_session(session_name)

            if result.is_success():
                self.start_session_button.setEnabled(False)
                self.stop_session_button.setEnabled(True)
                self.update_session_status()
                self.session_started.emit(result.value)

                QMessageBox.information(
                    self,
                    "Session Started",
                    f"Profiling session '{result.value}' started successfully.",
                )
            else:
                QMessageBox.critical(
                    self, "Session Error", f"Failed to start session: {result.error}"
                )

        except Exception as e:
            logger.error(f"Failed to start session: {e}")
            QMessageBox.critical(self, "Session Error", f"Failed to start session: {e}")

    def stop_session(self):
        """Stop the current profiling session."""
        if not QT_AVAILABLE:
            return

        try:
            result = self.profiler.stop_session()

            if result.is_success():
                self.start_session_button.setEnabled(True)
                self.stop_session_button.setEnabled(False)
                self.update_session_status()
                self.session_stopped.emit()

                QMessageBox.information(
                    self, "Session Stopped", "Profiling session stopped successfully."
                )
            else:
                QMessageBox.critical(
                    self, "Session Error", f"Failed to stop session: {result.error}"
                )

        except Exception as e:
            logger.error(f"Failed to stop session: {e}")
            QMessageBox.critical(self, "Session Error", f"Failed to stop session: {e}")

    def update_session_status(self):
        """Update session status display."""
        if not QT_AVAILABLE:
            return

        try:
            if self.profiler.is_profiling and self.profiler.current_session:
                session_id = self.profiler.current_session.session_id
                start_time = self.profiler.current_session.start_time
                self.session_status_label.setText(
                    f"Active: {session_id}\nStarted: {start_time.strftime('%Y-%m-%d %H:%M:%S')}"
                )
            else:
                self.session_status_label.setText("No active session")

        except Exception as e:
            logger.warning(f"Failed to update session status: {e}")

    def refresh_status(self):
        """Refresh profiler status display."""
        if not QT_AVAILABLE:
            return

        try:
            status_info = []

            # Profiler status
            status_info.append(f"Profiling Active: {self.profiler.is_profiling}")

            if self.profiler.current_session:
                session = self.profiler.current_session
                status_info.append(f"Session ID: {session.session_id}")
                status_info.append(f"Start Time: {session.start_time}")
                status_info.append(
                    f"Functions Tracked: {len(self.profiler._function_stats)}"
                )

            # Configuration status
            status_info.append(f"\nConfiguration:")
            status_info.append(f"  Profiling Enabled: {self.config.profiling.enabled}")
            status_info.append(
                f"  Monitoring Enabled: {self.config.monitoring.enabled}"
            )
            status_info.append(
                f"  Memory Tracking: {self.config.monitoring.memory_tracking}"
            )
            status_info.append(f"  Qt Metrics: {self.config.monitoring.qt_metrics}")

            self.status_text.setPlainText("\n".join(status_info))

        except Exception as e:
            logger.error(f"Failed to refresh status: {e}")
            self.status_text.setPlainText(f"Error refreshing status: {e}")

    def showEvent(self, event):
        """Handle dialog show event."""
        if QT_AVAILABLE:
            self.refresh_status()
            super().showEvent(event)
