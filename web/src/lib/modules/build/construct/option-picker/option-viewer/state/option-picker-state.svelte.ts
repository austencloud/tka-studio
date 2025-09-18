/**
 * Option Picker State
 * 
 * Factory function for creating option picker reactive state.
 * Follows the same pattern as the simplified start position picker.
 */

import type { PictographData } from "../../../../../../shared";
import type { OptionPickerState, SortMethod, TypeFilter } from "../domain/option-picker-types";
import type { OptionPickerLayout, OptionPickerStateConfig } from "../domain/option-viewer-models";

export function createOptionPickerState(config: OptionPickerStateConfig) {
  const { optionPickerService } = config;

  // Core reactive state
  let state = $state<OptionPickerState>('ready');
  let options = $state<PictographData[]>([]);
  let error = $state<string | null>(null);
  let sortMethod = $state<SortMethod>('type');
  let lastSequenceId = $state<string | null>(null); // Track last loaded sequence

  // Type filter state - all enabled by default
  let typeFilter = $state<TypeFilter>({
    type1: true, // Dual-Shift (A-V)
    type2: true, // Shift (W, X, Y, Z, Σ, Δ, θ, Ω)
    type3: true, // Cross-Shift (W-, X-, Y-, Z-, Σ-, Δ-, θ-, Ω-)
    type4: true, // Dash (Φ, Ψ, Λ)
    type5: true, // Dual-Dash (Φ-, Ψ-, Λ-)
    type6: true, // Static (α, β, Γ)
  });

  // New secondary filter states for different sort methods
  let endPositionFilter = $state({
    alpha: true,
    beta: true,
    gamma: true,
  });

  let reversalFilter = $state({
    continuous: true,
    '1-reversal': true,
    '2-reversals': true,
  });

  let layout = $state<OptionPickerLayout>({
    optionsPerRow: 4,
    optionSize: 100,
    gridGap: '8px',
    gridColumns: 'repeat(4, 1fr)',
    containerWidth: 800,
    containerHeight: 600
  });

  // Computed state
  const isLoading = $derived(() => state === 'loading');
  const hasError = $derived(() => state === 'error');
  const hasOptions = $derived(() => options.length > 0);

  const filteredOptions = $derived(() => {
    if (!hasOptions) {
      return [];
    }
    
    // Prepare filters based on current sort method
    let activeTypeFilter: TypeFilter | undefined;
    let activeEndPositionFilter: typeof endPositionFilter | undefined;
    let activeReversalFilter: typeof reversalFilter | undefined;
    
    switch (sortMethod) {
      case 'type':
        activeTypeFilter = typeFilter;
        break;
      case 'endPosition':
        activeEndPositionFilter = endPositionFilter;
        break;
      case 'reversals':
        activeReversalFilter = reversalFilter;
        break;
    }
    
    return optionPickerService.getFilteredOptions(
      options, 
      sortMethod, 
      activeTypeFilter, 
      activeEndPositionFilter, 
      activeReversalFilter
    );
  });

  // Actions
  async function loadOptions(sequence: PictographData[]) {
    if (state === 'loading') return; // Prevent concurrent loads

    // Create a simple sequence ID to prevent reloading the same sequence
    const sequenceId = sequence.length > 0 ?
      `${sequence.length}-${sequence[sequence.length - 1]?.id || 'empty'}` :
      'empty';

    if (lastSequenceId === sequenceId) {
      return; // Skip reload for same sequence
    }

    state = 'loading';
    error = null;
    lastSequenceId = sequenceId;

    try {
      const newOptions = await optionPickerService.loadOptionsFromSequence(sequence);

      options = newOptions;
      state = 'ready';
    } catch (err) {
      console.error("Failed to load options:", err);
      error = err instanceof Error ? err.message : 'Failed to load options';
      state = 'error';
      options = [];
    }
  }

  function setSortMethod(method: SortMethod) {
    sortMethod = method;
  }

  function toggleTypeFilter(typeNumber: number) {
    const typeKey = `type${typeNumber}` as keyof TypeFilter;
    typeFilter[typeKey] = !typeFilter[typeKey];
  }

  function toggleSecondaryFilter(filterKey: string) {
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

  function clearSecondaryFilters() {
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

  function getCurrentSecondaryFilters(): Record<string, boolean> {
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



  async function selectOption(option: PictographData) {
    try {
      await optionPickerService.selectOption(option);
    } catch (err) {
      console.error("Failed to select option:", err);
      error = err instanceof Error ? err.message : 'Failed to select option';
    }
  }

  function clearError() {
    error = null;
    if (state === 'error') {
      state = 'ready';
    }
  }

  function reset() {
    state = 'ready';
    options = [];
    error = null;
    sortMethod = 'type';
    lastSequenceId = null; // Clear sequence tracking
    
    // Reset all filters to enabled
    typeFilter = {
      type1: true,
      type2: true,
      type3: true,
      type4: true,
      type5: true,
      type6: true,
    };
    endPositionFilter = {
      alpha: true,
      beta: true,
      gamma: true,
    };
    reversalFilter = {
      continuous: true,
      '1-reversal': true,
      '2-reversals': true,
    };
  }

  // Return the state interface
  return {
    // State getters
    get state() { return state; },
    get options() { return options; },
    get error() { return error; },
    get sortMethod() { return sortMethod; },
    get typeFilter() { return typeFilter; },
    get endPositionFilter() { return endPositionFilter; },
    get reversalFilter() { return reversalFilter; },

    get layout() { return layout; },

    // Computed getters
    get isLoading() { return isLoading(); },
    get hasError() { return hasError(); },
    get hasOptions() { return hasOptions(); },
    get filteredOptions() { return filteredOptions(); },

    // Actions
    loadOptions,
    setSortMethod,
    toggleTypeFilter,
    toggleSecondaryFilter,
    clearSecondaryFilters,
    getCurrentSecondaryFilters,
    selectOption,
    clearError,
    reset
  };
}
