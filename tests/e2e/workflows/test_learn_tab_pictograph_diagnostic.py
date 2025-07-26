"""
Learn Tab Pictograph Rendering Diagnostic Test

This test focuses specifically on diagnosing pictograph rendering issues
and answer option management problems in the Learn tab.
"""

import logging
from typing import Any, Tuple

import pytest
from PyQt6.QtCore import QObject
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QWidget

from tests.e2e.framework.page_objects.browse_tab import BrowseTabPageObject
from tests.e2e.framework.page_objects.construct_tab import ConstructTabPage
from tests.e2e.framework.page_objects.learn_tab import LearnTabPageObject
from tests.e2e.framework.page_objects.sequence_card_tab import SequenceCardTabPageObject
from tests.e2e.framework.page_objects.sequence_workbench import SequenceWorkbenchPage
from tests.e2e.framework.steps.navigation_steps import NavigationSteps

logger = logging.getLogger(__name__)


class TestLearnTabPictographDiagnostic:
    """
    Focused diagnostic test for Learn tab pictograph rendering and component management.

    This test systematically investigates:
    1. Answer option count issues (finding 10 instead of 4)
    2. Pictograph rendering failures in lesson interfaces
    3. Component cleanup between questions
    4. Service integration issues
    """

    @pytest.fixture(autouse=True)
    def setup_test_environment(self, tka_app: Tuple[Any, Any]):
        """Setup test environment for diagnostic testing."""
        self.app_instance, self.main_window = tka_app
        self.navigation_steps = NavigationSteps(self.main_window)
        self.learn_tab = LearnTabPageObject(self.main_window)

    def test_learn_tab_pictograph_diagnostic(self):
        """
        Comprehensive diagnostic test for Learn tab pictograph rendering issues.

        This test systematically investigates all aspects of Learn tab functionality
        to identify the root causes of pictograph rendering failures.
        """
        logger.info("🔬 STARTING LEARN TAB PICTOGRAPH DIAGNOSTIC TEST")

        # ========================================
        # PHASE 1: BASIC NAVIGATION AND SETUP
        # ========================================
        logger.info("📋 PHASE 1: Basic navigation and component verification")

        # Navigate to Learn tab
        success = self.navigation_steps.navigate_to_learn_tab()
        assert success, "Should successfully navigate to Learn tab"

        current_tab = self.navigation_steps.get_current_tab()
        assert current_tab == "learn", f"Should be on learn tab, but on {current_tab}"
        logger.info("✅ Successfully navigated to Learn tab")

        # ========================================
        # PHASE 2: LESSON AVAILABILITY INVESTIGATION
        # ========================================
        logger.info("🔍 PHASE 2: Investigating lesson availability and structure")

        # Check lesson selector visibility
        selector_visible = self.learn_tab.is_lesson_selector_visible()
        logger.info(f"📋 Lesson selector visible: {selector_visible}")

        if selector_visible:
            # Get available lessons
            available_lessons = self.learn_tab.get_available_lessons()
            logger.info(f"📚 Available lessons: {available_lessons}")
            logger.info(f"📊 Total lesson count: {len(available_lessons)}")

            # Investigate lesson components
            self._investigate_lesson_components()

            # Test each lesson systematically
            for lesson_name in available_lessons:
                self._test_individual_lesson(lesson_name)

        else:
            logger.error(
                "❌ Lesson selector not visible - cannot proceed with diagnostic"
            )

        logger.info("🎯 LEARN TAB PICTOGRAPH DIAGNOSTIC COMPLETED")

    def _investigate_lesson_components(self):
        """Investigate the structure of lesson components."""
        logger.info("  🔍 Investigating lesson component structure")

        try:
            # Find all lesson-related widgets
            if hasattr(self.main_window, "findChildren"):
                all_children = self.main_window.findChildren(QObject)

                lesson_components = []
                answer_components = []
                pictograph_components = []

                for child in all_children:
                    class_name = child.__class__.__name__

                    # Categorize components
                    if any(
                        keyword in class_name.lower() for keyword in ["lesson", "learn"]
                    ):
                        lesson_components.append(class_name)
                    elif any(
                        keyword in class_name.lower()
                        for keyword in ["answer", "option", "choice"]
                    ):
                        answer_components.append(class_name)
                    elif any(
                        keyword in class_name.lower()
                        for keyword in ["pictograph", "view", "scene"]
                    ):
                        pictograph_components.append(class_name)

                logger.info(
                    f"  📋 Lesson components found: {len(set(lesson_components))} types"
                )
                logger.info(
                    f"  🔤 Answer components found: {len(set(answer_components))} types"
                )
                logger.info(
                    f"  🎨 Pictograph components found: {len(set(pictograph_components))} types"
                )

                # Log unique component types
                if lesson_components:
                    logger.info(
                        f"  📋 Lesson component types: {set(lesson_components)}"
                    )
                if answer_components:
                    logger.info(
                        f"  🔤 Answer component types: {set(answer_components)}"
                    )
                if pictograph_components:
                    logger.info(
                        f"  🎨 Pictograph component types: {set(pictograph_components)}"
                    )

        except Exception as e:
            logger.warning(f"  ⚠️ Error investigating lesson components: {e}")

    def _test_individual_lesson(self, lesson_name: str):
        """Test an individual lesson for pictograph rendering and answer options."""
        logger.info(f"  🎓 TESTING LESSON: {lesson_name}")

        try:
            # Select the lesson
            logger.info(f"    🎯 Selecting lesson: {lesson_name}")
            success = self.learn_tab.select_lesson(lesson_name)

            if success:
                logger.info(f"    ✅ Successfully selected lesson: {lesson_name}")

                # Wait for lesson to initialize
                QTest.qWait(2000)

                # Check if lesson widget is visible
                lesson_widget_visible = self.learn_tab.is_lesson_widget_visible()
                logger.info(f"    📋 Lesson widget visible: {lesson_widget_visible}")

                if lesson_widget_visible:
                    # Investigate pictograph rendering
                    self._investigate_pictograph_rendering(lesson_name)

                    # Investigate answer options
                    self._investigate_answer_options(lesson_name)

                    # Test question progression
                    self._test_question_progression(lesson_name)

                else:
                    logger.warning(f"    ⚠️ Lesson widget not visible for {lesson_name}")

                # Navigate back to selector for next lesson
                self._navigate_back_to_selector()

            else:
                logger.warning(f"    ⚠️ Failed to select lesson: {lesson_name}")

        except Exception as e:
            logger.error(f"    ❌ Error testing lesson {lesson_name}: {e}")

    def _investigate_pictograph_rendering(self, lesson_name: str):
        """Investigate pictograph rendering in the current lesson."""
        logger.info(f"      🎨 Investigating pictograph rendering for {lesson_name}")

        try:
            # Look for lesson-specific pictograph components
            learn_pictograph_widgets = self._find_learn_pictograph_widgets()
            logger.info(
                f"      🎨 Found {len(learn_pictograph_widgets)} Learn-specific pictograph widgets"
            )

            for i, widget in enumerate(learn_pictograph_widgets):
                widget_class = widget.__class__.__name__
                logger.info(f"      🎨 Learn pictograph widget {i+1}: {widget_class}")

                # Check if widget is visible and has content
                if hasattr(widget, "isVisible"):
                    visible = widget.isVisible()
                    logger.info(f"        📋 Widget {i+1} visible: {visible}")

                    if visible:
                        # Check widget size
                        if hasattr(widget, "size"):
                            size = widget.size()
                            logger.info(
                                f"        📏 Widget {i+1} size: {size.width()}x{size.height()}"
                            )

                        # Check for pictograph data
                        if hasattr(widget, "pictograph_data"):
                            has_data = widget.pictograph_data is not None
                            logger.info(
                                f"        📊 Widget {i+1} has pictograph data: {has_data}"
                            )

                        # Check for scene content
                        if hasattr(widget, "scene"):
                            scene = widget.scene()
                            if scene and hasattr(scene, "items"):
                                item_count = len(scene.items())
                                logger.info(
                                    f"        🎭 Widget {i+1} scene items: {item_count}"
                                )
                            else:
                                logger.warning(
                                    f"        ⚠️ Widget {i+1} has no scene or scene items"
                                )

                        # Check for rendering status
                        if hasattr(widget, "is_rendered"):
                            rendered = widget.is_rendered()
                            logger.info(f"        ✅ Widget {i+1} rendered: {rendered}")

            # Specifically check for question and answer pictographs
            self._check_question_pictograph_rendering()
            self._check_answer_pictograph_rendering()

        except Exception as e:
            logger.warning(f"      ⚠️ Error investigating pictograph rendering: {e}")

    def _check_question_pictograph_rendering(self):
        """Check if question pictographs are rendering correctly."""
        logger.info("        🔍 Checking question pictograph rendering")

        try:
            # Look for question display pictographs
            question_pictographs = []
            if hasattr(self.main_window, "findChildren"):
                all_children = self.main_window.findChildren(QWidget)

                for child in all_children:
                    class_name = child.__class__.__name__
                    if "LearnPictographView" in class_name and hasattr(
                        child, "isVisible"
                    ):
                        if child.isVisible():
                            # Check size to determine if it's question (larger) or answer (smaller)
                            if hasattr(child, "size"):
                                size = child.size()
                                if (
                                    size.width() >= 400
                                ):  # Question pictographs are typically larger
                                    question_pictographs.append(child)
                                    logger.info(
                                        f"        📋 Question pictograph found: {size.width()}x{size.height()}"
                                    )

                                    # Check if it has actual content
                                    if hasattr(child, "scene"):
                                        scene = child.scene()
                                        if scene and hasattr(scene, "items"):
                                            items = scene.items()
                                            logger.info(
                                                f"        🎭 Question pictograph has {len(items)} scene items"
                                            )

                                            # Check for specific pictograph elements
                                            for item in items[
                                                :5
                                            ]:  # Check first 5 items
                                                item_type = item.__class__.__name__
                                                logger.info(
                                                    f"          🎨 Scene item: {item_type}"
                                                )
                                        else:
                                            logger.warning(
                                                "        ⚠️ Question pictograph has no scene content"
                                            )

            if not question_pictographs:
                logger.warning("        ⚠️ No visible question pictographs found")
            else:
                logger.info(
                    f"        ✅ Found {len(question_pictographs)} visible question pictographs"
                )

        except Exception as e:
            logger.warning(
                f"        ⚠️ Error checking question pictograph rendering: {e}"
            )

    def _check_answer_pictograph_rendering(self):
        """Check if answer option pictographs are rendering correctly."""
        logger.info("        🔍 Checking answer pictograph rendering")

        try:
            # Look for answer option pictographs
            answer_pictographs = []
            if hasattr(self.main_window, "findChildren"):
                all_children = self.main_window.findChildren(QWidget)

                for child in all_children:
                    class_name = child.__class__.__name__
                    if "LearnPictographView" in class_name and hasattr(
                        child, "isVisible"
                    ):
                        if child.isVisible():
                            # Check size to determine if it's answer (smaller)
                            if hasattr(child, "size"):
                                size = child.size()
                                if (
                                    size.width() < 400
                                ):  # Answer pictographs are typically smaller
                                    answer_pictographs.append(child)
                                    logger.info(
                                        f"        🔤 Answer pictograph found: {size.width()}x{size.height()}"
                                    )

                                    # Check if it has actual content
                                    if hasattr(child, "scene"):
                                        scene = child.scene()
                                        if scene and hasattr(scene, "items"):
                                            items = scene.items()
                                            logger.info(
                                                f"        🎭 Answer pictograph has {len(items)} scene items"
                                            )
                                        else:
                                            logger.warning(
                                                "        ⚠️ Answer pictograph has no scene content"
                                            )

            if not answer_pictographs:
                logger.warning("        ⚠️ No visible answer pictographs found")
            else:
                logger.info(
                    f"        ✅ Found {len(answer_pictographs)} visible answer pictographs"
                )

        except Exception as e:
            logger.warning(f"        ⚠️ Error checking answer pictograph rendering: {e}")

    def _investigate_answer_options(self, lesson_name: str):
        """Investigate answer option count and management."""
        logger.info(f"      🔤 Investigating answer options for {lesson_name}")

        try:
            # Get answer options using different methods
            available_answers = self.learn_tab.get_available_answers()
            logger.info(
                f"      🔤 Available answers (method 1): {len(available_answers)} options"
            )

            # Direct widget search for answer components
            answer_widgets = self._find_answer_widgets()
            logger.info(
                f"      🔤 Answer widgets (direct search): {len(answer_widgets)} widgets"
            )

            # Detailed analysis of answer widgets
            for i, widget in enumerate(answer_widgets):
                widget_class = widget.__class__.__name__
                logger.info(f"        🔤 Answer widget {i+1}: {widget_class}")

                # Check visibility
                if hasattr(widget, "isVisible"):
                    visible = widget.isVisible()
                    logger.info(f"          📋 Widget {i+1} visible: {visible}")

                # Check text content
                if hasattr(widget, "text"):
                    text = widget.text()
                    logger.info(f"          📝 Widget {i+1} text: '{text}'")

                # Check parent widget
                if hasattr(widget, "parent"):
                    parent_class = (
                        widget.parent().__class__.__name__
                        if widget.parent()
                        else "None"
                    )
                    logger.info(
                        f"          👨‍👩‍👧‍👦 Widget {i+1} parent: {parent_class}"
                    )

            # Check for duplicate or stale widgets
            if len(answer_widgets) > 4:
                logger.warning(
                    f"      ⚠️ Found {len(answer_widgets)} answer widgets, expected 4"
                )
                logger.warning(
                    "      🔍 This suggests component cleanup issues between questions"
                )

        except Exception as e:
            logger.warning(f"      ⚠️ Error investigating answer options: {e}")

    def _test_question_progression(self, lesson_name: str):
        """Test question progression and component state management."""
        logger.info(f"      📝 Testing question progression for {lesson_name}")

        try:
            # Test answering a question
            available_answers = self.learn_tab.get_available_answers()

            if available_answers:
                # Select first answer
                first_answer = available_answers[0]
                logger.info(f"        ✅ Selecting answer: {first_answer}")

                # Count widgets before answering
                widgets_before = len(self._find_answer_widgets())
                logger.info(f"        📊 Answer widgets before: {widgets_before}")

                success = self.learn_tab.answer_question(first_answer)
                if success:
                    logger.info("        ✅ Successfully answered question")

                    # Wait for next question
                    QTest.qWait(1000)

                    # Count widgets after answering
                    widgets_after = len(self._find_answer_widgets())
                    logger.info(f"        📊 Answer widgets after: {widgets_after}")

                    # Check for component cleanup
                    if widgets_after > widgets_before:
                        logger.warning(
                            f"        ⚠️ Widget count increased: {widgets_before} → {widgets_after}"
                        )
                        logger.warning(
                            "        🔍 This indicates component cleanup failure"
                        )
                    elif widgets_after == widgets_before:
                        logger.info("        ✅ Widget count stable - good cleanup")
                    else:
                        logger.info(
                            f"        📉 Widget count decreased: {widgets_before} → {widgets_after}"
                        )

                else:
                    logger.warning("        ⚠️ Failed to answer question")
            else:
                logger.warning("        ⚠️ No answers available for testing")

        except Exception as e:
            logger.warning(f"      ⚠️ Error testing question progression: {e}")

    def _find_pictograph_widgets(self) -> list:
        """Find all pictograph-related widgets."""
        widgets = []

        if hasattr(self.main_window, "findChildren"):
            all_children = self.main_window.findChildren(QWidget)

            for child in all_children:
                class_name = child.__class__.__name__.lower()
                if any(
                    keyword in class_name
                    for keyword in ["pictograph", "view", "scene", "canvas"]
                ):
                    widgets.append(child)

        return widgets

    def _find_learn_pictograph_widgets(self) -> list:
        """Find Learn tab specific pictograph widgets."""
        widgets = []

        if hasattr(self.main_window, "findChildren"):
            all_children = self.main_window.findChildren(QWidget)

            for child in all_children:
                class_name = child.__class__.__name__
                # Look specifically for Learn tab pictograph components
                if "LearnPictographView" in class_name:
                    widgets.append(child)

        return widgets

    def _find_answer_widgets(self) -> list:
        """Find all answer-related widgets."""
        widgets = []

        if hasattr(self.main_window, "findChildren"):
            all_children = self.main_window.findChildren(QWidget)

            for child in all_children:
                class_name = child.__class__.__name__.lower()
                if any(
                    keyword in class_name
                    for keyword in ["answer", "option", "choice", "button"]
                ):
                    # Additional filtering to avoid false positives
                    if hasattr(child, "click") or hasattr(child, "text"):
                        widgets.append(child)

        return widgets

    def _navigate_back_to_selector(self):
        """Navigate back to lesson selector."""
        logger.info("      🔄 Navigating back to lesson selector")

        try:
            # Wait a moment for any ongoing operations
            QTest.qWait(500)

            # Try to find and click back button or navigate back
            # For now, we'll just wait and assume navigation happens
            QTest.qWait(1000)

            # Verify we're back at selector
            selector_visible = self.learn_tab.is_lesson_selector_visible()
            if selector_visible:
                logger.info("      ✅ Successfully returned to lesson selector")
            else:
                logger.warning("      ⚠️ May not have returned to lesson selector")

        except Exception as e:
            logger.warning(f"      ⚠️ Error navigating back to selector: {e}")
