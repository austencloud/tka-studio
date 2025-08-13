/**
 * Local Storage Persistence Service
 *
 * Handles data persistence using browser localStorage.
 * This provides a simple persistence layer for sequences and settings.
 */

import type { BeatData, SequenceData } from "$lib/domain";
import type { IPersistenceService } from "../interfaces";

export class LocalStoragePersistenceService implements IPersistenceService {
  private readonly SEQUENCES_KEY = "tka-v2-sequences";
  private readonly SEQUENCE_PREFIX = "tka-v2-sequence-";

  /**
   * Save a sequence to localStorage
   */
  async saveSequence(sequence: SequenceData): Promise<void> {
    try {
      // Save individual sequence
      const sequenceKey = `${this.SEQUENCE_PREFIX}${sequence.id}`;
      localStorage.setItem(sequenceKey, JSON.stringify(sequence));

      // Update sequence index
      await this.updateSequenceIndex(sequence);

      console.log(`Sequence "${sequence.name}" saved successfully`);
    } catch (error) {
      console.error("Failed to save sequence:", error);
      throw new Error(
        `Failed to save sequence: ${error instanceof Error ? error.message : "Unknown error"}`,
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
        const sequence = await this.loadSequence(id);
        if (sequence) {
          sequences.push(sequence);
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

      console.log(`Sequence ${id} deleted successfully`);
    } catch (error) {
      console.error(`Failed to delete sequence ${id}:`, error);
      throw new Error(
        `Failed to delete sequence: ${error instanceof Error ? error.message : "Unknown error"}`,
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
   * Validate sequence data structure
   */
  private validateSequenceData(raw: unknown): SequenceData {
    const data = (raw as Record<string, unknown>) || {};
    // Basic validation - ensure required fields exist
    if (
      typeof data.id !== "string" ||
      typeof data.name !== "string" ||
      !Array.isArray(data.beats)
    ) {
      throw new Error("Invalid sequence data structure");
    }

    // Ensure all required fields have defaults
    const nowIso = new Date().toISOString();
    const existingMeta = (data.metadata as Record<string, unknown>) || {};
    const metadata = {
      ...existingMeta,
      saved_at:
        typeof existingMeta.saved_at === "string"
          ? existingMeta.saved_at
          : nowIso,
      updated_at: nowIso,
    };
    const beatsArray = Array.isArray(data.beats)
      ? (data.beats as unknown[])
      : [];
    const beats: BeatData[] = beatsArray.filter((b): b is BeatData => {
      if (b == null || typeof b !== "object") return false;
      const candidate = b as Record<string, unknown>;
      return "beat_number" in candidate;
    });
    const result: SequenceData = {
      id: data.id as string,
      name: data.name as string,
      beats,
      word: (data.word as string) || "",
      thumbnails: (data.thumbnails as string[]) || [],
      is_favorite: Boolean(data.is_favorite),
      is_circular: Boolean(data.is_circular),
      tags: (data.tags as string[]) || [],
      metadata,
      // **CRITICAL: Include start_position field if it exists**
      ...(data.start_position
        ? { start_position: data.start_position as BeatData }
        : {}),
    };

    return result;
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
        if (key?.startsWith("tka-v2-")) {
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
}
