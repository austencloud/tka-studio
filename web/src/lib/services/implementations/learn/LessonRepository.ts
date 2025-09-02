/**
 * Lesson Repository Implementation
 *
 * Service implementation for lesson configuration management and retrieval.
 * Handles lesson types, configurations, and category management.
 */

import type { ILessonRepository, ILetterMappingRepository } from "$contracts";
import type { LessonConfiguration, LetterCategory } from "$domain";
import { inject, injectable } from "inversify";
import { TYPES } from "../../inversify/types";

@injectable()
export class LessonRepository implements ILessonRepository {
  private configurations: Map<string, LessonConfiguration> = new Map();
  private initialized = false;

  constructor(
    @inject(TYPES.ILetterMappingRepository)
    private letterMappingRepository: ILetterMappingRepository
  ) {}

  async initialize(): Promise<void> {
    if (this.initialized) {
      return;
    }

    try {
      // Initialize letter mapping repository first
      await this.letterMappingRepository.initialize();

      // Load lesson configurations
      await this.loadLessonConfigurations();

      this.initialized = true;
    } catch (error) {
      console.error("Failed to initialize LessonRepository:", error);
      throw error;
    }
  }

  getLessonConfiguration(lessonType: string): LessonConfiguration | null {
    if (!this.initialized) {
      console.warn(
        "LessonRepository not initialized. Call initialize() first."
      );
      return null;
    }

    return this.configurations.get(lessonType) || null;
  }

  getAllLessonTypes(): string[] {
    if (!this.initialized) {
      console.warn(
        "LessonRepository not initialized. Call initialize() first."
      );
      return [];
    }

    return Array.from(this.configurations.keys());
  }

  getLettersForLesson(lessonType: string): string[] {
    const config = this.getLessonConfiguration(lessonType);
    if (!config) {
      return [];
    }

    // Extract letters from lesson configuration
    return config.includedLetters || [];
  }

  getLessonCategories(lessonType: string): LetterCategory[] {
    const config = this.getLessonConfiguration(lessonType);
    if (!config) {
      return [];
    }

    // Extract categories from lesson configuration
    return config.categories || [];
  }

  private async loadLessonConfigurations(): Promise<void> {
    try {
      // TODO: Load from actual lesson configuration files
      // For now, create some default configurations
      const defaultLessons: LessonConfiguration[] = [
        {
          id: "basic-letters",
          type: "basic-letters",
          name: "Basic Letters",
          description: "Learn the basic letter formations",
          includedCategories: ["basic" as LetterCategory],
          letters: ["A", "B", "C", "D", "E"],
          categories: ["basic" as LetterCategory],
          difficulty: 1,
        },
        {
          id: "advanced-letters",
          type: "advanced-letters",
          name: "Advanced Letters",
          description: "Master advanced letter combinations",
          includedCategories: ["extended" as LetterCategory],
          letters: ["F", "G", "H", "I", "J"],
          categories: ["extended" as LetterCategory],
          difficulty: 2,
        },
      ];

      // Store configurations
      for (const lesson of defaultLessons) {
        if (lesson.id) {
          this.configurations.set(lesson.id, lesson);
        }
      }
    } catch (error) {
      console.error("Failed to load lesson configurations:", error);
      throw error;
    }
  }
}
