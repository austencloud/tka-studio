/**
 * Lesson Configuration Service
 *
 * Manages lesson configurations, validation, and provides utilities
 * for working with different lesson types and quiz modes.
 */

import {
  AnswerFormat,
  LESSON_CONFIGS,
  LESSON_INFO,
  LESSON_TYPE_NAMES,
  type LessonConfig,
  type LessonInfo,
  LessonType,
  QuestionFormat,
  QUIZ_DEFAULTS,
  QUIZ_MODE_NAMES,
  QuizMode,
} from "$lib/types/learn";

export class LessonConfigService {
  /**
   * Get configuration for a specific lesson type.
   */
  static getLessonConfig(lessonType: LessonType): LessonConfig {
    const config = LESSON_CONFIGS[lessonType];
    if (!config) {
      throw new Error(`No configuration found for lesson type: ${lessonType}`);
    }
    return config;
  }

  /**
   * Get lesson information for display.
   */
  static getLessonInfo(lessonType: LessonType): LessonInfo {
    const info = LESSON_INFO.find((lesson) => lesson.lessonType === lessonType);
    if (!info) {
      throw new Error(`No lesson info found for lesson type: ${lessonType}`);
    }
    return info;
  }

  /**
   * Get all available lesson types.
   */
  static getAvailableLessonTypes(): LessonType[] {
    return Object.values(LessonType);
  }

  /**
   * Get all available quiz modes.
   */
  static getAvailableQuizModes(): QuizMode[] {
    return Object.values(QuizMode);
  }

  /**
   * Get display name for a lesson type.
   */
  static getLessonTypeName(lessonType: LessonType): string {
    return LESSON_TYPE_NAMES[lessonType] || lessonType;
  }

  /**
   * Get display name for a quiz mode.
   */
  static getQuizModeName(quizMode: QuizMode): string {
    return QUIZ_MODE_NAMES[quizMode] || quizMode;
  }

  /**
   * Get total questions for a quiz mode.
   */
  static getTotalQuestions(quizMode: QuizMode): number {
    switch (quizMode) {
      case QuizMode.FIXED_QUESTION:
        return QUIZ_DEFAULTS.FIXED_QUESTION_COUNT;
      case QuizMode.COUNTDOWN:
        return 0; // Unlimited questions in countdown mode
      default:
        return QUIZ_DEFAULTS.FIXED_QUESTION_COUNT;
    }
  }

  /**
   * Get quiz time for a quiz mode.
   */
  static getQuizTime(quizMode: QuizMode): number {
    switch (quizMode) {
      case QuizMode.COUNTDOWN:
        return QUIZ_DEFAULTS.COUNTDOWN_TIME_SECONDS;
      case QuizMode.FIXED_QUESTION:
        return 0; // No time limit for fixed question mode
      default:
        return 0;
    }
  }

  /**
   * Validate lesson configuration.
   */
  static validateLessonConfig(config: LessonConfig): boolean {
    return (
      Object.values(LessonType).includes(config.lessonType) &&
      Object.values(QuestionFormat).includes(config.questionFormat) &&
      Object.values(AnswerFormat).includes(config.answerFormat) &&
      typeof config.quizDescription === "string" &&
      typeof config.questionPrompt === "string"
    );
  }

  /**
   * Check if a lesson type supports a specific question format.
   */
  static supportsQuestionFormat(
    lessonType: LessonType,
    format: QuestionFormat,
  ): boolean {
    const config = this.getLessonConfig(lessonType);
    return config.questionFormat === format;
  }

  /**
   * Check if a lesson type supports a specific answer format.
   */
  static supportsAnswerFormat(
    lessonType: LessonType,
    format: AnswerFormat,
  ): boolean {
    const config = this.getLessonConfig(lessonType);
    return config.answerFormat === format;
  }

  /**
   * Get lesson number from lesson type (for display purposes).
   */
  static getLessonNumber(lessonType: LessonType): number {
    switch (lessonType) {
      case LessonType.PICTOGRAPH_TO_LETTER:
        return 1;
      case LessonType.LETTER_TO_PICTOGRAPH:
        return 2;
      case LessonType.VALID_NEXT_PICTOGRAPH:
        return 3;
      default:
        return 0;
    }
  }

  /**
   * Get lesson type from lesson number.
   */
  static getLessonTypeFromNumber(lessonNumber: number): LessonType | null {
    switch (lessonNumber) {
      case 1:
        return LessonType.PICTOGRAPH_TO_LETTER;
      case 2:
        return LessonType.LETTER_TO_PICTOGRAPH;
      case 3:
        return LessonType.VALID_NEXT_PICTOGRAPH;
      default:
        return null;
    }
  }

  /**
   * Get formatted lesson title for display.
   */
  static getFormattedLessonTitle(lessonType: LessonType): string {
    const lessonNumber = this.getLessonNumber(lessonType);
    const lessonName = this.getLessonTypeName(lessonType);
    return `Lesson ${lessonNumber}: ${lessonName}`;
  }

  /**
   * Get lesson description for display.
   */
  static getLessonDescription(lessonType: LessonType): string {
    const info = this.getLessonInfo(lessonType);
    return info.description;
  }

  /**
   * Check if a lesson is available (for future use with unlocking system).
   */
  static isLessonAvailable(_lessonType: LessonType): boolean {
    // For now, all lessons are available
    // This can be extended to support lesson unlocking logic
    return true;
  }

  /**
   * Get recommended quiz mode for a lesson type.
   */
  static getRecommendedQuizMode(lessonType: LessonType): QuizMode {
    // For beginners, start with fixed questions
    // More advanced lessons could default to countdown
    switch (lessonType) {
      case LessonType.PICTOGRAPH_TO_LETTER:
        return QuizMode.FIXED_QUESTION;
      case LessonType.LETTER_TO_PICTOGRAPH:
        return QuizMode.FIXED_QUESTION;
      case LessonType.VALID_NEXT_PICTOGRAPH:
        return QuizMode.COUNTDOWN; // More challenging lesson
      default:
        return QuizMode.FIXED_QUESTION;
    }
  }

  /**
   * Get difficulty level for a lesson type (1-5 scale).
   */
  static getDifficultyLevel(lessonType: LessonType): number {
    switch (lessonType) {
      case LessonType.PICTOGRAPH_TO_LETTER:
        return 1; // Easiest - just matching pictograph to letter
      case LessonType.LETTER_TO_PICTOGRAPH:
        return 2; // Medium - requires understanding pictograph structure
      case LessonType.VALID_NEXT_PICTOGRAPH:
        return 4; // Hardest - requires understanding flow and transitions
      default:
        return 1;
    }
  }

  /**
   * Get estimated completion time for a lesson (in minutes).
   */
  static getEstimatedCompletionTime(
    lessonType: LessonType,
    quizMode: QuizMode,
  ): number {
    const baseTime = this.getDifficultyLevel(lessonType) * 2; // 2 minutes per difficulty level

    switch (quizMode) {
      case QuizMode.FIXED_QUESTION:
        return baseTime + 5; // Add 5 minutes for fixed questions
      case QuizMode.COUNTDOWN:
        return 2; // Countdown mode is always 2 minutes
      default:
        return baseTime;
    }
  }
}
