/**
 * Explore Cache Service
 *
 * Simple in-memory cache for gallery sequences.
 * Prevents redundant loading and metadata extraction operations.
 */

import type { SequenceData } from "$shared";
import { injectable } from "inversify";
import type { IExploreCacheService } from "../contracts/IExploreCacheService";

@injectable()
export class ExploreCacheService implements IExploreCacheService {
  private cachedSequences: SequenceData[] | null = null;

  getCached(): SequenceData[] | null {
    return this.cachedSequences;
  }

  setCached(sequences: SequenceData[]): void {
    this.cachedSequences = sequences;
  }

  clearCache(): void {
    this.cachedSequences = null;
  }
}
