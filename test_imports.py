#!/usr/bin/env python3
"""Test script to validate the service import reorganization."""

import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src" / "desktop" / "modern" / "src"
sys.path.insert(0, str(src_path))


def test_imports():
    """Test that all new import paths work correctly."""
    try:
        print("🔧 Testing new service import paths...")

        # Test sequence services
        from application.services.sequences.sequence_persistence_service import (
            SequencePersistenceService,
        )

        print("✅ SequencePersistenceService import OK")

        from application.services.sequences.sequence_loading_service import (
            SequenceLoadingService,
        )

        print("✅ SequenceLoadingService import OK")

        # Test pictograph services
        from application.services.pictographs.pictograph_management_service import (
            PictographManagementService,
        )

        print("✅ PictographManagementService import OK")

        from application.services.pictographs.application_orchestrator import (
            ApplicationOrchestrator,
        )

        print("✅ ApplicationOrchestrator import OK")

        # Test glyph services
        from application.services.glyphs.glyph_data_service import GlyphDataService

        print("✅ GlyphDataService import OK")

        # Test graph editor services
        from application.services.graph_editor.graph_editor_service import (
            GraphEditorService,
        )

        print("✅ GraphEditorService import OK")

        print("\n🎉 All new import paths work correctly!")
        print("✅ Service directory reorganization is successful!")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

    return True


if __name__ == "__main__":
    test_imports()
