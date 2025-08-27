/**
 * Unit tests for option-filter-state.svelte.ts
 */

import { beforeEach, describe, expect, it, vi } from "vitest";
import { createOptionFilterState } from "../../../../../../src/lib/components/construct/option-picker/state/focused/option-filter-state.svelte";

// Mock pictograph data for testing
interface MockPictographData {
  id: string;
  letter: string;
  category?: string;
}

// Mock the filter state module
vi.mock(
  "../../../../../../src/lib/components/construct/option-picker/state/focused/option-filter-state.svelte",
  () => {
    const mockGetSorter =
      () => (a: MockPictographData, b: MockPictographData) =>
        a.letter.localeCompare(b.letter);
    const mockDetermineGroupKey = (option: MockPictographData) =>
      option.category || "default";
    const mockGetSortedGroupKeys = (keys: string[]) => keys.sort();

    return {
      createOptionFilterState: (dataState: any, _uiState: any) => {
        let cachedGroupedOptions: Record<string, MockPictographData[]> = {};

        const filteredOptions = () => {
          const options = [...dataState.options];
          options.sort(mockGetSorter());
          return options;
        };

        const computeGroupedOptions = () => {
          const groups: Record<string, MockPictographData[]> = {};
          const options = filteredOptions();

          options.forEach((option) => {
            const groupKey = mockDetermineGroupKey(option);
            if (!groups[groupKey]) groups[groupKey] = [];
            groups[groupKey].push(option);
          });

          const sortedKeys = mockGetSortedGroupKeys(Object.keys(groups));
          const sortedGroups: Record<string, MockPictographData[]> = {};
          sortedKeys.forEach((key: string) => {
            if (groups[key]) {
              sortedGroups[key] = groups[key];
            }
          });

          cachedGroupedOptions = sortedGroups;
          return sortedGroups;
        };

        const categoryKeys = () => Object.keys(cachedGroupedOptions);

        return {
          get filteredOptions() {
            return filteredOptions();
          },
          get groupedOptions() {
            return computeGroupedOptions();
          },
          get categoryKeys() {
            return categoryKeys();
          },
        };
      },
    };
  }
);

describe("createOptionFilterState", () => {
  let mockDataState: any;
  let mockUIState: any;
  let filterState: any;

  beforeEach(() => {
    // Mock data state
    mockDataState = {
      options: [
        { id: "1", letter: "A", category: "vowels" },
        { id: "2", letter: "B", category: "consonants" },
        { id: "3", letter: "C", category: "consonants" },
        { id: "4", letter: "E", category: "vowels" },
      ] as MockPictographData[],
      sequence: [] as MockPictographData[],
    };

    // Mock UI state
    mockUIState = {
      sortMethod: "type",
    };

    // Create filter state
    const {
      createOptionFilterState,
    } = require("../../../../../../src/lib/components/construct/option-picker/state/focused/option-filter-state.svelte");
    filterState = createOptionFilterState(mockDataState, mockUIState);
  });

  describe("filteredOptions", () => {
    it("should return sorted options", () => {
      const filtered = filterState.filteredOptions;

      expect(filtered).toHaveLength(4);
      expect(filtered[0].letter).toBe("A");
      expect(filtered[1].letter).toBe("B");
      expect(filtered[2].letter).toBe("C");
      expect(filtered[3].letter).toBe("E");
    });

    it("should update when data state options change", () => {
      mockDataState.options = [
        { id: "1", letter: "Z", category: "consonants" },
        { id: "2", letter: "A", category: "vowels" },
      ];

      const filtered = filterState.filteredOptions;

      expect(filtered).toHaveLength(2);
      expect(filtered[0].letter).toBe("A");
      expect(filtered[1].letter).toBe("Z");
    });
  });

  describe("groupedOptions", () => {
    it("should group options by category", () => {
      const grouped = filterState.groupedOptions;

      expect(grouped).toHaveProperty("vowels");
      expect(grouped).toHaveProperty("consonants");

      expect(grouped.vowels).toHaveLength(2);
      expect(grouped.consonants).toHaveLength(2);

      // Check specific items
      expect(grouped.vowels.map((o: MockPictographData) => o.letter)).toEqual([
        "A",
        "E",
      ]);
      expect(
        grouped.consonants.map((o: MockPictographData) => o.letter)
      ).toEqual(["B", "C"]);
    });

    it("should handle options without categories", () => {
      mockDataState.options = [
        { id: "1", letter: "X" }, // No category
        { id: "2", letter: "Y", category: "special" },
      ];

      const grouped = filterState.groupedOptions;

      expect(grouped).toHaveProperty("default");
      expect(grouped).toHaveProperty("special");
      expect(grouped.default[0].letter).toBe("X");
      expect(grouped.special[0].letter).toBe("Y");
    });

    it("should update cache when called", () => {
      // First call should populate cache
      const grouped1 = filterState.groupedOptions;
      expect(filterState.categoryKeys).toEqual(["consonants", "vowels"]);

      // Change data
      mockDataState.options = [{ id: "1", letter: "X", category: "special" }];

      // Second call should update cache
      const grouped2 = filterState.groupedOptions;
      expect(filterState.categoryKeys).toEqual(["special"]);
    });
  });

  describe("categoryKeys", () => {
    it("should return sorted category keys", () => {
      // Trigger grouping first
      filterState.groupedOptions;

      const keys = filterState.categoryKeys;
      expect(keys).toEqual(["consonants", "vowels"]);
    });

    it("should return empty array when no groups exist", () => {
      mockDataState.options = [];

      // Trigger grouping with empty options
      filterState.groupedOptions;

      const keys = filterState.categoryKeys;
      expect(keys).toEqual([]);
    });

    it("should update when grouping changes", () => {
      // Initial grouping
      filterState.groupedOptions;
      expect(filterState.categoryKeys).toEqual(["consonants", "vowels"]);

      // Change data to different categories
      mockDataState.options = [
        { id: "1", letter: "X", category: "numbers" },
        { id: "2", letter: "Y", category: "symbols" },
      ];

      // Re-group and check keys
      filterState.groupedOptions;
      expect(filterState.categoryKeys).toEqual(["numbers", "symbols"]);
    });
  });

  describe("reactive behavior", () => {
    it("should reflect changes in data state options", () => {
      expect(filterState.filteredOptions).toHaveLength(4);

      // Add new option
      mockDataState.options.push({
        id: "5",
        letter: "D",
        category: "consonants",
      });

      expect(filterState.filteredOptions).toHaveLength(5);
      expect(
        filterState.filteredOptions.find(
          (o: MockPictographData) => o.letter === "D"
        )
      ).toBeDefined();
    });

    it("should handle empty options gracefully", () => {
      mockDataState.options = [];

      expect(filterState.filteredOptions).toEqual([]);
      expect(filterState.groupedOptions).toEqual({});
      expect(filterState.categoryKeys).toEqual([]);
    });
  });
});
