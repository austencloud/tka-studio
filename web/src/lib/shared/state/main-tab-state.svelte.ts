/**
 * Tab State Service
 *
 * Manages tab navigation and persistence.
 * Clean separation of tab logic from other state concerns.
 */

import { browser } from "$app/environment";
import type { IBrowseStatePersister } from "../../modules/browse/gallery/services/implementations/BrowseStatePersister";
import type { TabId } from "../domain";
// TEMPORARY: Service interfaces commented out until container is restored
import { resolve, TYPES } from "../inversify/container";
import type { IMainTabState } from "./app-state-interfaces";

class MainTabState implements IMainTabState {
  // Tab state
  #activeTab = $state<TabId>("construct");

  // Lazy-loaded services to avoid circular dependency (TEMPORARY: Type commented out)
  private _browseStatePersister: IBrowseStatePersister | null = null;

  constructor() {
    // Services will be resolved lazily when first accessed
  }

  // ============================================================================
  // GETTERS
  // ============================================================================

  get activeTab() {
    return this.#activeTab;
  }

  get browseStatePersistence(): IBrowseStatePersister {
    if (!this._browseStatePersister) {
      this._browseStatePersister = resolve<IBrowseStatePersister>(
        TYPES.IBrowseStatePersister
      );
    }
    // TypeScript knows this is not null after the check above
    return this._browseStatePersister as IBrowseStatePersister;
  }

  // ============================================================================
  // ACTIONS
  // ============================================================================

  async switchTab(tab: TabId): Promise<void> {
    if (this.#activeTab === tab) return;

    // Save current tab state before switching
    await this.saveCurrentTabState(this.#activeTab);

    const previousTab = this.#activeTab;
    this.#activeTab = tab;

    // Save application-level tab state
    await this.saveApplicationTabState(tab, previousTab);
  }

  isTabActive(tab: string): boolean {
    return this.#activeTab === tab;
  }

  // ============================================================================
  // PERSISTENCE
  // ============================================================================

  async saveCurrentTabState(currentTab: TabId): Promise<void> {
    if (!browser) return;

    try {
      // Save tab-specific state based on current tab
      switch (currentTab) {
        case "browse":
          // Browse state is handled by its own persistence service
          break;
        case "construct":
        case "sequence_card":
        case "write":
        case "learn":
          // Add tab-specific state saving logic as needed
          break;
      }
    } catch (error) {
      console.error(`Failed to save ${currentTab} tab state:`, error);
    }
  }

  async restoreApplicationState(): Promise<void> {
    if (!browser) return;

    try {
      const tabState =
        await this.browseStatePersistence.loadApplicationTabState();
      if (tabState?.activeTab && typeof tabState.activeTab === "string") {
        const validTabs: TabId[] = [
          "construct",
          "browse",
          "sequence_card",
          "write",
          "learn",
          "about",
          "animator",
        ];
        if (validTabs.includes(tabState.activeTab as TabId)) {
          this.#activeTab = tabState.activeTab as TabId;
        }
      }
    } catch (error) {
      console.error("Failed to restore application state:", error);
    }
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  private async saveApplicationTabState(
    newTab: TabId,
    previousTab: TabId
  ): Promise<void> {
    if (!browser) return;

    try {
      const tabState = {
        activeTab: newTab,
        lastActiveTab: previousTab,
        tabStates: {},
        lastUpdated: new Date(),
      };

      await this.browseStatePersistence.saveApplicationTabState(tabState);
    } catch (error) {
      console.error("Failed to save application tab state:", error);
    }
  }
}

// Export the class for DI container binding
// Singleton instance will be managed by the DI container
