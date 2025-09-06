/**
 * Memory Transport
 *
 * Stores logs in memory for later retrieval, useful for debug panels.
 */

import { type LogEntry, type LogTransport } from '../types';
import { MAX_MEMORY_LOGS } from '../constants';

export interface MemoryTransportOptions {
  maxEntries?: number;
  circular?: boolean;
}

export class MemoryTransport implements LogTransport {
  name = 'memory';
  private entries: LogEntry[] = [];
  private maxEntries: number;
  private circular: boolean;
  private listeners: Set<(entries: LogEntry[]) => void> = new Set();

  constructor(options: MemoryTransportOptions = {}) {
    this.maxEntries = options.maxEntries || MAX_MEMORY_LOGS;
    this.circular = options.circular !== false;
  }

  log(entry: LogEntry): void {
    // Add the entry to the buffer
    this.entries.push(entry);

    // If we've exceeded the max entries and circular buffer is enabled,
    // remove the oldest entry
    if (this.circular && this.entries.length > this.maxEntries) {
      this.entries.shift();
    }

    // Notify listeners
    this.notifyListeners();
  }

  getEntries(): LogEntry[] {
    return [...this.entries];
  }

  clear(): void {
    this.entries = [];
    this.notifyListeners();
  }

  /**
   * Add a listener that will be called whenever the entries change
   */
  addListener(listener: (entries: LogEntry[]) => void): () => void {
    this.listeners.add(listener);

    // Return a function to remove the listener
    return () => {
      this.listeners.delete(listener);
    };
  }

  /**
   * Notify all listeners of changes
   */
  private notifyListeners(): void {
    const entries = this.getEntries();
    this.listeners.forEach(listener => {
      try {
        listener(entries);
      } catch (error) {
        console.error('Error in memory transport listener:', error);
      }
    });
  }
}
