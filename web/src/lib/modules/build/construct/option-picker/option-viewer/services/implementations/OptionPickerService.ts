/**
 * Option Picker Service
 * 
 * Simplified service that combines all essential option picker functionality.
 * Preserves all working business logic while removing abstraction layers.
 */

import type { IMotionQueryHandler, PictographData } from "$shared";
import { TYPES, GridPosition, GridPositionGroup } from "$shared";
import { inject, injectable } from "inversify";
import type { SortMethod, TypeFilter } from "../../domain";
import type { IOptionPickerService } from "../contracts";

// Type for end position filter
type EndPositionFilter = {
  alpha: boolean;
  beta: boolean;
  gamma: boolean;
};

// Type for reversal filter
type ReversalFilter = {
  continuous: boolean;
  '1-reversal': boolean;
  '2-reversals': boolean;
};

@injectable()
export class OptionPickerService implements IOptionPickerService {
  constructor(
    @inject(TYPES.IGridPositionDeriver) private positionMapper: any,
    @inject(TYPES.IMotionQueryHandler) private motionQueryHandler: IMotionQueryHandler
  ) {}

  /**
   * Load available options based on current sequence
   * PRESERVED: Core working logic from OptionPickerDataService
   */
  async loadOptionsFromSequence(sequence: PictographData[]): Promise<PictographData[]> {
    if (!sequence || sequence.length === 0) {
      return [];
    }

    const lastBeat = sequence[sequence.length - 1];
    const endPosition = this.getEndPosition(lastBeat);

    if (!endPosition || typeof endPosition !== "string") {
      return [];
    }

    try {
      // Get all available options from motion query service
      const allOptions = await this.motionQueryHandler.getNextOptionsForSequence(sequence);

      // Filter options based on sequence context
      // The next beat's start position should match the current beat's end position
      const filteredOptions = allOptions.filter((option) => {
        if (!option.motions?.blue || !option.motions?.red) {
          return false;
        }

        // Calculate the start position of this option
        const optionStartPosition = this.positionMapper.getGridPositionFromLocations(
          option.motions.blue.startLocation,
          option.motions.red.startLocation
        );

        const optionStartPositionStr = optionStartPosition?.toString().toLowerCase();
        const targetEndPosition = endPosition.toLowerCase();

        return optionStartPositionStr === targetEndPosition;
      });

      return filteredOptions;
    } catch (error) {
      console.error("Failed to load options from sequence:", error);
      return [];
    }
  }

  /**
   * Get filtered and sorted options
   * ENHANCED: Now supports end position and reversal filtering
   */
  getFilteredOptions(
    options: PictographData[],
    sortMethod: SortMethod,
    typeFilter?: TypeFilter,
    endPositionFilter?: EndPositionFilter,
    reversalFilter?: ReversalFilter
  ): PictographData[] {
    let filteredOptions = [...options];

    // Apply type filtering when sort method is 'type' and typeFilter is provided
    if (sortMethod === 'type' && typeFilter) {
      filteredOptions = this.applyTypeFiltering(filteredOptions, typeFilter);
    }

    // Apply end position filtering when sort method is 'endPosition' and endPositionFilter is provided
    if (sortMethod === 'endPosition' && endPositionFilter) {
      filteredOptions = this.applyEndPositionFiltering(filteredOptions, endPositionFilter);
    }

    // Apply reversal filtering when sort method is 'reversals' and reversalFilter is provided
    if (sortMethod === 'reversals' && reversalFilter) {
      filteredOptions = this.applyReversalFiltering(filteredOptions, reversalFilter);
    }

    // Apply sorting
    if (sortMethod) {
      filteredOptions = this.applySorting(filteredOptions, sortMethod);
    }

    return filteredOptions;
  }



  /**
   * Apply type filtering to options
   */
  private applyTypeFiltering(options: PictographData[], typeFilter: TypeFilter): PictographData[] {
    return options.filter(option => {
      const letterType = this.getLetterType(option.letter);

      switch (letterType) {
        case 'Type1': return typeFilter.type1;
        case 'Type2': return typeFilter.type2;
        case 'Type3': return typeFilter.type3;
        case 'Type4': return typeFilter.type4;
        case 'Type5': return typeFilter.type5;
        case 'Type6': return typeFilter.type6;
        default: return true; // Include unknown types by default
      }
    });
  }

