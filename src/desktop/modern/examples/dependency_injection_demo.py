"""
Demonstration of the refactored pictograph services with dependency injection.

This script shows how the services can now be used with different implementations
and how they're much more testable and flexible.
"""

import sys
from pathlib import Path
from unittest.mock import Mock
import pandas as pd

# Add src to path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from application.services.pictograph.pictograph_position_matcher import PictographPositionMatcher
from application.services.pictograph.pictograph_validator import PictographValidator
from application.services.pictograph.visibility_state_manager import VisibilityStateManager
from application.services.pictograph.arrow_rendering_service import ArrowRenderingService


def demo_position_matcher_flexibility():
    """Demonstrate how PictographPositionMatcher can use different data sources."""
    print("🎯 PictographPositionMatcher Flexibility Demo")
    print("-" * 45)
    
    # Create a mock CSV manager with test data
    mock_csv_manager = Mock()
    test_data = pd.DataFrame({
        'start_pos': ['alpha1', 'alpha1', 'beta2', 'gamma3'],
        'letter': ['A', 'B', 'C', 'D'],
        'motion_type': ['pro', 'anti', 'pro', 'static'],
        'end_pos': ['beta2', 'gamma3', 'alpha1', 'beta2']
    })
    mock_csv_manager._load_csv_data.return_value = test_data
    
    # Create matcher with injected dependency
    matcher = PictographPositionMatcher(csv_manager=mock_csv_manager)
    
    print(f"✅ Created matcher with mock CSV manager")
    print(f"📊 Dataset groups: {list(matcher.pictograph_dataset.keys())}")
    print(f"🔍 Alpha1 options: {len(matcher.pictograph_dataset.get('alpha1', []))}")
    
    # Demonstrate that we can easily swap data sources
    print("\n🔄 Swapping to different data source...")
    
    different_csv_manager = Mock()
    different_data = pd.DataFrame({
        'start_pos': ['beta2', 'beta2'],
        'letter': ['X', 'Y'],
        'motion_type': ['float', 'dash']
    })
    different_csv_manager._load_csv_data.return_value = different_data
    
    different_matcher = PictographPositionMatcher(csv_manager=different_csv_manager)
    print(f"📊 New dataset groups: {list(different_matcher.pictograph_dataset.keys())}")
    
    print("✨ This flexibility makes testing and configuration much easier!\n")


def demo_validator_testability():
    """Demonstrate how PictographValidator can be tested with mocked dependencies."""
    print("🧪 PictographValidator Testability Demo")
    print("-" * 42)
    
    # Create mock pictograph data
    mock_pictograph = Mock()
    mock_pictograph.letter = "A"
    
    # Create mock orientation calculator
    mock_orientation_calc = Mock()
    mock_orientation_calc.calculate_end_orientation.return_value = "OUT"
    
    # Create validator with injected dependencies
    validator = PictographValidator(
        pictograph_data=mock_pictograph,
        orientation_calculator=mock_orientation_calc
    )
    
    print("✅ Created validator with mocked dependencies")
    print(f"📝 Pictograph letter: {validator.pictograph_data.letter}")
    print(f"🧮 Has orientation calculator: {validator.orientation_calculator is not None}")
    
    # Demonstrate that we can control the behavior for testing
    mock_motion = Mock()
    result = validator._get_arrow_end_orientation(mock_motion)
    
    print(f"🎯 Orientation calculation result: {result}")
    print(f"📞 Calculator was called: {mock_orientation_calc.calculate_end_orientation.called}")
    
    print("✨ Perfect for unit testing - we control all dependencies!\n")


def demo_visibility_manager_configuration():
    """Demonstrate how VisibilityStateManager can be configured with different services."""
    print("⚙️ VisibilityStateManager Configuration Demo")
    print("-" * 48)
    
    # Create mock services
    mock_visibility_service = Mock()
    mock_global_service = Mock()
    
    # Create manager with injected dependencies
    manager = VisibilityStateManager(
        visibility_service=mock_visibility_service,
        global_visibility_service=mock_global_service
    )
    
    print("✅ Created manager with injected services")
    print(f"🔧 Visibility service type: {type(manager.visibility_service).__name__}")
    print(f"🌐 Global service type: {type(manager._global_service).__name__}")
    
    # Demonstrate observer pattern still works
    callback_called = False
    def test_callback():
        nonlocal callback_called
        callback_called = True
    
    manager.register_observer(test_callback, ["glyph"])
    print(f"👀 Registered observer: {len(manager._observers['glyph'])} observers")
    
    print("✨ Services can be swapped without breaking functionality!\n")


def demo_arrow_service_asset_management():
    """Demonstrate how ArrowRenderingService can use different asset managers."""
    print("🎨 ArrowRenderingService Asset Management Demo")
    print("-" * 50)
    
    # Create mock asset manager
    mock_asset_manager = Mock()
    mock_asset_manager.get_arrow_svg_path.return_value = "/mock/path/arrow.svg"
    
    # Create service with injected dependency
    service = ArrowRenderingService(asset_manager=mock_asset_manager)
    
    print("✅ Created service with mock asset manager")
    print(f"📁 Asset manager type: {type(service.asset_manager).__name__}")
    
    # Demonstrate asset retrieval
    mock_motion = Mock()
    svg_path = service.get_arrow_svg_path(mock_motion, "blue")
    
    print(f"🎯 Retrieved SVG path: {svg_path}")
    print(f"📞 Asset manager was called: {mock_asset_manager.get_arrow_svg_path.called}")
    
    print("✨ Easy to test with different asset sources!\n")


def demo_before_and_after():
    """Show the difference between old hard-coded and new flexible approach."""
    print("🔄 Before vs After Comparison")
    print("-" * 30)
    
    print("❌ BEFORE (Hard-coded dependencies):")
    print("   class PictographPositionMatcher:")
    print("       def __init__(self):")
    print("           self.csv_manager = PictographCSVManager()  # HARD-CODED!")
    print("   # ❌ Can't test in isolation")
    print("   # ❌ Can't swap implementations")
    print("   # ❌ Always uses real CSV files")
    
    print("\n✅ AFTER (Dependency injection):")
    print("   class PictographPositionMatcher:")
    print("       def __init__(self, csv_manager=None):")
    print("           self.csv_manager = csv_manager or PictographCSVManager()")
    print("   # ✅ Can inject mocks for testing")
    print("   # ✅ Can swap implementations easily")
    print("   # ✅ Flexible and configurable")
    
    print("\n🎉 The refactoring makes services:")
    print("   • Testable in isolation")
    print("   • Flexible and configurable")
    print("   • Free from circular dependencies")
    print("   • Environment-agnostic")


def main():
    """Run all demonstrations."""
    print("🚀 Dependency Injection Refactoring Demo")
    print("=" * 50)
    print("Demonstrating the benefits of the pictograph services refactoring\n")
    
    try:
        demo_position_matcher_flexibility()
        demo_validator_testability()
        demo_visibility_manager_configuration()
        demo_arrow_service_asset_management()
        demo_before_and_after()
        
        print("\n🎊 Demo completed successfully!")
        print("The dependency injection refactoring provides significant benefits")
        print("for testing, flexibility, and maintainability.")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
