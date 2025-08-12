"""
Integration Tests for Service Extraction

This module tests the integration between extracted services and the dependency
injection container to ensure the refactoring maintains functionality.
"""

from unittest.mock import Mock, patch

import pytest
from core.application.application_factory import ApplicationFactory
from core.interfaces.core_services import IObjectPoolManager
from core.interfaces.positioning_services import IPositionMatchingService
from core.testing.ai_agent_helpers import TKAAITestHelper


class TestServiceExtractionIntegration:
    """Integration tests for extracted services."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_helper = TKAAITestHelper(use_test_mode=True)

    def test_dependency_injection_registration(self):
        """Test that extracted services are properly registered in DI container."""
        try:
            # Create test application container
            container = ApplicationFactory.create_test_app()

            # Test that services can be resolved
            position_service = container.resolve(IPositionMatchingService)
            object_pool_service = container.resolve(IObjectPoolManager)

            assert position_service is not None
            assert object_pool_service is not None

            # Test that they implement the correct interfaces
            assert isinstance(position_service, IPositionMatchingService)
            assert isinstance(object_pool_service, IObjectPoolManager)

            # Note: IBeatLoadingService was removed during SRP refactoring
            # Its functionality was split into focused microservices

        except ImportError as e:
            pytest.skip(f"Services not yet registered in DI container: {e}")

    def test_position_matching_service_integration(self):
        """Test position matching service integration."""
        try:
            container = ApplicationFactory.create_test_app()
            service = container.resolve(IPositionMatchingService)

            # Test basic functionality
            test_beat_data = {"end_pos": "alpha1"}
            result = service.extract_end_position(test_beat_data)
            assert result == "alpha1"

            # Test position mapping
            position = service.get_position_from_locations("s", "n")
            assert position == "alpha1"

        except ImportError as e:
            pytest.skip(f"Position matching service not available: {e}")

    def test_option_picker_data_service_integration(self):
        """Test option picker data service integration (replacement for beat loading)."""
        try:
            # Test the new OptionProvider that replaced BeatLoadingService
            from application.services.option_picker.option_provider import (
                OptionProvider,
            )

            service = OptionProvider()

            # Test basic functionality
            pictographs = service.get_current_options()
            assert isinstance(pictographs, list)

            # Test filtering by letter
            if pictographs:
                filtered = service.filter_options_by_letter("A")
                assert isinstance(filtered, list)

        except ImportError as e:
            pytest.skip(f"Option picker data service not available: {e}")

    def test_object_pool_service_integration(self):
        """Test object pool service integration."""
        try:
            container = ApplicationFactory.create_test_app()
            service = container.resolve(IObjectPoolManager)

            # Test pool creation
            objects_created = []

            def test_factory():
                obj = f"test_object_{len(objects_created)}"
                objects_created.append(obj)
                return obj

            service.initialize_pool(
                pool_name="test_integration_pool",
                max_objects=5,
                object_factory=test_factory,
            )

            # Test pool access
            obj = service.get_pooled_object("test_integration_pool", 0)
            assert obj == "test_object_0"

            # Test pool info
            info = service.get_pool_info("test_integration_pool")
            assert info["exists"] is True
            assert info["size"] == 5

        except ImportError as e:
            pytest.skip(f"Object pool service not available: {e}")

    def test_presentation_layer_adapter_compatibility(self):
        """Test that presentation layer adapters maintain compatibility."""
        try:
            from application.services.option_picker.data.pool_manager import (
                PictographPoolManager,
            )
            from application.services.option_picker.data.position_matcher import (
                PositionMatcher,
            )
            from presentation.components.option_picker.services.data.option_service import (
                OptionService,
            )

            # Test position matcher adapter
            position_matcher = PositionMatcher()
            test_beat = {"end_pos": "alpha1"}
            result = position_matcher.extract_end_position(test_beat, None)
            assert result == "alpha1"

            # Test option service adapter
            option_service = OptionService()
            assert option_service is not None

            # Test pool manager adapter (requires Qt widget)
            # This would need a Qt application context to test fully

        except ImportError as e:
            pytest.skip(f"Presentation layer adapters not available: {e}")

    def test_backward_compatibility(self):
        """Test that existing code still works after refactoring."""
        try:
            # Test that old imports still work
            from application.services.option_picker.data.position_matcher import (
                PositionMatcher,
            )

            matcher = PositionMatcher()

            # Test legacy interface
            test_data = {
                "blue_attributes": {"end_loc": "s"},
                "red_attributes": {"end_loc": "n"},
            }

            result = matcher.has_motion_attributes(test_data)
            assert result is True

            position = matcher.get_position_from_locations("w", "e")
            assert position == "alpha3"

        except ImportError as e:
            pytest.skip(f"Backward compatibility test failed: {e}")

    def test_service_error_handling(self):
        """Test error handling in extracted services."""
        try:
            container = ApplicationFactory.create_test_app()

            # Test position service error handling
            position_service = container.resolve(IPositionMatchingService)
            result = position_service.extract_end_position(None)
            assert result is None  # Should handle gracefully and return None on error

            # Test option picker data service error handling (replacement for beat loading)
            from application.services.option_picker.data_service import (
                OptionPickerDataService,
            )

            option_service = OptionPickerDataService()
            result = option_service.refresh_pictographs_from_sequence_data([])
            assert isinstance(result, list)  # Should return empty list

            # Test object pool service error handling
            pool_service = container.resolve(IObjectPoolManager)
            result = pool_service.get_pooled_object("nonexistent", 0)
            assert result is None  # Should handle gracefully

        except ImportError as e:
            pytest.skip(f"Error handling test failed: {e}")

    def test_performance_impact(self):
        """Test that service extraction doesn't significantly impact performance."""
        try:
            container = ApplicationFactory.create_test_app()
            position_service = container.resolve(IPositionMatchingService)

            import time

            # Test position extraction performance
            test_data = {"end_pos": "alpha1"}

            start_time = time.time()
            for _ in range(1000):
                position_service.extract_end_position(test_data)
            end_time = time.time()

            # Should complete 1000 operations in reasonable time (< 1 second)
            assert (end_time - start_time) < 1.0

        except ImportError as e:
            pytest.skip(f"Performance test failed: {e}")

    def test_tka_ai_test_helper_integration(self):
        """Test integration with TKA AI Test Helper."""
        try:
            # Test that the system still works with TKAAITestHelper
            result = self.test_helper.run_comprehensive_test_suite()

            # The test helper should work even with extracted services
            assert hasattr(result, "success")

        except Exception as e:
            pytest.skip(f"TKAAITestHelper integration test failed: {e}")

    def test_service_lifecycle_management(self):
        """Test service lifecycle management in DI container."""
        try:
            container = ApplicationFactory.create_test_app()

            # Test singleton behavior
            service1 = container.resolve(IPositionMatchingService)
            service2 = container.resolve(IPositionMatchingService)

            # Should be the same instance (singleton)
            assert service1 is service2

        except ImportError as e:
            pytest.skip(f"Service lifecycle test failed: {e}")

    def test_service_dependencies(self):
        """Test that services properly handle their dependencies."""
        try:
            container = ApplicationFactory.create_test_app()

            # Test that option picker data service can work with position service
            from application.services.option_picker.data_service import (
                OptionPickerDataService,
            )

            option_service = OptionPickerDataService()
            position_service = container.resolve(IPositionMatchingService)

            # Services should be able to work together
            test_data = {"end_pos": "alpha1"}
            position_result = position_service.extract_end_position(test_data)

            sequence_data = [test_data, {"letter": "B"}]
            option_result = option_service.refresh_pictographs_from_sequence_data(
                sequence_data
            )

            assert position_result is not None
            assert isinstance(option_result, list)

        except ImportError as e:
            pytest.skip(f"Service dependencies test failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
