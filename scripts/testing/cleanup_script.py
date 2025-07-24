#!/usr/bin/env python3
"""
TKA Dead Code Cleanup Script

Automated cleanup of dead code identified by Vulture analysis.
Focus on safe removals with high confidence.
"""

import re
import os
from pathlib import Path

class TKADeadCodeCleaner:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.changes_made = []
        
    def remove_unused_mainwidget_imports(self):
        """Remove unused MainWidget imports from legacy files."""
        files_to_fix = [
            "src/desktop/legacy/src/base_widgets/base_beat_frame.py",
            "src/desktop/legacy/src/base_widgets/base_go_back_button.py", 
            "src/desktop/legacy/src/main_window/main_widget/browse_tab/browse_tab.py",
            "src/desktop/legacy/src/main_window/main_widget/generate_tab/generate_tab.py",
            "src/desktop/legacy/src/main_window/main_widget/learn_tab/learn_tab.py",
            # Add more files from vulture output
        ]
        
        for file_path in files_to_fix:
            full_path = self.root_path / file_path
            if full_path.exists():
                self._remove_mainwidget_import(full_path)
    
    def _remove_mainwidget_import(self, file_path: Path):
        """Remove MainWidget import from a specific file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Pattern to match MainWidget imports
            patterns = [
                r'from .* import .*MainWidget.*\n',
                r'from typing import TYPE_CHECKING.*MainWidget.*\n',
                r'if TYPE_CHECKING:\s*\n\s*from .* import .*MainWidget.*\n',
            ]
            
            original_content = content
            for pattern in patterns:
                content = re.sub(pattern, '', content, flags=re.MULTILINE)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.changes_made.append(f"Removed MainWidget import from {file_path}")
                print(f"✅ Cleaned MainWidget import from {file_path}")
            
        except Exception as e:
            print(f"❌ Error cleaning {file_path}: {e}")
    
    def remove_unused_variables(self):
        """Remove clearly unused variables (not in interfaces)."""
        specific_fixes = [
            ("src/desktop/legacy/src/letter_determination/services/motion_comparator.py", 46, "other_copy"),
            ("src/desktop/legacy/src/main_window/main_widget/browse_tab/sequence_picker/sequence_picker_sorter.py", 173, "skip_image"),
        ]
        
        for file_path, line_num, var_name in specific_fixes:
            full_path = self.root_path / file_path
            if full_path.exists():
                self._remove_unused_variable(full_path, line_num, var_name)
    
    def _remove_unused_variable(self, file_path: Path, line_num: int, var_name: str):
        """Remove unused variable from specific line."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if line_num <= len(lines):
                line = lines[line_num - 1]
                if var_name in line:
                    # Try to remove the variable assignment
                    new_line = re.sub(rf'\b{var_name}\s*=\s*[^,\n]*,?\s*', '', line)
                    if new_line.strip() and new_line != line:
                        lines[line_num - 1] = new_line
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(lines)
                        
                        self.changes_made.append(f"Removed unused variable '{var_name}' from {file_path}:{line_num}")
                        print(f"✅ Removed unused variable '{var_name}' from {file_path}")
        
        except Exception as e:
            print(f"❌ Error removing variable from {file_path}: {e}")
    
    def fix_syntax_error(self):
        """Fix the syntax error in domain_fixtures.py."""
        file_path = self.root_path / "src/desktop/modern/tests/fixtures/domain_fixtures.py"
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Fix trailing comma issue
                content = re.sub(r'domain\.models\.pictograph_models,\s*$', 'domain.models.pictograph_models', content, flags=re.MULTILINE)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.changes_made.append(f"Fixed syntax error in {file_path}")
                print(f"✅ Fixed syntax error in domain_fixtures.py")
                
            except Exception as e:
                print(f"❌ Error fixing syntax error: {e}")
    
    def remove_unreachable_code(self):
        """Remove unreachable code after return statements."""
        file_path = self.root_path / "src/desktop/legacy/src/main_window/main_widget/generate_tab/circular/CAP_executors/strict_rotated_CAP_executor.py"
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Find line 373 and check for unreachable code
                if len(lines) >= 373:
                    line = lines[372]  # 0-indexed
                    if 'return' in line:
                        # Check next lines for unreachable code
                        i = 373
                        while i < len(lines) and lines[i].strip() and not lines[i].startswith('def ') and not lines[i].startswith('class '):
                            lines[i] = ''  # Remove unreachable line
                            i += 1
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(lines)
                        
                        self.changes_made.append(f"Removed unreachable code from {file_path}")
                        print(f"✅ Removed unreachable code from CAP executor")
            
            except Exception as e:
                print(f"❌ Error removing unreachable code: {e}")
    
    def cleanup_test_imports(self):
        """Remove unused imports from test files."""
        test_files = [
            "src/desktop/modern/tests/application/services/graph_editor/test_hotkey_service.py",
            "src/desktop/modern/tests/unit/interfaces/test_thumbnail_generation_service_interface.py",
        ]
        
        for file_path in test_files:
            full_path = self.root_path / file_path
            if full_path.exists():
                self._remove_unused_test_imports(full_path)
    
    def _remove_unused_test_imports(self, file_path: Path):
        """Remove unused imports from test files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove unused MagicMock imports
            patterns = [
                r'from unittest\.mock import.*MagicMock.*\n',
                r'from .* import.*MagicMock.*\n',
            ]
            
            original_content = content
            for pattern in patterns:
                content = re.sub(pattern, '', content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.changes_made.append(f"Cleaned test imports from {file_path}")
                print(f"✅ Cleaned test imports from {file_path}")
        
        except Exception as e:
            print(f"❌ Error cleaning test imports from {file_path}: {e}")
    
    def run_cleanup(self):
        """Run all cleanup operations."""
        print("🧹 Starting TKA Dead Code Cleanup...")
        
        # Start with critical syntax error
        self.fix_syntax_error()
        
        # Safe removals
        self.remove_unused_mainwidget_imports()
        self.remove_unused_variables()
        self.remove_unreachable_code()
        self.cleanup_test_imports()
        
        print(f"\n✅ Cleanup complete! Made {len(self.changes_made)} changes:")
        for change in self.changes_made:
            print(f"  - {change}")
        
        print("\n🔍 Recommended next steps:")
        print("  1. Run vulture again to see remaining issues")
        print("  2. Run your tests to ensure nothing broke")
        print("  3. Review interface files manually (many 'unused' variables are actually API contracts)")

if __name__ == "__main__":
    cleaner = TKADeadCodeCleaner("F:/CODE/TKA")
    cleaner.run_cleanup()
