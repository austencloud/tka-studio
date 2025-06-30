#!/usr/bin/env python3
"""
Comprehensive Debugging and Testing Solution for Modern Visibility Tab.

This standalone test application launches only the new visibility tab in isolation,
enabling real-time testing and comprehensive data collection without requiring
additional user interaction.

Features:
- Standalone QApplication with debug controls
- Comprehensive logging and diagnostics
- Interactive testing features
- Automated validation checks
- Performance metrics and reporting
"""

import sys
import os
import json
import time
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Add the modern src directory to Python path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src")
)

try:
    from PyQt6.QtWidgets import (
        QApplication,
        QMainWindow,
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QSplitter,
        QPushButton,
        QLabel,
        QTextEdit,
        QGroupBox,
        QGridLayout,
        QScrollArea,
        QFrame,
        QCheckBox,
        QProgressBar,
    )
    from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, QObject
    from PyQt6.QtGui import QFont, QKeySequence, QShortcut

    QT_AVAILABLE = True
except ImportError:
    print("⚠️ PyQt6 not available - running in headless mode")
    QT_AVAILABLE = False

# Import TKA components
try:
    from core.application.application_factory import ApplicationFactory
    from core.testing.ai_agent_helpers import TKAAITestHelper
    from core.interfaces.tab_settings_interfaces import IVisibilityService

    from application.services.settings.visibility_state_manager import (
        ModernVisibilityStateManager,
    )
    from application.services.pictograph.global_visibility_service import (
        GlobalVisibilityService,
    )

    if QT_AVAILABLE:
        from presentation.components.ui.settings.tabs.visibility_tab import (
            VisibilityTab,
        )
        from presentation.components.ui.settings.visibility_pictograph_preview import (
            VisibilityPictographPreview,
        )

    TKA_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ TKA components not available: {e}")
    TKA_AVAILABLE = False


@dataclass
class ComponentMetrics:
    """Metrics for a UI component."""

    name: str
    width: int
    height: int
    x: int
    y: int
    visible: bool
    enabled: bool
    creation_time: float
    render_time: Optional[float] = None
    error_count: int = 0
    last_error: Optional[str] = None


@dataclass
class TestResults:
    """Complete test results and diagnostics."""

    timestamp: str
    total_duration: float
    components: Dict[str, ComponentMetrics]
    state_changes: List[Dict[str, Any]]
    performance_metrics: Dict[str, float]
    validation_results: Dict[str, bool]
    issues_found: List[str]
    recommendations: List[str]


class DebugLogger:
    """Enhanced logging system for visibility debugging."""

    def __init__(self):
        self.setup_logging()
        self.events = []
        self.start_time = time.time()

    def setup_logging(self):
        """Setup comprehensive logging configuration."""
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler("visibility_debug.log", mode="w"),
            ],
        )
        self.logger = logging.getLogger("VisibilityDebug")

    def log_event(self, category: str, event: str, data: Optional[Dict] = None):
        """Log an event with timestamp and optional data."""
        timestamp = time.time() - self.start_time
        event_data = {
            "timestamp": timestamp,
            "category": category,
            "event": event,
            "data": data or {},
        }
        self.events.append(event_data)
        self.logger.info(f"[{category}] {event}: {data}")

    def get_events(self) -> List[Dict]:
        """Get all logged events."""
        return self.events


