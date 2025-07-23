#!/usr/bin/env python3
"""
Test Lesson3 Fix - Verify that position data is working correctly
"""

import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_mock_service():
    """Test the mock pictograph data service for Lesson3 compatibility."""
    print("=" * 60)
    print("Testing Mock Pictograph Data Service for Lesson3")
    print("=" * 60)
    
    try:
        from application.services.learn.mock_pictograph_data_service import MockPictographDataService
        
        # Create service
        mock_service = MockPictographDataService()
        
        # Get dataset
        dataset = mock_service.get_pictograph_dataset()
        print(f"✅ Dataset loaded with {len(dataset)} letters")
        
        # Test a specific letter
        letter_a_data = dataset.get("A", [])
        print(f"✅ Letter 'A' has {len(letter_a_data)} pictographs")
        
        if letter_a_data:
            # Check first pictograph for position data
            sample = letter_a_data[0]
            print(f"✅ Sample pictograph keys: {list(sample.keys())}")
            
            # Check for START_POS and END_POS
            has_start_pos = "start_pos" in sample
            has_end_pos = "end_pos" in sample
            print(f"✅ Has start_pos: {has_start_pos}")
            print(f"✅ Has end_pos: {has_end_pos}")
            
            if has_start_pos and has_end_pos:
                print(f"✅ Position data: start_pos={sample['start_pos']}, end_pos={sample['end_pos']}")
            
            # Count pictographs where start_pos == end_pos (needed for Lesson3 initial question)
            same_pos_count = sum(1 for p in letter_a_data if p.get('start_pos') == p.get('end_pos'))
            print(f"✅ Pictographs with start_pos == end_pos: {same_pos_count}")
            
            # Count pictographs with different start positions (needed for answer options)
            start_positions = set(p.get('start_pos') for p in letter_a_data)
            print(f"✅ Unique start positions: {sorted(start_positions)}")
            
            # Check if we have enough data for valid next pictograph questions
            if same_pos_count > 0 and len(start_positions) >= 4:
                print("🎉 SUCCESS: Mock service should support Lesson3 properly!")
                return True
            else:
                print("❌ ISSUE: Mock service may not have enough variety for Lesson3")
                return False
        else:
            print("❌ No data for letter A")
            return False
            
    except Exception as e:
        print(f"❌ Mock service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_question_generation():
    """Test question generation for valid next pictograph."""
    print("\n" + "=" * 60)
    print("Testing Question Generation for Lesson3")
    print("=" * 60)
    
    try:
        from PyQt6.QtWidgets import QApplication
        
        # Create Qt application if needed
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        from core.dependency_injection.di_container import DIContainer
        from core.dependency_injection.learn_service_registration import register_learn_services
        from core.interfaces.learn_services import IQuestionGenerationService, IQuizSessionService
        from domain.models.learn import LessonType, QuizMode
        
        # Setup DI container
        container = DIContainer()
        register_learn_services(container)
        
        # Get services
        session_service = container.resolve(IQuizSessionService)
        question_service = container.resolve(IQuestionGenerationService)
        
        print("✅ Services resolved successfully")
        
        # Create a quiz session for Lesson3
        session_id = session_service.create_session(LessonType.VALID_NEXT_PICTOGRAPH, QuizMode.FIXED_QUESTION)
        print(f"✅ Quiz session created: {session_id}")
        
        # Get lesson config for Lesson3
        from application.services.learn.lesson_configuration_service import LessonConfigurationService
        config_service = LessonConfigurationService()
        lesson3_config = config_service.get_lesson_config(LessonType.VALID_NEXT_PICTOGRAPH)
        
        if not lesson3_config:
            print("❌ Could not get Lesson3 configuration")
            return False
        
        # Try to generate a question
        question = question_service.generate_question(session_id, lesson3_config)
        
        if question:
            print("✅ Question generated successfully!")
            print(f"   - Question type: {question.question_type}")
            print(f"   - Has content: {question.question_content is not None}")
            print(f"   - Number of options: {len(question.answer_options)}")
            print(f"   - Has correct answer: {question.correct_answer is not None}")
            
            # Check if we have the expected 4 answer options for Lesson3
            if len(question.answer_options) >= 4:
                print("🎉 SUCCESS: Question has enough answer options!")
                return True
            else:
                print(f"❌ ISSUE: Question only has {len(question.answer_options)} options (need 4)")
                return False
        else:
            print("❌ Question generation returned None")
            return False
            
    except Exception as e:
        print(f"❌ Question generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Lesson3 Fix")
    print("Verifying that Lesson3 shows correct start position and 4 answer options")
    
    results = []
    
    # Test mock service
    results.append(test_mock_service())
    
    # Test question generation  
    results.append(test_question_generation())
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Lesson3 fixes should be working correctly.")
        print("\nThe Learn Tab should now have:")
        print("• Proper start position pictograph display in Lesson3")
        print("• All 4 answer options (1 correct + 3 wrong) for valid next pictograph")
        print("• Working position data for 'valid next pictograph' logic")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
