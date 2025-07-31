"""
Web Pictograph Service Example

Demonstrates how the framework-agnostic core pictograph renderer can be used
in web services without any QT dependencies.
"""

import json
import logging
import os

# Import the framework-agnostic core services
import sys
from typing import Optional

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from shared.application.services.core.pictograph_renderer import (
    CorePictographRenderer,
    IPictographAssetProvider,
)
from shared.application.services.core.types import (
    RenderCommand,
    Size,
    SvgAsset,
)

logger = logging.getLogger(__name__)


# ============================================================================
# WEB ASSET PROVIDER
# ============================================================================


class WebAssetProvider(IPictographAssetProvider):
    """Web-specific asset provider using file system or CDN."""

    def __init__(self, assets_base_url: str = "/static/assets/"):
        """Initialize with base URL for assets."""
        self.assets_base_url = assets_base_url
        self._asset_cache: dict[str, SvgAsset] = {}
        logger.info(f"Web asset provider initialized with base URL: {assets_base_url}")

    def get_grid_asset(self, grid_mode: str) -> Optional[SvgAsset]:
        """Get grid asset for web rendering."""
        asset_key = f"grid_{grid_mode}"

        if asset_key not in self._asset_cache:
            self._asset_cache[asset_key] = self._create_web_grid_asset(grid_mode)

        return self._asset_cache[asset_key]

    def get_prop_asset(self, prop_type: str, color: str) -> Optional[SvgAsset]:
        """Get prop asset for web rendering."""
        asset_key = f"prop_{prop_type}"

        if asset_key not in self._asset_cache:
            self._asset_cache[asset_key] = self._create_web_prop_asset(prop_type)

        return self._asset_cache[asset_key]

    def get_glyph_asset(self, glyph_type: str, glyph_id: str) -> Optional[SvgAsset]:
        """Get glyph asset for web rendering."""
        asset_key = f"glyph_{glyph_type}_{glyph_id}"

        if asset_key not in self._asset_cache:
            self._asset_cache[asset_key] = self._create_web_glyph_asset(
                glyph_type, glyph_id
            )

        return self._asset_cache[asset_key]

    def get_arrow_asset(self, arrow_type: str) -> Optional[SvgAsset]:
        """Get arrow asset for web rendering."""
        asset_key = f"arrow_{arrow_type}"

        if asset_key not in self._asset_cache:
            self._asset_cache[asset_key] = self._create_web_arrow_asset(arrow_type)

        return self._asset_cache[asset_key]

    def _create_web_grid_asset(self, grid_mode: str) -> SvgAsset:
        """Create web-optimized grid asset."""
        if grid_mode == "diamond":
            svg_content = """
            <svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
                <polygon points="200,50 350,200 200,350 50,200"
                         fill="none" stroke="#cccccc" stroke-width="2"/>
                <line x1="200" y1="50" x2="200" y2="350" stroke="#cccccc" stroke-width="1" opacity="0.5"/>
                <line x1="50" y1="200" x2="350" y2="200" stroke="#cccccc" stroke-width="1" opacity="0.5"/>
            </svg>
            """
        else:  # box
            svg_content = """
            <svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
                <rect x="50" y="50" width="300" height="300"
                      fill="none" stroke="#cccccc" stroke-width="2"/>
                <line x1="200" y1="50" x2="200" y2="350" stroke="#cccccc" stroke-width="1" opacity="0.5"/>
                <line x1="50" y1="200" x2="350" y2="200" stroke="#cccccc" stroke-width="1" opacity="0.5"/>
            </svg>
            """

        return SvgAsset(
            asset_id=f"grid_{grid_mode}",
            svg_content=svg_content,
            original_size=Size(400, 400),
            color_properties={"stroke": "#cccccc"},
        )

    def _create_web_prop_asset(self, prop_type: str) -> SvgAsset:
        """Create web-optimized prop asset."""
        if prop_type.lower() == "staff":
            svg_content = """
            <svg viewBox="0 0 50 200" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="staffGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:#0066cc;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#004499;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <rect x="20" y="10" width="10" height="180" fill="url(#staffGradient)" rx="5"/>
                <circle cx="25" cy="15" r="8" fill="#0066cc"/>
                <circle cx="25" cy="185" r="8" fill="#0066cc"/>
            </svg>
            """
        else:
            # Default prop
            svg_content = """
            <svg viewBox="0 0 50 200" xmlns="http://www.w3.org/2000/svg">
                <rect x="20" y="10" width="10" height="180" fill="#0066cc" rx="5"/>
            </svg>
            """

        return SvgAsset(
            asset_id=f"prop_{prop_type}",
            svg_content=svg_content,
            original_size=Size(50, 200),
            color_properties={"fill": "#0066cc"},
        )

    def _create_web_glyph_asset(self, glyph_type: str, glyph_id: str) -> SvgAsset:
        """Create web-optimized glyph asset."""
        svg_content = f"""
        <svg viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">
            <text x="25" y="35" text-anchor="middle" font-family="Arial, sans-serif"
                  font-size="28" font-weight="bold" fill="#000000">{glyph_id}</text>
        </svg>
        """

        return SvgAsset(
            asset_id=f"glyph_{glyph_type}_{glyph_id}",
            svg_content=svg_content,
            original_size=Size(50, 50),
            color_properties={"fill": "#000000"},
        )

    def _create_web_arrow_asset(self, arrow_type: str) -> SvgAsset:
        """Create web-optimized arrow asset."""
        svg_content = """
        <svg viewBox="0 0 100 20" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="7"
                 refX="10" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#000000"/>
                </marker>
            </defs>
            <line x1="5" y1="10" x2="90" y2="10" stroke="#000000"
                  stroke-width="2" marker-end="url(#arrowhead)"/>
        </svg>
        """

        return SvgAsset(
            asset_id=f"arrow_{arrow_type}",
            svg_content=svg_content,
            original_size=Size(100, 20),
            color_properties={"stroke": "#000000", "fill": "#000000"},
        )