class VisibilityDebugWindow(QMainWindow):
    """Main debug window for visibility tab testing."""

    def __init__(self):
        super().__init__()
        self.debug_logger = DebugLogger()
        self.test_results = TestResults(
            timestamp=datetime.now().isoformat(),
            total_duration=0.0,
            components={},
            state_changes=[],
            performance_metrics={},
            validation_results={},
            issues_found=[],
            recommendations=[],
        )

        # TKA components
        self.container = None
        self.visibility_service = None
        self.state_manager = None
        self.global_service = None
        self.visibility_tab = None

        # UI components
        self.status_label = None
        self.log_display = None
        self.metrics_display = None

        self.setup_tka_services()
        self.setup_ui()
        self.setup_shortcuts()
        self.start_monitoring()

    def setup_tka_services(self):
        """Initialize TKA services using dependency injection."""
        try:
            self.debug_logger.log_event("INIT", "Setting up TKA services")

            # Create test application container
            self.container = ApplicationFactory.create_test_app()
            self.debug_logger.log_event("INIT", "Created test application container")

            # Resolve services
            self.visibility_service = self.container.resolve(IVisibilityService)
            self.debug_logger.log_event("INIT", "Resolved IVisibilityService")

            # Create our new components
            self.state_manager = ModernVisibilityStateManager(self.visibility_service)
            self.global_service = GlobalVisibilityService()
            self.debug_logger.log_event("INIT", "Created modern visibility components")

            # Validate TKA system
            helper = TKAAITestHelper(use_test_mode=True)
            result = helper.run_comprehensive_test_suite()

            if result.success:
                self.debug_logger.log_event(
                    "VALIDATION",
                    "TKA system validation passed",
                    {"success_rate": result.metadata.get("success_rate", 0)},
                )
            else:
                self.debug_logger.log_event(
                    "ERROR", "TKA system validation failed", {"errors": result.errors}
                )

        except Exception as e:
            self.debug_logger.log_event(
                "ERROR", "Failed to setup TKA services", {"error": str(e)}
            )
            raise

    def setup_ui(self):
        """Setup the debug UI."""
        self.setWindowTitle("Modern Visibility Tab - Debug & Test Environment")
        self.setGeometry(100, 100, 1400, 900)

        # Central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left side - Visibility Tab under test
        self.setup_visibility_tab_section(splitter)

        # Right side - Debug controls and monitoring
        self.setup_debug_panel(splitter)

        # Set splitter proportions (70% tab, 30% debug)
        splitter.setSizes([980, 420])
        main_layout.addWidget(splitter)

        self.debug_logger.log_event("UI", "Debug window setup complete")

    def setup_visibility_tab_section(self, parent_splitter):
        """Setup the visibility tab section."""
        try:
            # Create container for visibility tab
            tab_container = QFrame()
            tab_container.setFrameStyle(QFrame.Shape.Box)
            tab_container.setStyleSheet(
                """
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(30, 41, 59, 1.0),
                        stop:1 rgba(15, 23, 42, 1.0));
                    border: 2px solid rgba(59, 130, 246, 0.3);
                    border-radius: 8px;
                }
            """
            )

            layout = QVBoxLayout(tab_container)

            # Title
            title = QLabel("Modern Visibility Tab - Live Test")
            title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            title.setStyleSheet(
                "color: white; padding: 10px; background: rgba(59, 130, 246, 0.2); border-radius: 4px;"
            )
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title)

            # Create the actual visibility tab only if available
            if QT_AVAILABLE and TKA_AVAILABLE and 'VisibilityTab' in globals():
                start_time = time.time()
                self.visibility_tab = VisibilityTab(
                    visibility_service=self.visibility_service,
                    global_visibility_service=self.global_service,
                )
                creation_time = time.time() - start_time

                layout.addWidget(self.visibility_tab)
                parent_splitter.addWidget(tab_container)

                # Record metrics
                self.record_component_metrics(
                    "VisibilityTab", self.visibility_tab, creation_time
                )
                self.debug_logger.log_event(
                    "COMPONENT", "VisibilityTab created", {"creation_time": creation_time}
                )
            else:
                raise RuntimeError("VisibilityTab is not available (QT_AVAILABLE or TKA_AVAILABLE is False)")

        except Exception as e:
            self.debug_logger.log_event(
                "ERROR", "Failed to create VisibilityTab", {"error": str(e)}
            )
            # Create error placeholder
            error_widget = QLabel(f"Error creating VisibilityTab:\n{str(e)}")
            error_widget.setStyleSheet(
                "color: red; padding: 20px; background: rgba(255, 0, 0, 0.1);"
            )
            parent_splitter.addWidget(error_widget)

    def setup_debug_panel(self, parent_splitter):
        """Setup the debug control panel."""
        debug_panel = QWidget()
        layout = QVBoxLayout(debug_panel)

        # Status section
        status_group = QGroupBox("System Status")
        status_layout = QVBoxLayout(status_group)

        self.status_label = QLabel("Initializing...")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        status_layout.addWidget(self.status_label)

        # Progress bar for operations
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        status_layout.addWidget(self.progress_bar)

        layout.addWidget(status_group)

        # Control buttons
        controls_group = QGroupBox("Test Controls")
        controls_layout = QGridLayout(controls_group)

        # Create control buttons
        buttons = [
            ("Capture State (F1)", self.capture_current_state),
            ("Stress Test (F2)", self.run_stress_test),
            ("Reset Defaults (F3)", self.reset_to_defaults),
            ("Validate All (F4)", self.run_validation),
            ("Export Report (F5)", self.export_report),
            ("Toggle All Motions", self.toggle_all_motions),
            ("Toggle All Elements", self.toggle_all_elements),
            ("Simulate User Flow", self.simulate_user_flow),
        ]

        for i, (text, callback) in enumerate(buttons):
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            btn.setMinimumHeight(30)
            controls_layout.addWidget(btn, i // 2, i % 2)

        layout.addWidget(controls_group)

        # Metrics display
        metrics_group = QGroupBox("Live Metrics")
        metrics_layout = QVBoxLayout(metrics_group)

        self.metrics_display = QTextEdit()
        self.metrics_display.setMaximumHeight(150)
        self.metrics_display.setStyleSheet("font-family: monospace; font-size: 10px;")
        metrics_layout.addWidget(self.metrics_display)

        layout.addWidget(metrics_group)

        # Log display
        log_group = QGroupBox("Debug Log")
        log_layout = QVBoxLayout(log_group)

        self.log_display = QTextEdit()
        self.log_display.setStyleSheet(
            "font-family: monospace; font-size: 10px; background: black; color: lime;"
        )
        log_layout.addWidget(self.log_display)

        layout.addWidget(log_group)

        parent_splitter.addWidget(debug_panel)

    def setup_shortcuts(self):
        """Setup keyboard shortcuts for quick testing."""
        shortcuts = [
            (QKeySequence("F1"), self.capture_current_state),
            (QKeySequence("F2"), self.run_stress_test),
            (QKeySequence("F3"), self.reset_to_defaults),
            (QKeySequence("F4"), self.run_validation),
            (QKeySequence("F5"), self.export_report),
        ]

        for key_seq, callback in shortcuts:
            shortcut = QShortcut(key_seq, self)
            shortcut.activated.connect(callback)

    def start_monitoring(self):
        """Start continuous monitoring of components."""
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_monitoring)
        self.monitor_timer.start(1000)  # Update every second

        self.status_label.setText("✅ System Ready - Monitoring Active")
        self.debug_logger.log_event("MONITOR", "Started continuous monitoring")

    def record_component_metrics(
        self, name: str, widget: QWidget, creation_time: float
    ):
        """Record metrics for a component."""
        if widget:
            metrics = ComponentMetrics(
                name=name,
                width=widget.width(),
                height=widget.height(),
                x=widget.x(),
                y=widget.y(),
                visible=widget.isVisible(),
                enabled=widget.isEnabled(),
                creation_time=creation_time,
            )
            self.test_results.components[name] = metrics

    def update_monitoring(self):
        """Update monitoring displays."""
        try:
            # Update metrics display
            if self.visibility_tab:
                state_summary = self.visibility_tab.get_state_summary()
                metrics_text = f"""Component Status:
Tab Size: {self.visibility_tab.width()}x{self.visibility_tab.height()}
Motion States: {state_summary.get('motion_states', {})}
Element States: {len(state_summary.get('element_states', {}))} elements
Warning Visible: {state_summary.get('dependency_warning_visible', False)}
Validation: {state_summary.get('state_manager_validation', {}).get('valid', 'Unknown')}

Performance:
Events Logged: {len(self.debug_logger.get_events())}
Uptime: {time.time() - self.debug_logger.start_time:.1f}s"""

                self.metrics_display.setText(metrics_text)

            # Update log display with recent events
            recent_events = self.debug_logger.get_events()[-10:]  # Last 10 events
            log_text = "\n".join(
                [
                    f"[{event['timestamp']:.2f}s] {event['category']}: {event['event']}"
                    for event in recent_events
                ]
            )
            self.log_display.setText(log_text)

        except Exception as e:
            self.debug_logger.log_event(
                "ERROR", "Monitoring update failed", {"error": str(e)}
            )

    def capture_current_state(self):
        """Capture complete current state with detailed diagnostics."""
        self.debug_logger.log_event("TEST", "Capturing current state")

        try:
            state_data = {
                "timestamp": time.time(),
                "visibility_tab": self.diagnose_visibility_tab(),
                "pictograph_preview": self.diagnose_pictograph_preview(),
                "state_manager": self.diagnose_state_manager(),
                "global_service": self.diagnose_global_service(),
                "layout_metrics": self.measure_layout_metrics(),
                "performance": self.measure_performance(),
            }

            # Log to console with formatting
            print("\n" + "=" * 60)
            print("📊 CURRENT STATE CAPTURE")
            print("=" * 60)

            for category, data in state_data.items():
                print(f"\n🔍 {category.upper()}:")
                if isinstance(data, dict):
                    for key, value in data.items():
                        print(f"  {key}: {value}")
                else:
                    print(f"  {data}")

            # Store in test results
            self.test_results.state_changes.append(state_data)
            self.status_label.setText(
                f"✅ State captured at {datetime.now().strftime('%H:%M:%S')}"
            )

        except Exception as e:
            self.debug_logger.log_event(
                "ERROR", "State capture failed", {"error": str(e)}
            )
            self.status_label.setText(f"❌ State capture failed: {str(e)}")

    def diagnose_visibility_tab(self) -> Dict[str, Any]:
        """Diagnose the main visibility tab component."""
        if not self.visibility_tab:
            return {"error": "VisibilityTab not created"}

        try:
            # Get comprehensive state summary
            state_summary = self.visibility_tab.get_state_summary()

            # Measure widget geometry
            geometry = {
                "size": f"{self.visibility_tab.width()}x{self.visibility_tab.height()}",
                "position": f"({self.visibility_tab.x()}, {self.visibility_tab.y()})",
                "visible": self.visibility_tab.isVisible(),
                "enabled": self.visibility_tab.isEnabled(),
            }

            # Check component counts
            motion_count = len(self.visibility_tab.motion_toggles)
            element_count = len(self.visibility_tab.element_toggles)

            # Check preview component
            preview_status = "Present" if self.visibility_tab.preview else "Missing"

            return {
                "geometry": geometry,
                "motion_toggles": motion_count,
                "element_toggles": element_count,
                "preview_component": preview_status,
                "dependency_warning_visible": state_summary.get(
                    "dependency_warning_visible", False
                ),
                "state_validation": state_summary.get(
                    "state_manager_validation", {}
                ).get("valid", "Unknown"),
                "motion_states": state_summary.get("motion_states", {}),
                "element_states_count": len(state_summary.get("element_states", {})),
            }

        except Exception as e:
            return {"error": f"Diagnosis failed: {str(e)}"}

    def diagnose_pictograph_preview(self) -> Dict[str, Any]:
        """Diagnose the pictograph preview component."""
        if not self.visibility_tab or not self.visibility_tab.preview:
            return {"error": "PictographPreview not available"}

        try:
            preview = self.visibility_tab.preview

            # Check scene and view
            scene_status = "Present" if preview.scene else "Missing"
            view_status = "Present" if preview.view else "Missing"
            sample_data_status = "Present" if preview.sample_beat_data else "Missing"

            # Measure preview geometry
            preview_geometry = {
                "size": f"{preview.width()}x{preview.height()}",
                "visible": preview.isVisible(),
                "enabled": preview.isEnabled(),
            }

            # Check scene details if available
            scene_details = {}
            if preview.scene:
                scene_details = {
                    "scene_rect": f"{preview.scene.sceneRect().width()}x{preview.scene.sceneRect().height()}",
                    "items_count": len(preview.scene.items()),
                    "background_brush": str(
                        preview.scene.backgroundBrush().color().name()
                    ),
                }

            # Check sample data details
            sample_data_details = {}
            if preview.sample_beat_data:
                sample_data_details = {
                    "letter": preview.sample_beat_data.letter,
                    "has_blue_motion": preview.sample_beat_data.blue_motion is not None,
                    "has_red_motion": preview.sample_beat_data.red_motion is not None,
                    "has_glyph_data": preview.sample_beat_data.glyph_data is not None,
                    "is_blank": preview.sample_beat_data.is_blank,
                }

            return {
                "geometry": preview_geometry,
                "scene_status": scene_status,
                "view_status": view_status,
                "sample_data_status": sample_data_status,
                "scene_details": scene_details,
                "sample_data_details": sample_data_details,
            }

        except Exception as e:
            return {"error": f"Preview diagnosis failed: {str(e)}"}

    def diagnose_state_manager(self) -> Dict[str, Any]:
        """Diagnose the state manager component."""
        if not self.state_manager:
            return {"error": "StateManager not available"}

        try:
            # Get all visibility states
            all_states = self.state_manager.get_all_visibility_states()

            # Run validation
            validation = self.state_manager.validate_state()

            # Check observer counts
            observer_counts = {}
            for category, observers in self.state_manager._observers.items():
                observer_counts[category] = len(observers)

            return {
                "all_motions_visible": self.state_manager.are_all_motions_visible(),
                "validation_valid": validation["valid"],
                "validation_issues": len(validation["issues"]),
                "validation_warnings": len(validation["warnings"]),
                "observer_counts": observer_counts,
                "glyph_states": all_states.get("glyphs", {}),
                "motion_states": all_states.get("motions", {}),
                "non_radial_visible": all_states.get("non_radial", False),
            }

        except Exception as e:
            return {"error": f"StateManager diagnosis failed: {str(e)}"}

    def diagnose_global_service(self) -> Dict[str, Any]:
        """Diagnose the global visibility service."""
        if not self.global_service:
            return {"error": "GlobalService not available"}

        try:
            # Get statistics
            stats = self.global_service.get_statistics()

            # Get registered pictographs
            pictographs = self.global_service.get_all_registered_pictographs()

            # Get component types
            component_types = self.global_service.get_component_types()

            return {
                "statistics": stats,
                "registered_pictographs": len(pictographs),
                "component_types": component_types,
                "active_registrations": stats.get("active_registrations", 0),
                "total_registrations": stats.get("total_registrations", 0),
                "update_calls": stats.get("update_calls", 0),
                "failed_updates": stats.get("failed_updates", 0),
            }

        except Exception as e:
            return {"error": f"GlobalService diagnosis failed: {str(e)}"}

    def measure_layout_metrics(self) -> Dict[str, Any]:
        """Measure detailed layout metrics."""
        if not self.visibility_tab:
            return {"error": "VisibilityTab not available"}

        try:
            # Find splitter and measure proportions
            splitter = self.visibility_tab.findChild(QSplitter)
            splitter_info = {}
            if splitter:
                sizes = splitter.sizes()
                total_size = sum(sizes)
                proportions = (
                    [size / total_size * 100 for size in sizes]
                    if total_size > 0
                    else []
                )
                splitter_info = {
                    "sizes": sizes,
                    "proportions": [f"{p:.1f}%" for p in proportions],
                    "orientation": (
                        "Horizontal"
                        if splitter.orientation() == Qt.Orientation.Horizontal
                        else "Vertical"
                    ),
                }

            # Measure motion controls
            motion_controls_info = {}
            for color, toggle in self.visibility_tab.motion_toggles.items():
                motion_controls_info[f"{color}_motion"] = {
                    "size": f"{toggle.width()}x{toggle.height()}",
                    "visible": toggle.isVisible(),
                    "enabled": toggle.isEnabled(),
                    "checked": toggle.isChecked(),
                }

            # Measure element controls
            element_controls_info = {}
            for name, toggle in self.visibility_tab.element_toggles.items():
                element_controls_info[name] = {
                    "size": f"{toggle.width()}x{toggle.height()}",
                    "visible": toggle.isVisible(),
                    "enabled": toggle.isEnabled(),
                    "checked": toggle.isChecked(),
                }

            return {
                "splitter": splitter_info,
                "motion_controls": motion_controls_info,
                "element_controls": element_controls_info,
                "total_tab_size": f"{self.visibility_tab.width()}x{self.visibility_tab.height()}",
            }

        except Exception as e:
            return {"error": f"Layout measurement failed: {str(e)}"}

    def measure_performance(self) -> Dict[str, Any]:
        """Measure performance metrics."""
        try:
            events = self.debug_logger.get_events()

            # Calculate timing metrics
            init_events = [e for e in events if e["category"] == "INIT"]
            component_events = [e for e in events if e["category"] == "COMPONENT"]
            error_events = [e for e in events if e["category"] == "ERROR"]

            # Calculate uptime
            uptime = time.time() - self.debug_logger.start_time

            # Memory usage (basic)
            import psutil

            process = psutil.Process()
            memory_info = process.memory_info()

            return {
                "uptime_seconds": round(uptime, 2),
                "total_events": len(events),
                "init_events": len(init_events),
                "component_events": len(component_events),
                "error_events": len(error_events),
                "memory_mb": round(memory_info.rss / 1024 / 1024, 2),
                "error_rate": (
                    f"{len(error_events)/len(events)*100:.1f}%" if events else "0%"
                ),
            }

        except Exception as e:
            return {"error": f"Performance measurement failed: {str(e)}"}

    def run_stress_test(self):
        """Run stress test with rapid state changes."""
        self.debug_logger.log_event("TEST", "Starting stress test")
        self.status_label.setText("🔥 Running stress test...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 100)

        try:
            # Test rapid motion toggles
            for i in range(10):
                self.progress_bar.setValue(i * 10)
                QApplication.processEvents()

                # Toggle motions rapidly
                if self.visibility_tab:
                    for color in ["blue", "red"]:
                        if color in self.visibility_tab.motion_toggles:
                            toggle = self.visibility_tab.motion_toggles[color]
                            current_state = toggle.isChecked()
                            toggle.setChecked(not current_state)
                            QApplication.processEvents()
                            time.sleep(0.1)  # Brief pause
                            toggle.setChecked(current_state)
                            QApplication.processEvents()

                # Toggle elements rapidly
                element_names = list(self.visibility_tab.element_toggles.keys())[
                    :3
                ]  # First 3 elements
                for name in element_names:
                    if name in self.visibility_tab.element_toggles:
                        toggle = self.visibility_tab.element_toggles[name]
                        current_state = toggle.isChecked()
                        toggle.setChecked(not current_state)
                        QApplication.processEvents()
                        time.sleep(0.05)
                        toggle.setChecked(current_state)
                        QApplication.processEvents()

            self.progress_bar.setValue(100)
            self.status_label.setText("✅ Stress test completed")
            self.debug_logger.log_event("TEST", "Stress test completed successfully")

        except Exception as e:
            self.debug_logger.log_event(
                "ERROR", "Stress test failed", {"error": str(e)}
            )
            self.status_label.setText(f"❌ Stress test failed: {str(e)}")
        finally:
            self.progress_bar.setVisible(False)

    def reset_to_defaults(self):
        """Reset to default state."""
        self.debug_logger.log_event("TEST", "Resetting to defaults")
        self.status_label.setText("🔄 Resetting to defaults...")

        try:
            if self.visibility_tab:
                # Reset motion toggles to default (both enabled)
                for color, toggle in self.visibility_tab.motion_toggles.items():
                    toggle.setChecked(True)

                # Reset element toggles to default states
                default_states = {
                    "TKA": True,
                    "Reversals": True,
                    "VTG": True,
                    "Elemental": True,
                    "Positions": True,
                    "Non-radial_points": True,
                }

                for name, toggle in self.visibility_tab.element_toggles.items():
                    default_state = default_states.get(name, True)
                    toggle.setChecked(default_state)

                # Refresh the tab
                self.visibility_tab.refresh_all_settings()

                self.status_label.setText("✅ Reset to defaults completed")
                self.debug_logger.log_event("TEST", "Reset to defaults completed")

        except Exception as e:
            self.debug_logger.log_event("ERROR", "Reset failed", {"error": str(e)})
            self.status_label.setText(f"❌ Reset failed: {str(e)}")

    def run_validation(self):
        """Run comprehensive validation."""
        self.debug_logger.log_event("TEST", "Running comprehensive validation")
        self.status_label.setText("🔍 Running validation...")

        validation_results = {}
        issues_found = []

        try:
            # Validate visibility tab creation
            if self.visibility_tab:
                validation_results["visibility_tab_created"] = True

                # Check motion toggles
                motion_count = len(self.visibility_tab.motion_toggles)
                validation_results["motion_toggles_count"] = motion_count
                if motion_count != 2:
                    issues_found.append(
                        f"Expected 2 motion toggles, found {motion_count}"
                    )

                # Check element toggles
                element_count = len(self.visibility_tab.element_toggles)
                validation_results["element_toggles_count"] = element_count
                if element_count < 5:
                    issues_found.append(
                        f"Expected at least 5 element toggles, found {element_count}"
                    )

                # Check preview component
                if self.visibility_tab.preview:
                    validation_results["preview_component"] = True

                    # Check scene
                    if self.visibility_tab.preview.scene:
                        validation_results["preview_scene"] = True
                    else:
                        issues_found.append("Preview scene not created")
                        validation_results["preview_scene"] = False

                    # Check sample data
                    if self.visibility_tab.preview.sample_beat_data:
                        validation_results["sample_beat_data"] = True
                    else:
                        issues_found.append("Sample beat data not created")
                        validation_results["sample_beat_data"] = False
                else:
                    issues_found.append("Preview component not created")
                    validation_results["preview_component"] = False
            else:
                issues_found.append("Visibility tab not created")
                validation_results["visibility_tab_created"] = False

            # Validate state manager
            if self.state_manager:
                validation_results["state_manager_created"] = True

                # Run state manager validation
                state_validation = self.state_manager.validate_state()
                validation_results["state_manager_valid"] = state_validation["valid"]

                if not state_validation["valid"]:
                    issues_found.extend(state_validation["issues"])

                # Check observer registration
                observer_count = sum(
                    len(observers)
                    for observers in self.state_manager._observers.values()
                )
                validation_results["observer_count"] = observer_count

            else:
                issues_found.append("State manager not created")
                validation_results["state_manager_created"] = False

            # Validate global service
            if self.global_service:
                validation_results["global_service_created"] = True
                stats = self.global_service.get_statistics()
                validation_results["global_service_stats"] = stats
            else:
                issues_found.append("Global service not created")
                validation_results["global_service_created"] = False

            # Store results
            self.test_results.validation_results = validation_results
            self.test_results.issues_found = issues_found

            # Update status
            if issues_found:
                self.status_label.setText(
                    f"⚠️ Validation completed with {len(issues_found)} issues"
                )
                print(f"\n⚠️ VALIDATION ISSUES FOUND:")
                for issue in issues_found:
                    print(f"  - {issue}")
            else:
                self.status_label.setText("✅ Validation passed - no issues found")
                print("\n✅ VALIDATION PASSED - All checks successful")

            self.debug_logger.log_event(
                "TEST",
                "Validation completed",
                {"issues_count": len(issues_found), "results": validation_results},
            )

        except Exception as e:
            self.debug_logger.log_event("ERROR", "Validation failed", {"error": str(e)})
            self.status_label.setText(f"❌ Validation failed: {str(e)}")

    def toggle_all_motions(self):
        """Toggle all motion states."""
        self.debug_logger.log_event("TEST", "Toggling all motions")

        try:
            if self.visibility_tab:
                # Get current states
                current_states = {}
                for color, toggle in self.visibility_tab.motion_toggles.items():
                    current_states[color] = toggle.isChecked()

                # Toggle each motion
                for color, toggle in self.visibility_tab.motion_toggles.items():
                    toggle.setChecked(not current_states[color])

                self.status_label.setText("🔄 Toggled all motion states")
                self.debug_logger.log_event(
                    "TEST", "Motion toggle completed", {"states": current_states}
                )

        except Exception as e:
            self.debug_logger.log_event(
                "ERROR", "Motion toggle failed", {"error": str(e)}
            )
            self.status_label.setText(f"❌ Motion toggle failed: {str(e)}")

    def toggle_all_elements(self):
        """Toggle all element states."""
        self.debug_logger.log_event("TEST", "Toggling all elements")

        try:
            if self.visibility_tab:
                # Get current states
                current_states = {}
                for name, toggle in self.visibility_tab.element_toggles.items():
                    current_states[name] = toggle.isChecked()

                # Toggle each element
                for name, toggle in self.visibility_tab.element_toggles.items():
                    toggle.setChecked(not current_states[name])

                self.status_label.setText("🔄 Toggled all element states")
                self.debug_logger.log_event(
                    "TEST", "Element toggle completed", {"states": current_states}
                )

        except Exception as e:
            self.debug_logger.log_event(
                "ERROR", "Element toggle failed", {"error": str(e)}
            )
            self.status_label.setText(f"❌ Element toggle failed: {str(e)}")

    def simulate_user_flow(self):
        """Simulate typical user interaction flow."""
        self.debug_logger.log_event("TEST", "Simulating user flow")
        self.status_label.setText("👤 Simulating user interaction flow...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 10)

        try:
            # Step 1: Start with defaults
            self.progress_bar.setValue(1)
            self.reset_to_defaults()
            QApplication.processEvents()
            time.sleep(0.5)

            # Step 2: Disable blue motion
            self.progress_bar.setValue(2)
            if "blue" in self.visibility_tab.motion_toggles:
                self.visibility_tab.motion_toggles["blue"].setChecked(False)
            QApplication.processEvents()
            time.sleep(0.5)

            # Step 3: Try to disable red motion (should be prevented)
            self.progress_bar.setValue(3)
            if "red" in self.visibility_tab.motion_toggles:
                self.visibility_tab.motion_toggles["red"].setChecked(False)
            QApplication.processEvents()
            time.sleep(0.5)

            # Step 4: Re-enable blue motion
            self.progress_bar.setValue(4)
            if "blue" in self.visibility_tab.motion_toggles:
                self.visibility_tab.motion_toggles["blue"].setChecked(True)
            QApplication.processEvents()
            time.sleep(0.5)

            # Step 5: Toggle some elements
            self.progress_bar.setValue(5)
            element_names = ["TKA", "VTG", "Elemental"]
            for name in element_names:
                if name in self.visibility_tab.element_toggles:
                    toggle = self.visibility_tab.element_toggles[name]
                    toggle.setChecked(not toggle.isChecked())
                    QApplication.processEvents()
                    time.sleep(0.3)

            # Step 6: Capture state
            self.progress_bar.setValue(8)
            self.capture_current_state()

            # Step 7: Reset to defaults
            self.progress_bar.setValue(10)
            self.reset_to_defaults()

            self.status_label.setText("✅ User flow simulation completed")
            self.debug_logger.log_event("TEST", "User flow simulation completed")

        except Exception as e:
            self.debug_logger.log_event(
                "ERROR", "User flow simulation failed", {"error": str(e)}
            )
            self.status_label.setText(f"❌ User flow simulation failed: {str(e)}")
        finally:
            self.progress_bar.setVisible(False)

    def export_report(self):
        """Export comprehensive test report."""
        self.debug_logger.log_event("TEST", "Exporting comprehensive report")
        self.status_label.setText("📄 Exporting test report...")

        try:
            # Finalize test results
            self.test_results.total_duration = (
                time.time() - self.debug_logger.start_time
            )
            self.test_results.performance_metrics = self.measure_performance()

            # Create comprehensive report
            report = {
                "test_session": asdict(self.test_results),
                "all_events": self.debug_logger.get_events(),
                "final_state": {
                    "visibility_tab": self.diagnose_visibility_tab(),
                    "pictograph_preview": self.diagnose_pictograph_preview(),
                    "state_manager": self.diagnose_state_manager(),
                    "global_service": self.diagnose_global_service(),
                    "layout_metrics": self.measure_layout_metrics(),
                },
            }

            # Export to JSON file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"visibility_debug_report_{timestamp}.json"

            with open(filename, "w") as f:
                json.dump(report, f, indent=2, default=str)

            # Print summary to console
            print(f"\n📄 COMPREHENSIVE TEST REPORT EXPORTED")
            print(f"📁 File: {filename}")
            print(f"⏱️ Total Duration: {self.test_results.total_duration:.2f}s")
            print(f"📊 Events Logged: {len(self.debug_logger.get_events())}")
            print(f"⚠️ Issues Found: {len(self.test_results.issues_found)}")

            if self.test_results.issues_found:
                print(f"\n🔍 ISSUES SUMMARY:")
                for issue in self.test_results.issues_found:
                    print(f"  - {issue}")

            self.status_label.setText(f"✅ Report exported: {filename}")
            self.debug_logger.log_event(
                "TEST", "Report exported", {"filename": filename}
            )

        except Exception as e:
            self.debug_logger.log_event(
                "ERROR", "Report export failed", {"error": str(e)}
            )
            self.status_label.setText(f"❌ Report export failed: {str(e)}")


def main():
    """Main entry point for the debug application."""
    print("🔧 Modern Visibility Tab - Debug & Test Environment")
    print("=" * 60)

    if not QT_AVAILABLE:
        print("❌ PyQt6 not available - cannot run GUI debug application")
        return 1

    if not TKA_AVAILABLE:
        print("❌ TKA components not available - cannot run debug application")
        return 1

    try:
        app = QApplication(sys.argv)
        app.setApplicationName("TKA Visibility Debug")

        # Create and show debug window
        debug_window = VisibilityDebugWindow()
        debug_window.show()

        print("✅ Debug application launched successfully")
        print("📋 Use F1-F5 for quick testing, or use the control panel")
        print("📊 Monitor the right panel for real-time diagnostics")

        return app.exec()

    except Exception as e:
        print(f"❌ Failed to launch debug application: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
