/**
 * Motion Helper Service Implementation
 * 
 * Provides utilities for working with motion types and motion-related calculations.
 * Migrated from components/tabs/motion-tester-tab/utils/motion-helpers.ts to proper service architecture.
 */

import { injectable } from "inversify";
import type { IMotionHelperService } from "$contracts";
import type { MotionType } from "$domain";
import { MotionType as MotionTypeEnum } from "$domain";

@injectable()
export class MotionHelperService implements IMotionHelperService {
  /**
   * Get all available motion types
   */
  getAvailableMotionTypes(): MotionType[] {
    return Object.values(MotionTypeEnum);
  }

  /**
   * Check if a motion type is valid
   */
  isValidMotionType(motionType: string): boolean {
    return Object.values(MotionTypeEnum).includes(motionType as MotionType);
  }

  /**
   * Get motion type display name
   */
  getMotionTypeDisplayName(motionType: MotionType): string {
    const displayNames: Record<MotionType, string> = {
      [MotionTypeEnum.STATIC]: "Static",
      [MotionTypeEnum.PRO]: "Pro",
      [MotionTypeEnum.ANTI]: "Anti",
      [MotionTypeEnum.FLOAT]: "Float",
      [MotionTypeEnum.DASH]: "Dash",
    };

    return displayNames[motionType] || motionType;
  }

  /**
   * Get motion type description
   */
  getMotionTypeDescription(motionType: MotionType): string {
    const descriptions: Record<MotionType, string> = {
      [MotionTypeEnum.STATIC]: "Props remain stationary",
      [MotionTypeEnum.PRO]: "Props rotate in the same direction as the body",
      [MotionTypeEnum.ANTI]: "Props rotate opposite to the body direction",
      [MotionTypeEnum.FLOAT]: "Props float freely without rotation",
      [MotionTypeEnum.DASH]: "Props move in a dashing motion",
    };

    return descriptions[motionType] || "Unknown motion type";
  }
}
