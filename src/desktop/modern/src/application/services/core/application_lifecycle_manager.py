"""
Application Lifecycle Manager

Pure service for managing application lifecycle and startup sequence.
Extracted from KineticConstructorModern to follow single responsibility principle.

PROVIDES:
- Application initialization sequence
- Window positioning and sizing
- Parallel testing mode detection
- Screen detection and multi-monitor support
- API server startup coordination
"""

from typing import Optional, Tuple, Callable
from abc import ABC, abstractmethod
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QGuiApplication

# Import session service interface
from core.interfaces.session_services import ISessionStateService


class IApplicationLifecycleManager(ABC):
    """Interface for application lifecycle operations."""

    @abstractmethod
    def initialize_application(
        self,
        main_window: QMainWindow,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
        progress_callback: Optional[Callable] = None,
    ) -> None:
        """Initialize application with proper lifecycle management."""

    @abstractmethod
    def set_window_dimensions(
        self,
        main_window: QMainWindow,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
    ) -> None:
        """Set window dimensions using modern responsive design."""

    @abstractmethod
    def detect_parallel_testing_mode(self) -> Tuple[bool, str, str]:
        """Detect if we're running in parallel testing mode."""


class ApplicationLifecycleManager(IApplicationLifecycleManager):
    """
    Pure service for application lifecycle management.

    Handles application initialization, window management, and startup coordination
    without business logic dependencies. Uses clean separation of concerns.
    """

    def __init__(self, session_service: Optional[ISessionStateService] = None):
        """Initialize application lifecycle manager."""
        self.api_enabled = True
        self._session_service = session_service
        self._pending_session_data = None

    def initialize_application(
        self,
        main_window: QMainWindow,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
        progress_callback: Optional[Callable] = None,
    ) -> None:
        """Initialize application with proper lifecycle management."""
        if progress_callback:
            progress_callback(10, "Initializing application lifecycle...")

        # Set window title based on mode
        if parallel_mode:
            main_window.setWindowTitle("TKA Modern - Parallel Testing")
        else:
            main_window.setWindowTitle("🚀 Kinetic Constructor")

        # Set window dimensions
        self.set_window_dimensions(
            main_window, target_screen, parallel_mode, parallel_geometry
        )

        if progress_callback:
            progress_callback(85, "Restoring previous session...")

        # NEW: Restore session state if available
        if self._session_service:
            print("🔍 [LIFECYCLE] Session service available, attempting restoration...")
            try:
                restore_result = self._session_service.load_session_state()
                print(
                    f"🔍 [LIFECYCLE] Session load result: success={restore_result.success}, restored={restore_result.session_restored}"
                )

                if restore_result.success and restore_result.session_restored:
                    self._pending_session_data = restore_result.session_data
                    print(f"✅ [LIFECYCLE] Session data loaded for later restoration")
                    print(
                        f"🔍 [LIFECYCLE] Session contains sequence: {self._pending_session_data.current_sequence_id}"
                    )
                    print(
                        f"🔍 [LIFECYCLE] Selected beat: {self._pending_session_data.selected_beat_index}"
                    )
                    print(
                        f"🔍 [LIFECYCLE] Active tab: {self._pending_session_data.active_tab}"
                    )
                    print(
                        "🔍 [LIFECYCLE] Session restoration will be triggered after UI setup"
                    )
                else:
                    print("ℹ️ [LIFECYCLE] No previous session to restore")
                    if restore_result.warnings:
                        for warning in restore_result.warnings:
                            print(f"⚠️ [LIFECYCLE] Session warning: {warning}")
            except Exception as e:
                print(f"⚠️ [LIFECYCLE] Failed to restore session: {e}")
                import traceback

                traceback.print_exc()
                # Continue without session restoration
        else:
            print("⚠️ [LIFECYCLE] No session service available for restoration")

        if progress_callback:
            progress_callback(90, "Session restoration complete")

        if progress_callback:
            progress_callback(95, "Application lifecycle initialized")

    def trigger_deferred_session_restoration(self):
        """Trigger session restoration after UI components are ready."""
        if self._pending_session_data:
            print("🔍 [LIFECYCLE] Triggering deferred session restoration...")
            print(f"🔍 [LIFECYCLE] UI components should now be ready to receive events")
            self._apply_restored_session_to_ui(self._pending_session_data)
            self._pending_session_data = None  # Clear after use
        else:
            print("ℹ️ [LIFECYCLE] No pending session data to restore")

    def _apply_restored_session_to_ui(self, session_data):
        """Apply restored session data to UI components."""
        print("🔍 [LIFECYCLE] Starting UI restoration process...")
        try:
            from core.events.event_bus import get_event_bus, UIEvent, EventPriority

            # Get event bus for publishing restoration events
            event_bus = get_event_bus()
            print("🔍 [LIFECYCLE] Event bus obtained successfully")

            # Restore sequence if available
            if session_data.current_sequence_id and session_data.current_sequence_data:
                print(
                    f"🔄 [LIFECYCLE] Restoring sequence: {session_data.current_sequence_id}"
                )
                print(
                    f"🔍 [LIFECYCLE] Sequence data type: {type(session_data.current_sequence_data)}"
                )

                # Convert sequence data back to SequenceData object if needed
                sequence_data = session_data.current_sequence_data
                if isinstance(sequence_data, dict):
                    print("🔍 [LIFECYCLE] Converting dict to SequenceData object...")
                    from domain.models.core_models import SequenceData, BeatData

                    beats_data = sequence_data.get("beats", [])
                    print(f"🔍 [LIFECYCLE] Sequence has {len(beats_data)} beats")

                    # Convert beat dicts back to BeatData objects
                    beat_objects = []
                    for i, beat_dict in enumerate(beats_data):
                        if isinstance(beat_dict, dict):
                            print(
                                f"🔍 [LIFECYCLE] Converting beat {i}: {beat_dict.get('letter', 'Unknown')}"
                            )
                            beat_obj = BeatData.from_dict(beat_dict)
                            beat_objects.append(beat_obj)
                        else:
                            print(
                                f"⚠️ [LIFECYCLE] Beat {i} is not a dict: {type(beat_dict)}"
                            )
                            beat_objects.append(beat_dict)

                    print(f"🔍 [LIFECYCLE] Converted {len(beat_objects)} beat objects")

                    # Convert dict back to SequenceData object
                    sequence_data = SequenceData(
                        id=sequence_data.get("id", session_data.current_sequence_id),
                        name=sequence_data.get("name", "Restored Sequence"),
                        beats=beat_objects,
                    )
                    print(
                        f"🔍 [LIFECYCLE] Created SequenceData: {sequence_data.name} (ID: {sequence_data.id})"
                    )
                    
                    # CRITICAL FIX: Recalculate sequence name from beat letters exactly like legacy
                    if beat_objects:
                        calculated_word = self._calculate_sequence_word_from_beats(beat_objects)
                        sequence_data = sequence_data.update(name=calculated_word)
                        print(f"✅ [LIFECYCLE] Recalculated sequence name: '{calculated_word}'")
                    else:
                        print("ℹ️ [LIFECYCLE] No beats to calculate name from")
                else:
                    print(
                        f"🔍 [LIFECYCLE] Sequence data is already SequenceData object: {sequence_data.name}"
                    )
                    
                    # CRITICAL FIX: Also recalculate name for existing SequenceData objects
                    if sequence_data.beats:
                        calculated_word = self._calculate_sequence_word_from_beats(sequence_data.beats)
                        sequence_data = sequence_data.update(name=calculated_word)
                        print(f"✅ [LIFECYCLE] Recalculated existing sequence name: '{calculated_word}'")
                    else:
                        print("ℹ️ [LIFECYCLE] No beats in existing sequence to calculate name from")

                # Publish sequence restoration event
                print("🔍 [LIFECYCLE] Publishing sequence restoration event...")
                event = UIEvent(
                    component="session_restoration",
                    action="sequence_restored",
                    state_data={
                        "sequence_data": sequence_data,
                        "sequence_id": session_data.current_sequence_id,
                        "selected_beat_index": session_data.selected_beat_index,
                        "start_position_data": session_data.start_position_data,
                    },
                    source="application_lifecycle_manager",
                    priority=EventPriority.HIGH,
                )
                event_bus.publish(event)
                print(
                    f"✅ [LIFECYCLE] Published sequence restoration event for: {session_data.current_sequence_id}"
                )
            else:
                print("ℹ️ [LIFECYCLE] No sequence data to restore")
                if not session_data.current_sequence_id:
                    print("🔍 [LIFECYCLE] No sequence ID in session")
                if not session_data.current_sequence_data:
                    print("🔍 [LIFECYCLE] No sequence data in session")

            # Restore UI state
            if session_data.active_tab:
                print(f"🔄 Restoring active tab: {session_data.active_tab}")
                event = UIEvent(
                    component="session_restoration",
                    action="tab_restored",
                    state_data={"active_tab": session_data.active_tab},
                    source="application_lifecycle_manager",
                    priority=EventPriority.HIGH,
                )
                event_bus.publish(event)

        except Exception as e:
            print(f"⚠️ Failed to apply restored session to UI: {e}")
            import traceback

            traceback.print_exc()

    def set_window_dimensions(
        self,
        main_window: QMainWindow,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
    ) -> None:
        """Set window dimensions using modern responsive design: 90% of screen size."""
        # Check for parallel testing mode first
        if parallel_mode and parallel_geometry:
            try:
                x, y, width, height = map(int, parallel_geometry.split(","))
                main_window.setGeometry(x, y, width, height)
                main_window.setMinimumSize(1400, 900)
                print(f"🔄 Modern positioned at: {x},{y} ({width}x{height})")
                return
            except Exception as e:
                print(f"⚠️ Failed to apply parallel testing geometry: {e}")
                # Fall through to normal positioning

        # Use target screen for consistent positioning
        screen = target_screen or QGuiApplication.primaryScreen()

        if not screen:
            main_window.setGeometry(100, 100, 1400, 900)
            main_window.setMinimumSize(1400, 900)
            return

        # Calculate responsive dimensions (90% of screen)
        available_geometry = screen.availableGeometry()
        window_width = int(available_geometry.width() * 0.9)
        window_height = int(available_geometry.height() * 0.9)
        x = available_geometry.x() + int(
            (available_geometry.width() - window_width) / 2
        )
        y = available_geometry.y() + int(
            (available_geometry.height() - window_height) / 2
        )

        main_window.setGeometry(x, y, window_width, window_height)
        main_window.setMinimumSize(1400, 900)

    def detect_parallel_testing_mode(self) -> Tuple[bool, str, str]:
        """Detect if we're running in parallel testing mode."""
        import argparse
        import os

        # Check command line arguments
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--parallel-testing", action="store_true")
        parser.add_argument(
            "--monitor", choices=["primary", "secondary", "left", "right"]
        )
        args, _ = parser.parse_known_args()

        # Check environment variables
        env_parallel = os.environ.get("TKA_PARALLEL_TESTING", "").lower() == "true"
        env_monitor = os.environ.get("TKA_PARALLEL_MONITOR", "")
        env_geometry = os.environ.get("TKA_PARALLEL_GEOMETRY", "")

        parallel_mode = args.parallel_testing or env_parallel
        monitor = args.monitor or env_monitor

        if parallel_mode:
            print(f"🔄 Modern Parallel Testing Mode: {monitor} monitor")
            if env_geometry:
                print(f"   📐 Target geometry: {env_geometry}")

        return parallel_mode, monitor, env_geometry

    def determine_target_screen(self, parallel_mode=False, monitor=""):
        """Determine target screen for application placement."""
        screens = QGuiApplication.screens()

        # Override screen selection for parallel testing
        if parallel_mode and len(screens) > 1:
            if monitor in ["secondary", "right"]:
                # Determine which screen is physically on the right
                primary_screen = screens[0]
                secondary_screen = screens[1]

                # If secondary has higher X coordinate, it's on the right
                if secondary_screen.geometry().x() > primary_screen.geometry().x():
                    target_screen = secondary_screen
                    print(
                        f"🔄 Modern forced to RIGHT monitor (secondary) for parallel testing"
                    )
                else:
                    target_screen = primary_screen
                    print(
                        f"🔄 Modern forced to RIGHT monitor (primary) for parallel testing"
                    )

            elif monitor in ["primary", "left"]:
                # Determine which screen is physically on the left
                primary_screen = screens[0]
                secondary_screen = screens[1]

                # If secondary has lower X coordinate, it's on the left
                if secondary_screen.geometry().x() < primary_screen.geometry().x():
                    target_screen = secondary_screen
                    print(
                        f"🔄 Modern forced to LEFT monitor (secondary) for parallel testing"
                    )
                else:
                    target_screen = primary_screen
                    print(
                        f"🔄 Modern forced to LEFT monitor (primary) for parallel testing"
                    )
            else:
                target_screen = screens[1]  # Default to secondary
        else:
            # Normal behavior: prefer secondary monitor if available
            target_screen = (
                screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
            )

        return target_screen

    def start_api_server(self, enable_api=True) -> bool:
        """Start the API server if dependencies are available."""
        if not enable_api:
            print("🚫 API server is disabled")
            return False

        try:
            from infrastructure.api.integration import start_api_server
            import platform

            # Enhanced logging for Windows
            if platform.system() == "Windows":
                print("🪟 Starting API server on Windows...")
                print("   Note: Some ports may require administrator privileges")

            # Start API server
            success = start_api_server(enabled=enable_api, auto_port=True)

            if success:
                print("🌐 TKA API server started successfully")
                from infrastructure.api.integration import get_api_integration

                api = get_api_integration()
                server_url = api.get_server_url()
                docs_url = api.get_docs_url()
                if server_url:
                    print(f"   📍 Server: {server_url}")
                if docs_url:
                    print(f"   📚 Docs: {docs_url}")
                return True
            else:
                print("⚠️ API server startup failed - continuing without API")
                return False

        except ImportError as e:
            print(f"⚠️ API server dependencies not available: {e}")
            print("   To enable API features: pip install fastapi uvicorn")
            print("   Continuing without API server...")
            return False
        except PermissionError as e:
            print(f"⚠️ Windows permission error for API server: {e}")
            print("   Possible solutions:")
            print("   1. Run as administrator")
            print("   2. Check Windows Firewall/Antivirus settings")
            print("   3. The application will continue without API server")
            return False
        except OSError as e:
            if "10013" in str(e):  # Windows socket permission error
                print(f"⚠️ Windows socket permission error: {e}")
                print("   This is a common Windows security restriction")
                print("   The application will continue without API server")
            else:
                print(f"⚠️ Network error starting API server: {e}")
                print("   Continuing without API server...")
            return False
        except Exception as e:
            print(f"⚠️ Unexpected error starting API server: {e}")
            print("   This does not affect the main application functionality")
            print("   Continuing without API server...")
            return False

    def get_application_info(self) -> dict:
        """Get application information and status."""
        return {
            "title": "🚀 Kinetic Constructor",
            "version": "Modern",
            "api_enabled": self.api_enabled,
            "minimum_size": (1400, 900),
            "responsive_sizing": True,
        }

    def validate_screen_configuration(self) -> dict:
        """Validate screen configuration and return status."""
        screens = QGuiApplication.screens()
        primary_screen = QGuiApplication.primaryScreen()

        return {
            "screen_count": len(screens),
            "primary_screen_available": primary_screen is not None,
            "multi_monitor_support": len(screens) > 1,
            "screen_geometries": [
                {
                    "index": i,
                    "geometry": screen.geometry(),
                    "available_geometry": screen.availableGeometry(),
                }
                for i, screen in enumerate(screens)
            ],
        }

    def cleanup_application(self) -> None:
        """Clean up application and save session state."""
        # NEW: Save current session state before cleanup
        if self._session_service:
            try:
                success = self._session_service.save_session_state()
                if success:
                    print("✅ Session state saved successfully")
                else:
                    print("⚠️ Failed to save session state")
            except Exception as e:
                print(f"⚠️ Failed to save session state: {e}")

        # Additional cleanup can be added here as needed
        print("🧹 Application cleanup completed")

    def set_session_service(self, session_service: ISessionStateService) -> None:
        """Set the session service for lifecycle integration."""
        self._session_service = session_service

    def _calculate_sequence_word_from_beats(self, beat_objects) -> str:
        """Calculate sequence word from beat letters exactly like legacy SequencePropertiesManager"""
        if not beat_objects:
            return ""
            
        # Extract letters from beats exactly like legacy calculate_word method
        word = "".join(beat.letter for beat in beat_objects if hasattr(beat, 'letter'))
        
        # Apply word simplification for circular sequences like legacy
        return self._simplify_repeated_word(word)
    
    def _simplify_repeated_word(self, word: str) -> str:
        """Simplify repeated patterns exactly like legacy WordSimplifier"""
        def can_form_by_repeating(s: str, pattern: str) -> bool:
            pattern_len = len(pattern)
            return all(
                s[i : i + pattern_len] == pattern for i in range(0, len(s), pattern_len)
            )

        n = len(word)
        for i in range(1, n // 2 + 1):
            pattern = word[:i]
            if n % i == 0 and can_form_by_repeating(word, pattern):
                return pattern
        return word
