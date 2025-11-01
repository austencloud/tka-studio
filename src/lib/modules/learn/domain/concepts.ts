/**
 * TKA Studio - Complete Learning Path for The Kinetic Alphabet
 *
 * This file defines the complete progression of concepts from the TKA Level 1 curriculum.
 * Concepts are organized into categories and unlock sequentially to guide learners
 * through a logical progression from foundation to advanced techniques.
 */

import type { ConceptCategory, LearnConcept } from "./types";

/**
 * Complete TKA Learning Path - 28 Concepts
 * Based on "The Kinetic Alphabet Level 1" curriculum
 */
export const TKA_CONCEPTS: LearnConcept[] = [
  // ============================================================================
  // FOUNDATION CATEGORY
  // Core building blocks - understanding the grid and basic positions/motions
  // ============================================================================
  {
    id: "grid",
    order: 1,
    category: "foundation",
    name: "The Grid",
    shortName: "Grid",
    description: "Master the 4-point diamond and box grid system",
    icon: "◇",
    pdfPages: [7],
    prerequisites: [],
    estimatedMinutes: 5,
    concepts: [
      "Diamond vs Box mode",
      "4-point grid structure",
      "8-point combined grid",
      "Center, hand, and outer points",
    ],
  },
  {
    id: "hand-positions",
    order: 2,
    category: "foundation",
    name: "Hand Positions",
    shortName: "Positions",
    description: "Learn Alpha, Beta, and Gamma hand positions",
    icon: "✋",
    pdfPages: [8],
    prerequisites: ["grid"],
    estimatedMinutes: 8,
    concepts: [
      "Alpha - hands across from each other",
      "Beta - hands at same point",
      "Gamma - hands form right angle",
    ],
  },
  {
    id: "hand-motions-intro",
    order: 3,
    category: "foundation",
    name: "Hand Motions Overview",
    shortName: "Motions",
    description: "Understand the three fundamental hand motions",
    icon: "→",
    pdfPages: [9],
    prerequisites: ["hand-positions"],
    estimatedMinutes: 10,
    concepts: [
      "Shift - move to adjacent point",
      "Dash - move to opposite point",
      "Static - remain at current point",
    ],
  },
  {
    id: "dual-shifts-alpha-beta",
    order: 4,
    category: "foundation",
    name: "Dual-Shifts: Alpha & Beta",
    shortName: "Dual-Shifts",
    description: "Practice split-same and tog-same dual-shift patterns",
    icon: "⇄",
    pdfPages: [10],
    prerequisites: ["hand-motions-intro"],
    estimatedMinutes: 12,
    concepts: [
      "Split-Same (SS)",
      "Tog-Same (TS)",
      "Split-Opp (SO)",
      "Tog-Opp (TO)",
    ],
  },
  {
    id: "gamma-motion",
    order: 5,
    category: "foundation",
    name: "Gamma Motions",
    shortName: "Gamma",
    description: "Master quarter-time movements in gamma position",
    icon: "Γ",
    pdfPages: [11],
    prerequisites: ["dual-shifts-alpha-beta"],
    estimatedMinutes: 15,
    concepts: [
      "Quarter-Opp (parallel & antiparallel)",
      "Quarter-Same patterns",
      "Continuous vs non-continuous",
    ],
  },
  {
    id: "shifts-type2",
    order: 6,
    category: "foundation",
    name: "Type 2: Shifts",
    shortName: "Shifts",
    description: "Move between Gamma and Alpha/Beta positions",
    icon: "↗",
    pdfPages: [12],
    prerequisites: ["gamma-motion"],
    estimatedMinutes: 10,
    concepts: [
      "One hand shifts, one static",
      "Opening vs closing shifts",
      "Γ ↔ α/β transitions",
    ],
  },
  {
    id: "cross-shifts-type3",
    order: 7,
    category: "foundation",
    name: "Type 3: Cross-Shifts",
    shortName: "Cross-Shifts",
    description: "Combine shifts with dashes for dynamic motion",
    icon: "⤫",
    pdfPages: [13],
    prerequisites: ["shifts-type2"],
    estimatedMinutes: 12,
    concepts: [
      "Shift + Dash combination",
      "Halfway point technique",
      "Zan's Diamond variations",
    ],
  },
  {
    id: "dash-type4",
    order: 8,
    category: "foundation",
    name: "Type 4: Dash",
    shortName: "Dash",
    description: "One hand dashes while the other remains static",
    icon: "⟹",
    pdfPages: [14],
    prerequisites: ["cross-shifts-type3"],
    estimatedMinutes: 8,
    concepts: [
      "Single dash motion",
      "Creating multi-beat sequences",
      "β→α and γ→γ dashes",
    ],
  },
  {
    id: "dual-dash-type5",
    order: 9,
    category: "foundation",
    name: "Type 5: Dual-Dash",
    shortName: "Dual-Dash",
    description: "Both hands dash simultaneously",
    icon: "⇉",
    pdfPages: [14],
    prerequisites: ["dash-type4"],
    estimatedMinutes: 8,
    concepts: [
      "Simultaneous dashing",
      "Position maintenance",
      "α→α, β→β, γ→γ patterns",
    ],
  },
  {
    id: "static-type6",
    order: 10,
    category: "foundation",
    name: "Type 6: Static",
    shortName: "Static",
    description: "Hold positions for beats with no motion",
    icon: "◯",
    pdfPages: [14],
    prerequisites: ["dual-dash-type5"],
    estimatedMinutes: 5,
    concepts: [
      "Static holds in sequences",
      "Adding prop rotations to statics",
      "Body turns during static beats",
    ],
  },
  {
    id: "staff-positions",
    order: 11,
    category: "foundation",
    name: "Staff Positions",
    shortName: "Staff Pos.",
    description: "Track thumb orientations for staff work",
    icon: "|",
    pdfPages: [15],
    prerequisites: ["static-type6"],
    estimatedMinutes: 10,
    concepts: [
      "Thumbs in/out orientations",
      "Marking the thumb end",
      "Position checking on beats",
    ],
  },
  {
    id: "staff-motions",
    order: 12,
    category: "foundation",
    name: "Staff Motions",
    shortName: "Staff Motion",
    description: "Learn prospin and antispin rotations",
    icon: "↻",
    pdfPages: [16],
    prerequisites: ["staff-positions"],
    estimatedMinutes: 15,
    concepts: [
      "Prospin - rotate with handpath",
      "Antispin - rotate opposite handpath",
      "90° isolation as base unit",
      "Thumb orientation changes",
    ],
  },
  {
    id: "negative-space",
    order: 13,
    category: "foundation",
    name: "Negative Space & Body Turns",
    shortName: "Negative Space",
    description: "Essential techniques for advanced sequences",
    icon: "◐",
    pdfPages: [17],
    prerequisites: ["staff-motions"],
    estimatedMinutes: 20,
    concepts: [
      "360° Isolation",
      "4-Petal Antispin",
      "Shoulder/elbow negative space",
      "Body turn timing",
    ],
  },

  // ============================================================================
  // LETTERS CATEGORY
  // Learning the alphabet - categorizing motions into letters
  // ============================================================================
  {
    id: "letter-codex-intro",
    order: 14,
    category: "letters",
    name: "Letter Codex Overview",
    shortName: "Codex Intro",
    description: "Introduction to the TKA letter system",
    icon: "Σ",
    pdfPages: [18, 19, 20],
    prerequisites: ["negative-space"],
    estimatedMinutes: 10,
    concepts: [
      "Type 1-6 motion categories",
      "Pro, Anti, Hybrid patterns",
      "Letter organization system",
    ],
  },
  {
    id: "type1-abc-ghi",
    order: 15,
    category: "letters",
    name: "Type 1: ABC & GHI",
    shortName: "ABC/GHI",
    description: "Split-Same and Tog-Same dual-shift letters",
    icon: "A",
    pdfPages: [21],
    prerequisites: ["letter-codex-intro"],
    estimatedMinutes: 15,
    concepts: [
      "A - Pro split-same (α→α)",
      "B - Anti split-same",
      "C - Hybrid split-same",
      "G - Pro tog-same (β→β)",
      "H - Anti tog-same",
      "I - Hybrid tog-same",
    ],
  },
  {
    id: "type1-compound",
    order: 16,
    category: "letters",
    name: "Type 1: DJ, EK, FL",
    shortName: "Compound",
    description: "Compound letters moving between α and β",
    icon: "D",
    pdfPages: [22, 23],
    prerequisites: ["type1-abc-ghi"],
    estimatedMinutes: 12,
    concepts: [
      "D, E, F (β→α)",
      "J, K, L (α→β)",
      "Iso, Anti, Hybrid variations",
      "Memory phrases (Disco Jam, etc.)",
    ],
  },
  {
    id: "type1-gamma-compound",
    order: 17,
    category: "letters",
    name: "Type 1: MP, NQ, OR",
    shortName: "Γ Compound",
    description: "Quarter-Opp gamma compound letters",
    icon: "M",
    pdfPages: [24],
    prerequisites: ["type1-compound"],
    estimatedMinutes: 12,
    concepts: [
      "M, N, O (Γ→Γ opp)",
      "P, Q, R (Γ→Γ opp mirror)",
      "Magic Potion, Never Quit, Open Road",
    ],
  },
  {
    id: "type1-stuv",
    order: 18,
    category: "letters",
    name: "Type 1: STUV",
    shortName: "STUV",
    description: "Quarter-Same gamma letters with leading hand",
    icon: "S",
    pdfPages: [24, 25],
    prerequisites: ["type1-gamma-compound"],
    estimatedMinutes: 10,
    concepts: [
      "S, T (Γ→Γ same)",
      "U - leads with isolation (round)",
      "V - leads with antispin (spiky)",
      "Leading vs following hand",
    ],
  },
  {
    id: "type2-wxyz",
    order: 19,
    category: "letters",
    name: "Type 2: WXYZ, ΣΔθΩ",
    shortName: "Type 2",
    description: "Shift letters - one shifts, one static",
    icon: "W",
    pdfPages: [26],
    prerequisites: ["type1-stuv"],
    estimatedMinutes: 10,
    concepts: [
      "W, X (Γ→α open)",
      "Y, Z (Γ→β close)",
      "Σ, Δ (α→Γ close)",
      "θ, Ω (β→Γ open)",
    ],
  },
  {
    id: "type3-cross-shift-letters",
    order: 20,
    category: "letters",
    name: "Type 3: Cross-Shift Letters",
    shortName: "Type 3",
    description: "Letters with dash notation (W-, Σ-, etc.)",
    icon: "W-",
    pdfPages: [27],
    prerequisites: ["type2-wxyz"],
    estimatedMinutes: 12,
    concepts: [
      "Dash notation explained",
      "W-, X-, Y-, Z- variations",
      "Σ-, Δ-, θ-, Ω- variations",
      "Halfway point timing",
    ],
  },
  {
    id: "type456-dash-static",
    order: 21,
    category: "letters",
    name: "Type 4/5/6: Φ Ψ Λ",
    shortName: "Dash/Static",
    description: "Dash, Dual-Dash, and Static letter types",
    icon: "Φ",
    pdfPages: [28],
    prerequisites: ["type3-cross-shift-letters"],
    estimatedMinutes: 10,
    concepts: [
      "Φ - Dash (β→α)",
      "Ψ - Dash (α→β)",
      "Λ - Dash (Γ→Γ)",
      "Dual-dash (-) variants",
      "α, β, Γ static positions",
    ],
  },

  // ============================================================================
  // COMBINATIONS CATEGORY
  // Putting letters together into words, sequences, and patterns
  // ============================================================================
  {
    id: "words-alpha-beta",
    order: 22,
    category: "combinations",
    name: "Words: Alpha/Beta",
    shortName: "AB Words",
    description: "Self-combining letters (AA, BB, CC, etc.)",
    icon: "AA",
    pdfPages: [29, 30],
    prerequisites: ["type456-dash-static"],
    estimatedMinutes: 20,
    concepts: [
      "AABB pattern exploration",
      "Thumb orientation variations",
      "Negative space application",
      "Letters as categories not specifics",
    ],
  },
  {
    id: "compound-words",
    order: 23,
    category: "combinations",
    name: "Compound Words",
    shortName: "Compound",
    description: "DJ, EK, FL two-letter sequences",
    icon: "DJ",
    pdfPages: [22, 23],
    prerequisites: ["words-alpha-beta"],
    estimatedMinutes: 15,
    concepts: [
      "DJ sequences",
      "EK sequences",
      "FL sequences",
      "Tog-Opp vs Split-Opp execution",
    ],
  },
  {
    id: "gamma-words",
    order: 24,
    category: "combinations",
    name: "Gamma Words",
    shortName: "Γ Words",
    description: "Four-letter gamma sequences",
    icon: "MPMP",
    pdfPages: [25],
    prerequisites: ["compound-words"],
    estimatedMinutes: 18,
    concepts: [
      "MPMP, NQNQ, OROR patterns",
      "SSSS, TTTT sequences",
      "UUUU, VVVV sequences",
      "Γ→Γ continuous motion",
    ],
  },
  {
    id: "caps-intro",
    order: 25,
    category: "combinations",
    name: "CAPs - Continuous Assembly Patterns",
    shortName: "CAPs",
    description: "Repeating patterns that return to start position",
    icon: "🔄",
    pdfPages: [31, 32, 33],
    prerequisites: ["gamma-words"],
    estimatedMinutes: 20,
    concepts: [
      "Mirrored CAPs",
      "Rotated CAPs",
      "Swapped CAPs",
      "Returning to home position",
    ],
  },
  {
    id: "reversals",
    order: 26,
    category: "combinations",
    name: "Reversals",
    shortName: "Reversals",
    description: "Hand, prop, and full reversal techniques",
    icon: "⟲",
    pdfPages: [32, 33, 34, 35],
    prerequisites: ["caps-intro"],
    estimatedMinutes: 25,
    concepts: [
      "Hand reversals (simplest)",
      "Prop reversals (R/R notation)",
      "Full reversals (backwards in time)",
      "Reversal placement in CAPs",
    ],
  },
  {
    id: "advanced-caps",
    order: 27,
    category: "combinations",
    name: "Advanced CAP Examples",
    shortName: "Adv. CAPs",
    description: "16-count sequences and 8-letter words",
    icon: "🎯",
    pdfPages: [36, 37, 38, 39, 40, 41],
    prerequisites: ["reversals"],
    estimatedMinutes: 30,
    concepts: [
      "Type 1 CAPs (DJII, BBLF, KIEC)",
      "Gamma rotated CAPs",
      "Type 2 CAPs",
      "16-count sequences",
      "8-letter word construction",
      "Prop-reversal CAPs",
      "Full-reversal CAPs",
    ],
  },

  // ============================================================================
  // ADVANCED CATEGORY
  // Optional mastery concepts for dedicated learners
  // ============================================================================
  {
    id: "motion-type-mastery",
    order: 28,
    category: "advanced",
    name: "Motion Type Mastery",
    shortName: "Motion Types",
    description: "Master all 6 motion type combinations",
    icon: "⚡",
    pdfPages: [5, 6, 7, 8, 9],
    prerequisites: ["advanced-caps"],
    estimatedMinutes: 40,
    concepts: [
      "Type 1: Dual-Shift mastery",
      "Type 2: Shift mastery",
      "Type 3: Cross-Shift mastery",
      "Type 4: Dash mastery",
      "Type 5: Dual-Dash mastery",
      "Type 6: Static mastery",
      "Combining all types fluidly",
    ],
  },
];

