#!/usr/bin/env python3
"""
Debug launcher that ensures proper virtual environment usage
This fallback script forces the correct paths and environment setup
"""
import sys
import os
from pathlib import Path

def setup_debug_environment():
    """Set up the environment to use virtual environment packages exclusively"""
    # Get project root directory
    project_root = Path(__file__).parent.absolute()
    venv_path = project_root / ".venv"
    site_packages = venv_path / "Lib" / "site-packages"
    
    print("🔧 Debug Environment Setup")
    print("=" * 50)
    print(f"Project Root: {project_root}")
    print(f"Virtual Env: {venv_path}")
    print(f"Site Packages: {site_packages}")
    
    # Verify virtual environment exists
    if not venv_path.exists():
        print("❌ Virtual environment not found!")
        print("Run: py -3.12 -m venv .venv")
        sys.exit(1)
    
    if not site_packages.exists():
        print("❌ Site packages directory not found!")
        print("Run: .venv\\Scripts\\activate && pip install -r requirements.txt")
        sys.exit(1)
    
    # Keep the standard library paths but prioritize our virtual environment
    original_path = sys.path.copy()
    
    # Identify and preserve Python standard library paths
    stdlib_paths = []
    for path in original_path:
        path_obj = Path(path)
        # Keep standard library paths (typically contain python.exe parent or DLLs)
        if (path_obj.name in ['DLLs', 'lib', 'libs'] or 
            'python' in path.lower() and 'site-packages' not in path.lower() or
            path == ''):
            stdlib_paths.append(path)
    
    # Clear and rebuild with proper order
    sys.path.clear()
    
    # Add our project paths first (highest priority)
    project_paths = [
        str(project_root),                              # Project root
        str(project_root / "src"),                      # Source code
        str(project_root / "launcher"),                 # Launcher module
        str(project_root / "packages"),                 # Local packages
        str(project_root / "packages" / "shared-types" / "python"),
        str(project_root / "packages" / "constants" / "python"),
        str(project_root / "data"),                     # Data directory
    ]
    
    # Add virtual environment packages
    venv_paths = [str(site_packages)]
    
    # Combine in proper order: project -> venv -> stdlib
    for path in project_paths:
        if Path(path).exists():
            sys.path.append(path)
    
    for path in venv_paths:
        if Path(path).exists():
            sys.path.append(path)
    
    # Add standard library paths last
    sys.path.extend(stdlib_paths)
    
    # Set environment variables to force virtual env usage
    all_paths = project_paths + venv_paths + stdlib_paths
    os.environ["PYTHONPATH"] = ";".join(all_paths)
    os.environ["VIRTUAL_ENV"] = str(venv_path)
    # Don't set PYTHONHOME as it can break standard library access
    
    print("✅ Environment configured!")
    print(f"Python executable: {sys.executable}")
    print(f"Python paths ({len(sys.path)}):")
    for i, path in enumerate(sys.path[:8]):  # Show first 8 paths
        print(f"  {i+1}. {path}")
    if len(sys.path) > 8:
        print(f"  ... and {len(sys.path) - 8} more")
    print("=" * 50)

def main():
    """Main debug launcher function"""
    setup_debug_environment()
    
    try:
        # Import and run the main launcher
        print("🚀 Starting TKA Launcher...")
        
        # Try different import strategies
        import_attempts = [
            ("launcher.main", "main"),
            ("main", "main"),
            ("launcher", "main"),
        ]
        
        main_func = None
        for module_name, func_name in import_attempts:
            try:
                module = __import__(module_name, fromlist=[func_name])
                main_func = getattr(module, func_name, None)
                if main_func:
                    print(f"✅ Successfully imported {module_name}.{func_name}")
                    break
            except ImportError as e:
                print(f"⚠️  Failed to import {module_name}: {e}")
                continue
        
        if main_func:
            main_func()
        else:
            print("❌ Could not import main function!")
            print("Available modules in sys.modules:")
            for mod in sorted(sys.modules.keys()):
                if 'launcher' in mod or 'tka' in mod:
                    print(f"  - {mod}")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print(f"Python path: {sys.path}")
        print(f"Current working directory: {os.getcwd()}")
        print("\nTrying to diagnose the issue...")
        
        # Diagnostic information
        launcher_path = Path("launcher")
        if launcher_path.exists():
            print(f"✅ Launcher directory exists")
            main_py = launcher_path / "main.py"
            if main_py.exists():
                print(f"✅ launcher/main.py exists")
            else:
                print(f"❌ launcher/main.py not found")
        else:
            print(f"❌ Launcher directory not found")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
