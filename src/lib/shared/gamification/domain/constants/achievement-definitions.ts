/**
 * Achievement Definitions
 *
 * All available achievements in TKA Studio.
 * These are the "templates" that users can unlock.
 */

import type { Achievement } from "../models";

// ============================================================================
// CREATOR ACHIEVEMENTS (Building Sequences)
// ============================================================================

const CREATOR_ACHIEVEMENTS: Achievement[] = [
  {
    id: "first_sequence",
    title: "First Steps",
    description: "Create your first sequence",
    category: "creator",
    tier: "bronze",
    xpReward: 50,
    icon: "fa-sparkles",
    requirement: {
      type: "sequence_count",
      target: 1,
    },
  },
  {
    id: "sequences_10",
    title: "Sequence Builder",
    description: "Create 10 sequences",
    category: "creator",
    tier: "silver",
    xpReward: 100,
    icon: "fa-hammer",
    requirement: {
      type: "sequence_count",
      target: 10,
    },
  },
  {
    id: "sequences_50",
    title: "Flow Composer",
    description: "Create 50 sequences",
    category: "creator",
    tier: "gold",
    xpReward: 250,
    icon: "fa-palette",
    requirement: {
      type: "sequence_count",
      target: 50,
    },
  },
  {
    id: "sequences_100",
    title: "Master Choreographer",
    description: "Create 100 sequences",
    category: "creator",
    tier: "platinum",
    xpReward: 500,
    icon: "fa-crown",
    requirement: {
      type: "sequence_count",
      target: 100,
    },
  },
  {
    id: "spell_name",
    title: "Personal Touch",
    description: "Create a sequence that spells your name",
    category: "creator",
    tier: "bronze",
    xpReward: 75,
    icon: "fa-pen-fancy",
    requirement: {
      type: "specific_action",
      target: 1,
      metadata: { action: "spell_name" },
    },
  },
  {
    id: "alphabet_master",
    title: "Alphabet Master",
    description: "Create sequences using all 26 letters",
    category: "creator",
    tier: "gold",
    xpReward: 300,
    icon: "fa-spell-check",
    requirement: {
      type: "letter_usage",
      target: 26,
    },
  },
  {
    id: "long_sequence",
    title: "Marathon Flow",
    description: "Create a sequence with 10+ beats",
    category: "creator",
    tier: "silver",
    xpReward: 150,
    icon: "fa-ruler",
    requirement: {
      type: "sequence_length",
      target: 10,
    },
  },
];

// ============================================================================
// SCHOLAR ACHIEVEMENTS (Learning Concepts)
// ============================================================================

const SCHOLAR_ACHIEVEMENTS: Achievement[] = [
  {
    id: "first_concept",
    title: "Curious Mind",
    description: "Complete your first concept",
    category: "scholar",
    tier: "bronze",
    xpReward: 50,
    icon: "fa-book-open",
    requirement: {
      type: "concept_completion",
      target: 1,
    },
  },
  {
    id: "concepts_5",
    title: "Dedicated Student",
    description: "Complete 5 concepts",
    category: "scholar",
    tier: "silver",
    xpReward: 100,
    icon: "fa-graduation-cap",
    requirement: {
      type: "concept_completion",
      target: 5,
    },
  },
  {
    id: "concepts_15",
    title: "Scholar",
    description: "Complete 15 concepts",
    category: "scholar",
    tier: "gold",
    xpReward: 250,
    icon: "fa-book",
    requirement: {
      type: "concept_completion",
      target: 15,
    },
  },
  {
    id: "concepts_28",
    title: "TKA Master",
    description: "Complete all 28 concepts",
    category: "scholar",
    tier: "platinum",
    xpReward: 500,
    icon: "fa-trophy",
    requirement: {
      type: "concept_completion",
      target: 28,
    },
  },
];

// ============================================================================
// PRACTITIONER ACHIEVEMENTS (Daily Streaks & Practice)
// ============================================================================

