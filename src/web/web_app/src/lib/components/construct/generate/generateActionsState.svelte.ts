/**
 * Simple generation actions state for GeneratePanel
 *
 * Just extracts the generation button logic without over-engineering
 */

import type { GenerationConfig } from './generateConfigState.svelte.ts';

/**
 * Creates simple reactive state for generation actions
 */
export function createGenerationActionsState() {
	// Simple generation state
	let isGenerating = $state(false);

	// Simple generate function (matches your original logic)
	function onGenerateClicked(config: GenerationConfig) {
		if (isGenerating) return;
		isGenerating = true;

		console.log('🎯 Generate clicked with config:', config);

		// Your original timeout logic
		setTimeout(() => {
			isGenerating = false;
		}, 2000);
	}

	// Simple auto-complete function (matches your original logic)
	function onAutoCompleteClicked() {
		if (isGenerating) return;
		console.log('🔄 Auto-complete clicked');
	}

	return {
		// State
		get isGenerating() {
			return isGenerating;
		},

		// Actions
		onGenerateClicked,
		onAutoCompleteClicked,
	};
}
