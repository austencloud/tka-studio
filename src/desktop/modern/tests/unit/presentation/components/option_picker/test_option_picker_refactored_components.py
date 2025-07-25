"""
Tests for OptionPickerScroll refactored components.

Tests all the new focused components to ensure they work correctly.
"""

from unittest.mock import MagicMock, Mock, patch

import pytest
from domain.models.beat_data import BeatData
from domain.models.sequence_data import SequenceData
from presentation.components.option_picker.components.option_picker_animator import (
    OptionPickerAnimator,
)
from presentation.components.option_picker.components.option_picker_layout_orchestrator import (
    OptionPickerLayoutOrchestrator,
)
from presentation.components.option_picker.components.option_picker_section_manager import (
    OptionPickerSectionManager,
)
from presentation.components.option_picker.components.option_picker_size_manager import (
    OptionPickerSizeManager,
)
from presentation.components.option_picker.components.option_picker_widget_pool_manager import (
    OptionPickerWidgetPoolManager,
)
from presentation.components.option_picker.types.letter_types import LetterType
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget


class TestOptionPickerAnimator:
    """Test the OptionPickerAnimator component."""

    def test_animator_initialization(self, qtbot):
        """Test animator initializes correctly."""
        parent = QWidget()
        qtbot.addWidget(parent)

        animator = OptionPickerAnimator(parent)

        assert animator._parent == parent
        assert not animator.is_animating()
        assert animator._pending_fade_callback is None

    def test_animator_skip_animation(self, qtbot):
        """Test skipping animation calls update directly."""
        parent = QWidget()
        qtbot.addWidget(parent)

        animator = OptionPickerAnimator(parent)
        callback_called = False

        def test_callback():
            nonlocal callback_called
            callback_called = True

        animator.skip_animation_and_update(test_callback)

        assert callback_called
        assert not animator.is_animating()

    def test_animator_with_no_frames(self, qtbot):
        """Test animator with no frames calls update directly."""
        parent = QWidget()
        qtbot.addWidget(parent)

        animator = OptionPickerAnimator(parent)
        callback_called = False

        def test_callback():
            nonlocal callback_called
            callback_called = True

        animator.fade_out_and_update([], test_callback)

        assert callback_called
        assert not animator.is_animating()

    def test_animator_with_fade_in_callback(self, qtbot):
        """Test animator calls fade_in_callback when provided."""
        parent = QWidget()
        qtbot.addWidget(parent)

        animator = OptionPickerAnimator(parent)
        update_called = False
        fade_in_called = False

        def update_callback():
            nonlocal update_called
            update_called = True

        def fade_in_callback():
            nonlocal fade_in_called
            fade_in_called = True

        # Test with no frames - should call update directly and skip fade_in_callback
        animator.fade_out_and_update([], update_callback, fade_in_callback)

        assert update_called
        assert not fade_in_called  # Should not be called when no frames to animate
        assert not animator.is_animating()


class TestOptionPickerSizeManager:
    """Test the OptionPickerSizeManager component."""

    def test_size_manager_initialization(self, qtbot):
        """Test size manager initializes correctly."""
        widget = QWidget()
        qtbot.addWidget(widget)

        size_provider = Mock(return_value=QSize(1200, 800))
        size_manager = OptionPickerSizeManager(widget, size_provider)

        assert size_manager._widget == widget
        assert size_manager._mw_size_provider == size_provider
        assert size_manager._last_calculated_width == 0

    def test_calculate_optimal_width_with_parent(self, qtbot):
        """Test width calculation with valid parent."""
        parent = QWidget()
        widget = QWidget(parent)
        qtbot.addWidget(parent)

        # Set parent to reasonable size
        parent.resize(1000, 600)

        size_provider = Mock(return_value=QSize(1200, 800))
        size_manager = OptionPickerSizeManager(widget, size_provider)

        width = size_manager.calculate_optimal_width()

        assert width == 1000  # Should use parent width
        assert size_manager._last_calculated_width == 1000

    def test_calculate_optimal_width_fallback(self, qtbot):
        """Test width calculation with fallback to main window."""
        widget = QWidget()
        qtbot.addWidget(widget)

        size_provider = Mock(return_value=QSize(1200, 800))
        size_manager = OptionPickerSizeManager(widget, size_provider)

        width = size_manager.calculate_optimal_width()

        assert width == 600  # Should use main window width // 2
        assert size_manager._last_calculated_width == 600

    def test_width_accuracy_validation(self, qtbot):
        """Test width accuracy validation."""
        widget = QWidget()
        qtbot.addWidget(widget)

        size_provider = Mock(return_value=QSize(1200, 800))
        size_manager = OptionPickerSizeManager(widget, size_provider)

        # Valid width
        assert size_manager.is_width_accurate(400)  # 33% of main window

        # Invalid widths
        assert not size_manager.is_width_accurate(0)  # Zero
        assert not size_manager.is_width_accurate(100)  # Too small (< 20%)
        assert not size_manager.is_width_accurate(1000)  # Too large (> 80%)
        assert not size_manager.is_width_accurate(622)  # Problematic width

    def test_ui_readiness_check(self, qtbot):
        """Test UI readiness checking."""
        widget = QWidget()
        qtbot.addWidget(widget)

        size_provider = Mock(return_value=QSize(1200, 800))
        size_manager = OptionPickerSizeManager(widget, size_provider)

        # Widget not visible initially
        assert not size_manager.is_ui_ready_for_sizing()

        # Make widget visible and sized
        widget.show()
        widget.resize(400, 300)

        # Should be ready now
        assert size_manager.is_ui_ready_for_sizing()


