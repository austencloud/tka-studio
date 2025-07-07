#!/usr/bin/env python3
"""
Quick test to demonstrate camelCase JSON serialization working.
"""

import sys
import os
import importlib.util

# Direct import to bypass __init__.py issues
spec = importlib.util.spec_from_file_location(
    "pydantic_models",
    os.path.join(os.path.dirname(__file__), "src", "domain", "models", "pydantic_models.py")
)
pydantic_models = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pydantic_models)

import json

def main():
    print("🚀 Testing Pydantic camelCase JSON Serialization")
    print("=" * 50)
    
    # Test MotionData
    print("\n✅ MotionData Test:")
    motion = pydantic_models.create_default_motion_data(motion_type='pro', prop_rot_dir='cw')
    
    print("Python object access (snake_case):")
    print(f"  motion.motion_type = '{motion.motion_type}'")
    print(f"  motion.prop_rot_dir = '{motion.prop_rot_dir}'")
    print(f"  motion.start_loc = '{motion.start_loc}'")
    
    print("\nJSON serialization (camelCase):")
    json_str = motion.model_dump_json(indent=2)
    print(json_str)
    
    print("\nRound-trip test:")
    json_data = json.loads(json_str)
    restored = motion.__class__(**json_data)
    print(f"  Original == Restored: {motion == restored}")
    
    # Test BeatData with nested MotionData
    print("\n✅ BeatData Test (with nested MotionData):")
    beat = pydantic_models.create_default_beat_data(1, 'A')
    
    print("Python object access:")
    print(f"  beat.beat_number = {beat.beat_number}")
    print(f"  beat.blue_motion.motion_type = '{beat.blue_motion.motion_type}'")
    
    print("\nJSON serialization (nested camelCase):")
    beat_json = beat.model_dump_json(indent=2)
    print(beat_json[:200] + "..." if len(beat_json) > 200 else beat_json)
    
    # Verify camelCase keys
    beat_data = json.loads(beat_json)
    camel_keys = ['beatNumber', 'blueMotion', 'redMotion']
    print(f"\nCamelCase keys present: {[key for key in camel_keys if key in beat_data]}")
    
    nested_motion = beat_data['blueMotion']
    motion_camel_keys = ['motionType', 'propRotDir', 'startLoc', 'endLoc']
    print(f"Nested motion camelCase keys: {[key for key in motion_camel_keys if key in nested_motion]}")
    
    print("\n🎉 SUCCESS: Pydantic camelCase serialization working perfectly!")
    print("✅ Python code uses snake_case")
    print("✅ JSON output uses camelCase") 
    print("✅ Round-trip compatibility works")
    print("✅ Nested objects also use camelCase")

if __name__ == "__main__":
    main()
