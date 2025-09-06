/**
 * Gallery Tab State Manager
 *
 * Manages comprehensive state persistence for the Gallery tab including:
 * - Filter state memory
 * - Sort state memory
 * - Scroll position memory
 * - View mode memory
 * - Selected sequence memory
 *
 * Integrates with GalleryStatePersister for cross-session persistence.
 */

import { browser } from "$app/environment";
import { GallerySortMethod } from "../domain";
// import type { SequenceData } from "$shared/domain";
import type {
  CompleteGalleryState,
  GalleryScrollState,
  GalleryViewState,
} from "./gallery-state-models";

// ============================================================================
// BROWSE TAB STATE MANAGER
// ============================================================================

export class GalleryTabStateManager {
  private persistenceService = resolve(TYPES.IBrowseStatePersister);
  private saveTimeout: number | null = null;
  private readonly SAVE_DEBOUNCE_MS = 500; // Debounce saves to avoid excessive localStorage writes

  // ============================================================================
  // STATE PERSISTENCE
  // ============================================================================

  /**
   * Save complete browse state
   */
  async saveState(state: CompleteGalleryState): Promise<void> {
    if (!browser) return;

    // Debounce saves to avoid excessive localStorage writes
    if (this.saveTimeout) {
      clearTimeout(this.saveTimeout);
    }

    this.saveTimeout = window.setTimeout(async () => {
      try {
        // Convert to persistence service format
        const persistenceState = {
          filter: null, // TODO: Map from state.searchQuery
          sort: {
            method: state.sort.sortMethod as
              | "name_asc"
              | "name_desc"
              | "difficulty"
              | "length"
              | "recent"
              | "author",
            direction: state.sort.sortDirection,
            appliedAt: new Date(),
          },
          view: {
            mode: state.view.viewMode,
            gridColumns: state.view.itemsPerPage,
            thumbnailSize: "medium" as const,
          },
          scroll: state.scroll,
          selection: {
            selectedSequenceId: state.selectedItems?.[0] || null,
            selectedVariationIndex: null,
            lastSelectedAt: null,
          },
          lastUpdated: new Date(),
          version: 1,
        };
        await this.persistenceService.saveBrowseState(persistenceState);
        console.log("💾 Gallery state saved successfully");
      } catch (error) {
        console.error("❌ Failed to save browse state:", error);
      }
    }, this.SAVE_DEBOUNCE_MS);
  }

  /**
   * Load complete browse state
   */
  async loadState(): Promise<CompleteGalleryState | null> {
    if (!browser) return null;

    try {
      const state = await this.persistenceService.loadBrowseState();
      if (state) {
        console.log("📖 Gallery state loaded successfully");
        // Convert from persistence format to state manager format
        const convertedState: CompleteGalleryState = {
          scroll: state.scroll,
          sort: {
            sortMethod: state.sort.method,
            sortDirection: state.sort.direction,
          },
          view: {
            viewMode: state.view.mode,
            showPreview: false,
            itemsPerPage: state.view.gridColumns || 12,
          },
          searchQuery: "",
          selectedItems: state.selection.selectedSequenceId
            ? [state.selection.selectedSequenceId]
            : [],
        };
        return convertedState;
      }
    } catch (error) {
      console.error("❌ Failed to load browse state:", error);
    }

    return null;
  }

  /**
   * Get default state when no saved state exists
   */
  getDefaultState(): CompleteGalleryState {
    const defaultPersistenceState =
      this.persistenceService.createDefaultBrowseState();
    // Convert from persistence format to state manager format
    const convertedState: CompleteGalleryState = {
      scroll: defaultPersistenceState.scroll,
      sort: {
        sortMethod: defaultPersistenceState.sort.method,
        sortDirection: defaultPersistenceState.sort.direction,
      },
      view: {
        viewMode: defaultPersistenceState.view.mode,
        showPreview: false,
        itemsPerPage: defaultPersistenceState.view.gridColumns || 12,
      },
      searchQuery: "",
      selectedItems: [],
    };
    return convertedState;
  }

  // ============================================================================
  // INDIVIDUAL STATE COMPONENT HELPERS
  // ============================================================================

  /**
   * Save filter state
   */
  async saveFilterState(type: string | null, value: unknown): Promise<void> {
    if (!browser) return;

    const filterState = {
      type,
      value,
      appliedAt: new Date(),
    };

    try {
      await this.persistenceService.saveFilterState(filterState);
    } catch (error) {
      console.error("❌ Failed to save filter state:", error);
    }
  }

  /**
   * Save sort state
   */
  async saveSortState(method: GallerySortMethod): Promise<void> {
    if (!browser) return;

    const sortState = {
      method: this.mapSortMethodToString(method),
      direction: "asc" as const, // Default direction
      appliedAt: new Date(),
    };

    try {
      await this.persistenceService.saveSortState(sortState);
    } catch (error) {
      console.error("❌ Failed to save sort state:", error);
    }
  }

