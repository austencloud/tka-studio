"""
Pictograph Context Detection Service.

Provides robust, explicit context detection for pictograph rendering components.
Replaces brittle string matching with explicit context declaration and service-based resolution.
"""

import logging
from typing import Any, Dict, Optional, Protocol, runtime_checkable

from application.services.pictograph.scaling_service import RenderingContext
from core.interfaces.core_services import IPictographContextDetector

logger = logging.getLogger(__name__)


@runtime_checkable
class IPictographContextProvider(Protocol):
    """Protocol for components that can provide their rendering context."""

    def get_rendering_context(self) -> RenderingContext:
        """Return the rendering context for this component."""


class PictographContextDetector(IPictographContextDetector):
    """
    Service for robust pictograph context detection.

    Uses explicit context declaration instead of brittle string matching.
    Integrates with TKA's dependency injection and service architecture.
    """

    def __init__(self):
        """Initialize the context service."""
        self._component_contexts: Dict[str, RenderingContext] = {}
        self._context_providers: Dict[str, IPictographContextProvider] = {}

    def register_context_provider(self, component_id: str, context: Any) -> None:
        """
        Register a component with its explicit context.

        Args:
            component_id: Unique identifier for the component
            context: The rendering context for this component (RenderingContext enum)
        """
        # Convert to RenderingContext if needed
        if isinstance(context, RenderingContext):
            rendering_context = context
        elif isinstance(context, str):
            # Try to convert string to enum
            try:
                rendering_context = RenderingContext(context)
            except ValueError as exc:
                raise ValueError(f"Invalid context string: {context}") from exc
        else:
            raise ValueError(
                f"Context must be a RenderingContext enum or string, got {type(context)}"
            )

        self._component_contexts[component_id] = rendering_context
        logger.debug(
            f"Registered context {rendering_context.value} for component {component_id}"
        )

    def get_context_for_component(self, component_id: str) -> Any:
        """
        Get the rendering context for a specific component.

        Args:
            component_id: Unique identifier for the component

        Returns:
            The rendering context for the component, or UNKNOWN if not registered
        """
        context = self._component_contexts.get(component_id, RenderingContext.UNKNOWN)

        if context == RenderingContext.UNKNOWN:
            logger.warning(f"No context registered for component {component_id}")

        return context

    def determine_context_from_provider(self, provider: Any) -> Any:
        """
        Determine context from a context provider component.

        Args:
            provider: Component that implements IPictographContextProvider

        Returns:
            The rendering context from the provider
        """
        try:
            if hasattr(provider, "get_rendering_context"):
                context = provider.get_rendering_context()
                logger.debug(
                    f"Context provider returned: {context.value if hasattr(context, 'value') else context}"
                )
                return context
            else:
                logger.warning(
                    "Provider does not implement get_rendering_context method"
                )
                return RenderingContext.UNKNOWN
        except Exception as e:
            logger.error(f"Failed to get context from provider: {e}")
            return RenderingContext.UNKNOWN

    def determine_context_from_scene(self, scene: Any) -> Any:
        """
        Determine context from a pictograph scene (fallback method).

        This method provides backward compatibility while encouraging migration
        to explicit context declaration.

        Args:
            scene: The pictograph scene object

        Returns:
            The determined rendering context
        """
        if not scene:
            logger.warning("Scene is None, returning UNKNOWN context")
            return RenderingContext.UNKNOWN

        # Check if scene has explicit context
        if hasattr(scene, "rendering_context"):
            context = getattr(scene, "rendering_context")
            if isinstance(context, RenderingContext):
                logger.debug(f"Scene has explicit context: {context.value}")
                return context

        # Check if scene has a context provider parent
        parent = getattr(scene, "parent", lambda: None)()
        if parent and isinstance(parent, IPictographContextProvider):
            logger.debug(f"Found context provider parent: {parent.__class__.__name__}")
            return self.determine_context_from_provider(parent)

        # Check if scene has a registered component ID
        scene_id = getattr(scene, "component_id", None)
        if scene_id:
            return self.get_context_for_component(scene_id)

        # Fallback: limited safe detection for backward compatibility
        return self._safe_fallback_detection(scene)

    def _safe_fallback_detection(self, scene: Any) -> RenderingContext:
        """
        Safe fallback detection with minimal string matching.

        This is a temporary bridge for components that haven't migrated
        to explicit context declaration yet.
        """
        try:
            parent = getattr(scene, "parent", lambda: None)()
            if not parent:
                logger.debug("No parent found for scene, returning UNKNOWN")
                return RenderingContext.UNKNOWN

            # Very limited, safe class name checking
            class_name = parent.__class__.__name__.lower()

            # Only check for very specific, stable class names
            if class_name == "grapheditorwidget":
                logger.debug("Detected graph editor context via safe fallback")
                return RenderingContext.GRAPH_EDITOR
            elif class_name == "beatframewidget":
                logger.debug("Detected beat frame context via safe fallback")
                return RenderingContext.BEAT_FRAME
            else:
                logger.debug(f"Unknown parent class {class_name}, returning UNKNOWN")
                return RenderingContext.UNKNOWN

        except Exception as e:
            logger.error(f"Fallback detection failed: {e}")
            return RenderingContext.UNKNOWN


class ContextAwareComponent:
    """
    Mixin class for components that need to declare their rendering context.

    Components can inherit from this to easily provide context information.
    """

    def __init__(
        self, rendering_context: RenderingContext, component_id: Optional[str] = None
    ):
        """
        Initialize context-aware component.

        Args:
            rendering_context: The rendering context for this component
            component_id: Optional unique identifier for registration
        """
        self.rendering_context = rendering_context
        self.component_id = component_id or f"{self.__class__.__name__}_{id(self)}"

    def get_rendering_context(self) -> RenderingContext:
        """Return the rendering context for this component."""
        return self.rendering_context


def create_context_aware_scene(
    rendering_context: RenderingContext, scene_class: type, *args, **kwargs
):
    """
    Factory function to create context-aware pictograph scenes.

    Args:
        rendering_context: The rendering context for the scene
        scene_class: The scene class to instantiate
        *args, **kwargs: Arguments to pass to the scene constructor

    Returns:
        Scene instance with explicit rendering context
    """
    scene = scene_class(*args, **kwargs)
    scene.rendering_context = rendering_context
    scene.component_id = f"{scene_class.__name__}_{id(scene)}"

    logger.debug(f"Created context-aware scene with context: {rendering_context.value}")
    return scene
