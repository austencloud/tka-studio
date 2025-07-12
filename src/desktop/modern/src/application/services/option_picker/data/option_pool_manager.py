"""
Pool Manager - UI Adapter for Object Pool Management

This is now a thin UI adapter that delegates business logic to the
ObjectPoolService. It maintains backward compatibility while using
the extracted business service and handles Qt-specific concerns.
"""

import logging
import weakref
from typing import TYPE_CHECKING, Callable, List, Optional

from core.interfaces.core_services import IObjectPoolManager
from domain.models.enums import GridMode
from domain.models.grid_data import GridData
from domain.models.pictograph_data import PictographData
from presentation.components.option_picker.components.frames.pictograph_option_frame import (
    PictographOptionFrame,
)
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class OptionPoolManager(QObject):
    """
    UI adapter for pictograph object pool management.

    This class now delegates business logic to the IObjectPoolService
    while maintaining Qt-specific functionality and the same public interface
    for backward compatibility.
    """

    MAX_PICTOGRAPHS = 36  # Same as Legacy's OptionFactory.MAX_PICTOGRAPHS

    def __init__(
        self, parent_widget: QWidget, pool_service: Optional[IObjectPoolManager] = None
    ):
        """
        Initialize pictograph pool manager with injected business service.

        Args:
            parent_widget: Parent Qt widget for pictograph frames
            pool_service: Injected object pool service
        """
        super().__init__()
        self.parent_widget = parent_widget
        self._pictograph_pool: List[PictographOptionFrame] = []
        self._pool_initialized = False
        self._click_handler: Optional[Callable] = None
        self._pictograph_click_handler: Optional[Callable] = None
        self._pool_service = pool_service

        # Fallback for legacy compatibility - will be removed in future versions
        if not self._pool_service:
            try:
                from application.services.core.object_pool_manager import (
                    ObjectPoolManager,
                )

                self._pool_service = ObjectPoolManager()

            except ImportError:
                logger.error("Object pool service not available")
                self._pool_service = None

    def set_click_handler(self, handler: Callable[[str], None]) -> None:
        """Set the click handler for all pool objects"""
        self._click_handler = handler

    def set_pictograph_click_handler(self, pictograph_handler: Callable) -> None:
        """Set the pictograph click handler for all pool objects"""
        self._pictograph_click_handler = pictograph_handler

    def initialize_pool(self, progress_callback: Optional[Callable] = None) -> None:
        """
        Initialize pictograph object pool with progress updates.

        Args:
            progress_callback: Optional progress reporting callback
        """
        if self._pool_initialized:
            logger.debug("Pool already initialized")
            return

        if not self._pool_service:
            logger.error("Pool service not available, using fallback")
            return

        try:
            # WINDOW MANAGEMENT FIX: Prevent any window appearance during pool creation
            from PyQt6.QtCore import Qt
            from PyQt6.QtWidgets import QApplication

            # Create factory function for pictograph frames
            def pictograph_frame_factory() -> Optional[PictographOptionFrame]:
                frame = self._create_pictograph_frame()
                # POOL CREATION FIX: Ensure frame is completely hidden during creation
                if frame:
                    # Set additional window flags to prevent any appearance
                    frame.setWindowFlags(frame.windowFlags() | Qt.WindowType.Tool)
                    frame.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen, True)
                    frame.hide()
                    frame.setVisible(False)

                    if (
                        hasattr(frame, "pictograph_component")
                        and frame.pictograph_component
                    ):
                        frame.pictograph_component.setAttribute(
                            Qt.WidgetAttribute.WA_DontShowOnScreen, True
                        )
                        frame.pictograph_component.hide()
                        frame.pictograph_component.setVisible(False)
                return frame

            # Use business service to initialize pool
            self._pool_service.initialize_pool(
                pool_name="pictographs",
                max_objects=self.MAX_PICTOGRAPHS,
                object_factory=pictograph_frame_factory,
                progress_callback=progress_callback,
            )

            # Get the created objects from the service
            for i in range(self.MAX_PICTOGRAPHS):
                frame = self._pool_service.get_pooled_object("pictographs", i)
                if frame:
                    self._pictograph_pool.append(frame)

            self._pool_initialized = True

        except Exception as e:
            logger.error(f"Error initializing pool via service: {e}")
            # WINDOW MANAGEMENT FIX: Restore normal behavior even on error
            app = QApplication.instance()

    def _create_pictograph_frame(self) -> Optional[PictographOptionFrame]:
        """
        Create a single pictograph frame with real data.

        Returns:
            ClickablePictographFrame if successful, None otherwise
        """
        try:
            # Use dependency injection to get shared services
            from application.services.data.dataset_query import IDatasetQuery
            from application.services.data.position_resolver import PositionResolver
            from core.dependency_injection.di_container import get_container

            container = get_container()
            dataset_service = container.resolve(IDatasetQuery)
            position_resolver = PositionResolver()
            start_positions = position_resolver.get_start_positions("diamond")

            # Cycle through start positions
            position_key = start_positions[
                len(self._pictograph_pool) % len(start_positions)
            ]
            # Use the new pictograph-based approach
            real_pictograph_data = dataset_service.get_start_position_pictograph_data(
                position_key, "diamond"
            )

            if real_pictograph_data is None:
                # Fallback to creating minimal pictograph data
                real_pictograph_data = self._create_minimal_pictograph_data()

            # Create frame directly with PictographData
            # Use parent=None to avoid RuntimeError that causes pictograph_component to be None
            # The frame is designed to handle parent=None safely with proper cleanup
            frame = PictographOptionFrame(real_pictograph_data, parent=None)

            # Store reference to main widget for proper cleanup later
            frame._pool_manager_ref = weakref.ref(self)

            # Debug: Check if pictograph_component was created successfully
            if hasattr(frame, "pictograph_component") and frame.pictograph_component:
                logger.debug(
                    f"✅ Frame {len(self._pictograph_pool)} created with pictograph_component"
                )
            else:
                logger.warning(
                    f"❌ Frame {len(self._pictograph_pool)} created WITHOUT pictograph_component"
                )

            # Set up event handlers
            if self._click_handler:
                frame.clicked.connect(self._click_handler)
            if self._pictograph_click_handler:
                frame.pictograph_clicked.connect(self._pictograph_click_handler)

            frame.setVisible(False)
            frame.set_container_widget(self.parent_widget)

            return frame

        except Exception as e:
            logger.error(f"Error creating pictograph frame: {e}")
            return None

    def get_pictograph_from_pool(self, index: int) -> Optional[PictographOptionFrame]:
        """Get frame from pool at specified index"""
        if 0 <= index < len(self._pictograph_pool):
            return self._pictograph_pool[index]
        return None

    def get_pool_size(self) -> int:
        """Get current pool size"""
        return len(self._pictograph_pool)

    def resize_all_frames(self) -> None:
        """Resize all frames using Legacy's algorithm"""
        for frame in self._pictograph_pool:
            if frame and hasattr(frame, "resize_frame"):
                try:
                    frame.resize_frame()
                except RuntimeError:
                    pass

    def _create_minimal_pictograph_data(self):
        """Create minimal pictograph data as fallback."""
        from domain.models.arrow_data import ArrowData
        from domain.models.enums import Location, MotionType, RotationDirection
        from domain.models.motion_data import MotionData

        # Create motion data
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            turns=0.0,
            start_ori="in",
            end_ori="in",
        )

        red_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.SOUTH,
            end_loc=Location.WEST,
            turns=0.0,
            start_ori="in",
            end_ori="in",
        )

        # Create arrow data (without motion_data - motion data now in motions dictionary)
        blue_arrow = ArrowData(color="blue", is_visible=True)
        red_arrow = ArrowData(color="red", is_visible=True)

        # Create grid data
        grid_data = GridData(grid_mode=GridMode.DIAMOND)

        # Create pictograph data with motions dictionary
        return PictographData(
            grid_data=grid_data,
            arrows={"blue": blue_arrow, "red": red_arrow},
            props={},
            motions={"blue": blue_motion, "red": red_motion},  # Add motions dictionary
            letter="A",
            metadata={"source": "fallback"},
        )

    def cleanup(self) -> None:
        """Clean up pool manager resources and ensure proper memory management."""
        try:
            # Clean up all frames in the pool
            for frame in self._pictograph_pool:
                if frame and hasattr(frame, "cleanup"):
                    frame.cleanup()

            # Clear the pool
            self._pictograph_pool.clear()

            # Clean up pool service if available
            if hasattr(self._pool_service, "cleanup"):
                self._pool_service.cleanup()

            logger.debug("Pool manager cleaned up successfully")

        except Exception as e:
            logger.error(f"Error during pool manager cleanup: {e}")
