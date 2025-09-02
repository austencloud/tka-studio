/**
 * Browse Display State Service
 *
 * Focused microservice for managing browse UI display state.
 * Handles loading, error, and display settings without business logic.
 */

import type { BrowseDisplayState, BrowseLoadingState } from "$domain";
import { createDefaultDisplayState, createDefaultLoadingState } from "$domain";

export interface IBrowseDisplayStateService {
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

export class BrowseDisplayStateService implements IBrowseDisplayStateService {
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
    return this.#loadingState.error !== null;
  }

  // Loading actions
  setLoading(loading: boolean, operation?: string): void {
    this.#loadingState.isLoading = loading;
    if (operation) {
      this.#loadingState.currentOperation = operation;
    }
    if (loading) {
      this.#loadingState.error = null; // Clear error when starting new operation
    }
  }

  setError(error: string | null): void {
    this.#loadingState.error = error;
    this.#loadingState.isLoading = false; // Stop loading on error
  }

  clearError(): void {
    this.#loadingState.error = null;
  }

  // Display actions
  updateDisplaySettings(settings: Partial<BrowseDisplayState>): void {
    this.#displayState = { ...this.#displayState, ...settings };
  }

  resetDisplayState(): void {
    this.#displayState = createDefaultDisplayState();
  }
}
