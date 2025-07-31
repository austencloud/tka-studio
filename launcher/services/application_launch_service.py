from datetime import datetime
import logging
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Optional

from desktop.modern.core.interfaces import (
    IApplicationLaunchService,
    ILauncherStateService,
)
from desktop.modern.domain.models import (
    ApplicationData,
    ApplicationStatus,
    LaunchRequest,
    LaunchResult,
)

logger = logging.getLogger(__name__)


class ApplicationLaunchService(IApplicationLaunchService):
    def __init__(self, state_service: Optional[ILauncherStateService] = None):
        self._state_service = state_service
        self._running_processes: dict[str, subprocess.Popen] = {}

    def launch_application(self, request: LaunchRequest) -> LaunchResult:
        start_time = time.time()
        try:
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

            self._state_service.update_application_status(
                request.application_id, ApplicationStatus.STARTING
            )

            if self._is_debugger_attached() and self._is_tka_application(app):
                process = self._launch_with_debugger_support(app, request)
            else:
                process = self._launch_process(app, request)

            if process:
                self._running_processes[request.application_id] = process
                self._state_service.update_application_status(
                    request.application_id, ApplicationStatus.RUNNING, process.pid
                )
                timestamp = datetime.now().isoformat()
                updated_app = app.mark_launched(timestamp, process.pid)
                self._state_service.add_application(updated_app)
                execution_time = int((time.time() - start_time) * 1000)
                logger.info(f"Launched {app.title} (PID: {process.pid})")
                return LaunchResult.success_result(request, process.pid, execution_time)
            else:
                self._state_service.update_application_status(
                    request.application_id, ApplicationStatus.ERROR
                )
                execution_time = int((time.time() - start_time) * 1000)
                return LaunchResult.error_result(
                    request, "Failed to start application process", execution_time
                )

        except Exception as e:
            if self._state_service:
                self._state_service.update_application_status(
                    request.application_id, ApplicationStatus.ERROR
                )
            execution_time = int((time.time() - start_time) * 1000)
            logger.error(f"Launch failed: {str(e)}")
            return LaunchResult.error_result(
                request, f"Launch failed: {str(e)}", execution_time
            )

    def _launch_with_debugger_support(
        self, app: ApplicationData, request: LaunchRequest
    ) -> Optional[subprocess.Popen]:
        python_executable = sys.executable

        if self._is_tka_desktop_app(app):
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
            command = [python_executable, str(script_path)]
        else:
            if app.command.startswith("python"):
                command_parts = app.command.split()
                command = [python_executable] + command_parts[1:]
            else:
                command = app.command.split()

        tka_root = Path(app.working_dir).parent.parent.parent
        env = os.environ.copy()
        if app.environment_vars:
            env.update(app.environment_vars)

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

        existing_pythonpath = env.get("PYTHONPATH", "")
        if existing_pythonpath:
            pythonpath_parts.append(existing_pythonpath)

        env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

        logger.info(f"Launching with debugger: {' '.join(command)} (cwd: {tka_root})")

        try:
            process = subprocess.Popen(
                command,
                cwd=str(tka_root),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=None,
                universal_newlines=True,
                bufsize=1,
                encoding="utf-8",
                errors="replace",
                shell=False,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
            time.sleep(0.2)
            if process.poll() is None:
                import threading

                def forward_output():
                    try:
                        for line in process.stdout:
                            print(f"[{app.title}] {line.rstrip()}")
                            sys.stdout.flush()
                    except Exception as e:
                        logger.error(f"Error forwarding output: {e}")

                threading.Thread(target=forward_output, daemon=True).start()
                return process
            else:
                logger.error(
                    f"Debug process exited immediately with code: {process.returncode}"
                )
                return None

        except Exception as e:
            logger.error(f"Failed to launch debug process: {e}")
            return None

    def _launch_process(
        self, app: ApplicationData, request: LaunchRequest
    ) -> Optional[subprocess.Popen]:
        try:
            command = app.command
            working_dir = app.working_dir or Path.cwd()
            env = dict(app.environment_vars) if app.environment_vars else None
            launch_options = request.launch_options or {}

            logger.info(f"Launching: {command}")

            if app.category.value in ["Desktop Applications", "Web Applications"]:
                process = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=working_dir,
                    env=env,
                    **launch_options,
                )
            else:
                process = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=working_dir,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    **launch_options,
                )

            time.sleep(0.5)
            if process.poll() is None:
                logger.info(f"Process started successfully (PID: {process.pid})")
                return process
            else:
                logger.error(
                    f"Process exited immediately with code: {process.returncode}"
                )
                return None

        except Exception as e:
            logger.error(f"Failed to launch process: {e}")
            return None

    def stop_application(self, app_id: str) -> bool:
        try:
            if app_id in self._running_processes:
                process = self._running_processes[app_id]
                logger.info(f"Stopping application {app_id} (PID: {process.pid})")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    logger.warning(f"Force killing {app_id}")
                    process.kill()
                    process.wait()
                del self._running_processes[app_id]
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
        if app_id not in self._running_processes:
            return False
        process = self._running_processes[app_id]
        if process.poll() is None:
            return True
        else:
            del self._running_processes[app_id]
            if self._state_service:
                self._state_service.update_application_status(
                    app_id, ApplicationStatus.STOPPED
                )
            return False

    def get_running_applications(self) -> list[ApplicationData]:
        if not self._state_service:
            return []
        state = self._state_service.get_current_state()
        return state.get_running_applications()

    def get_application_process_id(self, app_id: str) -> Optional[int]:
        if app_id in self._running_processes:
            process = self._running_processes[app_id]
            if process.poll() is None:
                return process.pid
        return None

    def kill_application(self, app_id: str) -> bool:
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
        if self.is_application_running(app_id):
            self.stop_application(app_id)
            time.sleep(1)
        request = LaunchRequest(
            application_id=app_id,
            timestamp=datetime.now().isoformat(),
            session_id="restart",
            user_initiated=True,
        )
        return self.launch_application(request)

    def _is_debugger_attached(self) -> bool:
        try:
            import debugpy

            return debugpy.is_client_connected()
        except ImportError:
            pass
        try:
            import sys

            return hasattr(sys, "gettrace") and sys.gettrace() is not None
        except:
            pass
        return False

    def _is_tka_application(self, app: ApplicationData) -> bool:
        tka_app_ids = {
            "desktop_modern",
            "desktop_legacy",
            "desktop_modern_debug",
            "desktop_legacy_debug",
        }
        return app.id in tka_app_ids

    def _is_tka_desktop_app(self, app: ApplicationData) -> bool:
        return app.id in {"desktop_modern", "desktop_legacy"}

    def cleanup(self):
        logger.info("Cleaning up application launch service...")
        for app_id in list(self._running_processes.keys()):
            try:
                self.stop_application(app_id)
            except Exception as e:
                logger.error(f"Error stopping {app_id} during cleanup: {e}")
        self._running_processes.clear()
        logger.info("Application launch service cleanup complete")
