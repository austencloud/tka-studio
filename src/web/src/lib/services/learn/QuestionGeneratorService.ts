/**
 * Question Generator Service
 *
 * Generates quiz questions for different lesson types based on pictograph data.
 * Matches the desktop implementation's question generation logic.
 */

import {
  AnswerFormat,
  type AnswerOption,
  LessonType,
  type QuestionData,
  QuestionFormat,
} from "$lib/types/learn";

// Mock pictograph data structure (this would come from the actual pictograph service)
interface PictographData {
  letter: string;
  start_pos: string;
  end_pos: string;
  grid_mode: string;
  // ... other pictograph properties
}

export class QuestionGeneratorService {
  private static previousCorrectLetter: string | null = null;
  private static previousPictographs: Set<string> = new Set();

  /**
   * Generate a question for a specific lesson type.
   */
  static generateQuestion(
    lessonType: LessonType,
    pictographDataset?: Record<string, PictographData[]>,
  ): QuestionData {
    const questionId = this.generateQuestionId();

    switch (lessonType) {
      case LessonType.PICTOGRAPH_TO_LETTER:
        return this.generatePictographToLetterQuestion(
          questionId,
          pictographDataset,
        );
      case LessonType.LETTER_TO_PICTOGRAPH:
        return this.generateLetterToPictographQuestion(
          questionId,
          pictographDataset,
        );
      case LessonType.VALID_NEXT_PICTOGRAPH:
        return this.generateValidNextPictographQuestion(
          questionId,
          pictographDataset,
        );
      default:
        throw new Error(`Unsupported lesson type: ${lessonType}`);
    }
  }

  /**
   * Generate a pictograph-to-letter question.
   */
  private static generatePictographToLetterQuestion(
    questionId: string,
    _pictographDataset?: Record<string, PictographData[]>,
  ): QuestionData {
    // For now, use mock data - this would be replaced with actual pictograph service
    const availableLetters = ["A", "B", "C", "D", "E", "F", "G", "H"];
    const correctLetter = this.getRandomLetter(availableLetters);

    // Mock pictograph data for the correct letter
    const correctPictograph = {
      letter: correctLetter,
      start_pos: "s",
      end_pos: "n",
      grid_mode: "diamond",
    };

    // Generate wrong letter options
    const wrongLetters = this.generateWrongLetters(
      correctLetter,
      availableLetters,
      3,
    );
    const allOptions = [correctLetter, ...wrongLetters];
    this.shuffleArray(allOptions);

    // Create answer options
    const answerOptions: AnswerOption[] = allOptions.map((letter) => ({
      id: this.generateOptionId(),
      content: letter,
      isCorrect: letter === correctLetter,
    }));

    return {
      questionId,
      questionContent: correctPictograph,
      answerOptions,
      correctAnswer: correctLetter,
      questionType: QuestionFormat.PICTOGRAPH,
      answerType: AnswerFormat.BUTTON,
      lessonType: LessonType.PICTOGRAPH_TO_LETTER,
      generationTimestamp: new Date().toISOString(),
    };
  }

  /**
   * Generate a letter-to-pictograph question.
   */
  private static generateLetterToPictographQuestion(
    questionId: string,
    _pictographDataset?: Record<string, PictographData[]>,
  ): QuestionData {
    const availableLetters = ["A", "B", "C", "D", "E", "F", "G", "H"];
    const correctLetter = this.getRandomLetter(availableLetters);

    // Mock correct pictograph
    const correctPictograph = {
      letter: correctLetter,
      start_pos: "s",
      end_pos: "n",
      grid_mode: "diamond",
    };

    // Generate wrong pictographs
    const wrongPictographs = this.generateWrongPictographs(
      correctLetter,
      availableLetters,
      3,
    );
    const allPictographs = [correctPictograph, ...wrongPictographs];
    this.shuffleArray(allPictographs);

    // Create answer options
    const answerOptions: AnswerOption[] = allPictographs.map((pictograph) => ({
      id: this.generateOptionId(),
      content: pictograph,
      isCorrect: pictograph.letter === correctLetter,
    }));

    return {
      questionId,
      questionContent: correctLetter,
      answerOptions,
      correctAnswer: correctPictograph,
      questionType: QuestionFormat.LETTER,
      answerType: AnswerFormat.PICTOGRAPH,
      lessonType: LessonType.LETTER_TO_PICTOGRAPH,
      generationTimestamp: new Date().toISOString(),
    };
  }

