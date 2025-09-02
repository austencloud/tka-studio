/**
 * Motion Helper Service Interface
 * 
 * Provides utilities for working with motion types and motion-related calculations.
 */

import type { MotionType } from "$domain";

export interface IMotionHelperService {
  /**
   * Get all available motion types
   */
  getAvailableMotionTypes(): MotionType[];

  /**
   * Check if a motion type is valid
   */
  isValidMotionType(motionType: string): boolean;

  /**
   * Get motion type display name
   */
  getMotionTypeDisplayName(motionType: MotionType): string;

  /**
   * Get motion type description
   */
  getMotionTypeDescription(motionType: MotionType): string;
}
