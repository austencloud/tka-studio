"""
LayoutOrchestrator

Coordinates the overall layout structure and component organization.
This is Qt-agnostic and focuses on coordination logic.
"""


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

    def get_component(self, name: str):
        """Get a registered component."""
        return self.components.get(name)

    def get_initialization_order(self) -> list[str]:
        """Get the order in which components should be initialized."""
        return self.initialization_order.copy()

    def get_tab_for_panel(self, panel_index: int) -> int:
        """Get the tab index that should be active for a given panel."""
        return self.panel_tab_mapping.get(panel_index, 0)

    def should_allow_transition(self, from_index: int, to_index: int) -> bool:
        """
        Determine if a transition between panels should be allowed.

        Args:
            from_index: Current panel index
            to_index: Target panel index

        Returns:
            True if transition should be allowed, False otherwise
        """
        # For now, allow all transitions
        # This could be extended to include business logic
        return from_index != to_index

    def get_transition_preparation_steps(self, target_panel: int) -> list[str]:
        """
        Get the steps needed to prepare for a transition to the target panel.

        Args:
            target_panel: Index of the target panel

        Returns:
            List of preparation steps
        """
        steps = []

        if target_panel == 0:  # start_position_picker
            steps.append("prepare_start_position_picker")
        elif target_panel == 1:  # option_picker
            steps.append("prepare_option_picker")
        elif target_panel == 2:  # graph_editor
            steps.append("prepare_graph_editor")
        elif target_panel == 3:  # generate_controls
            steps.append("prepare_generate_controls")

        return steps

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

    def validate_component_setup(self) -> tuple[bool, list[str]]:
        """
        Validate that all required components are properly set up.

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        # Check that all required components are registered
        required_components = self.initialization_order
        for component_name in required_components:
            if component_name not in self.components:
                issues.append(f"Missing required component: {component_name}")
                continue

            component = self.components[component_name]
            if component is None:
                issues.append(f"Component {component_name} is None")

        # Check dependencies
        for component_name, component in self.components.items():
            if component is None:
                continue

            dependencies = self.get_component_dependencies(component_name)
            for dep in dependencies:
                if dep not in self.components or self.components[dep] is None:
                    issues.append(
                        f"Component {component_name} missing dependency: {dep}"
                    )

        return len(issues) == 0, issues

    def get_panel_configuration(self) -> dict:
        """
        Get the configuration for all panels.

        Returns:
            Dictionary containing panel configuration
        """
        return {
            "panels": [
                {
                    "index": 0,
                    "name": "start_position_picker",
                    "tab": 0,
                    "component": "start_position_picker",
                },
                {
                    "index": 1,
                    "name": "option_picker",
                    "tab": 0,
                    "component": "option_picker",
                },
                {
                    "index": 2,
                    "name": "graph_editor",
                    "tab": 1,
                    "component": "graph_editor",
                },
                {
                    "index": 3,
                    "name": "generate_controls",
                    "tab": 2,
                    "component": "generate_controls",
                },
            ],
            "default_panel": 0,
            "layout_type": "horizontal_split",
        }
