/**
 * Firestore Collection Names and Paths
 *
 * Centralized constants for Firestore collections used in gamification.
 */

export const FIRESTORE_COLLECTIONS = {
  // User-specific collections
  USER_ACHIEVEMENTS: "userAchievements",
  USER_XP: "userXP",
  XP_EVENTS: "xpEvents",
  USER_CHALLENGE_PROGRESS: "userChallengeProgress",
  USER_STREAKS: "userStreaks",
  USER_NOTIFICATIONS: "userNotifications",

  // Global collections
  DAILY_CHALLENGES: "dailyChallenges",
} as const;

/**
 * Get path to user's achievements collection
 */
export function getUserAchievementsPath(userId: string): string {
  return `users/${userId}/achievements`;
}

/**
 * Get path to user's XP document
 */
export function getUserXPPath(userId: string): string {
  return `users/${userId}/xp/current`;
}

/**
 * Get path to user's XP events collection
 */
export function getUserXPEventsPath(userId: string): string {
  return `users/${userId}/xpEvents`;
}

/**
 * Get path to user's challenge progress collection
 */
export function getUserChallengeProgressPath(userId: string): string {
  return `users/${userId}/challengeProgress`;
}

/**
 * Get path to user's streak document
 */
export function getUserStreakPath(userId: string): string {
  return `users/${userId}/streak/current`;
}

/**
 * Get path to user's notifications collection
 */
export function getUserNotificationsPath(userId: string): string {
  return `users/${userId}/notifications`;
}

/**
 * Get path to daily challenges collection
 */
export function getDailyChallengesPath(): string {
  return "dailyChallenges";
}
