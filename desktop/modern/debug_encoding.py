#!/usr/bin/env python3
import sys
import locale
import os

print('Python version:', sys.version)
print('stdout encoding:', sys.stdout.encoding)
print('stderr encoding:', sys.stderr.encoding)
print('filesystem encoding:', sys.getfilesystemencoding())
print('preferred encoding:', locale.getpreferredencoding())
print('PYTHONIOENCODING:', os.environ.get('PYTHONIOENCODING', 'Not set'))

# Test emoji printing
try:
    print('Testing emoji: 🔧 ✅ ❌')
    print('Emoji test successful!')
except UnicodeEncodeError as e:
    print(f'Emoji test failed: {e}')
    print('Trying to reconfigure stdout...')
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        print('Testing emoji after reconfigure: 🔧 ✅ ❌')
        print('Reconfigure successful!')
    except Exception as e2:
        print(f'Reconfigure failed: {e2}')