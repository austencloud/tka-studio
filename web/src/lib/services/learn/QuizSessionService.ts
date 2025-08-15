/**
 * Quiz Session Service
 *
 * Manages quiz sessions, progress tracking, and session state.
 * Handles both fixed question and countdown quiz modes.
 */

import {
  type LessonProgress,
  type LessonResults,
  type QuizSession,
  type TimerState,
  LessonType,
  QuizMode,
} from "$lib/types/learn";
import { LessonConfigService } from "./LessonConfigService";

export class QuizSessionService {
  private static activeSessions: Map<string, QuizSession> = new Map();
  private static timers: Map<string, NodeJS.Timeout> = new Map();

  /**
   * Create a new quiz session.
   */
  static createSession(lessonType: LessonType, quizMode: QuizMode): string {
    const sessionId = this.generateSessionId();
    const totalQuestions = LessonConfigService.getTotalQuestions(quizMode);
    const quizTime = LessonConfigService.getQuizTime(quizMode);

    const session: QuizSession = {
      sessionId,
      lessonType,
      quizMode,
      currentQuestion: 1,
      totalQuestions,
      questionsAnswered: 0,
      correctAnswers: 0,
      incorrectGuesses: 0,
      quizTime,
      startTime: new Date(),
      lastInteraction: new Date(),
      isActive: true,
      isCompleted: false,
    };

    this.activeSessions.set(sessionId, session);
    return sessionId;
  }

  /**
   * Get an active session.
   */
  static getSession(sessionId: string): QuizSession | null {
    return this.activeSessions.get(sessionId) || null;
  }

  /**
   * Update session progress.
   */
  static updateSessionProgress(
    sessionId: string,
    isCorrect: boolean,
    timeElapsed?: number
  ): QuizSession | null {
    const session = this.getSession(sessionId);
    if (!session || !session.isActive) {
      return null;
    }

    // Update progress
    session.questionsAnswered++;
    if (isCorrect) {
      session.correctAnswers++;
    } else {
      session.incorrectGuesses++;
    }

    // Update timing
    session.lastInteraction = new Date();
    if (timeElapsed !== undefined && session.quizMode === QuizMode.COUNTDOWN) {
      session.quizTime = Math.max(0, session.quizTime - timeElapsed);
    }

    // Move to next question for fixed question mode
    if (session.quizMode === QuizMode.FIXED_QUESTION) {
      session.currentQuestion++;
    }

    // Check completion conditions
    this.checkSessionCompletion(sessionId);

    return session;
  }

  /**
   * Check if session should be completed.
   */
  private static checkSessionCompletion(sessionId: string): void {
    const session = this.getSession(sessionId);
    if (!session) return;

    let shouldComplete = false;

    if (session.quizMode === QuizMode.FIXED_QUESTION) {
      // Complete when all questions are answered
      shouldComplete = session.questionsAnswered >= session.totalQuestions;
    } else if (session.quizMode === QuizMode.COUNTDOWN) {
      // Complete when time runs out
      shouldComplete = session.quizTime <= 0;
    }

    if (shouldComplete) {
      this.completeSession(sessionId);
    }
  }

  /**
   * Complete a quiz session.
   */
  static completeSession(sessionId: string): LessonResults | null {
    const session = this.getSession(sessionId);
    if (!session) return null;

    session.isActive = false;
    session.isCompleted = true;

    // Stop any running timers
    this.stopTimer(sessionId);

    // Calculate results
    const results = this.calculateResults(session);

    // Clean up session
    this.activeSessions.delete(sessionId);

    return results;
  }

  /**
   * Calculate lesson results from session.
   */
  private static calculateResults(session: QuizSession): LessonResults {
    if (!session.lessonType || !session.quizMode) {
      throw new Error(
        "Session must have lessonType and quizMode to calculate results"
      );
    }

    const completionTime =
      (new Date().getTime() - session.startTime.getTime()) / 1000;
    const accuracyPercentage =
      session.questionsAnswered > 0
        ? (session.correctAnswers / session.questionsAnswered) * 100
        : 0;
    const averageTimePerQuestion =
      session.questionsAnswered > 0
        ? completionTime / session.questionsAnswered
        : 0;

    return {
      sessionId: session.sessionId,
      lessonType: session.lessonType,
      quizMode: session.quizMode,
      totalQuestions: session.totalQuestions,
      correctAnswers: session.correctAnswers,
      incorrectGuesses: session.incorrectGuesses,
      questionsAnswered: session.questionsAnswered,
      accuracyPercentage: Math.round(accuracyPercentage * 100) / 100,
      completionTimeSeconds: Math.round(completionTime),
      completedAt: new Date(),
      averageTimePerQuestion: Math.round(averageTimePerQuestion * 100) / 100,
      streakLongestCorrect: 0, // TODO: Implement streak tracking
    };
  }

