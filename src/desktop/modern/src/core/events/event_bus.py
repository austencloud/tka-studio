"""
TypeSafe Event Bus for Decoupled Component Communication

Provides a type-safe, high-performance event system for Modern architecture:
- Type-safe event definitions with dataclasses
- Async and sync event handling
- Event filtering and priority handling
- Comprehensive logging and debugging
- Memory-efficient subscription management
"""
from __future__ import annotations

from abc import ABC, abstractmethod
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import threading
from typing import Any, Callable, TypeVar, Union
import uuid
import weakref


# Type definitions
T = TypeVar("T")
EventHandler = Union[Callable[[T], None], Callable[[T], asyncio.Future]]


class EventPriority(Enum):
    """Event priority levels for ordered processing."""

    CRITICAL = 0  # System-critical events (errors, shutdown)
    HIGH = 1  # Important UI updates, user actions
    NORMAL = 2  # Standard application events
    LOW = 3  # Background tasks, logging
    BACKGROUND = 4  # Non-essential events


@dataclass(frozen=True)
class BaseEvent(ABC):
    """Base class for all events in the system."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    source: str | None = None
    priority: EventPriority = EventPriority.NORMAL

    @property
    @abstractmethod
    def event_type(self) -> str:
        """Unique identifier for this event type."""


@dataclass(frozen=True)
class SequenceEvent(BaseEvent):
    """Events related to sequence operations."""

    sequence_id: str = ""
    operation: str = ""  # 'created', 'updated', 'deleted', 'beat_added', 'beat_removed'
    data: dict[str, Any] = field(default_factory=dict)

    @property
    def event_type(self) -> str:
        return f"sequence.{self.operation}"


@dataclass(frozen=True)
class ArrowEvent(BaseEvent):
    """Events related to arrow operations."""

    arrow_color: str = ""
    operation: str = ""  # 'positioned', 'mirrored', 'updated'
    pictograph_id: str | None = None
    position_data: dict[str, Any] = field(default_factory=dict)

    @property
    def event_type(self) -> str:
        return f"arrow.{self.operation}"


@dataclass(frozen=True)
class MotionEvent(BaseEvent):
    """Events related to motion operations."""

    motion_id: str = ""
    operation: str = ""  # 'validated', 'generated', 'orientation_calculated'
    validation_result: bool | None = None
    errors: list[str] = field(default_factory=list)

    @property
    def event_type(self) -> str:
        return f"motion.{self.operation}"


@dataclass(frozen=True)
class UIEvent(BaseEvent):
    """Events related to UI state changes."""

    component: str = ""
    action: str = ""  # 'shown', 'hidden', 'updated', 'clicked'
    state_data: dict[str, Any] = field(default_factory=dict)

    @property
    def event_type(self) -> str:
        return f"ui.{self.component}.{self.action}"


@dataclass
class EventSubscription:
    """Represents a subscription to an event type."""

    subscription_id: str
    event_type: str
    handler: EventHandler
    priority: EventPriority
    is_async: bool
    weak_ref: bool = True
    filter_func: Callable[[BaseEvent], bool] | None = None

    def __post_init__(self):
        if self.weak_ref and hasattr(self.handler, "__self__"):
            # Create weak reference for bound methods
            self.handler = weakref.WeakMethod(self.handler)


class IEventBus(ABC):
    """Interface for event bus implementations."""

    @abstractmethod
    def publish(self, event: BaseEvent) -> None:
        """Publish an event to all subscribers."""

    @abstractmethod
    async def publish_async(self, event: BaseEvent) -> None:
        """Publish an event asynchronously."""

    @abstractmethod
    def subscribe(
        self,
        event_type: str,
        handler: EventHandler,
        priority: EventPriority = EventPriority.NORMAL,
        filter_func: Callable[[BaseEvent], bool] | None = None,
    ) -> str:
        """Subscribe to an event type."""

    @abstractmethod
    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from an event type."""


