"""
SequenceLoadingService

Handles sequence loading from persistence and startup restoration.
Responsible for loading sequences from current_sequence.json and managing startup workflows.
"""

from typing import Optional, Callable
from PyQt6.QtCore import QObject, pyqtSignal

from domain.models.core_models import SequenceData, BeatData
from application.services.core.sequence_persistence_service import (
    SequencePersistenceService,
)

from presentation.components.workbench.workbench import SequenceWorkbench


class SequenceLoadingService(QObject):
    """
    Service for loading sequences from persistence and handling startup restoration.

    Responsibilities:
    - Loading sequences from current_sequence.json
    - Converting legacy format to modern SequenceData
    - Managing startup sequence restoration
    - Coordinating with workbench for sequence loading
    """

    sequence_loaded = pyqtSignal(object)  # SequenceData object
    start_position_loaded = pyqtSignal(object, str)  # BeatData object, position_key

    def __init__(
        self,
        workbench_getter: Optional[Callable[[], SequenceWorkbench]] = None,
        workbench_setter: Optional[Callable[[SequenceData], None]] = None,
        data_converter: Optional[object] = None,
    ):
        super().__init__()
        self.workbench_getter = workbench_getter
        self.workbench_setter = workbench_setter
        self.data_converter = data_converter
        self.persistence_service = SequencePersistenceService()

    def load_sequence_on_startup(self):
        """Load sequence from current_sequence.json on startup - exactly like legacy"""
        try:
            # Load sequence from persistence
            sequence_data = self.persistence_service.load_current_sequence()

            if len(sequence_data) <= 1:
                print("ℹ️ [SEQUENCE_LOADING] Empty sequence detected on startup")
                # CRITICAL FIX: Always initialize start position component for empty sequences
                # This ensures the "START" text overlay is visible even when no sequence exists
                self._initialize_empty_sequence_start_position()
                return

            print(
                f"🔍 [SEQUENCE_LOADING] Loading sequence from current_sequence.json..."
            )
            print(f"🔍 [SEQUENCE_LOADING] Sequence has {len(sequence_data)} items")

            # Extract metadata and beats
            metadata = sequence_data[0]
            sequence_word = metadata.get("word", "")
            print(f"🔍 [SEQUENCE_LOADING] Sequence word: '{sequence_word}'")

            # Find start position (beat 0) and actual beats (beat 1+)
            start_position_data = None
            beats_data = []

            for item in sequence_data[1:]:
                if item.get("beat") == 0:
                    start_position_data = item
                    print(
                        f"✅ [SEQUENCE_LOADING] Found start position: {item.get('sequence_start_position', 'unknown')}"
                    )
                elif "letter" in item and not item.get("is_placeholder", False):
                    beats_data.append(item)
                    print(
                        f"✅ [SEQUENCE_LOADING] Found beat {item.get('beat', '?')}: {item.get('letter', '?')}"
                    )

            # Convert beats to modern format with full pictograph data
            beat_objects = []
            if self.data_converter:
                for i, beat_dict in enumerate(beats_data):
                    try:
                        # Convert legacy format back to modern BeatData with full data
                        beat_obj = self.data_converter.convert_legacy_to_beat_data(
                            beat_dict, i + 1
                        )
                        beat_objects.append(beat_obj)
                        print(
                            f"✅ [SEQUENCE_LOADING] Converted beat {beat_obj.letter} with motion data"
                        )
                    except Exception as e:
                        print(
                            f"⚠️ [SEQUENCE_LOADING] Failed to convert beat {beat_dict.get('letter', '?')}: {e}"
                        )
                        # Create fallback beat with proper numbering
                        fallback_beat = BeatData.empty().update(
                            letter=beat_dict.get("letter", "?"),
                            beat_number=i + 1,  # Sequential numbering
                            duration=beat_dict.get("duration", 1.0),
                        )
                        beat_objects.append(fallback_beat)

            # CRITICAL FIX: Handle start position loading INDEPENDENTLY of beats
            # This ensures start positions are visible even when there are no beats
            if start_position_data:
                try:
                    # Extract the position key from the start position data
                    position_key = start_position_data.get(
                        "sequence_start_position", "alpha"
                    )
                    end_pos = start_position_data.get("end_pos", "alpha1")

                    print(
                        f"🎯 [SEQUENCE_LOADING] Loading start position: {position_key} -> {end_pos}"
                    )

                    # Create start position BeatData from the saved data
                    if self.data_converter:
                        start_position_beat = self.data_converter.convert_legacy_start_position_to_beat_data(
                            start_position_data
                        )

                        # Set start position directly in workbench (don't trigger selection flow)
                        workbench = self.workbench_getter()
                        if workbench and hasattr(workbench, "set_start_position"):
                            workbench.set_start_position(start_position_beat)
                            print(
                                f"✅ [SEQUENCE_LOADING] Start position loaded into workbench: {end_pos}"
                            )

                            # Emit signal for UI coordination with position key
                            self.start_position_loaded.emit(
                                start_position_beat, position_key
                            )
                        else:
                            print(
                                f"⚠️ [SEQUENCE_LOADING] Workbench doesn't have set_start_position method"
                            )

                except Exception as e:
                    print(f"⚠️ [SEQUENCE_LOADING] Failed to load start position: {e}")
                    import traceback

                    traceback.print_exc()

            # Create and set the sequence (even if empty, to maintain state)
            loaded_sequence = SequenceData(
                id="loaded_sequence",
                name=sequence_word or "Loaded Sequence",
                beats=beat_objects,  # May be empty, that's fine
            )

            print(
                f"✅ [SEQUENCE_LOADING] Created sequence: '{loaded_sequence.name}' with {len(beat_objects)} beats"
            )

            # Set sequence in workbench
            if self.workbench_setter:
                self.workbench_setter(loaded_sequence)
                print(f"✅ [SEQUENCE_LOADING] Sequence loaded into workbench")

            # Emit signal for UI coordination
            self.sequence_loaded.emit(loaded_sequence)

            # Handle UI state transition based on what was loaded
            if start_position_data and not beat_objects:
                print(
                    "🎯 [SEQUENCE_LOADING] Start position loaded with no beats - should show option picker"
                )
            elif not start_position_data and not beat_objects:
                print(
                    "ℹ️ [SEQUENCE_LOADING] No start position or beats found - empty sequence"
                )

        except Exception as e:
            print(f"❌ [SEQUENCE_LOADING] Failed to load sequence on startup: {e}")
            import traceback

            traceback.print_exc()

    def _initialize_empty_sequence_start_position(self):
        """Initialize start position component for empty sequences"""
        try:
            print(
                "🔧 [SEQUENCE_LOADING] Initializing start position for empty sequence"
            )

            # Get workbench to initialize start position component
            if self.workbench_getter:
                workbench = self.workbench_getter()
                if workbench and hasattr(workbench, "_beat_frame_section"):
                    beat_frame_section = workbench._beat_frame_section
                    if beat_frame_section and hasattr(
                        beat_frame_section, "initialize_cleared_start_position"
                    ):
                        beat_frame_section.initialize_cleared_start_position()
                        print(
                            "✅ [SEQUENCE_LOADING] Start position component initialized for empty sequence"
                        )
                    else:
                        print(
                            "⚠️ [SEQUENCE_LOADING] Beat frame section not available for start position initialization"
                        )
                else:
                    print(
                        "⚠️ [SEQUENCE_LOADING] Workbench not available for start position initialization"
                    )
            else:
                print(
                    "⚠️ [SEQUENCE_LOADING] No workbench getter available for start position initialization"
                )

        except Exception as e:
            print(
                f"❌ [SEQUENCE_LOADING] Failed to initialize empty sequence start position: {e}"
            )
            import traceback

            traceback.print_exc()

    def get_current_sequence_from_workbench(self) -> Optional[SequenceData]:
        """Get the current sequence from workbench"""
        if self.workbench_getter:
            try:
                workbench = self.workbench_getter()
                if workbench and hasattr(workbench, "get_sequence"):
                    return workbench.get_sequence()
            except Exception as e:
                print(f"❌ Error getting current sequence: {e}")
        return None
