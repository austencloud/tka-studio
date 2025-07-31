"""
Application Manager for TKA Unified Launcher.
Handles launching and managing TKA applications.
"""

from pathlib import Path
import subprocess
from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal


class ApplicationManager(QObject):
    """Manages application launching and lifecycle."""

    # Signals
    app_launched = pyqtSignal(str, str)  # app_id, process_info
    app_finished = pyqtSignal(str, int)  # app_id, exit_code
    app_error = pyqtSignal(str, str)  # app_id, error_message

    def __init__(self, app_definitions):
        super().__init__()
        self.app_definitions = app_definitions
        self.running_processes: dict[str, subprocess.Popen] = {}

    def launch_application(self, app_id: str) -> bool:
        """Launch an application by ID."""
        try:
            app = self.app_definitions.get_by_id(app_id)
            if not app:
                self.app_error.emit(app_id, f"Application '{app_id}' not found")
                return False

            # Get the command to execute
            command = self._get_launch_command(app)
            if not command:
                self.app_error.emit(app_id, f"No launch command for '{app_id}'")
                return False

            # Launch the process
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=self._get_working_directory(app),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Store the process
            self.running_processes[app_id] = process

            # Emit success signal
            self.app_launched.emit(app_id, f"Process started (PID: {process.pid})")

            return True

        except Exception as e:
            self.app_error.emit(app_id, str(e))
            return False

    def _get_launch_command(self, app) -> Optional[str]:
        """Get the launch command for an application."""
        if app.id == "desktop_legacy":
            return "python main.py --legacy"
        elif app.id == "desktop_modern":
            return "python main.py --modern"
        elif app.id == "web_app":
            return "python -m http.server 8000"
        elif app.id == "dev_tools":
            return "python main.py --dev"
        else:
            return app.command if hasattr(app, "command") else None

    def _get_working_directory(self, app) -> str:
        """Get the working directory for an application."""
        # Default to TKA root directory
        return str(Path(__file__).parent.parent.parent)

    def stop_application(self, app_id: str) -> bool:
        """Stop a running application."""
        if app_id in self.running_processes:
            try:
                process = self.running_processes[app_id]
                process.terminate()
                exit_code = process.wait(timeout=5)
                del self.running_processes[app_id]
                self.app_finished.emit(app_id, exit_code)
                return True
            except Exception as e:
                self.app_error.emit(app_id, f"Failed to stop: {e}")
                return False
        return False

    def is_running(self, app_id: str) -> bool:
        """Check if an application is currently running."""
        if app_id in self.running_processes:
            process = self.running_processes[app_id]
            return process.poll() is None
        return False

    def cleanup(self):
        """Clean up all running processes."""
        for app_id in list(self.running_processes.keys()):
            self.stop_application(app_id)
