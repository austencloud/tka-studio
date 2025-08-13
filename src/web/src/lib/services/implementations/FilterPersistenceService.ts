/**
 * Filter Persistence Service - Manages filter state persistence
 *
 * Handles saving and restoring filter states across sessions,
 * following the microservices architecture pattern.
 */

import type { FilterType, FilterValue, SortMethod } from "../interfaces";

export interface FilterState {
  type: FilterType;
  value: FilterValue;
  appliedAt: Date;
}

export interface BrowseState {
  currentFilter: FilterState | null;
  sortMethod: SortMethod;
  navigationMode: "filter_selection" | "sequence_browser";
  searchQuery: string;
  lastUpdated: Date;
}

export interface IFilterPersistenceService {
  /** Save current browse state */
  saveBrowseState(state: BrowseState): Promise<void>;

  /** Load saved browse state */
  loadBrowseState(): Promise<BrowseState | null>;

  /** Save filter history */
  saveFilterToHistory(filter: FilterState): Promise<void>;

  /** Get filter history */
  getFilterHistory(): Promise<FilterState[]>;

  /** Clear filter history */
  clearFilterHistory(): Promise<void>;

  /** Get recently used filters */
  getRecentFilters(limit?: number): Promise<FilterState[]>;

  /** Clear all saved state */
  clearAllState(): Promise<void>;
}

export class FilterPersistenceService implements IFilterPersistenceService {
  private readonly BROWSE_STATE_KEY = "tka-browse-state";
  private readonly FILTER_HISTORY_KEY = "tka-filter-history";
  private readonly MAX_HISTORY_SIZE = 50;

  async saveBrowseState(state: BrowseState): Promise<void> {
    try {
      const stateToSave = {
        ...state,
        lastUpdated: new Date(),
      };
      sessionStorage.setItem(
        this.BROWSE_STATE_KEY,
        JSON.stringify(stateToSave),
      );
    } catch (error) {
      console.error("Failed to save browse state:", error);
    }
  }

  async loadBrowseState(): Promise<BrowseState | null> {
    try {
      const saved = sessionStorage.getItem(this.BROWSE_STATE_KEY);
      if (!saved) return null;

      const parsed = JSON.parse(saved);

      // Convert date strings back to Date objects
      if (parsed.currentFilter?.appliedAt) {
        parsed.currentFilter.appliedAt = new Date(
          parsed.currentFilter.appliedAt,
        );
      }
      if (parsed.lastUpdated) {
        parsed.lastUpdated = new Date(parsed.lastUpdated);
      }

      // Validate state is not too old (older than 1 day)
      const oneDay = 24 * 60 * 60 * 1000;
      if (
        parsed.lastUpdated &&
        Date.now() - parsed.lastUpdated.getTime() > oneDay
      ) {
        return null;
      }

      return parsed as BrowseState;
    } catch (error) {
      console.warn("Failed to load browse state:", error);
      return null;
    }
  }

  async saveFilterToHistory(filter: FilterState): Promise<void> {
    try {
      const history = await this.getFilterHistory();

      // Remove duplicate filters (same type and value)
      const filteredHistory = history.filter(
        (f) =>
          !(
            f.type === filter.type &&
            JSON.stringify(f.value) === JSON.stringify(filter.value)
          ),
      );

      // Add new filter to the beginning
      const newHistory = [filter, ...filteredHistory];

      // Limit history size
      const trimmedHistory = newHistory.slice(0, this.MAX_HISTORY_SIZE);

      sessionStorage.setItem(
        this.FILTER_HISTORY_KEY,
        JSON.stringify(trimmedHistory),
      );
    } catch (error) {
      console.error("Failed to save filter to history:", error);
    }
  }

  async getFilterHistory(): Promise<FilterState[]> {
    try {
      const saved = sessionStorage.getItem(this.FILTER_HISTORY_KEY);
      if (!saved) return [];

      const parsed = JSON.parse(saved);

      // Convert date strings back to Date objects
      return parsed.map(
        (filter: {
          type: FilterType;
          value: FilterValue;
          appliedAt: string;
        }) => ({
          ...filter,
          appliedAt: new Date(filter.appliedAt),
        }),
      );
    } catch (error) {
      console.warn("Failed to load filter history:", error);
      return [];
    }
  }

  async clearFilterHistory(): Promise<void> {
    try {
      sessionStorage.removeItem(this.FILTER_HISTORY_KEY);
    } catch (error) {
      console.error("Failed to clear filter history:", error);
    }
  }

  async getRecentFilters(limit: number = 10): Promise<FilterState[]> {
    const history = await this.getFilterHistory();
    return history.slice(0, limit);
  }

  async clearAllState(): Promise<void> {
    try {
      sessionStorage.removeItem(this.BROWSE_STATE_KEY);
      sessionStorage.removeItem(this.FILTER_HISTORY_KEY);
    } catch (error) {
      console.error("Failed to clear all state:", error);
    }
  }

  // Utility methods for filter management
  async getFilterFrequency(): Promise<Map<string, number>> {
    const history = await this.getFilterHistory();
    const frequency = new Map<string, number>();

    history.forEach((filter) => {
      const key = `${filter.type}:${JSON.stringify(filter.value)}`;
      frequency.set(key, (frequency.get(key) || 0) + 1);
    });

    return frequency;
  }

  async getMostUsedFilters(limit: number = 5): Promise<FilterState[]> {
    const history = await this.getFilterHistory();
    const frequency = await this.getFilterFrequency();

    // Group filters by type:value and find most frequent
    const filterMap = new Map<string, FilterState>();
    history.forEach((filter) => {
      const key = `${filter.type}:${JSON.stringify(filter.value)}`;
      if (!filterMap.has(key)) {
        filterMap.set(key, filter);
      }
    });

    return Array.from(filterMap.values())
      .sort((a, b) => {
        const keyA = `${a.type}:${JSON.stringify(a.value)}`;
        const keyB = `${b.type}:${JSON.stringify(b.value)}`;
        return (frequency.get(keyB) || 0) - (frequency.get(keyA) || 0);
      })
      .slice(0, limit);
  }

  async getDefaultBrowseState(): Promise<BrowseState> {
    return {
      currentFilter: null,
      sortMethod: "alphabetical" as SortMethod,
      navigationMode: "filter_selection",
      searchQuery: "",
      lastUpdated: new Date(),
    };
  }
}
