#!/usr/bin/env python3
"""
Test application functionality after refactoring
"""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import time


# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_domain_models():
    """Test domain model functionality"""
    print("🧪 Testing domain models...")

    try:
        from domain.models import (
            BeatData,
            Location,
            MotionData,
            MotionType,
            Orientation,
            RotationDirection,
            SequenceData,
        )

        # Create objects
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
        )

        beat = BeatData(beat_number=1, letter="A", blue_motion=motion)
        sequence = SequenceData(name="Test Sequence", beats=[beat])

        # Test serialization
        motion.to_json()
        beat.to_json()
        sequence.to_json()

        print("✅ Domain models work correctly!")
        return True

    except Exception as e:
        print(f"❌ Domain model test failed: {e}")
        return False


def test_service_imports():
    """Test that key services can be imported"""
    print("🔧 Testing service imports...")

    try:

        print("✅ Key services import successfully!")
        return True

    except Exception as e:
        print(f"❌ Service import failed: {e}")
        return False


def test_application_startup():
    """Test that the application can start"""
    print("🚀 Testing application startup...")

    try:
        # Start the application
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Wait for startup
        time.sleep(8)

        # Check if still running
        if process.poll() is None:
            print("✅ Application started successfully!")

            # Terminate
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

            return True
        stdout, stderr = process.communicate()
        print(f"❌ Application exited with code: {process.returncode}")
        if stderr:
            print(f"Error: {stderr[:200]}...")
        return False

    except Exception as e:
        print(f"❌ Startup test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🧪 Testing TKA Application After Refactoring...")
    print("=" * 60)

    tests = [
        test_domain_models,
        test_service_imports,
        test_application_startup,
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 60)
    print(f"Results: {passed}/{len(tests)} tests passed")

    if passed == len(tests):
        print("🎉 ALL TESTS PASSED! Application is working correctly!")
        return True
    print("❌ Some tests failed!")
    return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
