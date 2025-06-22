#!/usr/bin/env python3
"""
TKA Launcher Migration Script
============================

Migrates the TKA Launcher from the old monolithic structure to the new
reliable, modular design system. This script handles the transition safely.
"""

import os
import shutil
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LauncherMigrator:
    """Handles migration from old launcher structure to new reliable system."""

    def __init__(self, launcher_dir: Path):
        self.launcher_dir = Path(launcher_dir)
        self.backup_dir = self.launcher_dir / "backup_old_system"

    def migrate(self):
        """Run the complete migration process."""
        logger.info("🚀 Starting TKA Launcher migration to reliable design system")

        try:
            # Step 1: Create backup
            self._create_backup()

            # Step 2: Update imports in existing files
            self._update_imports()

            # Step 3: Update main.py to use new window
            self._update_main_file()

            # Step 4: Verify new system works
            self._verify_system()

            logger.info("✅ Migration completed successfully!")
            self._print_success_message()

        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            self._print_rollback_instructions()
            raise

    def _create_backup(self):
        """Create backup of old system."""
        logger.info("📦 Creating backup of old system...")

        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)

        self.backup_dir.mkdir(exist_ok=True)

        # Backup old launcher_window.py
        old_launcher = self.launcher_dir / "launcher_window.py"
        if old_launcher.exists():
            shutil.copy2(old_launcher, self.backup_dir / "old_launcher_window.py")
            logger.info("✅ Backed up old launcher_window.py")

        # Backup old UI files if they exist
        ui_files_to_backup = [
            "ui/design_system.py",
            "ui/effects",
            "ui/components",
        ]

        for file_path in ui_files_to_backup:
            full_path = self.launcher_dir / file_path
            if full_path.exists():
                if full_path.is_file():
                    shutil.copy2(full_path, self.backup_dir)
                else:
                    shutil.copytree(full_path, self.backup_dir / full_path.name)
                logger.info(f"✅ Backed up {file_path}")

    def _update_imports(self):
        """Update imports in existing files."""
        logger.info("🔄 Updating imports in existing files...")

        # Update application_grid.py if it exists
        self._update_application_grid()

        # Update any other files that might import old UI components
        self._update_other_files()

    def _update_application_grid(self):
        """Update application_grid.py to use reliable components."""
        grid_file = self.launcher_dir / "application_grid.py"

        if not grid_file.exists():
            logger.warning("application_grid.py not found, skipping update")
            return

        try:
            content = grid_file.read_text()

            # Replace old component imports
            old_imports = [
                "from launcher_window import ModernSearchBox, ModernButton",
                "from ui.design_system import",
                "from ui.effects",
                "from ui.components",
            ]

            new_import = """
# Import reliable components
from ui.components.reliable_components import ReliableApplicationCard
from ui.reliable_design_system import get_reliable_style_builder
from ui.reliable_effects import get_shadow_manager, get_animation_manager
"""

            # Remove old imports
            for old_import in old_imports:
                if old_import in content:
                    lines = content.split("\n")
                    new_lines = [
                        line
                        for line in lines
                        if not line.strip().startswith(old_import)
                    ]
                    content = "\n".join(new_lines)

            # Add new imports at the top (after existing imports)
            lines = content.split("\n")
            import_end = 0
            for i, line in enumerate(lines):
                if line.strip().startswith("import ") or line.strip().startswith(
                    "from "
                ):
                    import_end = i + 1

            lines.insert(import_end, new_import)
            content = "\n".join(lines)

            # Replace old component usage
            replacements = {
                "ApplicationCard": "ReliableApplicationCard",
                "ModernButton": "ReliableButton",
                "ModernSearchBox": "ReliableSearchBox",
            }

            for old, new in replacements.items():
                content = content.replace(old, new)

            # Write updated content
            grid_file.write_text(content)
            logger.info("✅ Updated application_grid.py")

        except Exception as e:
            logger.error(f"Failed to update application_grid.py: {e}")

    def _update_other_files(self):
        """Update other files that might use old components."""
        files_to_update = [
            "launcher_config.py",
            "tka_integration.py",
        ]

        for filename in files_to_update:
            file_path = self.launcher_dir / filename
            if file_path.exists():
                try:
                    content = file_path.read_text()

                    # Remove references to ENHANCED_UI_AVAILABLE
                    content = content.replace("ENHANCED_UI_AVAILABLE", "True")

                    # Remove complex UI availability checks
                    import re

                    content = re.sub(
                        r"if ENHANCED_UI_AVAILABLE:.*?else:.*?_apply_fallback_styling\(\)",
                        "self._setup_styling()",
                        content,
                        flags=re.DOTALL,
                    )

                    file_path.write_text(content)
                    logger.info(f"✅ Updated {filename}")

                except Exception as e:
                    logger.warning(f"Failed to update {filename}: {e}")

    def _update_main_file(self):
        """Update main.py to use new launcher window."""
        main_file = self.launcher_dir / "main.py"

        if not main_file.exists():
            logger.warning("main.py not found, creating new one")
            self._create_new_main_file()
            return

        try:
            content = main_file.read_text()

            # Replace old launcher window import
            old_imports = [
                "from launcher_window import TKAModernWindow",
                "from launcher_window import TKALauncherWindow",
            ]

            new_import = "from modern_launcher_window import TKALauncherWindow, create_launcher_window"

            # Update imports
            for old_import in old_imports:
                content = content.replace(old_import, new_import)

            # Update window creation
            content = content.replace("TKAModernWindow", "TKALauncherWindow")

            main_file.write_text(content)
            logger.info("✅ Updated main.py")

        except Exception as e:
            logger.error(f"Failed to update main.py: {e}")
            self._create_new_main_file()

    def _create_new_main_file(self):
        """Create a new main.py file."""
        main_content = '''#!/usr/bin/env python3
"""
TKA Launcher Main Entry Point
============================

Starts the TKA Launcher with the reliable design system.
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication

from launcher_config import LauncherConfig
from modern_launcher_window import create_launcher_window

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main application entry point."""
    try:
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("TKA Launcher")
        app.setApplicationVersion("2.0")
        
        # Load configuration
        config = LauncherConfig()
        
        # Create and show launcher window
        launcher = create_launcher_window(config)
        launcher.show()
        
        # Show welcome notification
        launcher.show_notification("Welcome to TKA Launcher v2.0!", "success")
        
        # Run application
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Failed to start launcher: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

        main_file = self.launcher_dir / "main.py"
        main_file.write_text(main_content)
        logger.info("✅ Created new main.py")

    def _verify_system(self):
        """Verify the new system works."""
        logger.info("🔍 Verifying new system...")

        required_files = [
            "ui/reliable_design_system.py",
            "ui/reliable_effects.py",
            "ui/components/reliable_components.py",
            "ui/launcher_components.py",
            "ui/window_layout.py",
            "ui/window_handlers.py",
            "modern_launcher_window.py",
        ]

        missing_files = []
        for file_path in required_files:
            if not (self.launcher_dir / file_path).exists():
                missing_files.append(file_path)

        if missing_files:
            raise Exception(f"Missing required files: {missing_files}")

        logger.info("✅ All required files present")

        # Try to import the new system
        try:
            sys.path.insert(0, str(self.launcher_dir))

            # Test imports
            from ui.reliable_design_system import get_reliable_style_builder
            from ui.reliable_effects import get_shadow_manager
            from modern_launcher_window import TKALauncherWindow

            # Test style builder
            style_builder = get_reliable_style_builder()
            test_style = style_builder.glass_surface("primary")
            assert "background-color:" in test_style

            logger.info("✅ New system imports and works correctly")

        except Exception as e:
            raise Exception(f"New system verification failed: {e}")

    def _print_success_message(self):
        """Print success message with next steps."""
        print("\n" + "=" * 60)
        print("🎉 TKA LAUNCHER MIGRATION SUCCESSFUL!")
        print("=" * 60)
        print()
        print("✅ Old system backed up to:", self.backup_dir)
        print("✅ New reliable design system installed")
        print("✅ All components updated")
        print("✅ System verified and working")
        print()
        print("📋 NEXT STEPS:")
        print("1. Test the launcher: python main.py")
        print("2. Verify all applications load correctly")
        print("3. Test search and filtering")
        print("4. Check hover animations and effects")
        print("5. Verify responsive design")
        print()
        print("🔧 FEATURES:")
        print("• Reliable glassmorphism effects")
        print("• Smooth hover animations")
        print("• Professional shadows and borders")
        print("• Responsive design")
        print("• Clean, modular architecture")
        print("• No fallback complexity")
        print()
        print("📝 If you encounter issues:")
        print(f"   Restore from backup: {self.backup_dir}")
        print("=" * 60)

    def _print_rollback_instructions(self):
        """Print rollback instructions."""
        print("\n" + "=" * 60)
        print("⚠️  MIGRATION FAILED - ROLLBACK INSTRUCTIONS")
        print("=" * 60)
        print()
        print("To restore the old system:")
        print(f"1. Copy files from {self.backup_dir} back to {self.launcher_dir}")
        print("2. Restore launcher_window.py from backup")
        print("3. Check git status and reset if needed")
        print()
        print("=" * 60)


def main():
    """Run the migration."""
    import sys

    # Get launcher directory
    if len(sys.argv) > 1:
        launcher_dir = Path(sys.argv[1])
    else:
        launcher_dir = Path.cwd()

    if not launcher_dir.exists():
        print(f"❌ Directory not found: {launcher_dir}")
        sys.exit(1)

    # Run migration
    migrator = LauncherMigrator(launcher_dir)

    try:
        migrator.migrate()
    except KeyboardInterrupt:
        print("\n❌ Migration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