class TypeSafeEventBus(IEventBus):
    """
    High-performance, type-safe event bus implementation.

    Features:
    - Type-safe event definitions
    - Priority-based event processing
    - Async and sync handler support
    - Weak reference management
    - Event filtering
    - Comprehensive logging
    """

    def __init__(self, max_workers: int = 4):
        self._subscriptions: dict[str, list[EventSubscription]] = {}
        self._subscription_lookup: dict[str, EventSubscription] = {}
        self._lock = threading.RLock()
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._logger = logging.getLogger(__name__)
        self._event_stats: dict[str, int] = {}

    def publish(self, event: BaseEvent) -> None:
        """Publish an event to all subscribers synchronously."""
        with self._lock:
            subscriptions = self._subscriptions.get(event.event_type, [])

            # Sort by priority
            subscriptions.sort(key=lambda s: s.priority.value)

            # Track event statistics
            self._event_stats[event.event_type] = (
                self._event_stats.get(event.event_type, 0) + 1
            )

            self._logger.debug(
                f"Publishing event {event.event_type} to {len(subscriptions)} subscribers"
            )

            for subscription in subscriptions:
                try:
                    self._handle_subscription(subscription, event)
                except Exception as e:
                    self._logger.exception(f"Error handling event {event.event_type}: {e}")

    async def publish_async(self, event: BaseEvent) -> None:
        """Publish an event to all subscribers asynchronously."""
        with self._lock:
            subscriptions = self._subscriptions.get(event.event_type, [])

            # Sort by priority
            subscriptions.sort(key=lambda s: s.priority.value)

            # Track event statistics
            self._event_stats[event.event_type] = (
                self._event_stats.get(event.event_type, 0) + 1
            )

            self._logger.debug(
                f"Publishing async event {event.event_type} to {len(subscriptions)} subscribers"
            )

            # Handle async subscriptions
            async_tasks = []
            for subscription in subscriptions:
                try:
                    if subscription.is_async:
                        task = self._handle_subscription_async(subscription, event)
                        async_tasks.append(task)
                    else:
                        # Run sync handlers in executor
                        loop = asyncio.get_event_loop()
                        task = loop.run_in_executor(
                            self._executor,
                            self._handle_subscription,
                            subscription,
                            event,
                        )
                        async_tasks.append(task)
                except Exception as e:
                    self._logger.exception(
                        f"Error handling async event {event.event_type}: {e}"
                    )

            # Wait for all handlers to complete
            if async_tasks:
                await asyncio.gather(*async_tasks, return_exceptions=True)

    def subscribe(
        self,
        event_type: str,
        handler: EventHandler,
        priority: EventPriority = EventPriority.NORMAL,
        filter_func: Callable[[BaseEvent], bool] | None = None,
    ) -> str:
        """Subscribe to an event type with optional filtering."""
        subscription_id = str(uuid.uuid4())

        # Determine if handler is async
        is_async = asyncio.iscoroutinefunction(handler)

        subscription = EventSubscription(
            subscription_id=subscription_id,
            event_type=event_type,
            handler=handler,
            priority=priority,
            is_async=is_async,
            filter_func=filter_func,
        )

        with self._lock:
            if event_type not in self._subscriptions:
                self._subscriptions[event_type] = []

            self._subscriptions[event_type].append(subscription)
            self._subscription_lookup[subscription_id] = subscription

        self._logger.debug(f"Subscribed to {event_type} with priority {priority.name}")
        return subscription_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from an event type."""
        with self._lock:
            if subscription_id not in self._subscription_lookup:
                return False

            subscription = self._subscription_lookup[subscription_id]
            event_type = subscription.event_type

            # Remove from subscriptions list
            if event_type in self._subscriptions:
                self._subscriptions[event_type] = [
                    s
                    for s in self._subscriptions[event_type]
                    if s.subscription_id != subscription_id
                ]

                # Clean up empty event type lists
                if not self._subscriptions[event_type]:
                    del self._subscriptions[event_type]

            # Remove from lookup
            del self._subscription_lookup[subscription_id]

            self._logger.debug(f"Unsubscribed from {event_type}")
            return True

    def get_event_stats(self) -> dict[str, int]:
        """Get event publishing statistics."""
        with self._lock:
            return self._event_stats.copy()

    def get_subscription_count(self, event_type: str | None = None) -> int:
        """Get number of active subscriptions."""
        with self._lock:
            if event_type:
                return len(self._subscriptions.get(event_type, []))
            return len(self._subscription_lookup)

    def clear_dead_references(self) -> int:
        """Clean up dead weak references and return count removed."""
        removed_count = 0

        with self._lock:
            for event_type in list(self._subscriptions.keys()):
                original_count = len(self._subscriptions[event_type])

                # Filter out dead weak references
                self._subscriptions[event_type] = [
                    s
                    for s in self._subscriptions[event_type]
                    if not self._is_dead_reference(s)
                ]

                removed_count += original_count - len(self._subscriptions[event_type])

                # Clean up empty lists
                if not self._subscriptions[event_type]:
                    del self._subscriptions[event_type]

            # Update lookup table
            self._subscription_lookup = {
                s.subscription_id: s
                for subscriptions in self._subscriptions.values()
                for s in subscriptions
            }

        if removed_count > 0:
            self._logger.debug(f"Cleaned up {removed_count} dead references")

        return removed_count

    def _handle_subscription(
        self, subscription: EventSubscription, event: BaseEvent
    ) -> None:
        """Handle a single subscription synchronously."""
        # Check if reference is dead
        if self._is_dead_reference(subscription):
            return

        # Apply filter if present
        if subscription.filter_func and not subscription.filter_func(event):
            return

        # Get actual handler (resolve weak reference if needed)
        handler = self._resolve_handler(subscription)
        if handler is None:
            return

        # Call handler
        if subscription.is_async:
            # For async handlers in sync context, schedule them
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = handler(event)
                if result is not None:
                    loop.run_until_complete(result)
            finally:
                loop.close()
        else:
            handler(event)

    async def _handle_subscription_async(
        self, subscription: EventSubscription, event: BaseEvent
    ) -> None:
        """Handle a single subscription asynchronously."""
        # Check if reference is dead
        if self._is_dead_reference(subscription):
            return

        # Apply filter if present
        if subscription.filter_func and not subscription.filter_func(event):
            return

        # Get actual handler (resolve weak reference if needed)
        handler = self._resolve_handler(subscription)
        if handler is None:
            return

        # Call handler
        if subscription.is_async:
            await handler(event)
        else:
            handler(event)

    def _is_dead_reference(self, subscription: EventSubscription) -> bool:
        """Check if subscription has a dead weak reference."""
        if isinstance(subscription.handler, weakref.WeakMethod):
            return subscription.handler() is None
        return False

    def _resolve_handler(
        self, subscription: EventSubscription
    ) -> EventHandler | None:
        """Resolve handler from subscription (handle weak references)."""
        if isinstance(subscription.handler, weakref.WeakMethod):
            return subscription.handler()
        return subscription.handler

    def shutdown(self) -> None:
        """Shutdown the event bus and cleanup resources."""
        with self._lock:
            self._subscriptions.clear()
            self._subscription_lookup.clear()
            self._executor.shutdown(wait=True)

        self._logger.info("Event bus shutdown complete")


# Global event bus instance
_global_event_bus: TypeSafeEventBus | None = None


def get_event_bus() -> TypeSafeEventBus:
    """Get the global event bus instance."""
    global _global_event_bus
    if _global_event_bus is None:
        _global_event_bus = TypeSafeEventBus()
    return _global_event_bus


def reset_event_bus() -> None:
    """Reset the global event bus (useful for testing)."""
    global _global_event_bus
    if _global_event_bus:
        _global_event_bus.shutdown()
    _global_event_bus = None
