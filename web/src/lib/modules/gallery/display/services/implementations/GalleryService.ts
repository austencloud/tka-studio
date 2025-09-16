/**
 * Browse Service Implementation
 *
 * Handles loading, filtering, and sorting of sequence metadata for the browse tab.
 * Ported and adapted from desktop app's GalleryService.
 */

import { injectable } from "inversify";
import { createSequenceData, GridMode, GridPositionGroup, PropType, type BeatData, type SequenceData } from "../../../../../shared";
import { GalleryFilterType, type GalleryFilterValue } from "../../../../../shared/persistence/domain";
import { PngMetadataExtractor } from "../../../../../shared/pictograph/shared/utils/png-metadata-extractor";
import { GallerySortMethod } from "../../../shared/domain/enums";
import type { IGalleryService } from "../contracts/IGalleryService";

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
    filterType: GalleryFilterType,
    filterValue: GalleryFilterValue
  ): Promise<SequenceData[]> {
    console.log("🔍 GalleryService.applyFilter() called with:");
    console.log("  - filterType:", filterType);
    console.log("  - filterValue:", filterValue);
    console.log("  - input sequences:", sequences.length, "items");

    if (filterType === GalleryFilterType.ALL_SEQUENCES) {
      console.log(
        "✅ ALL_SEQUENCES filter detected - returning all sequences:",
        sequences.length
      );
      return sequences;
    }

    console.log("🔄 Applying specific filter...");
    let filtered: SequenceData[];

    switch (filterType) {
      case GalleryFilterType.STARTING_LETTER:
        filtered = this.filterByStartingLetter(sequences, filterValue);
        break;
      case GalleryFilterType.CONTAINS_LETTERS:
        filtered = this.filterByContainsLetters(sequences, filterValue);
        break;
      case GalleryFilterType.LENGTH:
        filtered = this.filterByLength(sequences, filterValue);
        break;
      case GalleryFilterType.DIFFICULTY:
        filtered = this.filterByDifficulty(sequences, filterValue);
        break;
      case GalleryFilterType.STARTING_POSITION:
        filtered = this.filterByStartingPosition(sequences, filterValue);
        break;
      case GalleryFilterType.AUTHOR:
        filtered = this.filterByAuthor(sequences, filterValue);
        break;
      case GalleryFilterType.GRID_MODE:
        filtered = this.filterByGridMode(sequences, filterValue);
        break;
      case GalleryFilterType.FAVORITES:
        filtered = sequences.filter((s) => s.isFavorite);
        break;
      case GalleryFilterType.RECENT:
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

  async getFilterOptions(filterType: GalleryFilterType): Promise<string[]> {
    switch (filterType) {
      case GalleryFilterType.STARTING_LETTER:
        return ["A-D", "E-H", "I-L", "M-P", "Q-T", "U-Z"];
      case GalleryFilterType.LENGTH:
        return ["3", "4", "5", "6", "7", "8+"];
      case GalleryFilterType.DIFFICULTY:
        return ["beginner", "intermediate", "advanced"];
      case GalleryFilterType.AUTHOR:
        return this.getUniqueValues("author");
      case GalleryFilterType.GRID_MODE:
        return [GridMode.DIAMOND, GridMode.BOX];
      default:
        return [];
    }
  }

  // Private helper methods

  /**
   * Extract real metadata from PNG file for a sequence
   * Based on desktop MetaDataExtractor implementation
   */
  private async extractRealMetadata(sequenceName: string): Promise<{
    beats: BeatData[];
    author: string;
    difficultyLevel: string;
    dateAdded: Date | string;
    gridMode: GridMode;
    isCircular: boolean;
    propType: PropType;
    sequenceLength: number;
    startingPosition: string;
  }> {
    try {
      // Use the PngMetadataExtractor that we know works with simple JSON metadata
      const metadata = await PngMetadataExtractor.extractCompleteMetadata(sequenceName);
      
      if (!metadata || !metadata.sequence || metadata.sequence.length === 0) {
        throw new Error(`No metadata found for ${sequenceName}`);
      }

      const sequenceData = metadata.sequence;


      // Extract basic information from first entry (like desktop implementation)
      const firstEntry = sequenceData[0] as Record<string, unknown>;
      const author = String(firstEntry.author || "Unknown");
      const level = Number(firstEntry.level || 1);
      const gridMode = firstEntry.gridMode === "diamond" ? GridMode.DIAMOND : GridMode.BOX;
      const isCircular = Boolean(firstEntry.isCircular);
      const propType = String(firstEntry.propType || "Staff") as PropType;

      // Extract beats (filter out metadata entries and start position)
      // Based on desktop logic: metadata.slice(1).filter(step => step.letter && !step.sequence_start_position)
      const realBeats = sequenceData
        .slice(1) // Skip first entry (metadata)
        .filter((step: Record<string, unknown>) => 
          step.letter && !step.sequence_start_position
        )
        .map((step: Record<string, unknown>, index: number) => {
          return {
            id: `beat-${sequenceName}-${index + 1}`,
            beatNumber: Number(step.beat || index + 1),
            duration: 1.0,
            blueReversal: false,
            redReversal: false,
            isBlank: false,
            pictographData: {
              id: `pictograph-${sequenceName}-${index + 1}`,
              letter: String(step.letter || ""),
              startPosition: null,
              endPosition: null,
              motions: {},
            }
          } as BeatData;
        });

      // Calculate sequence length using desktop formula but with realBeats
      // Desktop uses: len(metadata["sequence"]) - 2
      // We add 2 to realBeats.length since we filtered out metadata entries
      const sequenceLength = realBeats.length + 2;

      // Use the actual beat count (realBeats.length) not the calculated length
      const actualBeatCount = realBeats.length;

      // Convert difficulty level number to string
      let difficultyLevel = "beginner";
      if (level >= 3) {
        difficultyLevel = "advanced";
      } else if (level >= 2) {
        difficultyLevel = "intermediate";
      }

      // Extract starting position
      const startPositionEntries = sequenceData.filter(
        (step: Record<string, unknown>) => step.sequence_start_position
      );
      const startingPosition = String(
        startPositionEntries[0]?.sequence_start_position || "alpha"
      );

      // Extract date information - check both top-level and first entry
      let dateAdded: Date | string = new Date(); // Default fallback



      // Try top-level first, then first entry fields
      if (metadata.date_added) {
        try {
          dateAdded = new Date(String(metadata.date_added));
          console.log(`✅ Found TOP-LEVEL date_added for ${sequenceName}:`, dateAdded);
        } catch {
          console.warn(`Invalid date format in TOP-LEVEL metadata for ${sequenceName}:`, metadata.date_added);
        }
      } else if (firstEntry.date_added) {
        try {
          dateAdded = new Date(String(firstEntry.date_added));
          console.log(`✅ Found date_added for ${sequenceName}:`, dateAdded);
        } catch {
          console.warn(`Invalid date format in metadata for ${sequenceName}:`, firstEntry.date_added);
        }
      } else if (firstEntry.created_date) {
        try {
          dateAdded = new Date(String(firstEntry.created_date));
          console.log(`✅ Found created_date for ${sequenceName}:`, dateAdded);
        } catch {
          console.warn(`Invalid date format in metadata for ${sequenceName}:`, firstEntry.created_date);
        }
      } else if (firstEntry.timestamp) {
        try {
          dateAdded = new Date(String(firstEntry.timestamp));
          console.log(`✅ Found timestamp for ${sequenceName}:`, dateAdded);
        } catch {
          console.warn(`Invalid timestamp format in metadata for ${sequenceName}:`, firstEntry.timestamp);
        }
      } else if (firstEntry.date) {
        try {
          dateAdded = new Date(String(firstEntry.date));
          console.log(`✅ Found date for ${sequenceName}:`, dateAdded);
        } catch {
          console.warn(`Invalid date format in metadata for ${sequenceName}:`, firstEntry.date);
        }
      } else if (firstEntry.dateAdded) {
        try {
          dateAdded = new Date(String(firstEntry.dateAdded));
          console.log(`✅ Found dateAdded for ${sequenceName}:`, dateAdded);
        } catch {
          console.warn(`Invalid dateAdded format in metadata for ${sequenceName}:`, firstEntry.dateAdded);
        }
      } else {
        console.warn(`⚠️ No date field found for ${sequenceName}, using current date`);
        console.log(`🔍 Available firstEntry fields:`, Object.keys(firstEntry));
      }

      console.log(`✅ Extracted real metadata for ${sequenceName}: ${author}, ${difficultyLevel}, ${actualBeatCount} beats`);

      return {
        beats: realBeats,
        author,
        difficultyLevel,
        dateAdded,
        gridMode,
        isCircular,
        propType,
        sequenceLength: actualBeatCount,
        startingPosition,
      };
    } catch (error) {
      console.warn(`⚠️ Failed to extract PNG metadata for ${sequenceName}:`, error);
      throw error;
    }
  }

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

    // ✅ FIXED: Process real sequences with PNG metadata extraction
    const sequences: SequenceData[] = [];

    for (const seq of rawSequences) {
      const word = seq.word || seq.name || seq.id;

      // Only filter out sequences that are clearly invalid
      if (!word || (typeof word === "string" && word.length === 0)) {
        console.warn(
          `🚫 Filtering sequence with no word: ${JSON.stringify(seq)}`
        );
        continue;
      }

      try {
        // Extract real metadata from PNG file
        const realMetadata = await this.extractRealMetadata(String(word));
        
        // Use real gridMode from metadata, or process string values from index
        let gridMode: GridMode = realMetadata.gridMode;
        if (!gridMode && seq.gridMode) {
          const gridModeValue = seq.gridMode;
          if (typeof gridModeValue === "string") {
            if (gridModeValue === "GridMode.DIAMOND" || gridModeValue === "diamond") {
              gridMode = GridMode.DIAMOND;
            } else if (gridModeValue === "GridMode.BOX" || gridModeValue === "box") {
              gridMode = GridMode.BOX;
            } else {
              gridMode = GridMode.BOX; // Default fallback
            }
          } else {
            gridMode = gridModeValue as GridMode;
          }
        }
        if (!gridMode) {
          gridMode = GridMode.BOX; // Final fallback
        }

        // Fix date strings to Date objects
        let dateAdded = realMetadata.dateAdded || seq.dateAdded;
        if (typeof dateAdded === "string") {
          dateAdded = new Date(dateAdded);
        }

        const result = createSequenceData({
          id: String(word), // Use word for ID to preserve casing
          name: String(seq.name || word || "Unnamed Sequence"),
          word: String(word),
          beats: realMetadata.beats, // Real beats from PNG metadata
          thumbnails: Array.isArray(seq.thumbnails)
            ? (seq.thumbnails as string[])
            : [],
          isFavorite: Boolean(seq.isFavorite),
          isCircular: Boolean(realMetadata.isCircular ?? seq.isCircular),
          tags: Array.isArray(seq.tags)
            ? (seq.tags as string[])
            : ["flow", "practice"],
          metadata:
            typeof seq.metadata === "object" && seq.metadata !== null
              ? (seq.metadata as Record<string, unknown>)
              : { source: "tka_dictionary" },
          // Use real metadata with fallback to index data
          author: realMetadata.author || String(seq.author || "Unknown"),
          gridMode: gridMode || GridMode.BOX,
          difficultyLevel: realMetadata.difficultyLevel || (seq.difficultyLevel && typeof seq.difficultyLevel === "string" ? seq.difficultyLevel : "beginner"),
          sequenceLength: realMetadata.sequenceLength, // Real sequence length from PNG
          level: typeof seq.level === "number" ? seq.level : undefined,
          dateAdded: dateAdded instanceof Date ? dateAdded : new Date(),
          propType: (realMetadata.propType || seq.propType) as PropType || "Staff",
          startingPositionGroup: (realMetadata.startingPosition || seq.startingPosition) as GridPositionGroup || "alpha",
        });

        console.log(`✅ Loaded sequence with real metadata: ${result.word} (${result.author}, ${result.sequenceLength} beats)`);
        sequences.push(result);
      } catch (error) {
        console.warn(`⚠️ Failed to extract metadata for ${word}, using fallback:`, error);
        
        // Fallback to index data if PNG extraction fails
        // Fix GridMode references that might be strings  
        let gridMode: GridMode = GridMode.BOX; // Default
        if (seq.gridMode) {
          if (typeof seq.gridMode === "string") {
            if (seq.gridMode === "GridMode.DIAMOND" || seq.gridMode === "diamond") {
              gridMode = GridMode.DIAMOND;
            } else if (seq.gridMode === "GridMode.BOX" || seq.gridMode === "box") {
              gridMode = GridMode.BOX;
            }
          } else {
            gridMode = seq.gridMode as GridMode;
          }
        }

        // Fix date strings to Date objects
        let dateAdded = seq.dateAdded;
        if (typeof dateAdded === "string") {
          dateAdded = new Date(dateAdded);
        }

        const fallbackResult = createSequenceData({
          id: String(word),
          name: String(seq.name || word || "Unnamed Sequence"),
          word: String(word),
          beats: [], // Empty beats array as fallback
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
          // Fallback values
          author: String(seq.author || "Unknown"),
          gridMode: (gridMode as GridMode) || GridMode.BOX,
          difficultyLevel: (seq.difficultyLevel && typeof seq.difficultyLevel === "string" ? seq.difficultyLevel : "beginner"),
          sequenceLength: typeof seq.sequenceLength === "number" ? seq.sequenceLength : 0,
          level: typeof seq.level === "number" ? seq.level : undefined,
          dateAdded: dateAdded instanceof Date ? dateAdded : new Date(),
          propType: (seq.propType as PropType) || "Staff",
          startingPositionGroup: (seq.startingPosition as GridPositionGroup) || "alpha",
        });

        sequences.push(fallbackResult);
      }
    }

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
