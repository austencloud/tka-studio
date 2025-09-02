/**
 * Settings Service Interface
 *
 * Interface for managing application settings and user preferences.
 * Handles loading, saving, and updating application configuration.
 */

import type { AppSettings } from "$domain";

export interface ISettingsService {
  currentSettings: AppSettings;
  updateSetting<K extends keyof AppSettings>(
    key: K,
    value: AppSettings[K]
  ): Promise<void>;
  loadSettings(): Promise<void>;
}
