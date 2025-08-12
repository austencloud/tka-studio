"""
End-to-End Tests for TKA Auto-Save/Restore System

Tests the complete user workflow from application startup to shutdown,
validating that users can continue exactly where they left off.
"""

import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add TKA src to path
tka_src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(tka_src_path))

from application.services.core.application_lifecycle_manager import (
    ApplicationLifecycleManager,
)
from core.application.application_factory import ApplicationFactory
from core.interfaces.core_services import IUIStateManagementService
from core.interfaces.session_services import ISessionStateService
from core.testing.ai_agent_helpers import TKAAITestHelper
from domain.models.beat_data import BeatData
from domain.models.sequence_data import SequenceData


class TestSessionEndToEnd:
    """End-to-end tests for the complete session state workflow."""

    def setup_method(self):
        """Setup test environment."""
        # Create test application container
        self.container = ApplicationFactory.create_test_app()

        # Create temporary directory for session files
        self.temp_dir = tempfile.mkdtemp()
        self.session_file = Path(self.temp_dir) / "session_state.json"

        # Create test helper
        self.test_helper = TKAAITestHelper(use_test_mode=True)

        # Get services
        self.session_service = self.container.resolve(ISessionStateService)
        self.ui_state_service = self.container.resolve(IUIStateManagementService)

        # Override session file location for testing
        if hasattr(self.session_service, "session_file"):
            self.session_service.session_file = self.session_file

    def teardown_method(self):
        """Cleanup after each test."""
        # Clean up temporary files
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_complete_user_workflow_with_session_restore(self):
        """
        Test complete user workflow:
        1. User creates sequence and selects beats
        2. User closes application (session saved)
        3. User reopens application (session restored)
        4. User continues exactly where they left off
        """
        print("\n=== Testing Complete User Workflow with Session Restore ===")

        # === PHASE 1: User creates content ===
        print("Phase 1: User creates sequence and selects beats...")

        # Create a sequence
        sequence_result = self.test_helper.create_sequence("My Workflow Test", 8)
        assert (
            sequence_result.success
        ), f"Failed to create sequence: {sequence_result.error}"

        sequence_data = sequence_result.data
        # Handle both dict and object types for sequence data
        sequence_name = (
            sequence_data.get("name")
            if isinstance(sequence_data, dict)
            else sequence_data.name
        )
        sequence_id = (
            sequence_data.get("id")
            if isinstance(sequence_data, dict)
            else sequence_data.id
        )
        beats_count = (
            len(sequence_data.get("beats", []))
            if isinstance(sequence_data, dict)
            else len(sequence_data.beats)
        )
        print(f"✅ Created sequence: {sequence_name} with {beats_count} beats")

        # Update session with sequence
        self.session_service.update_current_sequence(sequence_data, sequence_id)

        # User selects a beat
        beat_data = BeatData(beat_number=3, letter="C", duration=1.5)
        selected_beat_index = 2
        self.session_service.update_workbench_state(
            selected_beat_index, beat_data, None
        )
        print(f"✅ Selected beat {selected_beat_index} with letter {beat_data.letter}")

        # User opens graph editor
        self.session_service.update_graph_editor_state(
            True, selected_beat_index, "red_arrow", 350
        )
        print("✅ Opened graph editor and selected red arrow")

        # User switches to dictionary tab
        self.session_service.update_ui_state("dictionary", {"rows": 3, "cols": 6})
        print("✅ Switched to dictionary tab")

        # === PHASE 2: Application shutdown (auto-save) ===
        print("\nPhase 2: Application shutdown with auto-save...")

        save_success = self.session_service.save_session_state()
        assert save_success, "Session should save successfully on shutdown"
        assert self.session_file.exists(), "Session file should exist after save"
        print("✅ Session saved successfully on application shutdown")

        # === PHASE 3: Application restart and session restore ===
        print("\nPhase 3: Application restart with session restore...")

        # Simulate application restart by creating new service instances
        new_container = ApplicationFactory.create_test_app()
        new_session_service = new_container.resolve(ISessionStateService)
        new_ui_state_service = new_container.resolve(IUIStateManagementService)

        # Override session file location for new service
        if hasattr(new_session_service, "session_file"):
            new_session_service.session_file = self.session_file

        # Restore session on startup
        restore_result = new_session_service.load_session_state()
        assert (
            restore_result.success
        ), f"Session restore failed: {restore_result.error_message}"
        assert restore_result.session_restored, "Session should be restored"
        print("✅ Session restored successfully on application startup")

        # === PHASE 4: Verify restored state ===
        print("\nPhase 4: Verifying restored state...")

        restored_session = restore_result.session_data

        # Verify sequence was restored
        assert restored_session.current_sequence_id == sequence_id
        assert restored_session.current_sequence_data is not None
        print(f"✅ Sequence restored: {restored_session.current_sequence_id}")

        # Verify workbench state was restored
        assert restored_session.selected_beat_index == selected_beat_index
        assert restored_session.selected_beat_data is not None
        print(
            f"✅ Beat selection restored: index {restored_session.selected_beat_index}"
        )

        # Verify graph editor state was restored
        assert restored_session.graph_editor_visible is True
        assert restored_session.graph_editor_selected_beat_index == selected_beat_index
        assert restored_session.graph_editor_selected_arrow == "red_arrow"
        assert restored_session.graph_editor_height == 350
        print("✅ Graph editor state restored: visible, red arrow selected")

        # Verify UI state was restored
        assert restored_session.active_tab == "dictionary"
        assert restored_session.beat_layout == {"rows": 3, "cols": 6}
        print("✅ UI state restored: dictionary tab, custom layout")

        print(
            "\n🎉 Complete workflow test PASSED - User can continue exactly where they left off!"
        )

    def test_application_lifecycle_integration(self):
        """Test integration with ApplicationLifecycleManager."""
        print("\n=== Testing Application Lifecycle Integration ===")

        # Create lifecycle manager with session service
        lifecycle_manager = ApplicationLifecycleManager()
        lifecycle_manager.set_session_service(self.session_service)

        # Create some session data
        self.session_service.update_current_sequence({"test": "data"}, "lifecycle_test")

        # Test cleanup (simulates application shutdown)
        lifecycle_manager.cleanup_application()

        # Verify session was saved
        assert self.session_file.exists(), "Session should be saved during cleanup"
        print("✅ Session saved during application cleanup")

        # Test initialization with session restore
        # Note: In real app, this would restore UI state
        restore_result = self.session_service.load_session_state()
        assert restore_result.success and restore_result.session_restored
        print("✅ Session restored during application initialization")

    def test_performance_no_ui_lag(self):
        """Test that auto-save operations don't cause UI lag."""
        print("\n=== Testing Performance - No UI Lag ===")

        # Enable auto-save with realistic delay
        self.session_service.auto_save_delay_ms = 2000  # 2 seconds

        # Measure time for rapid interactions
        start_time = time.time()

        # Simulate rapid user interactions
        for i in range(10):
            self.session_service.update_workbench_state(i, None, None)
            self.session_service.update_graph_editor_state(True, i, f"arrow_{i}")
            self.session_service.update_ui_state(f"tab_{i}")

        interaction_time = time.time() - start_time

        # All interactions should complete quickly (under 100ms)
        assert (
            interaction_time < 0.1
        ), f"Interactions took too long: {interaction_time:.3f}s"
        print(
            f"✅ 30 rapid interactions completed in {interaction_time:.3f}s (no UI lag)"
        )

        # Verify session state is updated correctly
        current_session = self.session_service.get_current_session_state()
        assert current_session.selected_beat_index == 9  # Last update
        assert current_session.active_tab == "tab_9"  # Last update
        print("✅ Session state correctly reflects latest interactions")

    def test_graceful_degradation_on_errors(self):
        """Test that application continues to work when session features fail."""
        print("\n=== Testing Graceful Degradation on Errors ===")

        # Mock file system service to simulate failures
        with patch.object(self.session_service, "file_system_service") as mock_fs:
            mock_fs.write_file.side_effect = Exception("Disk full")

            # Try to save session (should fail gracefully)
            save_success = self.session_service.save_session_state()
            assert not save_success, "Save should fail due to mocked error"
            print("✅ Session save failure handled gracefully")

            # Application should continue working
            self.session_service.update_current_sequence({"test": "data"}, "error_test")
            current_session = self.session_service.get_current_session_state()
            assert current_session.current_sequence_id == "error_test"
            print("✅ Application continues working despite session save failure")

    def test_backward_compatibility(self):
        """Test that session system doesn't break existing functionality."""
        print("\n=== Testing Backward Compatibility ===")

        # Test that UI state service works without session service
        ui_service_without_session = self.container.resolve(IUIStateManagementService)
        ui_service_without_session._session_service = None

        # These operations should work without session service
        ui_service_without_session.set_setting("test_key", "test_value")
        ui_service_without_session.set_active_tab("sequence_builder")

        # Verify settings still work
        assert ui_service_without_session.get_setting("test_key") == "test_value"
        assert ui_service_without_session.get_active_tab() == "sequence_builder"
        print("✅ UI state service works correctly without session service")

        # Test that session service can be added later
        ui_service_without_session.set_session_service(self.session_service)
        ui_service_without_session.set_active_tab("dictionary")

        # Verify session is now being updated
        current_session = self.session_service.get_current_session_state()
        assert current_session.active_tab == "dictionary"
        print("✅ Session service can be added to existing UI service")

    def test_session_file_location_and_format(self):
        """Test that session files are created in correct location with correct format."""
        print("\n=== Testing Session File Location and Format ===")

        # Create session data
        self.session_service.update_current_sequence(
            {"name": "Format Test"}, "format_test"
        )
        self.session_service.update_ui_state("test_tab", {"test": "layout"})

        # Save session
        save_success = self.session_service.save_session_state()
        assert save_success and self.session_file.exists()

        # Verify file format
        import json

        with open(self.session_file, "r") as f:
            session_data = json.load(f)

        # Check required sections
        required_sections = [
            "session_metadata",
            "current_sequence",
            "workbench_state",
            "graph_editor_state",
            "ui_state",
        ]
        for section in required_sections:
            assert section in session_data, f"Missing section: {section}"

        # Check metadata format
        metadata = session_data["session_metadata"]
        assert "session_id" in metadata
        assert "created_at" in metadata
        assert "last_interaction" in metadata
        assert "tka_version" in metadata

        print("✅ Session file format is correct and complete")
        print(f"✅ Session file created at: {self.session_file}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
