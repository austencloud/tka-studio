/**
 * Tab State Service
 *
 * Manages tab navigation and persistence.
 * Clean separation of tab logic from other state concerns.
 */

import { browser } from "$app/environment";
import type { IBrowseStatePersister } from "$lib/services/implementations/browse/BrowseStatePersister";
import type { ItabStateService, TabId } from "./state-service-interfaces";

class TabStateService implements ItabStateService {
  // Tab state
  #activeTab = $state<TabId>("construct");

  constructor() {}

  // ============================================================================
  // GETTERS
  // ============================================================================

  get activeTab() {
    return this.#activeTab;
  }

  get browseStatePersistence(): IBrowseStatePersister {
    // TODO: Inject the actual browse state persistence service
    // For now, return a placeholder that matches the interface
    throw new Error(
      "browseStatePersistence not implemented - needs dependency injection"
    );
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
          "motion-tester",
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

// Singleton instance
export const tabStateService = new TabStateService();
