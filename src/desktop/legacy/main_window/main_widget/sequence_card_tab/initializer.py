from __future__ import annotations

# src/main_window/main_widget/sequence_card_tab/tab.py
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from utils.path_helpers import get_sequence_card_image_exporter_path

if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.sequence_card_tab import (
        SequenceCardTab,
    )

USE_PRINTABLE_LAYOUT = True


class SequenceCardInitializer:
    def __init__(self, parent: "SequenceCardTab"):
        self.parent = parent

    def initialize_content(self):
        self.parent.is_initializing = True

        try:
            images_path = get_sequence_card_image_exporter_path()
            images_exist = self.parent.resource_manager.has_sequence_images(images_path)

            if not images_exist:
                self.parent.header.description_label.setText(
                    "Generating sequence images..."
                )
                QApplication.processEvents()

                # Re-enable image generation to test the arrow fix
                print("DEBUG: Starting image generation with arrow fix...")
                if hasattr(self.parent.image_exporter, "export_all_images"):
                    self.parent.image_exporter.export_all_images()

            self._apply_saved_settings()

        except Exception as e:
            self.parent.header.description_label.setText(f"Error: {str(e)}")
        finally:
            self.parent.setCursor(Qt.CursorShape.ArrowCursor)
            self.parent.is_initializing = False

    def _apply_saved_settings(self):
        settings = self.parent.settings_manager_obj

        if USE_PRINTABLE_LAYOUT and hasattr(self.parent, "printable_displayer"):
            self.parent.printable_displayer.columns_per_row = (
                settings.saved_column_count
            )

            if hasattr(self.parent.nav_sidebar, "column_dropdown"):
                index = self.parent.nav_sidebar.column_dropdown.findText(
                    str(settings.saved_column_count)
                )
                if index >= 0:
                    self.parent.nav_sidebar.column_dropdown.setCurrentIndex(index)
                    QApplication.processEvents()

        self.parent.nav_sidebar.selected_length = settings.saved_length
        self.parent.currently_displayed_length = settings.saved_length

        if hasattr(self.parent.nav_sidebar, "update_selection_styles"):
            self.parent.nav_sidebar.update_selection_styles()

        self.parent.header.description_label.setText("Loading saved sequence view...")
        QApplication.processEvents()

        if USE_PRINTABLE_LAYOUT and hasattr(self.parent, "printable_displayer"):
            QApplication.processEvents()
            self.parent.printable_displayer.display_sequences(settings.saved_length)
            self.parent._sync_pages_from_displayer()
