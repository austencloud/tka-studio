"""
Usage examples for the modern fade animation system.

This file demonstrates how to use the new fade system and migrate
from the legacy FadeManager.
"""

import asyncio
from typing import List
from PyQt6.QtWidgets import QWidget, QStackedWidget

from desktop.modern.core.interfaces.animation_interfaces import (
    IFadeOrchestrator,
    FadeOptions,
    StackFadeOptions,
    ParallelStackOperation,
    EasingType
)


class FadeSystemUsageExamples:
    """Examples of how to use the modern fade system."""
    
    def __init__(self, fade_orchestrator: IFadeOrchestrator):
        self.fade_orchestrator = fade_orchestrator
    
    # Basic fade operations
    
    async def example_fade_single_widget(self, widget: QWidget):
        """Example: Fade a single widget in and out."""
        # Fade out
        await self.fade_orchestrator.fade_widget_out(widget)
        
        # Fade in with custom options
        options = FadeOptions(
            duration=500,
            easing=EasingType.IN_OUT_CUBIC
        )
        await self.fade_orchestrator.fade_widget_in(widget, options)
    
    async def example_fade_multiple_widgets(self, widgets: List[QWidget]):
        """Example: Fade multiple widgets simultaneously."""
        # Fade all out together
        await self.fade_orchestrator.fade_widgets_out(widgets)
        
        # Wait a moment
        await asyncio.sleep(0.1)
        
        # Fade all in together
        await self.fade_orchestrator.fade_widgets_in(widgets)
    
    async def example_cross_fade(self, old_widget: QWidget, new_widget: QWidget):
        """Example: Cross-fade between two widgets."""
        await self.fade_orchestrator.cross_fade_widgets(old_widget, new_widget)
    
    async def example_fade_to_opacity(self, widget: QWidget):
        """Example: Fade widget to specific opacity."""
        # Fade to 50% opacity
        await self.fade_orchestrator.fade_to_opacity(widget, 0.5)
        
        # Fade back to full opacity
        await self.fade_orchestrator.fade_to_opacity(widget, 1.0)
    
    # Stack operations
    
    async def example_stack_transition(self, stack: QStackedWidget, new_index: int):
        """Example: Animated stack transition."""
        options = StackFadeOptions(
            duration=300,
            easing=EasingType.IN_OUT_QUAD
        )
        await self.fade_orchestrator.fade_stack_transition(stack, new_index, options)
    
    async def example_parallel_stack_transition(
        self, 
        left_stack: QStackedWidget,
        right_stack: QStackedWidget
    ):
        """Example: Parallel stack transition with layout changes."""
        operation = ParallelStackOperation(
            left_stack=left_stack,
            left_new_index=1,
            right_stack=right_stack,
            right_new_index=2,
            layout_ratio=(2, 1),  # 2:1 ratio
            options=StackFadeOptions(duration=400)
        )
        await self.fade_orchestrator.fade_parallel_stack_transition(operation)
    
    # Advanced operations
    
    async def example_fade_and_update(self, widgets: List[QWidget]):
        """Example: Fade out, update content, fade in."""
        def update_content():
            # Update your UI content here
            for widget in widgets:
                # Example: update widget content
                if hasattr(widget, 'setText'):
                    widget.setText("Updated content")
        
        await self.fade_orchestrator.fade_widgets_and_update(
            widgets, 
            update_content
        )
    
    async def example_sequential_fades(self, widgets: List[QWidget]):
        """Example: Sequential fade operations."""
        for i, widget in enumerate(widgets):
            # Stagger the fades with delays
            await asyncio.sleep(i * 0.1)
            await self.fade_orchestrator.fade_widget_in(widget)
    
    async def example_with_callbacks(self, widget: QWidget):
        """Example: Using callbacks with fades."""
        def on_fade_complete():
            print(f"Fade completed for widget: {widget}")
        
        options = FadeOptions(callback=on_fade_complete)
        await self.fade_orchestrator.fade_widget_in(widget, options)


