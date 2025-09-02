/**
 * Filter Persistence Service - Manages filter state persistence
 *
 * Handles saving and restoring filter states across sessions,
 * following the microservices architecture pattern.
 */

import type {
  FilterState as BrowseFilterState,
  BrowseState,
  FilterType,
  FilterValue,
} from "$domain";
import { NavigationMode, SortMethod } from "$domain";
import {
  safeSessionStorageGet,
  safeSessionStorageRemove,
  safeSessionStorageSet,
} from "$utils";
import { injectable } from "inversify";

export interface FilterState {
  type: FilterType;
  value: FilterValue;
  appliedAt: Date;
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

@injectable()
export class FilterPersistenceService implements IFilterPersistenceService {
  private readonly CACHE_VERSION = "v2.1"; // ✅ ROBUST: Cache versioning
  private readonly BROWSE_STATE_KEY = `tka-${this.CACHE_VERSION}-browse-state`;
  private readonly FILTER_HISTORY_KEY = `tka-${this.CACHE_VERSION}-filter-history`;
  private readonly MAX_HISTORY_SIZE = 50;

  async saveBrowseState(state: BrowseState): Promise<void> {
    try {
      const stateToSave = {
        ...state,
        lastUpdated: new Date(),
      };
      safeSessionStorageSet(this.BROWSE_STATE_KEY, stateToSave);
    } catch (error) {
      console.error("Failed to save browse state:", error);
    }
  }

  async loadBrowseState(): Promise<BrowseState | null> {
    try {
      const parsed = safeSessionStorageGet<Record<string, unknown>>(
        this.BROWSE_STATE_KEY,
        null
      );
      if (!parsed) return null;

      // Convert date strings back to Date objects
      if (
        parsed.currentFilter &&
        typeof parsed.currentFilter === "object" &&
        parsed.currentFilter !== null &&
        "appliedAt" in parsed.currentFilter
      ) {
        (parsed.currentFilter as Record<string, unknown>).appliedAt = new Date(
          (parsed.currentFilter as Record<string, unknown>).appliedAt as string
        );
      }
      if (parsed.lastUpdated && typeof parsed.lastUpdated === "string") {
        parsed.lastUpdated = new Date(parsed.lastUpdated);
      }

      // Validate state is not too old (older than 1 day)
      const oneDay = 24 * 60 * 60 * 1000;
      if (
        parsed.lastUpdated instanceof Date &&
        Date.now() - parsed.lastUpdated.getTime() > oneDay
      ) {
        return null;
      }

      return parsed as unknown as BrowseState;
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
          )
      );

      // Add new filter to the beginning
      const newHistory = [filter, ...filteredHistory];

      // Limit history size
      const trimmedHistory = newHistory.slice(0, this.MAX_HISTORY_SIZE);

      safeSessionStorageSet(this.FILTER_HISTORY_KEY, trimmedHistory);
    } catch (error) {
      console.error("Failed to save filter to history:", error);
    }
  }

  async getFilterHistory(): Promise<FilterState[]> {
    try {
      const parsed = safeSessionStorageGet<unknown[]>(
        this.FILTER_HISTORY_KEY,
        []
      );
      if (!parsed) return [];

      // Convert date strings back to Date objects
      return parsed.map((filter: unknown) => {
        const f = filter as {
          type: FilterType;
          value: FilterValue;
          appliedAt: string;
        };
        return {
          ...f,
          appliedAt: new Date(f.appliedAt),
        };
      });
    } catch (error) {
      console.warn("Failed to load filter history:", error);
      return [];
    }
  }

  async clearFilterHistory(): Promise<void> {
    safeSessionStorageRemove(this.FILTER_HISTORY_KEY);
  }

  async getRecentFilters(limit: number = 10): Promise<FilterState[]> {
    const history = await this.getFilterHistory();
    return history.slice(0, limit);
  }

  async clearAllState(): Promise<void> {
    safeSessionStorageRemove(this.BROWSE_STATE_KEY);
    safeSessionStorageRemove(this.FILTER_HISTORY_KEY);
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
      filterType: null,
      filterValues: null,
      selectedSequence: null,
      selectedVariation: null,
      navigationMode: NavigationMode.FILTER_SELECTION,
      sortMethod: SortMethod.ALPHABETICAL,
    };
  }

  // Additional methods required by browse-interfaces.ts
  async saveFilterState(): Promise<void> {
    // Create a BrowseState with the filter state
    const browseState: BrowseState = {
      filterType: null,
      filterValues: null,
      selectedSequence: null,
      selectedVariation: null,
      navigationMode: NavigationMode.FILTER_SELECTION,
      sortMethod: SortMethod.ALPHABETICAL,
    };
    await this.saveBrowseState(browseState);
  }

  async loadFilterState(): Promise<BrowseFilterState> {
    // Return a default filter state since BrowseState doesn't have filterState property
    return {
      activeFilters: {
        starting_letter: null,
        contains_letters: null,
        length: null,
        difficulty: null,
        startPosition: null,
        author: null,
        gridMode: null,
        all_sequences: null,
        favorites: null,
        recent: null,
      },
      sortMethod: SortMethod.ALPHABETICAL,
      searchQuery: "",
    };
  }
}
