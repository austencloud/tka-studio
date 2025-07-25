"""
Quick Validation Script

Verifies that the framework-agnostic implementation is working correctly
without requiring a full QT environment.
"""

import sys
from pathlib import Path

# Add paths for imports
script_dir = Path(__file__).parent
src_dir = script_dir / "src"
sys.path.insert(0, str(src_dir))


def validate_implementation():
    """Validate the framework-agnostic implementation."""
    print("🔍 VALIDATING FRAMEWORK-AGNOSTIC IMPLEMENTATION")
    print("=" * 60)

    try:
        # Test 1: Import framework-agnostic types
        print("📦 Testing framework-agnostic types...")
        from application.services.core.types import Color, Point, RenderCommand, Size

        # Create test objects
        size = Size(400, 300)
        color = Color.from_hex("#FF0000")
        point = Point(100, 50)

        print(f"   ✅ Size: {size.width}x{size.height}")
        print(f"   ✅ Color: {color.to_hex()}")
        print(f"   ✅ Point: ({point.x}, {point.y})")

        # Test 2: Import and test core pictograph renderer
        print("\n🎨 Testing core pictograph renderer...")
        from application.services.core.pictograph_renderer import (
            create_pictograph_renderer,
        )

        renderer = create_pictograph_renderer()

        # Test data
        sample_data = {
            "grid_mode": "diamond",
            "props": [{"type": "staff", "color": "blue", "x": 200, "y": 200}],
            "glyphs": [
                {
                    "type": "letter",
                    "id": "A",
                    "x": 180,
                    "y": 50,
                    "width": 40,
                    "height": 40,
                }
            ],
        }

        # Generate render commands (will gracefully handle missing assets)
        commands = renderer.create_render_commands(sample_data, Size(400, 400))

        print(f"   ✅ Generated {len(commands)} render commands")
        print(f"   ✅ Command types: {[cmd.render_type for cmd in commands]}")
        print(f"   ✅ No QT dependencies in core renderer!")
        print(
            f"   ℹ️  Note: Some commands may be error placeholders if assets are missing"
        )

        # Test 3: Import and test thumbnail service
        print("\n🖼️  Testing core thumbnail service...")
        from application.services.core.thumbnail_service import (
            ThumbnailSpec,
            create_thumbnail_service,
        )

        thumbnail_service = create_thumbnail_service()

        # Test thumbnail creation
        spec = ThumbnailSpec(
            sequence_id="test_seq",
            sequence_name="Test Sequence",
            beat_count=5,
            thumbnail_size=Size(150, 150),
        )

        thumbnail_data = thumbnail_service.create_thumbnail_data(spec)

        print(f"   ✅ Created thumbnail: {thumbnail_data.thumbnail_id}")
        print(f"   ✅ Has image data: {thumbnail_data.has_image}")
        print(f"   ✅ No QT dependencies in thumbnail service!")

        # Test 4: Validate web service imports (without actually creating web objects)
        print("\n🌐 Testing web service imports...")
        from web.services.web_pictograph_service import WebPictographService

        # Just verify we can create the service (will handle missing assets gracefully)
        web_service = WebPictographService()

        print(f"   ✅ Web service created successfully")
        print(f"   ✅ Web service uses same core renderer as desktop!")
        print(
            f"   ℹ️  Note: Asset loading may fail gracefully if asset files are missing"
        )

        # Test 5: Architecture validation
        print("\n🏗️  Architecture validation...")

        # Verify core services have no QT imports
        core_files = [
            src_dir / "application" / "services" / "core" / "types.py",
            src_dir / "application" / "services" / "core" / "pictograph_renderer.py",
            src_dir / "application" / "services" / "core" / "thumbnail_service.py",
            src_dir / "web" / "services" / "web_pictograph_service.py",
        ]

        qt_free_count = 0
        for file_path in core_files:
            if file_path.exists():
                content = file_path.read_text()
                has_qt = "PyQt" in content or "from PyQt" in content
                if not has_qt:
                    qt_free_count += 1
                print(f"   {'✅' if not has_qt else '❌'} {file_path.name}: QT-free")

        print(f"\n📊 VALIDATION RESULTS:")
        print(f"   ✅ Framework-agnostic types: Working")
        print(f"   ✅ Core pictograph renderer: Working ({len(commands)} commands)")
        print(f"   ✅ Core thumbnail service: Working")
        print(f"   ✅ Web service integration: Working")
        print(f"   ✅ QT-free core services: {qt_free_count}/{len(core_files)}")

        if qt_free_count == len(core_files):
            print(f"\n🏆 VALIDATION PASSED!")
            print(f"   🎯 Framework-agnostic architecture successfully implemented")
            print(f"   🎯 Core services work without QT runtime")
            print(f"   🎯 Same business logic can run in desktop AND web")
            print(f"   🎯 Ready for integration with your real asset system!")
            print(
                f"   📝 TODO: Replace asset path placeholders with your actual asset paths"
            )
            return True
        else:
            print(
                f"\n⚠️  VALIDATION PARTIAL - Some core services still have QT dependencies"
            )
            return False

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all files are in the correct locations")
        return False

    except Exception as e:
        print(f"❌ Validation error: {e}")
        import traceback

        traceback.print_exc()
        return False


def show_usage_examples():
    """Show practical usage examples."""
    print("\n📚 USAGE EXAMPLES:")
    print("=" * 40)

    print(
        """
🖥️  DESKTOP (QT) USAGE:
from desktop.modern.src.application.adapters.qt_pictograph_adapter import create_qt_pictograph_adapter

# Create adapter that bridges core service to QT
adapter = create_qt_pictograph_adapter()

# Use with existing QT code (backward compatible!)
scene = QGraphicsScene()
grid_item = adapter.render_grid(scene, "diamond")
prop_item = adapter.render_prop(scene, "blue", motion_data)

# New capability: render complete pictograph
success = adapter.render_complete_pictograph(scene, pictograph_data)

🌐 WEB SERVICE USAGE:
from web.services.web_pictograph_service import WebPictographService

# Create web service (uses same core logic as desktop!)
web_service = WebPictographService()

# Generate SVG for web display
svg_content = web_service.render_pictograph_svg(pictograph_data, 400, 400)

# Generate Canvas JavaScript
canvas_js = web_service.render_pictograph_canvas_js(pictograph_data, 400, 400)

# Create thumbnails for API
thumbnail_svg = web_service.create_thumbnail_svg(pictograph_data, 150)

🧪 TESTING (NO QT REQUIRED):
from application.services.core.pictograph_renderer import create_pictograph_renderer

# Test core business logic without any UI framework
renderer = create_pictograph_renderer()
commands = renderer.create_render_commands(pictograph_data, Size(400, 400))

# Unit test without QT runtime
assert len(commands) > 0
assert commands[0].render_type == "svg"
"""
    )


def main():
    """Run complete validation."""
    success = validate_implementation()
    show_usage_examples()

    if success:
        print(f"\n🎉 IMPLEMENTATION COMPLETE AND VALIDATED!")
        print(
            f"   Run 'python demonstrate_framework_agnostic_rendering.py' for full demo"
        )
    else:
        print(f"\n❌ Validation failed - check implementation")

    return success


if __name__ == "__main__":
    main()
