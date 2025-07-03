"""
Pool Manager - UI Adapter for Object Pool Management

This is now a thin UI adapter that delegates business logic to the
ObjectPoolService. It maintains backward compatibility while using
the extracted business service and handles Qt-specific concerns.
"""

import logging
from typing import TYPE_CHECKING, List, Optional, Callable
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject

from domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)
from core.interfaces.core_services import IObjectPoolService
from presentation.components.option_picker.components.frames.clickable_pictograph_frame import (
    ClickablePictographFrame,
)

if TYPE_CHECKING:
    from application.services.data.pictograph_dataset_service import (
        PictographDatasetService,
    )

logger = logging.getLogger(__name__)


class PictographPoolManager(QObject):
    """
    UI adapter for pictograph object pool management.

    This class now delegates business logic to the IObjectPoolService
    while maintaining Qt-specific functionality and the same public interface
    for backward compatibility.
    """

    MAX_PICTOGRAPHS = 36  # Same as Legacy's OptionFactory.MAX_PICTOGRAPHS

    def __init__(
        self, parent_widget: QWidget, pool_service: Optional[IObjectPoolService] = None
    ):
        """
        Initialize pictograph pool manager with injected business service.

        Args:
            parent_widget: Parent Qt widget for pictograph frames
            pool_service: Injected object pool service
        """
        super().__init__()
        self.parent_widget = parent_widget
        self._pictograph_pool: List[ClickablePictographFrame] = []
        self._pool_initialized = False
        self._click_handler: Optional[Callable] = None
        self._beat_data_click_handler: Optional[Callable] = None
        self._pool_service = pool_service

        # Fallback for legacy compatibility - will be removed in future versions
        if not self._pool_service:
            try:
                from application.services.core.object_pool_service import (
                    ObjectPoolService,
                )

                self._pool_service = ObjectPoolService()
                logger.warning(
                    "Using fallback object pool service - consider using DI container"
                )
            except ImportError:
                logger.error("Object pool service not available")
                self._pool_service = None

    def set_click_handler(self, handler: Callable[[str], None]) -> None:
        """Set the click handler for all pool objects"""
        self._click_handler = handler

    def set_beat_data_click_handler(self, beat_data_handler: Callable) -> None:
        """Set the beat data click handler for all pool objects"""
        self._beat_data_click_handler = beat_data_handler

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
            self._create_fallback_pool(progress_callback)
            return

        try:
            # Create factory function for pictograph frames
            def pictograph_frame_factory() -> Optional[ClickablePictographFrame]:
                return self._create_pictograph_frame()

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

            logger.info(
                f"Pictograph pool initialized with {len(self._pictograph_pool)} objects"
            )

        except Exception as e:
            logger.error(f"Error initializing pool via service: {e}")
            self._create_fallback_pool(progress_callback)

    def _create_pictograph_frame(self) -> Optional[ClickablePictographFrame]:
        """
        Create a single pictograph frame with real data.

        Returns:
            ClickablePictographFrame if successful, None otherwise
        """
        try:
            from application.services.data.pictograph_dataset_service import (
                PictographDatasetService,
            )

            dataset_service = PictographDatasetService()
            start_positions = ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]

            # Cycle through start positions
            position_key = start_positions[
                len(self._pictograph_pool) % len(start_positions)
            ]
            real_beat_data = dataset_service.get_start_position_pictograph(
                position_key, "diamond"
            )

            if real_beat_data is None:
                real_beat_data = self._get_fallback_beat_data(dataset_service)

            if real_beat_data is None:
                real_beat_data = self._create_minimal_beat_data()

            frame = ClickablePictographFrame(real_beat_data, parent=self.parent_widget)

            # Set up event handlers
            if self._click_handler:
                frame.clicked.connect(self._click_handler)
            if self._beat_data_click_handler:
                frame.beat_data_clicked.connect(self._beat_data_click_handler)

            frame.setVisible(False)
            frame.set_container_widget(self.parent_widget)

            return frame

        except Exception as e:
            logger.error(f"Error creating pictograph frame: {e}")
            return None

    def _get_fallback_beat_data(
        self, dataset_service: "PictographDatasetService"
    ) -> Optional[BeatData]:
        """Get fallback beat data from dataset"""
        if (
            hasattr(dataset_service, "_diamond_dataset")
            and dataset_service._diamond_dataset is not None
        ):
            if not dataset_service._diamond_dataset.empty:
                first_entry = dataset_service._diamond_dataset.iloc[0]
                return dataset_service._dataset_entry_to_beat_data(first_entry)
        return None

    def _create_minimal_beat_data(self) -> BeatData:
        """Create minimal valid beat data as final fallback"""
        return BeatData(
            letter="A",
            blue_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
                turns=1.0,
                start_ori="in",
                end_ori="out",
            ),
            red_motion=MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.NORTH,
                turns=1.0,
                start_ori="in",
                end_ori="out",
            ),
        )

    def _create_fallback_pool(
        self, progress_callback: Optional[Callable] = None
    ) -> None:
        """Create fallback pool with minimal beat data"""
        if progress_callback:
            progress_callback("Dataset failed, using fallback pool", 0.7)

        for i in range(self.MAX_PICTOGRAPHS):
            try:
                dummy_beat = self._create_minimal_beat_data()
                frame = ClickablePictographFrame(dummy_beat, parent=self.parent_widget)
                if self._click_handler:
                    frame.clicked.connect(self._click_handler)
                if self._beat_data_click_handler:
                    frame.beat_data_clicked.connect(self._beat_data_click_handler)
                frame.setVisible(False)
                frame.set_container_widget(self.parent_widget)
                self._pictograph_pool.append(frame)
            except Exception as e:
                print(f"❌ Failed to create fallback pool object {i}: {e}")
                break

    def get_pictograph_from_pool(
        self, index: int
    ) -> Optional[ClickablePictographFrame]:
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
