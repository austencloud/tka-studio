"""
Learn Tab Page Object

Provides high-level interface for interacting with the Learn Tab,
including lesson selection, quiz functionality, and progress tracking.
"""

import logging
from typing import Optional

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget

from .base_page_object import BasePageObject

logger = logging.getLogger(__name__)


class LearnTabPageObject(BasePageObject):
    """
    Page object for the Learn Tab.

    Provides methods for:
    - Lesson selection and navigation
    - Quiz interaction
    - Progress tracking
    - Component visibility verification
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.element_selectors = {
            "learn_tab": "learn_tab",
            "lesson_selector": "lesson_selector",
            "lesson_widget": "lesson_widget",
            "results_panel": "results_panel",
            "lesson_items": "lesson_item",
            "quiz_questions": "quiz_question",
        }

    # ========================================
    # COMPONENT VISIBILITY METHODS
    # ========================================

    def is_lesson_selector_visible(self) -> bool:
        """Check if lesson selector is visible."""
        logger.debug("Checking lesson selector visibility")

        selector = self.get_element("lesson_selector")
        if selector and hasattr(selector, "isVisible"):
            return selector.isVisible()

        # Fallback: look for lesson selector related components
        return self._find_lesson_selector_components() is not None

    def is_lesson_widget_visible(self) -> bool:
        """Check if lesson widget is visible."""
        logger.debug("Checking lesson widget visibility")

        widget = self.get_element("lesson_widget")
        if widget and hasattr(widget, "isVisible"):
            return widget.isVisible()

        # Fallback: look for lesson widget related components
        return self._find_lesson_widget_components() is not None

    def is_results_panel_visible(self) -> bool:
        """Check if results panel is visible."""
        logger.debug("Checking results panel visibility")

        panel = self.get_element("results_panel")
        if panel and hasattr(panel, "isVisible"):
            return panel.isVisible()

        # Fallback: look for results related components
        return self._find_results_components() is not None

    # ========================================
    # LESSON SELECTION METHODS
    # ========================================

    def get_available_lessons(self) -> list[str]:
        """Get list of available lessons."""
        logger.debug("Getting available lessons")

        try:
            # Look for lesson items in the selector
            lesson_elements = self._find_lesson_elements()

            lessons = []
            for element in lesson_elements:
                # Extract lesson name from element
                lesson_name = self._extract_lesson_name(element)
                if lesson_name:
                    lessons.append(lesson_name)

            logger.info(f"📚 Found {len(lessons)} available lessons")
            return lessons

        except Exception as e:
            logger.warning(f"Error getting available lessons: {e}")
            return []

    def select_lesson(self, lesson_name: str) -> bool:
        """Select a specific lesson."""
        logger.info(f"📚 Selecting lesson: {lesson_name}")

        try:
            # Find the lesson element
            lesson_element = self._find_lesson_element(lesson_name)

            if lesson_element and hasattr(lesson_element, "click"):
                lesson_element.click()
                logger.info(f"✅ Successfully selected lesson: {lesson_name}")
                return True
            else:
                logger.warning(
                    f"⚠️ Could not find clickable element for lesson: {lesson_name}"
                )
                return False

        except Exception as e:
            logger.error(f"❌ Error selecting lesson {lesson_name}: {e}")
            return False

    def get_current_lesson(self) -> Optional[str]:
        """Get the currently selected lesson."""
        logger.debug("Getting current lesson")

        try:
            # Look for selected lesson element
            selected_element = self._find_selected_lesson()
            if selected_element:
                return self._extract_lesson_name(selected_element)
            return None

        except Exception as e:
            logger.warning(f"Error getting current lesson: {e}")
            return None

    # ========================================
    # QUIZ INTERACTION METHODS
    # ========================================

    def start_lesson(self) -> bool:
        """Start the selected lesson."""
        logger.info("📚 Starting lesson")

        try:
            # Find and click start button
            start_button = self._find_start_button()
            if start_button and hasattr(start_button, "click"):
                start_button.click()
                logger.info("✅ Successfully started lesson")
                return True
            else:
                logger.warning("⚠️ Start button not found")
                return False

        except Exception as e:
            logger.error(f"❌ Error starting lesson: {e}")
            return False

    def answer_question(self, answer: str) -> bool:
        """Answer a quiz question."""
        logger.info(f"📚 Answering question with: {answer}")

        try:
            # Find the answer option
            answer_element = self._find_answer_element(answer)

            if answer_element and hasattr(answer_element, "click"):
                answer_element.click()
                logger.info(f"✅ Successfully answered: {answer}")
                return True
            else:
                logger.warning(f"⚠️ Could not find answer option: {answer}")
                return False

        except Exception as e:
            logger.error(f"❌ Error answering question: {e}")
            return False

    def get_current_question(self) -> Optional[str]:
        """Get the current quiz question text."""
        logger.debug("Getting current question")

        try:
            # Look for question text element
            question_element = self._find_question_element()
            if question_element and hasattr(question_element, "text"):
                return question_element.text()
            return None

        except Exception as e:
            logger.warning(f"Error getting current question: {e}")
            return None

    def get_available_answers(self) -> list[str]:
        """Get available answer options for current question."""
        logger.debug("Getting available answers")

        try:
            # Look for answer option elements
            answer_elements = self._find_answer_elements()

            answers = []
            for element in answer_elements:
                # Extract answer text from element
                answer_text = self._extract_answer_text(element)
                if answer_text:
                    answers.append(answer_text)

            logger.info(f"📚 Found {len(answers)} answer options")
            return answers

        except Exception as e:
            logger.warning(f"Error getting available answers: {e}")
            return []

    # ========================================
    # PROGRESS TRACKING METHODS
    # ========================================

    def get_lesson_progress(self) -> dict:
        """Get current lesson progress information."""
        logger.debug("Getting lesson progress")

        try:
            progress_info = {
                "current_question": 0,
                "total_questions": 0,
                "score": 0,
                "completed": False,
            }

            # Find progress indicators
            progress_element = self._find_progress_element()
            if progress_element:
                # Extract progress information
                progress_info.update(self._extract_progress_info(progress_element))

            return progress_info

        except Exception as e:
            logger.warning(f"Error getting lesson progress: {e}")
            return {}

    def is_lesson_completed(self) -> bool:
        """Check if current lesson is completed."""
        progress = self.get_lesson_progress()
        return progress.get("completed", False)

    # ========================================
    # PRIVATE HELPER METHODS
    # ========================================

    def _find_lesson_selector_components(self) -> Optional[QWidget]:
        """Find lesson selector related components."""
        # Look for various lesson selector related widgets
        for class_name in ["LessonSelector", "LessonPanel", "LessonList"]:
            components = self._find_components_by_class_name(class_name)
            if components:
                return components[0]
        return None

    def _find_lesson_widget_components(self) -> Optional[QWidget]:
        """Find lesson widget related components."""
        # Look for various lesson widget related widgets
        for class_name in ["LessonWidget", "QuizWidget", "LessonPanel"]:
            components = self._find_components_by_class_name(class_name)
            if components:
                return components[0]
        return None

    def _find_results_components(self) -> Optional[QWidget]:
        """Find results related components."""
        # Look for various results related widgets
        for class_name in ["ResultsPanel", "ScorePanel", "ProgressPanel"]:
            components = self._find_components_by_class_name(class_name)
            if components:
                return components[0]
        return None

    def _find_lesson_elements(self) -> list[QWidget]:
        """Find all lesson elements."""
        elements = []

        # Look for lesson items
        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                class_name = child.__class__.__name__.lower()
                if any(
                    indicator in class_name
                    for indicator in ["lesson", "course", "tutorial"]
                ):
                    if hasattr(child, "click") or hasattr(child, "isVisible"):
                        elements.append(child)

        return elements

    def _find_lesson_element(self, lesson_name: str) -> Optional[QWidget]:
        """Find specific lesson element by name."""
        elements = self._find_lesson_elements()

        for element in elements:
            if self._element_matches_name(element, lesson_name):
                return element

        return None

    def _find_selected_lesson(self) -> Optional[QWidget]:
        """Find the currently selected lesson element."""
        elements = self._find_lesson_elements()

        for element in elements:
            # Look for selection indicators
            if hasattr(element, "isSelected") and element.isSelected():
                return element
            if hasattr(element, "isChecked") and element.isChecked():
                return element

        return None

    def _find_start_button(self) -> Optional[QWidget]:
        """Find the start lesson button."""
        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                if hasattr(child, "text"):
                    text = child.text().lower()
                    if any(keyword in text for keyword in ["start", "begin", "play"]):
                        return child
        return None

    def _find_answer_elements(self) -> list[QWidget]:
        """Find lesson-specific answer option elements."""
        elements = []

        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                class_name = child.__class__.__name__

                # Look for lesson-specific answer components
                if any(
                    lesson_indicator in class_name
                    for lesson_indicator in [
                        "LessonButton",
                        "AnswerOption",
                        "QuestionOption",
                    ]
                ):
                    if hasattr(child, "click") or hasattr(child, "text"):
                        elements.append(child)

                # Also look for buttons that are children of lesson widgets
                elif "Button" in class_name and hasattr(child, "parent"):
                    parent = child.parent()
                    if parent:
                        parent_class = parent.__class__.__name__
                        if any(
                            lesson_parent in parent_class
                            for lesson_parent in [
                                "AnswerOptions",
                                "LessonWidget",
                                "QuestionDisplay",
                            ]
                        ):
                            # Check if it's visible and has text content
                            if (
                                hasattr(child, "isVisible")
                                and child.isVisible()
                                and hasattr(child, "text")
                                and child.text().strip()
                            ):
                                elements.append(child)

        return elements

    def _find_answer_element(self, answer: str) -> Optional[QWidget]:
        """Find specific answer element by text."""
        elements = self._find_answer_elements()

        for element in elements:
            if self._element_matches_name(element, answer):
                return element

        return None

    def _find_question_element(self) -> Optional[QWidget]:
        """Find the current question element."""
        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                class_name = child.__class__.__name__.lower()
                if "question" in class_name and hasattr(child, "text"):
                    return child
        return None

    def _find_progress_element(self) -> Optional[QWidget]:
        """Find the progress indicator element."""
        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                class_name = child.__class__.__name__.lower()
                if any(
                    indicator in class_name
                    for indicator in ["progress", "score", "status"]
                ):
                    return child
        return None

    def _extract_lesson_name(self, element: QWidget) -> Optional[str]:
        """Extract lesson name from element."""
        if hasattr(element, "text"):
            return element.text()
        if hasattr(element, "objectName"):
            return element.objectName()
        return element.__class__.__name__

    def _extract_answer_text(self, element: QWidget) -> Optional[str]:
        """Extract answer text from element."""
        if hasattr(element, "text"):
            return element.text()
        if hasattr(element, "objectName"):
            return element.objectName()
        return element.__class__.__name__

    def _extract_progress_info(self, element: QWidget) -> dict:
        """Extract progress information from element."""
        # This would be implemented based on specific progress UI
        return {}

    def _element_matches_name(self, element: QWidget, name: str) -> bool:
        """Check if element matches the given name."""
        element_text = self._extract_lesson_name(element) or ""
        return name.lower() in element_text.lower()

    def _find_components_by_class_name(self, class_name: str) -> list[QWidget]:
        """Find components by class name."""
        components = []

        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                if class_name.lower() in child.__class__.__name__.lower():
                    components.append(child)

        return components
