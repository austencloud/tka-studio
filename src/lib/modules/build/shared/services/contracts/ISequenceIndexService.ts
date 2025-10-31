/**
 * Sequence Index Service Contract
 *
 * Interface for sequence indexing and search functionality.
 * Based on the existing ISequenceIndexService from browse/Explore.
 */

import type { SequenceData } from "$shared";

export interface ISequenceIndexService {
  // Core indexing operations
  buildIndex(sequences: SequenceData[]): Promise<void>;
  loadSequenceIndex(): Promise<SequenceData[]>;
  refreshIndex(): Promise<void>;

  // Search operations
  searchSequences(query: string): Promise<SequenceData[]>;
  getSequencesByTag(tag: string): Promise<SequenceData[]>;
  getSuggestions(partialQuery: string, maxSuggestions?: number): Promise<string[]>;

  // Index management
  updateIndex(sequence: SequenceData): Promise<void>;
  removeFromIndex(sequenceId: string): Promise<void>;

  // Utility operations
  getSequenceById(id: string): Promise<SequenceData | null>;
  getIndexStats(): {
    totalSequences: number;
    indexedWords: number;
    indexedAuthors: number;
    indexedTags: number;
    indexedMetadata: number;
  };
}
