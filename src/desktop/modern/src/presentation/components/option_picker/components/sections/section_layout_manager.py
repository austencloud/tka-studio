"""
Section Layout Manager - Layout and Sizing Logic
Split from option_picker_section.py - contains layout calculations and resize handling
"""

from presentation.components.option_picker.types.letter_types import LetterType


class SectionLayoutManager:
    """Handles layout calculations and sizing for option picker sections."""

    def __init__(self, section_widget):
        self.section = section_widget
        self._last_width = None
        self._resize_in_progress = False
        self._debug_logged = False
        self._option_picker_width = 0

    def add_pictograph_from_pool(self, pictograph_frame):
        """Add pictograph with proper container sizing."""
        self._ensure_container_ready()
        self.section.section_pictograph_container.sync_width_with_section()
        self.section.section_pictograph_container.add_pictograph(pictograph_frame)
        self._update_size()

    def _get_global_pictograph_size(self) -> int:
        """Calculate consistent pictograph size using layout algorithm."""
        if self.section.mw_size_provider:
            main_window_width = self.section.mw_size_provider().width()
            frame_width = (
                self.section.section_pictograph_container.width()
                if self.section.section_pictograph_container.width() > 0
                else self.section.width()
            )

            if frame_width <= 0:
                frame_width = (
                    self.section.width()
                    if self.section.width() > 0
                    else main_window_width
                )

            size = max(main_window_width // 16, frame_width // 8)
            border_width = max(1, int(size * 0.015))
            spacing = self.section.section_pictograph_container.main_layout.spacing()
            final_size = size - (2 * border_width) - spacing
            final_size = max(60, min(final_size, 200))
            return final_size
        else:
            return 100

    def _update_size(self):
        """Update section size using layout calculation."""
        try:
            self.section.section_pictograph_container.sync_width_with_section()
            pictograph_size = self._get_global_pictograph_size()
            self.section.section_pictograph_container.resize_pictographs(
                pictograph_size
            )

            header_height = self.section.header.get_calculated_height()
            pictograph_height = (
                self.section.section_pictograph_container.calculate_required_height(
                    pictograph_size
                )
            )
            total_height = header_height + pictograph_height
            self.section.setMinimumHeight(total_height)

            if hasattr(self.section.header, "type_button"):
                self.section.header.type_button._resizing = True
                try:
                    calculated_height = self.section.header.get_calculated_height()
                    self.section.header.setFixedHeight(calculated_height)

                    if (
                        hasattr(self.section, "mw_size_provider")
                        and self.section.mw_size_provider
                    ):
                        parent_height = self.section.mw_size_provider().height()
                        font_size = max(parent_height // 70, 10)
                        label_height = max(int(font_size * 3), 20)
                        label_width = max(int(label_height * 6), 100)

                        from PyQt6.QtCore import QSize

                        self.section.header.type_button.setFixedSize(
                            QSize(label_width, label_height)
                        )
                finally:
                    self.section.header.type_button._resizing = False

            self.section.updateGeometry()

        except Exception as e:
            print(f"⚠️ [ERROR] Size update failed for {self.section.letter_type}: {e}")

    def handle_resize_event(self, event):
        """Handle resize events."""
        if self._resize_in_progress:
            return

        self._resize_in_progress = True
        try:
            if self.section.mw_size_provider:
                full_width = self.section.mw_size_provider().width()

                if self.section.letter_type in [
                    LetterType.TYPE4,
                    LetterType.TYPE5,
                    LetterType.TYPE6,
                ]:
                    section_width = full_width // 3
                else:
                    section_width = full_width

                if (
                    self._last_width is None
                    or abs(self._last_width - section_width) > 5
                ):
                    self._last_width = section_width
                    self.section.setFixedWidth(section_width)
                    self.section.section_pictograph_container.sync_width_with_section()

        except Exception as e:
            print(f"⚠️ [ERROR] Resize failed for {self.section.letter_type}: {e}")
        finally:
            self._resize_in_progress = False

    def register_for_sizing_updates(self):
        """Register this section to receive sizing updates."""
        widget = self.section.parent()
        while widget:
            if (
                hasattr(widget, "__class__")
                and "ModernOptionPickerWidget" in widget.__class__.__name__
            ):
                widget.add_sizing_callback(self._on_option_picker_resize)
                print(
                    f"🔗 Section {self.section.letter_type} registered for sizing updates"
                )
                break
            widget = widget.parent()

    def _on_option_picker_resize(self, option_picker_width: int):
        """Handle option picker width changes."""
        self._option_picker_width = option_picker_width
        if hasattr(self.section, "section_pictograph_container"):
            self.section.section_pictograph_container.update_sizing_reference(
                option_picker_width
            )

    def _ensure_container_ready(self):
        """Ensure the option picker container is properly sized."""
        if self.section.parent():
            widget = self.section.parent()
            while widget:
                if (
                    hasattr(widget, "__class__")
                    and "ModernOptionPickerWidget" in widget.__class__.__name__
                ):
                    widget.updateGeometry()
                    widget.update()
                    from PyQt6.QtWidgets import QApplication

                    QApplication.processEvents()
                    break
                elif (
                    hasattr(widget, "layout")
                    and widget.layout()
                    and widget.layout().__class__.__name__ == "QVBoxLayout"
                    and widget.width() > 500
                ):
                    widget.updateGeometry()
                    widget.update()
                    from PyQt6.QtWidgets import QApplication

                    QApplication.processEvents()
                    break
                widget = widget.parent()
