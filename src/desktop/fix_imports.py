#!/usr/bin/env python3
"""
Import Fixer for TKA Desktop Application

This script systematically finds and fixes relative import issues across the entire codebase.
It converts relative imports to absolute imports using the full module path.
"""

import re
from pathlib import Path

class ImportFixer:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.fixed_files = 0
        self.total_changes = 0
        
        # Common import patterns to fix
        self.import_patterns = [
            # from domain.models.xxx import yyy
            (r'from\s+domain\.models\.([a-zA-Z0-9_\.]+)\s+import', 
             r'from desktop.modern.domain.models.\1 import'),
            
            # from application.services.xxx import yyy
            (r'from\s+application\.services\.([a-zA-Z0-9_\.]+)\s+import', 
             r'from desktop.modern.application.services.\1 import'),
             
            # from presentation.components.xxx import yyy
            (r'from\s+presentation\.components\.([a-zA-Z0-9_\.]+)\s+import', 
             r'from desktop.modern.presentation.components.\1 import'),
             
            # from core.xxx import yyy
            (r'from\s+core\.([a-zA-Z0-9_\.]+)\s+import', 
             r'from desktop.modern.core.\1 import'),
             
            # from infrastructure.xxx import yyy
            (r'from\s+infrastructure\.([a-zA-Z0-9_\.]+)\s+import',
             r'from desktop.modern.infrastructure.\1 import'),
        ]
        
        # Files to exclude from processing
        self.exclude_patterns = [
            '__pycache__',
            '.pyc',
            '.git',
            'tests',
            'legacy',  # Skip legacy code
            'web_app',  # Skip web app code
        ]
    
    def should_process_file(self, file_path: Path) -> bool:
        """Check if file should be processed."""
        if not file_path.suffix == '.py':
            return False
            
        path_str = str(file_path)
        for pattern in self.exclude_patterns:
            if pattern in path_str:
                return False
                
        return True
    
    def fix_imports_in_file(self, file_path: Path) -> int:
        """Fix imports in a single file. Returns number of changes made."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            changes_made = 0
            
            # Apply each import pattern
            for pattern, replacement in self.import_patterns:
                new_content, count = re.subn(pattern, replacement, content)
                if count > 0:
                    print(f"  Fixed {count} imports with pattern: {pattern}")
                    content = new_content
                    changes_made += count
            
            # Only write if changes were made
            if changes_made > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Fixed {changes_made} imports in {file_path}")
                
            return changes_made
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            return 0
    
    def fix_all_imports(self) -> None:
        """Fix imports in all Python files in the modern directory."""
        print("🔧 Starting systematic import fixing...")
        
        # Process modern directory
        modern_dir = self.base_path / "src" / "desktop" / "modern"
        if modern_dir.exists():
            print(f"📁 Processing modern directory: {modern_dir}")
            self._process_directory(modern_dir)
        
        # Shared directory is no longer used - services moved to modern
            
        print(f"\n✅ Import fixing complete!")
        print(f"   Files processed: {self.fixed_files}")
        print(f"   Total changes: {self.total_changes}")
    
    def _process_directory(self, directory: Path) -> None:
        """Process all Python files in a directory recursively."""
        for file_path in directory.rglob("*.py"):
            if self.should_process_file(file_path):
                changes = self.fix_imports_in_file(file_path)
                if changes > 0:
                    self.fixed_files += 1
                    self.total_changes += changes

def main():
    """Main entry point."""
    # Get the TKA project root
    current_dir = Path(__file__).parent
    tka_root = current_dir
    
    # Find TKA root by going up until we find src/desktop
    while tka_root.parent != tka_root:
        if (tka_root / "src" / "desktop").exists():
            break
        tka_root = tka_root.parent
    
    if not (tka_root / "src" / "desktop").exists():
        print("❌ Could not find TKA project root")
        return
    
    print(f"🎯 TKA Project root: {tka_root}")
    
    # Create and run the fixer
    fixer = ImportFixer(str(tka_root))
    fixer.fix_all_imports()
    
    print("\n🚀 Import fixing complete! You can now run the application.")

if __name__ == "__main__":
    main()
