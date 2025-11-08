/**
 * Gamification Domain Models
 *
 * These models define the structure for achievements, XP, and daily challenges.
 */

// ============================================================================
// ACHIEVEMENT MODELS
// ============================================================================

export type AchievementCategory =
  | "creator" // Building sequences
  | "scholar" // Learning concepts
  | "practitioner" // Daily streaks & practice
  | "explorer" // Browsing gallery
  | "performer"; // Video submissions (Phase 3)

export type AchievementTier = "bronze" | "silver" | "gold" | "platinum";

export interface Achievement {
  id: string;
  title: string;
  description: string;
  category: AchievementCategory;
  tier: AchievementTier;
  xpReward: number;
  icon: string; // Emoji or icon identifier
  requirement: AchievementRequirement;
}

export interface AchievementRequirement {
  type:
    | "sequence_count" // Create X sequences
    | "concept_completion" // Complete X concepts
    | "daily_streak" // Login/practice X days in a row
    | "gallery_exploration" // Explore X sequences
    | "letter_usage" // Create sequence with specific letters
    | "sequence_length" // Create sequence of X beats
    | "generation_count" // Generate X sequences
    | "specific_action"; // Complete specific action once
  target: number; // How many to complete (1 for one-time achievements)
  metadata?: Record<string, any>; // Additional data (e.g., required letters, specific concept ID)
}

export interface UserAchievement {
  id: string; // Auto-generated
  achievementId: string; // Reference to Achievement
  userId?: string; // Optional: For future multi-user support
  unlockedAt: Date;
  progress: number; // Current progress toward completion
  isCompleted: boolean;
  notificationShown: boolean; // Track if user has seen the unlock notification
}

// ============================================================================
// XP & LEVEL MODELS
// ============================================================================

export interface UserXP {
  id: string; // "xp_progress" (single record per user)
  userId?: string; // Optional: For future multi-user support
  totalXP: number;
  currentLevel: number;
  xpToNextLevel: number;
  lastUpdated: Date;
}

export interface XPGainEvent {
  id: string;
  action: XPActionType;
  xpGained: number;
  timestamp: Date;
  metadata?: Record<string, any>;
}

export type XPActionType =
  | "sequence_created"
  | "sequence_generated"
  | "concept_learned"
  | "drill_completed"
  | "sequence_explored"
  | "daily_challenge_completed"
  | "achievement_unlocked"
  | "daily_login";

// ============================================================================
// DAILY CHALLENGE MODELS
// ============================================================================

export type ChallengeType =
  | "build_sequence" // Build specific sequence
  | "use_letters" // Use specific letters
  | "sequence_length" // Create X-beat sequence
  | "complete_concept" // Complete specific concept
  | "explore_gallery" // Explore X sequences
  | "generation_challenge"; // Generate sequences with criteria

export type ChallengeDifficulty = "beginner" | "intermediate" | "advanced";

export interface DailyChallenge {
  id: string; // Date-based: e.g., "challenge_2025-11-01"
  date: string; // ISO date string (YYYY-MM-DD)
  type: ChallengeType;
  difficulty: ChallengeDifficulty;
  title: string;
  description: string;
  xpReward: number;
  requirement: ChallengeRequirement;
  expiresAt: Date; // End of day
}

export interface ChallengeRequirement {
  type: ChallengeType;
  target: number;
  metadata?: Record<string, any>; // Challenge-specific data
}

export interface UserChallengeProgress {
  id: string; // Auto-generated
  challengeId: string;
  userId?: string;
  progress: number;
  isCompleted: boolean;
  completedAt?: Date;
  startedAt: Date;
}

// ============================================================================
// STREAK MODELS
// ============================================================================

export interface UserStreak {
  id: string; // "streak_data" (single record per user)
  userId?: string;
  currentStreak: number; // Days in a row
  longestStreak: number;
  lastActivityDate: string; // ISO date string (YYYY-MM-DD)
  streakStartDate: string; // ISO date string
}

// ============================================================================
// NOTIFICATION MODELS
// ============================================================================

export interface AchievementNotification {
  id: string;
  type: "achievement" | "level_up" | "challenge_complete" | "streak_milestone";
  title: string;
  message: string;
  icon?: string;
  timestamp: Date;
  isRead: boolean;
  data?: Record<string, any>; // Additional notification data
}