class TestOptionPickerSectionManager:
    """Test the OptionPickerSectionManager component."""

    def test_section_manager_initialization(self):
        """Test section manager initializes correctly."""
        sections = {
            LetterType.TYPE1: Mock(),
            LetterType.TYPE2: Mock(),
        }

        section_manager = OptionPickerSectionManager(sections)

        assert section_manager._sections == sections
        assert not section_manager.is_update_in_progress()

    def test_update_all_sections_directly(self):
        """Test updating all sections directly."""
        # Create mock sections
        section1 = Mock()
        section2 = Mock()
        sections = {
            LetterType.TYPE1: section1,
            LetterType.TYPE2: section2,
        }

        section_manager = OptionPickerSectionManager(sections)

        # Create test data
        sequence_data = SequenceData(beats=[])
        options_by_type = {
            LetterType.TYPE1: [Mock()],
            LetterType.TYPE2: [Mock()],
        }

        # Update sections
        section_manager.update_all_sections_directly(sequence_data, options_by_type)

        # Verify sections were updated
        section1.load_options_from_sequence.assert_called_once()
        section2.load_options_from_sequence.assert_called_once()

    def test_clear_all_sections(self):
        """Test clearing all sections."""
        section1 = Mock()
        section2 = Mock()
        sections = {
            LetterType.TYPE1: section1,
            LetterType.TYPE2: section2,
        }

        section_manager = OptionPickerSectionManager(sections)
        section_manager.clear_all_sections()

        section1.clear_pictographs.assert_called_once()
        section2.clear_pictographs.assert_called_once()


class TestOptionPickerLayoutOrchestrator:
    """Test the OptionPickerLayoutOrchestrator component."""

    def test_layout_orchestrator_initialization(self, qtbot):
        """Test layout orchestrator initializes correctly."""
        container = QWidget()
        qtbot.addWidget(container)

        layout = QVBoxLayout(container)
        option_config_service = Mock()

        orchestrator = OptionPickerLayoutOrchestrator(
            layout, container, option_config_service
        )

        assert orchestrator._layout == layout
        assert orchestrator._container == container
        assert orchestrator._option_config_service == option_config_service
        assert orchestrator._header_widget is None

    def test_add_header_widget(self, qtbot):
        """Test adding header widget."""
        container = QWidget()
        qtbot.addWidget(container)

        layout = QVBoxLayout(container)
        option_config_service = Mock()

        orchestrator = OptionPickerLayoutOrchestrator(
            layout, container, option_config_service
        )

        header_widget = QWidget()
        orchestrator.add_header_widget(header_widget)

        assert orchestrator._header_widget == header_widget
        assert layout.count() > 0

    def test_add_section_widget(self, qtbot):
        """Test adding section widget."""
        container = QWidget()
        qtbot.addWidget(container)

        layout = QVBoxLayout(container)
        option_config_service = Mock()

        orchestrator = OptionPickerLayoutOrchestrator(
            layout, container, option_config_service
        )

        section_widget = QWidget()
        orchestrator.add_section_widget(section_widget)

        assert len(orchestrator._section_widgets) == 1
        assert orchestrator._section_widgets[0] == section_widget

    def test_clear_layout(self, qtbot):
        """Test clearing the layout."""
        container = QWidget()
        qtbot.addWidget(container)

        layout = QVBoxLayout(container)
        option_config_service = Mock()

        orchestrator = OptionPickerLayoutOrchestrator(
            layout, container, option_config_service
        )

        # Add some widgets
        header_widget = QWidget()
        section_widget = QWidget()

        orchestrator.add_header_widget(header_widget)
        orchestrator.add_section_widget(section_widget)

        # Clear layout
        orchestrator.clear_layout()

        assert orchestrator._header_widget is None
        assert len(orchestrator._section_widgets) == 0
        assert len(orchestrator._group_widgets) == 0

    def test_get_layout_info(self, qtbot):
        """Test getting layout information."""
        container = QWidget()
        qtbot.addWidget(container)

        layout = QVBoxLayout(container)
        option_config_service = Mock()

        orchestrator = OptionPickerLayoutOrchestrator(
            layout, container, option_config_service
        )

        # Add some widgets
        header_widget = QWidget()
        section_widget = QWidget()

        orchestrator.add_header_widget(header_widget)
        orchestrator.add_section_widget(section_widget)

        info = orchestrator.get_layout_info()

        assert info["header_widget"] is True
        assert info["section_count"] == 1
        assert info["group_count"] == 0


# Integration test
class TestOptionPickerComponentsIntegration:
    """Test integration between components."""

    def test_components_work_together(self, qtbot):
        """Test that components can work together."""
        # Create main widget
        parent = QWidget()
        qtbot.addWidget(parent)

        # Create layout
        layout = QVBoxLayout(parent)

        # Create mocks
        option_config_service = Mock()
        option_pool_service = Mock()
        pictograph_pool_manager = Mock()
        size_calculator = Mock()

        # Mock returns
        option_config_service.get_total_max_pictographs.return_value = 3
        pictograph_pool_manager.checkout_pictograph.return_value = Mock()

        # Create components
        size_provider = Mock(return_value=QSize(1200, 800))
        size_manager = OptionPickerSizeManager(parent, size_provider)

        orchestrator = OptionPickerLayoutOrchestrator(
            layout, parent, option_config_service
        )

        animator = OptionPickerAnimator(parent)

        # Test they can be used together
        width = size_manager.calculate_optimal_width()
        assert width > 0

        header_widget = QWidget()
        orchestrator.add_header_widget(header_widget)

        assert not animator.is_animating()

        # Test cleanup
        orchestrator.clear_layout()
        animator.cleanup()


if __name__ == "__main__":
    pytest.main([__file__])
