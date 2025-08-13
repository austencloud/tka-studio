/**
 * Browse Tab State Manager
 *
 * Manages comprehensive state persistence for the Browse tab including:
 * - Filter state memory
 * - Sort state memory
 * - Scroll position memory
 * - View mode memory
 * - Selected sequence memory
 *
 * Integrates with BrowseStatePersistenceService for cross-session persistence.
 */

import { browser } from "$app/environment";
import type { BrowseSequenceMetadata } from "$lib/domain/browse";
import { SortMethod } from "$lib/domain/browse";
import { getBrowseStatePersistence } from "./appState.svelte";
import type {
  BrowseFilterState,
  BrowseScrollState,
  BrowseSelectionState,
  BrowseSortState,
  BrowseViewState,
  CompleteBrowseState,
} from "../services/implementations/BrowseStatePersistenceService";

// ============================================================================
// BROWSE TAB STATE MANAGER
// ============================================================================

export class BrowseTabStateManager {
  private persistenceService = getBrowseStatePersistence();
  private saveTimeout: number | null = null;
  private readonly SAVE_DEBOUNCE_MS = 500; // Debounce saves to avoid excessive localStorage writes

  // ============================================================================
  // STATE PERSISTENCE
  // ============================================================================

  /**
   * Save complete browse state
   */
  async saveState(state: CompleteBrowseState): Promise<void> {
    if (!browser) return;

    // Debounce saves to avoid excessive localStorage writes
    if (this.saveTimeout) {
      clearTimeout(this.saveTimeout);
    }

    this.saveTimeout = window.setTimeout(async () => {
      try {
        await this.persistenceService.saveBrowseState(state);
        console.log("💾 Browse state saved successfully");
      } catch (error) {
        console.error("❌ Failed to save browse state:", error);
      }
    }, this.SAVE_DEBOUNCE_MS);
  }

  /**
   * Load complete browse state
   */
  async loadState(): Promise<CompleteBrowseState | null> {
    if (!browser) return null;

    try {
      const state = await this.persistenceService.loadBrowseState();
      if (state) {
        console.log("📖 Browse state loaded successfully");
        return state;
      }
    } catch (error) {
      console.error("❌ Failed to load browse state:", error);
    }

    return null;
  }

  /**
   * Get default state when no saved state exists
   */
  getDefaultState(): CompleteBrowseState {
    return this.persistenceService.createDefaultBrowseState();
  }

  // ============================================================================
  // INDIVIDUAL STATE COMPONENT HELPERS
  // ============================================================================

  /**
   * Save filter state
   */
  async saveFilterState(type: string | null, value: unknown): Promise<void> {
    if (!browser) return;

    const filterState: BrowseFilterState = {
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
  async saveSortState(method: SortMethod): Promise<void> {
    if (!browser) return;

    const sortState: BrowseSortState = {
      method: this.mapSortMethodToString(method),
      direction: "asc", // Default direction
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
    gridColumns?: number,
  ): Promise<void> {
    if (!browser) return;

    const viewState: BrowseViewState = {
      mode,
      gridColumns,
      thumbnailSize: "medium", // Default size
    };

    try {
      await this.persistenceService.saveViewState(viewState);
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
    containerWidth: number,
  ): Promise<void> {
    if (!browser) return;

    const scrollState: BrowseScrollState = {
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
    selectedVariationIndex: number | null,
  ): Promise<void> {
    if (!browser) return;

    const selectionState: BrowseSelectionState = {
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
    scrollState: BrowseScrollState,
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
          container.clientWidth,
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
   * Map SortMethod enum to string for persistence
   */
  private mapSortMethodToString(
    method: SortMethod,
  ): "name_asc" | "name_desc" | "difficulty" | "length" | "recent" | "author" {
    switch (method) {
      case SortMethod.ALPHABETICAL:
        return "name_asc";
      case SortMethod.DIFFICULTY_LEVEL:
        return "difficulty";
      case SortMethod.SEQUENCE_LENGTH:
        return "length";
      case SortMethod.DATE_ADDED:
        return "recent";
      case SortMethod.AUTHOR:
        return "author";
      default:
        return "name_asc";
    }
  }

  /**
   * Map string back to SortMethod enum
   */
  mapStringToSortMethod(method: string): SortMethod {
    switch (method) {
      case "name_asc":
      case "name_desc":
        return SortMethod.ALPHABETICAL;
      case "difficulty":
        return SortMethod.DIFFICULTY_LEVEL;
      case "length":
        return SortMethod.SEQUENCE_LENGTH;
      case "recent":
        return SortMethod.DATE_ADDED;
      case "author":
        return SortMethod.AUTHOR;
      default:
        return SortMethod.ALPHABETICAL;
    }
  }

  /**
   * Clear all browse state
   */
  async clearState(): Promise<void> {
    if (!browser) return;

    try {
      await this.persistenceService.clearBrowseState();
      console.log("🗑️ Browse state cleared successfully");
    } catch (error) {
      console.error("❌ Failed to clear browse state:", error);
    }
  }
}

// ============================================================================
// SINGLETON INSTANCE
// ============================================================================

let browseTabStateManager: BrowseTabStateManager | null = null;

/**
 * Get the singleton instance of BrowseTabStateManager
 */
export function getBrowseTabStateManager(): BrowseTabStateManager {
  if (!browseTabStateManager) {
    browseTabStateManager = new BrowseTabStateManager();
  }
  return browseTabStateManager;
}
