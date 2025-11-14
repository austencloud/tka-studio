/**
 * Explore Loader Service
 *
 * Orchestrates loading of gallery sequences from the sequence index.
 * Handles validation, metadata extraction, and data normalization.
 */

import {
  createSequenceData,
  GridPositionGroup,
  type SequenceData,
} from "$shared";
import { TYPES } from "$shared/inversify/types";
import { GridMode } from "$shared/pictograph/grid/domain/enums/grid-enums";
import { PropType } from "$shared/pictograph/prop/domain/enums/PropType";
import { inject, injectable } from "inversify";
import type { IExploreLoader } from "../contracts/IExploreLoader";
import type { IExploreMetadataExtractor } from "../contracts/IExploreMetadataExtractor";

// Constants for validation
const MAX_WORD_LENGTH = 200;
const SEQUENCE_INDEX_URL = "/sequence-index.json";

interface RawSequenceData {
  word?: string;
  name?: string;
  id?: string;
  thumbnails?: unknown;
  isFavorite?: unknown;
  isCircular?: unknown;
  tags?: unknown;
  metadata?: unknown;
  author?: string;
  gridMode?: unknown;
  difficultyLevel?: unknown;
  sequenceLength?: unknown;
  level?: unknown;
  dateAdded?: unknown;
  propType?: unknown;
  startingPosition?: unknown;
}

@injectable()
export class ExploreLoader implements IExploreLoader {
  constructor(
    @inject(TYPES.IExploreMetadataExtractor)
    private metadataExtractor: IExploreMetadataExtractor
  ) {}

  async loadSequenceMetadata(): Promise<SequenceData[]> {
    try {
      const rawSequences = await this.fetchSequenceIndex();
      const validSequences = await this.processRawSequences(rawSequences);
      return validSequences;
    } catch (error) {
      console.error("❌ Failed to load sequence metadata:", error);
      throw error;
    }
  }

  // ============================================================================
  // Data Loading
  // ============================================================================

  private async fetchSequenceIndex(): Promise<RawSequenceData[]> {
    // Add cache-busting parameter to force fresh load after difficulty calculator changes
    const cacheBuster = Date.now();
    const url = `${SEQUENCE_INDEX_URL}?v=${cacheBuster}`;

    const response = await fetch(url, {
      cache: 'no-store', // Prevent browser caching
    });

    if (!response.ok) {
      throw new Error(`Failed to load sequence index: ${response.status}`);
    }

    const data = await response.json();
    return data.sequences || [];
  }

  // ============================================================================
  // Data Processing
  // ============================================================================

  private async processRawSequences(
    rawSequences: RawSequenceData[]
  ): Promise<SequenceData[]> {
    const sequences: SequenceData[] = [];

    for (const rawSeq of rawSequences) {
      const word = this.extractWord(rawSeq);

      if (!this.isValidWord(word)) {
        console.warn(`🚫 Skipping invalid sequence: ${word}`);
        continue;
      }

      try {
        const sequence = await this.createSequenceFromRaw(rawSeq, word);
        sequences.push(sequence);
      } catch (error) {
        const shouldLog = !this.isRoutineError(error);
        if (shouldLog) {
          console.warn(`⚠️ Failed to process ${word}:`, error);
        }

        // Use fallback sequence creation
        const fallbackSequence = this.createFallbackSequence(rawSeq, word);
        sequences.push(fallbackSequence);
      }
    }

    return sequences;
  }

  // ============================================================================
  // Sequence Creation
  // ============================================================================

  private async createSequenceFromRaw(
    rawSeq: RawSequenceData,
    word: string
  ): Promise<SequenceData> {
    const thumbnailPath = this.extractThumbnailPath(rawSeq);
    const metadata = await this.metadataExtractor.extractMetadata(
      word,
      thumbnailPath
    );

    const gridMode = this.parseGridMode(rawSeq.gridMode) || metadata.gridMode;
    const dateAdded = this.parseDate(rawSeq.dateAdded) || metadata.dateAdded;

    // Get difficulty from metadata (calculated by difficulty calculator)
    const difficultyLevel =
      metadata.difficultyLevel || this.parseDifficulty(rawSeq.difficultyLevel);

    // Calculate numeric level from difficulty string (instead of using old stored value)
    const calculatedLevel = this.difficultyStringToLevel(difficultyLevel);

    return createSequenceData({
      id: word,
      name: this.cleanSequenceName(String(rawSeq.name || word || "Unnamed Sequence")),
      word,
      beats: metadata.beats,
      thumbnails: this.parseThumbnails(rawSeq.thumbnails),
      isFavorite: Boolean(rawSeq.isFavorite),
      isCircular: Boolean(metadata.isCircular ?? rawSeq.isCircular),
      tags: this.parseTags(rawSeq.tags),
      metadata: this.parseMetadata(rawSeq.metadata),
      author: metadata.author || String(rawSeq.author || "Unknown"),
      gridMode,
      difficultyLevel,
      sequenceLength: metadata.sequenceLength,
      level: calculatedLevel, // Use calculated level instead of old stored value
      dateAdded,
      propType: (metadata.propType || rawSeq.propType || "Staff") as PropType,
      startingPositionGroup: (metadata.startingPosition ||
        rawSeq.startingPosition ||
        "alpha") as GridPositionGroup,
    });
  }