class LegacyMigrationExamples:
    """Examples of migrating from legacy FadeManager to modern system."""
    
    def __init__(self, fade_orchestrator: IFadeOrchestrator):
        self.fade_orchestrator = fade_orchestrator
    
    async def migrate_widget_fade(self, widgets: List[QWidget]):
        """
        Legacy: fade_manager.widget_fader.fade_widgets(widgets, True, duration=250)
        Modern: await fade_orchestrator.fade_widgets_in(widgets, FadeOptions(duration=250))
        """
        # Legacy approach (for reference):
        # fade_manager.widget_fader.fade_widgets(widgets, True, duration=250)
        
        # Modern approach:
        options = FadeOptions(duration=250)
        await self.fade_orchestrator.fade_widgets_in(widgets, options)
    
    async def migrate_fade_and_update(self, widgets: List[QWidget]):
        """
        Legacy: fade_manager.widget_fader.fade_and_update(widgets, callback)
        Modern: await fade_orchestrator.fade_widgets_and_update(widgets, callback)
        """
        def update_callback():
            # Your update logic here
            pass
        
        # Legacy approach (for reference):
        # fade_manager.widget_fader.fade_and_update(widgets, update_callback)
        
        # Modern approach:
        await self.fade_orchestrator.fade_widgets_and_update(widgets, update_callback)
    
    async def migrate_stack_fade(self, stack: QStackedWidget, new_index: int):
        """
        Legacy: fade_manager.stack_fader.fade_stack(stack, new_index)
        Modern: await fade_orchestrator.fade_stack_transition(stack, new_index)
        """
        # Legacy approach (for reference):
        # fade_manager.stack_fader.fade_stack(stack, new_index)
        
        # Modern approach:
        await self.fade_orchestrator.fade_stack_transition(stack, new_index)
    
    async def migrate_parallel_stacks(
        self, 
        left_stack: QStackedWidget, 
        right_stack: QStackedWidget
    ):
        """
        Legacy: fade_manager.parallel_stack_fader.fade_both_stacks(...)
        Modern: await fade_orchestrator.fade_parallel_stack_transition(operation)
        """
        # Legacy approach (for reference):
        # fade_manager.parallel_stack_fader.fade_both_stacks(
        #     right_stack, 1, left_stack, 2, (2, 1), duration=300
        # )
        
        # Modern approach:
        operation = ParallelStackOperation(
            left_stack=left_stack,
            left_new_index=2,
            right_stack=right_stack,
            right_new_index=1,
            layout_ratio=(2, 1),
            options=StackFadeOptions(duration=300)
        )
        await self.fade_orchestrator.fade_parallel_stack_transition(operation)


class AsyncPatternExamples:
    """Examples of async/await patterns with the fade system."""
    
    def __init__(self, fade_orchestrator: IFadeOrchestrator):
        self.fade_orchestrator = fade_orchestrator
    
    async def example_error_handling(self, widget: QWidget):
        """Example: Proper error handling with async fades."""
        try:
            await self.fade_orchestrator.fade_widget_in(widget)
        except Exception as e:
            print(f"Fade operation failed: {e}")
            # Handle the error appropriately
    
    async def example_cancellation(self, widgets: List[QWidget]):
        """Example: Using asyncio for cancellation."""
        try:
            # Create a task that can be cancelled
            fade_task = asyncio.create_task(
                self.fade_orchestrator.fade_widgets_in(widgets)
            )
            
            # Wait with timeout
            await asyncio.wait_for(fade_task, timeout=5.0)
            
        except asyncio.TimeoutError:
            print("Fade operation timed out")
            fade_task.cancel()
    
    async def example_parallel_operations(self, widgets: List[QWidget]):
        """Example: Running multiple fade operations in parallel."""
        # Create multiple fade tasks
        tasks = [
            self.fade_orchestrator.fade_widget_in(widget)
            for widget in widgets
        ]
        
        # Wait for all to complete
        await asyncio.gather(*tasks)
    
    async def example_sequential_with_delays(self, widgets: List[QWidget]):
        """Example: Sequential operations with controlled timing."""
        for i, widget in enumerate(widgets):
            # Start fades with staggered timing
            if i > 0:
                await asyncio.sleep(0.1)  # 100ms delay between each
            
            await self.fade_orchestrator.fade_widget_in(widget)


# Integration with Qt event loop
class QtIntegrationExamples:
    """Examples of integrating async fade operations with Qt."""
    
    def __init__(self, fade_orchestrator: IFadeOrchestrator):
        self.fade_orchestrator = fade_orchestrator
    
    def sync_fade_for_slots(self, widget: QWidget):
        """
        Example: Using sync fade in Qt slots where async is not suitable.
        
        Note: This starts the animation but doesn't wait for completion.
        Use sparingly and prefer async methods when possible.
        """
        self.fade_orchestrator.fade_widget_sync(widget, fade_in=True)
    
    def create_callback_based_fade(self, widget: QWidget, completion_callback):
        """Example: Using callbacks instead of async/await when needed."""
        options = FadeOptions(callback=completion_callback)
        
        # Start async operation but don't await it
        asyncio.create_task(
            self.fade_orchestrator.fade_widget_in(widget, options)
        )
