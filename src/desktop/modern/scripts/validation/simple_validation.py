"""
Simple service validation test
"""
import sys
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

print("Testing basic imports...")

try:
    from core.interfaces.start_position_services import IStartPositionDataService
    print("✅ Interface import successful")
    
    from application.services.start_position.start_position_data_service import StartPositionDataService
    print("✅ Service import successful")
    
    service = StartPositionDataService()
    print("✅ Service instantiation successful")
    
    print("🎉 Basic validation passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
