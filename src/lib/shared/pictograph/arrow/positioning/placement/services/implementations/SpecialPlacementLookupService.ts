/**
 * Special Placement Lookup Service
 *
 * Performs lookups in special placement data with fallback strategies.
 * Handles hybrid vs non-hybrid letter lookup logic.
 */

import { Point } from "fabric";
import { inject, injectable } from "inversify";
import { TYPES } from "../../../../../../inversify";
import type { MotionData, PictographData } from "$shared";
import type { ILetterClassificationService } from "../contracts/ILetterClassificationService";
import type { ISpecialPlacementLookupService } from "../contracts/ISpecialPlacementLookupService";

@injectable()
export class SpecialPlacementLookupService
  implements ISpecialPlacementLookupService
{
  constructor(
    @inject(TYPES.ILetterClassificationService)
    private readonly letterClassificationService: ILetterClassificationService
  ) {}

  /**
   * Look up special placement adjustment from placement data.
   * Applies fallback strategies based on letter type (hybrid vs non-hybrid).
   */
  lookupAdjustment(
    letterData: Record<string, unknown>,
    turnsTuple: string,
    motionData: MotionData,
    pictographData: PictographData,
    arrowColor?: string,
    attributeKey?: string
  ): Point | null {
    if (!letterData) {
      return null;
    }

    // Handle nested structure like legacy system does
    // For G letter: letterData = { G: { "(0, 0)": { "red": [0, -130] } } }
    const letter = pictographData.letter || "";
    const actualLetterData =
      (letterData[letter] as Record<string, unknown>) || letterData;

    // Get turn-specific data
    const turnData = actualLetterData[turnsTuple] as
      | Record<string, unknown>
      | undefined;

    if (!turnData) {
      return null;
    }

    // Use attribute key if provided (preferred method)
    if (attributeKey && attributeKey in turnData) {
      const adjustmentValues = turnData[attributeKey];
      if (Array.isArray(adjustmentValues) && adjustmentValues.length === 2) {
        return new Point(adjustmentValues[0], adjustmentValues[1]);
      }
    }

    // FALLBACK LOGIC (when attributeKey not provided or not found)
    return this.applyFallbackStrategy(
      turnData,
      motionData,
      pictographData,
      arrowColor
    );
  }

  /**
   * Look up rotation angle override flag from placement data.
   */
  lookupRotationOverride(
    letterData: Record<string, unknown>,
    turnsTuple: string,
    rotationOverrideKey: string
  ): boolean {
    if (!letterData) {
      return false;
    }

    // Handle nested structure
    const letter = Object.keys(letterData)[0] || "";
    const actualLetterData =
      (letterData[letter] as Record<string, unknown>) || letterData;

    // Get turn-specific data
    const turnData = actualLetterData[turnsTuple] as
      | Record<string, unknown>
      | undefined;

    if (!turnData) {
      return false;
    }

    // Check if rotation override flag exists and is true
    const overrideFlag = turnData[rotationOverrideKey];
    return overrideFlag === true;
  }

  /**
   * Apply fallback lookup strategies based on letter type
   */
  private applyFallbackStrategy(
    turnData: Record<string, unknown>,
    motionData: MotionData,
    pictographData: PictographData,
    arrowColor?: string
  ): Point | null {
    const isHybridLetter = this.letterClassificationService.isHybridLetter(
      pictographData.letter || ""
    );
    const startsFromStandardOrientation =
      this.letterClassificationService.startsFromStandardOrientation(
        pictographData
      );

    // For HYBRID letters with standard orientation, use motion type as PRIMARY key
    if (isHybridLetter && startsFromStandardOrientation) {
      const result = this.lookupByMotionType(turnData, motionData);
      if (result) {
        return result;
      }
    } else {
      // For NON-HYBRID letters, try color-based lookup first
      const colorResult = this.lookupByColor(
        turnData,
        motionData,
        pictographData,
        arrowColor
      );
      if (colorResult) {
        return colorResult;
      }

      // Fallback: try motion-type-specific adjustment for NON-HYBRID letters
      const motionTypeResult = this.lookupByMotionType(turnData, motionData);
      if (motionTypeResult) {
        return motionTypeResult;
      }
    }

    return null;
  }

  /**
   * Look up adjustment by motion type key
   */
  private lookupByMotionType(
    turnData: Record<string, unknown>,
    motionData: MotionData
  ): Point | null {
    const motionTypeKey = motionData.motionType.toLowerCase() || "";

    if (motionTypeKey in turnData) {
      const adjustmentValues = turnData[motionTypeKey];
      if (Array.isArray(adjustmentValues) && adjustmentValues.length === 2) {
        return new Point(adjustmentValues[0], adjustmentValues[1]);
      }
    }

    return null;
  }

  /**
   * Look up adjustment by arrow color
   */
  private lookupByColor(
    turnData: Record<string, unknown>,
    motionData: MotionData,
    pictographData: PictographData,
    arrowColor?: string
  ): Point | null {
    let colorKey = "";

    if (arrowColor) {
      // Use provided arrow color directly
      colorKey = arrowColor;
    } else if (
      pictographData.motions.blue &&
      pictographData.motions.blue === motionData
    ) {
      colorKey = "blue";
    } else if (
      pictographData.motions.red &&
      pictographData.motions.red === motionData
    ) {
      colorKey = "red";
    } else {
      // Fallback: try to determine from motion data
      colorKey = "blue"; // Default fallback
    }

    if (colorKey in turnData) {
      const adjustmentValues = turnData[colorKey];
      if (Array.isArray(adjustmentValues) && adjustmentValues.length === 2) {
        return new Point(adjustmentValues[0], adjustmentValues[1]);
      }
    }

    return null;
  }
}
