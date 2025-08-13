/**
 * Letter Type Classification Utility
 *
 * Provides functions to classify letters into their appropriate types
 * and get associated colors/styling. Used across the application
 * for consistent letter type handling.
 */

export type LetterType =
  | "Type1"
  | "Type2"
  | "Type3"
  | "Type4"
  | "Type5"
  | "Type6";

// Letter classifications based on the legacy system
const LETTER_CLASSIFICATIONS: Record<LetterType, string[]> = {
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

// Border colors matching the legacy SelectionBorderOverlay system
const BORDER_COLORS: Record<LetterType, string> = {
  Type1: "var(--primary)",
  Type2: "var(--primary)",
  Type3: "var(--primary)",
  Type4: "var(--primary)",
  Type5: "var(--primary)",
  Type6: "#eb7d00", // Orange for Type 6
};

/**
 * Classify a letter into its type
 */
export function getLetterType(letter: string | null | undefined): LetterType {
  if (!letter) return "Type1";

  for (const [type, letters] of Object.entries(LETTER_CLASSIFICATIONS)) {
    if (letters.includes(letter)) {
      return type as LetterType;
    }
  }

  return "Type1"; // Default fallback
}

/**
 * Get the border color for a letter type
 */
export function getLetterBorderColor(
  letter: string | null | undefined,
): string {
  const letterType = getLetterType(letter);
  return BORDER_COLORS[letterType];
}

/**
 * Get the border color directly from letter type
 */
export function getBorderColorForType(letterType: LetterType): string {
  return BORDER_COLORS[letterType];
}

/**
 * Check if a letter is of a specific type
 */
export function isLetterType(
  letter: string | null | undefined,
  type: LetterType,
): boolean {
  return getLetterType(letter) === type;
}

/**
 * Get all letters of a specific type
 */
export function getLettersOfType(type: LetterType): string[] {
  return LETTER_CLASSIFICATIONS[type] || [];
}

/**
 * Get the safe filename for a letter (handles Greek letters and special characters)
 * The actual files use the literal characters, so no mapping is needed
 */
export function getLetterFilename(letter: string): string {
  // Files use the actual characters (W-.svg, Λ.svg, α.svg, etc.)
  // No mapping needed - return the letter as-is
  return letter;
}

/**
 * Get the full image path for a letter based on its type
 * URL-encodes the filename to match browser fetch behavior
 */
export function getLetterImagePath(letter: string): string {
  const letterType = getLetterType(letter);
  const filename = getLetterFilename(letter);
  // URL-encode the filename to match what the browser will actually request
  const encodedFilename = encodeURIComponent(filename);
  return `/images/letters_trimmed/${letterType}/${encodedFilename}.svg`;
}
