#!/usr/bin/env python3
"""
Minimal test script to verify Python environment.
"""

print("🔥 PYTHON IS WORKING!")
print("🐍 Python version:", __import__('sys').version)
print("📁 Working directory:", __import__('os').getcwd())

try:
    print("🧪 Testing PyQt6...")
    from PyQt6.QtWidgets import QApplication
    print("✅ PyQt6 import successful!")
    
    app = QApplication([])
    print("✅ QApplication created!")
    print("🎯 If you see this, Python + PyQt6 is working!")
    
except Exception as e:
    print(f"❌ PyQt6 test failed: {e}")
    import traceback
    traceback.print_exc()

print("🏁 Test complete!")
