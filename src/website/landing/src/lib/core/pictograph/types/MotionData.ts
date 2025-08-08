/**
 * UI-Specific MotionData Interface
 *
 * This extends the core domain MotionData with UI-specific properties.
 * TODO: Migrate to use @tka/domain MotionData as base and extend it.
 */

import type { MotionData as CoreMotionData } from "@tka/domain";

export interface MotionData extends CoreMotionData {
  // UI-specific properties
  id: string;
  color: "red" | "blue";
  handRotDir: "cw_shift" | "ccw_shift" | "cw" | "ccw";
  leadState: "leading" | "trailing" | null;
  prefloatMotionType: string | null;
  prefloatPropRotDir: string | null;
}
