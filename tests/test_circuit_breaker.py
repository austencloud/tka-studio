"""
Circuit Breaker Unit Tests - Phase 1

Comprehensive validation of circuit breaker pattern implementation
for resilient component creation.
"""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from concurrent.futures import ThreadPoolExecutor
import threading

from desktop.modern.presentation.tabs.construct.infrastructure.resilient_panel_factory import (
    CircuitBreaker,
    CircuitBreakerState,
    CircuitBreakerConfig,
    CircuitBreakerStats,
    ResilientPanelFactory
)
from desktop.modern.core.dependency_injection.di_container import DIContainer


class TestCircuitBreaker:
    """Test suite for CircuitBreaker implementation."""
    
    @pytest.fixture
    def circuit_breaker_config(self):
        """Create circuit breaker configuration for testing."""
        return CircuitBreakerConfig(
            failure_threshold=3,
            timeout_duration=1.0,
            recovery_timeout=2.0,
            success_threshold=2
        )
    
    @pytest.fixture
    def circuit_breaker(self, circuit_breaker_config):
        """Create circuit breaker instance for testing."""
        return CircuitBreaker("test_component", circuit_breaker_config)
    
    def test_initial_state(self, circuit_breaker):
        """Test circuit breaker initial state."""
        assert circuit_breaker.state == CircuitBreakerState.CLOSED
        assert circuit_breaker.can_execute()
        assert circuit_breaker.stats.total_requests == 0
        assert circuit_breaker.stats.consecutive_failures == 0
    
    def test_successful_request_recording(self, circuit_breaker):
        """Test recording successful requests."""
        circuit_breaker.record_success()
        
        assert circuit_breaker.stats.total_requests == 1
        assert circuit_breaker.stats.successful_requests == 1
        assert circuit_breaker.stats.consecutive_successes == 1
        assert circuit_breaker.stats.consecutive_failures == 0
        assert circuit_breaker.state == CircuitBreakerState.CLOSED
    
    def test_failure_recording(self, circuit_breaker):
        """Test recording failed requests."""
        error = Exception("Test failure")
        circuit_breaker.record_failure(error)
        
        assert circuit_breaker.stats.total_requests == 1
        assert circuit_breaker.stats.failed_requests == 1
        assert circuit_breaker.stats.consecutive_failures == 1
        assert circuit_breaker.stats.consecutive_successes == 0
        assert circuit_breaker.stats.last_failure_time is not None
    
    def test_failure_threshold_transition(self, circuit_breaker):
        """Test transition to OPEN after failure threshold."""
        # Record failures up to threshold
        for i in range(3):
            circuit_breaker.record_failure(Exception(f"Failure {i}"))
        
        assert circuit_breaker.state == CircuitBreakerState.OPEN
        assert not circuit_breaker.can_execute()
        assert circuit_breaker.stats.consecutive_failures == 3
        assert circuit_breaker.stats.state_changes == 1  # CLOSED -> OPEN
    
    def test_no_premature_opening(self, circuit_breaker):
        """Test circuit breaker doesn't open before threshold."""
        # Record failures below threshold
        for i in range(2):  # Below threshold of 3
            circuit_breaker.record_failure(Exception(f"Failure {i}"))
        
        assert circuit_breaker.state == CircuitBreakerState.CLOSED
        assert circuit_breaker.can_execute()
        assert circuit_breaker.stats.consecutive_failures == 2
    
    def test_recovery_after_timeout(self, circuit_breaker):
        """Test recovery to HALF_OPEN after timeout."""
        # Trigger OPEN state
        for i in range(3):
            circuit_breaker.record_failure(Exception(f"Failure {i}"))
        
        assert circuit_breaker.state == CircuitBreakerState.OPEN
        assert not circuit_breaker.can_execute()
        
        # Wait for recovery timeout
        time.sleep(2.1)  # Slightly more than recovery_timeout
        
        # Should transition to HALF_OPEN on next check
        assert circuit_breaker.can_execute()
        assert circuit_breaker.state == CircuitBreakerState.HALF_OPEN
    
    def test_half_open_success_recovery(self, circuit_breaker):
        """Test successful recovery from HALF_OPEN to CLOSED."""
        # Force HALF_OPEN state
        circuit_breaker.state = CircuitBreakerState.HALF_OPEN
        circuit_breaker.stats.consecutive_successes = 0
        
        # Record enough successes to close circuit
        for i in range(2):  # success_threshold = 2
            circuit_breaker.record_success()
        
        assert circuit_breaker.state == CircuitBreakerState.CLOSED
        assert circuit_breaker.stats.consecutive_successes == 2
    
    def test_half_open_failure_reopening(self, circuit_breaker):
        """Test reopening circuit on failure in HALF_OPEN state."""
        # Force HALF_OPEN state
        circuit_breaker.state = CircuitBreakerState.HALF_OPEN
        
        # Record failure
        circuit_breaker.record_failure(Exception("Half-open failure"))
        
        assert circuit_breaker.state == CircuitBreakerState.OPEN
        assert not circuit_breaker.can_execute()
    
    def test_statistics_calculation(self, circuit_breaker):
        """Test statistics collection and calculation."""
        # Record mixed results
        circuit_breaker.record_success()
        circuit_breaker.record_success()
        circuit_breaker.record_failure(Exception("failure"))
        circuit_breaker.record_success()
        
        stats = circuit_breaker.get_stats()
        
        assert stats["total_requests"] == 4
        assert stats["successful_requests"] == 3
        assert stats["failed_requests"] == 1
        assert stats["success_rate"] == 75.0
        assert stats["failure_rate"] == 25.0
        assert stats["consecutive_failures"] == 0  # Reset by last success
        assert stats["consecutive_successes"] == 1
    
    def test_manual_reset(self, circuit_breaker):
        """Test manual circuit breaker reset."""
        # Open the circuit breaker
        for i in range(3):
            circuit_breaker.record_failure(Exception(f"Failure {i}"))
        
        assert circuit_breaker.state == CircuitBreakerState.OPEN
        
        # Manual reset
        circuit_breaker.reset()
        
        assert circuit_breaker.state == CircuitBreakerState.CLOSED
        assert circuit_breaker.can_execute()
        assert circuit_breaker.stats.consecutive_failures == 0
    
    def test_statistics_persistence_across_states(self, circuit_breaker):
        """Test that statistics are maintained across state transitions."""
        # Record some activity
        circuit_breaker.record_success()
        circuit_breaker.record_failure(Exception("test"))
        
        initial_total = circuit_breaker.stats.total_requests
        
        # Force state change
        circuit_breaker.state = CircuitBreakerState.OPEN
        circuit_breaker.state = CircuitBreakerState.HALF_OPEN
        circuit_breaker.state = CircuitBreakerState.CLOSED
        
        # Statistics should persist
        assert circuit_breaker.stats.total_requests == initial_total
    
    def test_timeout_calculation(self, circuit_breaker):
        """Test timeout calculation accuracy."""
        # Open circuit breaker
        for i in range(3):
            circuit_breaker.record_failure(Exception(f"Failure {i}"))
        
        assert circuit_breaker.state == CircuitBreakerState.OPEN
        
        # Check timeout immediately
        assert not circuit_breaker._should_attempt_reset()
        
        # Wait partial timeout
        time.sleep(1.0)
        assert not circuit_breaker._should_attempt_reset()
        
        # Wait full timeout
        time.sleep(1.5)  # Total 2.5s > recovery_timeout of 2.0s
        assert circuit_breaker._should_attempt_reset()