  /**
   * Get current lesson progress.
   */
  static getLessonProgress(sessionId: string): LessonProgress | null {
    const session = this.getSession(sessionId);
    if (!session) return null;

    const timeElapsed =
      (new Date().getTime() - session.startTime.getTime()) / 1000;

    return {
      currentQuestion: session.currentQuestion,
      totalQuestions: session.totalQuestions,
      correctAnswers: session.correctAnswers,
      incorrectAnswers: session.incorrectGuesses,
      questionsAnswered: session.questionsAnswered,
      timeElapsed: Math.round(timeElapsed),
      streakCurrent: 0, // TODO: Implement streak tracking
      streakLongest: 0,
    };
  }

  /**
   * Start countdown timer for a session.
   */
  static startTimer(
    sessionId: string,
    onTick?: (timeRemaining: number) => void
  ): void {
    const session = this.getSession(sessionId);
    if (!session || session.quizMode !== QuizMode.COUNTDOWN) return;

    // Clear existing timer
    this.stopTimer(sessionId);

    const timer = setInterval(() => {
      const currentSession = this.getSession(sessionId);
      if (!currentSession || !currentSession.isActive) {
        this.stopTimer(sessionId);
        return;
      }

      currentSession.quizTime = Math.max(0, currentSession.quizTime - 1);
      onTick?.(currentSession.quizTime);

      if (currentSession.quizTime <= 0) {
        this.completeSession(sessionId);
      }
    }, 1000);

    this.timers.set(sessionId, timer);
  }

  /**
   * Stop timer for a session.
   */
  static stopTimer(sessionId: string): void {
    const timer = this.timers.get(sessionId);
    if (timer) {
      clearInterval(timer);
      this.timers.delete(sessionId);
    }
  }

  /**
   * Pause/resume timer for a session.
   */
  static pauseTimer(sessionId: string): void {
    this.stopTimer(sessionId);
  }

  /**
   * Get timer state for a session.
   */
  static getTimerState(sessionId: string): TimerState | null {
    const session = this.getSession(sessionId);
    if (!session || !session.quizMode) return null;

    const isRunning = this.timers.has(sessionId);
    const totalTime = LessonConfigService.getQuizTime(session.quizMode);

    return {
      timeRemaining: session.quizTime,
      isRunning,
      isPaused: !isRunning && session.isActive,
      totalTime,
    };
  }

  /**
   * Abandon a session.
   */
  static abandonSession(sessionId: string): void {
    this.stopTimer(sessionId);
    this.activeSessions.delete(sessionId);
  }

  /**
   * Get all active sessions.
   */
  static getActiveSessions(): QuizSession[] {
    return Array.from(this.activeSessions.values());
  }

  /**
   * Clean up expired sessions.
   */
  static cleanupExpiredSessions(maxAgeMinutes: number = 30): void {
    const now = new Date();
    const maxAge = maxAgeMinutes * 60 * 1000;

    for (const [sessionId, session] of this.activeSessions.entries()) {
      const age = now.getTime() - session.lastInteraction.getTime();
      if (age > maxAge) {
        this.abandonSession(sessionId);
      }
    }
  }

  /**
   * Generate unique session ID.
   */
  private static generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Format time for display (MM:SS).
   */
  static formatTime(seconds: number): string {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
  }

  /**
   * Get session statistics.
   */
  static getSessionStats(): {
    totalSessions: number;
    activeSessions: number;
    completedSessions: number;
  } {
    const activeSessions = this.activeSessions.size;
    // Note: We don't track completed sessions in this simple implementation
    // In a real app, you'd want to persist this data

    return {
      totalSessions: activeSessions, // This would be total from database
      activeSessions,
      completedSessions: 0, // This would be from database
    };
  }
}
