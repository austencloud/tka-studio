/**
 * ConstructTab Transition Service
 *
 * Handles tab transitions and animations for the ConstructTab component.
 * This service manages the complex transition logic that was previously
 * embedded in the massive ConstructTab component.
 */

import { constructTabState, type ActiveRightPanel } from '../../stores/constructTabState.svelte';
// Simplified transition service without complex fade orchestrator

export class ConstructTabTransitionService {
	/**
	 * Handle main tab transitions with fade animations
	 */
	async handleMainTabTransition(targetTab: ActiveRightPanel): Promise<void> {
		const currentTab = constructTabState.activeRightPanel;

		if (currentTab === targetTab) {
			return; // Already on this tab
		}

		// Simple immediate transition without complex fade orchestrator
		constructTabState.setActiveRightPanel(targetTab);
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

	/**
	 * Check if a transition is currently active
	 */
	isTransitionActive(): boolean {
		return constructTabState.isSubTabTransitionActive;
	}

	/**
	 * Get the current transition ID
	 */
	getCurrentTransitionId(): string | null {
		return constructTabState.currentSubTabTransition;
	}
}

// Create and export singleton instance
export const constructTabTransitionService = new ConstructTabTransitionService();
