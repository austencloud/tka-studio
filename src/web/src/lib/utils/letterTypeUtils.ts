/**
 * Letter Type Classification Utility
 *
 * Provides utilities for determining letter types and their associated colors.
 * This is shared across the application for consistent letter type handling.
 */

export type LetterType =
  | "Type1"
  | "Type2"
  | "Type3"
  | "Type4"
  | "Type5"
  | "Type6";

/**
 * Letter classifications by type
 */
const LETTER_TYPE_CLASSIFICATIONS: Record<LetterType, string[]> = {
  Type1: [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
  ],
  Type2: ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"],
  Type3: ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"],
  Type4: ["Φ", "Ψ", "Λ"],
  Type5: ["Φ-", "Ψ-", "Λ-"],
  Type6: ["α", "β", "Γ"],
};

/**
 * Border colors by letter type (matching SelectionBorderOverlay from legacy)
 */
const LETTER_TYPE_BORDER_COLORS: Record<LetterType, string> = {
  Type1: "var(--primary)",
  Type2: "var(--primary)",
  Type3: "var(--primary)",
  Type4: "var(--primary)",
  Type5: "var(--primary)",
  Type6: "#eb7d00", // Orange for Type 6 (α, β, Γ)
};

/**
 * Determines the letter type for a given letter
 */
export function getLetterType(letter: string | null): LetterType {
  if (!letter) return "Type1";

  // Find which type contains this letter
  for (const [type, letters] of Object.entries(LETTER_TYPE_CLASSIFICATIONS)) {
    if (letters.includes(letter)) {
      return type as LetterType;
    }
  }

  return "Type1"; // Default fallback
}

/**
 * Gets the border color for a letter based on its type
 */
export function getLetterBorderColor(letter: string | null): string {
  const letterType = getLetterType(letter);
  return LETTER_TYPE_BORDER_COLORS[letterType];
}

/**
 * Gets all letters of a specific type
 */
export function getLettersOfType(type: LetterType): string[] {
  return LETTER_TYPE_CLASSIFICATIONS[type] || [];
}

/**
 * Checks if a letter is of a specific type
 */
export function isLetterOfType(
  letter: string | null,
  type: LetterType,
): boolean {
  if (!letter) return type === "Type1";
  return getLetterType(letter) === type;
}
