/**
 * LocalStorage Transport
 *
 * Persists logs to localStorage for later retrieval.
 */

import { type LogEntry, type LogTransport, LogLevel } from '../types.js';
import { MAX_STORAGE_LOGS, STORAGE_KEY } from '../constants.js';
import { browser } from '$app/environment';

export interface LocalStorageTransportOptions {
  maxEntries?: number;
  storageKey?: string;
  minLevel?: LogLevel;
  throttleMs?: number;
}

export class LocalStorageTransport implements LogTransport {
  name = 'localStorage';
  private options: LocalStorageTransportOptions;
  private buffer: LogEntry[] = [];
  private throttleTimeout: ReturnType<typeof setTimeout> | null = null;

  constructor(options: LocalStorageTransportOptions = {}) {
    this.options = {
      maxEntries: MAX_STORAGE_LOGS,
      storageKey: STORAGE_KEY,
      minLevel: LogLevel.INFO, // Default to only storing INFO and above
      throttleMs: 1000, // Throttle writes to once per second
      ...options
    };

    // Load existing entries when created
    if (browser) {
      this.loadFromStorage();
    }
  }

  log(entry: LogEntry): void {
    // Skip if not in browser or below minimum level
    if (!browser || entry.level < this.options.minLevel!) {
      return;
    }

    // Add to buffer
    this.buffer.push(entry);

    // Schedule a write if not already scheduled
    if (!this.throttleTimeout) {
      this.throttleTimeout = setTimeout(() => {
        this.flushToStorage();
        this.throttleTimeout = null;
      }, this.options.throttleMs);
    }
  }

  /**
   * Immediately write buffered logs to storage
   */
  flush(): Promise<void> {
    return new Promise<void>((resolve) => {
      if (this.throttleTimeout) {
        clearTimeout(this.throttleTimeout);
        this.throttleTimeout = null;
      }

      this.flushToStorage();
      resolve();
    });
  }

  /**
   * Clear all stored logs
   */
  clear(): void {
    this.buffer = [];
    if (browser) {
      try {
        localStorage.removeItem(this.options.storageKey!);
      } catch (error) {
        console.error('Error clearing localStorage logs:', error);
      }
    }
  }

  /**
   * Get all stored entries
   */
  getEntries(): LogEntry[] {
    if (!browser) return [];

    const entries = this.loadFromStorage();
    return [...entries, ...this.buffer];
  }

  /**
   * Load entries from localStorage
   */
  private loadFromStorage(): LogEntry[] {
    if (!browser) return [];

    try {
      const storedData = localStorage.getItem(this.options.storageKey!);
      if (!storedData) return [];

      return JSON.parse(storedData) as LogEntry[];
    } catch (error) {
      console.error('Error loading logs from localStorage:', error);
      return [];
    }
  }

  /**
   * Write buffered entries to localStorage
   */
  private flushToStorage(): void {
    if (!browser || this.buffer.length === 0) return;

    try {
      // Get existing entries
      const existingEntries = this.loadFromStorage();

      // Combine with buffer
      const allEntries = [...existingEntries, ...this.buffer];

      // Trim to max size
      const trimmedEntries = allEntries.slice(-this.options.maxEntries!);

      // Save to localStorage
      localStorage.setItem(
        this.options.storageKey!,
        JSON.stringify(trimmedEntries)
      );

      // Clear buffer
      this.buffer = [];
    } catch (error) {
      console.error('Error writing logs to localStorage:', error);

      // If it's a quota error, try to reduce the number of entries
      if (error instanceof DOMException && error.name === 'QuotaExceededError') {
        try {
          // Try to save half as many entries
          const existingEntries = this.loadFromStorage();
          const reducedEntries = existingEntries.slice(-Math.floor(this.options.maxEntries! / 2));
          localStorage.setItem(
            this.options.storageKey!,
            JSON.stringify(reducedEntries)
          );
        } catch (retryError) {
          console.error('Failed to reduce localStorage logs after quota error:', retryError);
        }
      }
    }
  }
}
