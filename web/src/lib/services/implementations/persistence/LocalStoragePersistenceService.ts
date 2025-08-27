/**
 * Local Storage Persistence Service
 *
 * Handles data persistence using browser localStorage.
 * This provides a simple persistence layer for sequences and settings.
 */

import type { BeatData, SequenceData } from "$lib/domain";
import { SequenceDataSchema } from "$lib/domain/schemas";
import { safeParseOrNull } from "$lib/utils/validation";
import { injectable } from "inversify";
import type { IPersistenceService } from "../../interfaces/sequence-interfaces";

@injectable()
export class LocalStoragePersistenceService implements IPersistenceService {
  private readonly CACHE_VERSION = "v2.1"; // ✅ ROBUST: Cache versioning
  private readonly SEQUENCES_KEY = `tka-${this.CACHE_VERSION}-sequences`;
  private readonly SEQUENCE_PREFIX = `tka-${this.CACHE_VERSION}-sequence-`;

  /**
   * Normalize beats array to ensure all required properties are present
   */
  private normalizeBeats(beats: unknown[]): BeatData[] {
    return beats.map((beat: any) => ({
      ...beat,
      id: beat.id || crypto.randomUUID(),
      duration: beat.duration || 1,
      blueReversal: beat.blueReversal || false,
      redReversal: beat.redReversal || false,
      isBlank: beat.isBlank || false,
    }));
  }

  /**
   * Normalize a single beat to ensure all required properties are present
   */
  private normalizeBeat(beat: any): BeatData | undefined {
    if (!beat) return undefined;
    return {
      ...beat,
      id: beat.id || crypto.randomUUID(),
      duration: beat.duration || 1,
      blueReversal: beat.blueReversal || false,
      redReversal: beat.redReversal || false,
      isBlank: beat.isBlank || false,
    };
  }

  /**
   * Normalize a sequence to ensure all required properties are present
   */
  private normalizeSequence(sequence: any): SequenceData {
    return {
      ...sequence,
      id: sequence.id || crypto.randomUUID(),
      word: sequence.word || "",
      beats: this.normalizeBeats(sequence.beats || []),
      startingPositionBeat: this.normalizeBeat(sequence.startingPositionBeat),
      startPosition: this.normalizeBeat(sequence.startPosition),
      thumbnails: sequence.thumbnails || [],
      tags: sequence.tags || [],
      isFavorite: sequence.isFavorite || false,
      isCircular: sequence.isCircular || false,
      metadata: sequence.metadata || {},
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
        return;
      }

      // Save individual sequence
      const sequenceKey = `${this.SEQUENCE_PREFIX}${sequence.id}`;
      localStorage.setItem(sequenceKey, JSON.stringify(sequence));

      // Update sequence index
      await this.updateSequenceIndex(sequence);
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
      const metadata = {
        ...validatedSequence.metadata,
        saved_at: (validatedSequence.metadata?.saved_at as string) || nowIso,
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
