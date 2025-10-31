import { injectable } from "inversify";
import type { QuizResults } from "../domain";

export type LessonType =
  | "pictograph_to_letter"
  | "letter_to_pictograph"
  | "valid_next_pictograph";
export type QuizMode = "fixed_question" | "countdown";

export interface IQuizFormatterService {
  formatTime(seconds: number): string;
  getLessonDisplayName(lessonType: LessonType | undefined): string;
  getQuizModeDisplayName(quizMode: QuizMode | undefined): string;
  formatAccuracy(accuracy: number): string;
  formatDate(date: Date): string;
}

@injectable()
export class QuizFormatterService implements IQuizFormatterService {
  formatTime(seconds: number): string {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
  }

  getLessonDisplayName(lessonType: LessonType | undefined): string {
    if (!lessonType) return "Unknown Lesson";

    switch (lessonType) {
      case "pictograph_to_letter":
        return "Lesson 1: Pictograph to Letter";
      case "letter_to_pictograph":
        return "Lesson 2: Letter to Pictograph";
      case "valid_next_pictograph":
        return "Lesson 3: Valid Next Pictograph";
      default:
        return "Unknown Lesson";
    }
  }

  getQuizModeDisplayName(quizMode: QuizMode | undefined): string {
    if (!quizMode) return "Unknown Mode";

    switch (quizMode) {
      case "fixed_question":
        return "Fixed Questions";
      case "countdown":
        return "Countdown";
      default:
        return "Unknown Mode";
    }
  }

  formatAccuracy(accuracy: number): string {
    return `${accuracy.toFixed(1)}%`;
  }

  formatDate(date: Date): string {
    return date.toLocaleDateString();
  }
}
