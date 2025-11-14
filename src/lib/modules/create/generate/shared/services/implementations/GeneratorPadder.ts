/**
 * GeneratorPadder
 *
 * Calculates aspect-ratio-aware, responsive padding for the Generate panel.
 *
 * Core principles:
 * - Portrait panels: More vertical padding, less horizontal
 * - Landscape panels: More horizontal padding, ZERO vertical (maximize height)
 * - Constrained panels: No padding (maximize usable space)
 * - Progressive scaling: Larger panels get proportionally more padding
 *
 * @author TKA Studio
 * @date 2025-01-13
 */

export interface PaddingResult {
  top: number;
  right: number;
  bottom: number;
  left: number;
  scale: number;
}

export interface IGeneratorPadder {
  calculatePadding(width: number, height: number): PaddingResult;
}

export class GeneratorPadder implements IGeneratorPadder {
  private readonly BASE_PADDING = 6;

  /**
   * Calculate adaptive padding based on panel dimensions and aspect ratio
   */
  calculatePadding(width: number, height: number): PaddingResult {
    const aspectRatio = width / height;

    // === CONSTRAINED PANELS: Remove all padding ===

    // Extremely narrow panels (< 400px width)
    if (width < 400) {
      return { top: 0, right: 0, bottom: 0, left: 0, scale: 0 };
    }

    // Constrained dimensions (narrow AND short)
    if (width < 600 && height < 450) {
      return { top: 0, right: 0, bottom: 0, left: 0, scale: 0 };
    }

    // === SIZE-BASED SCALING ===
    const scale = this.calculateSizeScale(width, aspectRatio);

    // === ASPECT-RATIO-AWARE PADDING ===

    if (aspectRatio < 1) {
      // PORTRAIT: More vertical padding, less horizontal
      return this.calculatePortraitPadding(aspectRatio, scale);
    } else {
      // LANDSCAPE: Horizontal padding only, NO vertical
      return this.calculateLandscapePadding(aspectRatio, scale);
    }
  }

  /**
   * Calculate size-based scale multiplier
   * Includes special case for narrow portrait panels
   */
  private calculateSizeScale(width: number, aspectRatio: number): number {
    // Special case: narrow portrait panels (phone-like aspect ratio)
    if (width < 600 && aspectRatio < 0.65) {
      return 2; // Higher scale for narrow portrait
    }

    // Progressive scaling based on width
    if (width < 600) {
      return 1;
    } else if (width < 700) {
      const progress = (width - 200) / 200;
      return 1 + progress * 0.5; // 1x to 1.5x
    } else if (width < 850) {
      const progress = (width - 1000) / 200;
      return 4 + progress * 0.5; // 4x to 4.5x
    } else if (width < 1000) {
      const progress = (width - 1200) / 200;
      return 5 + progress * 0.5; // 5x to 5.5x
    } else if (width < 1100) {
      const progress = (width - 1200) / 200;
      return 6 + progress * 0.5; // 6x to 6.5x
    } else {
      return 3.0; // Max scale
    }
  }

  /**
   * Calculate portrait padding
   * More vertical padding to frame content, minimal horizontal
   */
  private calculatePortraitPadding(aspectRatio: number, scale: number): PaddingResult {
    const portraitFactor = Math.max(0, (1 - aspectRatio) / 0.7);

    // Vertical: 1.5x to 16x base padding (progressively more padding for narrower aspect ratios)
    const verticalMultiplier = 1.5 + portraitFactor * 14.5;

    // Horizontal: 1.5x to 1x base padding (less padding for narrower aspect ratios)
    const horizontalMultiplier = 1.5 - portraitFactor * 0.5;

    const verticalPadding = this.BASE_PADDING * verticalMultiplier * scale;
    const horizontalPadding = this.BASE_PADDING * horizontalMultiplier * scale;

    return {
      top: verticalPadding,
      bottom: verticalPadding,
      left: horizontalPadding,
      right: horizontalPadding,
      scale,
    };
  }

  /**
   * Calculate landscape padding
   * Horizontal padding only - vertical is ZERO to maximize height for card grid
   */
  private calculateLandscapePadding(aspectRatio: number, scale: number): PaddingResult {
    const landscapeFactor = Math.min(1, (aspectRatio - 1) / 2);

    // Horizontal: 1.5x to 8x base padding (progressively more padding for wider aspect ratios)
    const horizontalMultiplier = 1.5 + landscapeFactor * 6.5;

    const horizontalPadding = this.BASE_PADDING * horizontalMultiplier * scale;

    return {
      top: 0, // No top padding for landscape
      bottom: 0, // No bottom padding for landscape
      left: horizontalPadding,
      right: horizontalPadding,
      scale,
    };
  }
}
