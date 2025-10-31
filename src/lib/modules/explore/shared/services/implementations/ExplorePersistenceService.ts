/**
 * Local Storage Persistence Service
 *
 * Handles data persistence using browser localStorage.
 * This provides a simple persistence layer for sequences and settings.
 */

import type {
  BeatData,
  GridPosition,
  Letter,
  MotionData,
  PictographData,
  SequenceData,
} from "$shared";
import { safeParseOrNull, SequenceDataSchema } from "$shared";
import { injectable } from "inversify";
import type { IPersistenceService } from "../../../../build/shared/services/contracts";

// TODO: Figure out why this is importing the persistence service meant for the workbench - that doesn'tmake sense. fix this, augment!
@injectable()
export class ExplorePersistenceService implements IPersistenceService {
  private readonly CACHE_VERSION = "v2.1"; // ✅ ROBUST: Cache versioning
  private readonly SEQUENCES_KEY = `tka-${this.CACHE_VERSION}-sequences`;
  private readonly SEQUENCE_PREFIX = `tka-${this.CACHE_VERSION}-sequence-`;

  /**
   * Normalize beats array to ensure all required properties are present
   */
  private normalizeBeats(beats: unknown[]): BeatData[] {
    return beats.map((beat: unknown, index: number) => {
      const beatData = beat as Record<string, unknown>;

      // Handle both old format (with pictographData) and new unified format
      const pictographData = beatData as unknown as PictographData;

      return {
        // Core beat properties
        id: (beatData.id as string) || crypto.randomUUID(),
        beatNumber: (beatData.beatNumber as number) ?? index + 1,
        duration: (beatData.duration as number) || 1,
        blueReversal: (beatData.blueReversal as boolean) || false,
        redReversal: (beatData.redReversal as boolean) || false,
        isBlank: (beatData.isBlank as boolean) || false,

        // Pictograph properties (from old pictographData or directly from beat)
        letter: pictographData?.letter || (beatData.letter as Letter) || null,
        startPosition:
          pictographData?.startPosition ||
          (beatData.startPosition as GridPosition) ||
          null,
        endPosition:
          pictographData?.endPosition ||
          (beatData.endPosition as GridPosition) ||
          null,
        motions:
          pictographData?.motions ||
          (beatData.motions as Record<string, MotionData>) ||
          {},
      };
    });
  }

  /**
   * Normalize a single beat to ensure all required properties are present
   */
  private normalizeBeat(beat: unknown): BeatData | undefined {
    if (!beat) return undefined;
    const beatData = beat as Record<string, unknown>;

    // Handle both old format (with pictographData) and new unified format
    const pictographData = beatData as unknown as PictographData;

    return {
      // Core beat properties
      id: (beatData.id as string) || crypto.randomUUID(),
      beatNumber: (beatData.beatNumber as number) || 1,
      duration: (beatData.duration as number) || 1,
      blueReversal: (beatData.blueReversal as boolean) || false,
      redReversal: (beatData.redReversal as boolean) || false,
      isBlank: (beatData.isBlank as boolean) || false,

      // Pictograph properties (from old pictographData or directly from beat)
      letter: pictographData?.letter || (beatData.letter as Letter) || null,
      startPosition:
        pictographData?.startPosition ||
        (beatData.startPosition as GridPosition) ||
        null,
      endPosition:
        pictographData?.endPosition ||
        (beatData.endPosition as GridPosition) ||
        null,
      motions:
        pictographData?.motions ||
        (beatData.motions as Record<string, MotionData>) ||
        {},
    };
  }

  /**
   * Normalize a sequence to ensure all required properties are present
   */
  private normalizeSequence(sequence: unknown): SequenceData {
    const sequenceData = sequence as Record<string, unknown>;
    return {
      ...(sequenceData as object),
      id: (sequenceData.id as string) || crypto.randomUUID(),
      name:
        (sequenceData.name as string) || (sequenceData.word as string) || "",
      word: (sequenceData.word as string) || "",
      beats: this.normalizeBeats((sequenceData.beats as unknown[]) || []),
      startingPositionBeat: this.normalizeBeat(
        sequenceData.startingPositionBeat
      ),
      startPosition: this.normalizeBeat(sequenceData.startPosition),
      thumbnails: (sequenceData.thumbnails as string[]) || [],
      tags: (sequenceData.tags as string[]) || [],
      isFavorite: (sequenceData.isFavorite as boolean) || false,
      isCircular: (sequenceData.isCircular as boolean) || false,
      metadata: (sequenceData.metadata as Record<string, unknown>) || {},
    };
  }

