"""
Framework-Agnostic Thumbnail Service

Demonstrates how the thumbnail factory service can be refactored to be
framework-agnostic while maintaining compatibility with existing QT code.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

# Import framework-agnostic types
from desktop.modern.application.services.core.types import (
    ImageData,
    ImageFormat,
    Size,
)

logger = logging.getLogger(__name__)


# ============================================================================
# FRAMEWORK-AGNOSTIC CORE INTERFACES
# ============================================================================


@dataclass
class ThumbnailSpec:
    """Framework-agnostic thumbnail specification."""

    sequence_id: str
    sequence_name: str
    beat_count: int
    thumbnail_size: Size
    word: str | None = None
    thumbnail_paths: list[str] | None = None
    metadata: dict = None


@dataclass
class ThumbnailData:
    """Framework-agnostic thumbnail data."""

    thumbnail_id: str
    spec: ThumbnailSpec
    image_data: ImageData | None = None
    placeholder_text: str | None = None
    error_message: str | None = None

    @property
    def has_image(self) -> bool:
        return self.image_data is not None

    @property
    def has_error(self) -> bool:
        return self.error_message is not None


class IThumbnailImageLoader(Protocol):
    """Protocol for loading thumbnail images."""

    def load_image(self, image_path: str, target_size: Size) -> ImageData | None:
        """Load and resize image from path."""
        ...

    def create_placeholder_image(self, text: str, size: Size, style: dict) -> ImageData:
        """Create placeholder image with text."""
        ...


class IThumbnailFactory(ABC):
    """Framework-agnostic interface for thumbnail creation."""

    @abstractmethod
    def create_thumbnail_data(
        self, sequence_spec: ThumbnailSpec, options: dict | None = None
    ) -> ThumbnailData:
        """Create thumbnail data (framework-agnostic)."""

    @abstractmethod
    def batch_create_thumbnails(
        self, sequence_specs: list[ThumbnailSpec], options: dict | None = None
    ) -> list[ThumbnailData]:
        """Create multiple thumbnails efficiently."""


# ============================================================================
# CORE THUMBNAIL SERVICE (FRAMEWORK-AGNOSTIC)
# ============================================================================


class CoreThumbnailService(IThumbnailFactory):
    """
    Framework-agnostic core thumbnail service.

    Contains pure business logic for thumbnail creation without any
    UI framework dependencies.
    """

    def __init__(self, image_loader: IThumbnailImageLoader):
        """Initialize with image loader."""
        self.image_loader = image_loader
        self._thumbnail_counter = 0
        logger.info("Core thumbnail service initialized")

    def create_thumbnail_data(
        self, sequence_spec: ThumbnailSpec, options: dict | None = None
    ) -> ThumbnailData:
        """
        Create thumbnail data from sequence specification.

        Args:
            sequence_spec: Sequence specification for thumbnail
            options: Optional creation options

        Returns:
            ThumbnailData with image or placeholder
        """
        try:
            options = options or {}
            thumbnail_id = self._generate_thumbnail_id()

            # Try to load actual thumbnail image
            image_data = self._load_sequence_thumbnail_image(sequence_spec)

            if image_data:
                return ThumbnailData(
                    thumbnail_id=thumbnail_id, spec=sequence_spec, image_data=image_data
                )
            else:
                # Create placeholder
                placeholder_text = self._generate_placeholder_text(sequence_spec)
                placeholder_image = self._create_placeholder_thumbnail(
                    placeholder_text,
                    sequence_spec.thumbnail_size,
                    options.get("placeholder_style", {}),
                )

                return ThumbnailData(
                    thumbnail_id=thumbnail_id,
                    spec=sequence_spec,
                    image_data=placeholder_image,
                    placeholder_text=placeholder_text,
                )

        except Exception as e:
            logger.error(
                f"Failed to create thumbnail for {sequence_spec.sequence_id}: {e}"
            )
            return ThumbnailData(
                thumbnail_id=self._generate_thumbnail_id(),
                spec=sequence_spec,
                error_message=str(e),
            )

    def batch_create_thumbnails(
        self, sequence_specs: list[ThumbnailSpec], options: dict | None = None
    ) -> list[ThumbnailData]:
        """Create multiple thumbnails efficiently."""
        try:
            thumbnails = []

            for spec in sequence_specs:
                thumbnail_data = self.create_thumbnail_data(spec, options)
                thumbnails.append(thumbnail_data)

            logger.info(f"Created {len(thumbnails)} thumbnails in batch")
            return thumbnails

        except Exception as e:
            logger.error(f"Failed to create thumbnail batch: {e}")
            # Return error thumbnails for all specs
            return [
                ThumbnailData(
                    thumbnail_id=self._generate_thumbnail_id(),
                    spec=spec,
                    error_message=str(e),
                )
                for spec in sequence_specs
            ]

    def _load_sequence_thumbnail_image(self, spec: ThumbnailSpec) -> ImageData | None:
        """Load thumbnail image for sequence."""
        if not spec.thumbnail_paths:
            return None

        # Try each thumbnail path until one works
        for thumbnail_path in spec.thumbnail_paths:
            try:
                image_data = self.image_loader.load_image(
                    thumbnail_path, spec.thumbnail_size
                )
                if image_data:
                    logger.debug(f"Loaded thumbnail image: {thumbnail_path}")
                    return image_data
            except Exception as e:
                logger.warning(f"Failed to load thumbnail {thumbnail_path}: {e}")
                continue

        return None

    def _generate_placeholder_text(self, spec: ThumbnailSpec) -> str:
        """Generate placeholder text for thumbnail."""
        if spec.word:
            return f"📄\n{spec.word}"
        elif spec.sequence_name:
            return f"📄\n{spec.sequence_name}"
        else:
            return f"📄\nSequence\n{spec.beat_count} beats"

    def _create_placeholder_thumbnail(
        self, text: str, size: Size, style: dict
    ) -> ImageData:
        """Create placeholder thumbnail image."""
        try:
            # Use image loader to create placeholder
            return self.image_loader.create_placeholder_image(text, size, style)
        except Exception as e:
            logger.error(f"Failed to create placeholder: {e}")
            # Return minimal error image
            return ImageData(
                width=size.width,
                height=size.height,
                format=ImageFormat.PNG,
                data=b"",  # Empty data - would be handled by specific implementations
                metadata={"error": str(e)},
            )

    def _generate_thumbnail_id(self) -> str:
        """Generate unique thumbnail ID."""
        self._thumbnail_counter += 1
        return f"thumb_{self._thumbnail_counter:06d}"


# ============================================================================
# MOCK IMAGE LOADER FOR TESTING
# ============================================================================


class FileSystemImageLoader(IThumbnailImageLoader):
    """File system image loader for real asset loading."""

    def __init__(self, asset_base_path: str = "assets"):
        """Initialize with asset base path."""
        self.asset_base_path = Path(asset_base_path)

    def load_image(self, image_path: str, target_size: Size) -> ImageData | None:
        """Load image from file system."""
        try:
            image_path_obj = Path(image_path)
            if not image_path_obj.exists():
                logger.warning(f"Image file not found: {image_path_obj}")
                return None

            # Read image data
            image_data = image_path_obj.read_bytes()

            # Determine format from extension
            format_map = {
                ".png": ImageFormat.PNG,
                ".jpg": ImageFormat.JPEG,
                ".jpeg": ImageFormat.JPEG,
                ".svg": ImageFormat.SVG,
                ".webp": ImageFormat.WEBP,
            }

            file_format = format_map.get(image_path_obj.suffix.lower(), ImageFormat.PNG)

            return ImageData(
                width=target_size.width,  # Would need actual image processing to get real size
                height=target_size.height,
                format=file_format,
                data=image_data,
                metadata={"source": str(image_path_obj), "loader": "filesystem"},
            )

        except Exception as e:
            logger.error(f"Failed to load image {image_path}: {e}")
            return None

    def create_placeholder_image(self, text: str, size: Size, style: dict) -> ImageData:
        """Create simple placeholder image data."""
        try:
            # Create minimal SVG placeholder
            svg_content = f"""
            <svg width="{size.width}" height="{size.height}" xmlns="http://www.w3.org/2000/svg">
                <rect width="100%" height="100%" fill="#f0f0f0" stroke="#ccc"/>
                <text x="50%" y="50%" text-anchor="middle" dy=".3em"
                      font-family="Arial" font-size="12" fill="#666">{text}</text>
            </svg>
            """

            return ImageData(
                width=size.width,
                height=size.height,
                format=ImageFormat.SVG,
                data=svg_content.encode(),
                metadata={"placeholder": True, "text": text, "style": style},
            )

        except Exception as e:
            logger.error(f"Failed to create placeholder: {e}")
            # Return minimal placeholder
            return ImageData(
                width=size.width,
                height=size.height,
                format=ImageFormat.PNG,
                data=b"",
                metadata={"error": str(e)},
            )


# ============================================================================
# CONVERSION UTILITIES
# ============================================================================


def convert_sequence_data_to_spec(sequence_data, thumbnail_width: int) -> ThumbnailSpec:
    """Convert sequence data to thumbnail specification."""
    return ThumbnailSpec(
        sequence_id=getattr(sequence_data, "id", "unknown"),
        sequence_name=getattr(sequence_data, "name", "Untitled"),
        beat_count=len(getattr(sequence_data, "beats", [])),
        thumbnail_size=Size(thumbnail_width, thumbnail_width),
        word=getattr(sequence_data, "word", None),
        thumbnail_paths=getattr(sequence_data, "thumbnail_paths", None),
        metadata=getattr(sequence_data, "metadata", {}),
    )


def batch_convert_sequences_to_specs(
    sequences: list, thumbnail_width: int
) -> list[ThumbnailSpec]:
    """Convert multiple sequence data objects to specs."""
    return [convert_sequence_data_to_spec(seq, thumbnail_width) for seq in sequences]
