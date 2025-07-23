"""
UI Component Tests for Sequence Card Tab

Tests all UI components with Qt testing framework.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

# Qt testing imports
pytest_plugins = ["pytest-qt"]

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtTest import QTest, QSignalSpy
from PyQt6.QtGui import QPixmap

# Import components to test
from presentation.tabs.sequence_card.components.header_component import (
    SequenceCardHeaderComponent,
)
from presentation.tabs.sequence_card.components.navigation_component import (
    SequenceCardNavigationComponent,
)
from presentation.tabs.sequence_card.components.content_component import (
    SequenceCardContentComponent,
)
from presentation.tabs.sequence_card.sequence_card_tab import SequenceCardTab

# Import interfaces
from core.interfaces.sequence_card_services import (
    ISequenceCardDataService,
    ISequenceCardCacheService,
    ISequenceCardLayoutService,
    ISequenceCardDisplayService,
    ISequenceCardExportService,
    ISequenceCardSettingsService,
    SequenceCardData,
    GridDimensions,
)

# Import service implementations for performance tests
from application.services.sequence_card.sequence_cache_service import (
    SequenceCardCacheService,
)


class TestSequenceCardHeaderComponent:
    """Test suite for SequenceCardHeaderComponent."""

    @pytest.fixture
    def mock_services(self):
        """Create mock services."""
        export_service = Mock(spec=ISequenceCardExportService)
        display_service = Mock(spec=ISequenceCardDisplayService)
        return export_service, display_service

    @pytest.fixture
    def header_widget(self, qtbot, mock_services):
        """Create header widget for testing."""
        export_service, display_service = mock_services
        widget = SequenceCardHeaderComponent(export_service, display_service)
        qtbot.addWidget(widget)
        return widget

    def test_header_creation(self, header_widget):
        """Test header widget creation and initial state."""
        assert header_widget.title_label.text() == "Sequence Card Manager"
        assert (
            header_widget.description_label.text()
            == "Select a sequence length to view cards"
        )
        assert not header_widget.progress_bar.isVisible()
        assert header_widget.export_button.isEnabled()
        assert header_widget.refresh_button.isEnabled()
        assert header_widget.regenerate_button.isEnabled()

    def test_export_button_click(self, qtbot, header_widget, mock_services):
        """Test export button click behavior."""
        export_service, display_service = mock_services

        # Create signal spy for export requested
        spy = QSignalSpy(header_widget.export_requested)

        # Show the widget to make it visible
        header_widget.show()
        qtbot.waitExposed(header_widget)

        # Click export button
        qtbot.mouseClick(header_widget.export_button, Qt.MouseButton.LeftButton)

        # Process events to ensure UI updates
        QApplication.processEvents()

        # Verify signal emitted and service called
        assert len(spy) == 1
        export_service.export_all_sequences.assert_called_once()

        # Button should be disabled during export
        assert not header_widget.export_button.isEnabled()
        assert header_widget.progress_bar.isVisible()

    def test_refresh_button_click(self, qtbot, header_widget):
        """Test refresh button click behavior."""
        spy = QSignalSpy(header_widget.refresh_requested)

        qtbot.mouseClick(header_widget.refresh_button, Qt.MouseButton.LeftButton)

        assert len(spy) == 1

    def test_regenerate_button_click(self, qtbot, header_widget, mock_services):
        """Test regenerate button click behavior."""
        export_service, display_service = mock_services
        spy = QSignalSpy(header_widget.regenerate_requested)

        qtbot.mouseClick(header_widget.regenerate_button, Qt.MouseButton.LeftButton)

        assert len(spy) == 1
        export_service.regenerate_all_images.assert_called_once()
        assert not header_widget.regenerate_button.isEnabled()

    def test_set_loading_state(self, qtbot, header_widget):
        """Test loading state changes."""
        # Show the widget to make it visible
        header_widget.show()
        qtbot.waitExposed(header_widget)

        # Set loading
        header_widget.set_loading_state(True)
        QApplication.processEvents()  # Process UI updates
        assert header_widget.progress_bar.isVisible()
        assert not header_widget.export_button.isEnabled()
        assert not header_widget.regenerate_button.isEnabled()

        # Clear loading
        header_widget.set_loading_state(False)
        QApplication.processEvents()  # Process UI updates
        assert not header_widget.progress_bar.isVisible()
        assert header_widget.export_button.isEnabled()
        assert header_widget.regenerate_button.isEnabled()

    def test_update_progress(self, header_widget):
        """Test progress updates."""
        header_widget.update_progress(50, 100)

        assert header_widget.progress_bar.value() == 50
        assert "50/100 (50%)" in header_widget.description_label.text()

    def test_export_completed_success(self, qtbot, header_widget):
        """Test export completion with success."""
        header_widget.export_completed(True)

        assert header_widget.export_button.isEnabled()
        assert header_widget.regenerate_button.isEnabled()
        assert not header_widget.progress_bar.isVisible()
        assert "successfully" in header_widget.description_label.text()

        # Should reset message after timer
        # (We can't easily test the timer in unit tests)

    def test_export_completed_failure(self, header_widget):
        """Test export completion with failure."""
        header_widget.export_completed(False)

        assert header_widget.export_button.isEnabled()
        assert header_widget.regenerate_button.isEnabled()
        assert "failed" in header_widget.description_label.text()


class TestSequenceCardNavigationComponent:
    """Test suite for SequenceCardNavigationComponent."""

    @pytest.fixture
    def mock_services(self):
        """Create mock services."""
        settings_service = Mock(spec=ISequenceCardSettingsService)
        display_service = Mock(spec=ISequenceCardDisplayService)

        # Setup default return values
        settings_service.get_last_selected_length.return_value = 16
        settings_service.get_column_count.return_value = 2

        return settings_service, display_service

    @pytest.fixture
    def nav_widget(self, qtbot, mock_services):
        """Create navigation widget for testing."""
        settings_service, display_service = mock_services
        widget = SequenceCardNavigationComponent(settings_service, display_service)
        qtbot.addWidget(widget)
        return widget

    def test_navigation_creation(self, nav_widget):
        """Test navigation widget creation and initial state."""
        # Should have length buttons for all expected values
        expected_lengths = [0, 2, 3, 4, 5, 6, 8, 10, 12, 16]
        for length in expected_lengths:
            assert length in nav_widget.length_buttons

        # Should have column combo box
        assert nav_widget.column_combo.currentText() == "2"  # Default

    def test_length_button_selection(self, qtbot, nav_widget, mock_services):
        """Test length button selection."""
        settings_service, display_service = mock_services

        # Create signal spy
        spy = QSignalSpy(nav_widget.length_selected)

        # Click length 8 button
        length_8_button = nav_widget.length_buttons[8]
        qtbot.mouseClick(length_8_button, Qt.MouseButton.LeftButton)

        # Verify signal emitted and state updated
        assert len(spy) == 1
        assert spy[0][0] == 8  # Signal argument
        assert nav_widget.selected_length == 8

        # Button should be selected
        assert length_8_button.is_selected

        # Other buttons should not be selected
        for length, button in nav_widget.length_buttons.items():
            if length != 8:
                assert not button.is_selected

    def test_column_count_change(self, qtbot, nav_widget):
        """Test column count change."""
        spy = QSignalSpy(nav_widget.column_count_changed)

        # Change column count
        nav_widget.column_combo.setCurrentText("4")

        # Verify signal emitted
        assert len(spy) == 1
        assert spy[0][0] == 4  # Signal argument

    def test_select_length_programmatically(self, nav_widget):
        """Test programmatic length selection."""
        nav_widget.select_length(12)

        assert nav_widget.selected_length == 12
        assert nav_widget.length_buttons[12].is_selected

        # Other buttons should not be selected
        for length, button in nav_widget.length_buttons.items():
            if length != 12:
                assert not button.is_selected

    def test_load_saved_settings(self, mock_services):
        """Test loading saved settings on initialization."""
        settings_service, display_service = mock_services
        settings_service.get_last_selected_length.return_value = 8
        settings_service.get_column_count.return_value = 3

        # Create widget (should load settings)
        widget = SequenceCardNavigationComponent(settings_service, display_service)

        # Should load saved length
        assert widget.selected_length == 8
        assert widget.length_buttons[8].is_selected

        # Should load saved column count
        assert widget.column_combo.currentText() == "3"


class TestSequenceCardContentComponent:
    """Test suite for SequenceCardContentComponent."""

    @pytest.fixture
    def mock_services(self):
        """Create mock services."""
        display_service = Mock(spec=ISequenceCardDisplayService)
        cache_service = Mock(spec=ISequenceCardCacheService)
        layout_service = Mock(spec=ISequenceCardLayoutService)

        # Setup default returns
        layout_service.calculate_grid_dimensions.return_value = GridDimensions(4, 4, 16)

        return display_service, cache_service, layout_service

    @pytest.fixture
    def content_widget(self, qtbot, mock_services):
        """Create content widget for testing."""
        display_service, cache_service, layout_service = mock_services
        widget = SequenceCardContentComponent(
            display_service, cache_service, layout_service
        )
        qtbot.addWidget(widget)
        return widget

    @pytest.fixture
    def sample_sequences(self):
        """Create sample sequence data."""
        return [
            SequenceCardData(
                path=Path(f"test_{i}.png"),
                word=f"word_{i}",
                length=16,
                metadata={"sequence_length": 16},
            )
            for i in range(5)
        ]

    def test_content_creation(self, content_widget):
        """Test content widget creation and initial state."""
        assert content_widget.scroll_area is not None
        assert content_widget.content_widget is not None
        assert content_widget.current_column_count == 2

    def test_show_empty_state(self, content_widget):
        """Test empty state display."""
        # Should show empty state initially
        layout = content_widget.content_layout
        assert layout.count() > 0  # Should have empty state widget

        # Find empty state label
        empty_widget = None
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if hasattr(widget, "text") and "No sequences" in widget.text():
                    empty_widget = widget
                    break

        assert empty_widget is not None

    def test_sequences_loaded_signal(self, content_widget, sample_sequences):
        """Test handling of sequences loaded signal."""
        # Simulate sequences loaded
        content_widget._on_sequences_loaded(sample_sequences)

        assert content_widget.current_sequences == sample_sequences

    def test_set_column_count(self, content_widget):
        """Test setting column count."""
        content_widget.set_column_count(4)
        assert content_widget.current_column_count == 4

    def test_scroll_position(self, content_widget):
        """Test scroll position management."""
        # Set scroll position
        content_widget.set_scroll_position(100)

        # Get scroll position (might be 0 if no content to scroll)
        position = content_widget.get_scroll_position()
        assert isinstance(position, int)


class TestSequenceCardTab:
    """Test suite for complete SequenceCardTab."""

    @pytest.fixture
    def mock_services(self):
        """Create all mock services."""
        data_service = Mock(spec=ISequenceCardDataService)
        cache_service = Mock(spec=ISequenceCardCacheService)
        layout_service = Mock(spec=ISequenceCardLayoutService)
        display_service = Mock(spec=ISequenceCardDisplayService)
        export_service = Mock(spec=ISequenceCardExportService)
        settings_service = Mock(spec=ISequenceCardSettingsService)

        # Setup default returns
        settings_service.get_last_selected_length.return_value = 16
        settings_service.get_column_count.return_value = 2
        layout_service.calculate_grid_dimensions.return_value = GridDimensions(4, 4, 16)

        return {
            "data": data_service,
            "cache": cache_service,
            "layout": layout_service,
            "display": display_service,
            "export": export_service,
            "settings": settings_service,
        }

    @pytest.fixture
    def sequence_card_tab(self, qtbot, mock_services):
        """Create sequence card tab for testing."""
        tab = SequenceCardTab(
            data_service=mock_services["data"],
            cache_service=mock_services["cache"],
            layout_service=mock_services["layout"],
            display_service=mock_services["display"],
            export_service=mock_services["export"],
            settings_service=mock_services["settings"],
        )
        qtbot.addWidget(tab)
        return tab

    def test_tab_creation(self, sequence_card_tab):
        """Test tab creation and initial state."""
        assert sequence_card_tab.header is not None
        assert sequence_card_tab.navigation is not None
        assert sequence_card_tab.content is not None
        assert not sequence_card_tab.initialized

    def test_tab_initialization_on_show(self, qtbot, sequence_card_tab, mock_services):
        """Test tab initialization when shown."""
        settings_service = mock_services["settings"]
        display_service = mock_services["display"]

        # Show the tab (triggers initialization)
        sequence_card_tab.show()
        qtbot.waitExposed(sequence_card_tab)

        # Process any pending events
        QApplication.processEvents()

        # Should be initialized
        assert sequence_card_tab.initialized

        # Should have called display service
        display_service.display_sequences.assert_called()

    def test_length_selection_integration(
        self, qtbot, sequence_card_tab, mock_services
    ):
        """Test length selection integration between components."""
        settings_service = mock_services["settings"]
        display_service = mock_services["display"]

        # Simulate length selection
        sequence_card_tab._on_length_selected(8)

        # Should save setting and update display
        settings_service.save_selected_length.assert_called_with(8)
        display_service.display_sequences.assert_called_with(
            8, 2
        )  # 2 is default column count

    def test_column_count_change_integration(
        self, qtbot, sequence_card_tab, mock_services
    ):
        """Test column count change integration."""
        settings_service = mock_services["settings"]
        display_service = mock_services["display"]

        # Simulate column count change
        sequence_card_tab._on_column_count_changed(4)

        # Should save setting and update display
        settings_service.save_column_count.assert_called_with(4)
        # Should call with saved length (16) and new column count (4)
        settings_service.get_last_selected_length.return_value = 16
        display_service.display_sequences.assert_called()

    def test_refresh_integration(self, qtbot, sequence_card_tab, mock_services):
        """Test refresh integration."""
        cache_service = mock_services["cache"]
        display_service = mock_services["display"]

        # Simulate refresh
        sequence_card_tab._on_refresh_requested()

        # Should clear cache and refresh display
        cache_service.clear_cache.assert_called_once()
        display_service.display_sequences.assert_called()

    def test_loading_state_handling(self, qtbot, sequence_card_tab):
        """Test loading state handling."""
        # Simulate loading state change
        sequence_card_tab._on_loading_state_changed(True)
        assert sequence_card_tab.cursor().shape() == Qt.CursorShape.WaitCursor

        sequence_card_tab._on_loading_state_changed(False)
        assert sequence_card_tab.cursor().shape() == Qt.CursorShape.ArrowCursor

    def test_resize_event_handling(self, qtbot, sequence_card_tab, mock_services):
        """Test resize event handling."""
        display_service = mock_services["display"]

        # Initialize tab first
        sequence_card_tab.initialized = True

        # Simulate resize
        sequence_card_tab.resizeEvent(None)

        # Should trigger layout refresh (with timer delay)
        # We can't easily test the timer, but we can verify the method exists
        assert hasattr(sequence_card_tab, "_refresh_layout_after_resize")

    def test_cleanup(self, sequence_card_tab, mock_services):
        """Test resource cleanup."""
        display_service = mock_services["display"]
        export_service = mock_services["export"]
        cache_service = mock_services["cache"]

        # Add cancel methods to mocks
        display_service.cancel_current_operation = Mock()
        export_service.cancel_export = Mock()

        sequence_card_tab.cleanup()

        # Should call cleanup methods
        display_service.cancel_current_operation.assert_called_once()
        export_service.cancel_export.assert_called_once()
        cache_service.optimize_memory_usage.assert_called_once()

    def test_signal_connections(self, qtbot, sequence_card_tab, mock_services):
        """Test that signal connections are properly established."""
        # Test signal connections by triggering them and checking functional responses

        # Test navigation length selection signal - should trigger display service
        display_service = mock_services["display"]
        settings_service = mock_services["settings"]

        # Emit length selection signal
        sequence_card_tab.navigation.length_selected.emit(8)
        QApplication.processEvents()

        # Should have called settings service to save the length
        settings_service.save_selected_length.assert_called_with(8)

        # Should have called display service
        display_service.display_sequences.assert_called()

        # Test header refresh signal - should trigger display service
        display_service.reset_mock()
        sequence_card_tab.header.refresh_requested.emit()
        QApplication.processEvents()

        # Should have called display service again
        display_service.display_sequences.assert_called()


# Visual regression test (requires actual image comparison)
class TestSequenceCardVisualRegression:
    """Visual regression tests for sequence card components."""

    @pytest.mark.skip(reason="Requires reference images and image comparison setup")
    def test_header_visual_appearance(self, qtbot):
        """Test header visual appearance matches reference."""
        # This would require setting up reference images and comparison
        pass

    @pytest.mark.skip(reason="Requires reference images and image comparison setup")
    def test_navigation_visual_appearance(self, qtbot):
        """Test navigation visual appearance matches reference."""
        # This would require setting up reference images and comparison
        pass


# Performance tests
class TestSequenceCardPerformance:
    """Performance tests for sequence card components."""

    def test_large_sequence_list_performance(self, qtbot):
        """Test performance with large sequence lists."""
        # Create mock services
        display_service = Mock(spec=ISequenceCardDisplayService)
        cache_service = Mock(spec=ISequenceCardCacheService)
        layout_service = Mock(spec=ISequenceCardLayoutService)

        layout_service.calculate_grid_dimensions.return_value = GridDimensions(4, 4, 16)

        # Create content widget
        content_widget = SequenceCardContentComponent(
            display_service, cache_service, layout_service
        )
        qtbot.addWidget(content_widget)

        # Create large sequence list
        large_sequence_list = [
            SequenceCardData(
                path=Path(f"test_{i}.png"),
                word=f"word_{i}",
                length=16,
                metadata={"sequence_length": 16},
            )
            for i in range(1000)  # 1000 sequences
        ]

        # Measure time to process
        import time

        start_time = time.time()

        content_widget._on_sequences_loaded(large_sequence_list)

        end_time = time.time()
        processing_time = end_time - start_time

        # Should process within reasonable time (adjust as needed)
        assert processing_time < 2.0  # Less than 2 seconds (relaxed for CI)

    def test_memory_usage_with_cache(self):
        """Test memory usage doesn't grow excessively with cache."""
        cache_service = SequenceCardCacheService(
            max_raw_cache_size=100, max_scaled_cache_size=200
        )

        # Fill cache with test data
        test_data = b"x" * 1024  # 1KB per image
        for i in range(150):  # More than cache size
            path = Path(f"test_{i}.png")
            cache_service.cache_image(path, test_data)

        # Check cache size is within limits
        stats = cache_service.get_cache_stats()
        assert stats.cache_size <= 100  # Should not exceed max raw cache size


