/**
 * Browse State Persistence Service
 *
 * Comprehensive state persistence for the Browse tab including:
 * - Filter state memory (starting letter, difficulty, length, etc.)
 * - Sort state memory (Name A-Z, Difficulty, Length, Recently Added, Author)
 * - Scroll position memory (exact pixel position)
 * - View mode memory (grid/list view)
 * - Selected sequence memory
 * - Application-level tab memory
 */

import { injectable } from "inversify";
import type {
  ApplicationTabState,
  CompleteGalleryState,
  FilterHistoryEntry,
  GalleryScrollState,
  GallerySelectionState,
  GallerySortState,
  GalleryViewState,
} from "../../domain/models/gallery-models";

// Re-export FilterHistoryEntry for use by other services
export type { FilterHistoryEntry } from "../../domain/models/gallery-models";

export interface IBrowseStatePersister {
  // Browse state persistence
  saveBrowseState(state: CompleteGalleryState): Promise<void>;
  loadBrowseState(): Promise<CompleteGalleryState | null>;

  // Individual state component persistence
  saveFilterState(filter: FilterHistoryEntry): Promise<void>;
  loadFilterState(): Promise<FilterHistoryEntry | null>;

  saveSortState(sort: GallerySortState): Promise<void>;
  loadSortState(): Promise<GallerySortState | null>;

  saveViewState(view: GalleryViewState): Promise<void>;
  loadViewState(): Promise<GalleryViewState | null>;

  saveScrollState(scroll: GalleryScrollState): Promise<void>;
  loadScrollState(): Promise<GalleryScrollState | null>;

  saveSelectionState(selection: GallerySelectionState): Promise<void>;
  loadSelectionState(): Promise<GallerySelectionState | null>;

  // Application-level tab state
  saveApplicationTabState(tabState: ApplicationTabState): Promise<void>;
  loadApplicationTabState(): Promise<ApplicationTabState | null>;

  // Utility methods
  clearBrowseState(): Promise<void>;
  clearAllState(): Promise<void>;
  isStateValid(state: CompleteGalleryState): boolean;
  createDefaultBrowseState(): CompleteGalleryState;
}

@injectable()
export class BrowseStatePersister implements IBrowseStatePersister {
  private readonly BROWSE_STATE_KEY = "tka-browse-state-v2";
  private readonly FILTER_STATE_KEY = "tka-browse-filter-v2";
  private readonly SORT_STATE_KEY = "tka-browse-sort-v2";
  private readonly VIEW_STATE_KEY = "tka-browse-view-v2";
  private readonly SCROLL_STATE_KEY = "tka-browse-scroll-v2";
  private readonly SELECTION_STATE_KEY = "tka-browse-selection-v2";
  private readonly APP_TAB_STATE_KEY = "tka-app-tab-state-v2";

  private readonly CURRENT_VERSION = 1;
  private readonly MAX_STATE_AGE_DAYS = 30; // State expires after 30 days

  // ============================================================================
  // COMPLETE BROWSE STATE
  // ============================================================================

  async saveBrowseState(state: CompleteGalleryState): Promise<void> {
    try {
      const stateToSave = {
        ...state,
        lastUpdated: new Date(),
        version: this.CURRENT_VERSION,
      };

      localStorage.setItem(this.BROWSE_STATE_KEY, JSON.stringify(stateToSave));
    } catch (error) {
      console.error("❌ Failed to save browse state:", error);
    }
  }

