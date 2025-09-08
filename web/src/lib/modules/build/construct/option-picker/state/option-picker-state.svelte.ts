/**
 * Enhanced Option Picker State - Pure Reactive Layer
 *
 * ✅ Gold Standard Implementation:
 * - Pure reactive state with Svelte 5 runes
 * - Dependency injection via parameters  
 * - Business logic delegated to services
 * - Professional error handling
 * - Validation boundaries enforced
 * - Clean separation of concerns
 */

import type { PictographData } from "$shared";
import type { OptionPickerLayoutCalculationResult } from "../domain";
import type { OptionPickerErrorType } from "../domain/errors/OptionPickerError";
import type { IOptionPickerServiceAdapter } from "../services/contracts";
import type { IOptionPickerErrorHandler } from "../services/contracts/IOptionPickerErrorHandler";
import type { IOptionPickerStateValidator } from "../services/implementations/OptionPickerStateValidator";

export interface OptionPickerStateConfig {
  optionPickerService: IOptionPickerServiceAdapter;
  errorHandler: IOptionPickerErrorHandler;
  validator: IOptionPickerStateValidator;
}

export interface OptionPickerComputedState {
  hasOptions: boolean;
  hasError: boolean;
  canSelectOptions: boolean;
  canRetryLastOperation: boolean;
  displayOptions: PictographData[];
  errorMessage: string | null;
  recoverySuggestions: string[];
}

