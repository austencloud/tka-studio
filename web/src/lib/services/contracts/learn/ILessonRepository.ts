/**
 * Lesson Repository Interface
 *
 * Contract for lesson configuration management and retrieval.
 * Handles lesson types, configurations, and category management.
 */

import type { LessonConfiguration, LetterCategory } from "$domain";

export interface ILessonRepository {
  /**
   * Initialize the repository with lesson configurations
   */
  initialize(): Promise<void>;

  /**
   * Get lesson configuration by lesson type
   */
  getLessonConfiguration(lessonType: string): LessonConfiguration | null;

  /**
   * Get all available lesson types
   */
  getAllLessonTypes(): string[];

  /**
   * Get letters associated with a specific lesson
   */
  getLettersForLesson(lessonType: string): string[];

  /**
   * Get letter categories for a specific lesson
   */
  getLessonCategories(lessonType: string): LetterCategory[];
}
