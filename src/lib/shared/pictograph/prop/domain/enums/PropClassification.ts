/**
 * Prop Classification System
 *
 * This determines whether beta offset should be applied based on orientation.
 *
 * From desktop: legacy/enums/prop_type.py
 */

/**
 * Big Unilateral Props
 * - Large size
 * - SKIP beta offset when ending in radial (IN/OUT) or non-radial (CLOCK/COUNTER)
 */
export const BIG_UNILATERAL_PROPS = ["bighoop", "guitar", "sword"] as const;

/**
 * Small Unilateral Props
 * - Small/medium size
 * - SKIP beta offset when ending in radial (IN/OUT) or non-radial (CLOCK/COUNTER)
 */
export const SMALL_UNILATERAL_PROPS = [
  "fan",
  "club",
  "minihoop",
  "triad", // ← TRIAD IS UNILATERAL!
  "ukulele",
  "triquetra",
  "triquetra2",
] as const;

/**
 * Big Bilateral Props
 * - Large size
 * - ALWAYS apply beta offset
 */
export const BIG_BILATERAL_PROPS = [
  "bigstaff",
  "bigbuugeng",
  "bigdoublestar",
  "bigeightrings",
] as const;

/**
 * Small Bilateral Props
 * - Held with two hands
 * - Small/medium size
 * - ALWAYS apply beta offset
 */
export const SMALL_BILATERAL_PROPS = [
  "staff",
  "simple_staff",
  "buugeng",
  "doublestar",
  "quiad",
  "fractalgeng",
  "eightrings",
  "chicken",
] as const;

// Union types for type checking
export type BigUnilateralProp = (typeof BIG_UNILATERAL_PROPS)[number];
export type SmallUnilateralProp = (typeof SMALL_UNILATERAL_PROPS)[number];
export type BigBilateralProp = (typeof BIG_BILATERAL_PROPS)[number];
export type SmallBilateralProp = (typeof SMALL_BILATERAL_PROPS)[number];

export type UnilateralProp = BigUnilateralProp | SmallUnilateralProp;
export type BilateralProp = BigBilateralProp | SmallBilateralProp;

/**
 * Check if a prop is unilateral (one-handed)
 */
export function isUnilateralProp(propType: string): boolean {
  const normalizedType = propType.toLowerCase();
  return (
    (BIG_UNILATERAL_PROPS as readonly string[]).includes(normalizedType) ||
    (SMALL_UNILATERAL_PROPS as readonly string[]).includes(normalizedType)
  );
}

/**
 * Check if a prop is bilateral (two-handed)
 */
export function isBilateralProp(propType: string): boolean {
  const normalizedType = propType.toLowerCase();
  return (
    (BIG_BILATERAL_PROPS as readonly string[]).includes(normalizedType) ||
    (SMALL_BILATERAL_PROPS as readonly string[]).includes(normalizedType)
  );
}

/**
 * Check if a prop is big (requires larger spacing)
 */
export function isBigProp(propType: string): boolean {
  const normalizedType = propType.toLowerCase();
  return (
    (BIG_UNILATERAL_PROPS as readonly string[]).includes(normalizedType) ||
    (BIG_BILATERAL_PROPS as readonly string[]).includes(normalizedType)
  );
}

/**
 * Check if a prop is small (normal spacing)
 */
export function isSmallProp(propType: string): boolean {
  const normalizedType = propType.toLowerCase();
  return (
    (SMALL_UNILATERAL_PROPS as readonly string[]).includes(normalizedType) ||
    (SMALL_BILATERAL_PROPS as readonly string[]).includes(normalizedType)
  );
}

/**
 * Get the beta offset size for a prop type
 *
 * Based on desktop calculations:
 * - Large props: 950/60 = 15.83px
 * - Medium props (doublestar): 950/50 = 19px
 * - Default/small props: 950/45 = 21.11px
 *
 * Box mode applies diagonal compensation (÷√2) since diagonal vectors travel 1.414x farther
 * than cardinal vectors, resulting in equal visual spacing between diamond and box modes.
 */
export function getBetaOffsetSize(
  propType: string,
  gridMode?: "diamond" | "box" | "skewed"
): number {
  const normalizedType = propType.toLowerCase();

  let baseOffset: number;

  // Large props
  if (normalizedType === "club" || normalizedType === "eightrings") {
    baseOffset = 950 / 60; // 15.83px
  }
  // Medium props
  else if (normalizedType === "doublestar") {
    baseOffset = 950 / 50; // 19px
  }
  // Default/small props
  else {
    baseOffset = 950 / 45; // 21.11px
  }

  // Compensate for diagonal vector magnitude in box mode
  // Diagonal vectors have magnitude √2 ≈ 1.414, so we divide by √2 to achieve equal visual spacing
  if (gridMode === "box") {
    return baseOffset / Math.sqrt(2); // ÷ 1.414
  }

  return baseOffset;
}