  /**
   * Generate a valid-next-pictograph question.
   */
  private static generateValidNextPictographQuestion(
    questionId: string,
    _pictographDataset?: Record<string, PictographData[]>,
  ): QuestionData {
    // Mock initial pictograph
    const initialPictograph = {
      letter: "A",
      start_pos: "s",
      end_pos: "e",
      grid_mode: "diamond",
    };

    // Mock correct next pictograph (start_pos matches end_pos of initial)
    const correctNextPictograph = {
      letter: "B",
      start_pos: "e",
      end_pos: "n",
      grid_mode: "diamond",
    };

    // Generate wrong next pictographs
    const wrongNextPictographs = [
      { letter: "C", start_pos: "n", end_pos: "w", grid_mode: "diamond" },
      { letter: "D", start_pos: "w", end_pos: "s", grid_mode: "diamond" },
      { letter: "E", start_pos: "s", end_pos: "n", grid_mode: "diamond" },
    ];

    const allOptions = [correctNextPictograph, ...wrongNextPictographs];
    this.shuffleArray(allOptions);

    // Create answer options
    const answerOptions: AnswerOption[] = allOptions.map((pictograph) => ({
      id: this.generateOptionId(),
      content: pictograph,
      isCorrect: pictograph.start_pos === initialPictograph.end_pos,
    }));

    return {
      questionId,
      questionContent: initialPictograph,
      answerOptions,
      correctAnswer: correctNextPictograph,
      questionType: QuestionFormat.PICTOGRAPH,
      answerType: AnswerFormat.PICTOGRAPH,
      lessonType: LessonType.VALID_NEXT_PICTOGRAPH,
      generationTimestamp: new Date().toISOString(),
    };
  }

  /**
   * Generate wrong letter options.
   */
  private static generateWrongLetters(
    correctLetter: string,
    availableLetters: string[],
    count: number,
  ): string[] {
    const wrongLetters = availableLetters.filter(
      (letter) => letter !== correctLetter,
    );
    return this.getRandomItems(wrongLetters, count);
  }

  /**
   * Generate wrong pictograph options.
   */
  private static generateWrongPictographs(
    correctLetter: string,
    availableLetters: string[],
    count: number,
  ): PictographData[] {
    const wrongLetters = this.generateWrongLetters(
      correctLetter,
      availableLetters,
      count,
    );
    return wrongLetters.map((letter) => ({
      letter,
      start_pos: this.getRandomPosition(),
      end_pos: this.getRandomPosition(),
      grid_mode: "diamond",
    }));
  }

  /**
   * Get a random letter, avoiding the previous one.
   */
  private static getRandomLetter(availableLetters: string[]): string {
    let filteredLetters = availableLetters;
    if (this.previousCorrectLetter) {
      filteredLetters = availableLetters.filter(
        (letter) => letter !== this.previousCorrectLetter,
      );
    }
    const letter = this.getRandomItem(filteredLetters);
    this.previousCorrectLetter = letter;
    return letter;
  }

  /**
   * Get a random position.
   */
  private static getRandomPosition(): string {
    const positions = ["n", "e", "s", "w", "ne", "se", "sw", "nw"];
    return this.getRandomItem(positions);
  }

  /**
   * Utility: Get random item from array.
   */
  private static getRandomItem<T>(array: T[]): T {
    if (array.length === 0)
      throw new Error("getRandomItem called with empty array");
    return array[Math.floor(Math.random() * array.length)] as T;
  }

  /**
   * Utility: Get multiple random items from array.
   */
  private static getRandomItems<T>(array: T[], count: number): T[] {
    const shuffled = [...array].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
  }

  /**
   * Utility: Shuffle array in place.
   */
  private static shuffleArray<T>(array: T[]): void {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const tmp = array[i];
      const jValue = array[j];
      if (tmp !== undefined && jValue !== undefined) {
        array[i] = jValue;
        array[j] = tmp;
      }
    }
  }

  /**
   * Generate unique question ID.
   */
  private static generateQuestionId(): string {
    return `question_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;
  }

  /**
   * Generate unique option ID.
   */
  private static generateOptionId(): string {
    return `option_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;
  }

  /**
   * Reset generator state (for new quiz sessions).
   */
  static resetState(): void {
    this.previousCorrectLetter = null;
    this.previousPictographs.clear();
  }
}
