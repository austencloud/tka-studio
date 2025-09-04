/**
 * Browse Service Implementation
 *
 * Handles loading, filtering, and sorting of sequence metadata for the browse tab.
 * Ported and adapted from desktop app's GalleryService.
 */

import type { GalleryFilterValue } from "$shared/domain";
import {
  createSequenceData,
  FilterType,
  GallerySortMethod,
  GridMode,
  GridPositionGroup,
  PropType,
  type SequenceData,
} from "$shared/domain";
import { injectable } from "inversify";
import type { IGalleryService } from "../contracts";

@injectable()
export class GalleryService implements IGalleryService {
  private cachedSequences: SequenceData[] | null = null;

  /**
   * ✅ PERMANENT: Validate sequence metadata to prevent malformed data
   */
  private isValidSequenceMetadata(sequence: SequenceData): boolean {
    const word = sequence.word || sequence.name || sequence.id || "";

    // Basic validation for real dictionary sequences
    return (
      word.length > 0 &&
      word.length <= 200 && // Increased limit for complex sequences
      !word.toLowerCase().includes("test") // No test sequences
    );
  }

  async loadSequenceMetadata(): Promise<SequenceData[]> {
    console.log("🔍 GalleryService.loadSequenceMetadata() called");

    if (this.cachedSequences !== null) {
      console.log(
        "📦 Returning cached sequences:",
        this.cachedSequences.length,
        "items"
      );
      return this.cachedSequences;
    }

    try {
      // Try to load from sequence index first
      console.log("🔄 Loading from sequence index...");
      const sequences = await this.loadFromSequenceIndex();
      console.log(
        "✅ Successfully loaded from sequence index:",
        sequences.length,
        "sequences"
      );
      console.log(
        "📋 Sequence words:",
        `(${sequences.length})`,
        sequences.map((s) => s.word)
      );
      console.log(
        "🔑 Sequence IDs (first 10):",
        sequences.slice(0, 10).map((s) => s.id)
      );

      // ✅ PERMANENT: Filter out invalid sequences
      const validSequences = sequences.filter((seq) => {
        const isValid = this.isValidSequenceMetadata(seq);
        if (!isValid) {
          console.warn(
            `Filtered out invalid sequence: ${seq.word || seq.name || seq.id}`
          );
        }
        return isValid;
      });

      console.log(
        `🔍 Filtered ${sequences.length - validSequences.length} invalid sequences`
      );

      this.cachedSequences = validSequences;
      return validSequences;
    } catch (error) {
      console.warn(
        "❌ Failed to load sequence index, generating from dictionary:",
        error
      );
      // Fallback to scanning dictionary folders
      const sequences = await this.generateSequenceIndex();
      console.log(
        "🔧 Generated sequences as fallback:",
        sequences.length,
        "sequences"
      );
      this.cachedSequences = sequences;
      return sequences;
    }
  }

  async applyFilter(
    sequences: SequenceData[],
    filterType: FilterType,
    filterValue: GalleryFilterValue
  ): Promise<SequenceData[]> {
    console.log("🔍 GalleryService.applyFilter() called with:");
    console.log("  - filterType:", filterType);
    console.log("  - filterValue:", filterValue);
    console.log("  - input sequences:", sequences.length, "items");

    if (filterType === FilterType.ALL_SEQUENCES) {
      console.log(
        "✅ ALL_SEQUENCES filter detected - returning all sequences:",
        sequences.length
      );
      return sequences;
    }

    console.log("🔄 Applying specific filter...");
    let filtered: SequenceData[];

    switch (filterType) {
      case FilterType.STARTING_LETTER:
        filtered = this.filterByStartingLetter(sequences, filterValue);
        break;
      case FilterType.CONTAINS_LETTERS:
        filtered = this.filterByContainsLetters(sequences, filterValue);
        break;
      case FilterType.LENGTH:
        filtered = this.filterByLength(sequences, filterValue);
        break;
      case FilterType.DIFFICULTY:
        filtered = this.filterByDifficulty(sequences, filterValue);
        break;
      case FilterType.startPosition:
        filtered = this.filterByStartingPosition(sequences, filterValue);
        break;
      case FilterType.AUTHOR:
        filtered = this.filterByAuthor(sequences, filterValue);
        break;
      case FilterType.GRID_MODE:
        filtered = this.filterByGridMode(sequences, filterValue);
        break;
      case FilterType.FAVORITES:
        filtered = sequences.filter((s) => s.isFavorite);
        break;
      case FilterType.RECENT:
        filtered = this.filterByRecent(sequences);
        break;
      default:
        console.log("⚠️ Unknown filter type, returning all sequences");
        filtered = sequences;
    }

    console.log(
      "📊 Filter result:",
      filtered.length,
      "sequences after filtering"
    );
    return filtered;
  }

