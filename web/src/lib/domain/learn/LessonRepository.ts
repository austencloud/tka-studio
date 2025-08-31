/**
 * Lesson Configuration Repository
 *
 * Manages lesson configurations and determines which letters are included
 * in different lesson types.
 */

import type {
  LessonConfiguration,
  LetterCategory,
} from "$domain/learn/codex/types";
import { inject, injectable } from "inversify";
import { TYPES } from "../../services/inversify/types";
import type { ILetterMappingRepository } from "./codex/LetterMappingRepository";

export interface ILessonRepository {
  initialize(): Promise<void>;
  getLessonConfiguration(lessonType: string): LessonConfiguration | null;
  getAllLessonTypes(): string[];
  getLettersForLesson(lessonType: string): string[];
  getLessonCategories(lessonType: string): LetterCategory[];
}

interface LessonConfigurationFile {
  lessons: LessonConfiguration[];
}

@injectable()
export class LessonRepository implements ILessonRepository {
  private configurations: Map<string, LessonConfiguration> = new Map();
  private initialized = false;

  constructor(
    @inject(TYPES.ILetterMappingRepository)
    private letterMappingRepository: ILetterMappingRepository
  ) {}

  async initialize(): Promise<void> {
    if (this.initialized) return;

    try {
      // Ensure letter mapping repository is initialized
      await this.letterMappingRepository.initialize();

      // Load lesson configurations
      const response = await fetch("/config/codex/lesson-configurations.json");
      if (!response.ok) {
        throw new Error(
          `Failed to load lesson configurations: ${response.status}`
        );
      }

      const data: LessonConfigurationFile = await response.json();

      // Index configurations by type
      data.lessons.forEach((config) => {
        this.configurations.set(config.type, config);
      });

      this.initialized = true;
      console.log(
        "✅ Lesson repository initialized with",
        this.configurations.size,
        "lesson types"
      );
    } catch (error) {
      console.error("❌ Failed to initialize lesson repository:", error);
      throw error;
    }
  }

  getLessonConfiguration(lessonType: string): LessonConfiguration | null {
    this.ensureInitialized();
    return this.configurations.get(lessonType) || null;
  }

  getAllLessonTypes(): string[] {
    this.ensureInitialized();
    return Array.from(this.configurations.keys());
  }

  getLettersForLesson(lessonType: string): string[] {
    this.ensureInitialized();

    const config = this.configurations.get(lessonType);
    if (!config) {
      console.warn(`Unknown lesson type: ${lessonType}`);
      return [];
    }

    let letters: string[] = [];

    // Include letters from categories
    if (config.includedCategories) {
      for (const category of config.includedCategories) {
        const categoryLetters =
          this.letterMappingRepository.getLettersByCategory(category);
        letters.push(...categoryLetters);
      }
    }

    // Include specific letters
    if (config.includedLetters) {
      letters.push(...config.includedLetters);
    }

    // Remove duplicates
    letters = [...new Set(letters)];

    // Exclude specific letters
    if (config.excludedLetters) {
      letters = letters.filter(
        (letter) => !config.excludedLetters?.includes(letter)
      );
    }

    // Validate that all letters exist in mapping
    return letters.filter((letter) =>
      this.letterMappingRepository.isValidLetter(letter)
    );
  }

  getLessonCategories(lessonType: string): LetterCategory[] {
    this.ensureInitialized();

    const config = this.configurations.get(lessonType);
    return config?.includedCategories || [];
  }

  private ensureInitialized(): void {
    if (!this.initialized) {
      throw new Error(
        "Lesson repository not initialized. Call initialize() first."
      );
    }
  }
}
