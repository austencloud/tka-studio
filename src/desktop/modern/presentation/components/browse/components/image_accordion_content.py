"""
Image-based Accordion Content Component

Displays filter options with images (for start positions and difficulty levels).
"""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal

# Additional imports for SVG rendering
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.domain.models.browse_models import FilterType
from desktop.modern.presentation.styles.mixins import StyleMixin


try:
    from desktop.modern.application.services.assets.image_asset_utils import (
        get_image_path,
    )
except ImportError:
    # Fallback if import fails
    def get_image_path(filename: str) -> str:
        return f"images/{filename}"


from .category_button import CategoryButton


class ImageAccordionContent(QFrame, StyleMixin):
    """Image-based accordion content for start positions and difficulty."""

    filter_selected = pyqtSignal(FilterType, object)

    def __init__(
        self,
        filter_type: FilterType,
        options: list[str],
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.filter_type = filter_type
        self.options = options
        self.buttons = {}  # {value: button}
        self.images = {}  # {value: QLabel}
        self._content_height = 0
        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self) -> None:
        """Setup the image-based content layout."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 8, 16, 16)
        main_layout.setSpacing(8)

        # Create horizontal layout for image-based options
        options_layout = QHBoxLayout()
        options_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        options_layout.setSpacing(20)  # Space between position columns

        # Create image-based options
        if self.filter_type.value == "starting_position":
            self._create_start_position_layout(options_layout)
        elif self.filter_type.value == "difficulty":
            self._create_difficulty_layout(options_layout)
        elif self.filter_type.value == "grid_mode":
            self._create_grid_mode_layout(options_layout)
        else:
            # Fallback to regular buttons
            self._create_regular_layout(options_layout)

        main_layout.addLayout(options_layout)

        # Calculate and store content height
        self._calculate_content_height()

    def _create_start_position_layout(self, layout: QHBoxLayout) -> None:
        """Create start position layout with large images and grid layout."""

        # Position descriptions from legacy
        POSITION_DESCRIPTIONS = {
            "Alpha": "Hands apart.",
            "Beta": "Hands together.",
            "Gamma": "Hands form a right angle.",
        }

        # Get image directory path
        image_dir = get_image_path("position_images")

        # Create grid layout for proper spacing and centering
        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.setHorizontalSpacing(20)  # Space between columns
        grid_layout.setVerticalSpacing(12)  # Space between rows

        col = 0
        for position in ["Alpha", "Beta", "Gamma"]:
            if position in self.options:
                # Position image (top row, dynamic size)
                image_label = QLabel()
                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Calculate image size as 1/2 of available width dynamically (much larger)
                available_width = self.width() if self.width() > 0 else 800
                image_size = max(
                    200, available_width // 2
                )  # At least 200px, or 1/2 width (much larger than before)
                image_label.setFixedSize(image_size, image_size)

                # Load image
                image_path = Path(image_dir) / f"{position.lower()}.png"
                if image_path.exists():
                    pixmap = QPixmap(str(image_path))
                    scaled_pixmap = pixmap.scaled(
                        image_size,
                        image_size,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    image_label.setPixmap(scaled_pixmap)

                    # Make image clickable
                    image_label.setCursor(Qt.CursorShape.PointingHandCursor)
                    image_label.mousePressEvent = (
                        lambda ev, p=position: self._handle_image_click(p, ev)
                    )
                else:
                    image_label.setText("No Image")
                    image_label.setStyleSheet(
                        "color: rgba(255, 255, 255, 0.5); border: 1px dashed rgba(255, 255, 255, 0.3);"
                    )

                self.images[position] = image_label
                grid_layout.addWidget(image_label, 0, col, Qt.AlignmentFlag.AlignCenter)

                # Position button (below image)
                button = CategoryButton(position)
                button.clicked.connect(lambda _, p=position: self._select_filter(p))
                self.buttons[position] = button
                grid_layout.addWidget(button, 1, col, Qt.AlignmentFlag.AlignCenter)

                # Description label (below button) - More horizontal space to prevent wrapping
                description = QLabel(POSITION_DESCRIPTIONS.get(position, ""))
                description.setAlignment(Qt.AlignmentFlag.AlignCenter)
                description.setStyleSheet(
                    "color: rgba(255, 255, 255, 0.8); font-size: 14px; font-weight: 500;"
                )
                description.setWordWrap(True)
                description.setMaximumWidth(
                    image_size + 80
                )  # Much more width to prevent wrapping
                description.setMinimumHeight(40)  # Ensure enough height
                grid_layout.addWidget(description, 2, col, Qt.AlignmentFlag.AlignCenter)

                col += 1

        # Add grid to main layout
        layout.addLayout(grid_layout)

    def _create_difficulty_layout(self, layout: QHBoxLayout) -> None:
        """Create difficulty layout with large level images like legacy version."""

        # Legacy difficulty level configuration (matching legacy system)
        DIFFICULTY_CONFIG = {
            "beginner": (1, "🟢 Level 1", "Base letters with no turns."),
            "intermediate": (
                2,
                "🟡 Level 2",
                "Turns added with only radial orientations.",
            ),
            "advanced": (3, "🔴 Level 3", "Non-radial orientations."),
        }

        # Image directory (using centralized path resolver)
        try:
            from desktop.modern.infrastructure.path_resolver import path_resolver

            image_dir = path_resolver.get_image_path("level_images")
        except Exception as e:
            print(f"Warning: Could not use centralized path resolver: {e}")
            # Fallback to manual discovery
            current_file = Path(__file__)
            desktop_root = current_file.parent.parent.parent.parent.parent.parent
            image_dir = desktop_root / "images" / "level_images"

        # Create grid layout for proper spacing and centering
        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.setHorizontalSpacing(
            30
        )  # More space between columns for larger images
        grid_layout.setVerticalSpacing(15)  # More space between rows

        col = 0
        for difficulty in ["beginner", "intermediate", "advanced"]:
            # Check if difficulty exists in options (handle tuple format from accordion config)
            difficulty_exists = False
            for option in self.options:
                if isinstance(option, tuple):
                    # Option is like ("🟢 Beginner", "beginner")
                    if option[1] == difficulty:
                        difficulty_exists = True
                        break
                elif option == difficulty:
                    difficulty_exists = True
                    break

            if difficulty_exists:
                level_num, label, description = DIFFICULTY_CONFIG.get(
                    difficulty, (1, difficulty.capitalize(), "")
                )

                # Level image (top row, large size like start position)
                image_label = QLabel()
                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Calculate image size as 1/2 of available width dynamically (same as start position)
                available_width = self.width() if self.width() > 0 else 800
                image_size = max(
                    200, available_width // 2
                )  # At least 200px, or 1/2 width (much larger than before)
                image_label.setFixedSize(image_size, image_size)

                # Load level image
                image_path = Path(image_dir) / f"level_{level_num}.png"
                if image_path.exists():
                    pixmap = QPixmap(str(image_path))
                    if not pixmap.isNull():
                        # Scale pixmap to fit the label while maintaining aspect ratio
                        scaled_pixmap = pixmap.scaled(
                            image_size,
                            image_size,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation,
                        )
                        image_label.setPixmap(scaled_pixmap)
                    else:
                        image_label.setText(f"Level {level_num}")
                        image_label.setStyleSheet(
                            "color: white; font-size: 16px; font-weight: bold;"
                        )
                else:
                    # Fallback if image doesn't exist
                    image_label.setText(f"Level {level_num}")
                    image_label.setStyleSheet(
                        "color: white; font-size: 16px; font-weight: bold;"
                    )

                # Make image clickable
                image_label.setCursor(Qt.CursorShape.PointingHandCursor)
                image_label.mousePressEvent = (
                    lambda ev, d=difficulty: self._handle_image_click(d, ev)
                )

                self.images[difficulty] = image_label
                grid_layout.addWidget(image_label, 0, col, Qt.AlignmentFlag.AlignCenter)

                # Difficulty button (below image)
                button = CategoryButton(label)
                button.clicked.connect(lambda _, d=difficulty: self._select_filter(d))
                self.buttons[difficulty] = button
                grid_layout.addWidget(button, 1, col, Qt.AlignmentFlag.AlignCenter)

                # Description label (below button) - More space allocated
                desc_label = QLabel(description)
                desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                desc_label.setStyleSheet(
                    "color: rgba(255, 255, 255, 0.8); font-size: 14px; font-weight: 500; padding: 5px;"
                )
                desc_label.setWordWrap(True)
                desc_label.setMaximumWidth(
                    image_size + 60
                )  # More width for text to prevent spillover
                desc_label.setMinimumHeight(50)  # Ensure enough height for text
                grid_layout.addWidget(desc_label, 2, col, Qt.AlignmentFlag.AlignCenter)

                col += 1

        # Add grid to main layout
        layout.addLayout(grid_layout)

    def _create_grid_mode_layout(self, layout: QHBoxLayout) -> None:
        """Create grid mode layout with large SVG pictographs like legacy version."""

        # Legacy grid mode configuration (matching legacy system)

        # Image directory (using centralized path resolver)
        try:
            from desktop.modern.infrastructure.path_resolver import path_resolver

            image_dir = path_resolver.get_image_path("grid")
        except Exception as e:
            print(f"Warning: Could not use centralized path resolver: {e}")
            # Fallback to manual discovery
            current_file = Path(__file__)
            desktop_root = current_file.parent.parent.parent.parent.parent.parent
            image_dir = desktop_root / "images" / "grid"

        # Create grid layout for proper spacing and centering
        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.setHorizontalSpacing(
            40
        )  # More space between columns for larger images
        grid_layout.setVerticalSpacing(15)  # Space between rows

        # Grid mode configuration (diamond first, then box)
        GRID_MODE_CONFIG = {
            "diamond": ("💎 Diamond Grid", "Cardinal points"),
            "box": ("📦 Box Grid", "Inter cardinal points"),
        }

        col = 0
        for grid_style in ["diamond", "box"]:  # Diamond on left, box on right
            # Check if grid style exists in options (handle tuple format from accordion config)
            grid_style_exists = False
            for option in self.options:
                if isinstance(option, tuple):
                    # Option is like ("📦 Box Grid", "box")
                    if option[1] == grid_style:
                        grid_style_exists = True
                        break
                elif option == grid_style or option.lower() == grid_style:
                    grid_style_exists = True
                    break

            if grid_style_exists:
                label, description = GRID_MODE_CONFIG.get(
                    grid_style, (grid_style.capitalize(), "")
                )

                # Grid SVG image (top row, large size like start position)
                image_label = QLabel()
                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Calculate image size as 1/2 of available width dynamically (same as start position)
                available_width = self.width() if self.width() > 0 else 800
                image_size = max(
                    200, available_width // 2
                )  # At least 200px, or 1/2 width (much larger than before)
                image_label.setFixedSize(image_size, image_size)

                # Load grid SVG image
                svg_path = Path(image_dir) / f"{grid_style}_grid.svg"
                if svg_path.exists():
                    # Import here to avoid IDE removing unused imports
                    from PyQt6.QtGui import QPainter
                    from PyQt6.QtSvg import QSvgRenderer

                    # Render SVG to pixmap
                    svg_renderer = QSvgRenderer(str(svg_path))
                    if svg_renderer.isValid():
                        pixmap = QPixmap(image_size, image_size)
                        pixmap.fill(
                            Qt.GlobalColor.white
                        )  # White background like legacy
                        painter = QPainter(pixmap)
                        svg_renderer.render(painter)
                        painter.end()

                        image_label.setPixmap(pixmap)
                    else:
                        image_label.setText(f"{grid_style.capitalize()} Grid")
                        image_label.setStyleSheet(
                            "color: white; font-size: 16px; font-weight: bold;"
                        )
                else:
                    # Fallback if SVG doesn't exist
                    image_label.setText(f"{grid_style.capitalize()} Grid")
                    image_label.setStyleSheet(
                        "color: white; font-size: 16px; font-weight: bold;"
                    )

                # Make image clickable
                image_label.setCursor(Qt.CursorShape.PointingHandCursor)
                image_label.mousePressEvent = (
                    lambda ev, g=grid_style: self._handle_image_click(g, ev)
                )

                self.images[grid_style] = image_label
                grid_layout.addWidget(image_label, 0, col, Qt.AlignmentFlag.AlignCenter)

                # Grid style button (below image) - Make wider to fit full text
                button = CategoryButton(label)
                button.clicked.connect(lambda _, g=grid_style: self._select_filter(g))
                button.setMinimumWidth(image_size + 40)  # Wider than image to fit text
                self.buttons[grid_style] = button
                grid_layout.addWidget(button, 1, col, Qt.AlignmentFlag.AlignCenter)

                # Description label (below button) - More space allocated
                desc_label = QLabel(description)
                desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                desc_label.setStyleSheet(
                    "color: rgba(255, 255, 255, 0.8); font-size: 14px; font-weight: 500; padding: 5px;"
                )
                desc_label.setWordWrap(True)
                desc_label.setMaximumWidth(
                    image_size + 60
                )  # More width for text to prevent spillover
                desc_label.setMinimumHeight(50)  # Ensure enough height for text
                grid_layout.addWidget(desc_label, 2, col, Qt.AlignmentFlag.AlignCenter)

                col += 1

        # Add grid to main layout
        layout.addLayout(grid_layout)

    def _create_regular_layout(self, layout: QHBoxLayout) -> None:
        """Fallback to regular button layout."""
        for option in self.options:
            button = CategoryButton(option)
            button.clicked.connect(lambda _, o=option: self._select_filter(o))
            self.buttons[option] = button
            layout.addWidget(button)

    def _handle_image_click(self, value: str, _event) -> None:
        """Handle clicks on images."""
        self._select_filter(value)

    def _select_filter(self, value) -> None:
        """Handle filter selection."""
        print(f"🎯 [IMAGE ACCORDION] {self.filter_type.value} = {value}")
        self.filter_selected.emit(self.filter_type, value)

    def _calculate_content_height(self) -> None:
        """Calculate the natural height of the content."""
        # Force layout calculation
        self.updateGeometry()
        self.adjustSize()

        # Get the minimum size hint and add extra space for large images
        size_hint = self.sizeHint()

        # Give much more space for image-based sections
        if self.filter_type.value in ["starting_position", "difficulty", "grid_mode"]:
            self._content_height = (
                size_hint.height() + 200
            )  # Large space for big images
        else:
            self._content_height = size_hint.height() + 40  # Standard extra space

    def _apply_styling(self) -> None:
        """Apply glassmorphism styling to the content using standard patterns."""
        self.setStyleSheet(
            """
            ImageAccordionContent {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                margin: 0px 4px 4px 4px;
                padding: 0px;
            }
        """
        )

    @property
    def content_height(self) -> int:
        """Get the natural content height for animations."""
        return self._content_height

    def get_buttons(self) -> dict:
        """Get all buttons for external access."""
        return self.buttons.copy()

    def clear_selection(self) -> None:
        """Clear any visual selection state from buttons."""
        # This can be implemented later if needed for visual feedback
        pass
