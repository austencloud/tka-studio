/**
 * OptionFilteringService - Centralized option filtering utilities
 *
 * Handles filtering of pictograph options by various criteria including
 * position, letter types, rotation, and other motion parameters.
 */

import { getLetterType } from "$lib/domain";
import type { BeatData } from "$lib/domain/BeatData";
import type { PictographData } from "$lib/domain/PictographData";
import type { IPositionMapper } from "../../interfaces/movement/IPositionMapper";
import type { IEnumMappingService } from "./EnumMappingService";
import { injectable, inject } from "inversify";
import { TYPES } from "../../inversify/types";

export interface FilterCriteria {
  startPosition?: string;
  endPosition?: string;
  letterTypes?: string[];
  blueRotationDirection?: string;
  redRotationDirection?: string;
  motionTypes?: string[];
  difficulty?: string;
  excludeLetters?: string[];
}

export interface FilterResult {
  filtered: PictographData[];
  totalOriginal: number;
  totalFiltered: number;
  appliedFilters: string[];
}

export interface IOptionFilteringService {
  filterByStartPosition(
    options: PictographData[],
    startPosition: string
  ): PictographData[];
  filterByEndPosition(
    options: PictographData[],
    endPosition: string
  ): PictographData[];
  filterByLetterTypes(
    options: PictographData[],
    letterTypes: string[]
  ): PictographData[];
  filterByRotation(
    options: PictographData[],
    blueRotationDirection: string,
    redRotationDirection: string
  ): PictographData[];
  filterByCriteria(
    options: PictographData[],
    criteria: FilterCriteria
  ): FilterResult;
  extractEndPosition(lastBeat: BeatData): string | null;
}

@injectable()
export class OptionFilteringService implements IOptionFilteringService {
  constructor(
    @inject(TYPES.IEnumMappingService)
    private enumMappingService: IEnumMappingService,
    @inject(TYPES.IPositionMapper) private positionService: IPositionMapper
  ) {}

  /**
   * Filter options by start position
   */
  filterByStartPosition(
    options: PictographData[],
    startPosition: string
  ): PictographData[] {
    if (!startPosition) return options;

    return options.filter((option) => {
      // Compute startPosition from motion data
      const optionStartPos =
        option.motions?.blue && option.motions?.red
          ? this.positionService
              .getPositionFromLocations(
                option.motions.blue.startLocation,
                option.motions.red.startLocation
              )
              ?.toString()
              .toLowerCase()
          : null;
      const targetStartPos = startPosition.toLowerCase();
      return optionStartPos === targetStartPos;
    });
  }

  /**
   * Filter options by end position
   */
  filterByEndPosition(
    options: PictographData[],
    endPosition: string
  ): PictographData[] {
    if (!endPosition) return options;

    return options.filter((option) => {
      // Compute endPosition from motion data
      const optionEndPos =
        option.motions?.blue && option.motions?.red
          ? this.positionService
              .getPositionFromLocations(
                option.motions.blue.endLocation,
                option.motions.red.endLocation
              )
              ?.toString()
              .toLowerCase()
          : null;
      const targetEndPos = endPosition.toLowerCase();
      return optionEndPos === targetEndPos;
    });
  }

  /**
   * Filter options by letter types
   */
  filterByLetterTypes(
    options: PictographData[],
    letterTypes: string[]
  ): PictographData[] {
    if (!letterTypes || letterTypes.length === 0) return options;

    return options.filter((option) => {
      if (!option.letter) return false;

      const letterType = getLetterType(option.letter);
      return letterTypes.includes(letterType);
    });
  }

  /**
   * Filter options by rotation directions
   */
  filterByRotation(
    options: PictographData[],
    blueRotationDirection: string,
    redRotationDirection: string
  ): PictographData[] {
    return options.filter((option) => {
      let matches = true;

      // Check blue rotation if specified
      if (blueRotationDirection && blueRotationDirection !== "any") {
        const blueRotation = option.motions?.blue?.rotationDirection
          ?.toString()
          .toLowerCase();
        const targetBlueRotation = blueRotationDirection.toLowerCase();
        matches = matches && blueRotation === targetBlueRotation;
      }

      // Check red rotation if specified
      if (redRotationDirection && redRotationDirection !== "any") {
        const redRotation = option.motions?.red?.rotationDirection
          ?.toString()
          .toLowerCase();
        const targetRedRotation = redRotationDirection.toLowerCase();
        matches = matches && redRotation === targetRedRotation;
      }

      return matches;
    });
  }