  private createFallbackSequence(
    rawSeq: RawSequenceData,
    word: string
  ): SequenceData {
    const gridMode = this.parseGridMode(rawSeq.gridMode) || GridMode.BOX;
    const dateAdded = this.parseDate(rawSeq.dateAdded) || new Date();

    // Get difficulty and calculate numeric level
    const difficultyLevel = this.parseDifficulty(rawSeq.difficultyLevel);
    const calculatedLevel = this.difficultyStringToLevel(difficultyLevel);

    return createSequenceData({
      id: word,
      name: this.cleanSequenceName(String(rawSeq.name || word || "Unnamed Sequence")),
      word,
      beats: [],
      thumbnails: this.parseThumbnails(rawSeq.thumbnails),
      isFavorite: Boolean(rawSeq.isFavorite),
      isCircular: Boolean(rawSeq.isCircular),
      tags: this.parseTags(rawSeq.tags),
      metadata: this.parseMetadata(rawSeq.metadata),
      author: String(rawSeq.author || "Unknown"),
      gridMode,
      difficultyLevel,
      sequenceLength: this.parseSequenceLength(rawSeq.sequenceLength),
      level: calculatedLevel, // Use calculated level instead of old stored value
      dateAdded,
      propType: (rawSeq.propType || "Staff") as PropType,
      startingPositionGroup: (rawSeq.startingPosition ||
        "alpha") as GridPositionGroup,
    });
  }

  // ============================================================================
  // Validation
  // ============================================================================

  private extractWord(rawSeq: RawSequenceData): string {
    return rawSeq.word || rawSeq.name || rawSeq.id || "";
  }

  private isValidWord(word: string): boolean {
    return (
      word.length > 0 &&
      word.length <= MAX_WORD_LENGTH &&
      !word.toLowerCase().includes("test")
    );
  }

  private isRoutineError(error: unknown): boolean {
    const errorMessage = error instanceof Error ? error.message : String(error);
    return errorMessage.includes("No valid version found");
  }

  // ============================================================================
  // Data Parsing Helpers
  // ============================================================================

  private extractThumbnailPath(rawSeq: RawSequenceData): string | undefined {
    const thumbnails = this.parseThumbnails(rawSeq.thumbnails);
    return thumbnails[0];
  }

  private parseThumbnails(value: unknown): string[] {
    return Array.isArray(value) ? (value as string[]) : [];
  }

  private parseTags(value: unknown): string[] {
    return Array.isArray(value) ? (value as string[]) : ["flow", "practice"];
  }

  private parseMetadata(value: unknown): Record<string, unknown> {
    return typeof value === "object" && value !== null
      ? (value as Record<string, unknown>)
      : { source: "tka_dictionary" };
  }

  private parseGridMode(value: unknown): GridMode | null {
    if (!value) return null;

    if (typeof value === "string") {
      const normalized = value.toLowerCase();
      if (normalized === "gridmode.diamond" || normalized === "diamond") {
        return GridMode.DIAMOND;
      }
      if (normalized === "gridmode.box" || normalized === "box") {
        return GridMode.BOX;
      }
    }

    return value as GridMode;
  }

  private parseDifficulty(value: unknown): string {
    return typeof value === "string" ? value : "beginner";
  }

  private parseSequenceLength(value: unknown): number {
    return typeof value === "number" ? value : 0;
  }

  /**
   * Convert difficulty string to numeric level for SequenceCard styling
   * This ensures the card uses the NEW calculated difficulty, not old stored values
   */
  private difficultyStringToLevel(difficulty: string): number {
    const normalized = difficulty.toLowerCase();
    switch (normalized) {
      case "beginner":
        return 1;
      case "intermediate":
        return 2;
      case "advanced":
        return 3;
      case "mythic":
        return 4;
      case "legendary":
        return 5;
      default:
        return 1; // Default to beginner
    }
  }

  private parseDate(value: unknown): Date | null {
    if (!value) return null;

    if (value instanceof Date) {
      return value;
    }

    if (typeof value === "string") {
      const date = new Date(value);
      return isNaN(date.getTime()) ? null : date;
    }

    return null;
  }

  /**
   * Remove " Sequence" suffix from sequence names
   */
  private cleanSequenceName(name: string): string {
    return name.replace(/\s+Sequence$/i, "");
  }
}