# ============================================================================
# WEB RENDER ENGINE
# ============================================================================


class WebRenderEngine:
    """Web-specific render engine that converts commands to web formats."""

    def render_to_svg(self, commands: list[RenderCommand], canvas_size: Size) -> str:
        """Render commands to a complete SVG document."""
        try:
            # Create SVG document
            svg_parts = [
                f'<svg width="{canvas_size.width}" height="{canvas_size.height}" '
                f'viewBox="0 0 {canvas_size.width} {canvas_size.height}" '
                f'xmlns="http://www.w3.org/2000/svg">'
            ]

            # Sort commands by z-index
            sorted_commands = sorted(
                commands, key=lambda c: c.properties.get("z_index", 0)
            )

            # Process each command
            for command in sorted_commands:
                if command.render_type == "svg":
                    svg_element = self._command_to_svg_element(command)
                    if svg_element:
                        svg_parts.append(svg_element)
                elif command.render_type == "error":
                    error_element = self._create_error_svg_element(command)
                    svg_parts.append(error_element)

            svg_parts.append("</svg>")

            final_svg = "\n".join(svg_parts)
            logger.info(f"Generated SVG with {len(sorted_commands)} elements")
            return final_svg

        except Exception as e:
            logger.error(f"Failed to render to SVG: {e}")
            return f'<svg><text x="10" y="20">Render Error: {e}</text></svg>'

    def render_to_html_canvas(
        self, commands: list[RenderCommand], canvas_size: Size
    ) -> str:
        """Render commands to HTML5 Canvas JavaScript code."""
        try:
            js_parts = [
                f"// Canvas size: {canvas_size.width}x{canvas_size.height}",
                "const canvas = document.getElementById('pictograph-canvas');",
                "const ctx = canvas.getContext('2d');",
                f"canvas.width = {canvas_size.width};",
                f"canvas.height = {canvas_size.height};",
                "ctx.clearRect(0, 0, canvas.width, canvas.height);",
            ]

            # Sort by z-index
            sorted_commands = sorted(
                commands, key=lambda c: c.properties.get("z_index", 0)
            )

            for command in sorted_commands:
                js_code = self._command_to_canvas_js(command)
                if js_code:
                    js_parts.append(js_code)

            return "\n".join(js_parts)

        except Exception as e:
            logger.error(f"Failed to render to Canvas JS: {e}")
            return f"console.error('Render Error: {e}');"

    def _command_to_svg_element(self, command: RenderCommand) -> Optional[str]:
        """Convert render command to SVG element."""
        try:
            svg_content = command.properties.get("svg_content", "")
            if not svg_content:
                return None

            # Extract inner content (remove outer svg tag if present)
            inner_content = self._extract_svg_inner_content(svg_content)

            # Wrap in group with transform
            return (
                f'<g transform="translate({command.position.x},{command.position.y}) '
                f'scale({command.size.width / 100},{command.size.height / 100})">'
                f"{inner_content}"
                f"</g>"
            )

        except Exception as e:
            logger.error(f"Failed to convert command to SVG: {e}")
            return None

    def _create_error_svg_element(self, command: RenderCommand) -> str:
        """Create error SVG element."""
        return (
            f'<rect x="{command.position.x}" y="{command.position.y}" '
            f'width="{command.size.width}" height="{command.size.height}" '
            f'fill="red" fill-opacity="0.3" stroke="red" stroke-width="2"/>'
        )

    def _command_to_canvas_js(self, command: RenderCommand) -> Optional[str]:
        """Convert render command to Canvas JavaScript."""
        try:
            if command.render_type == "error":
                return (
                    f"ctx.fillStyle = 'rgba(255, 0, 0, 0.3)';\n"
                    f"ctx.fillRect({command.position.x}, {command.position.y}, "
                    f"{command.size.width}, {command.size.height});"
                )

            # For SVG content, we'd need to parse and convert to Canvas operations
            # This is complex, so for this example we'll create a placeholder
            return (
                f"// SVG content at ({command.position.x}, {command.position.y})\n"
                f"ctx.strokeRect({command.position.x}, {command.position.y}, "
                f"{command.size.width}, {command.size.height});"
            )

        except Exception as e:
            logger.error(f"Failed to convert command to Canvas JS: {e}")
            return None

    def _extract_svg_inner_content(self, svg_content: str) -> str:
        """Extract inner content from SVG."""
        try:
            # Simple extraction - remove outer <svg> tags
            start_tag_end = svg_content.find(">")
            end_tag_start = svg_content.rfind("</svg>")

            if start_tag_end != -1 and end_tag_start != -1:
                return svg_content[start_tag_end + 1 : end_tag_start].strip()
            else:
                return svg_content  # Return as-is if parsing fails

        except Exception:
            return svg_content


