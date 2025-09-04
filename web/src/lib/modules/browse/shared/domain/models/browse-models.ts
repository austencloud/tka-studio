import type { SequenceData } from "$shared/domain";

export interface BrowseDeleteConfirmationData {
  sequence: SequenceData;
  relatedSequences: SequenceData[];
  hasVariations: boolean;
  willFixVariationNumbers: boolean;
}

export interface BrowseDeleteResult {
  success: boolean;
  deletedSequence: SequenceData | null;
  affectedSequences: SequenceData[];
  error?: string;
}
