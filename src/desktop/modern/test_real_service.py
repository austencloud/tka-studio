#!/usr/bin/env python3
"""
Test Real Pictograph Service for Lesson3

Verify that the real service provides actual TKA pictographs
with proper position data for Lesson3 functionality.
"""

import sys
import logging
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Setup logging to see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_real_pictograph_service():
    """Test the real pictograph service for Lesson3 compatibility."""
    print("TESTING REAL PICTOGRAPH SERVICE")
    print("=" * 60)
    
    try:
        from PyQt6.QtWidgets import QApplication
        
        # Create Qt application
        app = QApplication(sys.argv)
        
        print("\nStep 1: Setup Real Service")
        print("-" * 40)
        
        from core.dependency_injection.di_container import DIContainer
        from core.dependency_injection.learn_service_registration import register_learn_services
        from core.interfaces.data_builder_services import IPictographDataService
        from domain.models.pictograph_data import PictographData
        
        # Setup DI container with real services
        container = DIContainer()
        register_learn_services(container)
        
        # Get the pictograph service (should be real now)
        pictograph_service = container.resolve(IPictographDataService)
        service_type = type(pictograph_service).__name__
        print(f"Service Type: {service_type}")
        
        if "Real" in service_type:
            print("SUCCESS: Using REAL Pictograph Service!")
        elif "Mock" in service_type:
            print("ERROR: Still using Mock Service - check service registration")
            return False
        else:
            print(f"WARNING: Unknown service type: {service_type}")
        
        print(f"\nStep 2: Test Real Dataset Retrieval")
        print("-" * 40)
        
        # Test dataset retrieval
        dataset = pictograph_service.get_pictograph_dataset()
        print(f"Dataset loaded with {len(dataset)} letters")
        
        if len(dataset) == 0:
            print("ERROR: No letters in dataset!")
            return False
        
        # Test specific letters
        test_letters = ["A", "B", "C"]
        total_variety_check = 0
        
        for letter in test_letters:
            letter_data = dataset.get(letter, [])
            print(f"Letter '{letter}' has {len(letter_data)} pictographs")
            
            if letter_data:
                sample = letter_data[0]
                print(f"   Keys: {list(sample.keys())}")
                
                # Check for both legacy and modern data
                has_start_pos = "start_pos" in sample
                has_end_pos = "end_pos" in sample
                has_data = "data" in sample
                
                print(f"   Has start_pos: {has_start_pos} - Value: {sample.get('start_pos', 'MISSING')}")
                print(f"   Has end_pos: {has_end_pos} - Value: {sample.get('end_pos', 'MISSING')}")
                print(f"   Has data: {has_data}")
                
                if has_data:
                    data_obj = sample["data"]
                    is_pictograph_data = isinstance(data_obj, PictographData)
                    print(f"   Data is PictographData: {is_pictograph_data}")
                    
                    if is_pictograph_data:
                        print(f"   REAL Pictograph: {data_obj.letter} - {data_obj.id}")
                        print(f"   Grid Mode: {data_obj.grid_data.grid_mode if data_obj.grid_data else 'None'}")
                        print(f"   Arrows: {len(data_obj.arrows) if data_obj.arrows else 0}")
                        
                        # Check if we have variety for Lesson3
                        same_pos_count = sum(1 for p in letter_data 
                                           if p.get('start_pos') == p.get('end_pos'))
                        print(f"   Same position pictographs: {same_pos_count}")
                        
                        start_positions = set(p.get('start_pos') for p in letter_data)
                        print(f"   Unique start positions: {sorted(start_positions)}")
                        
                        if same_pos_count > 0 and len(start_positions) >= 3:
                            print(f"   SUCCESS: Letter {letter} has good variety for Lesson3!")
                            total_variety_check += 1
                        else:
                            print(f"   WARNING: Letter {letter} has limited variety ({same_pos_count} same, {len(start_positions)} positions)")
                    else:
                        print(f"   ERROR: Data is not PictographData: {type(data_obj)}")
                        return False
                else:
                    print(f"   ERROR: No data field in sample")
                    return False
            else:
                print(f"   ERROR: No pictographs for letter {letter}")
        
        if total_variety_check == 0:
            print("ERROR: No letters have sufficient variety for Lesson3")
            return False
        
        print(f"\nStep 3: Test Question Generation with Real Data")
        print("-" * 40)
        
        # Test if question generation works with real data
        from core.interfaces.learn_services import IQuestionGenerationService, IQuizSessionService
        from domain.models.learn import LessonType, QuizMode
        from application.services.learn.lesson_configuration_service import LessonConfigurationService
        
        # Get services
        session_service = container.resolve(IQuizSessionService)
        question_service = container.resolve(IQuestionGenerationService)
        config_service = LessonConfigurationService()
        
        # Get Lesson3 config
        lesson3_config = config_service.get_lesson_config(LessonType.VALID_NEXT_PICTOGRAPH)
        
        if lesson3_config:
            print(f"Lesson3 config loaded: {lesson3_config.lesson_type}")
            
            # Create session
            session_id = session_service.create_session(LessonType.VALID_NEXT_PICTOGRAPH, QuizMode.FIXED_QUESTION)
            print(f"Created session: {session_id}")
            
            # Generate question with REAL data
            try:
                question = question_service.generate_question(session_id, lesson3_config)
                
                if question:
                    print("REAL question generated successfully!")
                    print(f"   Question type: {question.question_type}")
                    print(f"   Has question content: {question.question_content is not None}")
                    print(f"   Number of answer options: {len(question.answer_options)}")
                    
                    # Check if question content is real PictographData
                    if question.question_content and isinstance(question.question_content, dict):
                        q_data = question.question_content.get("data")
                        if isinstance(q_data, PictographData):
                            print(f"   SUCCESS: Question shows REAL pictograph: {q_data.letter} - {q_data.id}")
                        
                    # Check answer options
                    real_options = 0
                    for i, option in enumerate(question.answer_options):
                        if isinstance(option, dict) and "data" in option:
                            opt_data = option["data"]
                            if isinstance(opt_data, PictographData):
                                real_options += 1
                    
                    print(f"   Answer options with REAL pictographs: {real_options}/{len(question.answer_options)}")
                    
                    if len(question.answer_options) >= 4 and real_options >= 4:
                        print("SUCCESS: Real pictographs working for Lesson3!")
                        return True
                    else:
                        print(f"ERROR: Not enough real answer options")
                        return False
                        
                else:
                    print("ERROR: Question generation returned None!")
                    return False
                    
            except Exception as e:
                print(f"ERROR: Question generation failed: {e}")
                import traceback
                traceback.print_exc()
                return False
        else:
            print("ERROR: Could not get Lesson3 configuration!")
            return False
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Real Pictograph Service for Lesson3")
    
    success = test_real_pictograph_service()
    
    if success:
        print("\nSUCCESS: Real pictograph service is working!")
        print("The service now provides:")
        print("- REAL TKA pictographs (not fake mock data)")
        print("- Legacy position data for question generation")
        print("- Modern PictographData objects for rendering")
        print("\nLesson3 should now show REAL pictographs!")
    else:
        print("\nERROR: Real pictograph service needs more work")
        print("Check the output above for specific issues.")
    
    print(f"\nResult: {'PASS' if success else 'FAIL'}")
