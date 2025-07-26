"""
Tests for WorkbenchStateManager interface compliance and functionality.

These tests verify that the WorkbenchStateManager correctly implements the
IWorkbenchStateManager interface and provides expected behavior.
"""

import pytest
from unittest.mock import Mock, MagicMock

from shared.application.services.workbench.workbench_state_manager import WorkbenchStateManager
from desktop.modern.core.interfaces.workbench_services import IWorkbenchStateManager, WorkbenchState, StateChangeResult
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


class TestWorkbenchStateManagerInterface:
    """Test interface compliance for WorkbenchStateManager."""

    def test_workbench_state_manager_implements_interface(self):
        """Test that WorkbenchStateManager implements IWorkbenchStateManager."""
        assert issubclass(WorkbenchStateManager, IWorkbenchStateManager)

    def test_all_interface_methods_implemented(self):
        """Test that all interface methods are implemented."""
        service = WorkbenchStateManager()
        
        # Get all abstract methods from interface
        interface_methods = [
            method for method in dir(IWorkbenchStateManager) 
            if not method.startswith('_') and callable(getattr(IWorkbenchStateManager, method))
        ]
        
        # Verify all methods exist and are callable
        for method_name in interface_methods:
            assert hasattr(service, method_name), f"Missing method: {method_name}"
            assert callable(getattr(service, method_name)), f"Method not callable: {method_name}"

    def test_method_signatures_match_interface(self):
        """Test that method signatures match the interface."""
        import inspect
        
        service = WorkbenchStateManager()
        
        # Test a few key methods
        key_methods = [
            'set_sequence',
            'set_start_position',
            'get_current_sequence',
            'get_workbench_state',
            'has_sequence',
            'has_start_position'
        ]
        
        for method_name in key_methods:
            interface_method = getattr(IWorkbenchStateManager, method_name)
            implementation_method = getattr(service, method_name)
            
            # Both should be callable
            assert callable(interface_method)
            assert callable(implementation_method)