  async loadBrowseState(): Promise<CompleteGalleryState | null> {
    try {
      const saved = localStorage.getItem(this.BROWSE_STATE_KEY);
      if (!saved) return null;

      const parsed = JSON.parse(saved);

      // Convert date strings back to Date objects
      if (parsed.filter?.appliedAt) {
        parsed.filter.appliedAt = new Date(parsed.filter.appliedAt);
      }
      if (parsed.sort?.appliedAt) {
        parsed.sort.appliedAt = new Date(parsed.sort.appliedAt);
      }
      if (parsed.selection?.lastSelectedAt) {
        parsed.selection.lastSelectedAt = new Date(
          parsed.selection.lastSelectedAt
        );
      }
      if (parsed.lastUpdated) {
        parsed.lastUpdated = new Date(parsed.lastUpdated);
      }

      // Validate state age
      if (!this.isStateValid(parsed)) {
        console.warn("⚠️ Browse state is invalid or too old, clearing");
        await this.clearBrowseState();
        return null;
      }

      return parsed as CompleteGalleryState;
    } catch (error) {
      console.warn("⚠️ Failed to load browse state:", error);
      return null;
    }
  }

  // ============================================================================
  // INDIVIDUAL STATE COMPONENTS
  // ============================================================================

  async saveFilterState(filter: FilterHistoryEntry): Promise<void> {
    try {
      localStorage.setItem(this.FILTER_STATE_KEY, JSON.stringify(filter));
    } catch (error) {
      console.error("❌ Failed to save filter state:", error);
    }
  }

  async loadFilterState(): Promise<FilterHistoryEntry | null> {
    try {
      const saved = localStorage.getItem(this.FILTER_STATE_KEY);
      if (!saved) return null;

      const parsed = JSON.parse(saved);
      if (parsed.appliedAt) {
        parsed.appliedAt = new Date(parsed.appliedAt);
      }

      return parsed as FilterHistoryEntry;
    } catch (error) {
      console.warn("⚠️ Failed to load filter state:", error);
      return null;
    }
  }

  async saveSortState(sort: GallerySortState): Promise<void> {
    try {
      localStorage.setItem(this.SORT_STATE_KEY, JSON.stringify(sort));
    } catch (error) {
      console.error("❌ Failed to save sort state:", error);
    }
  }

  async loadSortState(): Promise<GallerySortState | null> {
    try {
      const saved = localStorage.getItem(this.SORT_STATE_KEY);
      if (!saved) return null;

      const parsed = JSON.parse(saved);
      if (parsed.appliedAt) {
        parsed.appliedAt = new Date(parsed.appliedAt);
      }

      return parsed as GallerySortState;
    } catch (error) {
      console.warn("⚠️ Failed to load sort state:", error);
      return null;
    }
  }

  async saveViewState(view: GalleryViewState): Promise<void> {
    try {
      localStorage.setItem(this.VIEW_STATE_KEY, JSON.stringify(view));
    } catch (error) {
      console.error("❌ Failed to save view state:", error);
    }
  }

  async loadViewState(): Promise<GalleryViewState | null> {
    try {
      const saved = localStorage.getItem(this.VIEW_STATE_KEY);
      if (!saved) return null;

      return JSON.parse(saved) as GalleryViewState;
    } catch (error) {
      console.warn("⚠️ Failed to load view state:", error);
      return null;
    }
  }

  async saveScrollState(scroll: GalleryScrollState): Promise<void> {
    try {
      localStorage.setItem(this.SCROLL_STATE_KEY, JSON.stringify(scroll));
    } catch (error) {
      console.error("❌ Failed to save scroll state:", error);
    }
  }

  async loadScrollState(): Promise<GalleryScrollState | null> {
    try {
      const saved = localStorage.getItem(this.SCROLL_STATE_KEY);
      if (!saved) return null;

      return JSON.parse(saved) as GalleryScrollState;
    } catch (error) {
      console.warn("⚠️ Failed to load scroll state:", error);
      return null;
    }
  }

  async saveSelectionState(selection: GallerySelectionState): Promise<void> {
    try {
      localStorage.setItem(this.SELECTION_STATE_KEY, JSON.stringify(selection));
    } catch (error) {
      console.error("❌ Failed to save selection state:", error);
    }
  }

