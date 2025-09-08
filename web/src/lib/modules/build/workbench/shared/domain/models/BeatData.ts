/**
 * Beat Domain Model - Shared
 *
 * Core beat data structure used across build and animator modules.
 */

import type { PictographData } from "../../../../../../shared/pictograph/shared/domain/models/PictographData";

export interface BeatData {
  readonly id: string;
  readonly beatNumber: number;
  readonly duration: number;
  readonly blueReversal: boolean;
  readonly redReversal: boolean;
  readonly isBlank: boolean;
  readonly pictographData: PictographData | null;
}