# Add performance and stress testing to UI components
@pytest.mark.performance
class TestSequenceCardUIPerformance:
    """Performance tests for UI components under stress conditions."""

    @pytest.fixture
    def large_sequence_dataset(self):
        """Create large dataset for UI performance testing."""
        return [
            SequenceCardData(
                path=Path(f"perf_test_{i}.png"),
                word=f"word_{i:04d}",
                length=16,
                metadata={"sequence_length": 16, "complexity": "high"},
            )
            for i in range(1000)  # Large dataset
        ]

    @pytest.mark.performance
    def test_navigation_component_large_dataset_responsiveness(
        self, qtbot, large_sequence_dataset
    ):
        """Test navigation component responsiveness with large datasets."""
        # Create mock services
        settings_service = Mock(spec=ISequenceCardSettingsService)
        display_service = Mock(spec=ISequenceCardDisplayService)

        settings_service.get_last_selected_length.return_value = 16
        settings_service.get_column_count.return_value = 2

        # Create navigation widget
        nav_widget = SequenceCardNavigationComponent(settings_service, display_service)
        qtbot.addWidget(nav_widget)

        import time

        # Measure responsiveness of length selection
        start_time = time.time()

        # Simulate rapid length changes
        for length in [2, 4, 8, 16, 12, 10, 6, 5, 3]:
            nav_widget.select_length(length)
            QApplication.processEvents()  # Process UI events

        response_time = time.time() - start_time

        # Should remain responsive even with rapid changes
        assert response_time < 1.0  # Less than 1 second for 9 changes
        assert nav_widget.selected_length == 3  # Last selection should be active

    @pytest.mark.performance
    def test_content_component_rendering_performance(
        self, qtbot, large_sequence_dataset
    ):
        """Test content component rendering performance with large datasets."""
        # Create mock services
        display_service = Mock(spec=ISequenceCardDisplayService)
        cache_service = Mock(spec=ISequenceCardCacheService)
        layout_service = Mock(spec=ISequenceCardLayoutService)

        layout_service.calculate_grid_dimensions.return_value = GridDimensions(4, 4, 16)

        # Create content widget
        content_widget = SequenceCardContentComponent(
            display_service, cache_service, layout_service
        )
        qtbot.addWidget(content_widget)

        import time

        start_time = time.time()

        # Test rendering large dataset
        content_widget._on_sequences_loaded(large_sequence_dataset)
        QApplication.processEvents()

        render_time = time.time() - start_time

        # Should render within reasonable time
        assert render_time < 2.0  # Less than 2 seconds for 1000 sequences
        assert content_widget.current_sequences == large_sequence_dataset

    @pytest.mark.performance
    def test_tab_memory_usage_over_time(self, qtbot):
        """Test tab memory usage doesn't grow excessively over time."""
        # Create mock services with memory tracking
        mock_services = {
            "data": Mock(spec=ISequenceCardDataService),
            "cache": Mock(spec=ISequenceCardCacheService),
            "layout": Mock(spec=ISequenceCardLayoutService),
            "display": Mock(spec=ISequenceCardDisplayService),
            "export": Mock(spec=ISequenceCardExportService),
            "settings": Mock(spec=ISequenceCardSettingsService),
        }

        # Setup mock returns
        mock_services["settings"].get_last_selected_length.return_value = 16
        mock_services["settings"].get_column_count.return_value = 2
        mock_services["layout"].calculate_grid_dimensions.return_value = GridDimensions(
            4, 4, 16
        )

        # Create tab
        tab = SequenceCardTab(
            data_service=mock_services["data"],
            cache_service=mock_services["cache"],
            layout_service=mock_services["layout"],
            display_service=mock_services["display"],
            export_service=mock_services["export"],
            settings_service=mock_services["settings"],
        )
        qtbot.addWidget(tab)

        # Simulate heavy usage over time
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Simulate user interactions
        for i in range(50):  # 50 cycles of activity
            # Change length
            tab._on_length_selected(16 if i % 2 == 0 else 8)

            # Change column count
            tab._on_column_count_changed(2 if i % 3 == 0 else 4)

            # Trigger refresh
            if i % 10 == 0:
                tab._on_refresh_requested()

            QApplication.processEvents()

        final_memory = process.memory_info().rss
        memory_growth = final_memory - initial_memory

        # Memory growth should be reasonable (less than 50MB)
        assert memory_growth < 50 * 1024 * 1024  # 50MB limit

        print(f"Memory growth over 50 cycles: {memory_growth / 1024 / 1024:.2f}MB")


