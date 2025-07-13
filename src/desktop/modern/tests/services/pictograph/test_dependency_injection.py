"""
Unit tests demonstrating dependency injection fixes for pictograph services.

These tests prove that the services are now properly testable and flexible
by mocking their dependencies instead of relying on hard-coded implementations.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import pandas as pd
from typing import Dict, Any, List

from application.services.pictograph.pictograph_position_matcher import PictographPositionMatcher
from application.services.pictograph.pictograph_validator import PictographValidator
from application.services.pictograph.visibility_state_manager import VisibilityStateManager
from application.services.pictograph.arrow_rendering_service import ArrowRenderingService
from domain.models.pictograph_data import PictographData
from domain.models.enums import Orientation
from domain.models.motion_data import MotionData


class TestPictographPositionMatcherDI(unittest.TestCase):
    """Test that PictographPositionMatcher properly uses dependency injection."""

    def setUp(self):
        """Set up test fixtures."""
        # Create mock CSV manager
        self.mock_csv_manager = Mock()
        
        # Create test dataframe
        self.test_df = pd.DataFrame({
            'start_pos': ['alpha1', 'alpha1', 'beta2', 'gamma3'],
            'letter': ['A', 'B', 'C', 'D'],
            'motion_type': ['pro', 'anti', 'pro', 'static']
        })
        
        # Configure mock to return test data
        self.mock_csv_manager._load_csv_data.return_value = self.test_df

    def test_uses_injected_csv_manager(self):
        """Test that the service uses the injected CSV manager instead of creating its own."""
        # Create service with mocked dependency
        matcher = PictographPositionMatcher(csv_manager=self.mock_csv_manager)
        
        # Verify the mock was used
        self.mock_csv_manager._load_csv_data.assert_called_once()
        self.assertIs(matcher.csv_manager, self.mock_csv_manager)

    def test_fallback_to_default_csv_manager(self):
        """Test that service creates default CSV manager when none provided."""
        with patch('application.services.pictograph.pictograph_position_matcher.PictographCSVManager') as mock_class:
            mock_instance = Mock()
            mock_class.return_value = mock_instance
            mock_instance._load_csv_data.return_value = self.test_df
            
            # Create service without dependency
            matcher = PictographPositionMatcher()
            
            # Verify default was created
            mock_class.assert_called_once()
            self.assertIs(matcher.csv_manager, mock_instance)

    def test_dataset_loading_with_mock(self):
        """Test that dataset loading works with mocked CSV manager."""
        matcher = PictographPositionMatcher(csv_manager=self.mock_csv_manager)
        
        # Verify dataset was processed correctly
        self.assertIsNotNone(matcher.pictograph_dataset)
        self.assertIn('alpha1', matcher.pictograph_dataset)
        self.assertEqual(len(matcher.pictograph_dataset['alpha1']), 2)  # Two alpha1 entries

    def test_csv_manager_error_handling(self):
        """Test error handling when CSV manager fails."""
        # Configure mock to raise exception
        self.mock_csv_manager._load_csv_data.side_effect = Exception("CSV load failed")
        
        # Service should handle the error gracefully
        matcher = PictographPositionMatcher(csv_manager=self.mock_csv_manager)
        
        # Dataset should be empty dict when loading fails
        self.assertEqual(matcher.pictograph_dataset, {})


class TestPictographValidatorDI(unittest.TestCase):
    """Test that PictographValidator properly uses dependency injection."""

    def setUp(self):
        """Set up test fixtures."""
        # Create mock pictograph data
        self.mock_pictograph = Mock(spec=PictographData)
        self.mock_pictograph.letter = "A"
        
        # Create mock orientation calculator
        self.mock_orientation_calc = Mock()
        self.mock_orientation_calc.calculate_end_orientation.return_value = Orientation.OUT

    def test_uses_injected_orientation_calculator(self):
        """Test that validator uses injected orientation calculator."""
        validator = PictographValidator(
            pictograph_data=self.mock_pictograph,
            orientation_calculator=self.mock_orientation_calc
        )
        
        # Create mock motion data
        mock_motion = Mock(spec=MotionData)
        mock_motion.start_ori = Orientation.IN
        mock_motion.turns = 0.5
        
        # Call method that uses orientation calculator
        result = validator._get_arrow_end_orientation(mock_motion)
        
        # Verify injected calculator was used
        self.mock_orientation_calc.calculate_end_orientation.assert_called_once()
        self.assertEqual(result, Orientation.OUT)

    def test_fallback_orientation_calculator(self):
        """Test fallback when no orientation calculator is provided."""
        validator = PictographValidator(pictograph_data=self.mock_pictograph)
        
        # Verify orientation_calculator is None (will use fallback)
        self.assertIsNone(validator.orientation_calculator)
        
        # The method should still work with fallback creation
        mock_motion = Mock(spec=MotionData)
        with patch('application.services.positioning.arrows.calculation.orientation_calculator.OrientationCalculator') as mock_calc_class:
            mock_calc_instance = Mock()
            mock_calc_class.return_value = mock_calc_instance
            mock_calc_instance.calculate_end_orientation.return_value = Orientation.OUT
            
            result = validator._get_arrow_end_orientation(mock_motion)
            
            # Verify fallback calculator was created and used
            mock_calc_class.assert_called_once()
            self.assertEqual(result, Orientation.OUT)

    def test_pictograph_data_validation(self):
        """Test that validator properly handles pictograph data."""
        validator = PictographValidator(pictograph_data=self.mock_pictograph)
        
        # Verify pictograph data is stored
        self.assertIs(validator.pictograph_data, self.mock_pictograph)


class TestVisibilityStateManagerDI(unittest.TestCase):
    """Test that VisibilityStateManager properly uses dependency injection."""

    def setUp(self):
        """Set up test fixtures."""
        # Create mock visibility service
        self.mock_visibility_service = Mock()
        
        # Create mock global visibility service
        self.mock_global_service = Mock()

    def test_uses_injected_global_service(self):
        """Test that manager uses injected global visibility service."""
        manager = VisibilityStateManager(
            visibility_service=self.mock_visibility_service,
            global_visibility_service=self.mock_global_service
        )
        
        # Verify injected global service is used
        self.assertIs(manager._global_service, self.mock_global_service)

    def test_fallback_global_service_creation(self):
        """Test fallback when no global service is provided."""
        with patch.object(VisibilityStateManager, '_get_global_service') as mock_get_global:
            mock_get_global.return_value = self.mock_global_service
            
            manager = VisibilityStateManager(visibility_service=self.mock_visibility_service)
            
            # Verify fallback method was called
            mock_get_global.assert_called_once()
            self.assertIs(manager._global_service, self.mock_global_service)

    def test_required_visibility_service(self):
        """Test that visibility service is properly stored."""
        manager = VisibilityStateManager(
            visibility_service=self.mock_visibility_service,
            global_visibility_service=self.mock_global_service
        )
        
        # Verify required service is stored
        self.assertIs(manager.visibility_service, self.mock_visibility_service)


class TestArrowRenderingServiceDI(unittest.TestCase):
    """Test that ArrowRenderingService properly uses dependency injection."""

    def setUp(self):
        """Set up test fixtures."""
        # Create mock asset manager
        self.mock_asset_manager = Mock()
        self.mock_asset_manager.get_arrow_svg_path.return_value = "/path/to/arrow.svg"

    def test_uses_injected_asset_manager(self):
        """Test that service uses injected asset manager."""
        service = ArrowRenderingService(asset_manager=self.mock_asset_manager)
        
        # Verify injected asset manager is used
        self.assertIs(service.asset_manager, self.mock_asset_manager)

    def test_fallback_asset_manager_creation(self):
        """Test fallback when no asset manager is provided."""
        with patch('application.services.pictograph.arrow_rendering_service.AssetManager') as mock_asset_class:
            mock_asset_instance = Mock()
            mock_asset_class.return_value = mock_asset_instance
            
            service = ArrowRenderingService()
            
            # Verify default asset manager was created
            mock_asset_class.assert_called_once()
            self.assertIs(service.asset_manager, mock_asset_instance)

    def test_asset_manager_integration(self):
        """Test that asset manager is properly integrated."""
        service = ArrowRenderingService(asset_manager=self.mock_asset_manager)
        
        # Create mock motion data
        mock_motion = Mock(spec=MotionData)
        
        # Test that asset manager methods can be called
        result = service.get_arrow_svg_path(mock_motion, "blue")
        
        # Verify asset manager was used
        self.mock_asset_manager.get_arrow_svg_path.assert_called_once()
        self.assertEqual(result, "/path/to/arrow.svg")


class TestDependencyInjectionBenefits(unittest.TestCase):
    """Integration tests demonstrating the benefits of dependency injection."""

    def test_different_implementations_same_interface(self):
        """Test that we can swap implementations easily."""
        # Create two different mock CSV managers
        csv_manager_1 = Mock()
        csv_manager_1._load_csv_data.return_value = pd.DataFrame({'start_pos': ['alpha1']})
        
        csv_manager_2 = Mock()
        csv_manager_2._load_csv_data.return_value = pd.DataFrame({'start_pos': ['beta2']})
        
        # Create two matchers with different implementations
        matcher_1 = PictographPositionMatcher(csv_manager=csv_manager_1)
        matcher_2 = PictographPositionMatcher(csv_manager=csv_manager_2)
        
        # Verify they use different data sources
        self.assertIn('alpha1', matcher_1.pictograph_dataset)
        self.assertIn('beta2', matcher_2.pictograph_dataset)
        self.assertNotIn('beta2', matcher_1.pictograph_dataset)
        self.assertNotIn('alpha1', matcher_2.pictograph_dataset)

    def test_error_isolation(self):
        """Test that errors in dependencies don't crash the service."""
        # Create failing mock
        failing_csv_manager = Mock()
        failing_csv_manager._load_csv_data.side_effect = Exception("Network error")
        
        # Service should handle the error gracefully
        matcher = PictographPositionMatcher(csv_manager=failing_csv_manager)
        
        # Service should still be usable (with empty dataset)
        self.assertEqual(matcher.pictograph_dataset, {})
        self.assertIsNotNone(matcher.csv_manager)


if __name__ == '__main__':
    unittest.main()
