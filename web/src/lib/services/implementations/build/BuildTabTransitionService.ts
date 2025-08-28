/**
 * ConstructTab Transition Service
 *
 * Handles tab transitions and animations for the ConstructTab component.
 * This service manages the complex transition logic that was previously
 * embedded in the massive ConstructTab component.
 */

import type { ActiveBuildSubTab } from "$lib/state/services/state-service-interfaces";

// Simplified transition service without complex fade orchestrator

export class BuildTabTransitionService {
  /**
   * Handle main tab transitions with fade animations
   * @param targetTab - The tab to transition to
   * @param currentTab - The current active tab
   * @param setActiveRightPanel - Function to update the active tab state
   */
  async handleMainTabTransition(
    targetTab: ActiveBuildSubTab,
    currentTab: ActiveBuildSubTab,
    setActiveRightPanel: (tab: ActiveBuildSubTab) => void
  ): Promise<void> {
    if (currentTab === targetTab) {
      return; // Already on this tab
    }

    // Simple immediate transition without complex fade orchestrator
    setActiveRightPanel(targetTab);
    console.log(`🎭 Sub-tab transition: ${currentTab} → ${targetTab}`);
  }

  /**
   * Get transition functions for Svelte transitions
   */
  getSubTabTransitions() {
    return {
      in: (_node: Element) => ({
        duration: 250,
        css: (t: number) => `opacity: ${t}`,
      }),
      out: (_node: Element) => ({
        duration: 200,
        css: (t: number) => `opacity: ${1 - t}`,
      }),
    };
  }

  // Note: Removed stateful methods - components should manage their own state
}

// Create and export singleton instance
export const constructTabTransitionService =
  new BuildTabTransitionService();
