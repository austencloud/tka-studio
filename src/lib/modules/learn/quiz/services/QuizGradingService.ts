import { injectable } from "inversify";

export interface PerformanceGrade {
  grade: string;
  color: string;
  message: string;
}

export interface IQuizGradingService {
  getPerformanceGrade(accuracy: number): PerformanceGrade;
  isPassingGrade(accuracy: number): boolean;
  isExcellentGrade(accuracy: number): boolean;
  isPerfectScore(accuracy: number): boolean;
}

@injectable()
export class QuizGradingService implements IQuizGradingService {
  getPerformanceGrade(accuracy: number): PerformanceGrade {
    if (accuracy >= 90) {
      return { grade: "A", color: "#10b981", message: "Excellent!" };
    }
    if (accuracy >= 80) {
      return { grade: "B", color: "#3b82f6", message: "Great job!" };
    }
    if (accuracy >= 70) {
      return { grade: "C", color: "#f59e0b", message: "Good work!" };
    }
    if (accuracy >= 60) {
      return { grade: "D", color: "#ef4444", message: "Keep practicing!" };
    }
    return { grade: "F", color: "#dc2626", message: "Try again!" };
  }

  isPassingGrade(accuracy: number): boolean {
    return accuracy >= 70;
  }

  isExcellentGrade(accuracy: number): boolean {
    return accuracy >= 90;
  }

  isPerfectScore(accuracy: number): boolean {
    return accuracy === 100;
  }
}
