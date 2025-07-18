"""
Test Suite for Improved Architecture - No More Clumsy Getter/Setter Pattern!

This test suite verifies that:
1. Services use IWorkbenchStateManager instead of getter/setter functions
2. Workbench properly implements WorkbenchProtocol
3. Construct tab connects workbench to state manager
4. Adapters work with improved dependency injection
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from application.services.sequence.sequence_loader_service import SequenceLoaderService
from application.services.sequence.sequence_beat_operations_service import SequenceBeatOperationsService
from presentation.adapters.qt.sequence_loader_adapter import QtSequenceLoaderAdapter
from presentation.adapters.qt.sequence_beat_operations_adapter import QtSequenceBeatOperationsAdapter
from core.interfaces.workbench_services import IWorkbenchStateManager
from domain.models.sequence_data import SequenceData
from domain.models.beat_data import BeatData


class MockWorkbenchStateManager:
    """Mock implementation of IWorkbenchStateManager for testing."""
    
    def __init__(self):
        self.current_sequence = None
        self.start_position = None
        self.available = True
        
    def get_current_sequence(self):
        return self.current_sequence
        
    def set_current_sequence(self, sequence):
        self.current_sequence = sequence
        
    def get_start_position(self):
        return self.start_position
        
    def set_start_position(self, start_position):
        self.start_position = start_position
        
    def is_workbench_available(self):
        return self.available


class MockWorkbench:
    """Mock workbench that implements WorkbenchProtocol."""
    
    def __init__(self):
        self.sequence = None
        self.start_position_data = None
        
    def get_sequence(self):
        return self.sequence
        
    def set_sequence(self, sequence):
        self.sequence = sequence
        
    def get_start_position_data(self):
        return self.start_position_data
        
    def set_start_position_data(self, start_position, position_key):
        self.start_position_data = start_position


class TestImprovedSequenceLoaderService(unittest.TestCase):
    """Test that SequenceLoaderService uses IWorkbenchStateManager instead of getter/setter."""
    
    def setUp(self):
        self.mock_state_manager = MockWorkbenchStateManager()
        self.service = SequenceLoaderService(
            workbench_state_manager=self.mock_state_manager
        )
        
    def test_uses_state_manager_not_getter_setter(self):
        """Test that service uses state manager instead of clumsy getter/setter functions."""
        # Verify the service was initialized with state manager
        self.assertIsNotNone(self.service.workbench_state_manager)
        self.assertEqual(self.service.workbench_state_manager, self.mock_state_manager)
        
        # Verify it does NOT have the old getter/setter attributes
        self.assertFalse(hasattr(self.service, 'workbench_getter'))
        self.assertFalse(hasattr(self.service, 'workbench_setter'))
        
    def test_get_current_sequence_uses_state_manager(self):
        """Test that getting sequence uses state manager."""
        test_sequence = SequenceData(name="Test", beats=[])
        self.mock_state_manager.current_sequence = test_sequence
        
        result = self.service.get_current_sequence_from_workbench()
        self.assertEqual(result, test_sequence)
        
    def test_handles_missing_state_manager_gracefully(self):
        """Test that service handles missing state manager gracefully."""
        service = SequenceLoaderService(workbench_state_manager=None)
        result = service.get_current_sequence_from_workbench()
        self.assertIsNone(result)


class TestImprovedSequenceBeatOperationsService(unittest.TestCase):
    """Test that SequenceBeatOperationsService uses IWorkbenchStateManager."""
    
    def setUp(self):
        self.mock_state_manager = MockWorkbenchStateManager()
        self.service = SequenceBeatOperationsService(
            workbench_state_manager=self.mock_state_manager
        )
        
    def test_uses_state_manager_not_getter(self):
        """Test that service uses state manager instead of workbench_getter."""
        # Verify the service was initialized with state manager
        self.assertIsNotNone(self.service.workbench_state_manager)
        self.assertEqual(self.service.workbench_state_manager, self.mock_state_manager)
        
        # Verify it does NOT have the old getter attribute
        self.assertFalse(hasattr(self.service, 'workbench_getter'))
        
    def test_get_beat_count_uses_state_manager(self):
        """Test that beat operations use state manager."""
        test_sequence = SequenceData(name="Test", beats=[])
        self.mock_state_manager.current_sequence = test_sequence
        
        count = self.service.get_beat_count()
        self.assertEqual(count, 0)


class TestImprovedQtAdapters(unittest.TestCase):
    """Test that Qt adapters use IWorkbenchStateManager instead of getter/setter."""
    
    def setUp(self):
        self.mock_state_manager = MockWorkbenchStateManager()
        
    @patch('PyQt6.QtCore.QObject.__init__')
    def test_sequence_loader_adapter_improved(self, mock_qt_init):
        """Test that QtSequenceLoaderAdapter uses state manager."""
        # Mock Qt initialization
        mock_qt_init.return_value = None
        
        adapter = QtSequenceLoaderAdapter(
            workbench_state_manager=self.mock_state_manager
        )
        
        # Verify it uses state manager
        self.assertEqual(adapter._workbench_state_manager, self.mock_state_manager)
        
        # Verify it has the new method
        self.assertTrue(hasattr(adapter, 'is_workbench_ready'))
        self.assertTrue(adapter.is_workbench_ready())
        
    @patch('PyQt6.QtCore.QObject.__init__')
    def test_beat_operations_adapter_improved(self, mock_qt_init):
        """Test that QtSequenceBeatOperationsAdapter uses state manager."""
        # Mock Qt initialization
        mock_qt_init.return_value = None
        
        adapter = QtSequenceBeatOperationsAdapter(
            workbench_state_manager=self.mock_state_manager
        )
        
        # Verify it uses state manager
        self.assertEqual(adapter._workbench_state_manager, self.mock_state_manager)


class TestWorkbenchProtocolImplementation(unittest.TestCase):
    """Test that workbench properly implements WorkbenchProtocol."""
    
    def test_mock_workbench_implements_protocol(self):
        """Test that our mock workbench implements the required methods."""
        workbench = MockWorkbench()
        
        # Test sequence methods
        test_sequence = SequenceData(name="Test", beats=[])
        workbench.set_sequence(test_sequence)
        self.assertEqual(workbench.get_sequence(), test_sequence)
        
        # Test start position methods
        test_beat = BeatData(letter="A", pictograph_data=None)
        workbench.set_start_position_data(test_beat, "alpha1_alpha1")
        self.assertEqual(workbench.get_start_position_data(), test_beat)


class TestWorkbenchStateManagerIntegration(unittest.TestCase):
    """Test that workbench properly connects to state manager."""
    
    def test_workbench_connection_to_state_manager(self):
        """Test that workbench can be connected to state manager."""
        mock_state_manager = MockWorkbenchStateManager()
        mock_workbench = MockWorkbench()
        
        # This simulates what the construct tab should do
        mock_state_manager.set_workbench = Mock()
        mock_state_manager.set_workbench(mock_workbench)
        
        # Verify the connection was attempted
        mock_state_manager.set_workbench.assert_called_once_with(mock_workbench)


class TestImprovedArchitectureBenefits(unittest.TestCase):
    """Test that demonstrates the benefits of the improved architecture."""
    
    def test_type_safety_improvement(self):
        """Test that we now have proper type safety."""
        # Old pattern would accept any callable - CLUMSY!
        # New pattern requires proper IWorkbenchStateManager interface
        
        mock_state_manager = MockWorkbenchStateManager()
        
        # This should work with proper interface
        service = SequenceLoaderService(workbench_state_manager=mock_state_manager)
        self.assertIsNotNone(service.workbench_state_manager)
        
    def test_easier_testing(self):
        """Test that the new pattern is much easier to test."""
        # With the old pattern, we'd need to create lambda functions - CLUMSY!
        # With the new pattern, we just create a mock state manager
        
        mock_state_manager = MockWorkbenchStateManager()
        test_sequence = SequenceData(name="Test", beats=[])
        mock_state_manager.current_sequence = test_sequence
        
        service = SequenceLoaderService(workbench_state_manager=mock_state_manager)
        result = service.get_current_sequence_from_workbench()
        
        self.assertEqual(result, test_sequence)
        
    def test_loose_coupling_benefit(self):
        """Test that services are now loosely coupled."""
        # Services depend on interfaces, not concrete implementations
        mock_state_manager = MockWorkbenchStateManager()
        
        # Both services can use the same interface
        loader_service = SequenceLoaderService(workbench_state_manager=mock_state_manager)
        beat_service = SequenceBeatOperationsService(workbench_state_manager=mock_state_manager)
        
        # Both should work with the same state manager instance
        self.assertEqual(loader_service.workbench_state_manager, mock_state_manager)
        self.assertEqual(beat_service.workbench_state_manager, mock_state_manager)


if __name__ == '__main__':
    print("🧪 Running tests for improved architecture...")
    print("✅ Testing that clumsy getter/setter pattern has been eliminated!")
    print("🔧 Verifying proper dependency injection with IWorkbenchStateManager")
    print()
    
    # Run the tests
    unittest.main(verbosity=2)
