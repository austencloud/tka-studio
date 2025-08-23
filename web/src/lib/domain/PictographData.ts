/**
 * Pictograph Domain Model
 *
 * Immutable data for a complete pictograph.
 * Based on modern desktop app's pictographData.py
 */

import { Letter } from "./Letter";
import type { MotionData } from "./MotionData";
import { MotionColor } from "./enums";

export interface PictographData {
  readonly id: string;
  readonly motions: Partial<Record<MotionColor, MotionData>>;
  readonly letter?: Letter | null;
  readonly isBlank: boolean;
  readonly metadata: Record<string, unknown>;
}

export function createPictographData(
  data: Partial<PictographData> = {}
): PictographData {
  return {
    id: data.id || crypto.randomUUID(),
    motions: data.motions || {},
    letter: data.letter || null,
    isBlank: data.isBlank ?? false,
    metadata: data.metadata || {},
  };
}
