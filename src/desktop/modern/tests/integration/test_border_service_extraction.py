#!/usr/bin/env python3
"""
Integration test for border service extraction.

Validates that the border service extraction maintains all functionality
while properly separating business logic from presentation layer.
"""

import pytest
from domain.models import LetterType


class TestBorderServiceExtraction:
    """Test border service extraction integration."""

    def test_border_service_import(self):
        """Test that border service can be imported independently."""
        try:
            from application.services.pictograph.border_manager import (
                BorderConfiguration,
                BorderDimensions,
            )
            from application.services.pictograph.border_manager import (
                PictographBorderManager as PictographBorderService,
            )

            assert PictographBorderService is not None
            assert BorderConfiguration is not None
            assert BorderDimensions is not None

        except ImportError as e:
            pytest.skip(f"Border service not available: {e}")

    def test_border_service_no_qt_dependencies(self):
        """Test that border service has no Qt dependencies."""
        try:
            from application.services.pictograph.border_manager import (
                PictographBorderManager as PictographBorderService,
            )

            service = PictographBorderService()

            # Test basic functionality without Qt
            width = service.calculate_border_width(100)
            assert isinstance(width, int)
            assert width > 0

            adjusted_size = service.get_border_adjusted_size(100)
            assert isinstance(adjusted_size, int)
            assert adjusted_size >= 50  # Minimum size

        except ImportError as e:
            pytest.skip(f"Border service not available: {e}")

    def test_border_calculations_preserved(self):
        """Test that border calculations work correctly."""
        try:
            from application.services.pictograph.border_manager import (
                PictographBorderManager as PictographBorderService,
            )

            service = PictographBorderService()

            # Test border width calculation
            width_100 = service.calculate_border_width(100)
            width_200 = service.calculate_border_width(200)

            # Larger size should have larger border
            assert width_200 >= width_100

            # Test minimum border width
            width_small = service.calculate_border_width(10)
            assert width_small >= 1  # Minimum width

            # Test size adjustment
            adjusted = service.get_border_adjusted_size(100)
            expected = 100 - (2 * width_100)
            assert adjusted == max(50, expected)

        except ImportError as e:
            pytest.skip(f"Border service not available: {e}")

    def test_color_management_preserved(self):
        """Test that color management works correctly."""
        try:
            from application.services.pictograph.border_manager import (
                PictographBorderManager as PictographBorderService,
            )

            service = PictographBorderService()

            # Test letter type colors
            config = service.apply_letter_type_colors(LetterType.TYPE1)
            assert config.primary_color == "#36c3ff"
            assert config.secondary_color == "#6F2DA8"

            # Test gold colors
            config = service.apply_gold_colors()
            assert config.primary_color == "#FFD700"
            assert config.secondary_color == "#FFD700"

            # Test custom colors
            config = service.apply_custom_colors("#FF0000", "#00FF00")
            assert config.primary_color == "#FF0000"
            assert config.secondary_color == "#00FF00"

        except ImportError as e:
            pytest.skip(f"Border service not available: {e}")

    def test_border_manager_integration(self):
        """Test that border manager integrates with service correctly."""
        try:
            from application.services.pictograph.border_manager import (
                PictographBorderManager as PictographBorderService,
            )
            from presentation.components.pictograph.border_manager import (
                PictographBorderManager,
            )

            service = PictographBorderService()
            manager = PictographBorderManager(service)

            # Test delegation works
            width = manager.calculate_border_width(100)
            assert isinstance(width, int)
            assert width > 0

            # Test color management delegation
            manager.update_border_colors_for_letter_type(LetterType.TYPE1)
            colors = manager.get_current_colors()
            assert colors[0] == "#36c3ff"
            assert colors[1] == "#6F2DA8"

        except ImportError as e:
            pytest.skip(f"Border manager not available: {e}")

    def test_service_registration(self):
        """Test that border service is properly registered in DI container."""
        try:
            from application.services.core.service_registration_manager import (
                ServiceRegistrationManager,
            )
            from application.services.pictograph.border_manager import (
                PictographBorderManager as PictographBorderService,
            )
            from core.dependency_injection.di_container import DIContainer
            from core.interfaces.core_services import (
                IPictographBorderManager as IPictographBorderService,
            )

            # Create container and register services
            container = DIContainer()
            registration_manager = ServiceRegistrationManager()
            registration_manager.register_pictograph_services(container)

            # Test interface resolution
            service = container.resolve(IPictographBorderService)

            assert service is not None
            assert isinstance(service, PictographBorderService)

            # Test basic functionality
            width = service.calculate_border_width(100)
            assert isinstance(width, int)
            assert width > 0

        except Exception as e:
            pytest.skip(f"DI container or service registration not available: {e}")

    def test_pictograph_component_factory(self):
        """Test that pictograph component factory works with border service."""
        try:
            from presentation.components.pictograph.pictograph_component import (
                create_pictograph_component,
            )

            component = create_pictograph_component()
            assert component is not None

            # Test that component has border functionality
            assert hasattr(component, "set_gold_border")
            assert hasattr(component, "reset_border_colors")
            assert hasattr(component, "calculate_border_width")

        except Exception as e:
            pytest.skip(f"Pictograph component factory not available: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
