"""
Application Launch Service Implementation.

Handles the actual process of launching applications, managing
process lifecycle, and providing launch feedback.
"""

import logging
import subprocess
import time
import psutil
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
    Service for launching and managing applications.

    Provides process management, launch feedback, and application
    lifecycle tracking with proper error handling.
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

            # Launch the application
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

    def stop_application(self, app_id: str) -> bool:
        """Stop a running application."""
        try:
            if app_id in self._running_processes:
                process = self._running_processes[app_id]

                # Try graceful termination first
                process.terminate()

                # Wait for process to terminate
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if graceful termination fails
                    process.kill()
                    process.wait()

                # Clean up
                del self._running_processes[app_id]

                # Update status
                if self._state_service:
                    self._state_service.update_application_status(
                        app_id, ApplicationStatus.STOPPED
                    )

                logger.info(f"Stopped application {app_id}")
                return True

            else:
                logger.warning(f"Application {app_id} is not running")
                return False

        except Exception as e:
            logger.error(f"Failed to stop application {app_id}: {e}")
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

    def _launch_process(
        self, app: ApplicationData, request: LaunchRequest
    ) -> Optional[subprocess.Popen]:
        """Launch the application process."""
        if not app.command:
            logger.error(f"No command specified for application {app.title}")
            return None

        try:
            # Prepare command
            command = app.command
            working_dir = app.working_dir or Path.cwd()

            # Prepare environment
            env = dict(app.environment_vars) if app.environment_vars else None

            # Launch options from request
            launch_options = request.launch_options or {}

            # Start the process
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=working_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                **launch_options,
            )

            logger.debug(f"Started process for {app.title}: {command}")
            return process

        except Exception as e:
            logger.error(f"Failed to launch {app.title}: {e}")
            return None

    def cleanup(self):
        """Cleanup all running processes."""
        logger.info("Cleaning up application launch service...")

        for app_id in list(self._running_processes.keys()):
            try:
                self.stop_application(app_id)
            except Exception as e:
                logger.error(f"Error stopping {app_id} during cleanup: {e}")

        self._running_processes.clear()
        logger.info("Application launch service cleanup complete")
