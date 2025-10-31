/**
 * Settings Service
 *
 * Manages application settings with persistence to localStorage.
 * Clean separation of settings logic from other concerns.
 */

import { browser } from "$app/environment";
import type { ISettingsService } from "$shared";
import { injectable } from "inversify";
import { BackgroundType, updateBodyBackground } from "../../background";
import { GridMode } from "../../pictograph";
import { ThemeService } from "../../theme";
import type { AppSettings } from "../domain";

const SETTINGS_STORAGE_KEY = "tka-modern-web-settings";

const DEFAULT_SETTINGS: AppSettings = {
  gridMode: GridMode.DIAMOND,
  backgroundType: BackgroundType.NIGHT_SKY,
  backgroundQuality: "medium",
  backgroundEnabled: true,
  hapticFeedback: true,
  reducedMotion: false,
} as AppSettings;

// Initialize with loaded settings immediately (non-reactive)
const initialSettings = (() => {
  if (!browser) return DEFAULT_SETTINGS;
  try {
    const stored = localStorage.getItem(SETTINGS_STORAGE_KEY);
    if (!stored) return DEFAULT_SETTINGS;
    const parsed = JSON.parse(stored);
    return { ...DEFAULT_SETTINGS, ...parsed };
  } catch {
    return DEFAULT_SETTINGS;
  }
})();

// Create reactive settings state with loaded settings
const settingsState = $state<AppSettings>(initialSettings);

@injectable()
class SettingsState implements ISettingsService {
  constructor() {
    // Settings are already loaded in the reactive state
  }

  // ============================================================================
  // GETTERS
  // ============================================================================

  get settings() {
    return settingsState;
  }

  get currentSettings() {
    return settingsState;
  }

  // ============================================================================
  // ACTIONS
  // ============================================================================

  async updateSetting<K extends keyof AppSettings>(
    key: K,
    value: AppSettings[K]
  ): Promise<void> {
    // CRITICAL: Direct assignment for Svelte 5 reactivity
    settingsState[key] = value;

    // Update body background immediately if background type changed
    if (key === "backgroundType") {
      updateBodyBackground(value as BackgroundType);
      ThemeService.updateTheme(value as string);
    }

    this.saveSettings();
  }

  async updateSettings(newSettings: Partial<AppSettings>): Promise<void> {
    // CRITICAL: In Svelte 5, we need to update individual properties to trigger reactivity
    // Object.assign doesn't trigger Svelte 5 runes reactivity
    for (const key in newSettings) {
      if (Object.prototype.hasOwnProperty.call(newSettings, key)) {
        settingsState[key as keyof AppSettings] = newSettings[
          key as keyof AppSettings
        ] as never;
      }
    }

    // Update body background immediately if background type changed
    if (newSettings.backgroundType) {
      updateBodyBackground(newSettings.backgroundType);
      ThemeService.updateTheme(newSettings.backgroundType);
    }

    this.saveSettings();
  }

  async loadSettings(): Promise<void> {
    const loadedSettings = this.loadSettingsFromStorage();
    Object.assign(settingsState, loadedSettings);
  }

  saveSettings(): void {
    this.saveSettingsToStorage(settingsState);
  }

  clearStoredSettings(): void {
    if (!browser) return;

    try {
      localStorage.removeItem(SETTINGS_STORAGE_KEY);
      Object.assign(settingsState, DEFAULT_SETTINGS);
    } catch (error) {
      console.error("Failed to clear stored settings:", error);
    }
  }

  async resetToDefaults(): Promise<void> {
    Object.assign(settingsState, DEFAULT_SETTINGS);
    this.saveSettings();
  }

  debugSettings(): void {
    if (!browser) return;

    try {
      console.log("🔍 Debug Settings:", {
        stored: localStorage.getItem(SETTINGS_STORAGE_KEY),
        parsed: JSON.parse(localStorage.getItem(SETTINGS_STORAGE_KEY) || "{}"),
        current: settingsState,
      });
    } catch (error) {
      console.error("Error debugging settings:", error);
    }
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  private loadSettingsFromStorage(): AppSettings {
    if (!browser) return DEFAULT_SETTINGS;

    try {
      const stored = localStorage.getItem(SETTINGS_STORAGE_KEY);
      if (!stored) {
        return DEFAULT_SETTINGS;
      }

      const parsed = JSON.parse(stored);
      const merged = { ...DEFAULT_SETTINGS, ...parsed };

      // Ensure developer mode is enabled for all tabs visibility
      if (
        merged.developerMode === false ||
        merged.developerMode === undefined
      ) {
        merged.developerMode = true;
        localStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(merged));
      }

      return merged;
    } catch (error) {
      console.warn("Failed to load settings from localStorage:", error);
      return DEFAULT_SETTINGS;
    }
  }

  private saveSettingsToStorage(settings: AppSettings): void {
    if (!browser) return;

    try {
      localStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(settings));
    } catch (error) {
      console.error("Failed to save settings to localStorage:", error);
    }
  }
}

// Export the class for DI container
export { SettingsState };

// Singleton instance
export const settingsService = new SettingsState();
