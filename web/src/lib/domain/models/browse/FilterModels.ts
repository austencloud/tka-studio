/**
 * Browse Filter Models
 *
 * Interface definitions for browse filtering functionality.
 */

import type { FilterType, FilterValue } from "$domain";

export interface FilterConfig {
  type: FilterType;
  value: FilterValue;
  displayName: string;
}
