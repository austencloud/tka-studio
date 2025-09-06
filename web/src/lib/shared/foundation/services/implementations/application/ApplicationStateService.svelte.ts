/**
 * Application State Service
 *
 * Manages core UI state like full screen, transitions, and settings dialog visibility.
 * Clean and focused on UI state only.
 */

// import type {
//   IApplicationStateService,
//   Theme,
// } from "$state/app-state-interfaces";

// Temporary interface definitions
interface IApplicationStateService {
  isFullScreen: boolean;
  theme: Theme;
  toggleFullScreen(): void;
  setTheme(theme: Theme): void;
}

enum Theme {
  LIGHT = "light",
  DARK = "dark",
  AUTO = "auto",
}

class ApplicationStateService implements IApplicationStateService {
  // Core UI state using Svelte 5 runes
  #isFullScreen = $state<boolean>(false);
  #isTransitioning = $state<boolean>(false);
  #showSettings = $state<boolean>(false);
  #theme = $state<Theme>(Theme.DARK);

  // ============================================================================
  // GETTERS (Reactive)
  // ============================================================================

  get isFullScreen() {
    return this.#isFullScreen;
  }

  get isTransitioning() {
    return this.#isTransitioning;
  }

  get showSettings() {
    return this.#showSettings;
  }

  get theme() {
    return this.#theme;
  }

  // Derived state
  get isReady() {
    // Will be connected to initialization service later
    return true; // Placeholder
  }

  get canUseApp() {
    return this.isReady && !this.#showSettings;
  }

  // ============================================================================
  // ACTIONS
  // ============================================================================

  setFullScreen(fullScreen: boolean): void {
    this.#isFullScreen = fullScreen;
  }

  toggleFullScreen(): void {
    this.#isFullScreen = !this.#isFullScreen;
  }

  setTransitioning(isTransitioning: boolean): void {
    this.#isTransitioning = isTransitioning;
  }

  showSettingsDialog(): void {
    this.#showSettings = true;
  }

  hideSettingsDialog(): void {
    this.#showSettings = false;
  }

  setTheme(theme: Theme): void {
    this.#theme = theme;
  }

  toggleSettingsDialog(): void {
    this.#showSettings = !this.#showSettings;
  }

  // ============================================================================
  // STATE MANAGEMENT
  // ============================================================================

  getStateSnapshot(): object {
    return {
      isFullScreen: this.#isFullScreen,
      isTransitioning: this.#isTransitioning,
      showSettings: this.#showSettings,
      theme: this.#theme,
    };
  }

  resetState(): void {
    this.#isFullScreen = false;
    this.#isTransitioning = false;
    this.#showSettings = false;
    this.#theme = Theme.DARK;
  }
}

// Export the class for DI container binding
// Singleton instance will be managed by the DI container
