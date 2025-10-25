import { injectable } from "inversify";
import type { QuizResults } from "../domain";

export interface IQuizFeedbackService {
  getPerformanceFeedback(results: QuizResults): string;
  getEncouragementMessage(accuracy: number): string;
}

@injectable()
export class QuizFeedbackService implements IQuizFeedbackService {
  getPerformanceFeedback(results: QuizResults): string {
    const accuracy = results.accuracyPercentage;
    const avgTime = results.averageTimePerQuestion || 0;

    if (accuracy >= 90) {
      if (avgTime < 3) {
        return "Outstanding! You're both accurate and fast.";
      } else {
        return "Excellent accuracy! You really understand this lesson.";
      }
    } else if (accuracy >= 70) {
      return "Good progress! Keep practicing to improve your speed and accuracy.";
    } else {
      return "Don't give up! Review the lesson materials and try again.";
    }
  }

  getEncouragementMessage(accuracy: number): string {
    if (accuracy >= 90) return "Keep up the amazing work!";
    if (accuracy >= 70) return "You're making great progress!";
    if (accuracy >= 50) return "Practice makes perfect!";
    return "Every attempt brings you closer to mastery!";
  }
}
