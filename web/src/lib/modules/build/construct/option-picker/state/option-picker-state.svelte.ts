/**
 * Option Picker State - Business Logic State
 *
 * Manages state for the option picker functionality.
 * Handles option loading, filtering, sorting, and selection logic.
 *
 * ✅ All option picker runes ($state, $derived, $effect) live here
 * ✅ Pure reactive wrappers - no business logic
 * ✅ Services injected via parameters
 * ✅ Component-scoped state (not global singleton)
 */

import type {
  OptionPickerLayoutCalculationResult,
} from "$build/domain";
import type { PictographData } from "$shared/domain";
import { OptionPickerServiceAdapter } from "../../../shared/services/implementations";

export function createOptionPickerState() {
  // Service adapter for business logic
  const optionPickerService = new OptionPickerServiceAdapter();

  // ============================================================================
  // REACTIVE STATE
  // ============================================================================

  // Core option data
  let options = $state<PictographData[]>([]);
  let layout = $state<OptionPickerLayoutCalculationResult | null>(null);
  let filteredOptions = $state<PictographData[]>([]);

  // Filtering and sorting state
  let sortMethod = $state("alphabetical");
  let reversalFilter = $state("all");

  // Loading and error state
  let isLoading = $state(false);
  let error = $state<string | null>(null);

  // Current sequence being processed
  let currentSequence = $state<PictographData[]>([]);

  // ============================================================================
  // DERIVED STATE
  // ============================================================================

  const hasOptions = $derived(options.length > 0);
  const hasError = $derived(error !== null);
  const canSelectOptions = $derived(hasOptions && !isLoading && !hasError);

  // ============================================================================
  // REACTIVE EFFECTS
  // ============================================================================

  // Update filtered options when dependencies change
  $effect(() => {
    if (options.length > 0) {
      const filtered = optionPickerService.getFilteredOptions(
        options,
        sortMethod,
        reversalFilter
      );
      filteredOptions = filtered;
    } else {
      filteredOptions = [];
    }
  });

  // ============================================================================
  // ACTIONS
  // ============================================================================

  async function loadOptionsForSequence(
    sequence: PictographData[],
    containerWidth: number,
    containerHeight: number
  ) {
    if (isLoading) return; // Prevent multiple simultaneous loads

    try {
      isLoading = true;
      error = null;
      currentSequence = sequence;

      // Use the service adapter for coordinated initialization
      const result = await optionPickerService.initializeOptionPicker(
        sequence,
        containerWidth,
        containerHeight
      );

      options = result.options;
      layout = result.layout;
    } catch (err) {
      error = err instanceof Error ? err.message : "Failed to load options";
      console.error("Failed to load options:", err);
    } finally {
      isLoading = false;
    }
  }

  async function selectOption(option: PictographData) {
    try {
      await optionPickerService.selectOption(option);
      return option;
    } catch (err) {
      error = err instanceof Error ? err.message : "Failed to select option";
      console.error("Failed to select option:", err);
      throw err;
    }
  }

  function setSortMethod(method: string) {
    sortMethod = method;
  }

  function setReversalFilter(filter: string) {
    reversalFilter = filter;
  }

  function recalculateLayout(containerWidth: number, containerHeight: number) {
    if (options.length > 0) {
      layout = optionPickerService.calculateLayout({
        count: options.length,
        containerWidth,
        containerHeight,
      });
    }
  }

  function clearError() {
    error = null;
  }

  function retryLoading(containerWidth: number, containerHeight: number) {
    loadOptionsForSequence(currentSequence, containerWidth, containerHeight);
  }

  // ============================================================================
  // PUBLIC API
  // ============================================================================

  return {
    // Readonly state access
    get options() {
      return options;
    },
    get layout() {
      return layout;
    },
    get filteredOptions() {
      return filteredOptions;
    },
    get sortMethod() {
      return sortMethod;
    },
    get reversalFilter() {
      return reversalFilter;
    },
    get isLoading() {
      return isLoading;
    },
    get error() {
      return error;
    },
    get currentSequence() {
      return currentSequence;
    },

    // Derived state
    get hasOptions() {
      return hasOptions;
    },
    get hasError() {
      return hasError;
    },
    get canSelectOptions() {
      return canSelectOptions;
    },

    // Actions
    loadOptionsForSequence,
    selectOption,
    setSortMethod,
    setReversalFilter,
    recalculateLayout,
    clearError,
    retryLoading,
  };
}
