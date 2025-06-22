"""
Pictograph Orchestrator

Orchestrates pictograph operations using focused services.
Replaces the monolithic PictographManagementService with clean architecture.

PROVIDES:
- Complete pictograph management pipeline coordination
- Service composition and orchestration
- Clean separation of concerns
- Context-aware pictograph configuration
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from domain.models.core_models import BeatData
from domain.models.pictograph_models import (
    ArrowData,
    GridData,
    GridMode,
    PictographData,
    PropData,
)

from ..data.csv_data_service import CSVDataService, ICSVDataService
from ..data.dataset_management_service import (
    DatasetManagementService,
    IDatasetManagementService,
    PictographSearchQuery,
)
from ..data.glyph_generation_service import (
    GlyphGenerationService,
    IGlyphGenerationService,
)


class PictographContext(Enum):
    """Pictograph context types."""

    SEQUENCE_EDITOR = "sequence_editor"
    STANDALONE_VIEWER = "standalone_viewer"
    DICTIONARY_BROWSER = "dictionary_browser"
    COMPARISON_VIEW = "comparison_view"


class IPictographOrchestrator(ABC):
    """Interface for pictograph orchestration."""

    @abstractmethod
    def create_pictograph(
        self, grid_mode: GridMode = GridMode.DIAMOND
    ) -> PictographData:
        """Create a new blank pictograph."""
        pass

    @abstractmethod
    def create_from_beat(self, beat_data: BeatData) -> PictographData:
        """Create pictograph from beat data."""
        pass

    @abstractmethod
    def update_pictograph_arrows(
        self, pictograph: PictographData, arrows: Dict[str, ArrowData]
    ) -> PictographData:
        """Update arrows in pictograph."""
        pass

    @abstractmethod
    def search_dataset(self, query: PictographSearchQuery) -> List[PictographData]:
        """Search pictograph dataset with query."""
        pass


class PictographOrchestrator(IPictographOrchestrator):
    """
    Orchestrates pictograph operations using focused services.

    Coordinates CSV data, glyph generation, and dataset management services.
    Returns immutable pictograph data following TKA architecture.
    """

    def __init__(
        self,
        csv_service: Optional[ICSVDataService] = None,
        glyph_service: Optional[IGlyphGenerationService] = None,
        dataset_service: Optional[IDatasetManagementService] = None,
    ):
        """Initialize with dependency injection."""
        self.csv_service = csv_service or CSVDataService()
        self.glyph_service = glyph_service or GlyphGenerationService()
        self.dataset_service = dataset_service or DatasetManagementService()

        # Context configuration
        self._context_configs = self._load_context_configs()

    def create_pictograph(
        self, grid_mode: GridMode = GridMode.DIAMOND
    ) -> PictographData:
        """Create a new blank pictograph."""
        grid_data = GridData(
            grid_mode=grid_mode,
            center_x=200.0,
            center_y=200.0,
            radius=100.0,
        )

        return PictographData(
            grid_data=grid_data,
            arrows={},
            props={},
            is_blank=True,
            metadata={"created_by": "pictograph_orchestrator"},
        )

    def create_from_beat(self, beat_data: BeatData) -> PictographData:
        """Create pictograph from beat data with glyph generation."""
        pictograph = self.create_pictograph()

        # Add arrows based on beat motions
        arrows = {}

        if beat_data.blue_motion:
            arrows["blue"] = ArrowData(
                color="blue",
                motion_data=beat_data.blue_motion,
                is_visible=True,
            )

        if beat_data.red_motion:
            arrows["red"] = ArrowData(
                color="red",
                motion_data=beat_data.red_motion,
                is_visible=True,
            )

        # Generate glyph data using glyph service
        glyph_data = self.glyph_service.generate_glyph_data(beat_data)

        return pictograph.update(
            arrows=arrows,
            is_blank=len(arrows) == 0,
            metadata={
                "created_from_beat": beat_data.beat_number,
                "letter": beat_data.letter,
                "glyph_data": glyph_data.to_dict() if glyph_data else None,
            },
        )

    def update_pictograph_arrows(
        self, pictograph: PictographData, arrows: Dict[str, ArrowData]
    ) -> PictographData:
        """Update arrows in pictograph."""
        return pictograph.update(
            arrows=arrows,
            is_blank=len(arrows) == 0,
        )

    def search_dataset(self, query: PictographSearchQuery) -> List[PictographData]:
        """Search pictograph dataset using dataset service."""
        return self.dataset_service.search_dataset(query)

    def configure_for_context(
        self, pictograph: PictographData, context: PictographContext
    ) -> PictographData:
        """Configure pictograph for specific context."""
        context_config = self._context_configs.get(context, {})

        # Apply context-specific modifications
        metadata = pictograph.metadata.copy()
        metadata.update(
            {
                "context": context.value,
                "context_config": context_config,
            }
        )

        return pictograph.update(metadata=metadata)

    def get_glyph_for_pictograph(self, pictograph: PictographData) -> Optional[str]:
        """Get glyph representation for pictograph using glyph service."""
        # Extract beat data from pictograph for glyph generation
        beat_data = self._extract_beat_data_from_pictograph(pictograph)
        if not beat_data:
            return None

        glyph_key = self.glyph_service.generate_glyph_key(beat_data)
        return self.glyph_service.get_glyph_symbol(glyph_key)

    def add_to_dataset(
        self, pictograph: PictographData, category: str = "user_created"
    ) -> str:
        """Add pictograph to dataset using dataset service."""
        return self.dataset_service.add_to_dataset(pictograph, category)

    def get_dataset_categories(self) -> List[str]:
        """Get all available dataset categories."""
        return self.dataset_service.get_dataset_categories()

    def get_pictographs_by_category(self, category: str) -> List[PictographData]:
        """Get all pictographs in a category."""
        return self.dataset_service.get_pictographs_by_category(category)

    def get_pictographs_by_letter(self, letter: str) -> List[BeatData]:
        """Get all pictographs for a specific letter using CSV service."""
        return self.csv_service.get_pictographs_by_letter(letter)

    def get_specific_pictograph(
        self, letter: str, index: int = 0
    ) -> Optional[BeatData]:
        """Get a specific pictograph by letter and index using CSV service."""
        return self.csv_service.get_specific_pictograph(letter, index)

    def get_start_position_pictograph(
        self, position_key: str, grid_mode: str = "diamond"
    ) -> Optional[BeatData]:
        """Get start position pictograph using CSV service."""
        return self.csv_service.get_start_position_pictograph(position_key, grid_mode)

    def _extract_beat_data_from_pictograph(
        self, pictograph: PictographData
    ) -> Optional[BeatData]:
        """Extract beat data from pictograph for glyph generation."""
        if not pictograph.arrows:
            return None

        # Extract motion data from arrows
        blue_motion = None
        red_motion = None

        if "blue" in pictograph.arrows:
            blue_motion = pictograph.arrows["blue"].motion_data

        if "red" in pictograph.arrows:
            red_motion = pictograph.arrows["red"].motion_data

        # Create beat data
        return BeatData(
            beat_number=pictograph.metadata.get("created_from_beat", 1),
            letter=pictograph.metadata.get("letter"),
            blue_motion=blue_motion,
            red_motion=red_motion,
        )

    def _load_context_configs(
        self,
    ) -> Dict[PictographContext, Dict[str, Union[str, int, bool]]]:
        """Load context-specific configurations."""
        return {
            PictographContext.SEQUENCE_EDITOR: {
                "show_grid": True,
                "show_arrows": True,
                "interactive": True,
            },
            PictographContext.STANDALONE_VIEWER: {
                "show_grid": False,
                "show_arrows": True,
                "interactive": False,
            },
            PictographContext.DICTIONARY_BROWSER: {
                "show_grid": False,
                "show_arrows": True,
                "interactive": False,
                "compact_view": True,
            },
        }
