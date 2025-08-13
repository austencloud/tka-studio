#!/usr/bin/env python3
"""
Diagnostic Script for Learn Tab Lesson3 Issues

This script checks what's actually happening in the modern learn tab
to help debug why Lesson3 is only showing 1 answer option.
"""

from __future__ import annotations

import logging
from pathlib import Path
import sys


# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Setup logging to see what's happening
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)


def diagnose_learn_tab():
    """Comprehensive diagnosis of learn tab Lesson3 issues."""

    print("🔍 LEARN TAB LESSON3 DIAGNOSTIC")
    print("=" * 60)

    try:
        from PyQt6.QtWidgets import QApplication

        # Create Qt application
        QApplication(sys.argv)

        print("\n📋 Step 1: Check Service Registration")
        print("-" * 40)

        from desktop.modern.core.dependency_injection.di_container import DIContainer
        from desktop.modern.core.dependency_injection.learn_service_registration import (
            register_learn_services,
        )
        from desktop.modern.core.interfaces.data_builder_services import (
            IPictographDataService,
        )
        from desktop.modern.core.interfaces.learn_services import (
            IQuestionGenerationService,
            IQuizSessionService,
        )

        # Setup DI container
        container = DIContainer()
        register_learn_services(container)

        # Check which pictograph service is registered
        pictograph_service = container.resolve(IPictographDataService)
        service_type = type(pictograph_service).__name__
        print(f"✅ Pictograph Service Type: {service_type}")

        if "Mock" in service_type:
            print("🎯 Using Mock Service (good for testing)")
        else:
            print("📡 Using Real Service (may need real data)")

        print("\n📋 Step 2: Test Pictograph Data Retrieval")
        print("-" * 40)

        # Test dataset retrieval
        dataset = pictograph_service.get_pictograph_dataset()
        print(f"✅ Dataset loaded with {len(dataset)} letters")

        # Test specific letter
        test_letter = "A"
        letter_data = dataset.get(test_letter, [])
        print(f"✅ Letter '{test_letter}' has {len(letter_data)} pictographs")

        if letter_data:
            sample = letter_data[0]
            print(f"✅ Sample pictograph keys: {list(sample.keys())}")

            # Check for position data
            has_start_pos = "start_pos" in sample
            has_end_pos = "end_pos" in sample
            print(
                f"✅ Has start_pos: {has_start_pos} - Value: {sample.get('start_pos', 'MISSING')}"
            )
            print(
                f"✅ Has end_pos: {has_end_pos} - Value: {sample.get('end_pos', 'MISSING')}"
            )

            # Count pictographs suitable for Lesson3 initial question (start_pos == end_pos)
            initial_candidates = [
                p for p in letter_data if p.get("start_pos") == p.get("end_pos")
            ]
            print(
                f"✅ Pictographs with start_pos == end_pos: {len(initial_candidates)}"
            )

            # Check position variety for answer options
            start_positions = {p.get("start_pos") for p in letter_data}
            end_positions = {p.get("end_pos") for p in letter_data}
            print(f"✅ Unique start positions: {sorted(start_positions)}")
            print(f"✅ Unique end positions: {sorted(end_positions)}")

            if len(initial_candidates) == 0:
                print("❌ PROBLEM: No pictographs with start_pos == end_pos found!")
                print("   This means Lesson3 can't generate an initial question.")

            if len(start_positions) < 4:
                print(
                    f"❌ PROBLEM: Only {len(start_positions)} unique start positions found!"
                )
                print("   This means not enough variety for 4 answer options.")

        print("\n📋 Step 3: Test Question Generation for Lesson3")
        print("-" * 40)

        # Get services
        session_service = container.resolve(IQuizSessionService)
        question_service = container.resolve(IQuestionGenerationService)

        # Test Lesson3 specifically
        from desktop.modern.application.services.learn.lesson_configuration_service import (
            LessonConfigurationService,
        )
        from desktop.modern.domain.models.learn import LessonType, QuizMode

        # Get Lesson3 config
        config_service = LessonConfigurationService()
        lesson3_config = config_service.get_lesson_config(
            LessonType.VALID_NEXT_PICTOGRAPH
        )

        if lesson3_config:
            print(f"✅ Lesson3 config: {lesson3_config.lesson_type}")
            print(f"   Question format: {lesson3_config.question_format}")
            print(f"   Answer format: {lesson3_config.answer_format}")
            print(f"   Description: {lesson3_config.quiz_description}")

            # Create session
            session_id = session_service.create_session(
                LessonType.VALID_NEXT_PICTOGRAPH, QuizMode.FIXED_QUESTION
            )
            print(f"✅ Created session: {session_id}")

            # Generate question
            try:
                question = question_service.generate_question(
                    session_id, lesson3_config
                )

                if question:
                    print("✅ Question generated successfully!")
                    print(f"   Question type: {question.question_type}")
                    print(
                        f"   Has question content: {question.question_content is not None}"
                    )
                    print(
                        f"   Number of answer options: {len(question.answer_options)}"
                    )
                    print(
                        f"   Has correct answer: {question.correct_answer is not None}"
                    )

                    # Analyze question content
                    if question.question_content:
                        q_content = question.question_content
                        if isinstance(q_content, dict):
                            q_start = q_content.get("start_pos", "UNKNOWN")
                            q_end = q_content.get("end_pos", "UNKNOWN")
                            print(f"   Question start_pos: {q_start}")
                            print(f"   Question end_pos: {q_end}")
                            print(
                                f"   Is initial pictograph (start==end): {q_start == q_end}"
                            )

                    # Analyze answer options
                    print("\n   Answer Options Analysis:")
                    for i, option in enumerate(question.answer_options):
                        if isinstance(option, dict):
                            opt_start = option.get("start_pos", "UNKNOWN")
                            opt_end = option.get("end_pos", "UNKNOWN")
                            is_correct = option == question.correct_answer
                            print(
                                f"     Option {i + 1}: start={opt_start}, end={opt_end} {'(CORRECT)' if is_correct else ''}"
                            )
                        else:
                            print(f"     Option {i + 1}: {type(option)} - {option}")

                    # Final assessment
                    if len(question.answer_options) >= 4:
                        print("🎉 SUCCESS: Question has enough answer options!")
                    else:
                        print(
                            f"❌ PROBLEM: Only {len(question.answer_options)} answer options (need 4)!"
                        )

                else:
                    print("❌ PROBLEM: Question generation returned None!")

            except Exception as e:
                print(f"❌ PROBLEM: Question generation failed: {e}")
                import traceback

                traceback.print_exc()
        else:
            print("❌ PROBLEM: Could not get Lesson3 configuration!")

        print("\n📋 Step 4: Summary & Recommendations")
        print("-" * 40)

        if service_type == "MockPictographDataService":
            print("✅ Using Mock Service - this should have fixed position data")
            print("   If still seeing issues, check question generation logic")
        else:
            print("⚠️  Using Real Service - may not have proper position data")
            print("   Consider switching to Mock Service for testing")

        print("\n🎯 To fix the issue:")
        print("1. Ensure MockPictographDataService is being used")
        print("2. Verify position data is present in pictographs")
        print("3. Check that question generation handles position data correctly")
        print("4. Make sure all 4 answer options are being generated")

        return True

    except Exception as e:
        print(f"❌ Diagnostic failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Starting Learn Tab Lesson3 Diagnostic...")

    success = diagnose_learn_tab()

    if success:
        print("\n✅ Diagnostic completed!")
        print("Check the output above to identify any issues.")
    else:
        print("\n❌ Diagnostic failed!")
        print("Check the error messages above.")

    print(f"\nResult: {'PASS' if success else 'FAIL'}")
