#!/usr/bin/env python3
"""
Test the updated mock service to verify PictographData creation is working
"""

import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_mock_service_pictograph_data():
    """Test that the mock service creates proper PictographData objects."""
    print("🧪 Testing Updated Mock Service")
    print("=" * 50)
    
    try:
        from application.services.learn.mock_pictograph_data_service import MockPictographDataService
        from domain.models.pictograph_data import PictographData
        
        # Create service
        mock_service = MockPictographDataService()
        
        # Get dataset
        dataset = mock_service.get_pictograph_dataset()
        print(f"✅ Dataset loaded with {len(dataset)} letters")
        
        # Test a specific letter
        letter_a_data = dataset.get("A", [])
        print(f"✅ Letter 'A' has {len(letter_a_data)} pictographs")
        
        if letter_a_data:
            sample = letter_a_data[0]
            print(f"✅ Sample pictograph keys: {list(sample.keys())}")
            
            # Check position data (for legacy compatibility)
            has_start_pos = "start_pos" in sample
            has_end_pos = "end_pos" in sample
            print(f"✅ Has start_pos: {has_start_pos} - Value: {sample.get('start_pos', 'MISSING')}")
            print(f"✅ Has end_pos: {has_end_pos} - Value: {sample.get('end_pos', 'MISSING')}")
            
            # Check PictographData object (for modern rendering)
            has_data = "data" in sample
            print(f"✅ Has data key: {has_data}")
            
            if has_data:
                data_obj = sample["data"]
                is_pictograph_data = isinstance(data_obj, PictographData)
                print(f"✅ Data is PictographData: {is_pictograph_data}")
                
                if is_pictograph_data:
                    print(f"   - ID: {data_obj.id}")
                    print(f"   - Letter: {data_obj.letter}")
                    print(f"   - Start Position: {data_obj.start_position}")
                    print(f"   - End Position: {data_obj.end_position}")
                    print(f"   - Grid Mode: {data_obj.grid_data.grid_mode}")
                    
                    # Check if we have variety for Lesson3
                    same_pos_count = sum(1 for p in letter_a_data 
                                       if p.get('start_pos') == p.get('end_pos'))
                    print(f"✅ Pictographs with start_pos == end_pos: {same_pos_count}")
                    
                    start_positions = set(p.get('start_pos') for p in letter_a_data)
                    print(f"✅ Unique start positions: {sorted(start_positions)}")
                    
                    if same_pos_count > 0 and len(start_positions) >= 4:
                        print("🎉 SUCCESS: Mock service has proper data for Lesson3!")
                        return True
                    else:
                        print(f"❌ ISSUE: Not enough variety for Lesson3")
                        return False
                else:
                    print(f"❌ ISSUE: Data is not PictographData: {type(data_obj)}")
                    return False
            else:
                print("❌ ISSUE: No data key in sample")
                return False
        else:
            print("❌ ISSUE: No data for letter A")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing Updated Mock Service for Lesson3")
    
    success = test_mock_service_pictograph_data()
    
    if success:
        print("\n🎉 Mock service update successful!")
        print("The service now provides:")
        print("- Proper PictographData objects for modern rendering")
        print("- Legacy position data for question generation")
        print("- Variety needed for Lesson3 (initial + 4 answer options)")
        print("\nThis should fix the 'Invalid pictograph data' errors!")
    else:
        print("\n❌ Mock service update needs more work")
    
    print(f"\nResult: {'PASS' if success else 'FAIL'}")
