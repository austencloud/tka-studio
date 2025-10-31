/**
 * Service for loading gallery sequences from various sources
 */

import type { SequenceData } from "$shared";

export interface IExploreLoader {
  /**
   * Load all sequence metadata from the sequence index
   */
  loadSequenceMetadata(): Promise<SequenceData[]>;
}