export function createOptionPickerState(config: OptionPickerStateConfig) {
  const { optionPickerService, errorHandler, validator } = config;

  // ============================================================================
  // REACTIVE STATE (Pure Data)
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
  let error = $state<OptionPickerErrorType | null>(null);
  let lastOperation = $state<{ type: string; params: unknown } | null>(null);

  // Current sequence being processed
  let currentSequence = $state<PictographData[]>([]);
  let lastSequenceId = $state<string | null>(null);

  // Container dimensions
  let containerWidth = $state(0);
  let containerHeight = $state(0);

  // ============================================================================
  // DERIVED STATE (Pure Computed Values)
  // ============================================================================

  const computedState = $derived(() => {
    const hasOptions = options.length > 0;
    const hasError = error !== null;
    const canSelectOptions = hasOptions && !isLoading && !hasError;
    const canRetryLastOperation = hasError && error?.retryable === true && lastOperation !== null;
    
    const displayOptions = hasOptions ? 
      optionPickerService.getFilteredOptions(options, sortMethod, reversalFilter) : 
      [];

    const errorMessage = hasError && error ? errorHandler.getUserMessage(error) : null;
    const recoverySuggestions = hasError && error ? errorHandler.getRecoverySuggestions(error) : [];

    return {
      hasOptions,
      hasError,
      canSelectOptions,
      canRetryLastOperation,
      displayOptions,
      errorMessage,
      recoverySuggestions
    };
  });

  // ============================================================================
  // REACTIVE EFFECTS (Pure Side Effect Management)
  // ============================================================================

  // Update filtered options when dependencies change
  $effect(() => {
    console.log("🔍 OptionPickerState: Updating filtered options");
    filteredOptions = computedState().displayOptions;
  });

  // ============================================================================
  // STATE ACTIONS (Business Logic Delegation)
  // ============================================================================

  function validateAndSetContainerDimensions(width: number, height: number): boolean {
    // Skip validation if dimensions are not yet properly initialized
    if (width <= 0 || height <= 0) {
      console.log("🔍 OptionPickerState: Skipping validation for uninitialized dimensions:", { width, height });
      return false;
    }

    const validation = validator.validateContainerDimensions(width, height);
    if (!validation.isValid) {
      const validationError = errorHandler.handleError(
        new Error(validation.error),
        { width, height }
      );
      setError(validationError);
      return false;
    }

    containerWidth = width;
    containerHeight = height;
    return true;
  }

  function shouldReloadOptions(sequence: PictographData[]): boolean {
    const currentSequenceId = sequence[0]?.id || null;
    
    if (currentSequenceId === lastSequenceId) {
      console.log("🔍 OptionPickerState: Skipping reload - same sequence ID:", currentSequenceId);
      return false;
    }

    const validation = validator.validateSequenceChange(sequence, containerWidth, containerHeight);
    if (!validation.isValid) {
      const validationError = errorHandler.handleError(
        new Error(validation.error), 
        { sequence: sequence.length, containerWidth, containerHeight }
      );
      setError(validationError);
      return false;
    }

    return true;
  }

  async function loadOptionsForSequence(
    sequence: PictographData[],
    width: number,
    height: number
  ): Promise<void> {
    if (isLoading) {
      console.log("🔍 OptionPickerState: Already loading, skipping");
      return;
    }

    try {
      console.log("🔍 OptionPickerState: Starting load");
      
      // Validate dimensions first
      if (!validateAndSetContainerDimensions(width, height)) {
        return;
      }

      // Check if reload is needed
      if (!shouldReloadOptions(sequence)) {
        return;
      }

      isLoading = true;
      error = null;
      currentSequence = sequence;
      lastSequenceId = sequence[0]?.id || null;

      // Store operation for retry capability
      lastOperation = { 
        type: 'loadOptions', 
        params: { sequence: sequence.length, width, height } 
      };

      // Delegate to service adapter
      const result = await optionPickerService.initializeOptionPicker(
        sequence,
        width,
        height
      );

      options = result.options;
      layout = result.layout;
      
      console.log("🔍 OptionPickerState: Loaded", options.length, "options");
      
    } catch (err) {
      const handledError = errorHandler.handleError(err, {
        operation: 'loadOptionsForSequence',
        sequenceLength: sequence.length,
        containerWidth: width,
        containerHeight: height
      });
      
      setError(handledError);
      errorHandler.logError(handledError);
      
    } finally {
      isLoading = false;
    }
  }

  async function selectOption(option: PictographData): Promise<PictographData> {
    try {
      // Validate selection
      const validation = validator.validateOptionSelection(option, computedState().displayOptions);
      if (!validation.isValid) {
        throw new Error(validation.error);
      }

      // Delegate to service
      await optionPickerService.selectOption(option);
      
      console.log("🔍 OptionPickerState: Option selected:", option.letter);
      return option;
      
    } catch (err) {
      const handledError = errorHandler.handleError(err, {
        operation: 'selectOption',
        option: option.letter
      });
      
      setError(handledError);
      errorHandler.logError(handledError);
      throw handledError;
    }
  }

  function setSortMethod(method: string): void {
    sortMethod = method;
    console.log("🔍 OptionPickerState: Sort method changed to:", method);
  }

  function setReversalFilter(filter: string): void {
    reversalFilter = filter;
    console.log("🔍 OptionPickerState: Reversal filter changed to:", filter);
  }

  function recalculateLayout(width: number, height: number): void {
    if (!validateAndSetContainerDimensions(width, height)) {
      return;
    }

    if (options.length > 0) {
      layout = optionPickerService.calculateLayout({
        count: options.length,
        containerWidth: width,
        containerHeight: height,
      });
      console.log("🔍 OptionPickerState: Layout recalculated");
    }
  }

  function clearError(): void {
    error = null;
    console.log("🔍 OptionPickerState: Error cleared");
  }

  async function retryLastOperation(): Promise<void> {
    if (!lastOperation || !error?.retryable) {
      console.warn("🔍 OptionPickerState: Cannot retry - no retryable operation available");
      return;
    }

    console.log("🔍 OptionPickerState: Retrying last operation:", lastOperation.type);

    switch (lastOperation.type) {
      case 'loadOptions':
        await loadOptionsForSequence(currentSequence, containerWidth, containerHeight);
        break;
      default:
        console.warn("🔍 OptionPickerState: Unknown operation type for retry:", lastOperation.type);
    }
  }

  function setError(newError: OptionPickerErrorType): void {
    error = newError;
    isLoading = false;
  }

  // ============================================================================
  // PUBLIC API (Readonly Access + Actions)
  // ============================================================================

  return {
    // Readonly state access
    get options() { return options; },
    get layout() { return layout; },
    get filteredOptions() { return filteredOptions; },
    get sortMethod() { return sortMethod; },
    get reversalFilter() { return reversalFilter; },
    get isLoading() { return isLoading; },
    get error() { return error; },
    get currentSequence() { return currentSequence; },
    get containerWidth() { return containerWidth; },
    get containerHeight() { return containerHeight; },

    // Computed state
    get state() { return computedState; },

    // Validation methods
    shouldReloadOptions,
    validateAndSetContainerDimensions,

    // Actions
    loadOptionsForSequence,
    selectOption,
    setSortMethod,
    setReversalFilter,
    recalculateLayout,
    clearError,
    retryLastOperation,

    // Legacy compatibility (deprecated - use state.*)
    get hasOptions() { return computedState().hasOptions; },
    get hasError() { return computedState().hasError; },
    get canSelectOptions() { return computedState().canSelectOptions; },
  };
}

export type OptionPickerState = ReturnType<typeof createOptionPickerState>;
