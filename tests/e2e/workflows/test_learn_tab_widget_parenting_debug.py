"""
Learn Tab Widget Parenting Debug Test

This test specifically debugs the parent widget assignment issue where
lesson question and answer widgets appear in separate standalone windows
instead of being properly embedded within the main application window.
"""

import logging
import sys
from typing import Any, Tuple

import pytest
from PyQt6.QtCore import QTimer
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QWidget

from tests.e2e.framework.page_objects.learn_tab import LearnTabPageObject
from tests.e2e.framework.steps.navigation_steps import NavigationSteps

logger = logging.getLogger(__name__)


class TestLearnTabWidgetParentingDebug:
    """
    Debug test for Learn tab widget parenting issues.

    This test systematically investigates why lesson question and answer
    widgets are appearing as standalone windows instead of being properly
    embedded in the main application window.
    """

    @pytest.fixture(autouse=True)
    def setup_test_environment(self, tka_app: Tuple[Any, Any]):
        """Setup test environment for parenting debug."""
        self.app_instance, self.main_window = tka_app
        self.navigation_steps = NavigationSteps(self.main_window)
        self.learn_tab = LearnTabPageObject(self.main_window)

        logger.info("🔧 LEARN TAB WIDGET PARENTING DEBUG TEST SETUP")
        logger.info(f"📱 Main window: {self.main_window}")
        logger.info(f"📱 Main window type: {type(self.main_window)}")

    def test_lesson_widget_parenting_debug(self):
        """
        Debug lesson widget parenting by navigating to Learn tab,
        selecting a lesson, and examining widget parent relationships.
        """
        logger.info("🚀 STARTING LESSON WIDGET PARENTING DEBUG")

        # Step 1: Navigate to Learn tab
        logger.info("📍 Step 1: Navigating to Learn tab")
        success = self.navigation_steps.navigate_to_learn_tab()
        assert success, "Should successfully navigate to learn tab"

        # Wait for tab to initialize
        QTest.qWait(1000)

        # Step 2: Check Learn tab structure
        self._debug_learn_tab_structure()

        # Step 3: Select Lesson 1
        logger.info("📍 Step 3: Selecting Lesson 1")
        available_lessons = self.learn_tab.get_available_lessons()
        logger.info(f"📚 Available lessons: {available_lessons}")

        if available_lessons:
            # Filter out non-lesson items and select a real lesson
            real_lessons = [
                lesson for lesson in available_lessons if lesson.startswith("Lesson")
            ]
            if real_lessons:
                lesson_name = real_lessons[0]  # Select first real lesson
                logger.info(f"📚 Selecting real lesson: {lesson_name}")
                success = self.learn_tab.select_lesson(lesson_name)
                assert success, f"Should successfully select lesson: {lesson_name}"
            else:
                logger.error("❌ No real lessons found in available lessons")
                return

            # Wait for lesson to initialize
            QTest.qWait(2000)

            # Step 4: Debug lesson widget structure
            self._debug_lesson_widget_structure()

            # Step 5: Generate and debug question widgets
            self._debug_question_widget_creation()

        else:
            logger.error("❌ No lessons available for testing")

        logger.info("🎯 LESSON WIDGET PARENTING DEBUG COMPLETED")

    def _debug_learn_tab_structure(self):
        """Debug the Learn tab structure and widget hierarchy."""
        logger.info("🔍 Debugging Learn tab structure")

        try:
            # First, let's find all widgets and see the hierarchy
            self._debug_widget_hierarchy()

            # Find the learn tab widget
            learn_tab_widget = self._find_learn_tab_widget()
            if learn_tab_widget:
                logger.info(f"✅ Found Learn tab widget: {learn_tab_widget}")
                logger.info(f"📱 Learn tab parent: {learn_tab_widget.parent()}")
                logger.info(
                    f"📱 Learn tab window flags: {learn_tab_widget.windowFlags()}"
                )

                # Check for stacked widget
                stack_widget = self._find_child_by_type(
                    learn_tab_widget, "QStackedWidget"
                )
                if stack_widget:
                    logger.info(f"✅ Found stack widget: {stack_widget}")
                    logger.info(f"📱 Stack widget parent: {stack_widget.parent()}")
                    logger.info(
                        f"📱 Stack widget current index: {stack_widget.currentIndex()}"
                    )
                    logger.info(f"📱 Stack widget count: {stack_widget.count()}")
                else:
                    logger.warning("⚠️ No stack widget found in Learn tab")
            else:
                logger.error("❌ Learn tab widget not found")
                # Try alternative search methods
                self._debug_alternative_search()

        except Exception as e:
            logger.error(f"❌ Error debugging Learn tab structure: {e}")

    def _debug_widget_hierarchy(self):
        """Debug the complete widget hierarchy to understand the structure."""
        logger.info("🔍 Debugging complete widget hierarchy")

        try:
            # Start from main window and traverse down
            self._traverse_widget_tree(self.main_window, 0, max_depth=4)

        except Exception as e:
            logger.error(f"❌ Error debugging widget hierarchy: {e}")

    def _traverse_widget_tree(self, widget, depth, max_depth=3):
        """Recursively traverse widget tree and log structure."""
        if depth > max_depth:
            return

        indent = "  " * depth
        widget_type = type(widget).__name__
        object_name = (
            widget.objectName() if hasattr(widget, "objectName") else "no_name"
        )

        logger.info(f"{indent}📦 {widget_type} (name: {object_name})")

        # Look for Learn-related widgets
        if "learn" in object_name.lower() or "Learn" in widget_type:
            logger.info(f"{indent}🎯 FOUND LEARN WIDGET: {widget}")
            logger.info(f"{indent}   Parent: {widget.parent()}")
            logger.info(f"{indent}   Window flags: {widget.windowFlags()}")

        # Traverse children
        if hasattr(widget, "children"):
            for child in widget.children():
                if hasattr(child, "isWidgetType") and child.isWidgetType():
                    self._traverse_widget_tree(child, depth + 1, max_depth)

    def _debug_alternative_search(self):
        """Try alternative methods to find Learn tab components."""
        logger.info("🔍 Trying alternative search methods")

        try:
            # Search by type name
            all_widgets = self.main_window.findChildren(QWidget)
            learn_widgets = []

            for widget in all_widgets:
                widget_type = type(widget).__name__
                object_name = widget.objectName()

                if (
                    "Learn" in widget_type
                    or "learn" in object_name.lower()
                    or "Lesson" in widget_type
                    or "lesson" in object_name.lower()
                ):
                    learn_widgets.append(widget)
                    logger.info(
                        f"🎯 Found Learn-related widget: {widget_type} (name: {object_name})"
                    )
                    logger.info(f"   Widget: {widget}")
                    logger.info(f"   Parent: {widget.parent()}")

            logger.info(f"📊 Total Learn-related widgets found: {len(learn_widgets)}")

        except Exception as e:
            logger.error(f"❌ Error in alternative search: {e}")

    def _debug_lesson_widget_structure(self):
        """Debug the lesson widget structure after lesson selection."""
        logger.info("🔍 Debugging lesson widget structure")

        try:
            learn_tab_widget = self._find_learn_tab_widget()
            if not learn_tab_widget:
                logger.error("❌ Learn tab widget not found")
                return

            # Find lesson widget panel
            lesson_widget_panel = self._find_child_by_name(
                learn_tab_widget, "lesson_widget"
            )
            if lesson_widget_panel:
                logger.info(f"✅ Found lesson widget panel: {lesson_widget_panel}")
                logger.info(f"📱 Lesson widget parent: {lesson_widget_panel.parent()}")
                logger.info(
                    f"📱 Lesson widget window flags: {lesson_widget_panel.windowFlags()}"
                )

                # Find question display and answer options
                self._debug_question_and_answer_components(lesson_widget_panel)
            else:
                logger.warning("⚠️ Lesson widget panel not found")

        except Exception as e:
            logger.error(f"❌ Error debugging lesson widget structure: {e}")

    def _debug_question_and_answer_components(self, lesson_widget_panel):
        """Debug question display and answer options components."""
        logger.info("🔍 Debugging question and answer components")

        try:
            # Find question display
            question_display = self._find_child_by_type(
                lesson_widget_panel, "QuestionDisplay"
            )
            if question_display:
                logger.info(f"✅ Found question display: {question_display}")
                logger.info(f"📱 Question display parent: {question_display.parent()}")
                logger.info(
                    f"📱 Question display window flags: {question_display.windowFlags()}"
                )

                # Check for pictograph widget in question display
                self._debug_pictograph_widgets_in_component(
                    question_display, "question"
                )
            else:
                logger.warning("⚠️ Question display not found")

            # Find answer options
            answer_options = self._find_child_by_type(
                lesson_widget_panel, "AnswerOptions"
            )
            if answer_options:
                logger.info(f"✅ Found answer options: {answer_options}")
                logger.info(f"📱 Answer options parent: {answer_options.parent()}")
                logger.info(
                    f"📱 Answer options window flags: {answer_options.windowFlags()}"
                )

                # Check for pictograph widgets in answer options
                self._debug_pictograph_widgets_in_component(answer_options, "answer")
            else:
                logger.warning("⚠️ Answer options not found")

        except Exception as e:
            logger.error(f"❌ Error debugging question and answer components: {e}")

    def _debug_pictograph_widgets_in_component(self, component, component_type):
        """Debug pictograph widgets within a component."""
        logger.info(f"🔍 Debugging pictograph widgets in {component_type} component")

        try:
            # Find all pictograph views
            pictograph_views = self._find_children_by_type(
                component, "LearnPictographView"
            )
            logger.info(
                f"📊 Found {len(pictograph_views)} pictograph views in {component_type}"
            )

            for i, view in enumerate(pictograph_views):
                logger.info(f"🎭 Pictograph view {i+1}:")
                logger.info(f"   📱 Widget: {view}")
                logger.info(f"   📱 Parent: {view.parent()}")
                logger.info(f"   📱 Window flags: {view.windowFlags()}")
                logger.info(f"   📱 Is window: {view.isWindow()}")
                logger.info(f"   📱 Window title: {view.windowTitle()}")
                logger.info(f"   📱 Visible: {view.isVisible()}")

                # Check if it's appearing as a standalone window
                if view.isWindow() or view.parent() is None:
                    logger.error(
                        f"❌ PROBLEM FOUND: Pictograph view {i+1} is appearing as standalone window!"
                    )
                    logger.error(f"   Expected parent: {component}")
                    logger.error(f"   Actual parent: {view.parent()}")

                    # Try to get the top-level window
                    top_level = view.window()
                    logger.error(f"   Top-level window: {top_level}")
                    logger.error(
                        f"   Top-level window title: {top_level.windowTitle()}"
                    )
                else:
                    logger.info(f"✅ Pictograph view {i+1} is properly parented")

        except Exception as e:
            logger.error(f"❌ Error debugging pictograph widgets: {e}")

    def _debug_question_widget_creation(self):
        """Debug the actual question widget creation process."""
        logger.info("🔍 Debugging question widget creation process")

        # Set up a timer to periodically check for new widgets
        self.widget_check_timer = QTimer()
        self.widget_check_timer.timeout.connect(self._check_for_new_widgets)
        self.widget_check_timer.start(500)  # Check every 500ms

        # Wait for potential question generation
        QTest.qWait(5000)

        # Stop the timer
        self.widget_check_timer.stop()

    def _check_for_new_widgets(self):
        """Check for newly created widgets that might be standalone windows."""
        try:
            # Get all top-level widgets
            from PyQt6.QtWidgets import QApplication

            all_widgets = QApplication.allWidgets()
            top_level_widgets = [
                w for w in all_widgets if w.isWindow() and w.isVisible()
            ]

            # Filter for potential pictograph widgets
            pictograph_windows = []
            for widget in top_level_widgets:
                widget_type = type(widget).__name__
                if "Pictograph" in widget_type or "Learn" in widget_type:
                    if widget != self.main_window:  # Exclude main window
                        pictograph_windows.append(widget)

            if pictograph_windows:
                logger.warning(
                    f"⚠️ Found {len(pictograph_windows)} potential standalone pictograph windows:"
                )
                for i, widget in enumerate(pictograph_windows):
                    logger.warning(
                        f"   Window {i+1}: {widget} ({type(widget).__name__})"
                    )
                    logger.warning(f"   Title: {widget.windowTitle()}")
                    logger.warning(f"   Size: {widget.size()}")
                    logger.warning(f"   Position: {widget.pos()}")

        except Exception as e:
            logger.error(f"❌ Error checking for new widgets: {e}")

    # Helper methods
    def _find_learn_tab_widget(self):
        """Find the Learn tab widget in the main window."""
        return self._find_child_by_name(self.main_window, "learn_tab")

    def _find_child_by_name(self, parent, name):
        """Find a child widget by object name."""
        return parent.findChild(QWidget, name)

    def _find_child_by_type(self, parent, type_name):
        """Find a child widget by type name."""
        for child in parent.findChildren(QWidget):
            if type(child).__name__ == type_name:
                return child
        return None

    def _find_children_by_type(self, parent, type_name):
        """Find all child widgets by type name."""
        return [
            child
            for child in parent.findChildren(QWidget)
            if type(child).__name__ == type_name
        ]