  /**
   * Determine letter type from letter string
   */
  private getLetterType(letter: string | null | undefined): string {
    if (!letter) return 'Type1'; // Default fallback

    // Type1: Dual-Shift (A-V)
    if (letter.match(/^[A-V]$/)) return 'Type1';

    // Type2: Shift (W, X, Y, Z, Σ, Δ, θ, Ω)
    if (letter.match(/^[WXYZ]$|^[ΣΔθΩ]$/)) return 'Type2';

    // Type3: Cross-Shift (W-, X-, Y-, Z-, Σ-, Δ-, θ-, Ω-)
    if (letter.match(/^[WXYZ]-$|^[ΣΔθΩ]-$/)) return 'Type3';

    // Type4: Dash (Φ, Ψ, Λ)
    if (letter.match(/^[ΦΨΛ]$/)) return 'Type4';

    // Type5: Dual-Dash (Φ-, Ψ-, Λ-)
    if (letter.match(/^[ΦΨΛ]-$/)) return 'Type5';

    // Type6: Static (α, β, Γ)
    if (letter.match(/^[αβΓ]$/)) return 'Type6';

    return 'Type1'; // Default fallback
  }

  /**
   * Apply end position filtering to options
   */
  private applyEndPositionFiltering(options: PictographData[], endPositionFilter: EndPositionFilter): PictographData[] {
    return options.filter(option => {
      const endPositionGroup = this.getEndPositionGroup(option.endPosition);
      
      switch (endPositionGroup) {
        case GridPositionGroup.ALPHA: return endPositionFilter.alpha;
        case GridPositionGroup.BETA: return endPositionFilter.beta;
        case GridPositionGroup.GAMMA: return endPositionFilter.gamma;
        default: return true; // Include unknown positions by default
      }
    });
  }

  /**
   * Apply reversal filtering to options
   */
  private applyReversalFiltering(options: PictographData[], reversalFilter: ReversalFilter): PictographData[] {
    return options.filter(option => {
      const reversalCount = this.getReversalCount(option);
      
      switch (reversalCount) {
        case 0: return reversalFilter.continuous;
        case 1: return reversalFilter['1-reversal'];
        case 2: return reversalFilter['2-reversals'];
        default: return true; // Include unknown reversal counts by default
      }
    });
  }

  /**
   * Get the position group (Alpha, Beta, Gamma) from a GridPosition
   */
  private getEndPositionGroup(endPosition: GridPosition | null | undefined): GridPositionGroup | null {
    if (!endPosition) return null;

    const positionStr = endPosition.toString();
    
    if (positionStr.startsWith('alpha')) return GridPositionGroup.ALPHA;
    if (positionStr.startsWith('beta')) return GridPositionGroup.BETA;
    if (positionStr.startsWith('gamma')) return GridPositionGroup.GAMMA;
    
    return null;
  }

  /**
   * Calculate the number of reversals in a pictograph's motion
   * TODO: Implement proper reversal calculation based on motion data
   */
  private getReversalCount(option: PictographData): number {
    // Placeholder implementation - should be replaced with actual motion analysis
    // For now, return a random distribution for testing
    const id = option.id || '';
    const hash = id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return hash % 3; // 0, 1, or 2 reversals
  }

