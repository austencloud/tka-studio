/**
 * Mock Configuration Repository for Testing
 *
 * Provides in-memory implementations of repositories for testing
 * without requiring actual JSON file fetching.
 */

import type { ILetterMappingRepository } from "$lib/repositories/LetterMappingRepository";
import type { ILessonRepository } from "$lib/repositories/LessonRepository";
import type {
  CodexConfiguration,
  LetterMapping,
  LetterCategory,
  LetterRow,
  LessonConfiguration,
} from "$lib/domain/codex/types";

// Mock data that matches our JSON files
const MOCK_LETTER_MAPPINGS: CodexConfiguration = {
  letters: {
    A: {
      startPosition: "alpha1",
      endPosition: "alpha3",
      blueMotionType: "pro",
      redMotionType: "pro",
    },
    B: {
      startPosition: "alpha1",
      endPosition: "alpha3",
      blueMotionType: "anti",
      redMotionType: "anti",
    },
    C: {
      startPosition: "alpha1",
      endPosition: "alpha3",
      blueMotionType: "anti",
      redMotionType: "pro",
    },
    G: {
      startPosition: "beta3",
      endPosition: "beta5",
      blueMotionType: "pro",
      redMotionType: "pro",
    },
    H: {
      startPosition: "beta3",
      endPosition: "beta5",
      blueMotionType: "anti",
      redMotionType: "anti",
    },
    I: {
      startPosition: "beta3",
      endPosition: "beta5",
      blueMotionType: "anti",
      redMotionType: "pro",
    },
    M: {
      startPosition: "gamma11",
      endPosition: "gamma1",
      blueMotionType: "pro",
      redMotionType: "pro",
    },
    N: {
      startPosition: "gamma11",
      endPosition: "gamma1",
      blueMotionType: "anti",
      redMotionType: "anti",
    },
    O: {
      startPosition: "gamma11",
      endPosition: "gamma1",
      blueMotionType: "anti",
      redMotionType: "pro",
    },
    Σ: {
      startPosition: "alpha3",
      endPosition: "gamma13",
      blueMotionType: "static",
      redMotionType: "pro",
    },
    Δ: {
      startPosition: "alpha3",
      endPosition: "gamma13",
      blueMotionType: "static",
      redMotionType: "anti",
    },
    Φ: {
      startPosition: "beta7",
      endPosition: "alpha3",
      blueMotionType: "static",
      redMotionType: "dash",
    },
    α: {
      startPosition: "alpha3",
      endPosition: "alpha3",
      blueMotionType: "static",
      redMotionType: "static",
    },
    β: {
      startPosition: "beta5",
      endPosition: "beta5",
      blueMotionType: "static",
      redMotionType: "static",
    },
  },
  rows: [
    { index: 0, category: "basic", letters: ["A", "B", "C"] },
    { index: 1, category: "basic", letters: ["G", "H", "I"] },
    { index: 2, category: "basic", letters: ["M", "N", "O"] },
    { index: 3, category: "greek", letters: ["Σ", "Δ"] },
    { index: 4, category: "special", letters: ["Φ"] },
    { index: 5, category: "static", letters: ["α", "β"] },
  ],
  categories: {
    basic: ["A", "B", "C", "G", "H", "I", "M", "N", "O"],
    extended: [],
    greek: ["Σ", "Δ"],
    dash: [],
    special: ["Φ"],
    dual_dash: [],
    static: ["α", "β"],
  },
};

const MOCK_LESSON_CONFIGURATIONS: LessonConfiguration[] = [
  {
    type: "basic_pro_anti",
    name: "Basic Pro & Anti",
    description: "Learn the fundamental pro and anti motions",
    includedCategories: ["basic"],
  },
  {
    type: "beginner",
    name: "Beginner Set",
    description: "Easy letters for beginners",
    includedCategories: [],
    includedLetters: ["A", "B", "C", "G", "H", "I", "M", "N", "O"],
  },
  {
    type: "all_letters",
    name: "Complete Codex",
    description: "Practice with all available letters",
    includedCategories: ["basic", "greek", "special", "static"],
  },
];

export class MockLetterMappingRepository implements ILetterMappingRepository {
  private initialized = false;

  async initialize(): Promise<void> {
    this.initialized = true;
    console.log("✅ Mock letter mapping repository initialized");
  }

  getLetterMapping(letter: string): LetterMapping | null {
    this.ensureInitialized();
    return MOCK_LETTER_MAPPINGS.letters[letter] || null;
  }

  getLettersByCategory(category: LetterCategory): string[] {
    this.ensureInitialized();
    return [...(MOCK_LETTER_MAPPINGS.categories[category] || [])];
  }

  getLetterRows(): LetterRow[] {
    this.ensureInitialized();
    return [...MOCK_LETTER_MAPPINGS.rows];
  }

  getAllLetters(): string[] {
    this.ensureInitialized();
    return Object.keys(MOCK_LETTER_MAPPINGS.letters);
  }

  isValidLetter(letter: string): boolean {
    this.ensureInitialized();
    return letter in MOCK_LETTER_MAPPINGS.letters;
  }

  private ensureInitialized(): void {
    if (!this.initialized) {
      throw new Error(
        "Mock letter mapping repository not initialized. Call initialize() first."
      );
    }
  }
}

export class MockLessonRepository implements ILessonRepository {
  private configurations: Map<string, LessonConfiguration> = new Map();
  private initialized = false;

  constructor(private letterMappingRepository: ILetterMappingRepository) {}

  async initialize(): Promise<void> {
    if (this.initialized) return;

    await this.letterMappingRepository.initialize();

    MOCK_LESSON_CONFIGURATIONS.forEach((config) => {
      this.configurations.set(config.type, config);
    });

    this.initialized = true;
    console.log("✅ Mock lesson repository initialized");
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
        "Mock lesson repository not initialized. Call initialize() first."
      );
    }
  }
}
