/**
 * Session Storage Cleanup Utility
 *
 * Safely cleans up problematic sessionStorage values that might cause
 * JSON parsing errors in SvelteKit's session storage handling.
 */

import { browser } from "$app/environment";

/**
 * Clean up problematic sessionStorage values on app startup
 */
export function cleanupSessionStorage(): void {
  if (!browser) return;

  try {
    // Get all sessionStorage keys
    const keysToCheck: string[] = [];
    for (let i = 0; i < sessionStorage.length; i++) {
      const key = sessionStorage.key(i);
      if (key) {
        keysToCheck.push(key);
      }
    }

    // Check each key for problematic values
    keysToCheck.forEach((key) => {
      try {
        const value = sessionStorage.getItem(key);

        // Remove entries that are undefined, null strings, or empty
        if (
          !value ||
          value === "undefined" ||
          value === "null" ||
          value.trim() === ""
        ) {
          sessionStorage.removeItem(key);
          return;
        }

        // Try to parse JSON to see if it's valid
        JSON.parse(value);
      } catch (parseError) {
        // If parsing fails, remove the problematic entry
        console.warn(
          `Removing invalid JSON in sessionStorage key: ${key}`,
          parseError
        );
        sessionStorage.removeItem(key);
      }
    });
  } catch (error) {
    console.error("❌ Failed to cleanup sessionStorage:", error);
  }
}

/**
 * Clean up specific TKA-related sessionStorage keys
 */
export function cleanupTKASessionStorage(): void {
  if (!browser) return;

  const tkaKeys = [
    "tka-browse-state-v2",
    "tka-filter-history-v2",
    // Add other known TKA sessionStorage keys here
  ];

  tkaKeys.forEach((key) => {
    try {
      const value = sessionStorage.getItem(key);
      if (value && (value === "undefined" || value === "null")) {
        sessionStorage.removeItem(key);
      }
    } catch (error) {
      console.warn(`Failed to check TKA sessionStorage key ${key}:`, error);
    }
  });
}
