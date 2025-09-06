/**
 * Application State Service Implementation
 *
 * Handles core application lifecycle state
 */

// import type { IAppStateInitializer } from "$state/app-state-interfaces";

// Temporary interface definition
interface IApplicationStateService {
  isFullScreen: boolean;
  theme: any;
  toggleFullScreen(): void;
  setTheme(theme: any): void;
}
import { injectable } from "inversify";

// Temporary interface definition
interface IAppStateInitializer {
  initialize(): Promise<void>;
  isInitialized: boolean;
}

@injectable()
export class ApplicationStateService implements IAppStateInitializer {
  // Core application state
  private state = $state({
    isInitialized: false,
    isInitializing: false,
    initializationError: null as string | null,
    initializationProgress: 0,
    isFullScreen: false,
    isTransitioning: false,
  });

  // Interface implementation - readonly getters
  get isInitialized(): boolean {
    return this.state.isInitialized;
  }

  get isInitializing(): boolean {
    return this.state.isInitializing;
  }

  get initializationError(): string | null {
    return this.state.initializationError;
  }

  get initializationProgress(): number {
    return this.state.initializationProgress;
  }

  get initializationComplete(): boolean {
    return (
      this.state.isInitialized &&
      !this.state.isInitializing &&
      !this.state.initializationError
    );
  }

  // Legacy getters (for backward compatibility)
  getIsInitialized(): boolean {
    return this.state.isInitialized;
  }

  getIsInitializing(): boolean {
    return this.state.isInitializing;
  }

  getInitializationError(): string | null {
    return this.state.initializationError;
  }

  getInitializationProgress(): number {
    return this.state.initializationProgress;
  }

  async initialize(): Promise<void> {
    this.state.isInitializing = true;
    this.state.initializationError = null;

    try {
      // Initialization logic would go here
      this.state.initializationProgress = 100;
      this.state.isInitialized = true;
    } catch (error) {
      this.state.initializationError =
        error instanceof Error ? error.message : String(error);
    } finally {
      this.state.isInitializing = false;
    }
  }

  getIsFullScreen(): boolean {
    return this.state.isFullScreen;
  }

  getIsTransitioning(): boolean {
    return this.state.isTransitioning;
  }

  // Derived state
  getIsReady(): boolean {
    return (
      this.state.isInitialized &&
      !this.state.isInitializing &&
      !this.state.initializationError
    );
  }

  getCanUseApp(): boolean {
    return this.getIsReady();
  }

  getInitializationComplete(): boolean {
    return this.state.initializationProgress >= 100;
  }

  // Actions
  setInitializationState(
    initialized: boolean,
    initializing: boolean,
    error: string | null = null,
    progress: number = 0
  ): void {
    this.state.isInitialized = initialized;
    this.state.isInitializing = initializing;
    this.state.initializationError = error;
    this.state.initializationProgress = progress;
  }

  setInitializationError(error: string): void {
    this.state.initializationError = error;
    this.state.isInitialized = false;
    this.state.isInitializing = false;
  }

  setInitializationProgress(progress: number): void {
    this.state.initializationProgress = progress;
  }

  resetInitializationState(): void {
    this.state.isInitialized = false;
    this.state.isInitializing = false;
    this.state.initializationError = null;
    this.state.initializationProgress = 0;
  }

  setFullScreen(fullScreen: boolean): void {
    this.state.isFullScreen = fullScreen;
  }

  setIsTransitioning(isTransitioning: boolean): void {
    this.state.isTransitioning = isTransitioning;
  }

  // Utilities
  getStateSnapshot() {
    return {
      isInitialized: this.state.isInitialized,
      isInitializing: this.state.isInitializing,
      initializationError: this.state.initializationError,
      initializationProgress: this.state.initializationProgress,
      isFullScreen: this.state.isFullScreen,
      isTransitioning: this.state.isTransitioning,
    };
  }

  resetState(): void {
    this.state.isInitialized = false;
    this.state.isInitializing = false;
    this.state.initializationError = null;
    this.state.initializationProgress = 0;
    this.state.isFullScreen = false;
    this.state.isTransitioning = false;
  }
}
