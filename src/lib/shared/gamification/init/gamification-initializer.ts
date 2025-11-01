/**
 * Gamification Initialization Helper
 *
 * Call this once on app startup to initialize all gamification services.
 */

import { resolve, TYPES } from "../../inversify";
import type {
  IAchievementService,
  IDailyChallengeService,
  IStreakService,
} from "../services/contracts";

export async function initializeGamification(): Promise<void> {
  try {
    console.log("🎮 Initializing gamification system...");

    // Resolve services
    const [achievementService, challengeService, streakService] =
      await Promise.all([
        resolve<IAchievementService>(TYPES.IAchievementService),
        resolve<IDailyChallengeService>(TYPES.IDailyChallengeService),
        resolve<IStreakService>(TYPES.IStreakService),
      ]);

    // Initialize in parallel
    await Promise.all([
      achievementService.initialize(),
      challengeService.initialize(),
      streakService.initialize(),
    ]);

    // Only record daily activity if user is logged in
    const { auth } = await import("../../auth/firebase");
    const user = auth.currentUser;

    if (user) {
      console.log("👤 User logged in, tracking daily activity...");

      // Record daily activity (for streak tracking)
      const streakResult = await streakService.recordDailyActivity();

      if (streakResult.streakIncremented) {
        console.log(`🔥 Streak: ${streakResult.currentStreak} days!`);

        // Award daily login XP
        await achievementService.trackAction("daily_login");

        // Check for streak milestone achievements
        if (
          streakResult.currentStreak === 3 ||
          streakResult.currentStreak === 7 ||
          streakResult.currentStreak === 30 ||
          streakResult.currentStreak === 100
        ) {
          await achievementService.trackAction("daily_login", {
            currentStreak: streakResult.currentStreak,
          });
        }
      }
    } else {
      console.log("👤 No user logged in, skipping streak tracking");
    }

    console.log("✅ Gamification system initialized successfully");
  } catch (error) {
    console.error("❌ Failed to initialize gamification:", error);
    // Don't throw - allow app to continue even if gamification fails
  }
}

/**
 * Track XP helper function
 * Use this throughout your app to track user actions
 */
export async function trackXP(
  action:
    | "sequence_created"
    | "sequence_generated"
    | "concept_learned"
    | "drill_completed"
    | "sequence_explored"
    | "daily_login"
    | "daily_challenge_completed",
  metadata?: Record<string, any>
): Promise<void> {
  try {
    const achievementService = await resolve<IAchievementService>(
      TYPES.IAchievementService
    );
    const result = await achievementService.trackAction(action, metadata);

    console.log(
      `✨ +${result.xpGained} XP (${result.achievementsUnlocked.length} achievements unlocked)`
    );

    if (result.newLevel) {
      console.log(`📈 Level Up! You're now level ${result.newLevel}`);
    }
  } catch (error) {
    console.error("Failed to track XP:", error);
    // Don't throw - silently fail
  }
}
