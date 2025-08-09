/**
 * ConstructTab Transition Service
 * 
 * Handles tab transitions and animations for the ConstructTab component.
 * This service manages the complex transition logic that was previously
 * embedded in the massive ConstructTab component.
 */

import {
	transitionToSubTab,
	completeSubTabTransition,
	type ConstructSubTabId,
} from '../ui/animation';
import { constructTabState, type ActiveRightPanel } from '../../stores/constructTabState.svelte';

export class ConstructTabTransitionService {
	/**
	 * Handle main tab transitions with fade animations
	 */
	async handleMainTabTransition(targetTab: ActiveRightPanel): Promise<void> {
		const currentTab = constructTabState.activeRightPanel;

		if (currentTab === targetTab) {
			return; // Already on this tab
		}

		try {
			// Start sub-tab transition
			const transitionId = await transitionToSubTab(
				currentTab as ConstructSubTabId,
				targetTab as ConstructSubTabId
			);

			if (transitionId) {
				constructTabState.setSubTabTransition(true, transitionId);

				// Update active panel for reactive state
				constructTabState.setActiveRightPanel(targetTab);

				// Complete transition after brief delay
				setTimeout(() => {
					completeSubTabTransition(transitionId, currentTab, targetTab);
					constructTabState.setSubTabTransition(false, null);
				}, 50);

				console.log(`🎭 Sub-tab transition: ${currentTab} → ${targetTab}`);
			} else {
				// Fallback to immediate switch
				constructTabState.setActiveRightPanel(targetTab);
			}
		} catch (error) {
			console.warn('Sub-tab transition failed, falling back to immediate switch:', error);
			constructTabState.setActiveRightPanel(targetTab);
		}
	}

	/**
	 * Get transition functions for Svelte transitions
	 */
	getSubTabTransitions() {
		return {
			in: (node: Element) => ({
				duration: 250,
				css: (t: number) => `opacity: ${t}`,
			}),
			out: (node: Element) => ({
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
