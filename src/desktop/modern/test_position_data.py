"""
Test script to switch to mock service and verify Lesson3 fix
"""

import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_with_mock_service():
    """Test using mock service to verify position data."""
    try:
        from application.services.learn.mock_pictograph_data_service import MockPictographDataService
        
        print("Testing Mock Pictograph Data Service")
        print("-" * 50)
        
        # Create mock service
        mock_service = MockPictographDataService()
        
        # Get dataset
        dataset = mock_service.get_pictograph_dataset()
        print(f"Dataset has {len(dataset)} letters")
        
        # Test letter A
        letter_a = dataset.get("A", [])
        print(f"Letter A has {len(letter_a)} pictographs")
        
        if letter_a:
            sample = letter_a[0]
            print(f"First pictograph keys: {list(sample.keys())}")
            
            # Check position data
            has_start = "start_pos" in sample
            has_end = "end_pos" in sample
            print(f"Has start_pos: {has_start}")
            print(f"Has end_pos: {has_end}")
            
            if has_start and has_end:
                print(f"Positions: start={sample['start_pos']}, end={sample['end_pos']}")
                
                # Count same position pictographs (needed for Lesson3 initial)
                same_pos = sum(1 for p in letter_a if p.get('start_pos') == p.get('end_pos'))
                print(f"Same position pictographs: {same_pos}")
                
                # Check unique positions (needed for answer variety)
                start_positions = set(p.get('start_pos') for p in letter_a)
                end_positions = set(p.get('end_pos') for p in letter_a)
                print(f"Unique start positions: {sorted(start_positions)}")
                print(f"Unique end positions: {sorted(end_positions)}")
                
                if same_pos > 0 and len(start_positions) >= 4:
                    print("✅ SUCCESS: Mock service has proper position data for Lesson3!")
                    return True
                else:
                    print(f"❌ ISSUE: Not enough variety (same_pos={same_pos}, positions={len(start_positions)})")
                    return False
            else:
                print("❌ Missing position data")
                return False
        else:
            print("❌ No data for letter A")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Lesson3 Position Data Fix")
    print("=" * 50)
    
    success = test_with_mock_service()
    
    if success:
        print("\n🎉 Position data fix appears to be working!")
        print("The mock service now provides:")
        print("- Pictographs with start_pos and end_pos data")
        print("- Some pictographs where start_pos == end_pos (for initial question)")
        print("- Multiple different start positions (for answer options)")
        print("- This should fix the Lesson3 issue with only 1 answer option")
    else:
        print("\n❌ Position data fix needs more work")
    
    print(f"\nResult: {'PASS' if success else 'FAIL'}")