class TestResilientPanelFactory:
    """Test suite for ResilientPanelFactory."""
    
    @pytest.fixture
    def container(self):
        """Create mock DI container."""
        container = Mock(spec=DIContainer)
        return container
    
    @pytest.fixture
    def resilient_factory(self, container):
        """Create resilient panel factory instance."""
        return ResilientPanelFactory(container)
    
    @pytest.fixture
    def mock_panel_factory(self):
        """Create mock panel factory."""
        factory = Mock()
        factory.create_workbench_panel.return_value = (Mock(), Mock())
        factory.create_start_position_panel.return_value = (Mock(), Mock())
        factory.create_option_picker_panel.return_value = (Mock(), Mock())
        return factory
    
    def test_initialization(self, resilient_factory, container):
        """Test resilient factory initialization."""
        assert resilient_factory.container is container
        assert resilient_factory.panel_factory is not None
        assert len(resilient_factory.circuit_breakers) > 0
        assert "workbench" in resilient_factory.circuit_breakers
        assert "start_position_picker" in resilient_factory.circuit_breakers
        assert "option_picker" in resilient_factory.circuit_breakers
    
    def test_successful_panel_creation(self, resilient_factory):
        """Test successful panel creation without circuit breaker interference."""
        with patch.object(resilient_factory.panel_factory, 'create_workbench_panel') as mock_create:
            mock_panel, mock_component = Mock(), Mock()
            mock_create.return_value = (mock_panel, mock_component)
            
            result = resilient_factory.create_workbench_panel()
            
            assert mock_create.called
            assert result == (mock_panel, mock_component)
            
            # Verify success was recorded
            workbench_cb = resilient_factory.circuit_breakers["workbench"]
            assert workbench_cb.stats.successful_requests == 1
    
    def test_circuit_breaker_protection(self, resilient_factory):
        """Test circuit breaker protection during failures."""
        with patch.object(resilient_factory.panel_factory, 'create_workbench_panel') as mock_create:
            mock_create.side_effect = Exception("Panel creation failed")
            
            # Trigger failures to open circuit breaker
            for i in range(6):  # More than threshold
                result = resilient_factory.create_workbench_panel()
                
                # Should get fallback after circuit opens
                if i >= 5:  # After threshold
                    assert result[0] is not None  # Fallback widget
                    assert result[1] is None      # No component
            
            # Verify circuit breaker is now open
            workbench_cb = resilient_factory.circuit_breakers["workbench"]
            assert workbench_cb.state == CircuitBreakerState.OPEN
    
    def test_fallback_widget_creation(self, resilient_factory):
        """Test fallback widget creation."""
        fallback_widget, fallback_component = resilient_factory._create_workbench_fallback("Test reason")
        
        assert fallback_widget is not None
        assert fallback_component is None
        assert hasattr(fallback_widget, 'setText')  # Should be a QLabel-like widget
    
    def test_all_panel_types_have_circuit_breakers(self, resilient_factory):
        """Test all panel types have associated circuit breakers."""
        expected_components = [
            "workbench",
            "start_position_picker", 
            "option_picker"
        ]
        
        for component in expected_components:
            assert component in resilient_factory.circuit_breakers
            cb = resilient_factory.circuit_breakers[component]
            assert isinstance(cb, CircuitBreaker)
            assert cb.component_name == component
    
    def test_circuit_breaker_status_reporting(self, resilient_factory):
        """Test circuit breaker status reporting."""
        status = resilient_factory.get_circuit_breaker_status()
        
        assert isinstance(status, dict)
        assert "workbench" in status
        assert "start_position_picker" in status
        assert "option_picker" in status
        
        for component_status in status.values():
            assert "state" in component_status
            assert "total_requests" in component_status
            assert "success_rate" in component_status
    
    def test_manual_reset_functionality(self, resilient_factory):
        """Test manual circuit breaker reset."""
        # Force circuit breaker to OPEN
        cb = resilient_factory.circuit_breakers["workbench"]
        cb.state = CircuitBreakerState.OPEN
        
        success = resilient_factory.reset_circuit_breaker("workbench")
        
        assert success
        assert cb.state == CircuitBreakerState.CLOSED
    
    def test_invalid_component_reset(self, resilient_factory):
        """Test reset with invalid component name."""
        success = resilient_factory.reset_circuit_breaker("invalid_component")
        
        assert not success
    
    def test_reset_all_circuit_breakers(self, resilient_factory):
        """Test resetting all circuit breakers."""
        # Open all circuit breakers
        for cb in resilient_factory.circuit_breakers.values():
            cb.state = CircuitBreakerState.OPEN
        
        resilient_factory.reset_all_circuit_breakers()
        
        # All should be closed
        for cb in resilient_factory.circuit_breakers.values():
            assert cb.state == CircuitBreakerState.CLOSED
    
    def test_concurrent_panel_creation(self, resilient_factory):
        """Test concurrent panel creation with circuit breaker protection."""
        with patch.object(resilient_factory.panel_factory, 'create_workbench_panel') as mock_create:
            # Mix successful and failed creations
            side_effects = [
                (Mock(), Mock()),  # Success
                Exception("Failure"),  # Failure
                (Mock(), Mock()),  # Success
                Exception("Failure"),  # Failure
            ]
            mock_create.side_effect = side_effects
            
            results = []
            
            def create_panel():
                try:
                    result = resilient_factory.create_workbench_panel()
                    results.append(("success", result))
                except Exception as e:
                    results.append(("error", str(e)))
            
            # Execute concurrent requests
            threads = []
            for i in range(4):
                thread = threading.Thread(target=create_panel)
                threads.append(thread)
                thread.start()
            
            for thread in threads:
                thread.join()
            
            # Should have handled all requests
            assert len(results) == 4
            
            # Circuit breaker should have recorded activity
            cb = resilient_factory.circuit_breakers["workbench"]
            assert cb.stats.total_requests > 0


