/**
 * FilterManager - Manages all filter-related state and operations
 *
 * Extracted from option-picker-state.svelte.ts to reduce complexity.
 * Handles type filters, end position filters, and reversal filters.
 */

import type { SortMethod, TypeFilter } from "../domain/option-picker-types";

export interface FilterState {
  typeFilter: TypeFilter;
  endPositionFilter: Record<string, boolean>;
  reversalFilter: Record<string, boolean>;
}

export function createFilterManager() {
  // Type filter state - all enabled by default
  let typeFilter = $state<TypeFilter>({
    type1: true, // Dual-Shift (A-V)
    type2: true, // Shift (W, X, Y, Z, Σ, Δ, θ, Ω)
    type3: true, // Cross-Shift (W-, X-, Y-, Z-, Σ-, Δ-, θ-, Ω-)
    type4: true, // Dash (Φ, Ψ, Λ)
    type5: true, // Dual-Dash (Φ-, Ψ-, Λ-)
    type6: true, // Static (α, β, Γ)
  });

  // End position filter state
  let endPositionFilter = $state({
    alpha: true,
    beta: true,
    gamma: true,
  });

  // Reversal filter state
  let reversalFilter = $state({
    continuous: true,
    '1-reversal': true,
    '2-reversals': true,
  });

  /**
   * Get the current filter state based on sort method
   */
  function getCurrentFilters(sortMethod: SortMethod): Record<string, boolean> {
    switch (sortMethod) {
      case 'type':
        return typeFilter;
      case 'endPosition':
        return endPositionFilter;
      case 'reversals':
        return reversalFilter;
      default:
        return {};
    }
  }

  /**
   * Toggle a specific filter based on sort method
   */
  function toggleFilter(sortMethod: SortMethod, filterKey: string): void {
    switch (sortMethod) {
      case 'type':
        if (filterKey in typeFilter) {
          const key = filterKey as keyof TypeFilter;
          typeFilter[key] = !typeFilter[key];
        }
        break;
      case 'endPosition':
        if (filterKey in endPositionFilter) {
          endPositionFilter[filterKey as keyof typeof endPositionFilter] =
            !endPositionFilter[filterKey as keyof typeof endPositionFilter];
        }
        break;
      case 'reversals':
        if (filterKey in reversalFilter) {
          reversalFilter[filterKey as keyof typeof reversalFilter] =
            !reversalFilter[filterKey as keyof typeof reversalFilter];
        }
        break;
    }
  }

  /**
   * Clear all filters for the current sort method
   */
  function clearFilters(sortMethod: SortMethod): void {
    switch (sortMethod) {
      case 'type':
        Object.keys(typeFilter).forEach(key => {
          typeFilter[key as keyof TypeFilter] = true;
        });
        break;
      case 'endPosition':
        Object.keys(endPositionFilter).forEach(key => {
          endPositionFilter[key as keyof typeof endPositionFilter] = true;
        });
        break;
      case 'reversals':
        Object.keys(reversalFilter).forEach(key => {
          reversalFilter[key as keyof typeof reversalFilter] = true;
        });
        break;
    }
  }

  /**
   * Clear all filters across all sort methods
   */
  function clearAllFilters(): void {
    // Reset all filters to enabled
    Object.assign(typeFilter, {
      type1: true,
      type2: true,
      type3: true,
      type4: true,
      type5: true,
      type6: true,
    });
    Object.assign(endPositionFilter, {
      alpha: true,
      beta: true,
      gamma: true,
    });
    Object.assign(reversalFilter, {
      continuous: true,
      '1-reversal': true,
      '2-reversals': true,
    });
  }

  /**
   * Check if any filters are currently active (disabled)
   */
  function hasActiveFilters(currentFilters: Record<string, boolean>): boolean {
    return Object.values(currentFilters).some(active => !active);
  }

  /**
   * Get the current filter state for serialization/persistence
   */
  function getFilterState(): FilterState {
    return {
      typeFilter: { ...typeFilter },
      endPositionFilter: { ...endPositionFilter },
      reversalFilter: { ...reversalFilter },
    };
  }

  /**
   * Restore filter state from serialized data
   */
  function restoreFilterState(state: FilterState): void {
    Object.assign(typeFilter, state.typeFilter);
    Object.assign(endPositionFilter, state.endPositionFilter);
    Object.assign(reversalFilter, state.reversalFilter);
  }

  return {
    get typeFilter() { return typeFilter; },
    get endPositionFilter() { return endPositionFilter; },
    get reversalFilter() { return reversalFilter; },
    getCurrentFilters,
    toggleFilter,
    clearFilters,
    clearAllFilters,
    hasActiveFilters,
    getFilterState,
    restoreFilterState,
  };
}