  async loadSelectionState(): Promise<GallerySelectionState | null> {
    try {
      const saved = localStorage.getItem(this.SELECTION_STATE_KEY);
      if (!saved) return null;

      const parsed = JSON.parse(saved);
      if (parsed.lastSelectedAt) {
        parsed.lastSelectedAt = new Date(parsed.lastSelectedAt);
      }

      return parsed as GallerySelectionState;
    } catch (error) {
      console.warn("⚠️ Failed to load selection state:", error);
      return null;
    }
  }

  // ============================================================================
  // APPLICATION TAB STATE
  // ============================================================================

  async saveApplicationTabState(tabState: ApplicationTabState): Promise<void> {
    try {
      const stateToSave = {
        ...tabState,
        lastUpdated: new Date(),
      };

      localStorage.setItem(this.APP_TAB_STATE_KEY, JSON.stringify(stateToSave));
    } catch (error) {
      console.error("❌ Failed to save application tab state:", error);
    }
  }

  async loadApplicationTabState(): Promise<ApplicationTabState | null> {
    try {
      const saved = localStorage.getItem(this.APP_TAB_STATE_KEY);
      if (!saved) return null;

      const parsed = JSON.parse(saved);
      if (parsed.lastUpdated) {
        parsed.lastUpdated = new Date(parsed.lastUpdated);
      }

      return parsed as ApplicationTabState;
    } catch (error) {
      console.warn("⚠️ Failed to load application tab state:", error);
      return null;
    }
  }

  // ============================================================================
  // UTILITY METHODS
  // ============================================================================

  async clearBrowseState(): Promise<void> {
    try {
      localStorage.removeItem(this.BROWSE_STATE_KEY);
      localStorage.removeItem(this.FILTER_STATE_KEY);
      localStorage.removeItem(this.SORT_STATE_KEY);
      localStorage.removeItem(this.VIEW_STATE_KEY);
      localStorage.removeItem(this.SCROLL_STATE_KEY);
      localStorage.removeItem(this.SELECTION_STATE_KEY);
    } catch (error) {
      console.error("❌ Failed to clear browse state:", error);
    }
  }

  async clearAllState(): Promise<void> {
    try {
      await this.clearBrowseState();
      localStorage.removeItem(this.APP_TAB_STATE_KEY);
    } catch (error) {
      console.error("❌ Failed to clear all state:", error);
    }
  }

  isStateValid(state: CompleteGalleryState): boolean {
    if (!state || !state.lastUpdated) return false;

    // Check version compatibility
    if (state.version !== this.CURRENT_VERSION) {
      console.warn("⚠️ State version mismatch, clearing state");
      return false;
    }

    // Check age
    const ageInDays =
      (Date.now() - state.lastUpdated.getTime()) / (1000 * 60 * 60 * 24);
    if (ageInDays > this.MAX_STATE_AGE_DAYS) {
      console.warn("⚠️ State is too old, clearing state");
      return false;
    }

    return true;
  }

  // ============================================================================
  // DEFAULT STATE FACTORIES
  // ============================================================================

  createDefaultBrowseState(): CompleteGalleryState {
    return {
      filter: null,
      sort: {
        method: "name_asc",
        direction: "asc",
        appliedAt: new Date(),
      },
      view: {
        mode: "grid",
        gridColumns: 4,
        thumbnailSize: "medium",
      },
      scroll: {
        scrollTop: 0,
        scrollLeft: 0,
        containerHeight: 0,
        containerWidth: 0,
      },
      selection: {
        selectedSequenceId: null,
        selectedVariationIndex: null,
        lastSelectedAt: null,
      },
      lastUpdated: new Date(),
      version: this.CURRENT_VERSION,
    };
  }

  createDefaultApplicationTabState(): ApplicationTabState {
    return {
      activeTab: "construct",
      lastActiveTab: null,
      tabStates: {},
      lastUpdated: new Date(),
    };
  }
}
