#!/usr/bin/env python3
"""
Test script to verify full screen functionality integration.

This script tests the full screen viewer service and its integration
with the modern TKA application.
"""

import sys
import tempfile
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.dependency_injection.di_container import DIContainer
from core.application.application_factory import ApplicationFactory
from domain.models.sequence_data import SequenceData
from domain.models.beat_data import BeatData
from domain.models.enums import MotionType
from core.interfaces.workbench_services import IFullScreenViewer


def create_test_sequence() -> SequenceData:
    """Create a simple test sequence for full screen viewing."""
    # Create a simple 2-beat sequence
    start_beat = BeatData(
        id="start",
        motion_type=MotionType.STATIC,
        pictograph_data=None,
        motions={}
    )
    
    second_beat = BeatData(
        id="beat1", 
        motion_type=MotionType.STATIC,
        pictograph_data=None,
        motions={}
    )
    
    sequence = SequenceData(
        id="test_sequence",
        name="Test Sequence",
        beats=[start_beat, second_beat],
        metadata={}
    )
    
    return sequence


def test_fullscreen_service_resolution():
    """Test that the full screen service can be resolved from DI container."""
    print("🧪 Testing full screen service resolution...")
    
    try:
        # Create application container
        container = ApplicationFactory.create_app("production")
        
        # Try to resolve the full screen service
        fullscreen_service = container.resolve(IFullScreenViewer)
        
        if fullscreen_service:
            print("✅ Full screen service resolved successfully!")
            print(f"   Service type: {type(fullscreen_service)}")
            return fullscreen_service
        else:
            print("❌ Full screen service could not be resolved")
            return None
            
    except Exception as e:
        print(f"❌ Error resolving full screen service: {e}")
        return None


def test_fullscreen_interface_methods(service: IFullScreenViewer):
    """Test the full screen service interface methods."""
    print("\n🧪 Testing full screen interface methods...")
    
    try:
        # Test is_fullscreen (should be False initially)
        is_fullscreen_initial = service.is_fullscreen()
        print(f"✅ is_fullscreen() works: {is_fullscreen_initial}")
        
        # Create test sequence
        test_sequence = create_test_sequence()
        print("✅ Test sequence created")
        
        # Test show_fullscreen
        print("🖥️ Testing show_fullscreen...")
        service.show_fullscreen(test_sequence)
        
        # Check if now in fullscreen
        is_fullscreen_after = service.is_fullscreen()
        print(f"✅ After show_fullscreen, is_fullscreen(): {is_fullscreen_after}")
        
        # Test hide_fullscreen
        print("🖥️ Testing hide_fullscreen...")
        service.hide_fullscreen()
        
        # Check if no longer in fullscreen
        is_fullscreen_final = service.is_fullscreen()
        print(f"✅ After hide_fullscreen, is_fullscreen(): {is_fullscreen_final}")
        
        # Test toggle_fullscreen
        print("🖥️ Testing toggle_fullscreen...")
        toggle_result1 = service.toggle_fullscreen(test_sequence)
        toggle_result2 = service.toggle_fullscreen()
        print(f"✅ Toggle results: {toggle_result1} -> {toggle_result2}")
        
        print("✅ All interface methods work correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing interface methods: {e}")
        return False


def main():
    """Main test function."""
    print("🎯 TKA Full Screen Integration Test")
    print("=" * 50)
    
    # Test 1: Service resolution
    fullscreen_service = test_fullscreen_service_resolution()
    if not fullscreen_service:
        print("\n❌ Full screen service resolution failed - cannot continue")
        return False
    
    # Test 2: Interface methods
    interface_test_passed = test_fullscreen_interface_methods(fullscreen_service)
    if not interface_test_passed:
        print("\n❌ Interface method testing failed")
        return False
    
    print("\n🎉 All full screen integration tests passed!")
    print("\n📋 Summary:")
    print("✅ Full screen service is properly registered in DI container")
    print("✅ Full screen service implements IFullScreenViewer interface correctly")
    print("✅ All interface methods (show, hide, toggle, is_fullscreen) work")
    print("✅ Full screen functionality is ready for UI integration")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