class TestCircuitBreakerConfiguration:
    """Test circuit breaker configuration variations."""
    
    def test_custom_thresholds(self):
        """Test circuit breaker with custom thresholds."""
        config = CircuitBreakerConfig(
            failure_threshold=10,
            success_threshold=5
        )
        
        cb = CircuitBreaker("test", config)
        
        # Should require 10 failures to open
        for i in range(9):
            cb.record_failure(Exception(f"Failure {i}"))
        
        assert cb.state == CircuitBreakerState.CLOSED
        
        # 10th failure should open
        cb.record_failure(Exception("Final failure"))
        assert cb.state == CircuitBreakerState.OPEN
    
    def test_timeout_configuration(self):
        """Test different timeout configurations."""
        config = CircuitBreakerConfig(
            failure_threshold=1,
            recovery_timeout=0.1  # Very short timeout
        )
        
        cb = CircuitBreaker("test", config)
        
        # Open circuit
        cb.record_failure(Exception("Test"))
        assert cb.state == CircuitBreakerState.OPEN
        
        # Wait for quick recovery
        time.sleep(0.15)
        
        # Should allow recovery attempt
        assert cb.can_execute()
        assert cb.state == CircuitBreakerState.HALF_OPEN


class TestCircuitBreakerIntegration:
    """Integration tests for circuit breaker with panel factory."""
    
    def test_multiple_component_isolation(self):
        """Test that component failures are isolated."""
        container = Mock()
        factory = ResilientPanelFactory(container)
        
        # Fail workbench creation
        with patch.object(factory.panel_factory, 'create_workbench_panel') as mock_workbench:
            mock_workbench.side_effect = Exception("Workbench failure")
            
            # Multiple failures should open workbench circuit
            for i in range(6):
                factory.create_workbench_panel()
        
        # Option picker should still work
        with patch.object(factory.panel_factory, 'create_option_picker_panel') as mock_option:
            mock_option.return_value = (Mock(), Mock())
            
            result = factory.create_option_picker_panel()
            assert result[0] is not None
            assert result[1] is not None
        
        # Verify isolation
        workbench_cb = factory.circuit_breakers["workbench"]
        option_cb = factory.circuit_breakers["option_picker"]
        
        assert workbench_cb.state == CircuitBreakerState.OPEN
        assert option_cb.state == CircuitBreakerState.CLOSED
