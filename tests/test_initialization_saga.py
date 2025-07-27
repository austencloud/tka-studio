"""
Initialization Saga Unit Tests - Phase 1

Comprehensive validation of Saga pattern implementation for
transactional component initialization with rollback capabilities.
"""

import pytest
from unittest.mock import Mock, AsyncMock, MagicMock
import asyncio
from typing import Dict, Any

from desktop.modern.presentation.tabs.construct.infrastructure.initialization_saga import (
    ConstructTabInitializationSaga,
    CreateWorkbenchStep,
    CreatePickersStep,
    SetupEventIntegrationStep,
    SagaContext,
    SagaStatus,
    SagaResult,
    ISagaStep,
    create_construct_tab_initialization_saga
)


class TestSagaContext:
    """Test suite for SagaContext."""
    
    def test_initialization(self):
        """Test saga context initialization."""
        context = SagaContext("test_saga_123")
        
        assert context.saga_id == "test_saga_123"
        assert context.status == SagaStatus.PENDING
        assert isinstance(context.shared_data, dict)
        assert len(context.shared_data) == 0
        assert isinstance(context.completed_steps, list)
        assert len(context.completed_steps) == 0
    
    def test_shared_data_management(self):
        """Test shared data management."""
        context = SagaContext("test")
        
        # Add data
        context.shared_data["workbench"] = Mock()
        context.shared_data["config"] = {"setting": "value"}
        
        assert "workbench" in context.shared_data
        assert context.shared_data["config"]["setting"] == "value"
    
    def test_step_tracking(self):
        """Test completed steps tracking."""
        context = SagaContext("test")
        
        context.completed_steps.append("step1")
        context.completed_steps.append("step2")
        
        assert len(context.completed_steps) == 2
        assert "step1" in context.completed_steps
        assert "step2" in context.completed_steps


class TestSagaResult:
    """Test suite for SagaResult."""
    
    def test_successful_result(self):
        """Test successful saga result."""
        result = SagaResult(success=True, message="Operation completed")
        
        assert result.success is True
        assert result.message == "Operation completed"
        assert result.error_message is None
        assert result.compensation_data is None
    
    def test_failed_result(self):
        """Test failed saga result."""
        compensation_data = {"rollback": "data"}
        result = SagaResult(
            success=False, 
            error_message="Step failed",
            compensation_data=compensation_data
        )
        
        assert result.success is False
        assert result.error_message == "Step failed"
        assert result.compensation_data == compensation_data


class TestCreateWorkbenchStep:
    """Test suite for CreateWorkbenchStep."""
    
    @pytest.fixture
    def mock_factory(self):
        """Create mock resilient panel factory."""
        factory = Mock()
        return factory
    
    @pytest.fixture
    def mock_container(self):
        """Create mock DI container."""
        return Mock()
    
    @pytest.fixture
    def workbench_step(self, mock_factory, mock_container):
        """Create workbench creation step."""
        return CreateWorkbenchStep(mock_factory, mock_container)
    
    @pytest.mark.asyncio
    async def test_successful_execution(self, workbench_step, mock_factory):
        """Test successful workbench creation."""
        mock_panel = Mock()
        mock_workbench = Mock()
        mock_factory.create_workbench_panel.return_value = (mock_panel, mock_workbench)
        
        context = SagaContext("test")
        
        result = await workbench_step.execute(context)
        
        assert result.success is True
        assert "workbench_panel" in context.shared_data
        assert "workbench_component" in context.shared_data
        assert context.shared_data["workbench_component"] is mock_workbench
        assert mock_factory.create_workbench_panel.called
    
    @pytest.mark.asyncio
    async def test_failed_execution(self, workbench_step, mock_factory):
        """Test failed workbench creation."""
        mock_factory.create_workbench_panel.side_effect = Exception("Creation failed")
        
        context = SagaContext("test")
        
        result = await workbench_step.execute(context)
        
        assert result.success is False
        assert "Creation failed" in result.error_message
        assert "workbench_panel" not in context.shared_data
        assert "workbench_component" not in context.shared_data
    
    @pytest.mark.asyncio
    async def test_compensation(self, workbench_step):
        """Test workbench step compensation."""
        mock_workbench = Mock()
        mock_workbench.cleanup = Mock()
        mock_panel = Mock()
        mock_panel.cleanup = Mock()
        
        context = SagaContext("test")
        context.shared_data["workbench_component"] = mock_workbench
        context.shared_data["workbench_panel"] = mock_panel
        
        result = await workbench_step.compensate(context)
        
        assert result.success is True
        assert mock_workbench.cleanup.called
        assert "workbench_component" not in context.shared_data
        assert "workbench_panel" not in context.shared_data
    
    @pytest.mark.asyncio
    async def test_compensation_with_missing_data(self, workbench_step):
        """Test compensation when workbench data is missing."""
        context = SagaContext("test")
        # No workbench data in context
        
        result = await workbench_step.compensate(context)
        
        # Should succeed even with missing data
        assert result.success is True
    
    def test_step_identification(self, workbench_step):
        """Test step identification properties."""
        assert workbench_step.step_id == "create_workbench"
        assert "workbench" in workbench_step.description.lower()