/**
 * Concept categories for organization
 */
export const CONCEPT_CATEGORIES: Record<
  ConceptCategory,
  {
    name: string;
    description: string;
    icon: string;
    color: string;
  }
> = {
  foundation: {
    name: "Foundation",
    description: "Core building blocks of The Kinetic Alphabet",
    icon: "🏛️",
    color: "#4A90E2", // Blue
  },
  letters: {
    name: "Letters",
    description: "Learn the TKA letter system and notation",
    icon: "📝",
    color: "#7B68EE", // Purple
  },
  combinations: {
    name: "Combinations",
    description: "Words, CAPs, and advanced sequences",
    icon: "🔗",
    color: "#50C878", // Green
  },
  advanced: {
    name: "Advanced",
    description: "Mastery-level concepts and techniques",
    icon: "🚀",
    color: "#FF6B6B", // Red
  },
};

/**
 * Get concepts by category
 */
export function getConceptsByCategory(
  category: ConceptCategory
): LearnConcept[] {
  return TKA_CONCEPTS.filter((concept) => concept.category === category);
}

/**
 * Get concept by ID
 */
export function getConceptById(id: string): LearnConcept | undefined {
  return TKA_CONCEPTS.find((concept) => concept.id === id);
}

/**
 * Get next concept in progression
 */
export function getNextConcept(currentId: string): LearnConcept | undefined {
  const currentIndex = TKA_CONCEPTS.findIndex((c) => c.id === currentId);
  return TKA_CONCEPTS[currentIndex + 1];
}

/**
 * Get previous concept
 */
export function getPreviousConcept(
  currentId: string
): LearnConcept | undefined {
  const currentIndex = TKA_CONCEPTS.findIndex((c) => c.id === currentId);
  return currentIndex > 0 ? TKA_CONCEPTS[currentIndex - 1] : undefined;
}

/**
 * Check if concept is unlocked based on completed prerequisites
 */
export function isConceptUnlocked(
  conceptId: string,
  completedConcepts: Set<string>
): boolean {
  const concept = getConceptById(conceptId);
  if (!concept) return false;

  // First concept is always unlocked
  if (concept.prerequisites.length === 0) return true;

  // Check if all prerequisites are completed
  return concept.prerequisites.every((prereq) => completedConcepts.has(prereq));
}