# ============================================================================
# WEB PICTOGRAPH SERVICE
# ============================================================================


class WebPictographService:
    """
    Web service for pictograph rendering using the framework-agnostic core.

    This demonstrates how the same business logic used in the QT desktop app
    can be used in web services without any QT dependencies.
    """

    def __init__(self, assets_base_url: str = "/static/assets/"):
        """Initialize web pictograph service."""
        self.asset_provider = WebAssetProvider(assets_base_url)
        self.core_renderer = CorePictographRenderer(self.asset_provider)
        self.web_engine = WebRenderEngine()

        logger.info("Web pictograph service initialized")

    def render_pictograph_svg(
        self,
        pictograph_data: dict,
        width: int = 400,
        height: int = 400,
        options: Optional[dict] = None,
    ) -> str:
        """
        Render pictograph as SVG for web display.

        Args:
            pictograph_data: Pictograph data dictionary
            width: Output width in pixels
            height: Output height in pixels
            options: Rendering options

        Returns:
            Complete SVG document as string
        """
        try:
            canvas_size = Size(width, height)

            # Use the same core logic as desktop app
            commands = self.core_renderer.create_render_commands(
                pictograph_data, canvas_size, options
            )

            # Render to SVG for web
            svg_document = self.web_engine.render_to_svg(commands, canvas_size)

            logger.info(f"Rendered pictograph SVG: {len(commands)} elements")
            return svg_document

        except Exception as e:
            logger.error(f"Failed to render pictograph SVG: {e}")
            return f'<svg><text x="10" y="20">Error: {e}</text></svg>'

    def render_pictograph_canvas_js(
        self,
        pictograph_data: dict,
        width: int = 400,
        height: int = 400,
        options: Optional[dict] = None,
    ) -> str:
        """
        Render pictograph as HTML5 Canvas JavaScript.

        Returns JavaScript code that can be executed to draw on a canvas.
        """
        try:
            canvas_size = Size(width, height)

            commands = self.core_renderer.create_render_commands(
                pictograph_data, canvas_size, options
            )

            js_code = self.web_engine.render_to_html_canvas(commands, canvas_size)

            logger.info(f"Generated Canvas JS: {len(commands)} elements")
            return js_code

        except Exception as e:
            logger.error(f"Failed to render Canvas JS: {e}")
            return f"console.error('Render Error: {e}');"

    def create_thumbnail_svg(self, pictograph_data: dict, size: int = 150) -> str:
        """Create small thumbnail SVG for sequence browsing."""
        return self.render_pictograph_svg(
            pictograph_data,
            width=size,
            height=size,
            options={"thumbnail_mode": True, "simplified": True},
        )

    def get_pictograph_metadata(self, pictograph_data: dict) -> dict:
        """Extract metadata from pictograph data."""
        try:
            return {
                "grid_mode": pictograph_data.get("grid_mode", "diamond"),
                "prop_count": len(pictograph_data.get("props", [])),
                "glyph_count": len(pictograph_data.get("glyphs", [])),
                "arrow_count": len(pictograph_data.get("arrows", [])),
                "complexity_score": self._calculate_complexity_score(pictograph_data),
            }
        except Exception as e:
            logger.error(f"Failed to extract metadata: {e}")
            return {"error": str(e)}

    def _calculate_complexity_score(self, pictograph_data: dict) -> int:
        """Calculate complexity score for caching/optimization decisions."""
        score = 0
        score += len(pictograph_data.get("props", [])) * 2
        score += len(pictograph_data.get("glyphs", [])) * 1
        score += len(pictograph_data.get("arrows", [])) * 3

        if pictograph_data.get("grid_mode") == "diamond":
            score += 1  # Diamond grid is slightly more complex

        return score