  async sortSequences(
    sequences: SequenceData[],
    sortMethod: GallerySortMethod
  ): Promise<SequenceData[]> {
    const sorted = [...sequences];

    switch (sortMethod) {
      case GallerySortMethod.ALPHABETICAL:
        return sorted.sort((a, b) => a.word.localeCompare(b.word));
      case GallerySortMethod.dateAdded:
        return sorted.sort((a, b) => {
          const dateA = a.dateAdded || new Date(0);
          const dateB = b.dateAdded || new Date(0);
          return dateB.getTime() - dateA.getTime();
        });
      case GallerySortMethod.difficultyLevel:
        return sorted.sort((a, b) => {
          const levelA = this.getDifficultyOrder(a.difficultyLevel);
          const levelB = this.getDifficultyOrder(b.difficultyLevel);
          return levelA - levelB;
        });
      case GallerySortMethod.sequenceLength:
        return sorted.sort(
          (a, b) => (a.sequenceLength || 0) - (b.sequenceLength || 0)
        );
      case GallerySortMethod.AUTHOR:
        return sorted.sort((a, b) =>
          (a.author || "").localeCompare(b.author || "")
        );
      case GallerySortMethod.POPULARITY:
        return sorted.sort(
          (a, b) => Number(b.isFavorite) - Number(a.isFavorite)
        );
      default:
        return sorted;
    }
  }

  async groupSequencesIntoSections(
    sequences: SequenceData[],
    sortMethod: GallerySortMethod
  ): Promise<Record<string, SequenceData[]>> {
    const sections: Record<string, SequenceData[]> = {};

    for (const sequence of sequences) {
      const sectionKey = this.getSectionKey(sequence, sortMethod);
      if (!sections[sectionKey]) {
        sections[sectionKey] = [];
      }
      sections[sectionKey].push(sequence);
    }

    return sections;
  }

  async getUniqueValues(field: keyof SequenceData): Promise<string[]> {
    const sequences = await this.loadSequenceMetadata();
    const values = new Set<string>();

    for (const sequence of sequences) {
      const value = sequence[field];
      if (value != null) {
        values.add(String(value));
      }
    }

    return Array.from(values).sort();
  }

  async getFilterOptions(filterType: FilterType): Promise<string[]> {
    switch (filterType) {
      case FilterType.STARTING_LETTER:
        return ["A-D", "E-H", "I-L", "M-P", "Q-T", "U-Z"];
      case FilterType.LENGTH:
        return ["3", "4", "5", "6", "7", "8+"];
      case FilterType.DIFFICULTY:
        return ["beginner", "intermediate", "advanced"];
      case FilterType.AUTHOR:
        return this.getUniqueValues("author");
      case FilterType.GRID_MODE:
        return [GridMode.DIAMOND, GridMode.BOX];
      default:
        return [];
    }
  }

