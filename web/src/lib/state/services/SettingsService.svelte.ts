/**
 * Settings Service
 *
 * Manages application settings with persistence to localStorage.
 * Clean separation of settings logic from other concerns.
 */

import { browser } from "$app/environment";
import type { AppSettings } from "$domain";
import { BackgroundType, GridMode } from "$domain";
import { updateBodyBackground } from "$lib/utils/background-preloader";
import type { ISettingsService } from "./state-service-interfaces";

const SETTINGS_STORAGE_KEY = "tka-modern-web-settings";

const DEFAULT_SETTINGS: AppSettings = {
  theme: "dark",
  gridMode: GridMode.DIAMOND,
  showBeatNumbers: true,
  autoSave: true,
  exportQuality: "high",
  workbenchColumns: 5,
  developerMode: true,
  animationsEnabled: true,
  backgroundType: BackgroundType.NIGHT_SKY,
  backgroundQuality: "medium",
  backgroundEnabled: true,
  visibility: {
    TKA: true,
    Reversals: true,
    Positions: true,
    Elemental: true,
    VTG: true,
    nonRadialPoints: true,
  },
} as AppSettings;

class SettingsService implements ISettingsService {
  // Settings state
  #settings = $state<AppSettings>(this.loadSettingsFromStorage());

  // ============================================================================
  // GETTERS
  // ============================================================================

  get settings() {
    return this.#settings;
  }

  // ============================================================================
  // ACTIONS
  // ============================================================================

  updateSettings(newSettings: Partial<AppSettings>): void {
    Object.assign(this.#settings, newSettings);

    // Update body background immediately if background type changed
    if (newSettings.backgroundType) {
      updateBodyBackground(newSettings.backgroundType);
    }

    this.saveSettings();
  }

  async loadSettings(): Promise<void> {
    const loadedSettings = this.loadSettingsFromStorage();
    Object.assign(this.#settings, loadedSettings);
  }

  saveSettings(): void {
    this.saveSettingsToStorage(this.#settings);
  }

  clearStoredSettings(): void {
    if (!browser) return;

    try {
      localStorage.removeItem(SETTINGS_STORAGE_KEY);
      Object.assign(this.#settings, DEFAULT_SETTINGS);
    } catch (error) {
      console.error("Failed to clear stored settings:", error);
    }
  }

  resetToDefaults(): void {
    Object.assign(this.#settings, DEFAULT_SETTINGS);
    this.saveSettings();
  }

  debugSettings(): void {
    if (!browser) return;

    try {
      console.log("🔍 Debug Settings:", {
        stored: localStorage.getItem(SETTINGS_STORAGE_KEY),
        parsed: JSON.parse(localStorage.getItem(SETTINGS_STORAGE_KEY) || "{}"),
        current: this.#settings,
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

// Singleton instance
export const settingsService = new SettingsService();
