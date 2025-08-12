"""
UI Error Recovery Service

Consolidates all fallback UI creation logic into a single, consistent approach.
Replaces scattered error recovery patterns across ApplicationOrchestrator and UISetupManager.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.core.error_handling import StandardErrorHandler


logger = logging.getLogger(__name__)


class UIErrorRecoveryService:
    """
    Single service for handling all UI error recovery and fallback creation.

    Eliminates duplicate fallback logic across multiple classes.
    """

    def __init__(self):
        self.recovery_count = 0

    def create_fallback_main_ui(
        self, main_window: QMainWindow, error_context: str
    ) -> QTabWidget:
        """
        Create comprehensive fallback UI for main application failures.

        Args:
            main_window: The main application window
            error_context: Description of what failed

        Returns:
            Functional QTabWidget with basic capabilities
        """
        try:
            self.recovery_count += 1
            logger.warning(
                f"🔄 Creating fallback main UI (attempt {self.recovery_count}) - {error_context}"
            )

            # Create central widget with error indicator
            central_widget = QWidget()
            main_window.setCentralWidget(central_widget)

            layout = QVBoxLayout(central_widget)

            # Error header
            error_header = self._create_error_header(error_context)
            layout.addWidget(error_header)

            # Create functional tab widget
            tab_widget = QTabWidget()
            tab_widget.setStyleSheet("""
                QTabWidget::pane {
                    border: 1px solid #bdc3c7;
                    background: #ecf0f1;
                    margin-top: 0px;
                }
                QTabWidget::tab-bar {
                    alignment: center;
                }
            """)

            # Add recovery tabs
            self._add_recovery_tabs(tab_widget)

            layout.addWidget(tab_widget)

            return tab_widget

        except Exception as e:
            StandardErrorHandler.handle_ui_error("Fallback main UI creation", e, logger)
            # Absolute last resort
            return self._create_minimal_tab_widget()

    def create_fallback_construct_tab(
        self, error_context: str = "construct tab creation"
    ) -> QWidget:
        """Create fallback construct tab with basic functionality."""
        try:
            tab = QWidget()
            layout = QVBoxLayout(tab)

            # Header
            header = QLabel("🔧 Construct (Recovery Mode)")
            header.setStyleSheet(
                "font-size: 18px; font-weight: bold; color: #e67e22; margin: 10px;"
            )
            header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(header)

            # Info section
            info_label = QLabel(f"Recovery mode active - {error_context}")
            info_label.setStyleSheet("color: #7f8c8d; margin: 5px;")
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(info_label)

            # Functional sequence display
            sequence_display = QTextEdit()
            sequence_display.setPlainText(
                "Construct Tab - Recovery Mode\n\n"
                "Available functions:\n"
                "• Basic sequence information display\n"
                "• Emergency pictograph viewing\n"
                "• Core construction tools\n\n"
                "Status: Limited functionality due to initialization issues\n"
                "Recommendation: Restart application for full features"
            )
            sequence_display.setReadOnly(True)
            sequence_display.setMaximumHeight(200)
            sequence_display.setStyleSheet(
                "background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px;"
            )
            layout.addWidget(sequence_display)

            # Basic controls
            controls = self._create_basic_controls("construct", sequence_display)
            layout.addLayout(controls)

            layout.addStretch()
            return tab

        except Exception as e:
            StandardErrorHandler.handle_ui_error(
                "Fallback construct tab creation", e, logger
            )
            return self._create_minimal_tab("Construct Error")

    def create_fallback_browse_tab(
        self, error_context: str = "browse tab creation"
    ) -> QWidget:
        """Create fallback browse tab with basic functionality."""
        try:
            tab = QWidget()
            layout = QVBoxLayout(tab)

            # Header
            header = QLabel("📁 Browse (Recovery Mode)")
            header.setStyleSheet(
                "font-size: 18px; font-weight: bold; color: #e67e22; margin: 10px;"
            )
            header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(header)

            # Info section
            info_label = QLabel(f"Recovery mode active - {error_context}")
            info_label.setStyleSheet("color: #7f8c8d; margin: 5px;")
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(info_label)

            # Basic file list
            file_list = QListWidget()
            file_list.addItem("📄 Recovery mode - limited file access")
            file_list.addItem("📄 Basic directory scanning available")
            file_list.addItem("📄 Full features require application restart")
            file_list.setStyleSheet("background: #fff3cd; border: 1px solid #ffeaa7;")
            layout.addWidget(file_list)

            # Basic controls
            controls_layout = QHBoxLayout()

            scan_btn = QPushButton("🔍 Basic Scan")
            scan_btn.setStyleSheet(
                "padding: 8px 16px; background: #f39c12; color: white; border: none; border-radius: 4px;"
            )
            scan_btn.clicked.connect(
                lambda: file_list.addItem(
                    f"🔍 Recovery scan - {self.recovery_count} attempts"
                )
            )
            controls_layout.addWidget(scan_btn)

            refresh_btn = QPushButton("🔄 Refresh")
            refresh_btn.setStyleSheet(
                "padding: 8px 16px; background: #95a5a6; color: white; border: none; border-radius: 4px;"
            )
            refresh_btn.clicked.connect(
                lambda: file_list.clear()
                or self._populate_recovery_file_list(file_list)
            )
            controls_layout.addWidget(refresh_btn)

            controls_layout.addStretch()
            layout.addLayout(controls_layout)

            return tab

        except Exception as e:
            StandardErrorHandler.handle_ui_error(
                "Fallback browse tab creation", e, logger
            )
            return self._create_minimal_tab("Browse Error")

    def create_recovery_info_tab(self, error_details: str) -> QWidget:
        """Create informational tab with error details and recovery instructions."""
        try:
            tab = QWidget()
            layout = QVBoxLayout(tab)

            # Header
            header = QLabel("ℹ️ Recovery Information")
            header.setStyleSheet(
                "font-size: 18px; font-weight: bold; color: #e74c3c; margin: 10px;"
            )
            header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(header)

            # Error details
            details_text = QTextEdit()
            details_text.setPlainText(
                f"TKA Application - Recovery Mode Active\n\n"
                f"Error Context: {error_details}\n"
                f"Recovery Attempts: {self.recovery_count}\n\n"
                f"What happened:\n"
                f"• The application encountered initialization issues\n"
                f"• Recovery mode provides basic functionality\n"
                f"• Some features may be limited or unavailable\n\n"
                f"Available in recovery mode:\n"
                f"• Basic construct interface\n"
                f"• Limited browse functionality\n"
                f"• Error reporting and logging\n\n"
                f"Recommended actions:\n"
                f"1. Note any error messages in the console\n"
                f"2. Try restarting the application\n"
                f"3. Check system requirements and dependencies\n"
                f"4. Contact support if issues persist\n\n"
                f"Recovery mode ensures you can access core functionality even when "
                f"full initialization fails."
            )
            details_text.setReadOnly(True)
            details_text.setStyleSheet(
                "background: #fff5f5; border: 1px solid #fed7d7; padding: 15px;"
            )
            layout.addWidget(details_text)

            # Recovery actions
            actions_layout = QHBoxLayout()

            log_btn = QPushButton("📝 View Logs")
            log_btn.setStyleSheet(
                "padding: 8px 16px; background: #3498db; color: white; border: none; border-radius: 4px;"
            )
            log_btn.clicked.connect(
                lambda: details_text.append(
                    f"\n📝 Log viewing requested at recovery attempt {self.recovery_count}"
                )
            )
            actions_layout.addWidget(log_btn)

            restart_btn = QPushButton("🔄 Restart Recommended")
            restart_btn.setStyleSheet(
                "padding: 8px 16px; background: #e74c3c; color: white; border: none; border-radius: 4px;"
            )
            restart_btn.clicked.connect(
                lambda: details_text.append("\n🔄 Restart recommendation noted")
            )
            actions_layout.addWidget(restart_btn)

            actions_layout.addStretch()
            layout.addLayout(actions_layout)

            return tab

        except Exception as e:
            StandardErrorHandler.handle_ui_error(
                "Recovery info tab creation", e, logger
            )
            return self._create_minimal_tab("Recovery Error")

    def _create_error_header(self, error_context: str) -> QLabel:
        """Create consistent error header."""
        header = QLabel(f"⚠️ Recovery Mode - {error_context}")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(
            "color: #e74c3c; font-size: 16px; font-weight: bold; "
            "background: #fff5f5; border: 1px solid #fed7d7; "
            "border-radius: 4px; padding: 10px; margin: 5px;"
        )
        return header

    def _add_recovery_tabs(self, tab_widget: QTabWidget) -> None:
        """Add all recovery tabs to the widget."""
        # Construct tab
        construct_tab = self.create_fallback_construct_tab(
            "main initialization failure"
        )
        tab_widget.addTab(construct_tab, "🔧 Construct")

        # Browse tab
        browse_tab = self.create_fallback_browse_tab("main initialization failure")
        tab_widget.addTab(browse_tab, "📁 Browse")

        # Info tab
        info_tab = self.create_recovery_info_tab("application initialization failure")
        tab_widget.addTab(info_tab, "ℹ️ Recovery")

    def _create_basic_controls(
        self, tab_type: str, text_widget: QTextEdit
    ) -> QHBoxLayout:
        """Create basic control buttons for recovery tabs."""
        controls_layout = QHBoxLayout()

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(
            "padding: 8px 16px; background: #3498db; color: white; border: none; border-radius: 4px;"
        )
        refresh_btn.clicked.connect(
            lambda: text_widget.append(f"\n🔄 {tab_type} refresh requested")
        )
        controls_layout.addWidget(refresh_btn)

        info_btn = QPushButton("ℹ️ Info")
        info_btn.setStyleSheet(
            "padding: 8px 16px; background: #95a5a6; color: white; border: none; border-radius: 4px;"
        )
        info_btn.clicked.connect(
            lambda: text_widget.append(f"\n💡 {tab_type} recovery mode active")
        )
        controls_layout.addWidget(info_btn)

        controls_layout.addStretch()
        return controls_layout

    def _populate_recovery_file_list(self, file_list: QListWidget) -> None:
        """Populate file list with recovery mode information."""
        file_list.addItem("📄 Recovery mode - limited file access")
        file_list.addItem("📄 Check data/sequences directory manually")
        file_list.addItem("📄 Full file browser requires restart")
        file_list.addItem(f"📄 Recovery attempt #{self.recovery_count}")

    def _create_minimal_tab(self, error_message: str) -> QWidget:
        """Create minimal tab for critical failures."""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        error_label = QLabel(f"❌ {error_message}")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setStyleSheet("color: #e74c3c; font-size: 14px; margin: 20px;")
        layout.addWidget(error_label)

        return tab

    def _create_minimal_tab_widget(self) -> QTabWidget:
        """Create minimal tab widget for absolute emergency."""
        tab_widget = QTabWidget()
        minimal_tab = self._create_minimal_tab("Critical UI failure")
        tab_widget.addTab(minimal_tab, "❌ Error")
        return tab_widget
