/**
 * Simple Filtering Models - Keep It Simple!
 *
 * Just the essential models for basic filtering.
 */

import type { ExploreFilterType } from "../enums/FilteringEnums";
import type { ExploreFilterValue } from "../types/FilteringTypes";

/**
 * Simple active filter - just type and value
 */
export interface ActiveFilter {
  type: ExploreFilterType;
  value: ExploreFilterValue;
  appliedAt: Date;
}

/**
 * Simple filter option for dropdowns
 */
export interface FilterOptionItem {
  label: string;
  value: ExploreFilterValue;
  count: number;
}
