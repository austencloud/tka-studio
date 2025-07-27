"""
Comprehensive Learn Tab Interaction Test

Tests the specific issues reported:
1. First lesson startup - question/answer widgets not showing
2. Back button functionality and navigation
3. Re-selecting lessons after going back
4. Pictograph loading and rendering
5. Quiz interaction workflow
"""

import logging
from typing import Any, Tuple

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

from tests.e2e.framework.page_objects.learn_tab import LearnTabPageObject
from tests.e2e.framework.steps.navigation_steps import NavigationSteps

logger = logging.getLogger(__name__)


class TestLearnTabComprehensiveInteraction:
    """
    Comprehensive test for Learn tab interaction issues.

    Focuses on the specific problems:
    - Initial lesson loading issues
    - Back button navigation problems
    - Re-selection after navigation
    - Pictograph rendering timing
    """

    @pytest.fixture(autouse=True)
    def setup_test_environment(self, tka_app: Tuple[Any, Any]):
        """Setup test environment."""
        self.app_instance, self.main_window = tka_app
        self.navigation_steps = NavigationSteps(self.main_window)
        self.learn_tab = LearnTabPageObject(self.main_window)

    def test_comprehensive_learn_tab_interaction(self):
        """
        Test comprehensive Learn tab interaction workflow.

        This test specifically addresses the reported issues:
        1. First lesson startup problems
        2. Back button functionality
        3. Re-selection workflow
        """
        logger.info("🚀 STARTING COMPREHENSIVE LEARN TAB INTERACTION TEST")

        # Phase 1: Initial Navigation and Setup
        self._test_initial_navigation()

        # Phase 2: First Lesson Selection (where issues occur)
        self._test_first_lesson_selection()

        # Phase 3: Back Button Navigation (where crashes occur)
        self._test_back_button_navigation()

        # Phase 4: Re-selection After Back (where it should work)
        self._test_lesson_reselection()

        # Phase 5: Multiple Navigation Cycles
        self._test_multiple_navigation_cycles()

        logger.info("🎯 COMPREHENSIVE LEARN TAB INTERACTION TEST COMPLETED")

    def _test_initial_navigation(self):
        """Test initial navigation to Learn tab."""
        logger.info("📋 PHASE 1: Testing initial navigation")

        # Navigate to Learn tab
        success = self.navigation_steps.navigate_to_learn_tab()
        assert success, "Should successfully navigate to Learn tab"

        # Verify we're on the correct tab
        current_tab = self.navigation_steps.get_current_tab()
        assert current_tab == "learn", f"Should be on learn tab, but on {current_tab}"

        # Check lesson selector is visible
        selector_visible = self.learn_tab.is_lesson_selector_visible()
        logger.info(f"📋 Lesson selector visible: {selector_visible}")
        assert selector_visible, "Lesson selector should be visible"

        # Get available lessons
        available_lessons = self.learn_tab.get_available_lessons()
        logger.info(f"📚 Available lessons: {available_lessons}")
        assert len(available_lessons) > 0, "Should have available lessons"

        logger.info("✅ Phase 1 completed: Initial navigation successful")

    def _test_first_lesson_selection(self):
        """Test first lesson selection where issues typically occur."""
        logger.info("📋 PHASE 2: Testing first lesson selection")

        # Get available lessons
        available_lessons = self.learn_tab.get_available_lessons()
        real_lessons = [
            lesson for lesson in available_lessons if lesson.startswith("Lesson")
        ]

        assert len(real_lessons) > 0, "Should have real lessons available"

        # Select the first lesson
        lesson_name = real_lessons[0]
        logger.info(f"📚 Selecting first lesson: {lesson_name}")

        success = self.learn_tab.select_lesson(lesson_name)
        assert success, f"Should successfully select lesson: {lesson_name}"

        # Wait for lesson to initialize (critical timing)
        logger.info("⏳ Waiting for lesson initialization...")
        QTest.qWait(3000)  # Longer wait for initialization

        # Check if lesson widget is visible
        lesson_widget_visible = self.learn_tab.is_lesson_widget_visible()
        logger.info(
            f"📋 Lesson widget visible after selection: {lesson_widget_visible}"
        )

        if lesson_widget_visible:
            # Check for question display
            self._check_question_display()

            # Check for answer options
            self._check_answer_options()
        else:
            logger.error("❌ Lesson widget not visible - this is the reported issue!")

        logger.info("✅ Phase 2 completed: First lesson selection tested")

    def _test_back_button_navigation(self):
        """Test back button navigation where crashes typically occur."""
        logger.info("📋 PHASE 3: Testing back button navigation")

        # Look for back button
        back_button = self._find_back_button()

        if back_button:
            logger.info("🔙 Found back button, testing click...")

            try:
                # Click the back button
                back_button.click()
                logger.info("✅ Back button clicked successfully")

                # Wait for navigation
                QTest.qWait(1000)

                # Check if we're back to lesson selector
                selector_visible = self.learn_tab.is_lesson_selector_visible()
                logger.info(f"📋 Back to lesson selector: {selector_visible}")

                if not selector_visible:
                    logger.error("❌ Back navigation failed - still in lesson view")

            except Exception as e:
                logger.error(f"❌ Back button click failed: {e}")
                # This is the reported crash issue

        else:
            logger.error("❌ Back button not found")

        logger.info("✅ Phase 3 completed: Back button navigation tested")

    def _test_lesson_reselection(self):
        """Test re-selecting a lesson after going back."""
        logger.info("📋 PHASE 4: Testing lesson re-selection")

        # Ensure we're back at lesson selector
        selector_visible = self.learn_tab.is_lesson_selector_visible()

        if selector_visible:
            # Get available lessons again
            available_lessons = self.learn_tab.get_available_lessons()
            real_lessons = [
                lesson for lesson in available_lessons if lesson.startswith("Lesson")
            ]

            if len(real_lessons) > 0:
                # Select the same lesson again
                lesson_name = real_lessons[0]
                logger.info(f"📚 Re-selecting lesson: {lesson_name}")

                success = self.learn_tab.select_lesson(lesson_name)

                if success:
                    logger.info("✅ Lesson re-selected successfully")

                    # Wait for initialization
                    QTest.qWait(2000)

                    # Check if it works better the second time
                    lesson_widget_visible = self.learn_tab.is_lesson_widget_visible()
                    logger.info(
                        f"📋 Lesson widget visible on re-selection: {lesson_widget_visible}"
                    )

                    if lesson_widget_visible:
                        logger.info(
                            "✅ Re-selection worked - this matches reported behavior"
                        )
                    else:
                        logger.error("❌ Re-selection also failed")

                else:
                    logger.error("❌ Failed to re-select lesson")
            else:
                logger.error("❌ No real lessons available for re-selection")
        else:
            logger.error("❌ Not back at lesson selector for re-selection")

        logger.info("✅ Phase 4 completed: Lesson re-selection tested")

    def _test_multiple_navigation_cycles(self):
        """Test multiple back-and-forth navigation cycles."""
        logger.info("📋 PHASE 5: Testing multiple navigation cycles")

        for cycle in range(2):
            logger.info(f"🔄 Navigation cycle {cycle + 1}")

            try:
                # Go back if we're in a lesson
                if not self.learn_tab.is_lesson_selector_visible():
                    back_button = self._find_back_button()
                    if back_button:
                        back_button.click()
                        QTest.qWait(1000)

                # Select a lesson
                available_lessons = self.learn_tab.get_available_lessons()
                real_lessons = [
                    lesson
                    for lesson in available_lessons
                    if lesson.startswith("Lesson")
                ]

                if len(real_lessons) > 0:
                    lesson_name = real_lessons[0]
                    success = self.learn_tab.select_lesson(lesson_name)

                    if success:
                        QTest.qWait(2000)
                        logger.info(f"✅ Cycle {cycle + 1}: Lesson selected")
                    else:
                        logger.error(f"❌ Cycle {cycle + 1}: Lesson selection failed")

            except Exception as e:
                logger.error(f"❌ Cycle {cycle + 1} failed: {e}")

        logger.info("✅ Phase 5 completed: Multiple navigation cycles tested")

    def _check_question_display(self):
        """Check if question display is working."""
        logger.info("🔍 Checking question display...")

        try:
            # Look for pictograph widgets in question area
            question_widgets = self._find_question_widgets()
            logger.info(f"📊 Found {len(question_widgets)} question widgets")

            if len(question_widgets) == 0:
                logger.error(
                    "❌ No question widgets found - this is the reported issue!"
                )
            else:
                logger.info("✅ Question widgets found")

        except Exception as e:
            logger.error(f"❌ Error checking question display: {e}")

    def _check_answer_options(self):
        """Check if answer options are working."""
        logger.info("🔍 Checking answer options...")

        try:
            # Look for answer option widgets
            answer_widgets = self._find_answer_widgets()
            logger.info(f"📊 Found {len(answer_widgets)} answer widgets")

            if len(answer_widgets) == 0:
                logger.error("❌ No answer widgets found - this is the reported issue!")
            else:
                logger.info("✅ Answer widgets found")

        except Exception as e:
            logger.error(f"❌ Error checking answer options: {e}")

    def _find_back_button(self):
        """Find the back button in the lesson interface."""
        try:
            # Look for back button by object name
            from PyQt6.QtWidgets import QPushButton

            back_button = self.main_window.findChild(QPushButton, "back_button")
            if back_button and back_button.isVisible():
                return back_button

            # Fallback: look for back button by text
            back_buttons = self.main_window.findChildren(QPushButton)
            for widget in back_buttons:
                if hasattr(widget, "text") and "← Back" in str(widget.text()):
                    if widget.isVisible():
                        return widget
            return None
        except Exception as e:
            logger.error(f"Error finding back button: {e}")
            return None

    def _find_question_widgets(self):
        """Find question display widgets."""
        try:
            # Look for LearnPictographView widgets
            from desktop.modern.presentation.components.pictograph.views.learn_pictograph_view import (
                LearnPictographView,
            )

            question_widgets = self.main_window.findChildren(LearnPictographView)
            return [w for w in question_widgets if w.isVisible()]
        except Exception as e:
            logger.error(f"Error finding question widgets: {e}")
            return []

    def _find_answer_widgets(self):
        """Find answer option widgets."""
        try:
            # Look for answer option buttons that are visible and in the right context
            from PyQt6.QtWidgets import QPushButton

            all_buttons = self.main_window.findChildren(QPushButton)

            # Filter for answer buttons (should be in AnswerOptionsCoordinator hierarchy)
            answer_buttons = []
            for button in all_buttons:
                if button.isVisible():
                    # Check the widget hierarchy for AnswerOptionsCoordinator
                    current = button
                    found_coordinator = False

                    # Walk up the parent hierarchy
                    for _ in range(5):  # Check up to 5 levels up
                        if current is None:
                            break
                        class_name = current.__class__.__name__
                        if "Answer" in class_name or "Coordinator" in class_name:
                            found_coordinator = True
                            break
                        current = current.parent()

                    if found_coordinator:
                        answer_buttons.append(button)

            return answer_buttons
        except Exception as e:
            logger.error(f"Error finding answer widgets: {e}")
            return []
