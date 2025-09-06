/**
 * Quiz Session Service Interface
 *
 * Interface for managing quiz sessions, progress tracking, and session state.
 */

import type { QuizMode, QuizResults, QuizSession, QuizType } from "../../domain";

export interface IQuizSessionService {
  /**
   * Start a new quiz session
   */
  startQuiz(lessonId: string): Promise<void>;

  /**
   * Get the current active session
   */
  getCurrentSession(): QuizSession | null;

  /**
   * Submit an answer for the current question
   */
  submitAnswer(answer: any): Promise<boolean>;

  /**
   * Complete the current quiz
   */
  completeQuiz(): Promise<QuizResults | null>;

  /**
   * Restart the current quiz
   */
  restartQuiz(): Promise<void>;

  /**
   * Clean up resources
   */
  cleanup(): void;

  /**
   * Create a new quiz session
   */
  createSession(lessonType: QuizType, quizMode: QuizMode): string;

  /**
   * Get session by ID
   */
  getSession(sessionId: string): QuizSession | null;

  /**
   * Update session progress
   */
  updateSessionProgress(
    sessionId: string,
    isCorrect: boolean,
    timeElapsed?: number
  ): QuizSession | null;

  /**
   * Complete a session
   */
  completeSession(sessionId: string): QuizResults | null;

  /**
   * Abandon a session
   */
  abandonSession(sessionId: string): void;
}
