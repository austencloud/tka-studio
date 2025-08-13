/**
 * Learn Tab Type Definitions
 *
 * TypeScript interfaces and enums that match the desktop Learn tab implementation
 * for consistent data structures across the application.
 */

/**
 * Types of lessons available in the learning module.
 */
export enum LessonType {
  PICTOGRAPH_TO_LETTER = "pictograph_to_letter",
  LETTER_TO_PICTOGRAPH = "letter_to_pictograph",
  VALID_NEXT_PICTOGRAPH = "valid_next_pictograph",
}

/**
 * Quiz modes for lesson execution.
 */
export enum QuizMode {
  FIXED_QUESTION = "fixed_question",
  COUNTDOWN = "countdown",
}

/**
 * Available views in the learn tab.
 */
export enum LearnView {
  LESSON_SELECTOR = "lesson_selector",
  LESSON_WORKSPACE = "lesson_workspace",
  LESSON_RESULTS = "lesson_results",
}

/**
 * Layout modes for lesson workspace.
 */
export enum LayoutMode {
  VERTICAL = "vertical", // Question top, answers bottom
  HORIZONTAL = "horizontal", // Question left, answers right
}

/**
 * Question formats for different lesson types.
 */
export enum QuestionFormat {
  PICTOGRAPH = "pictograph",
  LETTER = "letter",
  TEXT = "text",
}

/**
 * Answer formats for different lesson types.
 */
export enum AnswerFormat {
  BUTTON = "button",
  PICTOGRAPH = "pictograph",
}

/**
 * Answer feedback types.
 */
export enum AnswerFeedback {
  CORRECT = "correct",
  INCORRECT = "incorrect",
  NONE = "none",
}

/**
 * Configuration data for a lesson type.
 * Contains all static configuration needed to set up and run a lesson.
 */
export interface LessonConfig {
  lessonType: LessonType;
  questionFormat: QuestionFormat;
  answerFormat: AnswerFormat;
  quizDescription: string;
  questionPrompt: string;
}

/**
 * Lesson information for display in the lesson selector.
 */
export interface LessonInfo {
  name: string;
  description: string;
  lessonType: LessonType;
}

/**
 * Represents a quiz question with content and answer options.
 */
export interface QuestionData {
  questionId: string;
  questionContent: unknown; // Pictograph data, letter string, or text
  answerOptions: AnswerOption[]; // Array of answer choices
  correctAnswer: unknown; // The correct answer from the options
  questionType: QuestionFormat;
  answerType: AnswerFormat;
  lessonType: LessonType;
  generationTimestamp?: string;
  difficultyLevel?: number;
}

/**
 * Answer option for quiz questions.
 */
export interface AnswerOption {
  id: string;
  content: unknown; // Letter string, pictograph data, etc.
  isCorrect: boolean;
  feedback?: string;
}

/**
 * Timer state for countdown mode.
 */
export interface TimerState {
  timeRemaining: number; // seconds
  isRunning: boolean;
  isPaused: boolean;
  totalTime: number; // initial time in seconds
}

/**
 * Progress tracking for lessons.
 */
export interface LessonProgress {
  currentQuestion: number;
  totalQuestions: number;
  correctAnswers: number;
  incorrectAnswers: number;
  questionsAnswered: number;
  timeElapsed: number; // seconds
  streakCurrent: number;
  streakLongest: number;
}

/**
 * Represents an active quiz session with state and progress tracking.
 */
export interface QuizSession {
  sessionId: string;
  lessonType: LessonType | null;
  quizMode: QuizMode | null;
  currentQuestion: number;
  totalQuestions: number;
  questionsAnswered: number;
  correctAnswers: number;
  incorrectGuesses: number;
  quizTime: number; // seconds remaining for countdown mode
  startTime: Date;
  lastInteraction: Date;
  isActive: boolean;
  isCompleted: boolean;
}

/**
 * Represents the final results and statistics for a completed lesson.
 */
export interface LessonResults {
  sessionId: string;
  lessonType: LessonType;
  quizMode: QuizMode;
  totalQuestions: number;
  correctAnswers: number;
  incorrectGuesses: number;
  questionsAnswered: number;
  accuracyPercentage: number;
  completionTimeSeconds: number;
  completedAt: Date;
  averageTimePerQuestion?: number;
  streakLongestCorrect?: number;
}

/**
 * State for the learn tab.
 */
export interface LearnState {
  currentView: LearnView;
  selectedMode: QuizMode;
  activeSession: QuizSession | null;
  isLoading: boolean;
  error: string | null;
}

/**
 * Lesson configurations matching the desktop implementation.
 */
export const LESSON_CONFIGS: Record<LessonType, LessonConfig> = {
  [LessonType.PICTOGRAPH_TO_LETTER]: {
    lessonType: LessonType.PICTOGRAPH_TO_LETTER,
    questionFormat: QuestionFormat.PICTOGRAPH,
    answerFormat: AnswerFormat.BUTTON,
    quizDescription: "pictograph_to_letter",
    questionPrompt: "Choose the letter for:",
  },
  [LessonType.LETTER_TO_PICTOGRAPH]: {
    lessonType: LessonType.LETTER_TO_PICTOGRAPH,
    questionFormat: QuestionFormat.LETTER,
    answerFormat: AnswerFormat.PICTOGRAPH,
    quizDescription: "letter_to_pictograph",
    questionPrompt: "Choose the pictograph for:",
  },
  [LessonType.VALID_NEXT_PICTOGRAPH]: {
    lessonType: LessonType.VALID_NEXT_PICTOGRAPH,
    questionFormat: QuestionFormat.PICTOGRAPH,
    answerFormat: AnswerFormat.PICTOGRAPH,
    quizDescription: "valid_next_pictograph",
    questionPrompt: "Which pictograph can follow?",
  },
};

/**
 * Lesson information for display in the lesson selector.
 */
export const LESSON_INFO: LessonInfo[] = [
  {
    name: "Lesson 1",
    description: "Match the correct letter to the given pictograph",
    lessonType: LessonType.PICTOGRAPH_TO_LETTER,
  },
  {
    name: "Lesson 2",
    description: "Identify the correct pictograph for the displayed letter",
    lessonType: LessonType.LETTER_TO_PICTOGRAPH,
  },
  {
    name: "Lesson 3",
    description: "Choose the pictograph that logically follows",
    lessonType: LessonType.VALID_NEXT_PICTOGRAPH,
  },
];

/**
 * Default quiz settings.
 */
export const QUIZ_DEFAULTS = {
  FIXED_QUESTION_COUNT: 20,
  COUNTDOWN_TIME_SECONDS: 120,
  ANSWER_OPTIONS_COUNT: 4,
} as const;

/**
 * Quiz mode display names.
 */
export const QUIZ_MODE_NAMES: Record<QuizMode, string> = {
  [QuizMode.FIXED_QUESTION]: "Fixed Questions",
  [QuizMode.COUNTDOWN]: "Countdown",
};

/**
 * Lesson type display names.
 */
export const LESSON_TYPE_NAMES: Record<LessonType, string> = {
  [LessonType.PICTOGRAPH_TO_LETTER]: "Pictograph to Letter",
  [LessonType.LETTER_TO_PICTOGRAPH]: "Letter to Pictograph",
  [LessonType.VALID_NEXT_PICTOGRAPH]: "Valid Next Pictograph",
};
