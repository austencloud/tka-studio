from typing import List
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from .section_button import OptionPickerSectionButton
from .letter_types import LetterType


class OptionPickerSection(QWidget):
    def __init__(self, letter_type: str, parent=None, mw_size_provider=None):
        super().__init__(parent)
        self.letter_type = letter_type
        self.pictographs: List = []
        self.mw_size_provider = mw_size_provider
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Create a transparent container for the header button to ensure proper centering
        header_container = QWidget()
        header_container.setStyleSheet("background: transparent; border: none;")
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.addStretch()

        self.header_button = OptionPickerSectionButton(self)
        self.header_button.clicked.connect(self._toggle_section)
        header_layout.addWidget(self.header_button)
        header_layout.addStretch()

        layout.addWidget(header_container)

        # Container with QGridLayout for pictographs
        from PyQt6.QtWidgets import QFrame

        self.pictograph_container = QFrame()
        self.pictograph_layout = QGridLayout(self.pictograph_container)

        # Layout settings
        self.pictograph_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pictograph_layout.setContentsMargins(0, 0, 0, 0)
        self.pictograph_layout.setSpacing(8)

        layout.addWidget(self.pictograph_container)

        # Transparent background, no borders
        self.pictograph_container.setStyleSheet(
            """
            QWidget {
                background-color: transparent;
                border: none;
            }
        """
        )

        # Initialize container visibility to match button state (expanded by default)
        self.pictograph_container.setVisible(self.header_button.is_expanded)

    def _toggle_section(self):
        self.header_button.toggle_expansion()
        self.pictograph_container.setVisible(self.header_button.is_expanded)

    def add_pictograph(self, pictograph_frame):
        """Add pictograph using direct layout positioning with lifecycle safety"""
        if not self._ensure_layout_validity():
            self._recreate_layout_objects()
            if not self._ensure_layout_validity():
                return

        self.pictographs.append(pictograph_frame)

        COLUMN_COUNT = 8
        count = len(self.pictographs)
        row, col = divmod(count - 1, COLUMN_COUNT)

        try:
            if not self._ensure_layout_validity():
                self.pictographs.remove(pictograph_frame)
                return

            self.pictograph_layout.addWidget(pictograph_frame, row, col)
            pictograph_frame.setVisible(True)
            self._update_container_size()

        except RuntimeError:
            if pictograph_frame in self.pictographs:
                self.pictographs.remove(pictograph_frame)

    def clear_pictographs(self):
        """Clear pictographs using proper Qt widget lifecycle management"""
        for pictograph in self.pictographs:
            if pictograph is not None:
                try:
                    if hasattr(pictograph, "cleanup"):
                        pictograph.cleanup()

                    if self._ensure_layout_validity():
                        self.pictograph_layout.removeWidget(pictograph)

                    pictograph.setParent(None)
                    pictograph.deleteLater()

                except RuntimeError:
                    pass

        self.pictographs.clear()

    def clear_pictographs_pool_style(self):
        """Clear pictographs using pool approach: hide and remove from layout, don't delete"""
        for pictograph in self.pictographs:
            if pictograph is not None:
                try:
                    if self._ensure_layout_validity():
                        self.pictograph_layout.removeWidget(pictograph)
                    pictograph.setVisible(False)
                except RuntimeError:
                    pass

        self.pictographs.clear()

    def add_pictograph_from_pool(self, pictograph_frame):
        """Add pictograph from pool (reuse existing objects)"""
        if not self._ensure_layout_validity():
            self._recreate_layout_objects()
            if not self._ensure_layout_validity():
                return

        self.pictographs.append(pictograph_frame)

        COLUMN_COUNT = 8
        count = len(self.pictographs)
        row, col = divmod(count - 1, COLUMN_COUNT)

        try:
            if not self._ensure_layout_validity():
                self.pictographs.remove(pictograph_frame)
                return

            self.pictograph_layout.addWidget(pictograph_frame, row, col)

            pictograph_frame.setVisible(True)
            pictograph_frame.show()

            if hasattr(pictograph_frame, "pictograph_component"):
                pictograph_frame.pictograph_component.setVisible(True)
                pictograph_frame.pictograph_component.show()

            self._force_layout_activation()
            self._update_container_size()

        except RuntimeError:
            if pictograph_frame in self.pictographs:
                self.pictographs.remove(pictograph_frame)

    def _ensure_layout_validity(self) -> bool:
        """Check if layout objects are still valid (not deleted)"""
        try:
            # Try to access layout properties to check if they're still valid
            if self.pictograph_container is None:
                return False
            if self.pictograph_layout is None:
                return False

            # Try to access a property to see if the C++ object is still alive
            _ = self.pictograph_layout.count()
            _ = self.pictograph_container.isVisible()
            return True
        except (RuntimeError, AttributeError):
            return False

    def _recreate_layout_objects(self):
        """Recreate layout objects if they've been deleted"""
        try:
            from PyQt6.QtWidgets import QFrame

            if (
                hasattr(self, "pictograph_container")
                and self.pictograph_container is not None
            ):
                try:
                    self.pictograph_container.setParent(None)
                except RuntimeError:
                    pass

            self.pictograph_container = QFrame()
            self.pictograph_layout = QGridLayout(self.pictograph_container)

            self.pictograph_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.pictograph_layout.setContentsMargins(0, 0, 0, 0)
            self.pictograph_layout.setSpacing(8)

            parent_layout = self.layout()
            if parent_layout:
                parent_layout.addWidget(self.pictograph_container)

            self.pictograph_container.setStyleSheet(
                """
                QWidget {
                    background-color: transparent;
                    border: none;
                }
            """
            )

            self.pictograph_container.setVisible(self.header_button.is_expanded)

        except Exception:
            pass

    def _get_global_pictograph_size(self) -> int:
        """
        Calculate consistent pictograph size based on main window width.
        All pictographs use the same size regardless of section.
        """
        if self.mw_size_provider:
            main_window_width = self.mw_size_provider().width()
            
            # Better size calculation: use width/12 instead of width/16 for larger icons
            # This gives better sizes for typical window widths (800px+ common)
            base_size = max(main_window_width // 12, 80)  # Minimum 80px (up from 60px)
            final_size = min(base_size, 140)  # Maximum 140px (down from 160px)
            
            # DEBUG: Print sizing calculations
            print(f"🔍 [DEBUG] Pictograph Sizing for {self.letter_type}:")
            print(f"   Main Window Width: {main_window_width}px")
            print(f"   Base Size (width/12): {main_window_width // 12}px")
            print(f"   After min(80): {base_size}px")
            print(f"   Final Size (max 140): {final_size}px")
            
            return final_size
        else:
            print(f"🔍 [DEBUG] Pictograph Sizing for {self.letter_type}: Using fallback (100px)")
            return 100  # Fallback size

    def _update_container_size(self):
        """Update container size using consistent pictograph sizing for all sections"""
        if len(self.pictographs) == 0:
            return

        if not self._ensure_layout_validity():
            self._recreate_layout_objects()
            if not self._ensure_layout_validity():
                return

        try:
            # Get consistent pictograph size for ALL sections
            pictograph_size = self._get_global_pictograph_size()
            
            print(f"🔍 [DEBUG] Container Update for {self.letter_type}:")
            print(f"   Number of pictographs: {len(self.pictographs)}")
            print(f"   Calculated pictograph size: {pictograph_size}px")
            
            # Resize all pictographs to the same size
            self._resize_pictograph_frames(pictograph_size)

            # Calculate container dimensions based on section layout
            if self.mw_size_provider:
                full_width = self.mw_size_provider().width()
                print(f"   Full window width: {full_width}px")

                if self.letter_type in [
                    LetterType.TYPE4,
                    LetterType.TYPE5,
                    LetterType.TYPE6,
                ]:
                    # Bottom row sections share width equally
                    section_width = (full_width - 20) // 3
                    available_width = section_width - 20
                    # Use fewer columns for bottom sections to fit the narrower width
                    COLUMN_COUNT = min(4, max(2, available_width // (pictograph_size + 8)))
                    print(f"   Bottom row section - Section width: {section_width}px")
                    print(f"   Available width: {available_width}px")
                    print(f"   Column count: {COLUMN_COUNT}")
                else:
                    # Top sections get full width
                    section_width = full_width
                    available_width = section_width - 40
                    COLUMN_COUNT = 8
                    print(f"   Top section - Section width: {section_width}px")
                    print(f"   Available width: {available_width}px")
                    print(f"   Column count: {COLUMN_COUNT}")
            else:
                available_width = self._get_available_scroll_width()
                COLUMN_COUNT = 8
                print(f"   Using fallback width: {available_width}px")

            container_margins = 10
            grid_spacing = 8

            # Calculate container dimensions
            actual_width = available_width
            max_row = (len(self.pictographs) - 1) // COLUMN_COUNT
            rows_needed = max_row + 1

            container_height = (
                (rows_needed * pictograph_size)
                + (grid_spacing * (rows_needed - 1))
                + (2 * container_margins)
            )
            
            # HEIGHT DEBUG: Add comprehensive height analysis
            header_height = self.header_button.height() if hasattr(self, 'header_button') else 0
            section_height = container_height + header_height + 10  # Reduced from 20 to 10 for tighter spacing
            
            print(f"📏 HEIGHT: {self.letter_type} - Container: {container_height}px, Header: {header_height}px, Total: {section_height}px")

            if not self._ensure_layout_validity():
                return

            # Set container size
            self.pictograph_container.setMinimumSize(actual_width, container_height)
            self.pictograph_container.setMaximumWidth(actual_width)
            
            print(f"   Set container size to: {actual_width} × {container_height}px")

            from PyQt6.QtWidgets import QSizePolicy

            self.pictograph_container.setSizePolicy(
                QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.Minimum,
            )

            # Set section height based on content
            self.setMinimumHeight(section_height)
            self.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Minimum,
            )
            
            print(f"   Set section minimum height to: {section_height}px")

            self._force_layout_activation()

            self.pictograph_container.setVisible(True)
            self.pictograph_container.show()
            self.setVisible(True)
            self.show()
            
            # POST-LAYOUT HEIGHT DEBUG
            actual_section_height = self.height()
            actual_container_height = self.pictograph_container.height()
            actual_header_height = self.header_button.height() if hasattr(self, 'header_button') else 0
            
            print(f"   --- POST-LAYOUT ACTUAL SIZES ---")
            print(f"   Actual section size: {self.width()} × {actual_section_height}px")
            print(f"   Actual container size: {self.pictograph_container.width()} × {actual_container_height}px")
            print(f"   Actual header size: {self.header_button.width()} × {actual_header_height}px")
            print(f"   Height difference: calculated={section_height}px vs actual={actual_section_height}px")
            if actual_section_height != section_height:
                print(f"   ⚠️  HEIGHT MISMATCH: {actual_section_height - section_height}px difference")
            print(f"   --- END HEIGHT ANALYSIS ---\n")

        except RuntimeError:
            pass

    def _get_available_scroll_width(self) -> int:
        """Get available width from parent scroll area, accounting for scroll bars"""
        # Default fallback width
        default_width = 600

        # Try to find the scroll area in parent hierarchy
        parent = self.parent()
        while parent:
            if hasattr(parent, "viewport") and hasattr(parent, "verticalScrollBar"):
                # Found scroll area
                viewport_width = parent.viewport().width()
                scrollbar_width = (
                    parent.verticalScrollBar().width()
                    if parent.verticalScrollBar().isVisible()
                    else 0
                )
                available_width = (
                    viewport_width - scrollbar_width - 20
                )  # Account for margins
                return max(400, available_width)  # Minimum reasonable width
            parent = parent.parent()

        return default_width

    def _resize_pictograph_frames(self, target_size: int) -> None:
        """Resize all pictograph frames to the target size"""
        print(f"🔍 [DEBUG] Resizing {len(self.pictographs)} pictograph frames to {target_size}px for {self.letter_type}")
        
        resized_count = 0
        for pictograph_frame in self.pictographs:
            if pictograph_frame and hasattr(pictograph_frame, "setFixedSize"):
                try:
                    # Get current size before resize
                    current_size = (pictograph_frame.width(), pictograph_frame.height())
                    pictograph_frame.setFixedSize(target_size, target_size)
                    resized_count += 1
                    
                    if resized_count <= 3:  # Only print first few to avoid spam
                        print(f"   Frame {resized_count}: {current_size} -> ({target_size}, {target_size})")
                except RuntimeError:
                    continue
        
        print(f"   Successfully resized {resized_count}/{len(self.pictographs)} frames")

    def _force_layout_activation(self) -> None:
        """Force the QGridLayout to activate and position widgets correctly"""
        try:
            self.pictograph_layout.activate()
            self.pictograph_layout.update()
            self.pictograph_container.updateGeometry()

            from PyQt6.QtWidgets import QApplication

            QApplication.processEvents()
        except RuntimeError:
            pass

    def update_layout(self):
        return

    def _calculate_optimal_columns(self) -> int:
        """Calculate optimal columns based on available width"""
        # Get available width from the option picker container
        available_width = 600  # Default fallback

        # Try to get actual available width from parent hierarchy
        parent = self.parent()
        while parent:
            if hasattr(parent, "sections_container"):
                available_width = (
                    parent.sections_container.width() - 40
                )  # Account for margins
                break
            parent = parent.parent()

        pictograph_width = 160 + 8  # Frame width + spacing

        # Calculate max columns that fit
        max_possible_columns = max(1, available_width // pictograph_width)

        # Apply limits based on letter type
        if self.letter_type == LetterType.TYPE1:
            max_columns = min(8, max_possible_columns)
        elif self.letter_type in [LetterType.TYPE4, LetterType.TYPE5, LetterType.TYPE6]:
            max_columns = min(6, max_possible_columns)
        else:
            max_columns = min(7, max_possible_columns)

        result = max(2, max_columns)
        return result

    def resizeEvent(self, event):
        """Resize event to set proper section width"""
        print(f"🔍 [DEBUG] ResizeEvent triggered for {self.letter_type}")
        
        if self.mw_size_provider:
            # Different width handling for bottom row vs vertical sections
            full_width = self.mw_size_provider().width()
            print(f"   Main window width: {full_width}px")

            # Check if this section is in the bottom row (sections 4, 5, 6)
            if self.letter_type in [
                LetterType.TYPE4,
                LetterType.TYPE5,
                LetterType.TYPE6,
            ]:
                # Bottom row sections share the width equally (1/3 each)
                section_width = (
                    full_width - 20
                ) // 3  # Account for spacing between sections
                print(f"   Bottom row section - calculated width: {section_width}px")
            else:
                # Vertical sections (1, 2, 3) get full width
                section_width = full_width
                print(f"   Top section - using full width: {section_width}px")

            # Get current size before setting
            current_size = (self.width(), self.height())
            print(f"   Current section size: {current_size}")
            
            # Set the calculated width
            self.setFixedWidth(section_width)
            print(f"   Set section width to: {section_width}px")

            # Also ensure pictograph container uses available width
            if hasattr(self, "pictograph_container") and self.pictograph_container:
                container_width = section_width - 20  # Account for margins
                self.pictograph_container.setMinimumWidth(container_width)
                self.pictograph_container.setMaximumWidth(container_width)
                print(f"   Set container width to: {container_width}px")

        super().resizeEvent(event)
