/**
 * FilterLabelMapper - Utility for converting filter keys to readable labels
 *
 * Provides centralized mapping of filter keys to user-friendly display labels.
 * Extracted from OptionViewer for reusability and maintainability.
 */

export interface FilterLabelMapper {
  /**
   * Convert filter key to readable label
   */
  mapFilterKeyToLabel(key: string): string;

  /**
   * Convert multiple filter keys to readable labels
   */
  mapFilterKeysToLabels(keys: string[]): string[];

  /**
   * Get all available filter labels with their keys
   */
  getAllFilterLabels(): Record<string, string>;
}

export class FilterLabelMapperImpl implements FilterLabelMapper {
  private readonly labelMap: Record<string, string> = {
    // Type filters
    type1: "Type 1",
    type2: "Type 2",
    type3: "Type 3",
    type4: "Type 4",
    type5: "Type 5",
    type6: "Type 6",

    // End position filters
    alpha: "Alpha",
    beta: "Beta",
    gamma: "Gamma",

    // Reversal filters
    continuous: "Continuous",
    "1-reversal": "1-Rev",
    "2-reversals": "2-Rev",
  };

  mapFilterKeyToLabel(key: string): string {
    return this.labelMap[key] || key;
  }

  mapFilterKeysToLabels(keys: string[]): string[] {
    return keys.map((key) => this.mapFilterKeyToLabel(key));
  }

  getAllFilterLabels(): Record<string, string> {
    return { ...this.labelMap };
  }
}

// Factory function for creating the mapper
export function createFilterLabelMapper(): FilterLabelMapper {
  return new FilterLabelMapperImpl();
}