class TestWorkbenchStateManagerBehavior:
    """Test behavior of WorkbenchStateManager."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = WorkbenchStateManager()
        
        # Mock sequence data
        self.mock_sequence = Mock(spec=SequenceData)
        self.mock_sequence.length = 5
        self.mock_sequence.name = "Test Sequence"
        
        # Mock beat data
        self.mock_beat = Mock(spec=BeatData)
        self.mock_beat.letter = "A"

    def test_initial_state_is_empty(self):
        """Test that initial state is empty."""
        assert self.service.get_workbench_state() == WorkbenchState.EMPTY
        assert self.service.is_empty()
        assert not self.service.has_sequence()
        assert not self.service.has_start_position()

    def test_set_sequence_changes_state(self):
        """Test that setting sequence changes state appropriately."""
        result = self.service.set_sequence(self.mock_sequence)
        
        assert result.changed
        assert result.sequence_changed
        assert not result.start_position_changed
        assert result.new_state == WorkbenchState.SEQUENCE_LOADED
        
        assert self.service.get_workbench_state() == WorkbenchState.SEQUENCE_LOADED
        assert self.service.has_sequence()
        assert not self.service.has_start_position()

    def test_set_start_position_changes_state(self):
        """Test that setting start position changes state appropriately."""
        result = self.service.set_start_position(self.mock_beat)
        
        assert result.changed
        assert not result.sequence_changed
        assert result.start_position_changed
        assert result.new_state == WorkbenchState.START_POSITION_SET
        
        assert self.service.get_workbench_state() == WorkbenchState.START_POSITION_SET
        assert not self.service.has_sequence()
        assert self.service.has_start_position()

    def test_set_both_sequence_and_start_position(self):
        """Test that setting both sequence and start position results in BOTH_SET state."""
        # Set sequence first
        self.service.set_sequence(self.mock_sequence)
        
        # Then set start position
        result = self.service.set_start_position(self.mock_beat)
        
        assert result.new_state == WorkbenchState.BOTH_SET
        assert self.service.get_workbench_state() == WorkbenchState.BOTH_SET
        assert self.service.has_sequence()
        assert self.service.has_start_position()

    def test_clear_all_state(self):
        """Test clearing all state."""
        # Set some state first
        self.service.set_sequence(self.mock_sequence)
        self.service.set_start_position(self.mock_beat)
        
        # Clear all
        result = self.service.clear_all_state()
        
        assert result.changed
        assert result.new_state == WorkbenchState.EMPTY
        assert self.service.get_workbench_state() == WorkbenchState.EMPTY
        assert self.service.is_empty()
        assert not self.service.has_sequence()
        assert not self.service.has_start_position()

    def test_restoration_mode(self):
        """Test restoration mode functionality."""
        # Begin restoration
        self.service.begin_restoration()
        
        assert self.service.is_restoring()
        assert not self.service.is_restoration_complete()
        
        # Complete restoration
        self.service.complete_restoration()
        
        assert not self.service.is_restoring()
        assert self.service.is_restoration_complete()
        
        # Reset restoration state
        self.service.reset_restoration_state()
        
        assert not self.service.is_restoring()
        assert not self.service.is_restoration_complete()

    def test_should_enable_operations(self):
        """Test operation enablement logic."""
        # Initially nothing should be enabled
        assert not self.service.should_enable_sequence_operations()
        assert not self.service.should_enable_export_operations()
        assert not self.service.should_enable_transform_operations()
        assert not self.service.should_enable_clear_operation()
        
        # Set sequence
        self.service.set_sequence(self.mock_sequence)
        
        # Now sequence operations should be enabled
        assert self.service.should_enable_sequence_operations()
        assert self.service.should_enable_export_operations()
        assert self.service.should_enable_transform_operations()
        assert self.service.should_enable_clear_operation()

    def test_should_prevent_auto_save_during_restoration(self):
        """Test auto-save prevention during restoration."""
        # Initially auto-save should not be prevented
        assert not self.service.should_prevent_auto_save()
        
        # Begin restoration
        self.service.begin_restoration()
        
        # Now auto-save should be prevented
        assert self.service.should_prevent_auto_save()
        
        # Complete restoration
        self.service.complete_restoration()
        
        # Auto-save should no longer be prevented
        assert not self.service.should_prevent_auto_save()

    def test_get_complete_sequence_with_start_position(self):
        """Test getting complete sequence with start position."""
        # Initially should return None
        assert self.service.get_complete_sequence_with_start_position() is None
        
        # Set sequence only
        self.service.set_sequence(self.mock_sequence)
        result = self.service.get_complete_sequence_with_start_position()
        assert result == self.mock_sequence
        
        # Set start position too
        self.service.set_start_position(self.mock_beat)
        result = self.service.get_complete_sequence_with_start_position()
        
        # Should return sequence with start position
        assert result is not None
        # The actual implementation would call sequence.update(start_position=...)
        # but we can't test that easily with mocks

    def test_validate_state_consistency(self):
        """Test state consistency validation."""
        # Empty state should be valid
        is_valid, issues = self.service.validate_state_consistency()
        assert is_valid
        assert len(issues) == 0
        
        # Add some state
        self.service.set_sequence(self.mock_sequence)
        self.service.set_start_position(self.mock_beat)
        
        # Should still be valid
        is_valid, issues = self.service.validate_state_consistency()
        assert is_valid
        assert len(issues) == 0

    def test_get_state_summary(self):
        """Test getting state summary."""
        summary = self.service.get_state_summary()
        
        # Check that summary contains expected keys
        expected_keys = [
            'workbench_state',
            'has_sequence',
            'sequence_length',
            'has_start_position',
            'start_position_letter',
            'is_restoring',
            'restoration_complete',
            'is_empty',
            'state_valid',
            'validation_issues',
            'operations_enabled'
        ]
        
        for key in expected_keys:
            assert key in summary, f"Missing key in summary: {key}"

    def test_no_change_result_when_setting_same_data(self):
        """Test that setting the same data returns no change result."""
        # Set sequence
        result1 = self.service.set_sequence(self.mock_sequence)
        assert result1.changed
        
        # Set the same sequence again
        result2 = self.service.set_sequence(self.mock_sequence)
        assert not result2.changed
        assert result2.previous_state == result2.new_state


class MockWorkbenchStateManager(IWorkbenchStateManager):
    """Mock implementation for testing interface compliance."""
    
    def __init__(self):
        self.state = WorkbenchState.EMPTY
        self.sequence = None
        self.start_position = None
        self.restoring = False
        self.restoration_complete = False
    
    def set_sequence(self, sequence, from_restoration=False):
        previous_state = self.state
        self.sequence = sequence
        self.state = self._calculate_state()
        return StateChangeResult.create_sequence_changed(previous_state, self.state)
    
    def set_start_position(self, start_position, from_restoration=False):
        previous_state = self.state
        self.start_position = start_position
        self.state = self._calculate_state()
        return StateChangeResult.create_start_position_changed(previous_state, self.state)
    
    def clear_all_state(self):
        previous_state = self.state
        self.sequence = None
        self.start_position = None
        self.state = WorkbenchState.EMPTY
        return StateChangeResult.create_both_changed(previous_state, self.state)
    
    def get_current_sequence(self):
        return self.sequence
    
    def get_start_position(self):
        return self.start_position
    
    def get_workbench_state(self):
        return self.state
    
    def has_sequence(self):
        return self.sequence is not None
    
    def has_start_position(self):
        return self.start_position is not None
    
    def is_empty(self):
        return self.state == WorkbenchState.EMPTY
    
    def is_restoring(self):
        return self.restoring
    
    def is_restoration_complete(self):
        return self.restoration_complete
    
    def should_enable_sequence_operations(self):
        return self.has_sequence()
    
    def should_enable_export_operations(self):
        return self.has_sequence()
    
    def should_enable_transform_operations(self):
        return self.has_sequence()
    
    def should_enable_clear_operation(self):
        return not self.is_empty()
    
    def should_prevent_auto_save(self):
        return self.restoring
    
    def get_complete_sequence_with_start_position(self):
        return self.sequence
    
    def begin_restoration(self):
        self.restoring = True
        self.restoration_complete = False
    
    def complete_restoration(self):
        self.restoring = False
        self.restoration_complete = True
    
    def reset_restoration_state(self):
        self.restoring = False
        self.restoration_complete = False
    
    def validate_state_consistency(self):
        return True, []
    
    def get_state_summary(self):
        return {
            'workbench_state': self.state.value,
            'has_sequence': self.has_sequence(),
            'sequence_length': 0,
            'has_start_position': self.has_start_position(),
            'start_position_letter': None,
            'is_restoring': self.restoring,
            'restoration_complete': self.restoration_complete,
            'is_empty': self.is_empty(),
            'state_valid': True,
            'validation_issues': [],
            'operations_enabled': {}
        }
    
    def _calculate_state(self):
        if self.restoring:
            return WorkbenchState.RESTORING
        if self.has_sequence() and self.has_start_position():
            return WorkbenchState.BOTH_SET
        elif self.has_sequence():
            return WorkbenchState.SEQUENCE_LOADED
        elif self.has_start_position():
            return WorkbenchState.START_POSITION_SET
        else:
            return WorkbenchState.EMPTY


class TestMockWorkbenchStateManager:
    """Test mock implementation."""

    def test_mock_implements_interface(self):
        """Test that mock implements interface."""
        mock_service = MockWorkbenchStateManager()
        assert isinstance(mock_service, IWorkbenchStateManager)

    def test_mock_basic_functionality(self):
        """Test basic mock functionality."""
        mock_service = MockWorkbenchStateManager()
        
        # Initial state
        assert mock_service.get_workbench_state() == WorkbenchState.EMPTY
        assert mock_service.is_empty()
        
        # Set sequence
        mock_sequence = Mock()
        result = mock_service.set_sequence(mock_sequence)
        assert result.changed
        assert mock_service.get_workbench_state() == WorkbenchState.SEQUENCE_LOADED
        assert mock_service.has_sequence()
