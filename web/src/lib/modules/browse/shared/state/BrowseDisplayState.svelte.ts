/**
 * Browse Display State
 *
 * Focused microservice for managing browse UI display state.
 * Handles loading, error, and display settings without business logic.
 */

import type {
  GalleryDisplayState,
  GalleryLoadingState,
} from "$lib/modules/browse/gallery/domain";
import {
  createDefaultDisplayState,
  createDefaultLoadingState,
} from "$lib/modules/browse/gallery/domain";

export interface IGalleryDisplayState {
  // Reactive state getters
  readonly loadingState: GalleryLoadingState;
  readonly displayState: GalleryDisplayState;
  readonly isLoading: boolean;
  readonly hasError: boolean;

  // Loading actions
  setLoading(loading: boolean, operation?: string): void;
  setError(error: string | null): void;
  clearError(): void;

  // Display actions
  updateDisplaySettings(settings: Partial<GalleryDisplayState>): void;
  resetDisplayState(): void;
}

export class GalleryDisplayStateService implements IGalleryDisplayState {
  // Private reactive state
  #loadingState = $state<GalleryLoadingState>(createDefaultLoadingState());
  #displayState = $state<GalleryDisplayState>(createDefaultDisplayState());

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
      (this.#loadingState as GalleryLoadingState & { error: string | null })
        .error !== null
    );
  }

  // Loading actions
  setLoading(loading: boolean, operation?: string): void {
    this.#loadingState.isLoading = loading;
    if (operation) {
      (
        this.#loadingState as GalleryLoadingState & { currentOperation: string }
      ).currentOperation = operation;
    }
    if (loading) {
      (
        this.#loadingState as GalleryLoadingState & { error: string | null }
      ).error = null; // Clear error when starting new operation
    }
  }

  setError(error: string | null): void {
    (
      this.#loadingState as GalleryLoadingState & { error: string | null }
    ).error = error;
    this.#loadingState.isLoading = false; // Stop loading on error
  }

  clearError(): void {
    (
      this.#loadingState as GalleryLoadingState & { error: string | null }
    ).error = null;
  }

  // Display actions
  updateDisplaySettings(settings: Partial<GalleryDisplayState>): void {
    this.#displayState = { ...this.#displayState, ...settings };
  }

  resetDisplayState(): void {
    this.#displayState = createDefaultDisplayState();
  }
}
