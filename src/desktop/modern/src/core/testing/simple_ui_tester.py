"""
Simple UI Testing Framework - Chunk 1: Basic Infrastructure

Tests UI components and provides clear console guidance for AI agents.
Uses existing current_sequence.json and SequenceDataConverter.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
import time

from PyQt6.QtWidgets import QApplication

from desktop.modern.core.application.application_factory import ApplicationFactory
from desktop.modern.core.testing.ai_agent_helpers import AITestResult, TKAAITestHelper
from desktop.modern.core.testing.button_tester import ButtonTester
from desktop.modern.core.testing.component_initializer import ComponentInitializer
from desktop.modern.core.testing.graph_editor_tester import GraphEditorTester


logger = logging.getLogger(__name__)

class SimpleUITester:
    """Simple UI testing with rich console output for AI agents."""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.container = ApplicationFactory.create_test_app()
        self.ai_helper = TKAAITestHelper(use_test_mode=True)

        # Load real sequence data
        self.current_sequence_path = Path("current_sequence.json")
        self.sample_sequence_data = self._load_real_sequence_data()

        # Initialize QApplication
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication([])

        # Components (will be initialized in setup)
        self.workbench = None
        self.graph_editor = None

    def _load_real_sequence_data(self) -> list[dict]:
        """Load the real current_sequence.json data."""
        try:
            if self.current_sequence_path.exists():
                with open(self.current_sequence_path) as f:
                    data = json.load(f)
                print(f"✅ Loaded real sequence data: {len(data)-1} beats")
                return data
            print("⚠️  current_sequence.json not found, using minimal data")
            return self._create_minimal_sequence()
        except Exception as e:
            print(f"❌ Error loading sequence data: {e}")
            return self._create_minimal_sequence()

    def _create_minimal_sequence(self) -> list[dict]:
        """Create minimal sequence data if file not found."""
        return [
            {"word": "TEST", "author": "tester", "level": 1, "prop_type": "staff"},
            {
                "beat": 0, "sequence_start_position": "alpha", "letter": "α",
                "blue_attributes": {"start_loc": "s", "end_loc": "s", "motion_type": "static"},
                "red_attributes": {"start_loc": "n", "end_loc": "n", "motion_type": "static"}
            }
        ]

    def setup_test_environment(self) -> bool:
        """Set up test environment with real data."""
        try:
            print("🔧 Setting up test environment with real sequence data...")

            # Create test sequence using existing AI helper
            sequence_result = self.ai_helper.create_sequence("UI Test Sequence", 8)

            if not sequence_result.success:
                print(f"❌ Failed to create test sequence: {sequence_result.errors}")
                return False

            # Initialize components with real data
            self._initialize_components_with_data(sequence_result.data)

            print("✅ Test environment ready with real sequence data")
            return True

        except Exception as e:
            print(f"❌ Failed to setup test environment: {e}")
            return False

    def _initialize_components_with_data(self, sequence_data):
        """Initialize UI components with real sequence data."""
        print("� Initializing UI components...")

        # Use ComponentInitializer to set up workbench and graph editor
        self.workbench, self.graph_editor = ComponentInitializer.initialize_workbench_and_graph_editor(
            self.container, sequence_data
        )

        if self.workbench and self.graph_editor:
            print("✅ UI components initialized successfully")
            return True
        print("❌ Failed to initialize UI components")
        return False

    def test_workbench_buttons(self) -> AITestResult:
        """Test all workbench buttons."""
        print("🧪 Testing workbench buttons...")

        if not self.workbench:
            return AITestResult(
                success=False,
                errors=["Workbench not initialized"]
            )

        # Get button references
        button_map = ComponentInitializer.get_workbench_button_references(self.workbench)

        if not button_map:
            return AITestResult(
                success=False,
                errors=["No workbench buttons found"]
            )

        # Create button tester and run tests
        button_tester = ButtonTester(self.workbench, self.app)
        return button_tester.test_all_buttons(button_map)

    def test_graph_editor_interactions(self) -> AITestResult:
        """Test graph editor interactions."""
        print("🧪 Testing graph editor interactions...")

        if not self.graph_editor:
            return AITestResult(
                success=False,
                errors=["Graph editor not initialized"]
            )

        # Get control references
        control_map = ComponentInitializer.get_graph_editor_controls(self.graph_editor)

        # Create graph editor tester and run tests
        graph_tester = GraphEditorTester(self.graph_editor, self.app)
        return graph_tester.test_all_graph_editor_interactions(control_map)

    def run_comprehensive_tests(self) -> AITestResult:
        """Run all UI tests and return comprehensive results."""
        print("🚀 Starting comprehensive UI testing...")

        start_time = time.time()
        all_results = []

        # Setup environment
        if not self.setup_test_environment():
            return AITestResult(
                success=False,
                errors=["Failed to setup test environment"],
                execution_time=time.time() - start_time
            )

        # Verify components are initialized
        if not self.workbench or not self.graph_editor:
            return AITestResult(
                success=False,
                errors=["UI components not properly initialized"],
                execution_time=time.time() - start_time
            )

        # Test workbench buttons
        button_results = self.test_workbench_buttons()
        all_results.append(button_results)

        # Test graph editor
        graph_results = self.test_graph_editor_interactions()
        all_results.append(graph_results)

        # Calculate overall success
        overall_success = all(result.success for result in all_results)
        all_errors = []
        for result in all_results:
            all_errors.extend(result.errors)

        execution_time = time.time() - start_time

        print(f"✅ Comprehensive testing completed in {execution_time:.2f}s")
        print(f"📊 Overall success: {overall_success}")

        return AITestResult(
            success=overall_success,
            errors=all_errors,
            execution_time=execution_time,
            metadata={
                "total_tests": len(all_results),
                "successful_tests": sum(1 for r in all_results if r.success),
                "failed_tests": sum(1 for r in all_results if not r.success)
            }
        )
