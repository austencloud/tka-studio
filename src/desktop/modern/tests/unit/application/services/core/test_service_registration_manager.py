"""
Unit tests for ServiceRegistrationManager

Tests the pure service registration manager.
Validates extraction from KineticConstructorModern maintains functionality.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add modern/src to path for imports
modern_src_path = Path(__file__).parent.parent.parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

from application.services.core.service_registration_manager import (
    ServiceRegistrationManager,
    IServiceRegistrationManager,
)


class TestServiceRegistrationManager:
    """Test suite for ServiceRegistrationManager."""

    def setup_method(self):
        """Set up test fixtures."""
        self.progress_messages = []

        def mock_progress_callback(message: str):
            self.progress_messages.append(message)

        self.service = ServiceRegistrationManager(
            progress_callback=mock_progress_callback
        )
        self.mock_container = Mock()

    def test_interface_compliance(self):
        """Test that ServiceRegistrationManager implements the interface correctly."""
        assert isinstance(self.service, IServiceRegistrationManager)

    def test_progress_callback_functionality(self):
        """Test that progress callback is called correctly."""
        # Clear previous messages
        self.progress_messages.clear()

        # Call a method that should trigger progress updates
        self.service._update_progress("Test message")

        # Verify callback was called
        assert "Test message" in self.progress_messages

    def test_register_event_system_success(self):
        """Test successful event system registration."""
        with patch(
            "application.services.core.service_registration_manager.get_event_bus"
        ) as mock_get_bus:
            mock_event_bus = Mock()
            mock_get_bus.return_value = mock_event_bus

            # Test registration
            self.service.register_event_system(self.mock_container)

            # Verify container registration calls
            assert self.mock_container.register_instance.call_count >= 1

    def test_register_event_system_import_error(self):
        """Test event system registration with import error."""
        with patch(
            "application.services.core.service_registration_manager.get_event_bus",
            side_effect=ImportError("No module"),
        ):
            # Should not raise exception
            self.service.register_event_system(self.mock_container)

            # Should continue gracefully without registering

    def test_register_core_services(self):
        """Test core services registration."""
        # Mock the container resolve method
        self.mock_container.resolve.return_value = Mock()

        # Test registration
        self.service.register_core_services(self.mock_container)

        # Verify factory registration calls
        assert self.mock_container.register_factory.call_count >= 2

    def test_register_motion_services(self):
        """Test motion services registration."""
        # Test registration
        self.service.register_motion_services(self.mock_container)

        # Verify singleton registration calls
        assert self.mock_container.register_singleton.call_count >= 2

    def test_register_layout_services(self):
        """Test layout services registration (should be no-op)."""
        # Test registration - should not raise exception
        self.service.register_layout_services(self.mock_container)

        # Layout services are consolidated, so this should be a no-op

    def test_register_pictograph_services(self):
        """Test pictograph services registration."""
        # Test registration
        self.service.register_pictograph_services(self.mock_container)

        # Verify singleton registration calls
        assert self.mock_container.register_singleton.call_count >= 2

    def test_register_workbench_services(self):
        """Test workbench services registration."""
        with patch(
            "application.services.core.service_registration_manager.configure_workbench_services"
        ) as mock_configure:
            # Test registration
            self.service.register_workbench_services(self.mock_container)

            # Verify configure function was called
            mock_configure.assert_called_once_with(self.mock_container)

    def test_register_positioning_services(self):
        """Test positioning services registration."""
        # Test registration
        self.service.register_positioning_services(self.mock_container)

        # Verify singleton registration calls for orchestrators
        assert self.mock_container.register_singleton.call_count >= 3

    def test_register_data_services(self):
        """Test data services registration."""
        # Test registration
        self.service.register_data_services(self.mock_container)

        # Verify singleton registration calls
        assert self.mock_container.register_singleton.call_count >= 2

    def test_register_all_services_sequence(self):
        """Test that register_all_services calls all registration methods."""
        # Clear progress messages
        self.progress_messages.clear()

        with (
            patch.object(self.service, "register_event_system") as mock_event,
            patch.object(self.service, "register_core_services") as mock_core,
            patch.object(self.service, "register_motion_services") as mock_motion,
            patch.object(self.service, "register_layout_services") as mock_layout,
            patch.object(
                self.service, "register_pictograph_services"
            ) as mock_pictograph,
            patch.object(self.service, "register_workbench_services") as mock_workbench,
        ):
            # Test registration
            self.service.register_all_services(self.mock_container)

            # Verify all registration methods were called
            mock_event.assert_called_once_with(self.mock_container)
            mock_core.assert_called_once_with(self.mock_container)
            mock_motion.assert_called_once_with(self.mock_container)
            mock_layout.assert_called_once_with(self.mock_container)
            mock_pictograph.assert_called_once_with(self.mock_container)
            mock_workbench.assert_called_once_with(self.mock_container)

            # Verify progress messages
            assert "Configuring services..." in self.progress_messages
            assert "Services configured" in self.progress_messages

    def test_get_registration_status(self):
        """Test registration status reporting."""
        status = self.service.get_registration_status()

        assert isinstance(status, dict)
        assert "event_system_available" in status
        assert "services_registered" in status

    def test_service_registration_with_no_progress_callback(self):
        """Test service registration without progress callback."""
        service_no_callback = ServiceRegistrationManager()

        # Should not raise exception when calling _update_progress
        service_no_callback._update_progress("Test message")

    def test_factory_function_creation(self):
        """Test that factory functions are created correctly."""
        # Mock the container resolve method
        mock_event_bus = Mock()
        self.mock_container.resolve.return_value = mock_event_bus

        # Test core services registration
        self.service.register_core_services(self.mock_container)

        # Verify factory functions were registered
        assert self.mock_container.register_factory.call_count >= 2

        # Get the factory function calls
        factory_calls = self.mock_container.register_factory.call_args_list

        # Verify factory functions can be called
        for call in factory_calls:
            interface, factory_func = call[0]
            # Factory function should be callable
            assert callable(factory_func)

    def test_error_handling_in_registration(self):
        """Test error handling during service registration."""
        # Mock container to raise exception
        self.mock_container.register_singleton.side_effect = Exception(
            "Registration failed"
        )

        # Should handle exceptions gracefully
        try:
            self.service.register_motion_services(self.mock_container)
        except Exception:
            pytest.fail("Service registration should handle exceptions gracefully")

    def test_registration_order_dependency(self):
        """Test that services are registered in correct dependency order."""
        call_order = []

        def track_calls(method_name):
            def wrapper(*args, **kwargs):
                call_order.append(method_name)
                return Mock()

            return wrapper

        with (
            patch.object(
                self.service, "register_event_system", side_effect=track_calls("event")
            ),
            patch.object(
                self.service, "register_core_services", side_effect=track_calls("core")
            ),
            patch.object(
                self.service,
                "register_motion_services",
                side_effect=track_calls("motion"),
            ),
            patch.object(
                self.service,
                "register_layout_services",
                side_effect=track_calls("layout"),
            ),
            patch.object(
                self.service,
                "register_pictograph_services",
                side_effect=track_calls("pictograph"),
            ),
            patch.object(
                self.service,
                "register_workbench_services",
                side_effect=track_calls("workbench"),
            ),
        ):
            self.service.register_all_services(self.mock_container)

            # Verify correct order
            expected_order = [
                "event",
                "core",
                "motion",
                "layout",
                "pictograph",
                "workbench",
            ]
            assert call_order == expected_order


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