  /**
   * Filter options by multiple criteria with detailed result
   */
  filterByCriteria(
    options: PictographData[],
    criteria: FilterCriteria
  ): FilterResult {
    let filtered = [...options];
    const appliedFilters: string[] = [];
    const totalOriginal = options.length;

    // Apply start position filter
    if (criteria.startPosition) {
      filtered = this.filterByStartPosition(filtered, criteria.startPosition);
      appliedFilters.push(`startPosition: ${criteria.startPosition}`);
    }

    // Apply end position filter
    if (criteria.endPosition) {
      filtered = this.filterByEndPosition(filtered, criteria.endPosition);
      appliedFilters.push(`endPosition: ${criteria.endPosition}`);
    }

    // Apply letter types filter
    if (criteria.letterTypes && criteria.letterTypes.length > 0) {
      filtered = this.filterByLetterTypes(filtered, criteria.letterTypes);
      appliedFilters.push(`letterTypes: ${criteria.letterTypes.join(", ")}`);
    }

    // Apply rotation filter
    if (criteria.blueRotationDirection || criteria.redRotationDirection) {
      filtered = this.filterByRotation(
        filtered,
        criteria.blueRotationDirection || "",
        criteria.redRotationDirection || ""
      );
      appliedFilters.push(
        `rotation: blue=${criteria.blueRotationDirection || "any"}, red=${criteria.redRotationDirection || "any"}`
      );
    }

    // Apply motion types filter
    if (criteria.motionTypes && criteria.motionTypes.length > 0) {
      filtered = this.filterByMotionTypes(filtered, criteria.motionTypes);
      appliedFilters.push(`motionTypes: ${criteria.motionTypes.join(", ")}`);
    }

    // Apply exclude letters filter
    if (criteria.excludeLetters && criteria.excludeLetters.length > 0) {
      filtered = this.filterExcludeLetters(filtered, criteria.excludeLetters);
      appliedFilters.push(
        `excludeLetters: ${criteria.excludeLetters.join(", ")}`
      );
    }

    return {
      filtered,
      totalOriginal,
      totalFiltered: filtered.length,
      appliedFilters,
    };
  }

  /**
   * Extract end position from the last beat in a sequence
   * Computes end position from motion data using PositionMapper
   */
  extractEndPosition(lastBeat: BeatData): string | null {
    try {
      if (!lastBeat || !lastBeat.pictographData) {
        return null;
      }

      const pictographData = lastBeat.pictographData;
      if (!pictographData.motions?.blue || !pictographData.motions?.red) {
        return null;
      }

      const endPosition = this.positionService.getPositionFromLocations(
        pictographData.motions.blue.endLocation,
        pictographData.motions.red.endLocation
      );

      return endPosition ? endPosition.toString() : null;
    } catch (error) {
      console.warn("⚠️ Failed to extract end position from beat:", error);
      return null;
    }
  }

  /**
   * Filter by motion types
   */
  private filterByMotionTypes(
    options: PictographData[],
    motionTypes: string[]
  ): PictographData[] {
    return options.filter((option) => {
      const blueMotionType = option.motions?.blue?.motionType
        ?.toString()
        .toLowerCase();
      const redMotionType = option.motions?.red?.motionType
        ?.toString()
        .toLowerCase();

      const normalizedMotionTypes = motionTypes.map((mt) => mt.toLowerCase());

      return (
        normalizedMotionTypes.includes(blueMotionType || "") ||
        normalizedMotionTypes.includes(redMotionType || "")
      );
    });
  }

  /**
   * Filter to exclude specific letters
   */
  private filterExcludeLetters(
    options: PictographData[],
    excludeLetters: string[]
  ): PictographData[] {
    return options.filter((option) => {
      return !excludeLetters.includes(option.letter || "");
    });
  }

  /**
   * Get filtering statistics for debugging
   */
  getFilteringStats(
    originalOptions: PictographData[],
    criteria: FilterCriteria
  ): {
    originalCount: number;
    afterEachFilter: Array<{
      filterName: string;
      count: number;
      criteria: string;
    }>;
    finalCount: number;
  } {
    let current = [...originalOptions];
    const afterEachFilter: Array<{
      filterName: string;
      count: number;
      criteria: string;
    }> = [];

    // Track each filter step
    if (criteria.startPosition) {
      current = this.filterByStartPosition(current, criteria.startPosition);
      afterEachFilter.push({
        filterName: "startPosition",
        count: current.length,
        criteria: criteria.startPosition,
      });
    }

    if (criteria.endPosition) {
      current = this.filterByEndPosition(current, criteria.endPosition);
      afterEachFilter.push({
        filterName: "endPosition",
        count: current.length,
        criteria: criteria.endPosition,
      });
    }

    if (criteria.letterTypes && criteria.letterTypes.length > 0) {
      current = this.filterByLetterTypes(current, criteria.letterTypes);
      afterEachFilter.push({
        filterName: "letterTypes",
        count: current.length,
        criteria: criteria.letterTypes.join(", "),
      });
    }

    return {
      originalCount: originalOptions.length,
      afterEachFilter,
      finalCount: current.length,
    };
  }
}
