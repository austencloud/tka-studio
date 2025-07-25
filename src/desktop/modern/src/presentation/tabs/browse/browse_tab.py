"""
Modern Browse Tab - Layout Matching Legacy Structure

Rewritten to match the Legacy browse tab layout exactly:
- Horizontal layout with 2:1 ratio (left stack : sequence viewer)
- Left stack contains filter selection and sequence browser
- Navigation via QStackedWidget switching
"""

from pathlib import Path
from typing import Dict, List, Optional

from domain.models.sequence_data import SequenceData
from presentation.tabs.browse.components.filter_selection_panel import (
    FilterSelectionPanel,
)
from presentation.tabs.browse.components.modern_sequence_viewer_panel import (
    ModernSequenceViewerPanel,
)
from presentation.tabs.browse.components.sequence_browser_panel import (
    SequenceBrowserPanel,
)
from presentation.tabs.browse.models import FilterType
from presentation.tabs.browse.services.browse_service import BrowseService
from presentation.tabs.browse.services.browse_state_service import BrowseStateService
from presentation.tabs.browse.services.modern_dictionary_data_manager import (
    ModernDictionaryDataManager,
)
from presentation.tabs.browse.services.progressive_loading_service import (
    ProgressiveLoadingService,
)
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QStackedWidget, QWidget


