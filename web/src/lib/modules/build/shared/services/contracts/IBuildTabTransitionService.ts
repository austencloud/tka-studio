/**
 * Build Tab Transition Service Interface
 *
 * Interface for handling tab transitions and animations in the Build tab.
 */

import type { ActiveBuildTab } from "$shared/domain";

export interface IBuildTabTransitionService {
  /**
   * Handle main tab transitions with fade animations
   */
  handleMainTabTransition(
    targetTab: ActiveBuildTab,
    currentTab: ActiveBuildTab,
    setActiveRightPanel: (tab: ActiveBuildTab) => void
  ): Promise<void>;

  /**
   * Get transition functions for Svelte transitions
   */
  getSubTabTransitions(): {
    in: (node: Element) => { duration: number; css: (t: number) => string };
    out: (node: Element) => { duration: number; css: (t: number) => string };
  };

  /**
   * Transition to a specific tab
   */
  transitionToTab(tabId: string): Promise<void>;

  /**
   * Get current transition state
   */
  getTransitionState(): string;

  /**
   * Check if currently transitioning
   */
  isTransitioning(): boolean;
}
