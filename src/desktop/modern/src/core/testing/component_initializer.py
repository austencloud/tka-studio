"""
Simple UI Testing Framework - Chunk 2: Component Initialization

Initializes workbench and graph editor with real data.
"""
from __future__ import annotations

from desktop.modern.domain.models.sequence_data import SequenceData


class ComponentInitializer:
    """Handles initialization of UI components for testing."""

    @staticmethod
    def initialize_workbench_and_graph_editor(container, sequence_data: SequenceData):
        """Initialize workbench and graph editor with real data."""
        print("🔧 Initializing workbench and graph editor with real data...")

        try:
            # Get services from container
            from desktop.modern.core.interfaces.core_services import ILayoutService
            from desktop.modern.core.interfaces.workbench_services import (
                IBeatDeletionService,
                IDictionaryService,
                IFullScreenViewer,
                IGraphEditorService,
                ISequenceWorkbenchService,
            )

            layout_service = container.resolve(ILayoutService)
            workbench_service = container.resolve(ISequenceWorkbenchService)
            fullscreen_service = container.resolve(IFullScreenViewer)
            deletion_service = container.resolve(IBeatDeletionService)
            graph_service = container.resolve(IGraphEditorService)
            dictionary_service = container.resolve(IDictionaryService)

            # Create workbench
            from desktop.modern.presentation.components.workbench.workbench import (
                SequenceWorkbench,
            )

            workbench = SequenceWorkbench(
                layout_service=layout_service,
                workbench_service=workbench_service,
                fullscreen_service=fullscreen_service,
                deletion_service=deletion_service,
                graph_service=graph_service,
                dictionary_service=dictionary_service,
            )

            # Create graph editor
            from desktop.modern.presentation.components.graph_editor.graph_editor import (
                GraphEditor,
            )

            graph_editor = GraphEditor(
                graph_service=graph_service,
                parent=workbench,
                workbench_width=800,
                workbench_height=600,
            )

            # Set real data
            workbench.set_sequence(sequence_data)
            graph_editor.set_sequence(sequence_data)

            print(f"✅ Components initialized with {len(sequence_data.beats)} beats")
            return workbench, graph_editor

        except Exception as e:
            print(f"❌ Failed to initialize components: {e}")
            # Return None components to indicate failure
            return None, None

    @staticmethod
    def get_workbench_button_references(workbench) -> dict:
        """Get references to all workbench buttons for testing."""
        if not workbench:
            return {}

        try:
            # Map of button names to their widget references
            button_map = {
                "add_to_dictionary": getattr(
                    workbench, "add_to_dictionary_button", None
                ),
                "delete_beat": getattr(workbench, "delete_beat_button", None),
                "clone_beat": getattr(workbench, "clone_beat_button", None),
                "mirror_beat": getattr(workbench, "mirror_beat_button", None),
                "rotate_beat": getattr(workbench, "rotate_beat_button", None),
                "reset_beat": getattr(workbench, "reset_beat_button", None),
                "generate_beat": getattr(workbench, "generate_beat_button", None),
                "add_beat": getattr(workbench, "add_beat_button", None),
                "export_image": getattr(workbench, "export_image_button", None),
                "fullscreen": getattr(workbench, "fullscreen_button", None),
                "settings": getattr(workbench, "settings_button", None),
            }

            # Filter out None values
            valid_buttons = {
                name: button
                for name, button in button_map.items()
                if button is not None
            }

            print(
                f"📋 Found {len(valid_buttons)} workbench buttons: {list(valid_buttons.keys())}"
            )
            return valid_buttons

        except Exception as e:
            print(f"❌ Error getting button references: {e}")
            return {}

    @staticmethod
    def get_graph_editor_controls(graph_editor) -> dict:
        """Get references to all graph editor controls for testing."""
        if not graph_editor:
            return {}

        try:
            # Map of control names to their widget references
            control_map = {
                "turn_adjustment_left": getattr(
                    graph_editor, "turn_adjustment_left_button", None
                ),
                "turn_adjustment_right": getattr(
                    graph_editor, "turn_adjustment_right_button", None
                ),
                "orientation_picker": getattr(graph_editor, "orientation_picker", None),
                "prop_rotation_controls": getattr(
                    graph_editor, "prop_rotation_controls", None
                ),
                "grid_mode_selector": getattr(graph_editor, "grid_mode_selector", None),
            }

            # Filter out None values
            valid_controls = {
                name: control
                for name, control in control_map.items()
                if control is not None
            }

            print(
                f"📋 Found {len(valid_controls)} graph editor controls: {list(valid_controls.keys())}"
            )
            return valid_controls

        except Exception as e:
            print(f"❌ Error getting control references: {e}")
            return {}
