/**
 * Mock implementations for Codex services
 *
 * Used for testing to provide predictable data without external dependencies.
 */

import type {
  ILessonRepository,
  ILetterMappingRepository,
  LessonConfiguration,
  LetterCategory,
  LetterMapping,
  LetterRow,
} from "$domain";
import { MotionType } from "$domain";

/**
 * Mock Letter Mapping Repository for testing
 */
export class MockLetterMappingRepository implements ILetterMappingRepository {
  private mockLetters: Record<string, LetterMapping> = {
    A: {
      startPosition: "alpha1",
      endPosition: "alpha3",
      blueMotionType: MotionType.PRO,
      redMotionType: MotionType.PRO,
    },
    B: {
      startPosition: "alpha2",
      endPosition: "alpha4",
      blueMotionType: MotionType.PRO,
      redMotionType: MotionType.PRO,
    },
    C: {
      startPosition: "alpha3",
      endPosition: "alpha5",
      blueMotionType: MotionType.PRO,
      redMotionType: MotionType.PRO,
    },
    Σ: {
      startPosition: "alpha4",
      endPosition: "alpha6",
      blueMotionType: MotionType.ANTI,
      redMotionType: MotionType.ANTI,
    },
    Δ: {
      startPosition: "alpha5",
      endPosition: "alpha7",
      blueMotionType: MotionType.ANTI,
      redMotionType: MotionType.ANTI,
    },
    Φ: {
      startPosition: "alpha1",
      endPosition: "alpha1",
      blueMotionType: MotionType.DASH,
      redMotionType: MotionType.DASH,
    },
    α: {
      startPosition: "alpha1",
      endPosition: "alpha1",
      blueMotionType: MotionType.STATIC,
      redMotionType: MotionType.STATIC,
    },
    β: {
      startPosition: "alpha2",
      endPosition: "alpha2",
      blueMotionType: MotionType.STATIC,
      redMotionType: MotionType.STATIC,
    },
  };

  private mockRows: LetterRow[] = [
    {
      index: 0,
      letters: ["A", "B", "C"],
      category: "basic",
    },
    {
      index: 1,
      letters: ["Σ", "Δ"],
      category: "greek",
    },
    {
      index: 2,
      letters: ["Φ"],
      category: "dash",
    },
    {
      index: 3,
      letters: ["α", "β"],
      category: "static",
    },
  ];

  async initialize(): Promise<void> {
    // Mock initialization - no-op
  }

  getLetterMapping(letter: string): LetterMapping | null {
    return this.mockLetters[letter] || null;
  }

  getLettersByCategory(category: LetterCategory): string[] {
    const row = this.mockRows.find((r) => r.category === category);
    return row ? [...row.letters] : [];
  }

  getLetterRows(): LetterRow[] {
    return [...this.mockRows];
  }

  getAllLetters(): string[] {
    return Object.keys(this.mockLetters);
  }

  isValidLetter(letter: string): boolean {
    return letter in this.mockLetters;
  }
}

/**
 * Mock Lesson Repository for testing
 */
export class MockLessonRepository implements ILessonRepository {
  private mockLessons: Record<string, LessonConfiguration> = {
    basic_pro_anti: {
      name: "Basic Pro/Anti",
      description: "Basic pro and anti movements",
      type: "practice",
      includedCategories: ["basic"],
      includedLetters: [],
      excludedLetters: [],
    },
    all_letters: {
      name: "All Letters",
      description: "All available letters",
      type: "practice",
      includedCategories: ["basic"],
      includedLetters: [],
      excludedLetters: [],
    },
    beginner: {
      name: "Beginner",
      description: "Beginner friendly letters",
      type: "practice",
      includedCategories: ["basic"],
      includedLetters: ["A", "B", "C", "G", "H", "I", "M", "N", "O"],
      excludedLetters: [],
    },
  };

  constructor(private letterMappingRepo: ILetterMappingRepository) {}

  async initialize(): Promise<void> {
    // Mock initialization - no-op
  }

  getLessonConfiguration(lessonType: string): LessonConfiguration | null {
    return this.mockLessons[lessonType] || null;
  }

  getAllLessonTypes(): string[] {
    return Object.keys(this.mockLessons);
  }

  getLettersForLesson(lessonType: string): string[] {
    const lesson = this.mockLessons[lessonType];
    if (!lesson) return [];

    // If specific letters are included, return those
    if (lesson.includedLetters && lesson.includedLetters.length > 0) {
      return [...lesson.includedLetters];
    }

    // Otherwise, get letters by categories
    let letters: string[] = [];
    for (const category of lesson.includedCategories) {
      letters.push(...this.letterMappingRepo.getLettersByCategory(category));
    }

    // Remove excluded letters
    if (lesson.excludedLetters && lesson.excludedLetters.length > 0) {
      letters = letters.filter(
        (letter) => !(lesson.excludedLetters ?? []).includes(letter)
      );
    }

    return letters;
  }

  getLessonCategories(lessonType: string): LetterCategory[] {
    const lesson = this.mockLessons[lessonType];
    return lesson ? [...lesson.includedCategories] : [];
  }
}
