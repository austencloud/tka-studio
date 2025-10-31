import type { ExploreFilterType } from "../../domain/enums/FilteringEnums";
import type { ExploreFilterValue } from "../../domain/types/FilteringTypes";

// Simple filter history entry type
export interface FilterHistoryEntry {
  type: ExploreFilterType;
  value: ExploreFilterValue;
  appliedAt: Date;
}

// Simple browse state for persistence
export interface SimpleBrowseState {
  filterType: ExploreFilterType | null;
  filterValue: ExploreFilterValue;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  sortMethod: any; // Will be typed properly when we consolidate sort enums
}

/**
 * Service for persisting filter and browse state
 */
export interface IFilterPersistenceService {
  /** Save current browse state */
  saveBrowseState(state: SimpleBrowseState): Promise<void>;

  /** Load saved browse state */
  loadBrowseState(): Promise<SimpleBrowseState | null>;

  /** Save filter history */
  saveFilterToHistory(filter: FilterHistoryEntry): Promise<void>;

  /** Get filter history */
  getFilterHistory(): Promise<FilterHistoryEntry[]>;

  /** Clear filter history */
  clearFilterHistory(): Promise<void>;

  /** Get recently used filters */
  getRecentFilters(limit?: number): Promise<FilterHistoryEntry[]>;

  /** Clear all saved state */
  clearAllState(): Promise<void>;
}