class BrowseTab(QWidget):
    """
    Modern Browse Tab matching Legacy layout structure exactly.

    Layout:
    - Main horizontal layout (2:1 ratio)
    - Left: internal_left_stack (QStackedWidget)
      - Index 0: Filter selection panel
      - Index 1: Sequence browser panel
    - Right: Sequence viewer panel
    """

    # Signals for communication with main app
    sequence_selected = pyqtSignal(str)  # sequence_id
    open_in_construct = pyqtSignal(str)  # sequence_id

    def __init__(
        self, sequences_dir: Path, settings_file: Path, parent: Optional[QWidget] = None
    ):
        """Initialize the modern browse tab with Legacy-matching layout."""
        super().__init__(parent)

        # Initialize services
        # Find the TKA root directory and construct the data path
        tka_root = Path(__file__).resolve()
        while tka_root.parent != tka_root and tka_root.name != "TKA":
            tka_root = tka_root.parent
        data_dir = tka_root / "data"

        self.dictionary_manager = ModernDictionaryDataManager(data_dir)
        self.browse_service = BrowseService(sequences_dir)
        self.state_service = BrowseStateService(settings_file)
        self.progressive_loading_service = ProgressiveLoadingService(
            self.dictionary_manager
        )

        # Mapping from sequence UUID to word (for quick lookup)
        self.sequence_id_to_word: dict[str, str] = {}

        # Connect data manager signals
        self.dictionary_manager.data_loaded.connect(self._on_data_loaded)

        # Setup Legacy-matching layout
        self._setup_legacy_layout()
        self._connect_signals()

        # Load initial state
        QTimer.singleShot(100, self._load_initial_state)

    def _setup_legacy_layout(self) -> None:
        """Setup layout exactly matching Legacy structure."""
        # Main horizontal layout (2:1 ratio like Legacy)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left side - Internal stack for filter selection and sequence browsing
        self.internal_left_stack = QStackedWidget()

        # Create panels
        self.filter_selection_panel = FilterSelectionPanel(
            self.browse_service, self.dictionary_manager
        )
        self.sequence_browser_panel = SequenceBrowserPanel(
            self.browse_service, self.state_service, self.progressive_loading_service
        )

        # Add panels to stack (matching Legacy indexes)
        self.internal_left_stack.addWidget(
            self.filter_selection_panel
        )  # 0 - Filter selection
        self.internal_left_stack.addWidget(
            self.sequence_browser_panel
        )  # 1 - Sequence list

        # Start with filter selection visible (matching Legacy)
        self.internal_left_stack.setCurrentIndex(0)

        # Right side - Sequence viewer
        self.sequence_viewer_panel = ModernSequenceViewerPanel(self.state_service)

        # Add to main layout with 2:1 ratio (matching Legacy exactly)
        main_layout.addWidget(self.internal_left_stack, 2)  # 66.7% width
        main_layout.addWidget(self.sequence_viewer_panel, 1)  # 33.3% width

    def _connect_signals(self) -> None:
        """Connect component signals."""
        # Filter selection signals
        self.filter_selection_panel.filter_selected.connect(self._on_filter_selected)

        # Browser panel signals
        self.sequence_browser_panel.sequence_selected.connect(
            self._on_sequence_selected
        )
        self.sequence_browser_panel.open_in_construct.connect(
            self.open_in_construct.emit
        )
        self.sequence_browser_panel.back_to_filters.connect(self._show_filter_selection)

        # Sequence viewer panel signals
        self.sequence_viewer_panel.sequence_action.connect(self._on_sequence_action)
        self.sequence_viewer_panel.back_to_browser.connect(self._show_sequence_browser)

    def _load_initial_state(self) -> None:
        """Load initial data and restore state."""
        # Load sequences from dictionary
        self.dictionary_manager.load_all_sequences()

        # Always start with filter selection visible
        self._show_filter_selection()

    def _on_data_loaded(self, count: int) -> None:
        """Handle data loading completion."""
        print(f"📚 Loaded {count} sequences from dictionary")

        # Check for loading errors
        errors = self.dictionary_manager.get_loading_errors()
        if errors:
            pass  # Loading errors occurred

    def _on_filter_selected(self, filter_type: FilterType, filter_value) -> None:
        """Handle filter selection - switch to sequence browser with progressive loading."""
        # Save filter state
        self.state_service.set_filter(filter_type, filter_value)

        # IMMEDIATE NAVIGATION: Switch to sequence browser view first
        self._show_sequence_browser()

        # Start progressive loading - this will show incremental results
        self.sequence_browser_panel.show_sequences_progressive(
            filter_type, filter_value, chunk_size=8
        )

    def _apply_dictionary_filter(self, filter_type: FilterType, filter_value) -> List:
        """Apply filter using the dictionary data manager."""
        records = []

        if filter_type == FilterType.STARTING_LETTER:
            if isinstance(filter_value, str):
                # Handle letter ranges like "A-D"
                if "-" in filter_value and len(filter_value) == 3:
                    start_letter, end_letter = filter_value.split("-")
                    letters = [
                        chr(i) for i in range(ord(start_letter), ord(end_letter) + 1)
                    ]
                    records = self.dictionary_manager.get_records_by_starting_letters(
                        letters
                    )
                elif filter_value == "All Letters":
                    records = self.dictionary_manager.get_all_records()
                else:
                    # Single letter
                    records = self.dictionary_manager.get_records_by_starting_letter(
                        filter_value
                    )
            elif isinstance(filter_value, list):
                records = self.dictionary_manager.get_records_by_starting_letters(
                    filter_value
                )

        elif filter_type == FilterType.LENGTH:
            if isinstance(filter_value, int):
                records = self.dictionary_manager.get_records_by_length(filter_value)
            elif filter_value == "All":
                records = self.dictionary_manager.get_all_records()

        elif filter_type == FilterType.DIFFICULTY:
            if filter_value == "All":
                records = self.dictionary_manager.get_all_records()
            else:
                records = self.dictionary_manager.get_records_by_difficulty(
                    filter_value
                )

        elif filter_type == FilterType.AUTHOR:
            if filter_value == "All Authors":
                records = self.dictionary_manager.get_all_records()
            else:
                records = self.dictionary_manager.get_records_by_author(filter_value)

        elif filter_type == FilterType.GRID_MODE:
            if filter_value == "All":
                records = self.dictionary_manager.get_all_records()
            else:
                records = self.dictionary_manager.get_records_by_grid_mode(filter_value)

        elif filter_type == FilterType.FAVORITES:
            records = self.dictionary_manager.get_favorite_records()

        elif filter_type == FilterType.RECENT:
            records = self.dictionary_manager.get_recent_records()

        else:
            records = self.dictionary_manager.get_all_records()

        # Convert SequenceRecord to SequenceData format for compatibility
        return self._convert_records_to_sequence_data(records)

    def _convert_records_to_sequence_data(self, records) -> List:
        """Convert SequenceRecord objects to SequenceData format."""
        from domain.models.sequence_data import SequenceData

        sequence_data_list = []
        for record in records:
            # Create SequenceData object
            sequence_data = SequenceData(
                word=record.word,
                thumbnails=record.thumbnails,
                author=record.author,
                level=record.level,
                sequence_length=record.sequence_length,
                date_added=record.date_added,
                grid_mode=record.grid_mode,
                prop_type=record.prop_type,
                is_favorite=record.is_favorite,
                is_circular=record.is_circular,
                starting_position=record.starting_position,
                difficulty_level=record.difficulty_level,
                tags=record.tags,
            )

            # Store mapping from UUID to word for quick lookup
            self.sequence_id_to_word[sequence_data.id] = record.word

            sequence_data_list.append(sequence_data)

        return sequence_data_list

    def _on_sequence_selected(self, sequence_id: str) -> None:
        """Handle sequence selection from browser panel."""
        # Get sequence data
        sequence_data = self._get_sequence_data(sequence_id)
        if sequence_data:
            # Show sequence in viewer
            self.sequence_viewer_panel.show_sequence(sequence_data)
            print(f"🎭 Sequence selected: {sequence_data.word} ({sequence_id})")

        # Also emit the external signal
        self.sequence_selected.emit(sequence_id)

    def _on_sequence_action(self, action_type: str, sequence_id: str) -> None:
        """Handle sequence action from viewer panel - COMPLETE IMPLEMENTATION."""
        print(f"🎬 Sequence action: {action_type} on {sequence_id}")

        if action_type == "edit":
            self._handle_edit_sequence(sequence_id)
        elif action_type == "save":
            self._handle_save_image(sequence_id)
        elif action_type == "delete":
            self._handle_delete_variation(sequence_id)
        elif action_type == "fullscreen":
            self._handle_fullscreen_view(sequence_id)
        else:
            print(f"Unknown action type: {action_type}")

    def _handle_edit_sequence(self, sequence_id: str) -> None:
        """Handle edit sequence action."""
        print(f"✏️ Opening sequence {sequence_id} in construct tab")
        self.open_in_construct.emit(sequence_id)

    def _handle_save_image(self, sequence_id: str) -> None:
        """Handle save image action using basic file copy."""
        try:
            import shutil
            from pathlib import Path

            from PyQt6.QtWidgets import QFileDialog, QMessageBox

            print(f"💾 Saving image for sequence {sequence_id}")

            # Get sequence data
            sequence_data = self._get_sequence_data(sequence_id)
            if not sequence_data:
                QMessageBox.warning(
                    self, "No Sequence", "Please select a sequence first."
                )
                return

            # Get current variation index from the action panel
            current_variation = 0
            if hasattr(self.sequence_viewer_panel, "action_panel") and hasattr(
                self.sequence_viewer_panel.action_panel, "current_variation_index"
            ):
                current_variation = (
                    self.sequence_viewer_panel.action_panel.current_variation_index
                )

            # Get the thumbnail path for the current variation
            if (
                not sequence_data.thumbnails
                or current_variation < 0
                or current_variation >= len(sequence_data.thumbnails)
            ):
                QMessageBox.warning(
                    self, "No Image", "No image available for the selected variation."
                )
                return

            current_thumbnail_path = sequence_data.thumbnails[current_variation]

            # Use file dialog to get save location
            suggested_name = f"{sequence_data.word}_exported.png"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Sequence Image",
                suggested_name,
                "PNG Images (*.png);;All Files (*)",
            )

            if file_path:
                output_path = Path(file_path)
                source_path = Path(current_thumbnail_path)

                if source_path.exists():
                    shutil.copy2(source_path, output_path)
                    QMessageBox.information(
                        self,
                        "Export Successful",
                        f"Image saved successfully to:\n{output_path}",
                    )
                    print(f"✅ Successfully exported image to {output_path}")
                else:
                    QMessageBox.critical(
                        self, "Export Failed", f"Source image not found:\n{source_path}"
                    )
                    print(f"❌ Source image not found: {source_path}")

        except Exception as e:
            print(f"Error during image save: {e}")
            from PyQt6.QtWidgets import QMessageBox

            QMessageBox.critical(
                self,
                "Export Error",
                f"An error occurred while saving the image:\n{str(e)}",
            )

    def _handle_delete_variation(self, sequence_id: str) -> None:
        """Handle delete variation action with confirmation."""
        try:
            from pathlib import Path

            from PyQt6.QtWidgets import QMessageBox

            print(f"🗑️ Deleting variation for sequence {sequence_id}")

            # Get sequence data
            sequence_data = self._get_sequence_data(sequence_id)
            if not sequence_data:
                QMessageBox.warning(
                    self, "No Sequence", "Please select a sequence first."
                )
                return

            # Get current variation index
            current_variation = 0
            if hasattr(self.sequence_viewer_panel, "action_panel") and hasattr(
                self.sequence_viewer_panel.action_panel, "current_variation_index"
            ):
                current_variation = (
                    self.sequence_viewer_panel.action_panel.current_variation_index
                )

            if not sequence_data.thumbnails:
                QMessageBox.warning(
                    self, "No Variations", "No variations available to delete."
                )
                return

            # Show confirmation dialog
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete variation {current_variation + 1} of '{sequence_data.word}'?\n\nThis action cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Get the file path to delete
                if current_variation < len(sequence_data.thumbnails):
                    file_to_delete = Path(sequence_data.thumbnails[current_variation])

                    # Delete the file
                    if file_to_delete.exists():
                        file_to_delete.unlink()
                        print(f"✅ Successfully deleted {file_to_delete}")

                        QMessageBox.information(
                            self,
                            "Deletion Successful",
                            f"Variation {current_variation + 1} has been deleted.",
                        )

                        # Refresh to show changes
                        self.refresh_sequences()

                        # Update the viewer if there are remaining variations
                        updated_sequence_data = self._get_sequence_data(sequence_id)
                        if updated_sequence_data and updated_sequence_data.thumbnails:
                            self.sequence_viewer_panel.show_sequence(
                                updated_sequence_data
                            )
                        else:
                            # No variations left, clear viewer
                            self.sequence_viewer_panel.clear_sequence()
                            self._show_sequence_browser()
                    else:
                        QMessageBox.warning(
                            self,
                            "File Not Found",
                            f"The file to delete was not found:\n{file_to_delete}",
                        )
            else:
                print("Deletion cancelled by user")

        except Exception as e:
            print(f"Error during variation deletion: {e}")
            from PyQt6.QtWidgets import QMessageBox

            QMessageBox.critical(
                self,
                "Deletion Error",
                f"An error occurred while deleting the variation:\n{str(e)}",
            )

    def _handle_fullscreen_view(self, sequence_id: str) -> None:
        """Handle fullscreen view action using basic overlay."""
        try:
            from pathlib import Path

            from PyQt6.QtCore import Qt
            from PyQt6.QtGui import QPixmap
            from PyQt6.QtWidgets import QLabel, QMessageBox, QVBoxLayout, QWidget

            print(f"🔍 Opening fullscreen view for sequence {sequence_id}")

            # Get current image info from the viewer
            current_thumbnails = []
            current_index = 0

            if hasattr(self.sequence_viewer_panel, "image_viewer") and hasattr(
                self.sequence_viewer_panel.image_viewer, "current_thumbnails"
            ):
                current_thumbnails = (
                    self.sequence_viewer_panel.image_viewer.current_thumbnails
                )
                current_index = getattr(
                    self.sequence_viewer_panel.image_viewer, "current_index", 0
                )

            if (
                not current_thumbnails
                or current_index < 0
                or current_index >= len(current_thumbnails)
            ):
                QMessageBox.warning(
                    self, "No Image", "No image available for fullscreen view."
                )
                return

            current_thumbnail_path = Path(current_thumbnails[current_index])

            if not current_thumbnail_path.exists():
                QMessageBox.warning(
                    self,
                    "Image Not Found",
                    f"Image file not found:\n{current_thumbnail_path}",
                )
                return

            # Create and show basic fullscreen overlay
            overlay = QWidget(self)
            overlay.setWindowFlags(
                Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
            )
            overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.9);")
            overlay.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            overlay.setCursor(Qt.CursorShape.PointingHandCursor)

            # Setup image display
            layout = QVBoxLayout(overlay)
            layout.setContentsMargins(0, 0, 0, 0)

            image_label = QLabel()
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setCursor(Qt.CursorShape.PointingHandCursor)
            layout.addWidget(image_label)

            # Load and scale image
            pixmap = QPixmap(str(current_thumbnail_path))
            if not pixmap.isNull():
                # Scale to fit screen while maintaining aspect ratio
                screen_size = self.size()
                scaled_pixmap = pixmap.scaled(
                    screen_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                image_label.setPixmap(scaled_pixmap)

                # Make it cover the parent window
                overlay.setGeometry(self.geometry())

                # Click to close
                def close_overlay(event=None):
                    overlay.close()

                overlay.mousePressEvent = close_overlay
                image_label.mousePressEvent = close_overlay

                # Show overlay
                overlay.show()
                overlay.raise_()
                overlay.activateWindow()

                print(f"✅ Opened fullscreen view for {current_thumbnail_path}")
            else:
                QMessageBox.warning(
                    self,
                    "Invalid Image",
                    f"Could not load image:\n{current_thumbnail_path}",
                )

        except Exception as e:
            print(f"Error during fullscreen view: {e}")
            from PyQt6.QtWidgets import QMessageBox

            QMessageBox.critical(
                self,
                "Fullscreen Error",
                f"An error occurred while opening fullscreen view:\n{str(e)}",
            )

    def _get_sequence_data(self, sequence_id: str) -> Optional[SequenceData]:
        """Get sequence data by ID."""
        # First try to get the word from the progressive loading service mapping
        word = None
        if self.progressive_loading_service:
            mapping = self.progressive_loading_service.get_sequence_id_mapping()
            word = mapping.get(sequence_id)

        # Fallback to the old mapping if progressive loading didn't have it
        if not word:
            word = self.sequence_id_to_word.get(sequence_id)

        if not word:
            print(f"❌ No word mapping found for sequence_id: {sequence_id}")
            return None

        # Get all records from dictionary manager
        all_records = self.dictionary_manager.get_all_records()

        # Find the record by word
        target_record = None
        for record in all_records:
            if record.word == word:
                target_record = record
                break

        if not target_record:
            print(f"❌ No record found for word: {word}")
            return None

        # Convert SequenceRecord to SequenceData
        sequence_data = SequenceData(
            id=sequence_id,  # Use the original UUID
            word=target_record.word,
            thumbnails=target_record.thumbnails,
            author=target_record.author,
            level=target_record.level,
            sequence_length=target_record.sequence_length,
            date_added=target_record.date_added,
            grid_mode=target_record.grid_mode,
            prop_type=target_record.prop_type,
            is_favorite=target_record.is_favorite,
            is_circular=target_record.is_circular,
            starting_position=target_record.starting_position,
            difficulty_level=target_record.difficulty_level,
            tags=target_record.tags,
        )

        return sequence_data

    def _show_filter_selection(self) -> None:
        """Show filter selection panel (index 0)."""
        self.internal_left_stack.setCurrentIndex(0)

    def _show_sequence_browser(self) -> None:
        """Show sequence browser panel (index 1)."""
        self.internal_left_stack.setCurrentIndex(1)

    def refresh_sequences(self) -> None:
        """Refresh sequence data from disk."""
        # Clear and reload dictionary data
        self.dictionary_manager.refresh_data()

        # If we're currently showing filtered results, reapply the filter
        filter_type, filter_value = self.state_service.get_current_filter()
        if filter_type:
            print(
                f"♾️ Refreshing with progressive loading: {filter_type} = {filter_value}"
            )
            # Use progressive loading for refresh as well
            self.sequence_browser_panel.show_sequences_progressive(
                filter_type, filter_value, chunk_size=8
            )
