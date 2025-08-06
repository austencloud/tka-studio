"""
Core Testing Module for TKA

Provides comprehensive testing utilities including:
- AI agent testing helpers
- UI component testing framework
- CLI testing interface
- Test runners for integration
"""

from __future__ import annotations

from .ai_agent_helpers import (
    AITestResult,
    TKAAITestHelper,
    ai_test_pictograph_workflow,
    ai_test_sequence_workflow,
    ai_test_tka_comprehensive,
)
from .button_tester import ButtonTester
from .component_initializer import ComponentInitializer
from .graph_editor_tester import GraphEditorTester
from .simple_ui_tester import SimpleUITester
from .ui_test_runner import (
    UITestRunner,
    full_ui_test,
    quick_ui_test,
    test_buttons_only,
    test_graph_editor_only,
)


__all__ = [
    "AITestResult",
    "ButtonTester",
    "ComponentInitializer",
    "GraphEditorTester",
    "SimpleUITester",
    "TKAAITestHelper",
    "UITestRunner",
    "ai_test_pictograph_workflow",
    "ai_test_sequence_workflow",
    "ai_test_tka_comprehensive",
    "full_ui_test",
    "quick_ui_test",
    "test_buttons_only",
    "test_graph_editor_only",
]