class TestCreatePickersStep:
    """Test suite for CreatePickersStep."""
    
    @pytest.fixture
    def mock_factory(self):
        """Create mock resilient panel factory."""
        factory = Mock()
        return factory
    
    @pytest.fixture
    def mock_container(self):
        """Create mock DI container."""
        return Mock()
    
    @pytest.fixture
    def pickers_step(self, mock_factory, mock_container):
        """Create pickers creation step."""
        return CreatePickersStep(mock_factory, mock_container)
    
    @pytest.mark.asyncio
    async def test_successful_execution(self, pickers_step, mock_factory):
        """Test successful pickers creation."""
        # Mock start position picker
        mock_sp_panel = Mock()
        mock_sp_component = Mock()
        mock_factory.create_start_position_panel.return_value = (mock_sp_panel, mock_sp_component)
        
        # Mock option picker
        mock_op_panel = Mock()
        mock_op_component = Mock()
        mock_factory.create_option_picker_panel.return_value = (mock_op_panel, mock_op_component)
        
        context = SagaContext("test")
        
        result = await pickers_step.execute(context)
        
        assert result.success is True
        assert "start_position_picker_panel" in context.shared_data
        assert "start_position_picker_component" in context.shared_data
        assert "option_picker_panel" in context.shared_data
        assert "option_picker_component" in context.shared_data
        assert mock_factory.create_start_position_panel.called
        assert mock_factory.create_option_picker_panel.called
    
    @pytest.mark.asyncio
    async def test_partial_failure_compensation(self, pickers_step, mock_factory):
        """Test compensation when one picker creation fails."""
        # Start position picker succeeds
        mock_sp_panel = Mock()
        mock_sp_component = Mock()
        mock_factory.create_start_position_panel.return_value = (mock_sp_panel, mock_sp_component)
        
        # Option picker fails
        mock_factory.create_option_picker_panel.side_effect = Exception("Option picker failed")
        
        context = SagaContext("test")
        
        result = await pickers_step.execute(context)
        
        assert result.success is False
        assert "option picker failed" in result.error_message.lower()
        
        # Should have compensation data for start position picker
        assert result.compensation_data is not None
        assert "start_position_picker_component" in result.compensation_data
    
    @pytest.mark.asyncio
    async def test_compensation(self, pickers_step):
        """Test pickers step compensation."""
        mock_sp_component = Mock()
        mock_sp_component.cleanup = Mock()
        mock_op_component = Mock()
        mock_op_component.cleanup = Mock()
        
        context = SagaContext("test")
        context.shared_data.update({
            "start_position_picker_component": mock_sp_component,
            "option_picker_component": mock_op_component,
            "start_position_picker_panel": Mock(),
            "option_picker_panel": Mock(),
        })
        
        result = await pickers_step.compensate(context)
        
        assert result.success is True
        assert mock_sp_component.cleanup.called
        assert mock_op_component.cleanup.called
        
        # Data should be removed from context
        picker_keys = [
            "start_position_picker_component",
            "option_picker_component", 
            "start_position_picker_panel",
            "option_picker_panel"
        ]
        for key in picker_keys:
            assert key not in context.shared_data


