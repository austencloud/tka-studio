"""
Integration Script: Replace Browse Tab with Service-Enabled Version

This script integrates the new service-enabled browse tab into the modern architecture.
"""

from __future__ import annotations

import logging
from pathlib import Path
import shutil


logger = logging.getLogger(__name__)


def integrate_new_browse_tab():
    """Replace the old browse tab with the new service-enabled version."""
    try:
        logger.info("🔄 Integrating new browse tab with service support...")

        # Paths
        modern_dir = Path(__file__).parent
        old_browse_tab = (
            modern_dir / "src" / "presentation" / "tabs" / "browse" / "browse_tab.py"
        )
        new_browse_tab = (
            modern_dir / "src" / "presentation" / "tabs" / "browse" / "browse_tab.py"
        )
        backup_browse_tab = (
            modern_dir
            / "src"
            / "presentation"
            / "tabs"
            / "browse"
            / "browse_tab_backup.py"
        )

        # Create backup of original
        if old_browse_tab.exists() and not backup_browse_tab.exists():
            shutil.copy2(old_browse_tab, backup_browse_tab)
            logger.info(f"✅ Created backup: {backup_browse_tab}")

        # Replace with new version
        if new_browse_tab.exists():
            shutil.copy2(new_browse_tab, old_browse_tab)
            logger.info("✅ Replaced browse_tab.py with service-enabled version")
        else:
            logger.error(f"❌ New browse tab file not found: {new_browse_tab}")
            return False

        logger.info("🎉 Integration complete!")
        return True

    except Exception as e:
        logger.exception(f"❌ Integration failed: {e}")
        return False


def register_services_in_application_factory():
    """Instructions for updating the application factory to register browse services."""
    logger.info("\n" + "=" * 80)
    logger.info("📋 MANUAL INTEGRATION STEPS REQUIRED:")
    logger.info("=" * 80)
    logger.info("1. Update src/core/application/application_factory.py")
    logger.info("   Add this import:")
    logger.info(
        "   from desktop.modern.core.dependency_injection.browse_service_registration import register_browse_services"
    )
    logger.info("")
    logger.info("2. In the create_production_app() method, add:")
    logger.info("   register_browse_services(container, sequences_directory)")
    logger.info("")
    logger.info("3. Update any browse tab instantiation to pass the DI container:")
    logger.info("   browse_tab = BrowseTab(sequences_dir, settings_file, container)")
    logger.info("=" * 80)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    success = integrate_new_browse_tab()
    if success:
        register_services_in_application_factory()
    else:
        logger.error("Integration failed - manual steps may be required")
