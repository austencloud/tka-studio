/**
 * usePictographData.ts - Data Transformation Hook
 *
 * Handles all data transformation and derivation logic for the Pictograph component.
 * This includes merging different data sources, filtering, and computing display values.
 *
 * REFACTORED: Updated to use proper Svelte 5 runes with reactive getters.
 */

import type { MotionColor, MotionData, PictographData } from "$domain";

export interface PictographDataProps {
  pictographData?: PictographData | null;
}

export interface PictographDataState {
  /** Get the effective pictograph data from either prop */
  get effectivePictographData(): PictographData | null;
  /** Check if we have valid data to render */
  get hasValidData(): boolean;
  /** Get the display letter for the pictograph */
  get displayLetter(): string | null;
  /** Get motion data ready for rendering (embedded approach) */
  get motionsToRender(): Array<{ color: MotionColor; motionData: MotionData }>;
  /** @deprecated Use motionsToRender instead - kept for backward compatibility */
  get arrowsToRender(): Array<{ color: MotionColor; motionData: MotionData }>;
  /** @deprecated Use motionsToRender instead - kept for backward compatibility */
  get propsToRender(): Array<{ color: MotionColor; motionData: MotionData }>;
}

/**
 * Hook for managing pictograph data transformation and derivation
 * Returns reactive getters using Svelte 5 $derived pattern
 */
export function usePictographData(
  props: PictographDataProps
): PictographDataState {
  const { pictographData } = props;

  return {
    // Get effective pictograph data
    get effectivePictographData() {
      return pictographData || null;
    },

    // Check if we have valid data
    get hasValidData() {
      return this.effectivePictographData != null;
    },

    // Get display letter
    get displayLetter() {
      const data = this.effectivePictographData;
      if (data?.letter) return data.letter;
      return null;
    },

    // Get motions to render (embedded approach - single source of truth)
    get motionsToRender() {
      const data = this.effectivePictographData;
      if (!data?.motions) return [];

      return Object.entries(data.motions)
        .filter(([_, motionData]) => motionData?.isVisible)
        .filter(([, motionData]) => motionData !== null)
        .map(([color, motionData]) => ({
          color: color as MotionColor,
          motionData: motionData,
        }));
    },

    // Backward compatibility - arrows now come from motions
    get arrowsToRender() {
      return this.motionsToRender;
    },

    // Backward compatibility - props now come from motions
    get propsToRender() {
      return this.motionsToRender;
    },
  };
}
