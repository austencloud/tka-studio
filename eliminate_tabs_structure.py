#!/usr/bin/env python3
"""
Eliminate Tabs Structure Migration Script

This script completely eliminates the unnecessary tabs folder structure and
reorganizes everything into logical, flat component and view hierarchies.

Architecture Transformation:
- FROM: src/desktop/modern/presentation/tabs/[tab_name]/
- TO:   src/desktop/modern/presentation/[logical_category]/

Categories:
- components/ - Reusable UI components
- views/ - Top-level view/tab implementations
- controllers/ - View controllers and coordinators
- managers/ - UI-specific managers

This eliminates arbitrary nesting and creates a logical, maintainable structure.
"""

import re
import shutil
from pathlib import Path


class TabsStructureEliminator:
    """Eliminates the tabs folder structure completely."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.tabs_dir = project_root / "src/desktop/modern/presentation/tabs"
        self.presentation_dir = project_root / "src/desktop/modern/presentation"

        # Target directories
        self.components_dir = self.presentation_dir / "components"
        self.views_dir = self.presentation_dir / "views"
        self.controllers_dir = self.presentation_dir / "controllers"
        self.managers_dir = self.presentation_dir / "managers"

        # Track migration mappings
        self.migration_mappings: dict[str, str] = {}
        self.files_to_update: set[Path] = set()
        self.updated_files: list[Path] = []
        self.errors: list[tuple[Path, str]] = []

    def analyze_tabs_structure(self) -> dict[str, any]:
        """Analyze the current tabs structure to plan migration."""
        print("Analyzing tabs structure for elimination...")

        analysis = {"tabs_found": [], "total_files": 0, "migration_plan": {}}

        if not self.tabs_dir.exists():
            print("No tabs directory found - migration not needed")
            return analysis

        # Analyze each tab
        for tab_dir in self.tabs_dir.iterdir():
            if tab_dir.is_dir() and not tab_dir.name.startswith("__"):
                tab_name = tab_dir.name
                analysis["tabs_found"].append(tab_name)

                tab_analysis = self._analyze_single_tab(tab_dir, tab_name)
                analysis["migration_plan"][tab_name] = tab_analysis
                analysis["total_files"] += tab_analysis["file_count"]

        print(
            f"Found {len(analysis['tabs_found'])} tabs with {analysis['total_files']} total files"
        )
        return analysis

    def _analyze_single_tab(self, tab_dir: Path, tab_name: str) -> dict[str, any]:
        """Analyze a single tab directory."""
        analysis = {
            "file_count": 0,
            "subdirectories": [],
            "main_files": [],
            "migration_targets": {},
        }

        for item in tab_dir.rglob("*"):
            if item.is_file() and item.suffix == ".py":
                analysis["file_count"] += 1
                rel_path = item.relative_to(tab_dir)

                # Determine migration target based on file type and location
                target = self._determine_migration_target(item, tab_name, rel_path)
                analysis["migration_targets"][str(rel_path)] = target

        return analysis

    def _determine_migration_target(
        self, file_path: Path, tab_name: str, rel_path: Path
    ) -> str:
        """Determine where a file should be migrated to."""
        file_name = file_path.name
        parent_dir = rel_path.parent.name if rel_path.parent != Path(".") else ""

        # Main tab files go to views
        if file_name.endswith("_tab.py") or file_name == f"{tab_name}_tab.py":
            return f"views/{tab_name}"

        # Coordinators go to controllers
        if "coordinator" in file_name or "controller" in file_name:
            return f"controllers/{tab_name}"

        # Components go to components
        if parent_dir == "components" or "component" in file_name:
            return f"components/{tab_name}"

        # Views go to views (but in subdirectory)
        if parent_dir == "views" or "view" in file_name:
            return f"views/{tab_name}"

        # Managers go to managers
        if parent_dir == "managers" or "manager" in file_name:
            return f"managers/{tab_name}"

        # Controllers go to controllers
        if parent_dir == "controllers":
            return f"controllers/{tab_name}"

        # Infrastructure and other specialized folders
        if parent_dir in ["infrastructure", "adapters", "orchestrators"]:
            return f"controllers/{tab_name}/{parent_dir}"

        # State management
        if parent_dir == "state" or "state" in file_name:
            return f"controllers/{tab_name}/state"

        # Default: put in views with the tab
        return f"views/{tab_name}"

    def create_target_directories(self) -> None:
        """Create all target directories."""
        print("Creating target directory structure...")

        # Create main directories
        for target_dir in [
            self.components_dir,
            self.views_dir,
            self.controllers_dir,
            self.managers_dir,
        ]:
            target_dir.mkdir(parents=True, exist_ok=True)

        print("Target directories created")

    def backup_tabs_structure(self) -> Path:
        """Create backup of the entire tabs structure."""
        backup_dir = self.project_root / "tabs_elimination_backup"
        backup_dir.mkdir(exist_ok=True)

        print(f"Creating backup in {backup_dir}")

        if self.tabs_dir.exists():
            backup_tabs = backup_dir / "tabs_original"
            if backup_tabs.exists():
                shutil.rmtree(backup_tabs)
            shutil.copytree(self.tabs_dir, backup_tabs)

        return backup_dir

    def migrate_tab_files(self, analysis: dict[str, any]) -> bool:
        """Migrate all tab files to their new locations."""
        print("Migrating tab files...")

        success_count = 0
        total_files = analysis["total_files"]

        for tab_name, tab_analysis in analysis["migration_plan"].items():
            tab_dir = self.tabs_dir / tab_name

            print(f"  Migrating {tab_name} tab...")

            for rel_path_str, target_path in tab_analysis["migration_targets"].items():
                source_file = tab_dir / rel_path_str
                target_file = (
                    self.presentation_dir / target_path / Path(rel_path_str).name
                )

                # Create target directory
                target_file.parent.mkdir(parents=True, exist_ok=True)

                try:
                    # Copy file to new location
                    shutil.copy2(source_file, target_file)

                    # Track migration mapping for import updates
                    old_import_path = f"desktop.modern.presentation.tabs.{tab_name}"
                    if len(Path(rel_path_str).parts) > 1:
                        # Handle nested paths
                        nested_path = "/".join(Path(rel_path_str).parts[:-1])
                        old_import_path += f".{nested_path.replace('/', '.')}"

                    new_import_path = (
                        f"desktop.modern.presentation.{target_path.replace('/', '.')}"
                    )
                    self.migration_mappings[old_import_path] = new_import_path

                    success_count += 1

                except Exception as e:
                    self.errors.append((source_file, f"Failed to migrate: {e}"))

        print(f"Successfully migrated {success_count}/{total_files} files")
        return success_count == total_files

    def update_import_statements(self) -> bool:
        """Update all import statements throughout the codebase."""
        print("Updating import statements...")

        # Find all Python files that might import from tabs
        files_to_check = list(self.project_root.rglob("*.py"))

        updated_count = 0

        for py_file in files_to_check:
            if self._update_file_imports(py_file):
                updated_count += 1

        print(f"Updated imports in {updated_count} files")
        return len(self.errors) == 0

    def _update_file_imports(self, file_path: Path) -> bool:
        """Update import statements in a single file."""
        try:
            content = file_path.read_text(encoding="utf-8")
            original_content = content

            # Update imports from tabs structure
            for old_import, new_import in self.migration_mappings.items():
                # Handle 'from X import Y' statements
                pattern = rf"from\s+{re.escape(old_import)}"
                replacement = f"from {new_import}"
                content = re.sub(pattern, replacement, content)

                # Handle 'import X' statements
                pattern = rf"import\s+{re.escape(old_import)}"
                replacement = f"import {new_import}"
                content = re.sub(pattern, replacement, content)

            # Handle general tabs imports
            content = re.sub(
                r"from\s+desktop\.modern\.presentation\.tabs\.(\w+)",
                r"from desktop.modern.presentation.views.\1",
                content,
            )

            # Write back if changed
            if content != original_content:
                file_path.write_text(content, encoding="utf-8")
                self.updated_files.append(file_path)
                return True

            return False

        except Exception as e:
            self.errors.append((file_path, f"Failed to update imports: {e}"))
            return False

    def create_new_init_files(self) -> None:
        """Create __init__.py files in new directory structure."""
        print("Creating new __init__.py files...")

        # Create main __init__.py files
        for main_dir in [self.views_dir, self.controllers_dir, self.managers_dir]:
            init_file = main_dir / "__init__.py"
            if not init_file.exists():
                init_file.write_text(f'"""{main_dir.name.title()} Package"""\n')

        # Create subdirectory __init__.py files
        for subdir in self.presentation_dir.rglob("*"):
            if subdir.is_dir() and not (subdir / "__init__.py").exists():
                if any(f.suffix == ".py" for f in subdir.iterdir() if f.is_file()):
                    init_file = subdir / "__init__.py"
                    init_file.write_text(f'"""{subdir.name.title()} Package"""\n')

    def remove_tabs_directory(self) -> None:
        """Remove the old tabs directory structure."""
        print("Removing old tabs directory...")

        if self.tabs_dir.exists():
            shutil.rmtree(self.tabs_dir)
            print("Tabs directory removed")
        else:
            print("Tabs directory already removed")


def main():
    """Main elimination function."""
    print("Starting Tabs Structure Elimination")
    print("=" * 60)

    # Get project root
    script_path = Path(__file__).resolve()
    project_root = script_path.parent

    # Initialize eliminator
    eliminator = TabsStructureEliminator(project_root)

    # Analyze current structure
    analysis = eliminator.analyze_tabs_structure()

    if not analysis["tabs_found"]:
        print("No tabs structure found - elimination not needed")
        return True

    # Create backup
    backup_dir = eliminator.backup_tabs_structure()

    try:
        # Create target directories
        eliminator.create_target_directories()

        # Migrate files
        if eliminator.migrate_tab_files(analysis):
            print("Phase 1 Complete: Files migrated successfully!")

            # Update imports
            eliminator.update_import_statements()
            print("Phase 2 Complete: Import statements updated!")

            # Create new __init__.py files
            eliminator.create_new_init_files()
            print("Phase 3 Complete: New structure initialized!")

            # Remove old tabs directory
            eliminator.remove_tabs_directory()
            print("Phase 4 Complete: Old structure removed!")

            print(f"\nBackup created at: {backup_dir}")
            print("\nTabs structure successfully eliminated!")
            print("New structure:")
            print("- components/ - Reusable UI components")
            print("- views/ - Top-level views and tabs")
            print("- controllers/ - Controllers and coordinators")
            print("- managers/ - UI-specific managers")

            return True
        else:
            print("ERROR: File migration failed")
            return False

    except Exception as e:
        print(f"ERROR: Elimination failed: {e}")
        print(f"Backup available at: {backup_dir}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
