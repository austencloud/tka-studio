"""
Learn UI Service Implementation

Provides UI state management, responsive sizing calculations,
and styling support for the learn tab components.
"""

import logging

from desktop.modern.core.interfaces.learn_services import ILearnUIService

logger = logging.getLogger(__name__)


class LearnUIService(ILearnUIService):
    """
    Production implementation of learn tab UI state management.

    Provides responsive sizing calculations and UI state management
    following the patterns established in the browse tab.
    """

    def __init__(self):
        """Initialize learn UI service."""
        logger.info("Learn UI service initialized")

    def get_font_sizes(self, widget_width: int, widget_height: int) -> dict[str, int]:
        """
        Calculate responsive font sizes based on widget dimensions.

        Args:
            widget_width: Current widget width
            widget_height: Current widget height

        Returns:
            Dictionary mapping font type to size
        """
        try:
            # Base calculations on widget width following legacy patterns
            base_size = max(widget_width, 800)  # Minimum base size

            font_sizes = {
                # Title and header fonts
                "title": max(base_size // 50, 16),  # Main title
                "subtitle": max(base_size // 65, 14),  # Subtitles
                "header": max(base_size // 60, 14),  # Section headers
                # Content fonts
                "button": max(base_size // 80, 12),  # Button text
                "description": max(base_size // 140, 10),  # Description text
                "question_prompt": max(base_size // 65, 14),  # Question prompts
                "progress": max(base_size // 90, 11),  # Progress text
                # Interactive elements
                "lesson_button": max(base_size // 80, 12),  # Lesson buttons
                "answer_button": max(base_size // 85, 11),  # Answer buttons
                "control_button": max(base_size // 80, 12),  # Control buttons
                # Mode toggle elements
                "mode_label": max(base_size // 85, 11),  # Mode labels
                "mode_description": max(base_size // 120, 9),  # Mode descriptions
                # Timer and results
                "timer": max(base_size // 70, 14),  # Timer display
                "results_title": max(base_size // 45, 18),  # Results title
                "results_stat": max(base_size // 75, 13),  # Results statistics
            }

            return font_sizes

        except Exception as e:
            logger.error(f"Failed to calculate font sizes: {e}")
            return self._get_default_font_sizes()

    def get_component_sizes(
        self, widget_width: int, widget_height: int
    ) -> dict[str, tuple[int, int]]:
        """
        Calculate responsive component sizes based on widget dimensions.

        Args:
            widget_width: Current widget width
            widget_height: Current widget height

        Returns:
            Dictionary mapping component type to (width, height) tuple
        """
        try:
            component_sizes = {
                # Button sizes
                "lesson_button": (widget_width // 4, widget_height // 10),
                "answer_button": (widget_width // 5, widget_height // 12),
                "go_back_button": (widget_width // 10, widget_height // 20),
                "control_button": (widget_width // 8, widget_height // 15),
                # Question display
                "question_display": (widget_width // 2, widget_height // 3),
                "pictograph_view": (
                    widget_height // 4 if widget_height > 600 else widget_height // 5,
                    widget_height // 4 if widget_height > 600 else widget_height // 5,
                ),
                # Progress elements
                "progress_bar": (widget_width // 3, widget_height // 25),
                "timer_display": (widget_width // 4, widget_height // 20),
                # Mode toggle
                "mode_toggle": (widget_width // 2, widget_height // 15),
                # Results display
                "results_panel": (widget_width // 2, widget_height // 2),
                "results_stat": (widget_width // 4, widget_height // 25),
            }

            # Ensure minimum sizes
            for component, (width, height) in component_sizes.items():
                component_sizes[component] = (max(width, 100), max(height, 30))

            return component_sizes

        except Exception as e:
            logger.error(f"Failed to calculate component sizes: {e}")
            return self._get_default_component_sizes()

    def get_layout_spacing(
        self, widget_width: int, widget_height: int
    ) -> dict[str, int]:
        """
        Calculate responsive layout spacing based on widget dimensions.

        Args:
            widget_width: Current widget width
            widget_height: Current widget height

        Returns:
            Dictionary mapping spacing type to pixel value
        """
        try:
            # Calculate spacing based on widget size
            base_spacing = max(widget_width // 100, 5)

            spacing = {
                # Layout spacing
                "main_layout": base_spacing * 2,
                "component": base_spacing,
                "section": base_spacing * 3,
                # Button spacing
                "button_grid": max(widget_width // 80, 10),
                "answer_options": max(widget_width // 60, 15),
                # Content spacing
                "content_margin": base_spacing * 4,
                "text_spacing": base_spacing,
                # Specific areas
                "lesson_selector": base_spacing * 2,
                "question_area": base_spacing * 3,
                "progress_area": base_spacing,
            }

            return spacing

        except Exception as e:
            logger.error(f"Failed to calculate layout spacing: {e}")
            return self._get_default_spacing()

    def get_color_scheme(self, background_type: str = "default") -> dict[str, str]:
        """
        Get color scheme for learn tab components.

        Args:
            background_type: Type of background being used

        Returns:
            Dictionary mapping color roles to color values
        """
        try:
            # Base color scheme
            colors = {
                # Text colors
                "text_primary": "white",
                "text_secondary": "rgba(255, 255, 255, 0.8)",
                "text_muted": "rgba(255, 255, 255, 0.6)",
                # Button colors
                "button_background": "rgba(255, 255, 255, 0.2)",
                "button_border": "rgba(255, 255, 255, 0.3)",
                "button_hover": "rgba(255, 255, 255, 0.3)",
                "button_pressed": "rgba(255, 255, 255, 0.4)",
                # Feedback colors
                "correct_answer": "green",
                "incorrect_answer": "red",
                "neutral": "rgba(255, 255, 255, 0.5)",
                # Progress colors
                "progress_fill": "rgba(0, 255, 0, 0.7)",
                "progress_background": "rgba(255, 255, 255, 0.2)",
                # Panel colors
                "panel_background": "rgba(255, 255, 255, 0.1)",
                "panel_border": "rgba(255, 255, 255, 0.2)",
            }

            # Adjust for different background types
            if background_type in ["Rainbow", "AuroraBorealis", "Aurora"]:
                colors["text_primary"] = "black"
                colors["text_secondary"] = "rgba(0, 0, 0, 0.8)"
                colors["text_muted"] = "rgba(0, 0, 0, 0.6)"

            return colors

        except Exception as e:
            logger.error(f"Failed to get color scheme: {e}")
            return self._get_default_colors()

    def calculate_responsive_dimensions(
        self, parent_width: int, parent_height: int, aspect_ratio: float = 1.0
    ) -> tuple[int, int]:
        """
        Calculate responsive dimensions maintaining aspect ratio.

        Args:
            parent_width: Parent widget width
            parent_height: Parent widget height
            aspect_ratio: Desired aspect ratio (width/height)

        Returns:
            Tuple of (width, height) maintaining aspect ratio
        """
        try:
            # Calculate based on parent constraints
            max_width = int(parent_width * 0.8)
            max_height = int(parent_height * 0.8)

            # Calculate dimensions maintaining aspect ratio
            if max_width / aspect_ratio <= max_height:
                # Width is constraining
                width = max_width
                height = int(width / aspect_ratio)
            else:
                # Height is constraining
                height = max_height
                width = int(height * aspect_ratio)

            return (max(width, 100), max(height, 100))

        except Exception as e:
            logger.error(f"Failed to calculate responsive dimensions: {e}")
            return (200, 200)

    def _get_default_font_sizes(self) -> dict[str, int]:
        """Get default font sizes as fallback."""
        return {
            "title": 20,
            "subtitle": 16,
            "header": 16,
            "button": 14,
            "description": 12,
            "question_prompt": 16,
            "progress": 13,
            "lesson_button": 14,
            "answer_button": 12,
            "control_button": 14,
            "mode_label": 12,
            "mode_description": 10,
            "timer": 16,
            "results_title": 22,
            "results_stat": 14,
        }

    def _get_default_component_sizes(self) -> dict[str, tuple[int, int]]:
        """Get default component sizes as fallback."""
        return {
            "lesson_button": (200, 60),
            "answer_button": (150, 50),
            "go_back_button": (100, 40),
            "control_button": (120, 45),
            "question_display": (300, 200),
            "pictograph_view": (150, 150),
            "progress_bar": (250, 25),
            "timer_display": (150, 40),
            "mode_toggle": (300, 50),
            "results_panel": (400, 300),
            "results_stat": (200, 30),
        }

    def _get_default_spacing(self) -> dict[str, int]:
        """Get default spacing as fallback."""
        return {
            "main_layout": 10,
            "component": 5,
            "section": 15,
            "button_grid": 12,
            "answer_options": 18,
            "content_margin": 20,
            "text_spacing": 5,
            "lesson_selector": 10,
            "question_area": 15,
            "progress_area": 5,
        }

    def _get_default_colors(self) -> dict[str, str]:
        """Get default colors as fallback."""
        return {
            "text_primary": "white",
            "text_secondary": "rgba(255, 255, 255, 0.8)",
            "text_muted": "rgba(255, 255, 255, 0.6)",
            "button_background": "rgba(255, 255, 255, 0.2)",
            "button_border": "rgba(255, 255, 255, 0.3)",
            "button_hover": "rgba(255, 255, 255, 0.3)",
            "button_pressed": "rgba(255, 255, 255, 0.4)",
            "correct_answer": "green",
            "incorrect_answer": "red",
            "neutral": "rgba(255, 255, 255, 0.5)",
            "progress_fill": "rgba(0, 255, 0, 0.7)",
            "progress_background": "rgba(255, 255, 255, 0.2)",
            "panel_background": "rgba(255, 255, 255, 0.1)",
            "panel_border": "rgba(255, 255, 255, 0.2)",
        }
