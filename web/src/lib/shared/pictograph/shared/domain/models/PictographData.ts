/**
 * Pictograph Domain Model
 *
 * Immutable data for a complete pictograph.
 * Based on modern desktop app's pictographData.py
 */
import { GridPosition, Letter } from "$shared";
import { MotionColor } from "../enums/pictograph-enums";
import type { MotionData } from "./MotionData";

export interface PictographData {
  readonly id: string;

  // Letter and position data
  readonly letter?: Letter | null;
  readonly startPosition?: GridPosition | null;
  readonly endPosition?: GridPosition | null;

  // Movement data
  readonly motions: Partial<Record<MotionColor, MotionData>>;
}
