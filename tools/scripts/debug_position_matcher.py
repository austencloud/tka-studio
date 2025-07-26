#!/usr/bin/env python3
"""
Debug script to test the position matcher directly and see why it's not finding alpha1 options.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_position_matcher():
    """Test the position matcher directly to see what's happening."""
    print("🔍 Testing PictographPositionMatcher directly...")
    
    try:
        from shared.application.services.positioning.arrows.utilities.pictograph_position_matcher import PictographPositionMatcher
        
        # Create position matcher
        matcher = PictographPositionMatcher()
        
        # Check if dataset loaded
        if not matcher.pictograph_dataset:
            print("❌ Dataset is empty or not loaded")
            return
        
        print(f"✅ Dataset loaded with {len(matcher.pictograph_dataset)} groups")
        
        # Count total pictographs
        total_pictographs = sum(len(group) for group in matcher.pictograph_dataset.values())
        print(f"📊 Total pictographs in dataset: {total_pictographs}")
        
        # Test alpha1 lookup
        print("\n🎯 Testing alpha1 lookup...")
        alpha1_options = matcher.get_next_options("alpha1")
        
        print(f"📋 Found {len(alpha1_options)} options for alpha1")
        
        if alpha1_options:
            print("✅ Alpha1 options found:")
            for i, option in enumerate(alpha1_options[:5]):  # Show first 5
                print(f"  {i+1}. Letter: {option.letter}, Start: {option.start_position}, End: {option.end_position}")
        else:
            print("❌ No alpha1 options found")
            
            # Debug: Check what start positions exist
            print("\n🔍 Debugging: Checking what start positions exist in dataset...")
            start_positions = set()
            for group_key, group in matcher.pictograph_dataset.items():
                for item in group:
                    start_pos = item.get("start_pos")
                    if start_pos:
                        start_positions.add(start_pos)
            
            print(f"📊 Found {len(start_positions)} unique start positions:")
            sorted_positions = sorted(start_positions)
            for pos in sorted_positions[:20]:  # Show first 20
                print(f"  - {pos}")
            
            if "alpha1" in start_positions:
                print("✅ alpha1 IS in the dataset")
                
                # Find examples
                print("\n🔍 Finding alpha1 examples...")
                count = 0
                for group_key, group in matcher.pictograph_dataset.items():
                    for item in group:
                        if item.get("start_pos") == "alpha1":
                            count += 1
                            if count <= 3:
                                print(f"  Example {count}: Letter={item.get('letter')}, Start={item.get('start_pos')}, End={item.get('end_pos')}")
                
                print(f"📊 Total alpha1 entries found: {count}")
            else:
                print("❌ alpha1 is NOT in the dataset")
        
    except Exception as e:
        print(f"❌ Error testing position matcher: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_position_matcher()