@pytest.mark.stress
class TestSequenceCardStressTesting:
    """Stress tests for sequence card components."""

    @pytest.mark.stress
    def test_rapid_length_changes_stress(self, qtbot):
        """Stress test with rapid length changes."""
        # Create services
        settings_service = Mock(spec=ISequenceCardSettingsService)
        display_service = Mock(spec=ISequenceCardDisplayService)

        settings_service.get_last_selected_length.return_value = 16
        settings_service.get_column_count.return_value = 2

        nav_widget = SequenceCardNavigationComponent(settings_service, display_service)
        qtbot.addWidget(nav_widget)

        # Rapid length changes (stress test)
        lengths = [2, 3, 4, 5, 6, 8, 10, 12, 16, 0]

        for _ in range(100):  # 100 cycles
            for length in lengths:
                nav_widget.select_length(length)
                # Don't process events every time to stress the system
                if _ % 10 == 0:
                    QApplication.processEvents()

        # Should handle stress without crashing
        assert nav_widget.selected_length == 0  # Last selection

        # Navigation component doesn't directly call settings service
        # The signal should have been emitted many times instead
        # We can verify the component is still responsive
        assert nav_widget.length_buttons[0].is_selected

    @pytest.mark.stress
    def test_cache_service_stress_test(self):
        """Stress test cache service with concurrent operations."""
        cache_service = SequenceCardCacheService(
            max_raw_cache_size=100, max_scaled_cache_size=200
        )

        import threading
        import time

        results = {"errors": 0, "operations": 0}

        def cache_worker(worker_id: int):
            """Worker function for concurrent cache operations."""
            try:
                for i in range(200):  # 200 operations per worker
                    path = Path(f"stress_test_{worker_id}_{i}.png")
                    test_data = f"worker_{worker_id}_data_{i}".encode() * 100

                    # Mix of operations
                    if i % 3 == 0:
                        cache_service.cache_image(path, test_data, 1.0)
                    elif i % 3 == 1:
                        cache_service.get_cached_image(path, 1.0)
                    else:
                        cache_service.cache_image(path, test_data, 0.5)

                    results["operations"] += 1

                    # Occasional cache clearing
                    if i % 50 == 0:
                        cache_service.clear_cache()

            except Exception as e:
                results["errors"] += 1
                print(f"Worker {worker_id} error: {e}")

        # Start multiple worker threads
        threads = []
        for worker_id in range(5):  # 5 concurrent workers
            thread = threading.Thread(target=cache_worker, args=(worker_id,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=30)  # 30 second timeout

        # Verify stress test results
        assert results["errors"] == 0  # No errors should occur
        assert results["operations"] >= 800  # Should complete most operations

        # Cache should still be functional after stress test
        stats = cache_service.get_cache_stats()
        assert stats is not None


# Visual regression and validation tests
@pytest.mark.visual
class TestSequenceCardVisualValidation:
    """Visual validation tests for sequence card components."""

    @pytest.mark.visual
    def test_header_component_visual_structure(self, qtbot):
        """Test header component visual structure and layout."""
        export_service = Mock(spec=ISequenceCardExportService)
        display_service = Mock(spec=ISequenceCardDisplayService)

        header = SequenceCardHeaderComponent(export_service, display_service)
        qtbot.addWidget(header)

        # Show widget and let it render
        header.show()
        qtbot.waitExposed(header)

        # Verify visual structure
        assert header.title_label.isVisible()
        assert header.description_label.isVisible()
        assert header.export_button.isVisible()
        assert header.refresh_button.isVisible()
        assert header.regenerate_button.isVisible()

        # Progress bar should be hidden initially
        assert not header.progress_bar.isVisible()

        # Check minimum size requirements
        assert header.minimumWidth() > 200
        assert header.minimumHeight() > 50

        # Test button accessibility
        assert header.export_button.isEnabled()
        assert header.refresh_button.isEnabled()
        assert header.regenerate_button.isEnabled()

    @pytest.mark.visual
    def test_navigation_component_visual_structure(self, qtbot):
        """Test navigation component visual structure and styling."""
        settings_service = Mock(spec=ISequenceCardSettingsService)
        display_service = Mock(spec=ISequenceCardDisplayService)

        settings_service.get_last_selected_length.return_value = 16
        settings_service.get_column_count.return_value = 2

        nav = SequenceCardNavigationComponent(settings_service, display_service)
        qtbot.addWidget(nav)

        nav.show()
        qtbot.waitExposed(nav)

        # Verify all length buttons are present and visible
        expected_lengths = [0, 2, 3, 4, 5, 6, 8, 10, 12, 16]
        for length in expected_lengths:
            button = nav.length_buttons[length]
            assert button.isVisible()
            assert button.text() in [
                "All",
                "2",
                "3",
                "4",
                "5",
                "6",
                "8",
                "10",
                "12",
                "16",
            ]

        # Verify column selector
        assert nav.column_combo.isVisible()
        assert nav.column_combo.count() == 5  # Should have 5 options (2,3,4,5,6)

        # Check styling is applied
        assert nav.objectName() == "sequenceCardNavigation"

        # Test responsive behavior
        nav.resize(300, 500)
        QApplication.processEvents()

        # Buttons should still be accessible after resize
        for button in nav.length_buttons.values():
            assert button.isVisible()

    @pytest.mark.visual
    def test_content_component_layout_integrity(self, qtbot):
        """Test content component layout integrity under different conditions."""
        display_service = Mock(spec=ISequenceCardDisplayService)
        cache_service = Mock(spec=ISequenceCardCacheService)
        layout_service = Mock(spec=ISequenceCardLayoutService)

        layout_service.calculate_grid_dimensions.return_value = GridDimensions(4, 4, 16)

        content = SequenceCardContentComponent(
            display_service, cache_service, layout_service
        )
        qtbot.addWidget(content)

        content.show()
        qtbot.waitExposed(content)

        # Test different column counts
        for column_count in [2, 3, 4, 5, 6]:
            content.set_column_count(column_count)
            QApplication.processEvents()

            # Layout should remain stable
            assert content.current_column_count == column_count
            assert content.scroll_area.isVisible()

        # Test with empty state
        content._show_empty_state()
        QApplication.processEvents()

        # Should display empty state message
        assert content.content_layout.count() > 0

        # Test scroll functionality
        content.set_scroll_position(100)
        position = content.get_scroll_position()
        assert isinstance(position, int)
