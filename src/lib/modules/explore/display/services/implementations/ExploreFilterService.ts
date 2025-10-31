/**
 * Explore Filter Service
 *
 * Handles all filtering operations for gallery sequences.
 * Each filter type has its own dedicated method for clarity.
 */

import type { SequenceData } from "$shared";
import { GridMode } from "$shared/pictograph/grid/domain/enums/grid-enums";
import { injectable } from "inversify";
import {
  ExploreFilterType,
  type ExploreFilterValue,
} from "../../../../../shared/persistence/domain";
import type { IExploreFilterService } from "../contracts/IExploreFilterService";

// Constants
const THIRTY_DAYS_MS = 30 * 24 * 60 * 60 * 1000;

const STARTING_LETTER_RANGES = ["A-D", "E-H", "I-L", "M-P", "Q-T", "U-Z"];
const LENGTH_OPTIONS = ["3", "4", "5", "6", "7", "8+"];
const DIFFICULTY_OPTIONS = ["beginner", "intermediate", "advanced"];
const GRID_MODE_OPTIONS = [GridMode.DIAMOND, GridMode.BOX];

@injectable()
export class ExploreFilterService implements IExploreFilterService {
  applyFilter(
    sequences: SequenceData[],
    filterType: ExploreFilterType,
    filterValue: ExploreFilterValue
  ): SequenceData[] {
    if (filterType === ExploreFilterType.ALL_SEQUENCES) {
      return sequences;
    }

    switch (filterType) {
      case ExploreFilterType.STARTING_LETTER:
        return this.filterByStartingLetter(sequences, filterValue);
      case ExploreFilterType.CONTAINS_LETTERS:
        return this.filterByContainsLetters(sequences, filterValue);
      case ExploreFilterType.LENGTH:
        return this.filterByLength(sequences, filterValue);
      case ExploreFilterType.DIFFICULTY:
        return this.filterByDifficulty(sequences, filterValue);
      case ExploreFilterType.STARTING_POSITION:
        return this.filterByStartingPosition(sequences, filterValue);
      case ExploreFilterType.AUTHOR:
        return this.filterByAuthor(sequences, filterValue);
      case ExploreFilterType.GRID_MODE:
        return this.filterByGridMode(sequences, filterValue);
      case ExploreFilterType.FAVORITES:
        return this.filterByFavorites(sequences);
      case ExploreFilterType.RECENT:
        return this.filterByRecent(sequences);
      default:
        return sequences;
    }
  }

  getFilterOptions(
    filterType: ExploreFilterType,
    sequences: SequenceData[]
  ): string[] {
    switch (filterType) {
      case ExploreFilterType.STARTING_LETTER:
        return STARTING_LETTER_RANGES;
      case ExploreFilterType.LENGTH:
        return LENGTH_OPTIONS;
      case ExploreFilterType.DIFFICULTY:
        return DIFFICULTY_OPTIONS;
      case ExploreFilterType.AUTHOR:
        return this.getUniqueAuthors(sequences);
      case ExploreFilterType.GRID_MODE:
        return GRID_MODE_OPTIONS;
      default:
        return [];
    }
  }

  // ============================================================================
  // Filter Methods
  // ============================================================================

  private filterByStartingLetter(
    sequences: SequenceData[],
    filterValue: ExploreFilterValue
  ): SequenceData[] {
    if (!filterValue || typeof filterValue !== "string") {
      return sequences;
    }

    // Handle range format (e.g., "A-D")
    if (filterValue.includes("-")) {
      return this.filterByLetterRange(sequences, filterValue);
    }

    // Handle single letter
    return sequences.filter(
      (seq) => seq.word[0]?.toUpperCase() === filterValue.toUpperCase()
    );
  }

  private filterByLetterRange(
    sequences: SequenceData[],
    range: string
  ): SequenceData[] {
    const [start, end] = range.split("-");
    if (!start || !end) {
      return sequences;
    }

    return sequences.filter((seq) => {
      const firstLetter = seq.word[0]?.toUpperCase();
      return firstLetter && firstLetter >= start && firstLetter <= end;
    });
  }

  private filterByContainsLetters(
    sequences: SequenceData[],
    filterValue: ExploreFilterValue
  ): SequenceData[] {
    if (!filterValue || typeof filterValue !== "string") {
      return sequences;
    }

    const searchTerm = filterValue.toLowerCase();
    return sequences.filter((seq) =>
      seq.word.toLowerCase().includes(searchTerm)
    );
  }

  private filterByLength(
    sequences: SequenceData[],
    filterValue: ExploreFilterValue
  ): SequenceData[] {
    if (!filterValue) {
      return sequences;
    }

    // Handle "8+" case
    if (filterValue === "8+") {
      return sequences.filter((seq) => (seq.sequenceLength || 0) >= 8);
    }

    // Handle numeric length
    const length = parseInt(String(filterValue));
    if (isNaN(length)) {
      return sequences;
    }

    return sequences.filter((seq) => seq.sequenceLength === length);
  }

  private filterByDifficulty(
    sequences: SequenceData[],
    filterValue: ExploreFilterValue
  ): SequenceData[] {
    if (!filterValue) {
      return sequences;
    }

    return sequences.filter((seq) => seq.difficultyLevel === filterValue);
  }

  private filterByStartingPosition(
    sequences: SequenceData[],
    filterValue: ExploreFilterValue
  ): SequenceData[] {
    if (!filterValue) {
      return sequences;
    }

    return sequences.filter((seq) => seq.startingPositionGroup === filterValue);
  }

  private filterByAuthor(
    sequences: SequenceData[],
    filterValue: ExploreFilterValue
  ): SequenceData[] {
    if (!filterValue) {
      return sequences;
    }

    return sequences.filter((seq) => seq.author === filterValue);
  }

  private filterByGridMode(
    sequences: SequenceData[],
    filterValue: ExploreFilterValue
  ): SequenceData[] {
    if (!filterValue) {
      return sequences;
    }

    return sequences.filter((seq) => seq.gridMode === filterValue);
  }

  private filterByFavorites(sequences: SequenceData[]): SequenceData[] {
    return sequences.filter((seq) => seq.isFavorite);
  }

  private filterByRecent(sequences: SequenceData[]): SequenceData[] {
    const thirtyDaysAgo = new Date(Date.now() - THIRTY_DAYS_MS);
    return sequences.filter((seq) => {
      const dateAdded = seq.dateAdded || new Date(0);
      return dateAdded >= thirtyDaysAgo;
    });
  }

  // ============================================================================
  // Helper Methods
  // ============================================================================

  private getUniqueAuthors(sequences: SequenceData[]): string[] {
    const authors = new Set<string>();

    for (const sequence of sequences) {
      if (sequence.author) {
        authors.add(sequence.author);
      }
    }

    return Array.from(authors).sort();
  }
}
