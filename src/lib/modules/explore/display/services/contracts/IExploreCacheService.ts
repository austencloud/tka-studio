/**
 * Service for caching gallery sequences
 */

import type { SequenceData } from "$shared";

export interface IExploreCacheService {
  /**
   * Get cached sequences if available
   */
  getCached(): SequenceData[] | null;

  /**
   * Cache sequences
   */
  setCached(sequences: SequenceData[]): void;

  /**
   * Clear the cache
   */
  clearCache(): void;
}
