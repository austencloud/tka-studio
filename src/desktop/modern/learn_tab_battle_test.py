"""
Learn Tab Implementation Battle Test Script

Comprehensive testing script to validate the modern learn tab implementation
against all requirements and ensure functional parity with legacy system.
"""

import logging
import sys
import traceback
from pathlib import Path
from typing import List, Dict, Any, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LearnTabBattleTest:
    """
    Comprehensive battle test for the modern learn tab implementation.
    
    Tests all aspects of the implementation including:
    - Service registration and dependency injection
    - Domain model functionality
    - Service implementations
    - UI component creation
    - Integration between components
    - Functional parity with legacy system
    """
    
    def __init__(self):
        """Initialize battle test suite."""
        self.test_results: List[Dict[str, Any]] = []
        self.container = None
        self.learn_tab = None
        
        # Add project root to path for imports
        project_root = Path(__file__).parent.parent.parent.parent.parent
        sys.path.insert(0, str(project_root))
    
    def run_all_tests(self) -> bool:
        """
        Run all battle tests.
        
        Returns:
            True if all tests pass, False otherwise
        """
        logger.info("🚀 Starting Learn Tab Battle Test Suite")
        logger.info("=" * 60)
        
        test_methods = [
            self.test_domain_models,
            self.test_service_interfaces, 
            self.test_service_implementations,
            self.test_dependency_injection,
            self.test_ui_components,
            self.test_integration,
            self.test_functional_parity,
            self.test_error_handling,
            self.test_performance,
        ]
        
        all_passed = True
        
        for test_method in test_methods:
            try:
                logger.info(f"\n📋 Running {test_method.__name__}")
                result = test_method()
                
                if result:
                    logger.info(f"✅ {test_method.__name__} PASSED")
                else:
                    logger.error(f"❌ {test_method.__name__} FAILED")
                    all_passed = False
                    
            except Exception as e:
                logger.error(f"💥 {test_method.__name__} CRASHED: {e}")
                logger.error(traceback.format_exc())
                all_passed = False
        
        # Print summary
        logger.info("\n" + "=" * 60)
        if all_passed:
            logger.info("🎉 ALL TESTS PASSED - Implementation is battle-ready!")
        else:
            logger.error("💀 SOME TESTS FAILED - Implementation needs fixes")
        
        return all_passed
    
    def test_domain_models(self) -> bool:
        """Test domain model functionality."""
        logger.info("Testing domain models...")
        
        try:
            from domain.models.learn import (
                LessonConfig, LessonType, QuizMode, QuizSession, 
                QuestionData, LessonResults
            )
            
            # Test LessonConfig
            config = LessonConfig(
                lesson_type=LessonType.PICTOGRAPH_TO_LETTER,
                question_format="pictograph",
                answer_format="button", 
                quiz_description="pictograph_to_letter",
                question_prompt="Choose the letter for:"
            )
            
            config_dict = config.to_dict()
            assert "lesson_type" in config_dict
            assert config_dict["lesson_type"] == "pictograph_to_letter"
            
            restored_config = LessonConfig.from_dict(config_dict)
            assert restored_config.lesson_type == config.lesson_type
            
            # Test QuizSession
            session = QuizSession(
                lesson_type=LessonType.LETTER_TO_PICTOGRAPH,
                quiz_mode=QuizMode.FIXED_QUESTION
            )
            
            session_dict = session.to_dict()
            assert "session_id" in session_dict
            assert session_dict["lesson_type"] == "letter_to_pictograph"
            
            # Test session methods
            session.mark_interaction()
            session.complete_session()
            assert not session.is_active
            assert session.is_completed
            
            # Test QuestionData
            question = QuestionData(
                question_content="A",
                answer_options=["pic1", "pic2", "pic3", "pic4"],
                correct_answer="pic2",
                question_type="letter_to_pictograph"
            )
            
            assert question.is_valid()
            incorrect_options = question.get_incorrect_options()
            assert len(incorrect_options) == 3
            assert "pic2" not in incorrect_options
            
            # Test LessonResults
            results = LessonResults(
                session_id="test-session",
                lesson_type=LessonType.VALID_NEXT_PICTOGRAPH,
                quiz_mode=QuizMode.COUNTDOWN,
                total_questions=15,
                correct_answers=12,
                incorrect_guesses=5,
                questions_answered=15,
                accuracy_percentage=80.0,
                completion_time_seconds=95.5
            )
            
            assert results.grade_letter == "B"
            assert results.performance_level == "Good"
            assert results.calculate_score() == 80
            
            logger.info("✅ Domain models working correctly")
            return True
            
        except Exception as e:
            logger.error(f"❌ Domain models failed: {e}")
            return False
    
    def test_service_interfaces(self) -> bool:
        """Test service interface definitions."""
        logger.info("Testing service interfaces...")
        
        try:
            from core.interfaces.learn_services import (
                ILessonConfigurationService, IQuizSessionService,
                IQuestionGenerationService, IAnswerValidationService,
                ILessonProgressService, ILearnUIService,
                ILearnNavigationService, ILearnDataService
            )
            
            # Verify all interfaces have required methods
            required_methods = {
                ILessonConfigurationService: [
                    'get_all_lesson_configs', 'get_lesson_config', 'get_lesson_names'
                ],
                IQuizSessionService: [
                    'create_session', 'get_session', 'update_session_progress', 
                    'end_session', 'get_active_sessions'
                ],
                IQuestionGenerationService: [
                    'generate_question', 'get_pictograph_dataset', 'validate_question'
                ],
                IAnswerValidationService: [
                    'check_answer', 'record_answer', 'get_answer_history'
                ],
                ILessonProgressService: [
                    'get_progress_info', 'is_lesson_complete', 'calculate_results',
                    'should_advance_to_next_question'
                ],
                ILearnUIService: [
                    'get_font_sizes', 'get_component_sizes', 'get_layout_spacing'
                ],
                ILearnNavigationService: [
                    'navigate_to_lesson_selector', 'navigate_to_lesson', 
                    'navigate_to_results', 'get_current_view', 'can_navigate_back'
                ],
                ILearnDataService: [
                    'save_lesson_progress', 'load_lesson_progress',
                    'save_lesson_results', 'get_lesson_history'
                ]
            }
            
            for interface, methods in required_methods.items():
                for method_name in methods:
                    if not hasattr(interface, method_name):
                        logger.error(f"Interface {interface.__name__} missing method: {method_name}")
                        return False
            
            logger.info("✅ Service interfaces properly defined")
            return True
            
        except Exception as e:
            logger.error(f"❌ Service interfaces failed: {e}")
            return False
    
    def test_service_implementations(self) -> bool:
        """Test service implementation functionality."""
        logger.info("Testing service implementations...")
        
        try:
            from application.services.learn import (
                LessonConfigurationService, QuizSessionService,
                AnswerValidationService, LessonProgressService,
                LearnUIService, LearnNavigationService, LearnDataService
            )
            from domain.models.learn import LessonType, QuizMode
            
            # Test LessonConfigurationService
            config_service = LessonConfigurationService()
            configs = config_service.get_all_lesson_configs()
            assert len(configs) == 3  # Should have 3 lesson configs
            
            lesson1_config = config_service.get_lesson_config(LessonType.PICTOGRAPH_TO_LETTER)
            assert lesson1_config is not None
            assert lesson1_config.question_format == "pictograph"
            assert lesson1_config.answer_format == "button"
            
            # Test QuizSessionService
            session_service = QuizSessionService()
            session_id = session_service.create_session(
                LessonType.LETTER_TO_PICTOGRAPH, 
                QuizMode.FIXED_QUESTION
            )
            assert session_id is not None
            
            session = session_service.get_session(session_id)
            assert session is not None
            assert session.lesson_type == LessonType.LETTER_TO_PICTOGRAPH
            assert session.total_questions == 20
            
            # Test session updates
            update_success = session_service.update_session_progress(
                session_id, current_question=5, correct_answers=4
            )
            assert update_success
            
            updated_session = session_service.get_session(session_id)
            assert updated_session.current_question == 5
            assert updated_session.correct_answers == 4
            
            # Test AnswerValidationService
            validation_service = AnswerValidationService(session_service)
            
            from domain.models.learn import QuestionData
            question = QuestionData(
                question_content="test",
                answer_options=["A", "B", "C", "D"],
                correct_answer="B"
            )
            
            # Test correct answer
            is_correct = validation_service.check_answer(question, "B")
            assert is_correct
            
            # Test incorrect answer
            is_incorrect = validation_service.check_answer(question, "A")
            assert not is_incorrect
            
            # Test LearnUIService
            ui_service = LearnUIService()
            font_sizes = ui_service.get_font_sizes(1200, 800)
            assert "title" in font_sizes
            assert font_sizes["title"] > 0
            
            component_sizes = ui_service.get_component_sizes(1200, 800)
            assert "lesson_button" in component_sizes
            assert len(component_sizes["lesson_button"]) == 2  # width, height
            
            # Test LearnNavigationService
            nav_service = LearnNavigationService()
            nav_service.navigate_to_lesson(session_id)
            assert nav_service.get_current_view() == "lesson"
            assert nav_service.can_navigate_back()
            
            logger.info("✅ Service implementations working correctly")
            return True
            
        except Exception as e:
            logger.error(f"❌ Service implementations failed: {e}")
            return False
    
    def test_dependency_injection(self) -> bool:
        """Test dependency injection registration and resolution."""
        logger.info("Testing dependency injection...")
        
        try:
            from core.dependency_injection.di_container import DIContainer
            from core.dependency_injection.learn_service_registration import (
                register_learn_services, validate_learn_service_registration
            )
            
            # Create container and register services
            self.container = DIContainer()
            register_learn_services(self.container)
            
            # Validate registration
            validation_success = validate_learn_service_registration(self.container)
            assert validation_success, "Service registration validation failed"
            
            # Test individual service resolution
            from core.interfaces.learn_services import (
                ILessonConfigurationService, IQuizSessionService,
                ILearnUIService, ILearnNavigationService
            )
            
            config_service = self.container.resolve(ILessonConfigurationService)
            assert config_service is not None
            
            session_service = self.container.resolve(IQuizSessionService)
            assert session_service is not None
            
            ui_service = self.container.resolve(ILearnUIService)
            assert ui_service is not None
            
            nav_service = self.container.resolve(ILearnNavigationService)
            assert nav_service is not None
            
            # Test that services maintain singleton behavior
            config_service2 = self.container.resolve(ILessonConfigurationService)
            assert config_service is config_service2, "Services should be singletons"
            
            logger.info("✅ Dependency injection working correctly")
            return True
            
        except Exception as e:
            logger.error(f"❌ Dependency injection failed: {e}")
            return False
    
    def test_ui_components(self) -> bool:
        """Test UI component creation and basic functionality."""
        logger.info("Testing UI components...")
        
        try:
            # Note: This test may need to be adapted based on Qt availability
            # For now, test imports and basic instantiation
            
            from presentation.tabs.learn.components import (
                LessonSelectorPanel, LessonWidgetPanel, LessonResultsPanel
            )
            
            # Test component imports work
            assert LessonSelectorPanel is not None
            assert LessonWidgetPanel is not None  
            assert LessonResultsPanel is not None
            
            logger.info("✅ UI components can be imported")
            
            # If Qt is available, test basic instantiation
            try:
                from PyQt6.QtWidgets import QApplication
                import sys
                
                app = QApplication.instance()
                if app is None:
                    app = QApplication(sys.argv)
                
                # Test component creation with services
                if self.container:
                    from core.interfaces.learn_services import (
                        ILessonConfigurationService, ILearnUIService
                    )
                    
                    config_service = self.container.resolve(ILessonConfigurationService)
                    ui_service = self.container.resolve(ILearnUIService)
                    
                    # Test lesson selector panel creation
                    selector = LessonSelectorPanel(config_service, ui_service)
                    assert selector is not None
                    
                    logger.info("✅ UI components can be instantiated")
                
            except ImportError:
                logger.warning("⚠️ PyQt6 not available, skipping UI instantiation tests")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ UI components failed: {e}")
            return False
    
    def test_integration(self) -> bool:
        """Test integration between services and components."""
        logger.info("Testing service integration...")
        
        try:
            if not self.container:
                logger.error("Container not available for integration test")
                return False
            
            from core.interfaces.learn_services import (
                ILessonConfigurationService, IQuizSessionService,
                IQuestionGenerationService, IAnswerValidationService,
                ILessonProgressService
            )
            from domain.models.learn import LessonType, QuizMode, QuestionData
            
            # Get services
            config_service = self.container.resolve(ILessonConfigurationService)
            session_service = self.container.resolve(IQuizSessionService)
            validation_service = self.container.resolve(IAnswerValidationService)
            progress_service = self.container.resolve(ILessonProgressService)
            
            # Test full lesson flow
            lesson_type = LessonType.PICTOGRAPH_TO_LETTER
            quiz_mode = QuizMode.FIXED_QUESTION
            
            # 1. Create session
            session_id = session_service.create_session(lesson_type, quiz_mode)
            session = session_service.get_session(session_id)
            assert session is not None
            
            # 2. Get lesson config
            config = config_service.get_lesson_config(lesson_type)
            assert config is not None
            assert config.lesson_type == lesson_type
            
            # 3. Simulate answering questions
            for i in range(5):
                # Simulate question
                question = QuestionData(
                    question_content="test_pictograph",
                    answer_options=["A", "B", "C", "D"],
                    correct_answer="B"
                )
                
                # Simulate correct answer
                is_correct = validation_service.check_answer(question, "B")
                assert is_correct
                
                # Record answer
                validation_service.record_answer(session_id, f"q{i}", True)
                
                # Update session
                session_service.update_session_progress(
                    session_id,
                    current_question=i + 2,
                    correct_answers=i + 1
                )
            
            # 4. Check progress
            progress_info = progress_service.get_progress_info(session_id)
            assert progress_info["correct_answers"] == 5
            assert progress_info["current_question"] == 6
            
            # 5. Test completion check
            is_complete = progress_service.is_lesson_complete(session_id)
            assert not is_complete  # Should not be complete yet
            
            # Complete the session
            session_service.update_session_progress(session_id, current_question=21)
            is_complete = progress_service.is_lesson_complete(session_id)
            assert is_complete
            
            # 6. Calculate results
            results = progress_service.calculate_results(session_id)
            assert results.correct_answers == 5
            assert results.accuracy_percentage == 100.0
            
            logger.info("✅ Service integration working correctly")
            return True
            
        except Exception as e:
            logger.error(f"❌ Service integration failed: {e}")
            return False
    
    def test_functional_parity(self) -> bool:
        """Test functional parity with legacy system."""
        logger.info("Testing functional parity...")
        
        try:
            if not self.container:
                logger.error("Container not available for parity test")
                return False
            
            from core.interfaces.learn_services import ILessonConfigurationService
            config_service = self.container.resolve(ILessonConfigurationService)
            
            # Test all lesson types exist (matching legacy)
            configs = config_service.get_all_lesson_configs()
            expected_lessons = ["Lesson1", "Lesson2", "Lesson3"]
            
            for lesson_id in expected_lessons:
                assert lesson_id in configs, f"Missing lesson: {lesson_id}"
            
            # Test lesson 1 configuration (pictograph to letter)
            lesson1 = configs["Lesson1"]
            assert lesson1.question_format == "pictograph"
            assert lesson1.answer_format == "button"
            assert lesson1.quiz_description == "pictograph_to_letter"
            
            # Test lesson 2 configuration (letter to pictograph)
            lesson2 = configs["Lesson2"]
            assert lesson2.question_format == "letter"
            assert lesson2.answer_format == "pictograph"
            assert lesson2.quiz_description == "letter_to_pictograph"
            
            # Test lesson 3 configuration (valid next pictograph)
            lesson3 = configs["Lesson3"]
            assert lesson3.question_format == "pictograph"
            assert lesson3.answer_format == "pictograph"
            assert lesson3.quiz_description == "valid_next_pictograph"
            
            # Test quiz modes match legacy
            from domain.models.learn import QuizMode
            fixed_mode = QuizMode.FIXED_QUESTION
            countdown_mode = QuizMode.COUNTDOWN
            
            assert fixed_mode.value == "fixed_question"
            assert countdown_mode.value == "countdown"
            
            logger.info("✅ Functional parity verified")
            return True
            
        except Exception as e:
            logger.error(f"❌ Functional parity failed: {e}")
            return False
    
    def test_error_handling(self) -> bool:
        """Test error handling and edge cases."""
        logger.info("Testing error handling...")
        
        try:
            if not self.container:
                logger.error("Container not available for error test")
                return False
            
            from core.interfaces.learn_services import (
                IQuizSessionService, IAnswerValidationService
            )
            from domain.models.learn import QuestionData
            
            session_service = self.container.resolve(IQuizSessionService)
            validation_service = self.container.resolve(IAnswerValidationService)
            
            # Test invalid session operations
            invalid_session = session_service.get_session("invalid-session-id")
            assert invalid_session is None
            
            update_invalid = session_service.update_session_progress(
                "invalid-session-id", current_question=5
            )
            assert not update_invalid
            
            # Test invalid answer validation
            invalid_question = QuestionData()  # Empty question
            validation_result = validation_service.check_answer(invalid_question, "A")
            assert not validation_result  # Should handle gracefully
            
            # Test invalid lesson config requests
            from core.interfaces.learn_services import ILessonConfigurationService
            from domain.models.learn import LessonType
            
            config_service = self.container.resolve(ILessonConfigurationService)
            
            # This should handle gracefully and return None
            try:
                fake_lesson_type = "INVALID_LESSON_TYPE"
                config = config_service.get_lesson_config(fake_lesson_type)
                # Should return None rather than crash
            except Exception:
                # If it throws, that's also acceptable error handling
                pass
            
            logger.info("✅ Error handling working correctly")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error handling failed: {e}")
            return False
    
    def test_performance(self) -> bool:
        """Test basic performance requirements."""
        logger.info("Testing performance...")
        
        try:
            if not self.container:
                logger.error("Container not available for performance test")
                return False
            
            import time
            from core.interfaces.learn_services import (
                IQuizSessionService, ILessonConfigurationService
            )
            from domain.models.learn import LessonType, QuizMode
            
            session_service = self.container.resolve(IQuizSessionService)
            config_service = self.container.resolve(ILessonConfigurationService)
            
            # Test session creation performance
            start_time = time.time()
            for i in range(100):
                session_id = session_service.create_session(
                    LessonType.PICTOGRAPH_TO_LETTER,
                    QuizMode.FIXED_QUESTION
                )
            creation_time = time.time() - start_time
            
            # Should be able to create 100 sessions in reasonable time
            assert creation_time < 1.0, f"Session creation too slow: {creation_time}s"
            
            # Test config access performance
            start_time = time.time()
            for i in range(1000):
                configs = config_service.get_all_lesson_configs()
            config_time = time.time() - start_time
            
            # Should be able to access configs quickly
            assert config_time < 1.0, f"Config access too slow: {config_time}s"
            
            logger.info("✅ Performance requirements met")
            return True
            
        except Exception as e:
            logger.error(f"❌ Performance test failed: {e}")
            return False


def main():
    """Run the battle test suite."""
    battle_test = LearnTabBattleTest()
    success = battle_test.run_all_tests()
    
    if success:
        print("\n🎉 BATTLE TEST PASSED - Learn Tab implementation is ready!")
        return 0
    else:
        print("\n💀 BATTLE TEST FAILED - Implementation needs fixes")
        return 1


if __name__ == "__main__":
    exit(main())