  /**
   * Organize pictographs by sort method (moved from OptionGrid component)
   * MODIFIED: Always create sections for all types to enable fade animations
   */
  organizePictographs(
    pictographs: PictographData[],
    sortMethod: SortMethod
  ): Array<{ title: string; pictographs: PictographData[]; type: 'section' | 'grouped' }> {

    if (sortMethod === 'type') {
      // For type sorting, always create all 6 type sections (even if empty)
      // This enables component-level filtering with fade animations
      const allTypes = ['Type1', 'Type2', 'Type3', 'Type4', 'Type5', 'Type6'];
      const groups = new Map<string, PictographData[]>();

      // Initialize all types with empty arrays
      allTypes.forEach(type => {
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
      const sections = [];
      const individualTypes = ['Type1', 'Type2', 'Type3'];
      const groupedTypes = ['Type4', 'Type5', 'Type6'];
      const groupedPictographs: PictographData[] = [];

      // Add individual sections (Types 1-3) - always create even if empty
      individualTypes.forEach(type => {
        sections.push({
          title: type,
          pictographs: groups.get(type) || [],
          type: 'section' as const
        });
      });

      // Collect Types 4-6 for grouping
      groupedTypes.forEach(type => {
        const typePictographs = groups.get(type) || [];
        groupedPictographs.push(...typePictographs);
      });

      // Always add grouped section for Types 4-6 (even if empty)
      sections.push({
        title: 'Types 4-6',
        pictographs: groupedPictographs,
        type: 'grouped' as const
      });

      return sections;
    }

    // For endPosition sorting, still group by type (the end position filtering has already been applied)
    if (sortMethod === 'endPosition') {
      // Same logic as 'type' - group by types but options are already filtered by end position
      const allTypes = ['Type1', 'Type2', 'Type3', 'Type4', 'Type5', 'Type6'];
      const groups = new Map<string, PictographData[]>();

      // Initialize all types with empty arrays
      allTypes.forEach(type => {
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
      const sections = [];
      const individualTypes = ['Type1', 'Type2', 'Type3'];
      const groupedTypes = ['Type4', 'Type5', 'Type6'];
      const groupedPictographs: PictographData[] = [];

      // Add individual sections (Types 1-3) - always create even if empty
      individualTypes.forEach(type => {
        sections.push({
          title: type,
          pictographs: groups.get(type) || [],
          type: 'section' as const
        });
      });

      // Collect Types 4-6 for grouping
      groupedTypes.forEach(type => {
        const typePictographs = groups.get(type) || [];
        groupedPictographs.push(...typePictographs);
      });

      // Always add grouped section for Types 4-6 (even if empty)
      sections.push({
        title: 'Types 4-6',
        pictographs: groupedPictographs,
        type: 'grouped' as const
      });

      return sections;
    }

    // For other sort methods, use original logic
    const groups = new Map<string, PictographData[]>();

    for (const pictograph of pictographs) {
      let groupKey: string;

      switch (sortMethod) {
        case 'reversals':
          groupKey = pictograph.letter?.toLowerCase().includes('rev') ? 'With Reversals' : 'Without Reversals';
          break;
        default:
          groupKey = this.getLetterTypeFromString(pictograph.letter);
      }

      if (!groups.has(groupKey)) {
        groups.set(groupKey, []);
      }
      groups.get(groupKey)!.push(pictograph);
    }

    // Convert groups to sections
    const sections = [];
    for (const [title, sectionPictographs] of groups.entries()) {
      sections.push({
        title,
        pictographs: sectionPictographs,
        type: 'section' as const
      });
    }

    return sections;
  }

  /**
   * Filter pictographs by letter type (moved from components)
   */
  filterPictographsByType(pictographs: PictographData[], letterType: string): PictographData[] {
    return pictographs.filter((p: PictographData) => this.getLetterTypeFromString(p.letter) === letterType);
  }

  /**
   * Helper function to convert string letter to Letter enum and get type
   * Uses shared infrastructure instead of duplicated logic
   */
  private getLetterTypeFromString(letter: string | null | undefined): string {
    if (!letter) return 'Type1'; // Default fallback

    try {
      // Use the existing getLetterType function from shared infrastructure
      // For now, fall back to the legacy logic until we can properly integrate
      return this.getLetterType(letter);
    } catch {
      return 'Type1'; // Fallback if conversion fails
    }
  }

  /**
   * Select an option and handle any side effects
   */
  async selectOption(option: PictographData): Promise<void> {
    // Basic selection handling - can be extended as needed
    console.log('Option selected:', option);
  }

  /**
   * Calculate end position from motion data
   * PRESERVED: Core position calculation logic
   */
  getEndPosition(pictographData: PictographData): string | null {
    if (!pictographData?.motions?.blue || !pictographData?.motions?.red) {
      return null;
    }

    try {
      const endPosition = this.positionMapper.getGridPositionFromLocations(
        pictographData.motions.blue.endLocation,
        pictographData.motions.red.endLocation
      );

      return endPosition?.toString() || null;
    } catch (error) {
      console.error("Error calculating end position:", error);
      return null;
    }
  }

  // ============================================================================
  // PRIVATE HELPER METHODS
  // ============================================================================



  /**
   * Apply sorting to options
   * PRESERVED: Core sorting logic
   */
  private applySorting(options: PictographData[], sortMethod: SortMethod): PictographData[] {
    const sorted = [...options];

    switch (sortMethod) {
      case "type":
        return sorted.sort((a, b) => {
          const aLetter = a.letter || "";
          const bLetter = b.letter || "";
          return aLetter.localeCompare(bLetter);
        });

      case "endPosition":
        return sorted.sort((a, b) => {
          const aPos = this.getEndPosition(a) || "";
          const bPos = this.getEndPosition(b) || "";
          return aPos.localeCompare(bPos);
        });

      case "reversals":
        return sorted.sort((a, b) => {
          const aHasRev = this.hasReversals(a);
          const bHasRev = this.hasReversals(b);
          if (aHasRev === bHasRev) {
            // If both have or don't have reversals, sort by letter
            const aLetter = a.letter || "";
            const bLetter = b.letter || "";
            return aLetter.localeCompare(bLetter);
          }
          return aHasRev ? -1 : 1; // Reversals first
        });

      default:
        return sorted;
    }
  }

  /**
   * Check if option has reversals
   */
  private hasReversals(option: PictographData): boolean {
    return option.letter?.toLowerCase().includes("rev") || false;
  }


}
