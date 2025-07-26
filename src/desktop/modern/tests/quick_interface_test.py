"""
Simple test to verify interface implementation
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_interface_imports():
    """Test that interfaces can be imported correctly."""
    try:
        from desktop.modern.core.interfaces.pictograph_services import IPictographValidator, IScalingService
        from desktop.modern.core.interfaces.layout_services import IBeatLayoutCalculator
        from desktop.modern.core.interfaces.workbench_services import IWorkbenchSessionManager
        print("✅ All interfaces imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_implementation_imports():
    """Test that concrete implementations can be imported."""
    try:
        from shared.application.services.pictograph.pictograph_validator import PictographValidator
        from shared.application.services.pictograph.scaling_service import PictographScaler
        from shared.application.services.layout.beat_layout_calculator import BeatLayoutCalculator
        from shared.application.services.workbench.workbench_session_manager import WorkbenchSessionManager
        print("✅ All implementations imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Implementation import error: {e}")
        return False

def test_inheritance():
    """Test that implementations properly inherit from interfaces."""
    try:
        from desktop.modern.core.interfaces.pictograph_services import IPictographValidator, IScalingService
        from desktop.modern.core.interfaces.layout_services import IBeatLayoutCalculator
        from desktop.modern.core.interfaces.workbench_services import IWorkbenchSessionManager
        
        from shared.application.services.pictograph.scaling_service import PictographScaler
        from shared.application.services.layout.beat_layout_calculator import BeatLayoutCalculator
        from shared.application.services.workbench.workbench_session_manager import WorkbenchSessionManager
        
        # Test inheritance
        scaler = PictographScaler()
        assert isinstance(scaler, IScalingService), "PictographScaler should implement IScalingService"
        
        calculator = BeatLayoutCalculator()
        assert isinstance(calculator, IBeatLayoutCalculator), "BeatLayoutCalculator should implement IBeatLayoutCalculator"
        
        session_manager = WorkbenchSessionManager()
        assert isinstance(session_manager, IWorkbenchSessionManager), "WorkbenchSessionManager should implement IWorkbenchSessionManager"
        
        print("✅ All inheritance checks passed")
        return True
    except Exception as e:
        print(f"❌ Inheritance test error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Medium Priority Interface Implementation")
    print("=" * 60)
    
    success = True
    success &= test_interface_imports()
    success &= test_implementation_imports()
    success &= test_inheritance()
    
    print("=" * 60)
    if success:
        print("🎉 All tests passed! Interface implementation successful.")
    else:
        print("💥 Some tests failed. Check the output above.")
    
    sys.exit(0 if success else 1)
