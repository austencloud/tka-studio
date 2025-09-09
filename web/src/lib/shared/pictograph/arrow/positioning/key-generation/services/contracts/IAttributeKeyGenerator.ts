/**
 * Attribute Key Generator Contract
 */

import type { ArrowPlacementData, PictographData } from "$shared";

export interface IAttributeKeyGenerator {
  getKeyFromArrow(
    arrowData: ArrowPlacementData,
    pictographData: PictographData,
    color: string
  ): string;
}
