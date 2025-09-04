/**
 * Browse Display State
 *
 * Focused microservice for managing browse UI display state.
 * Handles loading, error, and display settings without business logic.
 */

import type { BrowseDisplayState, BrowseLoadingState } from "$browse/domain";
import {
  createDefaultDisplayState,
  createDefaultLoadingState,
} from "$browse/domain";

export interface IBrowseDisplayState {
  // Reactive state getters
  readonly loadingState: BrowseLoadingState;
  readonly displayState: BrowseDisplayState;
  readonly isLoading: boolean;
  readonly hasError: boolean;

  // Loading actions
  setLoading(loading: boolean, operation?: string): void;
  setError(error: string | null): void;
  clearError(): void;

  // Display actions
  updateDisplaySettings(settings: Partial<BrowseDisplayState>): void;
  resetDisplayState(): void;
}

export class BrowseDisplayStateService implements IBrowseDisplayState {
  // Private reactive state
  #loadingState = $state<BrowseLoadingState>(createDefaultLoadingState());
  #displayState = $state<BrowseDisplayState>(createDefaultDisplayState());

  // Reactive getters
  get loadingState() {
    return this.#loadingState;
  }

  get displayState() {
    return this.#displayState;
  }

  get isLoading() {
    return this.#loadingState.isLoading;
  }

  get hasError() {
    return (
      (this.#loadingState as BrowseLoadingState & { error: string | null })
        .error !== null
    );
  }

  // Loading actions
  setLoading(loading: boolean, operation?: string): void {
    this.#loadingState.isLoading = loading;
    if (operation) {
      (
        this.#loadingState as BrowseLoadingState & { currentOperation: string }
      ).currentOperation = operation;
    }
    if (loading) {
      (
        this.#loadingState as BrowseLoadingState & { error: string | null }
      ).error = null; // Clear error when starting new operation
    }
  }

  setError(error: string | null): void {
    (
      this.#loadingState as BrowseLoadingState & { error: string | null }
    ).error = error;
    this.#loadingState.isLoading = false; // Stop loading on error
  }

  clearError(): void {
    (
      this.#loadingState as BrowseLoadingState & { error: string | null }
    ).error = null;
  }

  // Display actions
  updateDisplaySettings(settings: Partial<BrowseDisplayState>): void {
    this.#displayState = { ...this.#displayState, ...settings };
  }

  resetDisplayState(): void {
    this.#displayState = createDefaultDisplayState();
  }
}
