"""
Performance Monitor Widget

Qt widget for real-time performance monitoring and visualization.
Provides live updates of performance metrics, memory usage, and system status.
"""

import logging
from typing import Optional
from datetime import datetime

try:
    from PyQt6.QtWidgets import (
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QLabel,
        QProgressBar,
        QTableWidget,
        QTableWidgetItem,
        QTabWidget,
        QPushButton,
        QTextEdit,
        QGroupBox,
        QGridLayout,
        QFrame,
    )
    from PyQt6.QtCore import QTimer, pyqtSignal

    QT_AVAILABLE = True
except ImportError:
    # Fallback for environments without PyQt6
    QT_AVAILABLE = False
    QWidget = object
    def pyqtSignal(*_args, **_kwargs):
        return None
0
from core.performance import get_profiler, get_qt_profiler, get_memory_tracker
from core.performance.config import get_performance_config

logger = logging.getLogger(__name__)


class PerformanceMonitorWidget(QWidget if QT_AVAILABLE else object):
    """
    Real-time performance monitoring widget.

    Features:
    - Live memory usage display
    - Function performance metrics
    - Qt event monitoring
    - Performance recommendations
    - Session control
    """

    # Signals for communication with parent widgets
    if QT_AVAILABLE:
        session_started = pyqtSignal(str)
        session_stopped = pyqtSignal(str)
        performance_alert = pyqtSignal(str, str)  # type, message

    def __init__(self, parent=None):
        if not QT_AVAILABLE:
            logger.warning("PyQt6 not available - Performance monitor widget disabled")
            return

        super().__init__(parent)

        # Performance components
        self.profiler = get_profiler()
        self.qt_profiler = get_qt_profiler()
        self.memory_tracker = get_memory_tracker()
        self.config = get_performance_config()

        # UI state
        self.current_session_id: Optional[str] = None
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_metrics)

        # Setup UI
        self.setup_ui()

        # Start monitoring
        if self.config.monitoring.enabled:
            self.start_monitoring()

    def setup_ui(self):
        """Setup the user interface."""
        if not QT_AVAILABLE:
            return

        self.setWindowTitle("Performance Monitor")
        self.setMinimumSize(800, 600)

        # Main layout
        layout = QVBoxLayout(self)

        # Control panel
        control_panel = self.create_control_panel()
        layout.addWidget(control_panel)

        # Metrics tabs
        metrics_tabs = self.create_metrics_tabs()
        layout.addWidget(metrics_tabs)

        # Status bar
        status_bar = self.create_status_bar()
        layout.addWidget(status_bar)

    def create_control_panel(self) -> QWidget:
        """Create the control panel for session management."""
        panel = QGroupBox("Session Control")
        layout = QHBoxLayout(panel)

        # Start/Stop buttons
        self.start_button = QPushButton("Start Profiling")
        self.start_button.clicked.connect(self.start_session)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Profiling")
        self.stop_button.clicked.connect(self.stop_session)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        # Session info
        self.session_label = QLabel("No active session")
        layout.addWidget(self.session_label)

        layout.addStretch()

        # Clear data button
        clear_button = QPushButton("Clear Data")
        clear_button.clicked.connect(self.clear_data)
        layout.addWidget(clear_button)

        return panel

    def create_metrics_tabs(self) -> QWidget:
        """Create tabbed interface for different metrics."""
        tabs = QTabWidget()

        # Memory tab
        memory_tab = self.create_memory_tab()
        tabs.addTab(memory_tab, "Memory")

        # Functions tab
        functions_tab = self.create_functions_tab()
        tabs.addTab(functions_tab, "Functions")

        # Qt Events tab
        qt_tab = self.create_qt_tab()
        tabs.addTab(qt_tab, "Qt Events")

        # Recommendations tab
        recommendations_tab = self.create_recommendations_tab()
        tabs.addTab(recommendations_tab, "Recommendations")

        return tabs

    def create_memory_tab(self) -> QWidget:
        """Create memory monitoring tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Memory usage display
        memory_group = QGroupBox("Memory Usage")
        memory_layout = QGridLayout(memory_group)

        # Current memory
        memory_layout.addWidget(QLabel("Current:"), 0, 0)
        self.current_memory_label = QLabel("0 MB")
        memory_layout.addWidget(self.current_memory_label, 0, 1)

        # Memory progress bar
        self.memory_progress = QProgressBar()
        self.memory_progress.setMaximum(int(self.config.profiling.memory_threshold_mb))
        memory_layout.addWidget(self.memory_progress, 1, 0, 1, 2)

        # Peak memory
        memory_layout.addWidget(QLabel("Peak:"), 2, 0)
        self.peak_memory_label = QLabel("0 MB")
        memory_layout.addWidget(self.peak_memory_label, 2, 1)

        layout.addWidget(memory_group)

        # Memory leak detection
        leak_group = QGroupBox("Leak Detection")
        leak_layout = QVBoxLayout(leak_group)

        self.leak_status_label = QLabel("No leaks detected")
        leak_layout.addWidget(self.leak_status_label)

        layout.addWidget(leak_group)
        layout.addStretch()

        return widget

    def create_functions_tab(self) -> QWidget:
        """Create function performance tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Top functions table
        functions_group = QGroupBox("Top Performance Bottlenecks")
        functions_layout = QVBoxLayout(functions_group)

        self.functions_table = QTableWidget()
        self.functions_table.setColumnCount(5)
        self.functions_table.setHorizontalHeaderLabels(
            ["Function", "Calls", "Total Time (ms)", "Avg Time (ms)", "Memory (MB)"]
        )
        functions_layout.addWidget(self.functions_table)

        layout.addWidget(functions_group)

        return widget

    def create_qt_tab(self) -> QWidget:
        """Create Qt events monitoring tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Qt events table
        qt_group = QGroupBox("Qt Event Performance")
        qt_layout = QVBoxLayout(qt_group)

        self.qt_events_table = QTableWidget()
        self.qt_events_table.setColumnCount(4)
        self.qt_events_table.setHorizontalHeaderLabels(
            ["Event Type", "Count", "Total Time (ms)", "Avg Time (ms)"]
        )
        qt_layout.addWidget(self.qt_events_table)

        layout.addWidget(qt_group)

        return widget

    def create_recommendations_tab(self) -> QWidget:
        """Create performance recommendations tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Recommendations display
        recommendations_group = QGroupBox("Performance Recommendations")
        recommendations_layout = QVBoxLayout(recommendations_group)

        self.recommendations_text = QTextEdit()
        self.recommendations_text.setReadOnly(True)
        recommendations_layout.addWidget(self.recommendations_text)

        layout.addWidget(recommendations_group)

        return widget

    def create_status_bar(self) -> QWidget:
        """Create status bar."""
        status_frame = QFrame()
        status_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QHBoxLayout(status_frame)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        layout.addStretch()

        self.update_time_label = QLabel("Last update: Never")
        layout.addWidget(self.update_time_label)

        return status_frame

    def start_session(self):
        """Start a new profiling session."""
        if not QT_AVAILABLE:
            return

        try:
            session_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            result = self.profiler.start_session(session_name)

            if result.is_success():
                self.current_session_id = result.value
                self.start_button.setEnabled(False)
                self.stop_button.setEnabled(True)
                self.session_label.setText(f"Active: {self.current_session_id}")
                self.status_label.setText("Profiling active")

                # Start Qt profiling if available
                if hasattr(self.qt_profiler, "start_profiling"):
                    self.qt_profiler.start_profiling()

                # Start memory tracking
                if hasattr(self.memory_tracker, "start_tracking"):
                    self.memory_tracker.start_tracking()

                self.session_started.emit(self.current_session_id)
                logger.info(f"Started profiling session: {self.current_session_id}")
            else:
                self.status_label.setText(f"Failed to start: {result.error}")
                logger.error(f"Failed to start profiling: {result.error}")

        except Exception as e:
            self.status_label.setText(f"Error: {e}")
            logger.error(f"Error starting session: {e}")

    def stop_session(self):
        """Stop the current profiling session."""
        if not QT_AVAILABLE or not self.current_session_id:
            return

        try:
            result = self.profiler.stop_session()

            if result.is_success():
                self.start_button.setEnabled(True)
                self.stop_button.setEnabled(False)
                self.session_label.setText("No active session")
                self.status_label.setText("Profiling stopped")

                # Stop Qt profiling
                if hasattr(self.qt_profiler, "stop_profiling"):
                    self.qt_profiler.stop_profiling()

                # Stop memory tracking
                if hasattr(self.memory_tracker, "stop_tracking"):
                    self.memory_tracker.stop_tracking()

                self.session_stopped.emit(self.current_session_id)
                logger.info(f"Stopped profiling session: {self.current_session_id}")

                self.current_session_id = None
            else:
                self.status_label.setText(f"Failed to stop: {result.error}")
                logger.error(f"Failed to stop profiling: {result.error}")

        except Exception as e:
            self.status_label.setText(f"Error: {e}")
            logger.error(f"Error stopping session: {e}")

    def clear_data(self):
        """Clear all performance data."""
        if not QT_AVAILABLE:
            return

        try:
            # Clear tables
            self.functions_table.setRowCount(0)
            self.qt_events_table.setRowCount(0)
            self.recommendations_text.clear()

            # Reset labels
            self.current_memory_label.setText("0 MB")
            self.peak_memory_label.setText("0 MB")
            self.memory_progress.setValue(0)
            self.leak_status_label.setText("No leaks detected")

            self.status_label.setText("Data cleared")
            logger.info("Performance data cleared")

        except Exception as e:
            logger.error(f"Error clearing data: {e}")

    def start_monitoring(self):
        """Start real-time monitoring updates."""
        if not QT_AVAILABLE:
            return

        self.update_timer.start(self.config.monitoring.interval_ms)
        logger.info("Started performance monitoring updates")

    def stop_monitoring(self):
        """Stop real-time monitoring updates."""
        if not QT_AVAILABLE:
            return

        self.update_timer.stop()
        logger.info("Stopped performance monitoring updates")

    def update_metrics(self):
        """Update all performance metrics displays."""
        if not QT_AVAILABLE:
            return

        try:
            # Update memory metrics
            self.update_memory_display()

            # Update function metrics
            self.update_functions_display()

            # Update Qt events
            self.update_qt_events_display()

            # Update recommendations
            self.update_recommendations_display()

            # Update timestamp
            self.update_time_label.setText(
                f"Last update: {datetime.now().strftime('%H:%M:%S')}"
            )

        except Exception as e:
            logger.error(f"Error updating metrics: {e}")

    def update_memory_display(self):
        """Update memory usage display."""
        try:
            current_memory = self.memory_tracker.get_current_usage()
            self.current_memory_label.setText(f"{current_memory:.1f} MB")
            self.memory_progress.setValue(int(current_memory))

            # Check for memory threshold
            if current_memory > self.config.profiling.memory_threshold_mb:
                self.current_memory_label.setStyleSheet(
                    "color: red; font-weight: bold;"
                )
                self.performance_alert.emit(
                    "memory", f"Memory usage ({current_memory:.1f}MB) exceeds threshold"
                )
            else:
                self.current_memory_label.setStyleSheet("")

        except Exception as e:
            logger.warning(f"Failed to update memory display: {e}")

    def update_functions_display(self):
        """Update function performance display."""
        try:
            bottlenecks = self.profiler.get_top_bottlenecks(10)

            self.functions_table.setRowCount(len(bottlenecks))
            for i, func_metrics in enumerate(bottlenecks):
                self.functions_table.setItem(i, 0, QTableWidgetItem(func_metrics.name))
                self.functions_table.setItem(
                    i, 1, QTableWidgetItem(str(func_metrics.call_count))
                )
                self.functions_table.setItem(
                    i, 2, QTableWidgetItem(f"{func_metrics.total_time * 1000:.1f}")
                )
                self.functions_table.setItem(
                    i, 3, QTableWidgetItem(f"{func_metrics.avg_time * 1000:.1f}")
                )
                self.functions_table.setItem(
                    i, 4, QTableWidgetItem(f"{func_metrics.memory_total:.1f}")
                )

        except Exception as e:
            logger.warning(f"Failed to update functions display: {e}")

    def update_qt_events_display(self):
        """Update Qt events display."""
        try:
            if hasattr(self.qt_profiler, "event_metrics"):
                events = list(self.qt_profiler.event_metrics.values())

                self.qt_events_table.setRowCount(len(events))
                for i, event_metrics in enumerate(events):
                    self.qt_events_table.setItem(
                        i, 0, QTableWidgetItem(event_metrics.event_type)
                    )
                    self.qt_events_table.setItem(
                        i, 1, QTableWidgetItem(str(event_metrics.count))
                    )
                    self.qt_events_table.setItem(
                        i, 2, QTableWidgetItem(f"{event_metrics.total_time * 1000:.1f}")
                    )
                    self.qt_events_table.setItem(
                        i, 3, QTableWidgetItem(f"{event_metrics.avg_time * 1000:.1f}")
                    )

        except Exception as e:
            logger.warning(f"Failed to update Qt events display: {e}")

    def update_recommendations_display(self):
        """Update performance recommendations display."""
        try:
            recommendations = []

            # Get recommendations from various sources
            if hasattr(self.profiler, "get_performance_summary"):
                summary = self.profiler.get_performance_summary()
                if "optimization_recommendations" in summary:
                    recommendations.extend(summary["optimization_recommendations"])

            # Format recommendations
            text = ""
            for i, rec in enumerate(recommendations[:10], 1):  # Show top 10
                priority = rec.get("priority", "medium").upper()
                text += f"{i}. [{priority}] {rec.get('issue', 'Unknown issue')}\n"
                text += (
                    f"   {rec.get('recommendation', 'No recommendation available')}\n\n"
                )

            if not text:
                text = "No performance issues detected."

            self.recommendations_text.setPlainText(text)

        except Exception as e:
            logger.warning(f"Failed to update recommendations display: {e}")

    def closeEvent(self, event):
        """Handle widget close event."""
        if QT_AVAILABLE:
            self.stop_monitoring()
            if self.current_session_id:
                self.stop_session()
            super().closeEvent(event)
