#!/usr/bin/env python3
"""
Debug script to test application startup and find the tab widget.
"""

import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def debug_application_startup():
    """Debug the application startup process."""
    try:
        logger.info("🚀 Starting application startup debug...")

        # Import Qt
        from PyQt6.QtCore import QObject, QTimer
        from PyQt6.QtTest import QTest
        from PyQt6.QtWidgets import QApplication, QTabWidget

        # Create application
        app = QApplication.instance()
        if not app:
            app = QApplication([])

        logger.info("✅ QApplication created")

        # Import and create main window
        from desktop.modern.main import create_application

        logger.info("📦 Creating application using create_application...")
        app, main_window = create_application()

        logger.info(f"✅ Application created: {type(main_window)}")
        logger.info(
            f"📋 Main window attributes: {[attr for attr in dir(main_window) if not attr.startswith('_')]}"
        )

        # Show the window
        main_window.show()
        logger.info("✅ Main window shown")

        # Wait for initialization
        QTest.qWait(5000)  # Wait 5 seconds for full initialization
        logger.info("⏰ Waited 5 seconds for initialization")

        # Check if tab_widget attribute exists
        if hasattr(main_window, "tab_widget"):
            tab_widget = main_window.tab_widget
            logger.info(f"✅ Found tab_widget attribute: {type(tab_widget)}")

            if tab_widget:
                logger.info(f"📋 Tab widget count: {tab_widget.count()}")
                for i in range(tab_widget.count()):
                    tab_text = tab_widget.tabText(i)
                    tab_widget_obj = tab_widget.widget(i)
                    logger.info(f"   Tab {i}: '{tab_text}' -> {type(tab_widget_obj)}")
            else:
                logger.warning("⚠️ tab_widget is None")
        else:
            logger.warning("⚠️ No tab_widget attribute found")

        # Try to find tab widget using findChild
        tab_widgets = main_window.findChildren(QTabWidget)
        logger.info(f"🔍 Found {len(tab_widgets)} QTabWidget children")

        for i, tw in enumerate(tab_widgets):
            logger.info(f"   TabWidget {i}: {type(tw)} with {tw.count()} tabs")
            for j in range(tw.count()):
                tab_text = tw.tabText(j)
                logger.info(f"      Tab {j}: '{tab_text}'")

        # Check all children
        all_children = main_window.findChildren(QObject)
        logger.info(f"🔍 Total children: {len(all_children)}")

        # Look for Browse tab specifically
        browse_related = []
        for child in all_children:
            class_name = child.__class__.__name__
            if "browse" in class_name.lower() or "tab" in class_name.lower():
                browse_related.append(f"{class_name}: {child}")

        if browse_related:
            logger.info("🎯 Browse/Tab related components:")
            for item in browse_related[:10]:  # Show first 10
                logger.info(f"   {item}")

        # Check central widget
        central_widget = main_window.centralWidget()
        if central_widget:
            logger.info(f"🏠 Central widget: {type(central_widget)}")
            central_children = central_widget.findChildren(QTabWidget)
            logger.info(f"🔍 Central widget tab widgets: {len(central_children)}")

        logger.info("🎉 Debug completed successfully!")

        # Keep window open for a moment
        QTimer.singleShot(2000, app.quit)
        app.exec()

        return True

    except Exception as e:
        logger.error(f"❌ Debug failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run the debug."""
    success = debug_application_startup()
    if success:
        print("✅ Debug completed successfully")
        return 0
    else:
        print("❌ Debug failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