# ============================================================================
# FASTAPI INTEGRATION EXAMPLE
# ============================================================================


def create_fastapi_pictograph_endpoints():
    """
    Example of how to integrate with FastAPI web framework.

    This shows how the framework-agnostic service can be used in a real web API.
    """

    # This would be in a separate file in a real application
    pictograph_service = WebPictographService()

    # Example endpoint implementations:
    example_endpoints = '''
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from typing import Dict, Optional

    app = FastAPI()
    pictograph_service = WebPictographService()

    class PictographRequest(BaseModel):
        pictograph_data: Dict
        width: Optional[int] = 400
        height: Optional[int] = 400
        format: Optional[str] = "svg"  # "svg" or "canvas_js"
        options: Optional[Dict] = None

    @app.post("/render/pictograph")
    async def render_pictograph(request: PictographRequest):
        """Render pictograph in requested format."""
        try:
            if request.format == "svg":
                result = pictograph_service.render_pictograph_svg(
                    request.pictograph_data,
                    request.width,
                    request.height,
                    request.options
                )
                return {"format": "svg", "content": result}

            elif request.format == "canvas_js":
                result = pictograph_service.render_pictograph_canvas_js(
                    request.pictograph_data,
                    request.width,
                    request.height,
                    request.options
                )
                return {"format": "canvas_js", "content": result}

            else:
                raise HTTPException(status_code=400, detail="Invalid format")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/render/thumbnail")
    async def render_thumbnail(pictograph_data: Dict, size: Optional[int] = 150):
        """Render small thumbnail."""
        try:
            svg_content = pictograph_service.create_thumbnail_svg(pictograph_data, size)
            return {"format": "svg", "content": svg_content}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/analyze/pictograph")
    async def analyze_pictograph(pictograph_data: Dict):
        """Get pictograph metadata and analysis."""
        try:
            metadata = pictograph_service.get_pictograph_metadata(pictograph_data)
            return metadata
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    '''

    return example_endpoints


# ============================================================================
# EXAMPLE USAGE
# ============================================================================


def demonstrate_web_service():
    """Demonstrate web service usage."""

    # Create service
    web_service = WebPictographService()

    # Example pictograph data (same format as desktop app)
    sample_pictograph = {
        "grid_mode": "diamond",
        "props": [
            {
                "type": "staff",
                "color": "blue",
                "x": 200,
                "y": 200,
                "motion_data": {"rotation": 0},
            }
        ],
        "glyphs": [
            {"type": "letter", "id": "A", "x": 180, "y": 50, "width": 40, "height": 40}
        ],
        "arrows": [
            {
                "type": "motion",
                "start_x": 150,
                "start_y": 150,
                "end_x": 250,
                "end_y": 250,
                "color": "black",
            }
        ],
    }

    # Render as SVG (same business logic as desktop!)
    svg_result = web_service.render_pictograph_svg(sample_pictograph)
    print("Generated SVG:")
    print(svg_result)
    print("\n" + "=" * 50 + "\n")

    # Render as Canvas JS
    canvas_js = web_service.render_pictograph_canvas_js(sample_pictograph)
    print("Generated Canvas JS:")
    print(canvas_js)
    print("\n" + "=" * 50 + "\n")

    # Get metadata
    metadata = web_service.get_pictograph_metadata(sample_pictograph)
    print("Pictograph Metadata:")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    # Run demonstration
    demonstrate_web_service()