  /**
   * Save view state
   */
  async saveViewState(
    mode: "grid" | "list",
    gridColumns?: number
  ): Promise<void> {
    if (!browser) return;

    const viewState: GalleryViewState = {
      viewMode: mode,
      itemsPerPage: gridColumns || 12,
      showPreview: false, // Default value
    };

    // Convert to persistence format
    const persistenceViewState = {
      mode: viewState.viewMode,
      gridColumns: viewState.itemsPerPage,
      thumbnailSize: "medium" as const,
    };

    try {
      await this.persistenceService.saveViewState(persistenceViewState);
    } catch (error) {
      console.error("❌ Failed to save view state:", error);
    }
  }

  /**
   * Save scroll state
   */
  async saveScrollState(
    scrollTop: number,
    scrollLeft: number,
    containerHeight: number,
    containerWidth: number
  ): Promise<void> {
    if (!browser) return;

    const scrollState: GalleryScrollState = {
      scrollTop,
      scrollLeft,
      containerHeight,
      containerWidth,
    };

    try {
      await this.persistenceService.saveScrollState(scrollState);
    } catch (error) {
      console.error("❌ Failed to save scroll state:", error);
    }
  }

  /**
   * Save selection state
   */
  async saveSelectionState(
    selectedSequenceId: string | null,
    selectedVariationIndex: number | null
  ): Promise<void> {
    if (!browser) return;

    const selectionState = {
      selectedSequenceId,
      selectedVariationIndex,
      lastSelectedAt: selectedSequenceId ? new Date() : null,
    };

    try {
      await this.persistenceService.saveSelectionState(selectionState);
    } catch (error) {
      console.error("❌ Failed to save selection state:", error);
    }
  }

  // ============================================================================
  // STATE RESTORATION HELPERS
  // ============================================================================

  /**
   * Restore scroll position to a container element
   */
  restoreScrollPosition(
    container: HTMLElement,
    scrollState: GalleryScrollState
  ): void {
    if (!container || !scrollState) return;

    // Use requestAnimationFrame to ensure the DOM is ready
    requestAnimationFrame(() => {
      try {
        container.scrollTop = scrollState.scrollTop;
        container.scrollLeft = scrollState.scrollLeft;
        console.log(`📜 Scroll position restored: ${scrollState.scrollTop}px`);
      } catch (error) {
        console.warn("⚠️ Failed to restore scroll position:", error);
      }
    });
  }

  /**
   * Create a scroll state observer for automatic saving
   */
  createScrollObserver(container: HTMLElement): () => void {
    if (!browser || !container) return () => {};

    let saveTimeout: number | null = null;

    const handleScroll = () => {
      if (saveTimeout) {
        clearTimeout(saveTimeout);
      }

      saveTimeout = window.setTimeout(() => {
        this.saveScrollState(
          container.scrollTop,
          container.scrollLeft,
          container.clientHeight,
          container.clientWidth
        );
      }, this.SAVE_DEBOUNCE_MS);
    };

    container.addEventListener("scroll", handleScroll, { passive: true });

    // Return cleanup function
    return () => {
      container.removeEventListener("scroll", handleScroll);
      if (saveTimeout) {
        clearTimeout(saveTimeout);
      }
    };
  }

  // ============================================================================
  // UTILITY METHODS
  // ============================================================================

  /**
   * Map GallerySortMethod enum to string for persistence
   */
  private mapSortMethodToString(
    method: GallerySortMethod
  ): "name_asc" | "name_desc" | "difficulty" | "length" | "recent" | "author" {
    switch (method) {
      case GallerySortMethod.ALPHABETICAL:
        return "name_asc";
      case GallerySortMethod.difficultyLevel:
        return "difficulty";
      case GallerySortMethod.sequenceLength:
        return "length";
      case GallerySortMethod.dateAdded:
        return "recent";
      case GallerySortMethod.AUTHOR:
        return "author";
      default:
        return "name_asc";
    }
  }

  /**
   * Map string back to GallerySortMethod enum
   */
  mapStringToSortMethod(method: string): GallerySortMethod {
    switch (method) {
      case "name_asc":
      case "name_desc":
        return GallerySortMethod.ALPHABETICAL;
      case "difficulty":
        return GallerySortMethod.difficultyLevel;
      case "length":
        return GallerySortMethod.sequenceLength;
      case "recent":
        return GallerySortMethod.dateAdded;
      case "author":
        return GallerySortMethod.AUTHOR;
      default:
        return GallerySortMethod.ALPHABETICAL;
    }
  }

  /**
   * Clear all browse state
   */
  async clearState(): Promise<void> {
    if (!browser) return;

    try {
      await this.persistenceService.clearBrowseState();
      console.log("🗑️ Gallery state cleared successfully");
    } catch (error) {
      console.error("❌ Failed to clear browse state:", error);
    }
  }
}

// ============================================================================
// SINGLETON INSTANCE
// ============================================================================

let browseTabStateManager: GalleryTabStateManager | null = null;

/**
 * Get the singleton instance of GalleryTabStateManager
 */
export function getGalleryStateManager(): GalleryTabStateManager {
  if (!browseTabStateManager) {
    browseTabStateManager = new GalleryTabStateManager();
  }
  return browseTabStateManager;
}
