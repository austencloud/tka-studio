import type { SequenceData } from "$shared";

export interface ISequenceIndexService {
  loadSequenceIndex(): Promise<SequenceData[]>;
  buildSearchIndex(sequences: SequenceData[]): Promise<void>;
  searchSequences(query: string): Promise<SequenceData[]>;
  refreshIndex(): Promise<void>;
}
