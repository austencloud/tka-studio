"""
Context-Aware Scaling Service for Modern Pictographs.

This service replicates context-specific scaling logic to ensure Modern pictographs
achieve the same visual prominence as proven pictographs in different usage contexts.
"""

from typing import Optional, Tuple
from enum import Enum
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget


class ScalingContext(Enum):
    """Different contexts where pictographs are displayed, each with specific scaling needs."""

    OPTION_VIEW = "option_view"
    START_POS_PICKER = "start_pos_picker"
    ADVANCED_START_POS = "advanced_start_pos"
    CODEX_VIEW = "codex_view"
    BEAT_VIEW = "beat_view"
    GRAPH_EDITOR_VIEW = "graph_editor_view"
    DEFAULT = "default"


class RenderingContext(Enum):
    """Different contexts where pictographs are rendered, affecting arrow behavior."""

    GRAPH_EDITOR = "graph_editor"
    BEAT_FRAME = "beat_frame"
    OPTION_PICKER = "option_picker"
    PREVIEW = "preview"
    SEQUENCE_VIEWER = "sequence_viewer"
    UNKNOWN = "unknown"


class PictographScaler:
    """
    Service that provides context-aware scaling calculations matching proven behavior.

    Uses different scaling formulas for different contexts:
    - OptionView: size = max(mw_width//16, option_picker.width//8)
    - StartPosPicker: size = size_provider.width//10
    - AdvancedStartPos: size = size_provider.width//12
    - CodexView: size = codex.main_widget.width//16
    - BeatView: view_scale = min(view_size/beat_scene_size)
    - GE_View: scale_factor = min(view_size/scene_size)
    """

    def __init__(self):
        self.border_width = 2  # Default border width used in calculations

    def calculate_scale(
        self,
        context: ScalingContext,
        container_size: QSize,
        scene_size: QSize,
        **context_params,
    ) -> Tuple[float, float]:
        """
        Calculate scale factors for a pictograph in a specific context.

        Args:
            context: The scaling context (enum)
            container_size: Size of the container widget
            scene_size: Size of the pictograph scene
            **context_params: Additional context-specific parameters

        Returns:
            Tuple of (scale_x, scale_y) factors
        """
        if context == ScalingContext.OPTION_VIEW:
            return self._calculate_option_view_scale(
                container_size, scene_size, **context_params
            )
        elif context == ScalingContext.START_POS_PICKER:
            return self._calculate_start_pos_picker_scale(
                container_size, scene_size, **context_params
            )
        elif context == ScalingContext.ADVANCED_START_POS:
            return self._calculate_advanced_start_pos_scale(
                container_size, scene_size, **context_params
            )
        elif context == ScalingContext.CODEX_VIEW:
            return self._calculate_codex_view_scale(
                container_size, scene_size, **context_params
            )
        elif context == ScalingContext.BEAT_VIEW:
            return self._calculate_beat_view_scale(
                container_size, scene_size, **context_params
            )
        elif context == ScalingContext.GRAPH_EDITOR_VIEW:
            return self._calculate_graph_editor_scale(
                container_size, scene_size, **context_params
            )
        else:
            return self._calculate_default_scale(container_size, scene_size)

    def _calculate_option_view_scale(
        self, container_size: QSize, scene_size: QSize, **context_params
    ) -> Tuple[float, float]:
        """Calculate scaling for option view context."""
        # Get required parameters
        main_window_width = context_params.get("main_window_width", 1200)
        option_picker_width = context_params.get("option_picker_width", 800)

        # Calculate target size using proven formula
        size_option_1 = main_window_width // 16
        size_option_2 = option_picker_width // 8
        target_size = max(size_option_1, size_option_2)

        # Apply responsive border width calculation
        border_width = max(1, int(target_size * 0.015))
        # Adjust for border and spacing
        spacing = context_params.get("spacing", 0)
        adjusted_size = target_size - (2 * border_width) - spacing
        adjusted_size = max(adjusted_size, 100)  # Minimum size

        # Calculate scale factors
        scale_x = adjusted_size / scene_size.width()
        scale_y = adjusted_size / scene_size.height()

        return (scale_x, scale_y)

    def _calculate_start_pos_picker_scale(
        self, container_size: QSize, scene_size: QSize, **context_params
    ) -> Tuple[float, float]:
        """Calculate scaling for start position picker context."""
        # Use container width divided by 10 (proven formula)
        target_size = container_size.width() // 10
        target_size = max(target_size, 80)  # Minimum size

        # Calculate scale factors
        scale_x = target_size / scene_size.width()
        scale_y = target_size / scene_size.height()

        return (scale_x, scale_y)

    def _calculate_advanced_start_pos_scale(
        self, container_size: QSize, scene_size: QSize, **context_params
    ) -> Tuple[float, float]:
        """Calculate scaling for advanced start position context."""
        # Use container width divided by 12 (proven formula)
        target_size = container_size.width() // 12
        target_size = max(target_size, 70)  # Minimum size

        # Calculate scale factors
        scale_x = target_size / scene_size.width()
        scale_y = target_size / scene_size.height()

        return (scale_x, scale_y)

    def _calculate_codex_view_scale(
        self, container_size: QSize, scene_size: QSize, **context_params
    ) -> Tuple[float, float]:
        """Calculate scaling for codex view context."""
        # Use container width divided by 16 (proven formula)
        target_size = container_size.width() // 16
        target_size = max(target_size, 60)  # Minimum size

        # Calculate scale factors
        scale_x = target_size / scene_size.width()
        scale_y = target_size / scene_size.height()

        return (scale_x, scale_y)

    def _calculate_beat_view_scale(
        self, container_size: QSize, scene_size: QSize, **context_params
    ) -> Tuple[float, float]:
        """Calculate scaling for beat view context."""
        # Calculate scale factor maintaining aspect ratio
        view_width = container_size.width()
        view_height = container_size.height()

        scale_x = view_width / scene_size.width()
        scale_y = view_height / scene_size.height()

        # Use minimum scale to maintain aspect ratio
        min_scale = min(scale_x, scale_y)

        # Apply beat view specific adjustments
        beat_enhancement = context_params.get("beat_enhancement_factor", 0.95)
        adjusted_scale = min_scale * beat_enhancement

        return (adjusted_scale, adjusted_scale)

    def _calculate_graph_editor_scale(
        self, container_size: QSize, scene_size: QSize, **context_params
    ) -> Tuple[float, float]:
        """Calculate scaling for graph editor view context."""
        # Calculate scale factor maintaining aspect ratio
        view_width = container_size.width()
        view_height = container_size.height()

        scale_x = view_width / scene_size.width()
        scale_y = view_height / scene_size.height()

        # Use minimum scale to maintain aspect ratio
        min_scale = min(scale_x, scale_y)

        # Apply graph editor specific enhancement
        ge_enhancement = context_params.get("ge_enhancement_factor", 1.05)
        enhanced_scale = min_scale * ge_enhancement

        return (enhanced_scale, enhanced_scale)

    def _calculate_default_scale(
        self, container_size: QSize, scene_size: QSize
    ) -> Tuple[float, float]:
        """Calculate default scaling when no specific context is provided."""
        # Enhanced default scaling for optimal visual presentation
        scale_x = container_size.width() / scene_size.width()
        scale_y = container_size.height() / scene_size.height()

        # Use minimum scale to maintain aspect ratio
        min_scale = min(scale_x, scale_y)

        # Apply conservative scaling factor
        conservative_scale = min_scale * 0.9

        return (conservative_scale, conservative_scale)

    def get_responsive_border_width(self, target_size: int) -> int:
        """Calculate responsive border width based on target size."""
        return max(1, int(target_size * 0.015))

    def validate_scaling_context(self, context: ScalingContext) -> bool:
        """Validate that the scaling context is supported."""
        return isinstance(context, ScalingContext)

    def get_minimum_size_for_context(self, context: ScalingContext) -> int:
        """Get the minimum size for a specific context."""
        minimums = {
            ScalingContext.OPTION_VIEW: 100,
            ScalingContext.START_POS_PICKER: 80,
            ScalingContext.ADVANCED_START_POS: 70,
            ScalingContext.CODEX_VIEW: 60,
            ScalingContext.BEAT_VIEW: 50,
            ScalingContext.GRAPH_EDITOR_VIEW: 100,
            ScalingContext.DEFAULT: 80,
        }
        return minimums.get(context, 80)
