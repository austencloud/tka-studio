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

export interface BrowseFilterState {
  type: string | null;
  value: unknown;
  appliedAt: Date;
}

export interface BrowseViewState {
  mode: "grid" | "list";
  gridColumns?: number;
  thumbnailSize?: "small" | "medium" | "large";
}

export interface BrowseScrollState {
  scrollTop: number;
  scrollLeft: number;
  containerHeight: number;
  containerWidth: number;
}

export interface BrowseSelectionState {
  selectedSequenceId: string | null;
  selectedVariationIndex: number | null;
  lastSelectedAt: Date | null;
}

export interface BrowseSortState {
  method:
    | "name_asc"
    | "name_desc"
    | "difficulty"
    | "length"
    | "recent"
    | "author";
  direction: "asc" | "desc";
  appliedAt: Date;
}

export interface CompleteBrowseState {
  filter: BrowseFilterState | null;
  sort: BrowseSortState;
  view: BrowseViewState;
  scroll: BrowseScrollState;
  selection: BrowseSelectionState;
  lastUpdated: Date;
  version: number; // For handling state migration
}

export interface ApplicationTabState {
  activeTab: string;
  lastActiveTab: string | null;
  tabStates: Record<string, unknown>;
  lastUpdated: Date;
}

export interface IBrowseStatePersistenceService {
  // Browse state persistence
  saveBrowseState(state: CompleteBrowseState): Promise<void>;
  loadBrowseState(): Promise<CompleteBrowseState | null>;

  // Individual state component persistence
  saveFilterState(filter: BrowseFilterState): Promise<void>;
  loadFilterState(): Promise<BrowseFilterState | null>;

  saveSortState(sort: BrowseSortState): Promise<void>;
  loadSortState(): Promise<BrowseSortState | null>;

  saveViewState(view: BrowseViewState): Promise<void>;
  loadViewState(): Promise<BrowseViewState | null>;

  saveScrollState(scroll: BrowseScrollState): Promise<void>;
  loadScrollState(): Promise<BrowseScrollState | null>;

  saveSelectionState(selection: BrowseSelectionState): Promise<void>;
  loadSelectionState(): Promise<BrowseSelectionState | null>;

  // Application-level tab state
  saveApplicationTabState(tabState: ApplicationTabState): Promise<void>;
  loadApplicationTabState(): Promise<ApplicationTabState | null>;

  // Utility methods
  clearBrowseState(): Promise<void>;
  clearAllState(): Promise<void>;
  isStateValid(state: CompleteBrowseState): boolean;
}

export class BrowseStatePersistenceService
  implements IBrowseStatePersistenceService
{
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

  async saveBrowseState(state: CompleteBrowseState): Promise<void> {
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

  async loadBrowseState(): Promise<CompleteBrowseState | null> {
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

      return parsed as CompleteBrowseState;
    } catch (error) {
      console.warn("⚠️ Failed to load browse state:", error);
      return null;
    }
  }

  // ============================================================================
  // INDIVIDUAL STATE COMPONENTS
  // ============================================================================

  async saveFilterState(filter: BrowseFilterState): Promise<void> {
    try {
      localStorage.setItem(this.FILTER_STATE_KEY, JSON.stringify(filter));
    } catch (error) {
      console.error("❌ Failed to save filter state:", error);
    }
  }

  async loadFilterState(): Promise<BrowseFilterState | null> {
    try {
      const saved = localStorage.getItem(this.FILTER_STATE_KEY);
      if (!saved) return null;

      const parsed = JSON.parse(saved);
      if (parsed.appliedAt) {
        parsed.appliedAt = new Date(parsed.appliedAt);
      }

      return parsed as BrowseFilterState;
    } catch (error) {
      console.warn("⚠️ Failed to load filter state:", error);
      return null;
    }
  }

  async saveSortState(sort: BrowseSortState): Promise<void> {
    try {
      localStorage.setItem(this.SORT_STATE_KEY, JSON.stringify(sort));
    } catch (error) {
      console.error("❌ Failed to save sort state:", error);
    }
  }

  async loadSortState(): Promise<BrowseSortState | null> {
    try {
      const saved = localStorage.getItem(this.SORT_STATE_KEY);
      if (!saved) return null;

      const parsed = JSON.parse(saved);
      if (parsed.appliedAt) {
        parsed.appliedAt = new Date(parsed.appliedAt);
      }

      return parsed as BrowseSortState;
    } catch (error) {
      console.warn("⚠️ Failed to load sort state:", error);
      return null;
    }
  }

  async saveViewState(view: BrowseViewState): Promise<void> {
    try {
      localStorage.setItem(this.VIEW_STATE_KEY, JSON.stringify(view));
    } catch (error) {
      console.error("❌ Failed to save view state:", error);
    }
  }

  async loadViewState(): Promise<BrowseViewState | null> {
    try {
      const saved = localStorage.getItem(this.VIEW_STATE_KEY);
      if (!saved) return null;

      return JSON.parse(saved) as BrowseViewState;
    } catch (error) {
      console.warn("⚠️ Failed to load view state:", error);
      return null;
    }
  }

  async saveScrollState(scroll: BrowseScrollState): Promise<void> {
    try {
      localStorage.setItem(this.SCROLL_STATE_KEY, JSON.stringify(scroll));
    } catch (error) {
      console.error("❌ Failed to save scroll state:", error);
    }
  }

  async loadScrollState(): Promise<BrowseScrollState | null> {
    try {
      const saved = localStorage.getItem(this.SCROLL_STATE_KEY);
      if (!saved) return null;

      return JSON.parse(saved) as BrowseScrollState;
    } catch (error) {
      console.warn("⚠️ Failed to load scroll state:", error);
      return null;
    }
  }

  async saveSelectionState(selection: BrowseSelectionState): Promise<void> {
    try {
      localStorage.setItem(this.SELECTION_STATE_KEY, JSON.stringify(selection));
    } catch (error) {
      console.error("❌ Failed to save selection state:", error);
    }
  }

  async loadSelectionState(): Promise<BrowseSelectionState | null> {
    try {
      const saved = localStorage.getItem(this.SELECTION_STATE_KEY);
      if (!saved) return null;

      const parsed = JSON.parse(saved);
      if (parsed.lastSelectedAt) {
        parsed.lastSelectedAt = new Date(parsed.lastSelectedAt);
      }

      return parsed as BrowseSelectionState;
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

  isStateValid(state: CompleteBrowseState): boolean {
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

  createDefaultBrowseState(): CompleteBrowseState {
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
