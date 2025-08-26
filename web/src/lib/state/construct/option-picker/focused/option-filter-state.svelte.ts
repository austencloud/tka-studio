/**
 * Option Filter State - Pure Svelte 5 Runes
 *
 * Handles filtering, sorting, and grouping logic using OptionsService.
 * Extracted from lines 60-85 of optionPickerRunes.svelte.ts
 */

import type { PictographData } from "$lib/domain/PictographData";
import {
  determineGroupKey,
  getSortedGroupKeys,
  getSorter,
  type OptionPickerGroupKey,
} from "$lib/services/implementations/construct/OptionsService";
import type { OptionDataState } from "./option-data-state.svelte";
import type { OptionUIState } from "./option-ui-state.svelte";

export function createOptionFilterState(
  dataState: OptionDataState,
  uiState: OptionUIState
) {
  // ===== Cached Grouped Options =====
  let cachedGroupedOptions = $state<Record<string, PictographData[]>>({});

  // ===== Derived Computations =====

  // Filtered and sorted options
  const filteredOptions = $derived(() => {
    const options = [...dataState.options];
    options.sort(getSorter(uiState.sortMethod, dataState.sequence));
    return options;
  });

  // Compute grouped options - only when explicitly needed
  function computeGroupedOptions(): Record<string, PictographData[]> {
    const groups: Record<string, PictographData[]> = {};
    const options = filteredOptions();
    options.forEach((option) => {
      const groupKey = determineGroupKey(
        option,
        uiState.sortMethod,
        dataState.sequence
      );
      if (!groups[groupKey]) groups[groupKey] = [];
      groups[groupKey].push(option);
    });

    const sortedKeys = getSortedGroupKeys(
      Object.keys(groups) as OptionPickerGroupKey[],
      uiState.sortMethod
    );
    const sortedGroups: Record<string, PictographData[]> = {};
    sortedKeys.forEach((key: string) => {
      if (groups[key]) {
        sortedGroups[key] = groups[key];
      }
    });
    cachedGroupedOptions = sortedGroups;
    return sortedGroups;
  }

  // Category keys available - simplified
  const categoryKeys = $derived(() => Object.keys(cachedGroupedOptions));

  // ===== Return Interface =====
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
}

export type OptionFilterState = ReturnType<typeof createOptionFilterState>;
