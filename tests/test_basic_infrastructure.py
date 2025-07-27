"""
Simple Infrastructure Test - Quick Validation

Let's test the basic event bus functionality first without complex imports.
"""

import pytest
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_basic_imports():
    """Test that we can import basic modules."""
    from desktop.modern.core.events.event_bus import TypeSafeEventBus
    # Should not raise an exception

def test_event_bus_creation():
    """Test creating an event bus instance."""
    from desktop.modern.core.events.event_bus import TypeSafeEventBus
    bus = TypeSafeEventBus()
    assert bus is not None

def test_domain_events_import():
    """Test importing domain events."""
    from desktop.modern.core.events.domain_events import SequenceUpdatedEvent
    # Should not raise an exception

if __name__ == "__main__":
    print("🧪 Running basic infrastructure tests...")
    
    try:
        test_basic_imports()
        print("✅ Basic imports test passed")
    except Exception as e:
        print(f"❌ Basic imports test failed: {e}")
    
    try:
        test_event_bus_creation()
        print("✅ Event bus creation test passed")
    except Exception as e:
        print(f"❌ Event bus creation test failed: {e}")
    
    try:
        test_domain_events_import()
        print("✅ Domain events import test passed")
    except Exception as e:
        print(f"❌ Domain events import test failed: {e}")
    
    print("🎉 Basic infrastructure tests completed!")
