/**
 * Settings Service - Application Settings Management
 *
 * Manages application settings with persistence and reactive updates.
 */

import type { ISettingsService } from "$contracts";
import { GridMode, type AppSettings, type BackgroundType } from "$domain";
import { updateBodyBackground } from "$utils";
import { injectable } from "inversify";

@injectable()
export class SettingsService implements ISettingsService {
  private readonly CACHE_VERSION = "v2.1"; // ✅ ROBUST: Cache versioning
  private readonly SETTINGS_KEY = `tka-${this.CACHE_VERSION}-settings`;

  private _settings: AppSettings = {
    theme: "dark",
    gridMode: GridMode.DIAMOND,
    showBeatNumbers: true,
    autoSave: true,
    exportQuality: "high",
    workbenchColumns: 3,
  };

  constructor() {
    // Load settings on initialization
    this.loadSettings();
  }

  /**
   * Get current settings
   */
  get currentSettings(): AppSettings {
    return { ...this._settings };
  }

  /**
   * Update a specific setting
   */
  async updateSetting<K extends keyof AppSettings>(
    key: K,
    value: AppSettings[K]
  ): Promise<void> {
    try {
      this._settings[key] = value;
      await this.persistSettings();

      // Update body background immediately if background type changed
      if (key === "backgroundType" && typeof value === "string") {
        updateBodyBackground(value as BackgroundType);
      }

      console.log(`Setting ${String(key)} updated to:`, value);
    } catch (error) {
      console.error(`Failed to update setting ${String(key)}:`, error);
      throw new Error(
        `Failed to update setting: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Load settings from storage
   */
  async loadSettings(): Promise<void> {
    try {
      const stored = localStorage.getItem(this.SETTINGS_KEY);
      if (stored) {
        const parsed = JSON.parse(stored) as Partial<AppSettings>;
        this._settings = { ...this._settings, ...parsed };
        console.log("Settings loaded:", this._settings);
      }
    } catch (error) {
      console.error("Failed to load settings:", error);
      // Continue with default settings
    }
  }

  /**
   * Persist settings to storage
   */
  private async persistSettings(): Promise<void> {
    try {
      localStorage.setItem(this.SETTINGS_KEY, JSON.stringify(this._settings));
    } catch (error) {
      console.error("Failed to persist settings:", error);
      throw error;
    }
  }

  /**
   * Reset settings to defaults
   */
  async resetToDefaults(): Promise<void> {
    this._settings = {
      theme: "dark",
      gridMode: GridMode.DIAMOND,
      showBeatNumbers: true,
      autoSave: true,
      exportQuality: "high",
      workbenchColumns: 3,
    };

    await this.persistSettings();
    console.log("Settings reset to defaults");
  }
}
