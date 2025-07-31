"""
Animation Orchestrator - High-level service combining core engine with platform adapters.
This is the main service that UI components interact with.

FIXED: Removed circular import by moving Qt-specific imports inside functions.
The shared package should not depend on desktop.modern at module level.
"""

import asyncio
from collections.abc import Callable
from typing import Any

# FIXED: Import only framework-agnostic components at module level
from desktop.modern.core.animation.animation_engine import (
    CoreAnimationEngine,
    DefaultSettingsProvider,
    SimpleEventBus,
)
from desktop.modern.core.interfaces.animation_core_interfaces import (
    AnimationConfig,
    FadeCommand,
    IAnimationCommand,
    IAnimationEngine,
    IAnimationOrchestrator,
    IEventBus,
    TransitionCommand,
)


class ModernAnimationOrchestrator(IAnimationOrchestrator):
    """
    Modern animation orchestrator that combines the framework-agnostic core
    with platform-specific adapters.

    FIXED: No longer imports Qt-specific adapters at module level.
    """

    def __init__(
        self,
        animation_engine: IAnimationEngine,
        target_adapter,  # Generic type instead of QtTargetAdapter
        renderer,  # Generic type instead of QtAnimationRenderer
        event_bus: IEventBus,
        stack_adapter,  # Generic type instead of QtStackWidgetAdapter
        effect_manager,  # Generic type instead of QtGraphicsEffectManager
        settings_integration,  # Generic type instead of QtSettingsIntegration
    ):
        self.animation_engine = animation_engine
        self.target_adapter = target_adapter
        self.renderer = renderer
        self.event_bus = event_bus
        self.stack_adapter = stack_adapter
        self.effect_manager = effect_manager
        self.settings_integration = settings_integration

        # Command history for undo functionality
        self._command_history: list[IAnimationCommand] = []
        self._max_history = 50

        # Subscribe to animation events to apply frames
        self.event_bus.subscribe("animation.frame", self._on_animation_frame)

    async def fade_target(
        self, target: Any, fade_in: bool, config: AnimationConfig | None = None
    ) -> str:
        """Fade a target in or out."""
        if config is None:
            config = AnimationConfig()

        # Adapt target to framework-agnostic representation
        animation_target = self.target_adapter.adapt_target(target)

        # Create and execute fade command
        command = FadeCommand(
            target=animation_target,
            fade_in=fade_in,
            config=config,
            engine=self.animation_engine,
        )

        success = await self.execute_command(command)
        return command._animation_id if success else ""

    async def fade_targets(
        self,
        targets: list[Any],
        fade_in: bool,
        config: AnimationConfig | None = None,
    ) -> list[str]:
        """Fade multiple targets simultaneously."""
        if not targets:
            return []

        if config is None:
            config = AnimationConfig()

        # Convert all targets and start animations
        animation_ids = []
        for target in targets:
            animation_id = await self.fade_target(target, fade_in, config)
            if animation_id:
                animation_ids.append(animation_id)

        return animation_ids

    async def transition_targets(
        self,
        targets: list[Any],
        update_callback: Callable[[], None],
        config: AnimationConfig | None = None,
    ) -> None:
        """Fade out targets, execute callback, then fade in."""
        if not targets:
            if update_callback:
                update_callback()
            return

        if config is None:
            config = AnimationConfig()

        # Phase 1: Fade out all targets
        await self.fade_targets(targets, fade_in=False, config=config)

        # Phase 2: Execute update callback
        if update_callback:
            update_callback()

        # Phase 3: Fade in all targets
        await self.fade_targets(targets, fade_in=True, config=config)

    async def fade_stack_transition(
        self,
        stack: Any,  # QStackedWidget
        new_index: int,
        config: AnimationConfig | None = None,
    ) -> str:
        """Animate stack widget transition."""
        if config is None:
            config = AnimationConfig()

        # Prepare stack transition
        current_target, next_target = self.stack_adapter.prepare_stack_transition(
            stack, new_index
        )

        if not current_target or not next_target:
            return ""

        # Phase 1: Fade out current widget
        fade_out_id = await self.fade_target(
            current_target, fade_in=False, config=config
        )

        # Phase 2: Switch stack index
        self.stack_adapter.switch_stack_index(stack, new_index)

        # Phase 3: Fade in next widget
        fade_in_id = await self.fade_target(next_target, fade_in=True, config=config)

        return fade_in_id

    async def cross_fade_targets(
        self, out_target: Any, in_target: Any, config: AnimationConfig | None = None
    ) -> tuple[str, str]:
        """Cross-fade between two targets simultaneously."""
        if config is None:
            config = AnimationConfig()

        # Start both animations simultaneously
        out_task = asyncio.create_task(
            self.fade_target(out_target, fade_in=False, config=config)
        )
        in_task = asyncio.create_task(
            self.fade_target(in_target, fade_in=True, config=config)
        )

        # Wait for both to complete
        out_id, in_id = await asyncio.gather(out_task, in_task)
        return out_id, in_id

    async def animate_property(
        self,
        target: Any,
        property_name: str,
        from_value: Any,
        to_value: Any,
        config: AnimationConfig | None = None,
    ) -> str:
        """Animate a specific property of a target."""
        if config is None:
            config = AnimationConfig()

        # Adapt target
        animation_target = self.target_adapter.adapt_target(target)

        # Create transition command
        command = TransitionCommand(
            target=animation_target,
            from_state={property_name: from_value},
            to_state={property_name: to_value},
            config=config,
            engine=self.animation_engine,
        )

        success = await self.execute_command(command)
        return command._animation_ids[0] if success and command._animation_ids else ""

    async def execute_command(self, command: IAnimationCommand) -> bool:
        """Execute an animation command and add to history."""
        try:
            success = await command.execute()

            if success:
                # Add to command history
                self._command_history.append(command)

                # Limit history size
                if len(self._command_history) > self._max_history:
                    self._command_history.pop(0)

            return success
        except Exception as e:
            print(f"Command execution failed: {e}")
            return False

    def get_animations_enabled(self) -> bool:
        """Check if animations are enabled."""
        return self.settings_integration.get_animations_enabled()

    def cleanup_effects(self, targets: list[Any]) -> None:
        """Clean up graphics effects for targets."""
        qt_widgets = []
        for target in targets:
            if hasattr(target, "setGraphicsEffect"):  # Qt widget
                qt_widgets.append(target)

        if qt_widgets:
            self.effect_manager.remove_effects(qt_widgets)

    def _on_animation_frame(self, event) -> None:
        """Handle animation frame events and apply to targets."""
        if event.metadata:
            property_name = event.metadata.get("property")
            value = event.metadata.get("value")

            if property_name and value is not None:
                # Apply the frame to the target
                asyncio.create_task(
                    self.renderer.render_frame(
                        event.target, property_name, value, event.progress
                    )
                )


