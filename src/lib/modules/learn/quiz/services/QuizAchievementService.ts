import { injectable } from "inversify";
import type { QuizResults } from "../domain";

export interface IQuizAchievementService {
  getAchievements(results: QuizResults): string[];
  hasAchievement(results: QuizResults, achievementName: string): boolean;
}

@injectable()
export class QuizAchievementService implements IQuizAchievementService {
  getAchievements(results: QuizResults): string[] {
    const achievements: string[] = [];

    // Perfect score achievement
    if (results.accuracyPercentage === 100) {
      achievements.push("🎯 Perfect Score");
    }

    // High achiever (90%+)
    if (results.accuracyPercentage >= 90) {
      achievements.push("⭐ High Achiever");
    }

    // Speed demon (avg < 3 seconds)
    if (results.averageTimePerQuestion && results.averageTimePerQuestion < 3) {
      achievements.push("⚡ Speed Demon");
    }

    // Hot streak (5+ correct in a row)
    if (results.streakLongestCorrect && results.streakLongestCorrect >= 5) {
      achievements.push("🔥 Hot Streak");
    }

    // Quick learner (completed in under 1 minute)
    if (results.completionTimeSeconds < 60) {
      achievements.push("🏃 Quick Learner");
    }

    // Perfectionist (no wrong answers)
    if (results.incorrectGuesses === 0 && results.correctAnswers > 0) {
      achievements.push("💎 Perfectionist");
    }

    // Marathon runner (10+ questions)
    if (results.totalQuestions >= 10) {
      achievements.push("🏅 Marathon Runner");
    }

    return achievements;
  }

  hasAchievement(results: QuizResults, achievementName: string): boolean {
    return this.getAchievements(results).includes(achievementName);
  }
}
