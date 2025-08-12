"""
Learn Navigation Service Implementation

Manages navigation state and transitions for the learn tab,
following the stack-based navigation pattern.
"""

from __future__ import annotations

import logging

from desktop.modern.core.interfaces.learn_services import ILearnNavigationService


logger = logging.getLogger(__name__)


class LearnNavigationService(ILearnNavigationService):
    """
    Production implementation of learn tab navigation management.

    Manages navigation state between lesson selector, lesson view,
    and results view using stack-based navigation.
    """

    # Navigation view constants
    VIEW_LESSON_SELECTOR = "lesson_selector"
    VIEW_LESSON = "lesson"
    VIEW_RESULTS = "results"

    def __init__(self):
        """Initialize learn navigation service."""
        self._current_view: str = self.VIEW_LESSON_SELECTOR
        self._current_session_id: str | None = None
        self._navigation_history: list[str] = [self.VIEW_LESSON_SELECTOR]

        logger.info("Learn navigation service initialized")

    def navigate_to_lesson_selector(self) -> None:
        """Navigate to lesson selector view."""
        try:
            self._current_view = self.VIEW_LESSON_SELECTOR
            self._current_session_id = None
            self._add_to_history(self.VIEW_LESSON_SELECTOR)

            logger.debug("Navigated to lesson selector")

        except Exception as e:
            logger.exception(f"Failed to navigate to lesson selector: {e}")

    def navigate_to_lesson(self, session_id: str) -> None:
        """
        Navigate to lesson view.

        Args:
            session_id: Session to navigate to
        """
        try:
            if not session_id:
                logger.warning("Cannot navigate to lesson with empty session ID")
                return

            self._current_view = self.VIEW_LESSON
            self._current_session_id = session_id
            self._add_to_history(self.VIEW_LESSON)

            logger.debug(f"Navigated to lesson view for session {session_id}")

        except Exception as e:
            logger.exception(f"Failed to navigate to lesson for session {session_id}: {e}")

    def navigate_to_results(self, session_id: str) -> None:
        """
        Navigate to results view.

        Args:
            session_id: Session to show results for
        """
        try:
            if not session_id:
                logger.warning("Cannot navigate to results with empty session ID")
                return

            self._current_view = self.VIEW_RESULTS
            self._current_session_id = session_id
            self._add_to_history(self.VIEW_RESULTS)

            logger.debug(f"Navigated to results view for session {session_id}")

        except Exception as e:
            logger.exception(f"Failed to navigate to results for session {session_id}: {e}")

    def get_current_view(self) -> str:
        """
        Get current view identifier.

        Returns:
            String identifier for current view
        """
        return self._current_view

    def get_current_session_id(self) -> str | None:
        """
        Get current session ID if in lesson or results view.

        Returns:
            Current session ID or None if in selector view
        """
        return self._current_session_id

    def can_navigate_back(self) -> bool:
        """
        Check if back navigation is possible.

        Returns:
            True if can navigate back, False otherwise
        """
        try:
            # Can navigate back if there's history beyond current view
            return len(self._navigation_history) > 1
        except Exception as e:
            logger.exception(f"Failed to check back navigation: {e}")
            return False

    def navigate_back(self) -> bool:
        """
        Navigate to previous view.

        Returns:
            True if navigation successful, False otherwise
        """
        try:
            if not self.can_navigate_back():
                logger.debug("Cannot navigate back - no history")
                return False

            # Remove current view from history
            if self._navigation_history:
                self._navigation_history.pop()

            # Navigate to previous view
            if self._navigation_history:
                previous_view = self._navigation_history[-1]

                if previous_view == self.VIEW_LESSON_SELECTOR:
                    self.navigate_to_lesson_selector()
                elif previous_view == self.VIEW_LESSON:
                    # For lesson view, we need session ID - this might need special handling
                    logger.warning(
                        "Cannot navigate back to lesson view without session ID"
                    )
                    self.navigate_to_lesson_selector()
                elif previous_view == self.VIEW_RESULTS:
                    # For results view, we need session ID - this might need special handling
                    logger.warning(
                        "Cannot navigate back to results view without session ID"
                    )
                    self.navigate_to_lesson_selector()

                logger.debug(f"Navigated back to {previous_view}")
                return True
            # Fallback to lesson selector
            self.navigate_to_lesson_selector()
            return True

        except Exception as e:
            logger.exception(f"Failed to navigate back: {e}")
            return False

    def get_navigation_stack_index(self) -> int:
        """
        Get current stack index for QStackedWidget.

        Returns:
            Stack index (0=selector, 1=lesson, 2=results)
        """
        try:
            view_to_index = {
                self.VIEW_LESSON_SELECTOR: 0,
                self.VIEW_LESSON: 1,
                self.VIEW_RESULTS: 2,
            }

            return view_to_index.get(self._current_view, 0)

        except Exception as e:
            logger.exception(f"Failed to get navigation stack index: {e}")
            return 0

    def reset_navigation(self) -> None:
        """Reset navigation to initial state."""
        try:
            self._current_view = self.VIEW_LESSON_SELECTOR
            self._current_session_id = None
            self._navigation_history = [self.VIEW_LESSON_SELECTOR]

            logger.debug("Navigation state reset")

        except Exception as e:
            logger.exception(f"Failed to reset navigation: {e}")

    def _add_to_history(self, view: str) -> None:
        """
        Add view to navigation history.

        Args:
            view: View identifier to add
        """
        try:
            # Avoid duplicate consecutive entries
            if not self._navigation_history or self._navigation_history[-1] != view:
                self._navigation_history.append(view)

            # Limit history size to prevent memory growth
            max_history_size = 10
            if len(self._navigation_history) > max_history_size:
                self._navigation_history = self._navigation_history[-max_history_size:]

        except Exception as e:
            logger.exception(f"Failed to add view to history: {e}")

    def get_navigation_state(self) -> dict:
        """
        Get current navigation state for debugging.

        Returns:
            Dictionary with navigation state information
        """
        try:
            return {
                "current_view": self._current_view,
                "current_session_id": self._current_session_id,
                "navigation_history": self._navigation_history.copy(),
                "stack_index": self.get_navigation_stack_index(),
                "can_navigate_back": self.can_navigate_back(),
            }
        except Exception as e:
            logger.exception(f"Failed to get navigation state: {e}")
            return {
                "current_view": "unknown",
                "current_session_id": None,
                "navigation_history": [],
                "stack_index": 0,
                "can_navigate_back": False,
            }
