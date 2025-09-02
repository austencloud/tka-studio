/**
 * Letter Border Colors
 *
 * Clean utility for getting letter border colors based on the desktop app's
 * PictographBorderManager dual border system.
 */

import { Letter, getLetterType } from "$domain";
import { LetterType } from "$domain";

/**
 * Letter type border color mapping from desktop app
 * Format: [primary, secondary] for outer and inner borders
 */
const LETTER_TYPE_COLORS = {
  [LetterType.TYPE1]: ["#36c3ff", "#6F2DA8"], // Dual-Shift: Cyan, Purple
  [LetterType.TYPE2]: ["#6F2DA8", "#6F2DA8"], // Shift: Purple, Purple
  [LetterType.TYPE3]: ["#26e600", "#6F2DA8"], // Cross-Shift: Green, Purple
  [LetterType.TYPE4]: ["#26e600", "#26e600"], // Dash: Green, Green
  [LetterType.TYPE5]: ["#00b3ff", "#26e600"], // Dual-Dash: Blue, Green
  [LetterType.TYPE6]: ["#eb7d00", "#eb7d00"], // Static: Orange, Orange
} as const;

/**
 * Get border colors for a letter
 */
export function getLetterBorderColors(letter: Letter | null | undefined) {
  if (!letter) return { primary: "#000000", secondary: "#000000" };

  const letterType = getLetterType(letter);
  const [primary, secondary] = LETTER_TYPE_COLORS[letterType] || [
    "#000000",
    "#000000",
  ];

  return { primary, secondary };
}

/**
 * Get primary border color for a letter
 */
export function getLetterBorderColor(
  letter: Letter | null | undefined
): string {
  return getLetterBorderColors(letter).primary;
}

// Legacy aliases for backward compatibility
export const getLetterBorderColorsSafe = getLetterBorderColors;
export const getLetterBorderColorSafe = getLetterBorderColor;
