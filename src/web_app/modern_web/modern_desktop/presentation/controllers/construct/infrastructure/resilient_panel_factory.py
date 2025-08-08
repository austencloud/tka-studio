"""
Circuit Breaker Enhancement for PanelFactory

Adds circuit breaker pattern to existing panel factory for improved resilience.
Builds on existing error handling with circuit breaker state management.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
import time
from typing import Any

from desktop.modern.core.dependency_injection.di_container import DIContainer


logger = __import__("logging").getLogger(__name__)


class CircuitBreakerState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, requests blocked
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration."""

    failure_threshold: int = 5
    timeout_duration: float = 30.0  # seconds
    recovery_timeout: float = 60.0  # seconds
    success_threshold: int = 3  # for half-open → closed


@dataclass
class CircuitBreakerStats:
    """Circuit breaker statistics."""

    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    last_failure_time: float | None = None
    state_changes: int = 0


class CircuitBreaker:
    """
    Circuit breaker implementation for panel creation.

    Protects against cascading failures when panel creation fails.
    Automatically tries to recover after timeout period.
    """

    def __init__(self, name: str, config: CircuitBreakerConfig):
        self.name = name
        self.config = config
        self.state = CircuitBreakerState.CLOSED
        self.stats = CircuitBreakerStats()

    def can_execute(self) -> bool:
        """Check if operation can be executed."""
        if self.state == CircuitBreakerState.CLOSED:
            return True
        if self.state == CircuitBreakerState.OPEN:
            # Check if timeout period has passed
            if self.stats.last_failure_time:
                time_since_failure = time.time() - self.stats.last_failure_time
                if time_since_failure >= self.config.recovery_timeout:
                    self._transition_to_half_open()
                    return True
            return False
        if self.state == CircuitBreakerState.HALF_OPEN:
            return True
        return False

    def record_success(self):
        """Record successful operation."""
        self.stats.total_requests += 1
        self.stats.successful_requests += 1
        self.stats.consecutive_failures = 0
        self.stats.consecutive_successes += 1

        if self.state == CircuitBreakerState.HALF_OPEN:
            if self.stats.consecutive_successes >= self.config.success_threshold:
                self._transition_to_closed()

    def record_failure(self, error: Exception):
        """Record failed operation."""
        self.stats.total_requests += 1
        self.stats.failed_requests += 1
        self.stats.consecutive_failures += 1
        self.stats.consecutive_successes = 0
        self.stats.last_failure_time = time.time()

        logger.warning(f"Circuit breaker {self.name}: failure recorded - {error}")

        if self.state in [CircuitBreakerState.CLOSED, CircuitBreakerState.HALF_OPEN]:
            if self.stats.consecutive_failures >= self.config.failure_threshold:
                self._transition_to_open()

    def _transition_to_open(self):
        """Transition to OPEN state."""
        old_state = self.state
        self.state = CircuitBreakerState.OPEN
        self.stats.state_changes += 1
        logger.warning(f"Circuit breaker {self.name}: {old_state.value} → OPEN")

    def _transition_to_half_open(self):
        """Transition to HALF_OPEN state."""
        old_state = self.state
        self.state = CircuitBreakerState.HALF_OPEN
        self.stats.state_changes += 1
        self.stats.consecutive_successes = 0
        logger.info(f"Circuit breaker {self.name}: {old_state.value} → HALF_OPEN")

    def _transition_to_closed(self):
        """Transition to CLOSED state."""
        old_state = self.state
        self.state = CircuitBreakerState.CLOSED
        self.stats.state_changes += 1
        logger.info(f"Circuit breaker {self.name}: {old_state.value} → CLOSED")

    def get_stats(self) -> dict[str, Any]:
        """Get circuit breaker statistics."""
        return {
            "name": self.name,
            "state": self.state.value,
            "total_requests": self.stats.total_requests,
            "successful_requests": self.stats.successful_requests,
            "failed_requests": self.stats.failed_requests,
            "success_rate": (
                self.stats.successful_requests / max(self.stats.total_requests, 1) * 100
            ),
            "consecutive_failures": self.stats.consecutive_failures,
            "state_changes": self.stats.state_changes,
        }