  // Private helper methods
  private async loadFromSequenceIndex(): Promise<SequenceData[]> {
    console.log("🌐 Fetching sequence-index.json...");
    const response = await fetch("/sequence-index.json");
    console.log("🌐 Response status:", response.status, response.statusText);

    if (!response.ok) {
      throw new Error(`Failed to load sequence index: ${response.status}`);
    }

    const data = await response.json();
    console.log("📄 Loaded sequence index data:", data);
    console.log("📄 Total sequences in index:", data.totalSequences);
    console.log("📄 Sequences array length:", data.sequences?.length || 0);

    const rawSequences = data.sequences || [];

    // ✅ FIXED: Process real sequences and fix any data format issues
    const sequences = rawSequences
      .filter((seq: Record<string, unknown>) => {
        const word = seq.word || seq.name || seq.id;

        // Only filter out sequences that are clearly invalid
        if (!word || (typeof word === "string" && word.length === 0)) {
          console.warn(
            `🚫 Filtering sequence with no word: ${JSON.stringify(seq)}`
          );
          return false;
        }

        return true;
      })
      .map((seq: Record<string, unknown>) => {
        // Fix GridMode references that might be strings
        let gridMode = seq.gridMode;
        if (typeof gridMode === "string") {
          if (gridMode === "GridMode.DIAMOND" || gridMode === "diamond") {
            gridMode = GridMode.DIAMOND;
          } else if (gridMode === "GridMode.BOX" || gridMode === "box") {
            gridMode = GridMode.BOX;
          }
        }

        // Fix date strings to Date objects
        let dateAdded = seq.dateAdded;
        if (typeof dateAdded === "string") {
          dateAdded = new Date(dateAdded);
        }

        const result = createSequenceData({
          id: String(seq.word || seq.id || crypto.randomUUID()), // Use word for ID to preserve casing
          name: String(seq.name || seq.word || "Unnamed Sequence"),
          word: String(seq.word || seq.name || ""),
          beats: [], // GalleryService doesn't load full beat data
          thumbnails: Array.isArray(seq.thumbnails)
            ? (seq.thumbnails as string[])
            : [],
          isFavorite: Boolean(seq.isFavorite),
          isCircular: Boolean(seq.isCircular),
          tags: Array.isArray(seq.tags)
            ? (seq.tags as string[])
            : ["flow", "practice"],
          metadata:
            typeof seq.metadata === "object" && seq.metadata !== null
              ? (seq.metadata as Record<string, unknown>)
              : { source: "tka_dictionary" },
          // Optional properties
          ...(seq.author && typeof seq.author === "string"
            ? { author: seq.author }
            : {}),
          ...(gridMode && typeof gridMode === "string"
            ? { gridMode: gridMode as GridMode }
            : {}),
          ...(seq.difficultyLevel && typeof seq.difficultyLevel === "string"
            ? {
                difficultyLevel: seq.difficultyLevel,
              }
            : {}),
          ...(seq.sequenceLength && typeof seq.sequenceLength === "number"
            ? {
                sequenceLength: seq.sequenceLength,
              }
            : {}),
          ...(seq.level && typeof seq.level === "number"
            ? { level: seq.level }
            : {}),
          ...(dateAdded instanceof Date ? { dateAdded } : {}),
          ...(seq.propType && typeof seq.propType === "string"
            ? { propType: seq.propType as PropType }
            : {}),
          ...(seq.startingPosition && typeof seq.startingPosition === "string"
            ? {
                startingPositionGroup:
                  seq.startingPosition as GridPositionGroup,
              }
            : {}),
        });

        return result;
      });

    console.log(
      `📦 Processed ${sequences.length} real sequences from dictionary`
    );
    console.log(
      "📋 Sample sequence words:",
      sequences.slice(0, 10).map((s: SequenceData) => s.id)
    );

    return sequences;
  }

  private async generateSequenceIndex(): Promise<SequenceData[]> {
    console.log("🔧 Scanning dictionary folder to generate sequence index...");

    try {
      // Scan the dictionary folder for real sequences
      const sequences: SequenceData[] = [];

      // This is a fallback method - in production, you should regenerate the sequence-index.json
      // For now, return empty array to force using the real sequence-index.json
      console.warn(
        "⚠️ Dictionary scanning not implemented - please ensure sequence-index.json is up to date"
      );
      return sequences;
    } catch (error) {
      console.error("❌ Failed to scan dictionary folder:", error);
      return [];
    }
  }

