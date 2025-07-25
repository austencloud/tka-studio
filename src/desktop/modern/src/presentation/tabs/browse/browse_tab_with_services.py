"""
Modern Browse Tab - Complete Implementation with Service Integration

Updated to include:
- DI container integration for service access
- Complete action handler implementations
- Full screen overlay functionality
- Image export capability
- Sequence deletion with confirmation
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

from core.dependency_injection.di_container import DIContainer
from core.interfaces.browse_services import ISequenceDeletionService
from core.interfaces.image_export_services import (
    ImageExportOptions,
    ISequenceImageExporter,
    ISequenceMetadataExtractor,
)
from domain.models.sequence_data import SequenceData
from presentation.components.ui.full_screen.full_screen_overlay import FullScreenOverlay
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
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QMessageBox, QStackedWidget, QWidget

logger = logging.getLogger(__name__)


class BrowseTab(QWidget):
    """
    Modern Browse Tab with complete service integration.

    Layout:
    - Main horizontal layout (2:1 ratio)
    - Left: internal_left_stack (QStackedWidget)
      - Index 0: Filter selection panel
      - Index 1: Sequence browser panel
    - Right: Sequence viewer panel

    Features:
    - Full image export functionality via DI services
    - Sequence deletion with confirmation dialogs
    - Full screen image viewing
    - Complete metadata extraction and handling
    """

    # Signals for communication with main app
    sequence_selected = pyqtSignal(str)  # sequence_id
    open_in_construct = pyqtSignal(str)  # sequence_id

    def __init__(
        self,
        sequences_dir: Path,
        settings_file: Path,
        container: DIContainer,
        parent: Optional[QWidget] = None,
    ):
        """
        Initialize the modern browse tab with complete service integration.

        Args:
            sequences_dir: Directory containing sequence files
            settings_file: Settings file path
            container: Dependency injection container with registered services
            parent: Parent widget
        """
        super().__init__(parent)

        # Store services and data
        self.sequences_dir = sequences_dir
        self.container = container

        # Initialize services from DI container
        try:
            self.image_export_service = container.get_service(ISequenceImageExporter)
            self.metadata_extractor = container.get_service(ISequenceMetadataExtractor)
            self.deletion_service = container.get_service(ISequenceDeletionService)
            logger.info("✅ All services initialized from DI container")
        except Exception as e:
            logger.error(f"❌ Failed to initialize services from DI container: {e}")
            # Create fallback services if needed
            self._initialize_fallback_services()

        # Initialize data managers and state
        # Find the TKA root directory and construct the data path
        tka_root = Path(__file__).resolve()
        while tka_root.parent != tka_root and tka_root.name != "TKA":
            tka_root = tka_root.parent
        data_dir = tka_root / "data"

        self.dictionary_manager = ModernDictionaryDataManager(data_dir)
        self.browse_service = BrowseService(sequences_dir)
        self.state_service = BrowseStateService(settings_file)

        # Mapping from sequence UUID to word (for quick lookup)
        self.sequence_id_to_word: dict[str, str] = {}

        # Connect data manager signals
        self.dictionary_manager.data_loaded.connect(self._on_data_loaded)
        self.dictionary_manager.loading_progress.connect(self._on_loading_progress)

        # Setup layout and UI
        self._setup_legacy_layout()
        self._connect_signals()

        # Load initial state
        QTimer.singleShot(100, self._load_initial_state)

    def _initialize_fallback_services(self):
        """Initialize fallback services if DI container services are not available."""
        logger.warning("Initializing fallback services")

        # Create basic fallback implementations
        from application.services.browse.sequence_deletion_service import (
            SequenceDeletionService,
        )
        from application.services.image_export.sequence_metadata_extractor import (
            SequenceMetadataExtractor,
        )

        self.metadata_extractor = SequenceMetadataExtractor()
        self.deletion_service = SequenceDeletionService(self.sequences_dir)
        self.image_export_service = None  # Will show error if used

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
            self.browse_service, self.state_service
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
        # Check for loading errors
        errors = self.dictionary_manager.get_loading_errors()
        if errors:
            logger.warning(f"⚠️  {len(errors)} loading errors occurred")
            for error in errors[:5]:  # Show first 5 errors
                logger.warning(f"   - {error}")

    def _on_loading_progress(self, message: str, current: int, total: int) -> None:
        """Handle loading progress updates."""
        if (
            current % 10 == 0 or current == total
        ):  # Update every 10th item or at completion
            logger.info(f"🔄 {message} ({current}/{total})")

    def _on_filter_selected(self, filter_type: FilterType, filter_value) -> None:
        """Handle filter selection - switch to sequence browser."""
        logger.info(f"🔍 Filter selected: {filter_type} = {filter_value}")

        # Save filter state
        self.state_service.set_filter(filter_type, filter_value)

        # Apply filter using dictionary manager
        filtered_sequences = self._apply_dictionary_filter(filter_type, filter_value)
        self.sequence_browser_panel.show_sequences(
            filtered_sequences, filter_type, filter_value
        )
        logger.info(f"📋 Filtered to {len(filtered_sequences)} sequences")

        # Switch to sequence browser view (matching Legacy navigation)
        self._show_sequence_browser()

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
            logger.info(f"🎭 Sequence selected: {sequence_data.word} ({sequence_id})")

        # Also emit the external signal
        self.sequence_selected.emit(sequence_id)

    def _on_sequence_action(self, action_type: str, sequence_id: str) -> None:
        """Handle sequence action from viewer panel - COMPLETE IMPLEMENTATION."""
        logger.info(f"🎬 Sequence action: {action_type} on {sequence_id}")

        if action_type == "edit":
            self._handle_edit_sequence(sequence_id)
        elif action_type == "save":
            self._handle_save_image(sequence_id)
        elif action_type == "delete":
            self._handle_delete_variation(sequence_id)
        elif action_type == "fullscreen":
            self._handle_fullscreen_view(sequence_id)
        else:
            logger.warning(f"Unknown action type: {action_type}")

    def _handle_edit_sequence(self, sequence_id: str) -> None:
        """Handle edit sequence action."""
        logger.info(f"✏️ Opening sequence {sequence_id} in construct tab")
        self.open_in_construct.emit(sequence_id)

    def _handle_save_image(self, sequence_id: str) -> None:
        """Handle save image action using the modern image export service."""
        try:
            logger.info(f"💾 Saving image for sequence {sequence_id}")

            if not self.image_export_service:
                QMessageBox.warning(
                    self,
                    "Service Unavailable",
                    "Image export service is not available.",
                )
                return

            # Get sequence data
            sequence_data = self._get_sequence_data(sequence_id)
            if not sequence_data:
                QMessageBox.warning(
                    self, "No Sequence", "Please select a sequence first."
                )
                return

            # Get current variation index
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

            current_thumbnail_path = Path(sequence_data.thumbnails[current_variation])

            # Extract sequence JSON from thumbnail metadata
            sequence_json_data = self.metadata_extractor.extract_metadata(
                current_thumbnail_path
            )
            if not sequence_json_data:
                QMessageBox.warning(
                    self,
                    "No Metadata",
                    "Could not extract sequence data from the selected image.",
                )
                return

            # Create export options (using default settings for now)
            export_options = ImageExportOptions(
                add_word=True,
                add_user_info=True,
                add_difficulty_level=True,
                include_start_position=True,
            )

            # Use file dialog to get save location
            from PyQt6.QtWidgets import QFileDialog

            suggested_name = f"{sequence_data.word}_exported.png"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Sequence Image",
                suggested_name,
                "PNG Images (*.png);;All Files (*)",
            )

            if file_path:
                output_path = Path(file_path)

                # Extract sequence beats from metadata
                sequence_beats = sequence_json_data.get("sequence", [])

                # Export the image
                result = self.image_export_service.export_sequence_image(
                    sequence_beats, sequence_data.word, output_path, export_options
                )

                if result.success:
                    QMessageBox.information(
                        self,
                        "Export Successful",
                        f"Image saved successfully to:\n{output_path}",
                    )
                    logger.info(f"✅ Successfully exported image to {output_path}")
                else:
                    QMessageBox.critical(
                        self,
                        "Export Failed",
                        f"Failed to export image:\n{result.error_message}",
                    )
                    logger.error(f"❌ Failed to export image: {result.error_message}")

        except Exception as e:
            logger.error(f"Error during image save: {e}", exc_info=True)
            QMessageBox.critical(
                self,
                "Export Error",
                f"An error occurred while saving the image:\n{str(e)}",
            )

    def _handle_delete_variation(self, sequence_id: str) -> None:
        """Handle delete variation action using the deletion service."""
        try:
            logger.info(f"🗑️ Deleting variation for sequence {sequence_id}")

            # Get sequence data
            sequence_data = self._get_sequence_data(sequence_id)
            if not sequence_data:
                QMessageBox.warning(
                    self, "No Sequence", "Please select a sequence first."
                )
                return

            # Get current variation index
            current_variation = (
                self.sequence_viewer_panel.action_panel.current_variation_index
            )

            if not sequence_data.thumbnails:
                QMessageBox.warning(
                    self, "No Variations", "No variations available to delete."
                )
                return

            # Perform deletion using the service
            success = self.deletion_service.delete_variation(
                sequence_data.word,
                sequence_data.thumbnails,
                current_variation,
                self,  # parent widget for dialogs
            )

            if success:
                logger.info(
                    f"✅ Successfully deleted variation {current_variation} of {sequence_data.word}"
                )

                # Refresh the data to reflect changes
                self.refresh_sequences()

                # Update the viewer
                updated_sequence_data = self._get_sequence_data(sequence_id)
                if updated_sequence_data and updated_sequence_data.thumbnails:
                    # Show updated sequence
                    self.sequence_viewer_panel.show_sequence(updated_sequence_data)
                else:
                    # No variations left, clear viewer
                    self.sequence_viewer_panel.clear_sequence()
                    self._show_sequence_browser()

        except Exception as e:
            logger.error(f"Error during variation deletion: {e}", exc_info=True)
            QMessageBox.critical(
                self,
                "Deletion Error",
                f"An error occurred while deleting the variation:\n{str(e)}",
            )

    def _handle_fullscreen_view(self, sequence_id: str) -> None:
        """Handle fullscreen view action using the full screen overlay."""
        try:
            logger.info(f"🔍 Opening fullscreen view for sequence {sequence_id}")

            # Get current image info
            current_thumbnails = (
                self.sequence_viewer_panel.image_viewer.current_thumbnails
            )
            current_index = self.sequence_viewer_panel.image_viewer.current_index

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

            # Create and show full screen overlay
            overlay = FullScreenOverlay(self)
            overlay.show_image(current_thumbnail_path)

            logger.info(f"✅ Opened fullscreen view for {current_thumbnail_path}")

        except Exception as e:
            logger.error(f"Error during fullscreen view: {e}", exc_info=True)
            QMessageBox.critical(
                self,
                "Fullscreen Error",
                f"An error occurred while opening fullscreen view:\n{str(e)}",
            )

    def _get_sequence_data(self, sequence_id: str) -> Optional[SequenceData]:
        """Get sequence data by ID."""
        # Get the word from the mapping
        word = self.sequence_id_to_word.get(sequence_id)
        if not word:
            logger.error(f"❌ No word mapping found for sequence_id: {sequence_id}")
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
            logger.error(f"❌ No record found for word: {word}")
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
        logger.info("🔄 Switched to filter selection view")

    def _show_sequence_browser(self) -> None:
        """Show sequence browser panel (index 1)."""
        self.internal_left_stack.setCurrentIndex(1)
        logger.info("🔄 Switched to sequence browser view")

    def refresh_sequences(self) -> None:
        """Refresh sequence data from disk."""
        # Clear and reload dictionary data
        self.dictionary_manager.refresh_data()

        # If we're currently showing filtered results, reapply the filter
        filter_type, filter_value = self.state_service.get_current_filter()
        if filter_type:
            filtered_sequences = self._apply_dictionary_filter(
                filter_type, filter_value
            )
            self.sequence_browser_panel.show_sequences(
                filtered_sequences, filter_type, filter_value
            )
