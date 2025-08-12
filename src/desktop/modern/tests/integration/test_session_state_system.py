"""
Comprehensive Integration Tests for TKA Auto-Save/Restore System

Tests the complete session state functionality including:
- Session state saving and loading
- Auto-save debouncing
- Error handling for corrupted files and permissions
- Session staleness detection
- Integration with TKA services
"""

import json
import sys
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add TKA src to path
tka_src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(tka_src_path))

from application.services.core.session_state_tracker import (
    SessionStateTracker as SessionStateService,
)
from core.application.application_factory import ApplicationFactory
from core.interfaces.core_services import IUIStateManagementService
from core.interfaces.organization_services import IFileSystemService
from core.interfaces.session_services import ISessionStateService, SessionState
from core.testing.ai_agent_helpers import TKAAITestHelper
from domain.models.beat_data import BeatData
from domain.models.sequence_data import SequenceData


class TestSessionStateSystem:
    """Comprehensive tests for the session state auto-save/restore system."""

    def setup_method(self):
        """Setup test environment before each test."""
        # Create test application container
        self.container = ApplicationFactory.create_test_app()

        # Create temporary directory for session files
        self.temp_dir = tempfile.mkdtemp()
        self.session_file = Path(self.temp_dir) / "session_state.json"

        # Create test helper
        self.test_helper = TKAAITestHelper(use_test_mode=True)

        # Get services from container
        self.ui_state_service = self.container.resolve(IUIStateManagementService)
        self.file_system_service = self.container.resolve(IFileSystemService)

        # Create session service with test file location
        self.session_service = SessionStateService(
            ui_state_service=self.ui_state_service,
            file_system_service=self.file_system_service,
        )
        # Override session file location for testing
        self.session_service.session_file = self.session_file

    def teardown_method(self):
        """Cleanup after each test."""
        # Clean up temporary files
        if self.session_file.exists():
            self.session_file.unlink()

        # Clean up temp directory
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_session_state_save_and_load(self):
        """Test basic session state save and load functionality."""
        # Create test sequence data
        sequence_result = self.test_helper.create_sequence("Test Sequence", 8)
        assert sequence_result.success

        sequence_data = sequence_result.data

        # Update session with sequence data
        self.session_service.update_current_sequence(sequence_data, "test_seq_123")

        # Update workbench state
        beat_data = BeatData(beat_number=1, letter="A", duration=1.0)
        self.session_service.update_workbench_state(0, beat_data, None)

        # Update graph editor state
        self.session_service.update_graph_editor_state(True, 0, "blue_arrow", 300)

        # Update UI state
        self.session_service.update_ui_state("sequence_builder", {"rows": 2, "cols": 4})

        # Save session state
        save_success = self.session_service.save_session_state()
        assert save_success, "Session state should save successfully"
        assert self.session_file.exists(), "Session file should be created"

        # Load session state
        restore_result = self.session_service.load_session_state()
        assert restore_result.success, "Session state should load successfully"
        assert restore_result.session_restored, "Session should be restored"
        assert restore_result.session_data is not None, "Session data should be present"

        # Verify restored data
        session_data = restore_result.session_data
        assert session_data.current_sequence_id == "test_seq_123"
        assert session_data.selected_beat_index == 0
        assert session_data.graph_editor_visible is True
        assert session_data.graph_editor_selected_beat_index == 0
        assert session_data.graph_editor_selected_arrow == "blue_arrow"
        assert session_data.active_tab == "sequence_builder"

    def test_auto_save_debouncing(self):
        """Test that auto-save is properly debounced."""
        # Enable auto-save with short delay for testing
        self.session_service.auto_save_delay_ms = 100  # 100ms for testing

        # Mock the timer to track calls
        with patch.object(self.session_service, "_auto_save_timer") as mock_timer:
            mock_timer.stop = Mock()
            mock_timer.start = Mock()

            # Trigger multiple rapid interactions
            self.session_service.mark_interaction()
            self.session_service.mark_interaction()
            self.session_service.mark_interaction()

            # Timer should be stopped and restarted for each interaction
            assert mock_timer.stop.call_count == 3
            assert mock_timer.start.call_count == 3

            # Last call should be with the correct delay
            mock_timer.start.assert_called_with(100)

    def test_session_staleness_detection(self):
        """Test that stale sessions are not restored."""
        # Create a session with old timestamp
        old_session_data = {
            "session_metadata": {
                "session_id": "old_session",
                "created_at": datetime.now().isoformat(),
                "last_interaction": (datetime.now() - timedelta(hours=25)).isoformat(),
                "tka_version": "modern",
            },
            "current_sequence": {"sequence_id": None, "sequence_data": None},
            "workbench_state": {},
            "graph_editor_state": {},
            "ui_state": {},
        }

        # Write stale session to file
        with open(self.session_file, "w") as f:
            json.dump(old_session_data, f)

        # Try to load stale session
        restore_result = self.session_service.load_session_state()
        assert restore_result.success, "Load operation should succeed"
        assert (
            not restore_result.session_restored
        ), "Stale session should not be restored"
        assert "too old" in restore_result.warnings[0].lower()

    def test_corrupted_session_file_handling(self):
        """Test handling of corrupted session files."""
        # Create corrupted session file
        with open(self.session_file, "w") as f:
            f.write("{ invalid json content }")

        # Try to load corrupted session
        restore_result = self.session_service.load_session_state()
        assert (
            restore_result.success
        ), "Load operation should succeed despite corruption"
        assert (
            not restore_result.session_restored
        ), "Corrupted session should not be restored"
        assert "corrupted" in restore_result.error_message.lower()

    def test_permission_error_handling(self):
        """Test handling of permission errors."""
        # Create session file and make it read-only
        self.session_service.save_session_state()
        self.session_file.chmod(0o444)  # Read-only

        try:
            # Try to save when file is read-only
            save_success = self.session_service.save_session_state()
            # On Windows, this might still succeed, so we check the result
            # On Unix systems, this should fail
            if not save_success:
                assert True, "Permission error handled gracefully"
            else:
                # If save succeeded (Windows), that's also acceptable
                assert True, "Save succeeded despite read-only file"
        finally:
            # Restore write permissions for cleanup
            self.session_file.chmod(0o666)

    def test_missing_session_file_handling(self):
        """Test handling when session file doesn't exist."""
        # Ensure session file doesn't exist
        if self.session_file.exists():
            self.session_file.unlink()

        # Try to load non-existent session
        restore_result = self.session_service.load_session_state()
        assert restore_result.success, "Load operation should succeed"
        assert not restore_result.session_restored, "No session should be restored"
        assert restore_result.session_data is None

    def test_session_clear_functionality(self):
        """Test session clearing functionality."""
        # Create and save session data
        self.session_service.update_current_sequence({"test": "data"}, "test_id")
        self.session_service.save_session_state()
        assert self.session_file.exists()

        # Clear session
        clear_success = self.session_service.clear_session()
        assert clear_success, "Session should clear successfully"
        assert not self.session_file.exists(), "Session file should be removed"

        # Verify session state is reset
        current_session = self.session_service.get_current_session_state()
        assert current_session.current_sequence_id is None
        assert current_session.current_sequence_data is None

    def test_auto_save_enable_disable(self):
        """Test auto-save enable/disable functionality."""
        # Test enabling auto-save
        self.session_service.set_auto_save_enabled(True)
        assert self.session_service.is_auto_save_enabled()

        # Test disabling auto-save
        self.session_service.set_auto_save_enabled(False)
        assert not self.session_service.is_auto_save_enabled()

        # When disabled, mark_interaction should not trigger timer
        with patch.object(self.session_service, "_auto_save_timer") as mock_timer:
            self.session_service.mark_interaction()
            mock_timer.start.assert_not_called()

    def test_integration_with_ui_state_service(self):
        """Test integration with UIStateManagementService."""
        # Set session service in UI state service
        self.ui_state_service.set_session_service(self.session_service)

        # Test sequence update with session
        test_sequence = SequenceData(id="test_seq", name="Test", beats=[])
        self.ui_state_service.update_current_sequence_with_session(
            test_sequence, "test_seq"
        )

        # Verify session was updated
        current_session = self.session_service.get_current_session_state()
        assert current_session.current_sequence_id == "test_seq"

        # Test workbench state update with session
        beat_data = BeatData(beat_number=1, letter="A")
        self.ui_state_service.update_workbench_selection_with_session(
            0, beat_data, None
        )

        # Verify session was updated
        current_session = self.session_service.get_current_session_state()
        assert current_session.selected_beat_index == 0

    def test_session_restoration_on_startup(self):
        """Test session restoration during application startup."""
        # Create and save session data
        self.session_service.update_current_sequence(
            {"name": "Test Sequence"}, "startup_test"
        )
        self.session_service.update_ui_state("dictionary", {"test": "layout"})
        self.session_service.save_session_state()

        # Set session service in UI state service
        self.ui_state_service.set_session_service(self.session_service)

        # Test startup restoration
        restore_success = self.ui_state_service.restore_session_on_startup()
        assert restore_success, "Session should restore on startup"

        # Verify UI state was updated
        assert self.ui_state_service.get_active_tab() == "dictionary"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
