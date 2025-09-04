/**
 * Pictograph Domain Model
 *
 * Immutable data for a complete pictograph.
 * Based on modern desktop app's pictographData.py
 */
import { GridPosition, Letter, MotionColor } from "../../enums";
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

export function createPictographData(
  data: Partial<PictographData> = {}
): PictographData {
  return {
    id: data.id || crypto.randomUUID(),
    motions: data.motions || {},
    letter: data.letter || null,
    startPosition: data.startPosition ?? null,
    endPosition: data.endPosition ?? null,
  };
}
