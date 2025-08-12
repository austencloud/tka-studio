"""
Framework-Agnostic Data Types

These types replace QT-specific types (QSize, QWidget, etc.) to enable
true framework independence for core services.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Protocol

# ============================================================================
# GEOMETRY AND LAYOUT TYPES
# ============================================================================


@dataclass(frozen=True)
class Size:
    """Framework-agnostic size representation (replaces QSize)."""

    width: int
    height: int

    def __post_init__(self):
        if self.width < 0 or self.height < 0:
            raise ValueError("Size dimensions must be non-negative")

    @property
    def scale(self, factor: float) -> "Size":
        """Scale size by factor while maintaining aspect ratio."""
        return Size(width=int(self.width * factor), height=int(self.height * factor))

    def fit_within(self, container: "Size") -> "Size":
        """Scale to fit within container while maintaining aspect ratio."""
        if self.width <= container.width and self.height <= container.height:
            return self

        scale_x = container.width / self.width
        scale_y = container.height / self.height
        scale_factor = min(scale_x, scale_y)

        return self.scale(scale_factor)


@dataclass(frozen=True)
class Point:
    """Framework-agnostic point representation."""

    x: int
    y: int

    def translate(self, dx: int, dy: int) -> "Point":
        """Translate point by offset."""
        return Point(self.x + dx, self.y + dy)


@dataclass(frozen=True)
class Rect:
    """Framework-agnostic rectangle representation."""

    x: int
    y: int
    width: int
    height: int

    @property
    @property
    def center(self) -> Point:
        return Point(self.x + self.width // 2, self.y + self.height // 2)

    @property
    def size(self) -> Size:
        return Size(self.width, self.height)

    def contains(self, point: Point) -> bool:
        """Check if rectangle contains point."""
        return (
            self.x <= point.x <= self.x + self.width
            and self.y <= point.y <= self.y + self.height
        )


# ============================================================================
# COLOR AND STYLING TYPES
# ============================================================================


@dataclass(frozen=True)
class Color:
    """Framework-agnostic color representation."""

    red: int
    green: int
    blue: int
    alpha: int = 255

    def __post_init__(self):
        for component in [self.red, self.green, self.blue, self.alpha]:
            if not 0 <= component <= 255:
                raise ValueError("Color components must be 0-255")

    @classmethod
    def from_hex(cls, hex_color: str) -> "Color":
        """Create color from hex string (e.g., '#FF0000' or 'FF0000')."""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:
            return cls(
                red=int(hex_color[0:2], 16),
                green=int(hex_color[2:4], 16),
                blue=int(hex_color[4:6], 16),
            )
        elif len(hex_color) == 8:
            return cls(
                red=int(hex_color[0:2], 16),
                green=int(hex_color[2:4], 16),
                blue=int(hex_color[4:6], 16),
                alpha=int(hex_color[6:8], 16),
            )
        else:
            raise ValueError("Invalid hex color format")

    def to_hex(self) -> str:
        """Convert to hex string."""
        if self.alpha == 255:
            return f"#{self.red:02X}{self.green:02X}{self.blue:02X}"
        else:
            return f"#{self.red:02X}{self.green:02X}{self.blue:02X}{self.alpha:02X}"

    def to_rgba_tuple(self) -> tuple[int, int, int, int]:
        """Convert to RGBA tuple."""
        return (self.red, self.green, self.blue, self.alpha)


# Common colors
class Colors:
    BLACK = Color(0, 0, 0)
    RED = Color(255, 0, 0)
    BLUE = Color(0, 0, 255)


# ============================================================================
# RENDERING TYPES
# ============================================================================


class RenderTargetType(Enum):
    """Types of rendering targets."""

    GRAPHICS_SCENE = auto()
    IMAGE_BUFFER = auto()
    SVG_DOCUMENT = auto()
    CANVAS = auto()


@dataclass
class RenderTarget:
    """Framework-agnostic render target."""

    target_id: str
    target_type: RenderTargetType
    size: Size
    properties: dict[str, Any]

    # Framework-specific handle (e.g., QGraphicsScene, HTML Canvas, etc.)
    native_handle: Any | None = None


@dataclass
class RenderCommand:
    """Framework-agnostic rendering command."""

    command_id: str
    target_id: str
    render_type: str
    position: Point
    size: Size
    properties: dict[str, Any]
    data: Any | None = None


class ImageFormat(Enum):
    """Supported image formats."""

    PNG = "png"
    JPEG = "jpeg"
    SVG = "svg"
    WEBP = "webp"


@dataclass
class ImageData:
    """Framework-agnostic image data."""

    width: int
    height: int
    format: ImageFormat
    data: bytes = b""  # Optional for export specifications
    metadata: dict[str, Any] = None
    background_color: Color | None = None
    render_commands: list[dict[str, Any]] | None = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.render_commands is None:
            self.render_commands = []


# ============================================================================
# COMPONENT HANDLE TYPES
# ============================================================================


@dataclass
class ComponentHandle:
    """Framework-agnostic component handle (replaces widget references)."""

    component_id: str
    component_type: str
    properties: dict[str, Any]

    # Framework-specific handle (e.g., QWidget, HTML Element, etc.)
    native_handle: Any | None = None


class WindowState(Enum):
    """Window states."""

    NORMAL = auto()
    MINIMIZED = auto()
    MAXIMIZED = auto()
    HIDDEN = auto()


@dataclass
class WindowHandle:
    """Framework-agnostic window handle (replaces QWidget references)."""

    window_id: str
    title: str
    size: Size
    position: Point
    state: WindowState
    properties: dict[str, Any]

    # Framework-specific handle (e.g., QMainWindow, browser window, etc.)
    native_handle: Any | None = None


# ============================================================================
# ASSET AND RESOURCE TYPES
# ============================================================================


@dataclass
class AssetHandle:
    """Framework-agnostic asset handle."""

    asset_id: str
    asset_type: str
    path: str
    size: Size | None = None
    metadata: dict[str, Any] = None


@dataclass
class SvgAsset:
    """Framework-agnostic SVG asset."""

    asset_id: str
    svg_content: str
    original_size: Size
    color_properties: dict[str, str]  # Map of color attributes to values

    def get_colored_svg(self, color_map: dict[str, Color]) -> str:
        """Get SVG content with colors replaced."""
        svg_content = self.svg_content
        for property_name, new_color in color_map.items():
            if property_name in self.color_properties:
                old_color = self.color_properties[property_name]
                svg_content = svg_content.replace(old_color, new_color.to_hex())
        return svg_content


# ============================================================================
# PROTOCOL INTERFACES
# ============================================================================


class RenderEngine(Protocol):
    """Protocol for framework-specific render engines."""

    def execute_command(self, command: RenderCommand, target: RenderTarget) -> bool:
        """Execute a render command on the target."""
        ...

    def create_image(self, size: Size, format: ImageFormat) -> ImageData:
        """Create an empty image of specified size and format."""
        ...

    def render_to_image(
        self, commands: list[RenderCommand], size: Size, format: ImageFormat
    ) -> ImageData:
        """Render commands to an image."""
        ...


class AssetLoader(Protocol):
    """Protocol for loading and caching assets."""

    def load_svg_asset(self, path: str) -> SvgAsset | None:
        """Load an SVG asset from path."""
        ...

    def get_cached_asset(self, asset_id: str) -> AssetHandle | None:
        """Get cached asset by ID."""
        ...


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
