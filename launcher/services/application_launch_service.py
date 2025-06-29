"""
Application Launch Service Implementation.

Handles the actual process of launching applications with multi-process debugging support,
process lifecycle management, and launch feedback.
"""

import logging
import subprocess
import time
import psutil
import os
import sys
from typing import List, Optional, Dict
from pathlib import Path
from datetime import datetime

from domain.models import (
    ApplicationData,
    LaunchRequest,
    LaunchResult,
    ApplicationStatus,
)
from core.interfaces import IApplicationLaunchService, ILauncherStateService

logger = logging.getLogger(__name__)


class ApplicationLaunchService(IApplicationLaunchService):
    """
    Service for launching and managing applications with debugging support.

    Provides process management, launch feedback, and application
    lifecycle tracking with VS Code multi-process debugging integration.
    """

    def __init__(self, state_service: Optional[ILauncherStateService] = None):
        """Initialize the application launch service."""
        self._state_service = state_service
        self._running_processes: Dict[str, subprocess.Popen] = {}

    def launch_application(self, request: LaunchRequest) -> LaunchResult:
        """Launch an application and return the result."""
        start_time = time.time()

        try:
            # Get application data
            if not self._state_service:
                return LaunchResult.error_result(
                    request, "No state service available", 0
                )

            state = self._state_service.get_current_state()
            app = state.get_application(request.application_id)

            if not app:
                return LaunchResult.error_result(
                    request, f"Application {request.application_id} not found", 0
                )

            if not app.enabled:
                return LaunchResult.error_result(
                    request, f"Application {app.title} is disabled", 0
                )

            # Update application status to starting
            self._state_service.update_application_status(
                request.application_id, ApplicationStatus.STARTING
            )

            # Launch based on whether VS Code debugger is attached
            if self._is_debugger_attached() and self._is_tka_application(app):
                logger.info(f"🐛 DEBUG LAUNCH: {app.title} with debugger support")
                process = self._launch_with_debugger_support(app, request)
            else:
                logger.info(f"🚀 STANDARD LAUNCH: {app.title}")
                process = self._launch_process(app, request)

            if process:
                # Store process reference
                self._running_processes[request.application_id] = process

                # Update application status to running
                self._state_service.update_application_status(
                    request.application_id, ApplicationStatus.RUNNING, process.pid
                )

                # Update launch statistics
                timestamp = datetime.now().isoformat()
                updated_app = app.mark_launched(timestamp, process.pid)
                self._state_service.add_application(updated_app)

                execution_time = int((time.time() - start_time) * 1000)

                logger.info(f"Successfully launched {app.title} (PID: {process.pid})")
                return LaunchResult.success_result(request, process.pid, execution_time)

            else:
                # Launch failed
                self._state_service.update_application_status(
                    request.application_id, ApplicationStatus.ERROR
                )

                execution_time = int((time.time() - start_time) * 1000)
                return LaunchResult.error_result(
                    request, "Failed to start application process", execution_time
                )

        except Exception as e:
            # Update status to error
            if self._state_service:
                self._state_service.update_application_status(
                    request.application_id, ApplicationStatus.ERROR
                )

            execution_time = int((time.time() - start_time) * 1000)
            error_msg = f"Launch failed: {str(e)}"
            logger.error(error_msg)

            return LaunchResult.error_result(request, error_msg, execution_time)

    def _launch_with_debugger_support(
        self, app: ApplicationData, request: LaunchRequest
    ) -> Optional[subprocess.Popen]:
        """Launch application with debugger support using VS Code's subprocess debugging."""

        logger.info("🐛 DEBUGGER MODE: Using automatic subprocess debugging")

        # Use the same Python interpreter that's being debugged
        # This leverages VS Code's "subProcess": true feature
        python_executable = sys.executable

        # Prepare the command based on application type
        if self._is_tka_desktop_app(app):
            # For TKA desktop apps, launch the main.py directly
            if "modern" in app.id:
                script_path = (
                    Path(app.working_dir).parent.parent.parent
                    / "src"
                    / "desktop"
                    / "modern"
                    / "main.py"
                )
            elif "legacy" in app.id:
                script_path = (
                    Path(app.working_dir).parent.parent.parent
                    / "src"
                    / "desktop"
                    / "legacy"
                    / "main.py"
                )
            else:
                script_path = Path(app.working_dir) / app.command.split()[-1]

            # Build command that will inherit debugger
            command = [python_executable, str(script_path)]

        else:
            # For other apps, use the original command but ensure Python subprocess inheritance
            if app.command.startswith("python"):
                command_parts = app.command.split()
                command = [python_executable] + command_parts[1:]
            else:
                command = app.command.split()

        # Environment setup for debugging - use TKA root as working directory
        tka_root = Path(
            app.working_dir
        ).parent.parent.parent  # Go from src/desktop/modern back to TKA root
        env = os.environ.copy()
        if app.environment_vars:
            env.update(app.environment_vars)

        # Ensure PYTHONPATH includes all necessary paths
        pythonpath_parts = [
            str(tka_root),
            str(tka_root / "src"),
            str(tka_root / "launcher"),
        ]

        if "modern" in app.id:
            pythonpath_parts.extend(
                [
                    str(tka_root / "src" / "desktop" / "modern"),
                    str(tka_root / "src" / "desktop" / "modern" / "src"),
                ]
            )
        elif "legacy" in app.id:
            pythonpath_parts.extend(
                [
                    str(tka_root / "src" / "desktop" / "legacy"),
                ]
            )

        # Add existing PYTHONPATH if present
        existing_pythonpath = env.get("PYTHONPATH", "")
        if existing_pythonpath:
            pythonpath_parts.append(existing_pythonpath)

        env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

        # Log the launch details for debugging
        logger.info(f"🔍 DEBUG LAUNCH DETAILS:")
        logger.info(f"   Command: {' '.join(command)}")
        logger.info(f"   Working Directory: {tka_root}")
        logger.info(f"   Python Executable: {python_executable}")
        logger.info(f"   PYTHONPATH: {env['PYTHONPATH']}")

        try:
            # Launch the process - capture output to forward to VS Code terminal
            process = subprocess.Popen(
                command,
                cwd=str(tka_root),  # Use TKA root as working directory
                env=env,
                stdout=subprocess.PIPE,  # Capture output to forward
                stderr=subprocess.STDOUT,  # Combine stderr with stdout
                stdin=None,
                universal_newlines=True,  # Handle text properly
                bufsize=1,  # Line buffered
                encoding="utf-8",  # Fix emoji encoding
                errors="replace",  # Replace problematic characters
                # Important: Don't use shell=True as it breaks subprocess debugging
                shell=False,
                # On Windows, don't create new console
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )

            # Give the process a moment to start
            time.sleep(0.2)  # Reduced from 0.5 for faster startup

            # Verify the process started successfully
            if process.poll() is None:
                logger.info(
                    f"✅ Debug process started successfully (PID: {process.pid})"
                )
                logger.info(f"🐛 Breakpoints should now work in the subprocess!")

                # Start a thread to forward subprocess output to main terminal
                import threading

                def forward_output():
                    """Forward subprocess output to main terminal."""
                    try:
                        for line in process.stdout:
                            # Forward subprocess output to main process stdout
                            print(f"[{app.title}] {line.rstrip()}")
                            sys.stdout.flush()
                    except Exception as e:
                        logger.error(f"Error forwarding output: {e}")

                # Start output forwarding thread
                output_thread = threading.Thread(target=forward_output, daemon=True)
                output_thread.start()

                return process
            else:
                logger.error(
                    f"❌ Debug process exited immediately with code: {process.returncode}"
                )
                return None

        except Exception as e:
            logger.error(f"❌ Failed to launch debug process: {e}")
            return None

    def _launch_process(
        self, app: ApplicationData, request: LaunchRequest
    ) -> Optional[subprocess.Popen]:
        """Launch application using standard process creation."""
        try:
            # Prepare command
            command = app.command
            working_dir = app.working_dir or Path.cwd()

            # Prepare environment
            env = dict(app.environment_vars) if app.environment_vars else None

            # Launch options from request
            launch_options = request.launch_options or {}

            logger.info(f"🚀 Standard launch: {command}")

            # Start the process
            if app.category.value in ["Desktop Applications", "Web Applications"]:
                # For GUI applications
                process = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=working_dir,
                    env=env,
                    **launch_options,
                )
            else:
                # Command-line tools - capture output
                process = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=working_dir,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    **launch_options,
                )

            # Give the process a moment to start
            time.sleep(0.5)

            # Check if process is still running
            if process.poll() is None:
                logger.info(
                    f"✅ Standard process started successfully (PID: {process.pid})"
                )
                return process
            else:
                logger.error(
                    f"❌ Standard process exited immediately with code: {process.returncode}"
                )
                return None

        except Exception as e:
            logger.error(f"❌ Failed to launch standard process: {e}")
            return None

    def stop_application(self, app_id: str) -> bool:
        """Stop a running application."""
        try:
            if app_id in self._running_processes:
                process = self._running_processes[app_id]

                logger.info(f"🛑 Stopping application {app_id} (PID: {process.pid})")

                # Try graceful termination first
                process.terminate()

                # Wait for process to terminate
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if graceful termination fails
                    logger.warning(f"⚠️ Force killing {app_id}")
                    process.kill()
                    process.wait()

                # Clean up
                del self._running_processes[app_id]

                # Update status
                if self._state_service:
                    self._state_service.update_application_status(
                        app_id, ApplicationStatus.STOPPED
                    )

                logger.info(f"✅ Stopped application {app_id}")
                return True

            else:
                logger.warning(f"⚠️ Application {app_id} is not running")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to stop application {app_id}: {e}")
            return False

    def is_application_running(self, app_id: str) -> bool:
        """Check if an application is currently running."""
        if app_id not in self._running_processes:
            return False

        process = self._running_processes[app_id]

        # Check if process is still alive
        if process.poll() is None:
            return True
        else:
            # Process has terminated, clean up
            del self._running_processes[app_id]

            if self._state_service:
                self._state_service.update_application_status(
                    app_id, ApplicationStatus.STOPPED
                )

            return False

    def get_running_applications(self) -> List[ApplicationData]:
        """Get all currently running applications."""
        if not self._state_service:
            return []

        state = self._state_service.get_current_state()
        return state.get_running_applications()

    def get_application_process_id(self, app_id: str) -> Optional[int]:
        """Get the process ID of a running application."""
        if app_id in self._running_processes:
            process = self._running_processes[app_id]
            if process.poll() is None:  # Still running
                return process.pid

        return None

    def kill_application(self, app_id: str) -> bool:
        """Force kill an application process."""
        try:
            if app_id in self._running_processes:
                process = self._running_processes[app_id]
                process.kill()
                process.wait()

                del self._running_processes[app_id]

                if self._state_service:
                    self._state_service.update_application_status(
                        app_id, ApplicationStatus.STOPPED
                    )

                logger.info(f"Force killed application {app_id}")
                return True

            else:
                logger.warning(f"Application {app_id} is not running")
                return False

        except Exception as e:
            logger.error(f"Failed to kill application {app_id}: {e}")
            return False

    def restart_application(self, app_id: str) -> LaunchResult:
        """Restart a running application."""
        # Stop the application first
        if self.is_application_running(app_id):
            self.stop_application(app_id)

            # Wait a moment for cleanup
            time.sleep(1)

        # Create new launch request
        request = LaunchRequest(
            application_id=app_id,
            timestamp=datetime.now().isoformat(),
            session_id="restart",
            user_initiated=True,
        )

        return self.launch_application(request)

    def _is_debugger_attached(self) -> bool:
        """Check if a debugger is currently attached (simplified)."""
        try:
            # Check for debugpy (VS Code debugger)
            import debugpy

            return debugpy.is_client_connected()
        except ImportError:
            pass

        try:
            # Check for pdb or other debuggers
            import sys

            return hasattr(sys, "gettrace") and sys.gettrace() is not None
        except:
            pass

        return False

    def _is_tka_application(self, app: ApplicationData) -> bool:
        """Check if this is a TKA application that supports debugging."""
        tka_app_ids = {
            "desktop_modern",
            "desktop_legacy",
            "desktop_modern_debug",
            "desktop_legacy_debug",
        }
        return app.id in tka_app_ids

    def _is_tka_desktop_app(self, app: ApplicationData) -> bool:
        """Check if this is specifically a TKA desktop application."""
        return app.id in {"desktop_modern", "desktop_legacy"}

    def cleanup(self):
        """Cleanup all running processes."""
        logger.info("🧹 Cleaning up application launch service...")

        for app_id in list(self._running_processes.keys()):
            try:
                self.stop_application(app_id)
            except Exception as e:
                logger.error(f"❌ Error stopping {app_id} during cleanup: {e}")

        self._running_processes.clear()
        logger.info("✅ Application launch service cleanup complete")
