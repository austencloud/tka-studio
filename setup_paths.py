#!/usr/bin/env python3
"""
Simple path setup for TKA project.
Adds only essential directories to Python path for clean imports.
"""

import sys
import os
from pathlib import Path

def setup_tka_paths():
    """Add only the essential paths for TKA imports to work correctly."""
    
    # Get project root (where this file is located)
    project_root = Path(__file__).parent
    
    # Essential directories for clean imports
    essential_paths = [
        # Legacy app structure
        project_root / "src" / "desktop" / "legacy" / "src",
        
        # Add specific core directories to resolve multiple core modules
        project_root / "src" / "desktop" / "legacy" / "src" / "main_window" / "main_widget" / "settings_dialog",
        
        # Modern app structure  
        project_root / "src" / "desktop" / "modern" / "src",
        
        # Shared data and utilities
        project_root / "data",
        project_root / "packages",
        
        # Root level for shared modules
        project_root,
    ]
    
    # Add paths if they exist and aren't already in sys.path
    added_count = 0
    for path in essential_paths:
        if path.exists() and path.is_dir():
            path_str = str(path)
            if path_str not in sys.path:
                sys.path.insert(0, path_str)
                added_count += 1
    
    return added_count

if __name__ == "__main__":
    count = setup_tka_paths()
    print(f"Added {count} essential paths to sys.path")
    for i, path in enumerate(sys.path[:count]):
        print(f"  {i+1}. {path}")
