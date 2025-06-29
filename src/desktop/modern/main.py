#!/usr/bin/env python3
"""
Kinetic Constructor - Main Application Entry Point

Modern modular architecture with dependency injection and clean separation of concerns.
"""

import sys
from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon, QGuiApplication

modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

from presentation.components.ui.splash_screen import SplashScreen

class TKAMainWindow(QMainWindow):
    def __init__(
        self,
        splash_screen: Optional[SplashScreen] = None,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
        enable_api=True,
    ):
        super().__init__()
        self.splash = splash_screen
        self.target_screen = target_screen
        self.parallel_mode = parallel_mode
        self.parallel_geometry = parallel_geometry
        self.enable_api = enable_api

        from application.services.core.application_orchestrator import (
            ApplicationOrchestrator,
        )

        self.orchestrator = ApplicationOrchestrator()
        self.tab_widget = self.orchestrator.initialize_application(
            self,
            splash_screen,
            target_screen,
            parallel_mode,
            parallel_geometry,
            enable_api,
        )

    def _attach_production_debugger(self) -> None:
        try:
            from debug import attach_to_application
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(1000, lambda: self._do_debugger_attachment())
        except Exception:
            pass

    def _do_debugger_attachment(self) -> None:
        try:
            from debug import attach_to_application, get_production_debugger
            attach_to_application(self)
        except Exception:
            import traceback
            traceback.print_exc()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        if hasattr(self, "orchestrator"):
            self.orchestrator.handle_window_resize(self)

def detect_parallel_testing_mode():
    import argparse
    import os

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--parallel-testing", action="store_true")
    parser.add_argument("--monitor", choices=["primary", "secondary", "left", "right"])
    args, _ = parser.parse_known_args()

    env_parallel = os.environ.get("TKA_PARALLEL_TESTING", "").lower() == "true"
    env_monitor = os.environ.get("TKA_PARALLEL_MONITOR", "")
    env_geometry = os.environ.get("TKA_PARALLEL_GEOMETRY", "")

    parallel_mode = args.parallel_testing or env_parallel
    monitor = args.monitor or env_monitor

    return parallel_mode, monitor, env_geometry

def create_application():
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        app.setStyle("Fusion")

    parallel_mode, monitor, geometry = detect_parallel_testing_mode()
    screens = QGuiApplication.screens()
    if parallel_mode and monitor == "secondary" and len(screens) > 1:
        target_screen = screens[1]
    elif parallel_mode and monitor == "primary":
        target_screen = screens[0]
    else:
        target_screen = (
            screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
        )

    window = TKAMainWindow(
        splash_screen=None,
        target_screen=target_screen,
        parallel_mode=parallel_mode,
        parallel_geometry=geometry,
    )

    return app, window

def main():
    parallel_mode, monitor, geometry = detect_parallel_testing_mode()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    screens = QGuiApplication.screens()

    if parallel_mode and len(screens) > 1:
        if monitor in ["secondary", "right"]:
            primary_screen = screens[0]
            secondary_screen = screens[1]
            if secondary_screen.geometry().x() > primary_screen.geometry().x():
                target_screen = secondary_screen
            else:
                target_screen = primary_screen
        elif monitor in ["primary", "left"]:
            primary_screen = screens[0]
            secondary_screen = screens[1]
            if secondary_screen.geometry().x() < primary_screen.geometry().x():
                target_screen = secondary_screen
            else:
                target_screen = primary_screen
        else:
            target_screen = screens[1]
    else:
        target_screen = (
            screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
        )

    try:
        splash = SplashScreen(target_screen=target_screen)
        fade_in_animation = splash.show_animated()
        window = None

        def start_initialization():
            nonlocal window
            try:
                splash.update_progress(5, "Initializing application...")
                app.processEvents()
                icon_path = Path(__file__).parent / "images" / "icons" / "app_icon.png"
                if icon_path.exists():
                    app.setWindowIcon(QIcon(str(icon_path)))
                splash.update_progress(15, "Creating main window...")
                window = TKAMainWindow(
                    splash_screen=splash,
                    target_screen=target_screen,
                    parallel_mode=parallel_mode,
                    parallel_geometry=geometry,
                )
                complete_startup()
            except Exception:
                import traceback
                traceback.print_exc()
                return

        def complete_startup():
            if window is None:
                return
            splash.update_progress(100, "Ready!")
            app.processEvents()
            QTimer.singleShot(200, lambda: splash.hide_animated())
            QTimer.singleShot(300, lambda: window.show())

        fade_in_animation.finished.connect(start_initialization)
        return app.exec()

    except Exception:
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
