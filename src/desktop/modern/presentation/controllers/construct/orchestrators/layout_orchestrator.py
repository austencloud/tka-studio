"""
LayoutOrchestrator

Coordinates the overall layout structure and component organization.
This is Qt-agnostic and focuses on coordination logic.
"""

from __future__ import annotations


class LayoutOrchestrator:
    """
    Orchestrates the overall layout structure and component coordination.

    Responsibilities:
    - Defining layout structure and organization
    - Coordinating component initialization order
    - Managing component lifecycle
    - Providing high-level transition coordination
    """

    def __init__(self):
        self.components = {}
        self.initialization_order = [
            "workbench",
            "start_position_picker",
            "option_picker",
            "graph_editor",
            "generate_controls",
            "export_panel",
        ]
        self.panel_tab_mapping = {
            0: 0,  # start_position_picker -> tab 0 (Build)
            1: 0,  # option_picker -> tab 0 (Build)
            2: 2,  # graph_editor (stack index 2) -> tab 2 (Edit)
            3: 1,  # generate_controls (stack index 3) -> tab 1 (Generate)
            4: 3,  # export_panel (stack index 4) -> tab 3 (Export)
        }

    def register_component(self, name: str, component):
        """Register a component with the orchestrator."""
        self.components[name] = component

    def get_component_dependencies(self, component_name: str) -> list[str]:
        """
        Get the dependencies for a specific component.

        Args:
            component_name: Name of the component

        Returns:
            List of dependency names
        """
        dependencies = {
            "workbench": [],
            "start_position_picker": [],
            "option_picker": [],
            "graph_editor": ["workbench"],
            "generate_controls": [],
        }

        return dependencies.get(component_name, [])
