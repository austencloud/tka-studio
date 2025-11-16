/**
 * Option Organizer Service Implementation
 *
 * Handles organization of pictograph options into sections and groups.
 * Extracted from OptionPickerService for better separation of concerns.
 * Eliminates code duplication by using a single organization method.
 */

import type { PictographData, Letter } from "$shared";
import { getLetterType, LetterType } from "$shared";
import { injectable } from "inversify";
import type { OrganizedSection, SortMethod } from "../../domain";
import type { IOptionOrganizer } from "../contracts/IOptionOrganizer";

@injectable()
export class OptionOrganizer implements IOptionOrganizer {
  /**
   * Organize pictographs by sort method into sections
   * OPTIMIZED: Single method eliminates code duplication from original service
   */
  organizePictographs(
    pictographs: PictographData[],
    sortMethod: SortMethod
  ): OrganizedSection[] {
    // For type, endPosition, and reversals sorting, use the same type-based organization
    if (
      sortMethod === "type" ||
      sortMethod === "endPosition" ||
      sortMethod === "reversals"
    ) {
      return this.organizeByTypes(pictographs);
    }

    // For other sort methods, use generic organization
    return this.organizeGeneric(pictographs, sortMethod);
  }

  /**
   * Organize pictographs by letter types (Types 1-6)
   * Used for type, endPosition, and reversals sorting
   */
  private organizeByTypes(pictographs: PictographData[]): OrganizedSection[] {
    const allTypes = ["Type1", "Type2", "Type3", "Type4", "Type5", "Type6"];
    const groups = new Map<string, PictographData[]>();

    // Initialize all types with empty arrays
    allTypes.forEach((type) => {
      groups.set(type, []);
    });

    // Distribute pictographs to their respective types
    for (const pictograph of pictographs) {
      const groupKey = this.getLetterTypeFromString(pictograph.letter);
      if (groups.has(groupKey)) {
        groups.get(groupKey)!.push(pictograph);
      }
    }

    // Create sections for Types 1-3 (individual sections)
    const sections: OrganizedSection[] = [];
    const individualTypes = ["Type1", "Type2", "Type3"];
    const groupedTypes = ["Type4", "Type5", "Type6"];
    const groupedPictographs: PictographData[] = [];

    // Add individual sections (Types 1-3) - always create even if empty
    individualTypes.forEach((type) => {
      sections.push({
        title: type,
        pictographs: groups.get(type) || [],
        type: "section" as const,
      });
    });

    // Collect Types 4-6 for grouping
    groupedTypes.forEach((type) => {
      const typePictographs = groups.get(type) || [];
      groupedPictographs.push(...typePictographs);
    });

    // Always add grouped section for Types 4-6 (even if empty)
    sections.push({
      title: "Types 4-6",
      pictographs: groupedPictographs,
      type: "grouped" as const,
    });

    return sections;
  }

  /**
   * Generic organization for other sort methods
   */
  private organizeGeneric(
    pictographs: PictographData[],
    sortMethod: SortMethod
  ): OrganizedSection[] {
    const groups = new Map<string, PictographData[]>();

    for (const pictograph of pictographs) {
      let groupKey: string;

      switch (sortMethod) {
        default:
          groupKey = this.getLetterTypeFromString(pictograph.letter);
      }

      if (!groups.has(groupKey)) {
        groups.set(groupKey, []);
      }
      groups.get(groupKey)!.push(pictograph);
    }

    // Convert groups to sections
    const sections: OrganizedSection[] = [];
    for (const [title, sectionPictographs] of groups.entries()) {
      sections.push({
        title,
        pictographs: sectionPictographs,
        type: "section" as const,
      });
    }

    return sections;
  }

  /**
   * Helper function to convert string letter to Letter enum and get type
   * Uses shared infrastructure instead of duplicated logic
   */
  private getLetterTypeFromString(letter: string | null | undefined): string {
    if (!letter) return LetterType.TYPE1;

    try {
      // Use the existing shared getLetterType function
      const letterEnum = letter as Letter;
      const letterType = getLetterType(letterEnum);
      return letterType; // Returns LetterType enum value (e.g., "Type1")
    } catch (error) {
      // Fallback for invalid letters
      console.warn(
        `Failed to determine letter type for "${letter}", defaulting to TYPE1:`,
        error
      );
      return LetterType.TYPE1;
    }
  }
}