  /**
   * Validate sequence data before storage operations
   */
  private isValidSequence(sequence: SequenceData): boolean {
    // ✅ PERMANENT: Validate sequence names to prevent malformed data
    const name = sequence.name || sequence.word || sequence.id || "";

    return (
      name.length > 0 &&
      name.length <= 100 && // Reasonable name length limit
      !name.includes("__") && // No double underscores
      !name.includes("test") // No test sequences
    );
  }

  /**
   * Save a sequence to localStorage
   */
  async saveSequence(sequence: SequenceData): Promise<void> {
    try {
      // ✅ PERMANENT: Validate before saving
      if (!this.isValidSequence(sequence)) {
        console.warn(
          `Skipping invalid sequence: ${sequence.name || sequence.id}`
        );
        return;
      }

      // ✅ CRITICAL: Validate with Zod schema before saving to prevent invalid data
      const validationResult = safeParseOrNull(
        SequenceDataSchema,
        sequence,
        `sequence ${sequence.id} before save`
      );

      if (!validationResult) {
        console.warn(
          `Sequence ${sequence.id} failed schema validation, skipping save`
        );
        return;
      }

      // Normalize the sequence to ensure all required fields are present
      const normalizedSequence = this.normalizeSequence(validationResult);

      // Save individual sequence
      const sequenceKey = `${this.SEQUENCE_PREFIX}${sequence.id}`;
      localStorage.setItem(sequenceKey, JSON.stringify(normalizedSequence));

      // Update sequence index
      await this.updateSequenceIndex(normalizedSequence);
    } catch (error) {
      console.error("Failed to save sequence:", error);
      throw new Error(
        `Failed to save sequence: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Load a sequence by ID
   */
  async loadSequence(id: string): Promise<SequenceData | null> {
    try {
      const sequenceKey = `${this.SEQUENCE_PREFIX}${id}`;
      const data = localStorage.getItem(sequenceKey);

      if (!data) {
        return null;
      }

      const sequence = JSON.parse(data) as SequenceData;
      return this.validateSequenceData(sequence);
    } catch (error) {
      console.error(`Failed to load sequence ${id}:`, error);
      return null;
    }
  }

  /**
   * Load all sequences
   */
  async loadAllSequences(): Promise<SequenceData[]> {
    try {
      const indexData = localStorage.getItem(this.SEQUENCES_KEY);
      if (!indexData) {
        return [];
      }

      const sequenceIds = JSON.parse(indexData) as string[];
      const sequences: SequenceData[] = [];

      for (const id of sequenceIds) {
        const sequenceKey = `${this.SEQUENCE_PREFIX}${id}`;
        const rawData = localStorage.getItem(sequenceKey);

        if (rawData) {
          try {
            const parsedData = JSON.parse(rawData);
            const validatedSequence = safeParseOrNull(
              SequenceDataSchema,
              parsedData,
              `sequence ${id}`
            );

            if (validatedSequence) {
              const normalizedSequence =
                this.normalizeSequence(validatedSequence);
              if (this.isValidSequence(normalizedSequence)) {
                sequences.push(normalizedSequence);
              }
            }
          } catch (error) {
            console.warn(`Skipping corrupted sequence ${id}:`, error);
          }
        }
      }

      return sequences.sort((a, b) => {
        // Sort by stored timestamp in metadata if available
        const aDate = new Date((a.metadata?.saved_at as string) || 0).getTime();
        const bDate = new Date((b.metadata?.saved_at as string) || 0).getTime();
        return bDate - aDate;
      });
    } catch (error) {
      console.error("Failed to load sequences:", error);
      return [];
    }
  }

  /**
   * Delete a sequence
   */
  async deleteSequence(id: string): Promise<void> {
    try {
      // Remove individual sequence
      const sequenceKey = `${this.SEQUENCE_PREFIX}${id}`;
      localStorage.removeItem(sequenceKey);

      // Update sequence index
      await this.removeFromSequenceIndex(id);
    } catch (error) {
      console.error(`Failed to delete sequence ${id}:`, error);
      throw new Error(
        `Failed to delete sequence: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Update the sequence index with a new or updated sequence
   */
  private async updateSequenceIndex(sequence: SequenceData): Promise<void> {
    try {
      const indexData = localStorage.getItem(this.SEQUENCES_KEY);
      const sequenceIds = indexData ? (JSON.parse(indexData) as string[]) : [];

      // Add sequence ID if not already present
      if (!sequenceIds.includes(sequence.id)) {
        sequenceIds.push(sequence.id);
        localStorage.setItem(this.SEQUENCES_KEY, JSON.stringify(sequenceIds));
      }
    } catch (error) {
      console.error("Failed to update sequence index:", error);
    }
  }

  /**
   * Remove a sequence ID from the index
   */
  private async removeFromSequenceIndex(id: string): Promise<void> {
    try {
      const indexData = localStorage.getItem(this.SEQUENCES_KEY);
      if (!indexData) return;

      const sequenceIds = JSON.parse(indexData) as string[];
      const filteredIds = sequenceIds.filter((existingId) => existingId !== id);

      localStorage.setItem(this.SEQUENCES_KEY, JSON.stringify(filteredIds));
    } catch (error) {
      console.error("Failed to remove from sequence index:", error);
    }
  }

  /**
   * Validate sequence data using Zod schema - replaces 50+ lines of manual validation
   */
  private validateSequenceData(raw: unknown): SequenceData {
    // Use safe parsing to handle corrupted localStorage data gracefully
    const validatedSequence = safeParseOrNull(
      SequenceDataSchema,
      raw,
      "localStorage sequence data"
    );

    if (validatedSequence) {
      // Ensure metadata has persistence timestamps
      const nowIso = new Date().toISOString();
      const existingMetadata: Record<string, unknown> =
        (validatedSequence.metadata as Record<string, unknown>) || {};
      const metadata: Record<string, unknown> = {
        ...existingMetadata,
        saved_at: (existingMetadata.saved_at as string) || nowIso,
        updated_at: nowIso,
      };

      return this.normalizeSequence({
        ...validatedSequence,
        metadata,
      });
    } else {
      throw new Error(
        "Invalid sequence data structure - failed Zod validation"
      );
    }
  }

  /**
   * Get storage usage statistics
   */
  getStorageInfo(): { used: number; available: number; sequences: number } {
    try {
      // Calculate used storage (rough estimate)
      let used = 0;
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key?.startsWith(`tka-${this.CACHE_VERSION}-`)) {
          // ✅ ROBUST: Only count current version storage
          const value = localStorage.getItem(key);
          used += (key.length + (value?.length || 0)) * 2; // UTF-16 encoding
        }
      }

      // Get sequence count
      const indexData = localStorage.getItem(this.SEQUENCES_KEY);
      const sequenceCount = indexData ? JSON.parse(indexData).length : 0;

      return {
        used: Math.round(used / 1024), // KB
        available: 5120, // Rough estimate of 5MB localStorage limit
        sequences: sequenceCount,
      };
    } catch {
      return { used: 0, available: 5120, sequences: 0 };
    }
  }

  /**
   * Clear old cached data and malformed sequences
   */
  async clearLegacyCache(): Promise<void> {
    try {
      // Keys to preserve (don't remove these important state keys)
      const preserveKeys = [
        "tka-app-tab-state-v2",
        "tka-modern-web-settings",
        "tka-browse-state-v2",
        "tka-browse-filter-v2",
        "tka-browse-sort-v2",
        "tka-browse-view-v2",
        "tka-browse-scroll-v2",
        "tka-browse-selection-v2",
      ];

      // Clear all old TKA storage keys except preserved ones
      const keysToRemove: string[] = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (
          key?.startsWith("tka-") &&
          !key.startsWith(`tka-${this.CACHE_VERSION}-`) &&
          !preserveKeys.includes(key)
        ) {
          keysToRemove.push(key);
        }
      }

      // Remove old keys
      keysToRemove.forEach((key) => {
        localStorage.removeItem(key);
      });

      // Clear session storage as well
      const sessionKeysToRemove: string[] = [];
      for (let i = 0; i < sessionStorage.length; i++) {
        const key = sessionStorage.key(i);
        if (key?.startsWith("tka-")) {
          sessionKeysToRemove.push(key);
        }
      }

      sessionKeysToRemove.forEach((key) => {
        sessionStorage.removeItem(key);
      });
    } catch (error) {
      console.error("Failed to clear legacy cache:", error);
    }
  }
}
