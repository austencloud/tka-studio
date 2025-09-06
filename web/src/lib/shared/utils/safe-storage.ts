/**
 * Safe Storage Utility
 *
 * Provides safe wrappers around localStorage and sessionStorage
 * to prevent JSON parsing errors and undefined value issues.
 */

/**
 * Safely get and parse a value from sessionStorage
 */
export function safeSessionStorageGet<T>(
  key: string,
  defaultValue: T | null = null
): T | null {
  try {
    const stored = sessionStorage.getItem(key);

    // Check for undefined, null, or empty string values
    if (
      !stored ||
      stored === "undefined" ||
      stored === "null" ||
      stored.trim() === ""
    ) {
      return defaultValue;
    }

    return JSON.parse(stored) as T;
  } catch (error) {
    console.warn(
      `Failed to parse sessionStorage value for key "${key}":`,
      error
    );
    return defaultValue;
  }
}

/**
 * Safely set a value to sessionStorage
 */
export function safeSessionStorageSet(key: string, value: unknown): boolean {
  try {
    const serialized = JSON.stringify(value);
    sessionStorage.setItem(key, serialized);
    return true;
  } catch (error) {
    console.error(`Failed to save to sessionStorage for key "${key}":`, error);
    return false;
  }
}

/**
 * Safely get and parse a value from localStorage
 */
export function safeLocalStorageGet<T>(
  key: string,
  defaultValue: T | null = null
): T | null {
  try {
    const stored = localStorage.getItem(key);

    // Check for undefined, null, or empty string values
    if (
      !stored ||
      stored === "undefined" ||
      stored === "null" ||
      stored.trim() === ""
    ) {
      return defaultValue;
    }

    return JSON.parse(stored) as T;
  } catch (error) {
    console.warn(`Failed to parse localStorage value for key "${key}":`, error);
    return defaultValue;
  }
}

/**
 * Safely set a value to localStorage
 */
export function safeLocalStorageSet(key: string, value: unknown): boolean {
  try {
    const serialized = JSON.stringify(value);
    localStorage.setItem(key, serialized);
    return true;
  } catch (error) {
    console.error(`Failed to save to localStorage for key "${key}":`, error);
    return false;
  }
}

/**
 * Safely remove a value from sessionStorage
 */
export function safeSessionStorageRemove(key: string): boolean {
  try {
    sessionStorage.removeItem(key);
    return true;
  } catch (error) {
    console.error(
      `Failed to remove from sessionStorage for key "${key}":`,
      error
    );
    return false;
  }
}

/**
 * Safely remove a value from localStorage
 */
export function safeLocalStorageRemove(key: string): boolean {
  try {
    localStorage.removeItem(key);
    return true;
  } catch (error) {
    console.error(
      `Failed to remove from localStorage for key "${key}":`,
      error
    );
    return false;
  }
}
