from __future__ import annotations

from typing import TYPE_CHECKING

from base_widgets.pictograph.elements.views.beat_view import LegacyBeatView
from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat import Beat

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.temp_beat_frame.temp_beat_frame import (
        TempBeatFrame,
    )
    from main_window.main_widget.sequence_workbench.legacy_beat_frame.legacy_beat_frame import (
        LegacyBeatFrame,
    )

    from .image_export_manager import ImageExportManager


class ImageExportBeatFactory:
    def __init__(
        self,
        export_manager: "ImageExportManager",
        beat_frame_class: "LegacyBeatFrame" | "TempBeatFrame",
    ):
        self.export_manager = export_manager
        self.beat_frame_class = beat_frame_class

    def process_sequence_to_beats(self, sequence: list[dict]) -> list[LegacyBeatView]:
        temp_beat_frame = None

        if self.beat_frame_class.__name__ in [
            "SequenceBeatFrame",
            "LegacyBeatFrame",
            "SequenceWorkbenchBeatFrame",
        ]:
            temp_beat_frame = self.beat_frame_class(
                self.export_manager.main_widget.sequence_workbench
            )
        elif self.beat_frame_class.__name__ == "TempBeatFrame":
            # Get browse tab using the new coordinator pattern
            browse_tab = self._get_browse_tab()
            if browse_tab:
                temp_beat_frame = self.beat_frame_class(browse_tab)
            else:
                # Create TempBeatFrame directly without browse tab dependency
                print(
                    "DEBUG: Creating TempBeatFrame directly without browse tab dependency"
                )
                from main_window.main_widget.browse_tab.temp_beat_frame.temp_beat_frame import (
                    TempBeatFrame,
                )

                # Create TempBeatFrame with minimal required dependencies
                # Create a simple wrapper object that has main_widget attribute
                class BrowseTabWrapper:
                    def __init__(self, main_widget):
                        self.main_widget = main_widget

                browse_tab_wrapper = BrowseTabWrapper(self.export_manager.main_widget)
                temp_beat_frame = TempBeatFrame(browse_tab_wrapper)

        if temp_beat_frame is None:
            raise ValueError(
                f"Unsupported beat frame class: {self.beat_frame_class.__name__}"
            )

        filled_beats = []
        current_beat_number = 1

        for beat_data in sequence[2:]:
            if beat_data.get("is_placeholder"):
                continue

            duration = beat_data.get("duration", 1)

            beat_view = self.create_beat_view_from_data(
                beat_data, current_beat_number, temp_beat_frame
            )

            filled_beats.append(beat_view)

            current_beat_number += duration

        return filled_beats

    def _get_browse_tab(self):
        """Get the browse tab using the new coordinator pattern with graceful fallbacks."""
        main_widget = self.export_manager.main_widget

        # Debug: Print the main widget structure
        print(f"DEBUG: main_widget type: {type(main_widget)}")
        print(f"DEBUG: main_widget attributes: {dir(main_widget)}")

        try:
            # Try to get browse tab through the new coordinator pattern
            if hasattr(main_widget, "get_tab_widget"):
                # Debug: Check what tabs are available
                if hasattr(main_widget, "tab_manager") and hasattr(
                    main_widget.tab_manager, "tabs"
                ):
                    available_tabs = list(main_widget.tab_manager.tabs.keys())
                    print(f"DEBUG: Available tabs: {available_tabs}")
                else:
                    print("DEBUG: No tab_manager.tabs found")

                # Try to access tab_manager directly
                if hasattr(main_widget, "tab_manager"):
                    tab_manager = main_widget.tab_manager
                    print(f"DEBUG: tab_manager type: {type(tab_manager)}")
                    print(
                        f"DEBUG: tab_manager attributes: {[attr for attr in dir(tab_manager) if not attr.startswith('_')]}"
                    )

                browse_tab = main_widget.get_tab_widget("browse")
                print(f"DEBUG: get_tab_widget('browse') returned: {browse_tab}")

                # Try alternative tab names
                if browse_tab is None:
                    for tab_name in ["browse_tab", "Browse", "BROWSE"]:
                        alt_tab = main_widget.get_tab_widget(tab_name)
                        print(
                            f"DEBUG: get_tab_widget('{tab_name}') returned: {alt_tab}"
                        )
                        if alt_tab is not None:
                            return alt_tab

                return browse_tab
        except Exception as e:
            print(f"DEBUG: get_tab_widget failed: {e}")

        try:
            # Fallback: try through tab_manager for backward compatibility
            if hasattr(main_widget, "tab_manager"):
                tab_manager = main_widget.tab_manager
                print(f"DEBUG: tab_manager: {tab_manager}")
                if hasattr(tab_manager, "get_tab_widget"):
                    browse_tab = tab_manager.get_tab_widget("browse")
                    print(
                        f"DEBUG: tab_manager.get_tab_widget('browse') returned: {browse_tab}"
                    )
                    return browse_tab
        except Exception as e:
            print(f"DEBUG: tab_manager fallback failed: {e}")

        try:
            # Final fallback: try direct access for legacy compatibility
            if hasattr(main_widget, "browse_tab"):
                browse_tab = main_widget.browse_tab
                print(f"DEBUG: direct browse_tab access returned: {browse_tab}")
                return browse_tab
        except Exception as e:
            print(f"DEBUG: direct access failed: {e}")

        print("DEBUG: All browse tab access methods failed")
        return None

    def create_beat_view_from_data(self, beat_data, number, temp_beat_frame):
        new_beat_view = LegacyBeatView(temp_beat_frame)
        beat = Beat(temp_beat_frame)
        beat.state.pictograph_data = beat_data
        beat.managers.updater.update_pictograph(beat_data)
        new_beat_view.set_beat(beat, number)
        return new_beat_view
