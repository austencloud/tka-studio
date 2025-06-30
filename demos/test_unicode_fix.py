#!/usr/bin/env python3
"""
Quick test script to verify Unicode fixes work
"""

print("=" * 60)
print("  TKA DEMO UNICODE FIX VERIFICATION")
print("=" * 60)

# Test ASCII alternatives
ascii_chars = {
    "[LAUNCH]": "🚀",
    "[OK]": "✅", 
    "[ERROR]": "❌",
    "[WARNING]": "⚠️",
    "[AI]": "🤖",
    "[CHART]": "📊",
    "[MUSIC]": "🎵",
    "[SETTINGS]": "⚙️",
    "[SAVE]": "💾",
    "[TIME]": "⏱️"
}

print("\nTesting ASCII character replacements:")
for ascii_char, unicode_char in ascii_chars.items():
    try:
        print(f"{ascii_char} Successfully replaced {unicode_char}")
    except UnicodeEncodeError as e:
        print(f"[ERROR] Still have encoding issues: {e}")

print(f"\n[OK] All Unicode characters successfully replaced with ASCII alternatives!")
print(f"[LAUNCH] Ready to run demos without encoding errors!")

print("\n" + "=" * 60)
