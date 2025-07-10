#!/usr/bin/env python3
"""
Legacy TKA Application Launcher

Launches the legacy TKA application with proper core import resolution.
Run this from the TKA project root directory.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Install core import hook
import core_import_hook

# Add legacy app source to path
legacy_src = project_root / 'src' / 'desktop' / 'legacy' / 'src'
sys.path.insert(0, str(legacy_src))

# Now launch the legacy app
if __name__ == "__main__":
    print("🚀 Starting Legacy TKA Application with Core Import Hook...")
    print(f"📁 Project Root: {project_root}")
    print(f"📁 Legacy Source: {legacy_src}")
    
    # Import and run the legacy main
    try:
        sys.path.insert(0, str(project_root / 'src' / 'desktop' / 'legacy'))
        from main import main
        print("✅ Legacy application imported successfully")
        sys.exit(main())
    except Exception as e:
        print(f"❌ Error launching legacy application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