class ResilientPanelFactory:
    """
    Enhanced panel factory with circuit breaker protection.

    Builds on existing PanelFactory error handling with circuit breaker pattern.
    Provides graceful degradation when components fail repeatedly.
    """

    def __init__(
        self,
        container: DIContainer,
        progress_callback: Callable[[int, str], None] | None = None,
    ):
        # Import the existing PanelFactory
        from .panel_factory import PanelFactory

        self.panel_factory = PanelFactory(container, progress_callback)
        self.container = container
        self.progress_callback = progress_callback

        # Circuit breakers for each component type
        self.circuit_breakers = {
            "workbench": CircuitBreaker("workbench", CircuitBreakerConfig()),
            "start_position_picker": CircuitBreaker(
                "start_position_picker", CircuitBreakerConfig()
            ),
            "option_picker": CircuitBreaker("option_picker", CircuitBreakerConfig()),
            "graph_editor": CircuitBreaker("graph_editor", CircuitBreakerConfig()),
            "generate_controls": CircuitBreaker(
                "generate_controls", CircuitBreakerConfig()
            ),
        }

        logger.info("ResilientPanelFactory initialized with circuit breakers")

    def create_workbench_panel(self):
        """Create workbench panel with circuit breaker protection."""
        return self._execute_with_circuit_breaker(
            "workbench",
            self.panel_factory.create_workbench_panel,
            self._create_workbench_fallback,
        )

    def create_start_position_panel(self):
        """Create start position panel with circuit breaker protection."""
        return self._execute_with_circuit_breaker(
            "start_position_picker",
            self.panel_factory.create_start_position_panel,
            self._create_start_position_fallback,
        )

    def create_option_picker_panel(self):
        """Create option picker panel with circuit breaker protection."""
        return self._execute_with_circuit_breaker(
            "option_picker",
            self.panel_factory.create_option_picker_panel,
            self._create_option_picker_fallback,
        )

    def create_graph_editor_panel(self):
        """Create graph editor panel with circuit breaker protection."""
        return self._execute_with_circuit_breaker(
            "graph_editor",
            self.panel_factory.create_graph_editor_panel,
            self._create_graph_editor_fallback,
        )

    def create_generate_controls_panel(self):
        """Create generate controls panel with circuit breaker protection."""
        return self._execute_with_circuit_breaker(
            "generate_controls",
            self.panel_factory.create_generate_controls_panel,
            self._create_generate_controls_fallback,
        )

    def _execute_with_circuit_breaker(
        self, component_name: str, create_func: Callable, fallback_func: Callable
    ):
        """Execute panel creation with circuit breaker protection."""
        circuit_breaker = self.circuit_breakers[component_name]

        if not circuit_breaker.can_execute():
            logger.warning(f"Circuit breaker {component_name} is OPEN, using fallback")
            return fallback_func(
                f"Circuit breaker protection: {component_name} temporarily unavailable"
            )

        try:
            result = create_func()
            circuit_breaker.record_success()
            return result
        except Exception as e:
            circuit_breaker.record_failure(e)
            logger.error(
                f"Panel creation failed for {component_name}: {e}", exc_info=True
            )
            return fallback_func(f"Creation failed: {e}")

    def _create_workbench_fallback(self, reason: str):
        """Create fallback workbench widget."""
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

        widget = QWidget()
        layout = QVBoxLayout(widget)

        label = QLabel(f"Workbench unavailable\\n{reason}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            "color: red; font-size: 14px; padding: 20px; background-color: #ffe6e6;"
        )
        layout.addWidget(label)

        return widget, None

    def _create_start_position_fallback(self, reason: str):
        """Create fallback start position picker widget."""
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

        widget = QWidget()
        layout = QVBoxLayout(widget)

        label = QLabel(f"Start Position Picker unavailable\\n{reason}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            "color: orange; font-size: 14px; padding: 20px; background-color: #fff3e0;"
        )
        layout.addWidget(label)

        return widget, None

    def _create_option_picker_fallback(self, reason: str):
        """Create fallback option picker widget."""
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

        widget = QWidget()
        layout = QVBoxLayout(widget)

        label = QLabel(f"Option Picker unavailable\\n{reason}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            "color: orange; font-size: 14px; padding: 20px; background-color: #fff3e0;"
        )
        layout.addWidget(label)

        return widget, None

    def _create_graph_editor_fallback(self, reason: str):
        """Create fallback graph editor widget."""
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

        widget = QWidget()
        layout = QVBoxLayout(widget)

        label = QLabel(f"Graph Editor unavailable\\n{reason}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            "color: red; font-size: 14px; padding: 20px; background-color: #ffe6e6;"
        )
        layout.addWidget(label)

        return widget, None

    def _create_generate_controls_fallback(self, reason: str):
        """Create fallback generate controls widget."""
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

        widget = QWidget()
        layout = QVBoxLayout(widget)

        label = QLabel(f"Generate Controls unavailable\\n{reason}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            "color: orange; font-size: 14px; padding: 20px; background-color: #fff3e0;"
        )
        layout.addWidget(label)

        return widget, None

    def reset_circuit_breaker(self, component_name: str) -> bool:
        """Reset specific circuit breaker to CLOSED state."""
        if component_name in self.circuit_breakers:
            breaker = self.circuit_breakers[component_name]
            breaker.state = CircuitBreakerState.CLOSED
            breaker.stats.consecutive_failures = 0
            breaker.stats.consecutive_successes = 0
            logger.info(f"Circuit breaker {component_name} manually reset to CLOSED")
            return True
        return False