const PRACTITIONER_ACHIEVEMENTS: Achievement[] = [
  {
    id: "streak_3",
    title: "Getting Started",
    description: "Practice 3 days in a row",
    category: "practitioner",
    tier: "bronze",
    xpReward: 75,
    icon: "fa-fire",
    requirement: {
      type: "daily_streak",
      target: 3,
    },
  },
  {
    id: "streak_7",
    title: "Weekly Warrior",
    description: "Practice 7 days in a row",
    category: "practitioner",
    tier: "silver",
    xpReward: 150,
    icon: "fa-calendar-days",
    requirement: {
      type: "daily_streak",
      target: 7,
    },
  },
  {
    id: "streak_30",
    title: "Dedicated Practitioner",
    description: "Practice 30 days in a row",
    category: "practitioner",
    tier: "gold",
    xpReward: 300,
    icon: "fa-dumbbell",
    requirement: {
      type: "daily_streak",
      target: 30,
    },
  },
  {
    id: "streak_100",
    title: "Flow Master",
    description: "Practice 100 days in a row",
    category: "practitioner",
    tier: "platinum",
    xpReward: 1000,
    icon: "fa-star",
    requirement: {
      type: "daily_streak",
      target: 100,
    },
  },
];

// ============================================================================
// EXPLORER ACHIEVEMENTS (Browsing Gallery)
// ============================================================================

const EXPLORER_ACHIEVEMENTS: Achievement[] = [
  {
    id: "explore_10",
    title: "Window Shopping",
    description: "Explore 10 sequences",
    category: "explorer",
    tier: "bronze",
    xpReward: 50,
    icon: "fa-magnifying-glass",
    requirement: {
      type: "gallery_exploration",
      target: 10,
    },
  },
  {
    id: "explore_50",
    title: "Gallery Enthusiast",
    description: "Explore 50 sequences",
    category: "explorer",
    tier: "silver",
    xpReward: 100,
    icon: "fa-images",
    requirement: {
      type: "gallery_exploration",
      target: 50,
    },
  },
  {
    id: "explore_100",
    title: "Sequence Connoisseur",
    description: "Explore 100 sequences",
    category: "explorer",
    tier: "gold",
    xpReward: 200,
    icon: "fa-wand-sparkles",
    requirement: {
      type: "gallery_exploration",
      target: 100,
    },
  },
];

// ============================================================================
// GENERATION ACHIEVEMENTS (Using Auto-Generate)
// ============================================================================

const GENERATION_ACHIEVEMENTS: Achievement[] = [
  {
    id: "generate_first",
    title: "Lucky Roll",
    description: "Generate your first sequence",
    category: "creator",
    tier: "bronze",
    xpReward: 25,
    icon: "fa-dice",
    requirement: {
      type: "generation_count",
      target: 1,
    },
  },
  {
    id: "generate_25",
    title: "Idea Generator",
    description: "Generate 25 sequences",
    category: "creator",
    tier: "silver",
    xpReward: 75,
    icon: "fa-lightbulb",
    requirement: {
      type: "generation_count",
      target: 25,
    },
  },
  {
    id: "generate_100",
    title: "Inspiration Engine",
    description: "Generate 100 sequences",
    category: "creator",
    tier: "gold",
    xpReward: 200,
    icon: "fa-gear",
    requirement: {
      type: "generation_count",
      target: 100,
    },
  },
];

// ============================================================================
// ALL ACHIEVEMENTS
// ============================================================================

export const ALL_ACHIEVEMENTS: Achievement[] = [
  ...CREATOR_ACHIEVEMENTS,
  ...SCHOLAR_ACHIEVEMENTS,
  ...PRACTITIONER_ACHIEVEMENTS,
  ...EXPLORER_ACHIEVEMENTS,
  ...GENERATION_ACHIEVEMENTS,
];

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

export function getAchievementById(id: string): Achievement | undefined {
  return ALL_ACHIEVEMENTS.find((achievement) => achievement.id === id);
}

export function getAchievementsByCategory(
  category: Achievement["category"]
): Achievement[] {
  return ALL_ACHIEVEMENTS.filter(
    (achievement) => achievement.category === category
  );
}

export function getAchievementsByTier(
  tier: Achievement["tier"]
): Achievement[] {
  return ALL_ACHIEVEMENTS.filter((achievement) => achievement.tier === tier);
}