class TestSetupEventIntegrationStep:
    """Test suite for SetupEventIntegrationStep."""
    
    @pytest.fixture
    def mock_event_integration(self):
        """Create mock event integration."""
        integration = Mock()
        integration.setup_event_handlers = Mock()
        integration.shutdown = Mock()
        return integration
    
    @pytest.fixture
    def integration_step(self, mock_event_integration):
        """Create event integration setup step."""
        return SetupEventIntegrationStep(mock_event_integration)
    
    @pytest.mark.asyncio
    async def test_successful_execution(self, integration_step, mock_event_integration):
        """Test successful event integration setup."""
        context = SagaContext("test")
        context.shared_data.update({
            "workbench_component": Mock(),
            "start_position_picker_component": Mock(),
            "option_picker_component": Mock(),
        })
        
        result = await integration_step.execute(context)
        
        assert result.success is True
        assert mock_event_integration.setup_event_handlers.called
        
        # Should pass components to event integration
        call_args = mock_event_integration.setup_event_handlers.call_args[0][0]
        assert "workbench" in call_args
        assert "start_position_picker" in call_args
        assert "option_picker" in call_args
    
    @pytest.mark.asyncio
    async def test_execution_with_missing_components(self, integration_step, mock_event_integration):
        """Test execution with missing components."""
        context = SagaContext("test")
        # Missing some components
        context.shared_data["workbench_component"] = Mock()
        
        result = await integration_step.execute(context)
        
        # Should still succeed but with limited components
        assert result.success is True
        assert mock_event_integration.setup_event_handlers.called
    
    @pytest.mark.asyncio
    async def test_compensation(self, integration_step, mock_event_integration):
        """Test event integration compensation."""
        context = SagaContext("test")
        
        result = await integration_step.compensate(context)
        
        assert result.success is True
        assert mock_event_integration.shutdown.called


class TestConstructTabInitializationSaga:
    """Test suite for ConstructTabInitializationSaga."""
    
    @pytest.fixture
    def saga(self):
        """Create saga instance."""
        return ConstructTabInitializationSaga()
    
    @pytest.fixture
    def mock_steps(self):
        """Create mock saga steps."""
        step1 = Mock(spec=ISagaStep)
        step1.step_id = "step1"
        step1.description = "Test Step 1"
        step1.execute = AsyncMock(return_value=SagaResult(success=True))
        step1.compensate = AsyncMock(return_value=SagaResult(success=True))
        
        step2 = Mock(spec=ISagaStep)
        step2.step_id = "step2"
        step2.description = "Test Step 2"
        step2.execute = AsyncMock(return_value=SagaResult(success=True))
        step2.compensate = AsyncMock(return_value=SagaResult(success=True))
        
        return [step1, step2]
    
    @pytest.mark.asyncio
    async def test_successful_saga_execution(self, saga, mock_steps):
        """Test successful saga execution."""
        for step in mock_steps:
            saga.add_step(step)
        
        result = await saga.execute()
        
        assert result is True
        assert saga.status == SagaStatus.COMPLETED
        assert len(saga.context.completed_steps) == 2
        
        # All steps should have been executed
        for step in mock_steps:
            assert step.execute.called
    
    @pytest.mark.asyncio
    async def test_saga_rollback_on_failure(self, saga, mock_steps):
        """Test saga rollback when step fails."""
        step1, step2 = mock_steps
        
        # Second step fails
        step2.execute = AsyncMock(return_value=SagaResult(success=False, error_message="Step 2 failed"))
        
        saga.add_step(step1)
        saga.add_step(step2)
        
        result = await saga.execute()
        
        assert result is False
        assert saga.status == SagaStatus.COMPENSATED
        
        # First step should be compensated
        assert step1.compensate.called
        # Second step should not be compensated (it failed)
        assert not step2.compensate.called
    
    @pytest.mark.asyncio
    async def test_compensation_failure_handling(self, saga, mock_steps):
        """Test handling of compensation failures."""
        step1, step2 = mock_steps
        
        # Second step fails
        step2.execute = AsyncMock(return_value=SagaResult(success=False, error_message="Step 2 failed"))
        # First step compensation fails
        step1.compensate = AsyncMock(return_value=SagaResult(success=False, error_message="Compensation failed"))
        
        saga.add_step(step1)
        saga.add_step(step2)
        
        result = await saga.execute()
        
        assert result is False
        assert saga.status == SagaStatus.COMPENSATION_FAILED
    
    @pytest.mark.asyncio
    async def test_empty_saga_execution(self, saga):
        """Test execution of saga with no steps."""
        result = await saga.execute()
        
        assert result is True
        assert saga.status == SagaStatus.COMPLETED
    
    @pytest.mark.asyncio
    async def test_saga_context_sharing(self, saga, mock_steps):
        """Test that context is shared between steps."""
        step1, step2 = mock_steps
        
        # First step adds data to context
        async def step1_execute(context):
            context.shared_data["test_data"] = "shared_value"
            return SagaResult(success=True)
        
        step1.execute = step1_execute
        
        # Second step should receive the same context
        received_contexts = []
        
        async def step2_execute(context):
            received_contexts.append(context)
            return SagaResult(success=True)
        
        step2.execute = step2_execute
        
        saga.add_step(step1)
        saga.add_step(step2)
        
        await saga.execute()
        
        # Verify context was shared
        assert len(received_contexts) == 1
        assert received_contexts[0].shared_data["test_data"] == "shared_value"
    
    def test_step_management(self, saga):
        """Test adding and removing steps."""
        step = Mock()
        step.step_id = "test_step"
        
        saga.add_step(step)
        assert len(saga.steps) == 1
        assert saga.steps[0] is step
    
    def test_saga_status_transitions(self, saga):
        """Test saga status transitions."""
        assert saga.status == SagaStatus.PENDING
        
        saga.context.status = SagaStatus.EXECUTING
        assert saga.status == SagaStatus.EXECUTING
        
        saga.context.status = SagaStatus.COMPLETED
        assert saga.status == SagaStatus.COMPLETED


