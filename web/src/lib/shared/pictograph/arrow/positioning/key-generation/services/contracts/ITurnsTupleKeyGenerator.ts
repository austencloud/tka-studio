/**
 * Turns Tuple Key Generator Contract
 */

import type { PictographData } from "$shared";

export interface ITurnsTupleKeyGenerator {
  generateTurnsTuple(pictographData: PictographData): number[];
}
