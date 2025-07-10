#!/usr/bin/env python3
"""
Debug import issues.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src"))

def test_direct_imports():
    """Test importing services directly."""
    print("🧪 Testing direct imports...")
    
    try:
        print("   Testing SequenceManager...")
        from application.services.sequence.sequence_manager import SequenceManager
        print("   ✅ SequenceManager imported successfully")
        
        print("   Testing SequenceOrchestrator...")
        from application.services.sequence.sequence_orchestrator import SequenceOrchestrator
        print("   ✅ SequenceOrchestrator imported successfully")
        
        print("   Testing SequencePersister...")
        from application.services.sequence.sequence_persister import SequencePersister
        print("   ✅ SequencePersister imported successfully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Direct import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_package_imports():
    """Test importing through package __init__.py."""
    print("\n🧪 Testing package imports...")
    
    try:
        print("   Testing sequence package...")
        from application.services.sequence import SequenceManager
        print("   ✅ SequenceManager imported from package")
        
        from application.services.sequence import SequenceOrchestrator
        print("   ✅ SequenceOrchestrator imported from package")
        
        from application.services.sequence import SequencePersister
        print("   ✅ SequencePersister imported from package")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Package import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_services_import():
    """Test importing from main services package."""
    print("\n🧪 Testing main services import...")
    
    try:
        print("   Testing main services package...")
        from application.services import SequenceManager
        print("   ✅ SequenceManager imported from main services")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Main services import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting import debug tests...\n")
    
    tests = [
        test_direct_imports,
        test_package_imports,
        test_main_services_import,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"\n📊 Import Debug Results:")
    print(f"   ✅ Passed: {success_count}/{total_count}")
    print(f"   ❌ Failed: {total_count - success_count}/{total_count}")
    
    sys.exit(0 if success_count == total_count else 1)
