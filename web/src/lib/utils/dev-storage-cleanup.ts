/**
 * Development Storage Cleanup Utility
 *
 * Provides utilities to clear localStorage and sessionStorage for development purposes.
 * This helps reset the application state when dealing with corrupted or outdated data.
 */

import { browser } from "$app/environment";

declare global {
  interface Window {
    TKADevUtils: {
      clearAllTKAStorage: () => void;
      clearSequenceData: () => void;
      clearSettingsData: () => void;
      listTKAStorageKeys: () => void;
      getStorageStats: () => {
        localStorage: number;
        sessionStorage: number;
        totalKeys: number;
      };
    };
  }
}

/**
 * Clear all TKA-related localStorage data
 */
export function clearAllTKAStorage(): void {
  if (!browser) {
    console.warn("Storage cleanup can only run in browser environment");
    return;
  }

  console.log("🧹 Starting complete TKA storage cleanup...");

  try {
    // Get all localStorage keys
    const keysToRemove: string[] = [];

    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key?.startsWith("tka-")) {
        keysToRemove.push(key);
      }
    }

    // Remove all TKA keys
    keysToRemove.forEach((key) => {
      localStorage.removeItem(key);
      console.log(`  ✅ Removed localStorage key: ${key}`);
    });

    // Clear sessionStorage as well
    const sessionKeysToRemove: string[] = [];
    for (let i = 0; i < sessionStorage.length; i++) {
      const key = sessionStorage.key(i);
      if (key?.startsWith("tka-")) {
        sessionKeysToRemove.push(key);
      }
    }

    sessionKeysToRemove.forEach((key) => {
      sessionStorage.removeItem(key);
      console.log(`  ✅ Removed sessionStorage key: ${key}`);
    });

    // Clear other known TKA keys
    const otherKeys = [
      "optionPickerSortMethod",
      "lastSelectedTab",
      "preloaded_options",
      "all_preloaded_options",
      "tka-modern-web-settings",
    ];

    otherKeys.forEach((key) => {
      if (localStorage.getItem(key)) {
        localStorage.removeItem(key);
        console.log(`  ✅ Removed other key: ${key}`);
      }
    });

    console.log("🎉 TKA storage cleanup completed successfully!");
    console.log("💡 Refresh the page to start with clean state");
  } catch (error) {
    console.error("❌ Failed to clear TKA storage:", error);
  }
}

/**
 * Clear only sequence data (preserve settings)
 */
export function clearSequenceData(): void {
  if (!browser) return;

  console.log("🧹 Clearing sequence data only...");

  try {
    const keysToRemove: string[] = [];

    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key?.includes("-sequence") || key?.includes("-sequences")) {
        keysToRemove.push(key);
      }
    }

    keysToRemove.forEach((key) => {
      localStorage.removeItem(key);
      console.log(`  ✅ Removed sequence key: ${key}`);
    });

    console.log("🎉 Sequence data cleared!");
  } catch (error) {
    console.error("❌ Failed to clear sequence data:", error);
  }
}

/**
 * Clear only settings (preserve sequences)
 */
export function clearSettingsData(): void {
  if (!browser) return;

  console.log("🧹 Clearing settings data only...");

  try {
    const settingsKeys = [
      "tka-modern-web-settings",
      "tka-v2.1-settings",
      "optionPickerSortMethod",
      "lastSelectedTab",
    ];

    settingsKeys.forEach((key) => {
      if (localStorage.getItem(key)) {
        localStorage.removeItem(key);
        console.log(`  ✅ Removed settings key: ${key}`);
      }
    });

    console.log("🎉 Settings data cleared!");
  } catch (error) {
    console.error("❌ Failed to clear settings data:", error);
  }
}

/**
 * List all TKA-related storage keys (for debugging)
 */
export function listTKAStorageKeys(): void {
  if (!browser) return;

  console.log("📋 TKA Storage Keys:");
  console.log("===================");

  // localStorage
  console.log("📦 localStorage:");
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (
      key?.startsWith("tka-") ||
      key?.includes("option") ||
      key?.includes("preloaded")
    ) {
      const value = localStorage.getItem(key);
      const size = value ? (value.length / 1024).toFixed(2) : "0";
      console.log(`  ${key} (${size} KB)`);
    }
  }

  // sessionStorage
  console.log("🗂️ sessionStorage:");
  for (let i = 0; i < sessionStorage.length; i++) {
    const key = sessionStorage.key(i);
    if (key?.startsWith("tka-")) {
      const value = sessionStorage.getItem(key);
      const size = value ? (value.length / 1024).toFixed(2) : "0";
      console.log(`  ${key} (${size} KB)`);
    }
  }
}

/**
 * Get storage usage statistics
 */
export function getStorageStats(): {
  localStorage: number;
  sessionStorage: number;
  totalKeys: number;
} {
  if (!browser) return { localStorage: 0, sessionStorage: 0, totalKeys: 0 };

  let localStorageSize = 0;
  let sessionStorageSize = 0;
  let totalKeys = 0;

  // Calculate localStorage usage
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (
      key?.startsWith("tka-") ||
      key?.includes("option") ||
      key?.includes("preloaded")
    ) {
      const value = localStorage.getItem(key);
      localStorageSize += (key.length + (value?.length || 0)) * 2; // UTF-16
      totalKeys++;
    }
  }

  // Calculate sessionStorage usage
  for (let i = 0; i < sessionStorage.length; i++) {
    const key = sessionStorage.key(i);
    if (key?.startsWith("tka-")) {
      const value = sessionStorage.getItem(key);
      sessionStorageSize += (key.length + (value?.length || 0)) * 2; // UTF-16
      totalKeys++;
    }
  }

  return {
    localStorage: Math.round(localStorageSize / 1024), // KB
    sessionStorage: Math.round(sessionStorageSize / 1024), // KB
    totalKeys,
  };
}

// Make functions available globally for console access
if (browser && typeof window !== "undefined") {
  window.TKADevUtils = {
    clearAllTKAStorage,
    clearSequenceData,
    clearSettingsData,
    listTKAStorageKeys,
    getStorageStats,
  };

  console.log("🛠️ TKA Dev Utils loaded! Available commands:");
  console.log("  TKADevUtils.clearAllTKAStorage() - Clear everything");
  console.log("  TKADevUtils.clearSequenceData() - Clear sequences only");
  console.log("  TKADevUtils.clearSettingsData() - Clear settings only");
  console.log("  TKADevUtils.listTKAStorageKeys() - List all keys");
  console.log("  TKADevUtils.getStorageStats() - Get usage stats");
}
