/**
 * Initialization Service
 *
 * Manages application initialization state and progress.
 * Clean separation of initialization logic from other concerns.
 */

import type { IAppStateInitializer } from "./app-state-interfaces";

class AppStateInitializer implements IAppStateInitializer {
  // Initialization state
  #isInitialized = $state<boolean>(false);
  #isInitializing = $state<boolean>(false);
  #initializationError = $state<string | null>(null);
  #initializationProgress = $state<number>(0);

  // ============================================================================
  // GETTERS
  // ============================================================================

  get isInitialized() {
    return this.#isInitialized;
  }

  get isInitializing() {
    return this.#isInitializing;
  }

  get initializationError() {
    return this.#initializationError;
  }

  get initializationProgress() {
    return this.#initializationProgress;
  }

  // Derived state
  get initializationComplete() {
    return this.#initializationProgress >= 100;
  }

  // ============================================================================
  // ACTIONS
  // ============================================================================

  setInitializationState(
    initialized: boolean,
    initializing: boolean,
    error: string | null = null,
    progress: number = 0
  ): void {
    this.#isInitialized = initialized;
    this.#isInitializing = initializing;
    this.#initializationError = error;
    this.#initializationProgress = progress;
  }

  setInitializationError(error: string): void {
    this.#initializationError = error;
    this.#isInitialized = false;
    this.#isInitializing = false;
  }

  setInitializationProgress(progress: number): void {
    this.#initializationProgress = progress;
  }

  resetInitializationState(): void {
    this.#isInitialized = false;
    this.#isInitializing = false;
    this.#initializationError = null;
    this.#initializationProgress = 0;
  }
}

// Export the class for DI container binding
// Singleton instance will be managed by the DI container