# Convenience wrapper that provides legacy-style interface
class LegacyFadeManagerWrapper:
    """
    Wrapper that provides a legacy FadeManager-like interface
    for easier migration from the old system.
    """

    def __init__(self, orchestrator: ModernAnimationOrchestrator):
        self.orchestrator = orchestrator

        # Create sub-components for legacy compatibility
        self.widget_fader = self._create_widget_fader()
        self.stack_fader = self._create_stack_fader()
        self.parallel_stack_fader = self._create_parallel_stack_fader()

    def fades_enabled(self) -> bool:
        """Legacy method to check if fades are enabled."""
        return self.orchestrator.get_animations_enabled()

    def _create_widget_fader(self):
        """Create widget fader adapter."""

        class WidgetFaderAdapter:
            def __init__(self, orchestrator):
                self.orchestrator = orchestrator

            def fade_widgets(self, widgets, fade_in, duration=250, callback=None):
                config = AnimationConfig(
                    duration=duration / 1000.0
                )  # Convert ms to seconds

                async def run_fade():
                    await self.orchestrator.fade_targets(widgets, fade_in, config)
                    if callback:
                        callback()

                asyncio.create_task(run_fade())

            def fade_and_update(self, widgets, callback, duration=250):
                config = AnimationConfig(duration=duration / 1000.0)

                if isinstance(callback, tuple):
                    update_callback, final_callback = callback
                else:
                    update_callback = callback
                    final_callback = None

                async def run_fade_and_update():
                    await self.orchestrator.transition_targets(
                        widgets, update_callback, config
                    )
                    if final_callback:
                        final_callback()

                asyncio.create_task(run_fade_and_update())

        return WidgetFaderAdapter(self.orchestrator)

    def _create_stack_fader(self):
        """Create stack fader adapter."""

        class StackFaderAdapter:
            def __init__(self, orchestrator):
                self.orchestrator = orchestrator

            def fade_stack(self, stack, new_index, duration=300, callback=None):
                config = AnimationConfig(duration=duration / 1000.0)

                async def run_stack_fade():
                    await self.orchestrator.fade_stack_transition(
                        stack, new_index, config
                    )
                    if callback:
                        callback()

                asyncio.create_task(run_stack_fade())

        return StackFaderAdapter(self.orchestrator)

    def _create_parallel_stack_fader(self):
        """Create parallel stack fader adapter."""

        class ParallelStackFaderAdapter:
            def __init__(self, orchestrator):
                self.orchestrator = orchestrator

            def fade_both_stacks(
                self,
                right_stack,
                right_new_index,
                left_stack,
                left_new_index,
                width_ratio,
                duration=300,
                callback=None,
            ):
                config = AnimationConfig(duration=duration / 1000.0)

                async def run_parallel_fade():
                    # Fade out both current widgets
                    tasks = []
                    if right_stack.currentWidget():
                        tasks.append(
                            self.orchestrator.fade_target(
                                right_stack.currentWidget(), False, config
                            )
                        )
                    if left_stack.currentWidget():
                        tasks.append(
                            self.orchestrator.fade_target(
                                left_stack.currentWidget(), False, config
                            )
                        )

                    if tasks:
                        await asyncio.gather(*tasks)

                    # Switch both stacks
                    right_stack.setCurrentIndex(right_new_index)
                    left_stack.setCurrentIndex(left_new_index)

                    # Apply layout ratio (if layout manager is available)
                    # This would need to be connected to your layout system

                    # Fade in both new widgets
                    tasks = []
                    if right_stack.currentWidget():
                        tasks.append(
                            self.orchestrator.fade_target(
                                right_stack.currentWidget(), True, config
                            )
                        )
                    if left_stack.currentWidget():
                        tasks.append(
                            self.orchestrator.fade_target(
                                left_stack.currentWidget(), True, config
                            )
                        )

                    if tasks:
                        await asyncio.gather(*tasks)

                    if callback:
                        callback()

                asyncio.create_task(run_parallel_fade())

        return ParallelStackFaderAdapter(self.orchestrator)


