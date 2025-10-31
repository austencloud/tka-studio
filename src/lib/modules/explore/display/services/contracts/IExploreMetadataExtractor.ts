/**
 * Service for extracting metadata from sequence files
 */

import type { BeatData } from "$shared";
import type { GridMode } from "$shared/pictograph/grid/domain/enums/grid-enums";
import type { PropType } from "$shared/pictograph/prop/domain/enums/PropType";

export interface SequenceMetadata {
  beats: BeatData[];
  author: string;
  difficultyLevel: string;
  dateAdded: Date;
  gridMode: GridMode;
  isCircular: boolean;
  propType: PropType;
  sequenceLength: number;
  startingPosition: string;
}

export interface IExploreMetadataExtractor {
  /**
   * Extract metadata from a sequence file (PNG, WebP, or JSON sidecar)
   */
  extractMetadata(
    sequenceName: string,
    thumbnailPath?: string
  ): Promise<SequenceMetadata>;
}
