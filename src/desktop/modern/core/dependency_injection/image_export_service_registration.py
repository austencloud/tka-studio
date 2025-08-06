"""
Image Export Service Registration

This module registers all image export services with the dependency injection container.
"""

from __future__ import annotations

import logging

from shared.application.services.image_export.sequence_image_layout_calculator import (
    SequenceImageLayoutCalculator,
)
from shared.application.services.image_export.sequence_metadata_extractor import (
    SequenceMetadataExtractor,
)

from desktop.modern.application.services.image_export.drawers.beat_drawer import (
    BeatDrawer,
)
from desktop.modern.application.services.image_export.drawers.difficulty_level_drawer import (
    DifficultyLevelDrawer,
)
from desktop.modern.application.services.image_export.drawers.font_margin_helper import (
    FontMarginHelper,
)
from desktop.modern.application.services.image_export.drawers.user_info_drawer import (
    UserInfoDrawer,
)
from desktop.modern.application.services.image_export.drawers.word_drawer import (
    WordDrawer,
)
from desktop.modern.application.services.image_export.sequence_image_exporter import (
    SequenceImageExporter,
)
from desktop.modern.application.services.image_export.sequence_image_renderer import (
    SequenceImageRenderer,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.image_export_services import (
    IBeatDrawer,
    IDifficultyLevelDrawer,
    IFontMarginHelper,
    ISequenceImageExporter,
    ISequenceImageLayoutCalculator,
    ISequenceImageRenderer,
    ISequenceMetadataExtractor,
    IUserInfoDrawer,
    IWordDrawer,
)


logger = logging.getLogger(__name__)


def register_image_export_services(container: DIContainer) -> None:
    """
    Register all image export services with the DI container.

    Args:
        container: The dependency injection container
    """

    try:
        # First register pictograph services that image export depends on
        _register_pictograph_services(container)

        # Register drawer services first (following Legacy drawer pattern)
        container.register_singleton(IFontMarginHelper, FontMarginHelper)
        container.register_factory(
            IWordDrawer, lambda: WordDrawer(container.resolve(IFontMarginHelper))
        )
        container.register_factory(
            IUserInfoDrawer,
            lambda: UserInfoDrawer(container.resolve(IFontMarginHelper)),
        )
        container.register_singleton(IDifficultyLevelDrawer, DifficultyLevelDrawer)
        container.register_factory(
            IBeatDrawer,
            lambda: BeatDrawer(container.resolve(IFontMarginHelper), container),
        )

        # Register core image export services as singletons
        # Pass container to image renderer so it can access pictograph services
        container.register_factory(
            ISequenceImageRenderer, lambda: SequenceImageRenderer(container=container)
        )
        container.register_singleton(
            ISequenceMetadataExtractor, SequenceMetadataExtractor
        )
        container.register_singleton(
            ISequenceImageLayoutCalculator, SequenceImageLayoutCalculator
        )

        # Register main export service as singleton
        container.register_singleton(ISequenceImageExporter, SequenceImageExporter)

    except Exception as e:
        logger.error(f"Failed to register image export services: {e}", exc_info=True)
        raise


def _register_pictograph_services(container: DIContainer) -> None:
    """Register pictograph services needed for real pictograph rendering."""
    try:
        # Temporarily ensure shared src is accessible for imports
        from pathlib import Path
        import sys

        # Find shared src path
        current_file = Path(__file__).resolve()
        tka_root = current_file.parents[6]  # Navigate up to TKA root
        shared_src = tka_root / "src"

        # Temporarily move shared src to front of path for imports
        shared_src_str = str(shared_src)
        if shared_src.exists() and shared_src_str in sys.path:
            sys.path.remove(shared_src_str)
            sys.path.insert(0, shared_src_str)

        # Import and register the pictograph service registrar
        from shared.application.services.core.registrars.pictograph_service_registrar import (
            PictographServiceRegistrar,
        )

        # Create and use the pictograph service registrar
        pictograph_registrar = PictographServiceRegistrar()
        pictograph_registrar.register_services(container)

        # CRITICAL FIX: Also register positioning services that pictograph scenes need
        _register_positioning_services(container)

    except Exception as e:
        logger.warning(f"Failed to register pictograph services: {e}")
        logger.info("Image export will fall back to simplified pictograph rendering")


def _register_positioning_services(container: DIContainer) -> None:
    """Register positioning services needed for pictograph scenes."""
    try:
        # Import and register the positioning service registrar
        from shared.application.services.core.registrars.positioning_service_registrar import (
            PositioningServiceRegistrar,
        )

        # Create and use the positioning service registrar
        positioning_registrar = PositioningServiceRegistrar()
        positioning_registrar.register_services(container)

    except Exception as e:
        logger.warning(f"Failed to register positioning services: {e}")
        logger.info("Image export will fall back to center positioning")