class TestSagaFactory:
    """Test the factory function for creating initialization saga."""
    
    @pytest.fixture
    def mock_dependencies(self):
        """Create mock dependencies."""
        return {
            "panel_factory": Mock(),
            "service_mesh": Mock(),
            "event_integration": Mock(),
            "container": Mock(),
        }
    
    def test_create_construct_tab_initialization_saga(self, mock_dependencies):
        """Test factory function creates proper saga."""
        saga = create_construct_tab_initialization_saga(
            mock_dependencies["panel_factory"],
            mock_dependencies["service_mesh"],
            mock_dependencies["event_integration"],
            mock_dependencies["container"]
        )
        
        assert isinstance(saga, ConstructTabInitializationSaga)
        assert len(saga.steps) > 0
        
        # Should contain expected step types
        step_ids = [step.step_id for step in saga.steps]
        assert "create_workbench" in step_ids
        assert "create_pickers" in step_ids
        assert "setup_event_integration" in step_ids


class TestSagaPerformance:
    """Test saga performance characteristics."""
    
    @pytest.mark.asyncio
    async def test_concurrent_step_execution_safety(self):
        """Test that saga handles concurrent execution safely."""
        saga = ConstructTabInitializationSaga()
        
        # Add steps that might interfere with each other
        for i in range(5):
            step = Mock(spec=ISagaStep)
            step.step_id = f"step_{i}"
            step.description = f"Step {i}"
            step.execute = AsyncMock(return_value=SagaResult(success=True))
            step.compensate = AsyncMock(return_value=SagaResult(success=True))
            saga.add_step(step)
        
        # Execute multiple sagas concurrently
        tasks = [saga.execute() for _ in range(3)]
        
        # Should not interfere with each other
        # (Only one should succeed, others should handle gracefully)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # At least one should succeed
        successful_results = [r for r in results if r is True]
        assert len(successful_results) >= 1
    
    @pytest.mark.asyncio
    async def test_saga_execution_timing(self):
        """Test saga execution performance."""
        saga = ConstructTabInitializationSaga()
        
        # Add steps with known execution time
        for i in range(3):
            step = Mock(spec=ISagaStep)
            step.step_id = f"timed_step_{i}"
            step.description = f"Timed Step {i}"
            
            async def fast_execute(context):
                await asyncio.sleep(0.01)  # 10ms
                return SagaResult(success=True)
            
            step.execute = fast_execute
            step.compensate = AsyncMock(return_value=SagaResult(success=True))
            saga.add_step(step)
        
        start_time = asyncio.get_event_loop().time()
        result = await saga.execute()
        end_time = asyncio.get_event_loop().time()
        
        execution_time = end_time - start_time
        
        assert result is True
        # Should complete within reasonable time (steps + overhead)
        assert execution_time < 0.1  # 100ms should be plenty