def create_modern_animation_system(
    settings_coordinator=None,
) -> tuple[ModernAnimationOrchestrator, LegacyFadeManagerWrapper]:
    """
    Factory function to create the complete modern animation system.

    Returns both the modern orchestrator and a legacy wrapper for migration.

    FIXED: Qt-specific imports moved inside function to break circular import.
    """
    # FIXED: Import Qt-specific components inside function instead of module level
    from desktop.modern.application.services.ui.animation.adapters.qt_adapters import (
        QtEventBridge,
        create_qt_animation_components,
    )

    qt_components = create_qt_animation_components(settings_coordinator)

    # Create core animation engine
    event_bus = SimpleEventBus()
    scheduler = qt_components["scheduler"]
    settings_provider = DefaultSettingsProvider()

    animation_engine = CoreAnimationEngine(event_bus, scheduler, settings_provider)

    # Create Qt event bridge
    qt_event_bridge = QtEventBridge(event_bus)

    # Create orchestrator
    orchestrator = ModernAnimationOrchestrator(
        animation_engine=animation_engine,
        target_adapter=qt_components["target_adapter"],
        renderer=qt_components["renderer"],
        event_bus=event_bus,
        stack_adapter=qt_components["stack_adapter"],
        effect_manager=qt_components["effect_manager"],
        settings_integration=qt_components["settings_integration"],
    )

    # Create legacy wrapper
    legacy_wrapper = LegacyFadeManagerWrapper(orchestrator)

    return orchestrator, legacy_wrapper