  private filterByStartingLetter(
    sequences: SequenceData[],
    filterValue: GalleryFilterValue
  ): SequenceData[] {
    if (!filterValue || typeof filterValue !== "string") return sequences;

    if (filterValue.includes("-")) {
      const [start, end] = filterValue.split("-");
      return sequences.filter((s) => {
        const firstLetter = s.word[0]?.toUpperCase();
        return (
          firstLetter &&
          start &&
          end &&
          firstLetter >= start &&
          firstLetter <= end
        );
      });
    }

    return sequences.filter(
      (s) => s.word[0]?.toUpperCase() === filterValue.toUpperCase()
    );
  }

  private filterByContainsLetters(
    sequences: SequenceData[],
    filterValue: GalleryFilterValue
  ): SequenceData[] {
    if (!filterValue || typeof filterValue !== "string") return sequences;
    return sequences.filter((s) =>
      s.word.toLowerCase().includes(filterValue.toLowerCase())
    );
  }

  private filterByLength(
    sequences: SequenceData[],
    filterValue: GalleryFilterValue
  ): SequenceData[] {
    if (!filterValue) return sequences;

    if (filterValue === "8+") {
      return sequences.filter((s) => (s.sequenceLength || 0) >= 8);
    }

    const length = parseInt(String(filterValue));
    if (isNaN(length)) return sequences;

    return sequences.filter((s) => s.sequenceLength === length);
  }

  private filterByDifficulty(
    sequences: SequenceData[],
    filterValue: GalleryFilterValue
  ): SequenceData[] {
    if (!filterValue) return sequences;
    return sequences.filter((s) => s.difficultyLevel === filterValue);
  }

  private filterByStartingPosition(
    sequences: SequenceData[],
    filterValue: GalleryFilterValue
  ): SequenceData[] {
    if (!filterValue) return sequences;
    return sequences.filter((s) => s.startingPositionGroup === filterValue);
  }

  private filterByAuthor(
    sequences: SequenceData[],
    filterValue: GalleryFilterValue
  ): SequenceData[] {
    if (!filterValue) return sequences;
    return sequences.filter((s) => s.author === filterValue);
  }

  private filterByGridMode(
    sequences: SequenceData[],
    filterValue: GalleryFilterValue
  ): SequenceData[] {
    if (!filterValue) return sequences;
    return sequences.filter((s) => s.gridMode === filterValue);
  }

  private filterByRecent(sequences: SequenceData[]): SequenceData[] {
    const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
    return sequences.filter((s) => {
      const dateAdded = s.dateAdded || new Date(0);
      return dateAdded >= thirtyDaysAgo;
    });
  }

  private getDifficultyOrder(difficulty?: string): number {
    switch (difficulty) {
      case "beginner":
        return 1;
      case "intermediate":
        return 2;
      case "advanced":
        return 3;
      default:
        return 0;
    }
  }

  private getSectionKey(
    sequence: SequenceData,
    sortMethod: GallerySortMethod
  ): string {
    switch (sortMethod) {
      case GallerySortMethod.ALPHABETICAL:
        return sequence.word[0]?.toUpperCase() || "#";
      case GallerySortMethod.difficultyLevel:
        return sequence.difficultyLevel || "Unknown";
      case GallerySortMethod.AUTHOR:
        return sequence.author || "Unknown";
      case GallerySortMethod.sequenceLength: {
        const length = sequence.sequenceLength || 0;
        if (length <= 4) return "3-4 beats";
        if (length <= 6) return "5-6 beats";
        if (length <= 8) return "7-8 beats";
        return "9+ beats";
      }
      default:
        return "All";
    }
  }

  clearCache(): void {
    this.cachedSequences = null;
  }
}
