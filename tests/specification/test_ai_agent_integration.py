"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Ensure AI agents can effectively test TKA workflows using existing architecture
PERMANENT: AI agent testing must work with our sophisticated domain models and services
AUTHOR: @ai-integration
"""

import pytest
from core.testing.ai_agent_helpers import (
    TKAAITestHelper,
    ai_test_pictograph_workflow,
    ai_test_sequence_workflow,
    ai_test_tka_comprehensive,
)


@pytest.mark.specification
@pytest.mark.critical
class TestAIAgentIntegrationContract:
    """Permanent AI agent integration contract - NEVER DELETE"""

    def test_ai_helper_initialization_contract(self):
        """PERMANENT: AI helper must initialize with test services"""
        helper = TKAAITestHelper(use_test_mode=True)

        # Contract: Must be able to resolve core services
        assert helper.sequence_service is not None
        assert helper.pictograph_service is not None
        assert helper.validation_service is not None

    def test_sequence_creation_contract(self):
        """PERMANENT: AI agents must be able to create sequences using real services"""
        helper = TKAAITestHelper()
        result = helper.create_sequence("AI Test", 4)

        # Contract: Must succeed with valid input
        assert result.success == True
        assert result.data is not None
        assert result.metadata["sequence_name"] == "AI Test"
        assert result.metadata["beat_count"] == 4

        # Contract: Result must contain sequence data (dict or SequenceData)
        assert result.data is not None
        assert "id" in result.data
        assert "name" in result.data

    def test_beat_creation_contract(self):
        """PERMANENT: AI agents must be able to create beats with motion data"""
        helper = TKAAITestHelper()
        result = helper.create_beat_with_motions(1, "A")

        # Contract: Must succeed with valid motion data
        assert result.success == True
        assert result.data is not None
        assert result.metadata["has_blue_motion"] == True
        assert result.metadata["has_red_motion"] == True

        # Contract: Result must contain actual BeatData
        from domain.models.beat_data import BeatData

        assert isinstance(result.data, BeatData)

    def test_existing_command_pattern_contract(self):
        """PERMANENT: AI agents must be able to use existing command pattern"""
        helper = TKAAITestHelper()
        result = helper.test_existing_command_pattern()

        # Contract: Must work regardless of command pattern availability
        assert result.success == True
        assert result.data is not None

        # Contract: Must indicate command pattern availability
        assert "command_pattern_available" in result.metadata

    def test_comprehensive_test_suite_contract(self):
        """PERMANENT: AI agents must be able to run full architecture tests"""
        helper = TKAAITestHelper()
        result = helper.run_comprehensive_test_suite()

        # Contract: Must test all major components
        assert result.data is not None
        test_breakdown = result.metadata.get("test_breakdown", {})

        expected_tests = [
            "sequence_creation",
            "beat_creation",
            "command_pattern",
            "pictograph_creation",
            "pictograph_from_beat",
            "csv_dataset",
        ]

        for test_name in expected_tests:
            assert test_name in test_breakdown

    def test_convenience_functions_contract(self):
        """PERMANENT: AI agents must have simple one-line test functions"""
        # Contract: Convenience functions must work
        result1 = ai_test_tka_comprehensive()
        assert "overall_success" in result1
        assert "test_breakdown" in result1

        result2 = ai_test_sequence_workflow()
        assert "success" in result2

        result3 = ai_test_pictograph_workflow()
        assert "success" in result3


@pytest.mark.specification
class TestAIAgentWorkflowContract:
    """Permanent AI agent workflow contract - NEVER DELETE"""

    def test_error_handling_contract(self):
        """PERMANENT: AI helpers must handle errors gracefully"""
        helper = TKAAITestHelper()

        # Test with invalid input
        result = helper.create_sequence("", 0)  # Invalid input

        # Contract: Must not crash and provide error information
        assert isinstance(result.success, bool)
        assert isinstance(result.errors, list)
        assert result.execution_time >= 0

    def test_execution_history_contract(self):
        """PERMANENT: AI helpers must track execution history"""
        helper = TKAAITestHelper()

        # Perform some operations
        helper.create_sequence("Test", 4)
        helper.create_beat_with_motions(1, "A")

        # Contract: Must track history
        summary = helper.get_execution_summary()
        assert summary["total_commands"] == 2
        assert "command_history" in summary
        assert len(summary["command_history"]) == 2
