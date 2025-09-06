/**
 * Lesson Repo Implementation
 *
 * Service implementation for lesson configuration management and retrieval.
 * Handles lesson types, configurations, and category management.
 */

import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { LetterCategory } from "../../../codex";
import {
  QuizAnswerFormat,
  QuizQuestionFormat,
  QuizType,
  type QuizConfig,
} from "../../domain";
import type { IQuizRepoManager } from "../contracts";
// import type { ICodexLetterMappingRepo } from "../../../codex/services/contracts/ICodexLetterMappingRepo";

// Temporary interface definition
interface ICodexLetterMappingRepo {
  getMapping(letter: string): Promise<any>;
  getAllMappings(): Promise<any[]>;
  initialize(): Promise<void>;
}

@injectable()
export class QuizRepoManager implements IQuizRepoManager {
  private configurations: Map<string, QuizConfig> = new Map();
  private initialized = false;

  constructor(
    @inject(TYPES.ICodexLetterMappingRepo)
    private letterMappingRepo: ICodexLetterMappingRepo
  ) {}

  async initialize(): Promise<void> {
    if (this.initialized) {
      return;
    }

    try {
      // Initialize letter mapping repository first
      await this.letterMappingRepo.initialize();

      // Load lesson configurations
      await this.loadQuizConfigs();

      this.initialized = true;
    } catch (error) {
      console.error("Failed to initialize QuizRepoManager:", error);
      throw error;
    }
  }

  getQuizConfig(lessonType: string): QuizConfig | null {
    if (!this.initialized) {
      console.warn("QuizRepoManager not initialized. Call initialize() first.");
      return null;
    }

    return this.configurations.get(lessonType) || null;
  }

  getAllQuizTypes(): string[] {
    if (!this.initialized) {
      console.warn("QuizRepoManager not initialized. Call initialize() first.");
      return [];
    }

    return Array.from(this.configurations.keys());
  }

  getLettersForLesson(lessonType: string): string[] {
    const config = this.getQuizConfig(lessonType);
    if (!config) {
      return [];
    }

    // Extract letters from lesson configuration
    return config.includedLetters || [];
  }

  getLessonCategories(lessonType: string): LetterCategory[] {
    const config = this.getQuizConfig(lessonType);
    if (!config) {
      return [];
    }

    // Extract categories from lesson configuration
    return config.categories || [];
  }

  private async loadQuizConfigs(): Promise<void> {
    try {
      // TODO: Load from actual lesson configuration files
      // For now, create some default configurations
      const defaultLessons: QuizConfig[] = [
        {
          id: "basic-letters",
          type: "basic-letters",
          name: "Basic Letters",
          description: "Learn the basic letter formations",
          includedCategories: ["basic" as LetterCategory],
          letters: ["A", "B", "C", "D", "E"],
          categories: ["basic" as LetterCategory],
          difficulty: 1,
          lessonType: QuizType.PICTOGRAPH_TO_LETTER,
          questionFormat: QuizQuestionFormat.PICTOGRAPH,
          answerFormat: QuizAnswerFormat.BUTTON,
          quizDescription: "",
          questionPrompt: "",
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
          lessonType: QuizType.PICTOGRAPH_TO_LETTER,
          questionFormat: QuizQuestionFormat.PICTOGRAPH,
          answerFormat: QuizAnswerFormat.BUTTON,
          quizDescription: "",
          questionPrompt: "",
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
