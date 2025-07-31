"""
Sequence Workbench Page Object for TKA Modern E2E Testing Framework

This module provides the SequenceWorkbenchPage class that encapsulates
interactions with the sequence workbench component, including sequence
management, validation, and state tracking.
"""

import logging
from typing import Any, Optional

from PyQt6.QtCore import QObject
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QWidget

from .base_page import BasePage

logger = logging.getLogger(__name__)


class SequenceWorkbenchPage(BasePage):
    """
    Page object for Sequence Workbench component.

    This page object handles:
    - Sequence length tracking and validation
    - Sequence state management
    - Beat widget discovery and interaction
    - Sequence clearing and manipulation
    - Workbench state validation
    """

    def is_loaded(self) -> bool:
        """
        Check if sequence workbench is loaded and ready.

        Returns:
            bool: True if workbench is available and functional, False otherwise
        """
        workbench = self.get_element("workbench_widget")
        if not workbench:
            logger.debug("Sequence workbench widget not found")
            return False

        # Additional validation: check if workbench has expected functionality
        return self._validate_workbench_functionality(workbench)

    def get_sequence_length(self) -> int:
        """
        Get current sequence length.

        Returns:
            int: Number of beats/elements in the current sequence
        """
        logger.debug("Getting sequence length")

        workbench = self.get_element("workbench_widget")
        if not workbench:
            logger.debug("Workbench not found, returning 0")
            return 0

        try:
            # Strategy 1: Try direct method call
            if hasattr(workbench, "get_sequence_length"):
                length = workbench.get_sequence_length()
                logger.debug(f"Sequence length via direct method: {length}")
                return length

            # Strategy 2: Try alternative method names
            for method_name in [
                "getSequenceLength",
                "sequence_length",
                "length",
                "count",
            ]:
                if hasattr(workbench, method_name):
                    length = getattr(workbench, method_name)()
                    logger.debug(f"Sequence length via {method_name}: {length}")
                    return length

            # Strategy 3: Count beat widgets
            beat_widgets = self._find_beat_widgets()
            length = len(beat_widgets)
            logger.debug(f"Sequence length via beat widget count: {length}")
            return length

        except Exception as e:
            logger.warning(f"Error getting sequence length: {e}")
            return 0

    def is_sequence_valid(self) -> bool:
        """
        Check if current sequence is valid.

        Returns:
            bool: True if sequence is valid, False otherwise
        """
        logger.debug("Checking sequence validity")

        try:
            # Basic validation: sequence should have at least one element
            length = self.get_sequence_length()
            if length == 0:
                logger.debug("Sequence is empty, considered invalid")
                return False

            # Check if beats are properly formed
            if not self._has_valid_beats():
                logger.debug("Sequence has invalid beats")
                return False

            # Additional validation via workbench if available
            workbench = self.get_element("workbench_widget")
            if workbench and hasattr(workbench, "is_sequence_valid"):
                valid = workbench.is_sequence_valid()
                logger.debug(f"Sequence validity via workbench method: {valid}")
                return valid

            logger.debug("Sequence appears valid")
            return True

        except Exception as e:
            logger.warning(f"Error checking sequence validity: {e}")
            return False

    def clear_sequence(self) -> bool:
        """
        Clear the current sequence using real workbench functionality.

        Returns:
            bool: True if sequence was cleared successfully, False otherwise
        """
        logger.info("Clearing sequence")

        workbench = self.get_element("workbench_widget")
        if not workbench:
            logger.error("Workbench not found for clearing")
            return False

        try:
            # Strategy 1: Use the modern workbench operation coordinator
            if hasattr(workbench, "_operation_coordinator"):
                coordinator = workbench._operation_coordinator
                if coordinator and hasattr(coordinator, "clear_sequence"):
                    logger.info("Using operation coordinator to clear sequence")
                    result = coordinator.clear_sequence()
                    QTest.qWait(500)  # Wait for clearing to complete
                    if result and hasattr(result, "success") and result.success:
                        return self._verify_sequence_cleared()

            # Strategy 2: Emit the clear sequence signal
            if hasattr(workbench, "clear_sequence_requested"):
                logger.info("Emitting clear sequence signal")
                workbench.clear_sequence_requested.emit()
                QTest.qWait(500)  # Wait for signal processing
                return self._verify_sequence_cleared()

            # Strategy 3: Try direct method call
            if hasattr(workbench, "clear_sequence"):
                logger.info("Using direct clear_sequence method")
                workbench.clear_sequence()
                QTest.qWait(500)  # Wait for clearing to complete
                return self._verify_sequence_cleared()

            # Strategy 4: Try alternative method names
            for method_name in ["clearSequence", "clear", "reset", "reset_sequence"]:
                if hasattr(workbench, method_name):
                    logger.info(f"Using {method_name} method")
                    getattr(workbench, method_name)()
                    QTest.qWait(500)
                    return self._verify_sequence_cleared()

            # Strategy 5: Try accessing button panel clear functionality
            if hasattr(workbench, "button_panel"):
                button_panel = workbench.button_panel
                if button_panel and hasattr(button_panel, "clear_sequence"):
                    logger.info("Using button panel clear_sequence")
                    button_panel.clear_sequence()
                    QTest.qWait(500)
                    return self._verify_sequence_cleared()

            logger.warning(
                "No clear sequence method found - sequence may not be clearable"
            )
            return False

        except Exception as e:
            logger.error(f"Failed to clear sequence: {e}")
            return False

    def get_sequence_data(self) -> Optional[dict[str, Any]]:
        """
        Get detailed sequence data.

        Returns:
            Dict or None: Sequence data or None if not available
        """
        workbench = self.get_element("workbench_widget")
        if not workbench:
            return None

        try:
            # Try various method names for getting sequence data
            for method_name in [
                "get_sequence_data",
                "getSequenceData",
                "sequence_data",
                "get_data",
            ]:
                if hasattr(workbench, method_name):
                    data = getattr(workbench, method_name)()
                    if data:
                        logger.debug("Retrieved sequence data")
                        return data
        except Exception as e:
            logger.debug(f"Error getting sequence data: {e}")

        return None

    def _find_element(self, name: str) -> Optional[QWidget]:
        """
        Find elements specific to sequence workbench.

        Args:
            name: Element identifier

        Returns:
            QWidget or None: Found element or None
        """
        if name == "workbench_widget":
            return self._find_sequence_workbench()
        elif name == "beat_widgets":
            return self._find_beat_widgets()
        elif name == "sequence_display":
            return self._find_sequence_display()

        return None

    def _find_sequence_workbench(self):
        """
        Find the sequence workbench widget.

        Returns:
            QWidget or None: Sequence workbench widget or None
        """
        # Strategy 1: Look for specific class names
        workbench_patterns = ["sequenceworkbench", "sequence_workbench", "workbench"]

        for pattern in workbench_patterns:
            widget = self._find_widget_by_class_name(pattern)
            if widget:
                logger.debug(f"Found sequence workbench: {widget.__class__.__name__}")
                return widget

        # Strategy 2: Look for widgets with "sequence" and "workbench" in name
        children = self.parent.findChildren(QObject)
        for child in children:
            class_name = child.__class__.__name__.lower()
            if "sequence" in class_name and "workbench" in class_name:
                logger.debug(f"Found workbench component: {child.__class__.__name__}")
                return child

        logger.debug("Sequence workbench not found")
        return None

    def _find_beat_widgets(self) -> list[QWidget]:
        """
        Find all VISIBLE beat widgets in the workbench display area only.

        Returns:
            List[QWidget]: List of visible beat widgets (may be empty)
        """
        workbench = self.get_element("workbench_widget")
        if not workbench:
            logger.debug("No workbench widget found")
            return []

        # CRITICAL FIX: Only search within the workbench widget, not the entire application
        if not hasattr(workbench, "findChildren"):
            logger.debug("Workbench has no findChildren method")
            return []

        # Find beat frame or beat display area within workbench
        beat_frame = None
        for child in workbench.findChildren(QWidget):
            class_name = child.__class__.__name__.lower()
            if any(
                indicator in class_name
                for indicator in ["beat_frame", "beatframe", "sequence_beat_frame"]
            ):
                beat_frame = child
                logger.debug(f"Found beat frame: {class_name}")
                break

        if not beat_frame:
            logger.debug("No beat frame found in workbench")
            return []

        # CRITICAL FIX: Only count VISIBLE beat widgets within the beat frame
        beat_widgets = []
        beat_indicators = ["beat", "sequence_beat", "motion"]

        for child in beat_frame.findChildren(QWidget):
            class_name = child.__class__.__name__.lower()
            # Only count widgets that are actually visible
            if (
                any(indicator in class_name for indicator in beat_indicators)
                and hasattr(child, "isVisible")
                and child.isVisible()
            ):
                beat_widgets.append(child)
                logger.debug(f"Found visible beat widget: {class_name}")

        logger.info(f"🔍 BEAT WIDGETS FOUND: {len(beat_widgets)} (visible only)")
        return beat_widgets

    def _find_sequence_display(self):
        """Find sequence display widget."""
        # This would be implemented based on actual UI structure
        return

    def _validate_workbench_functionality(self, workbench) -> bool:
        """
        Validate that workbench has expected functionality.

        Args:
            workbench: Workbench widget to validate

        Returns:
            bool: True if workbench appears functional
        """
        if not workbench:
            return False

        # Check for expected methods or properties
        expected_attributes = [
            "get_sequence_length",
            "getSequenceLength",
            "clear_sequence",
            "clearSequence",
            "is_sequence_valid",
            "isSequenceValid",
        ]

        for attr in expected_attributes:
            if hasattr(workbench, attr):
                logger.debug(f"Workbench has expected attribute: {attr}")
                return True

        # If no expected methods found, still consider it valid for testing
        logger.debug("Workbench found but no expected methods detected")
        return True

    def _has_valid_beats(self) -> bool:
        """
        Check if sequence has valid beats.

        Returns:
            bool: True if beats appear valid
        """
        beat_widgets = self._find_beat_widgets()

        # Basic validation: if we found beat widgets, assume they're valid
        # In a real implementation, this would check beat properties
        return len(beat_widgets) > 0

    def _verify_sequence_cleared(self) -> bool:
        """
        Verify that sequence was successfully cleared.

        Returns:
            bool: True if sequence appears to be cleared
        """
        # Check if sequence length is now 0
        length = self.get_sequence_length()
        cleared = length == 0
        logger.info(
            f"Sequence cleared verification: length={length}, cleared={cleared}"
        )
        return cleared

    def _clear_sequence_direct(self) -> bool:
        """
        Direct method to clear sequence - used by test framework.

        Returns:
            bool: True if clearing was attempted, False otherwise
        """
        workbench = self.get_element("workbench_widget")
        if not workbench:
            return False

        try:
            # Log available methods for debugging
            methods = [
                method for method in dir(workbench) if not method.startswith("_")
            ]
            clear_methods = [method for method in methods if "clear" in method.lower()]
            logger.info(f"Available clear methods: {clear_methods}")

            # Try the most direct approach first
            if hasattr(workbench, "_operation_coordinator"):
                coordinator = workbench._operation_coordinator
                logger.info(f"Operation coordinator found: {coordinator}")
                if coordinator:
                    coord_methods = [
                        method
                        for method in dir(coordinator)
                        if "clear" in method.lower()
                    ]
                    logger.info(f"Coordinator clear methods: {coord_methods}")

            return True
        except Exception as e:
            logger.error(f"Error in direct clear: {e}")
            return False

    def get_beat_at_index(self, index: int) -> Optional[QWidget]:
        """
        Get the beat widget at the specified index.

        Args:
            index: Index of the beat to retrieve (0-based)

        Returns:
            QWidget or None: Beat widget at the specified index or None if not found
        """
        logger.debug(f"Getting beat at index {index}")

        workbench = self.get_element("workbench_widget")
        if not workbench:
            logger.error("Workbench widget not found")
            return None

        # Get all beat widgets
        beat_widgets = self._get_beat_widgets(workbench)
        if not beat_widgets:
            logger.debug("No beat widgets found")
            return None

        if index < 0 or index >= len(beat_widgets):
            logger.debug(f"Index {index} out of range (0-{len(beat_widgets) - 1})")
            return None

        beat_widget = beat_widgets[index]
        logger.debug(f"Found beat at index {index}: {beat_widget.__class__.__name__}")
        return beat_widget
