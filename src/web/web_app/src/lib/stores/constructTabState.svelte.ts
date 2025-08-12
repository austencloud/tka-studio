/**
 * ConstructTab State Management
 *
 * Centralized state management for the ConstructTab component using Svelte 5 runes.
 * This store manages all the reactive state that was previously scattered throughout
 * the massive ConstructTab component.
 */

import { getCurrentSequence, state as sequenceState } from '../state/sequenceState.svelte';

export type ActiveRightPanel = 'build' | 'generate' | 'edit' | 'export';
export type GridMode = 'diamond' | 'box';

/**
 * ConstructTab state store using Svelte 5 runes
 */
class ConstructTabState {
	// Main tab state
	activeRightPanel = $state<ActiveRightPanel>('build');
	gridMode = $state<GridMode>('diamond');

	// Transition and loading states
	isTransitioning = $state(false);
	isSubTabTransitionActive = $state(false);
	currentSubTabTransition = $state<string | null>(null);

	// Error handling
	errorMessage = $state<string | null>(null);

	// Build tab conditional logic
	shouldShowStartPositionPicker = $state(true);

	constructor() {
		// Initialize shouldShowStartPositionPicker based on current sequence
		this.updateShouldShowStartPositionPicker();
	}

	// Method to update shouldShowStartPositionPicker - called from components
	updateShouldShowStartPositionPicker() {
		const sequence = sequenceState.currentSequence;

		// Show start position picker if:
		// 1. No sequence exists, OR
		// 2. Sequence exists but has no start position set
		const shouldShow = !sequence || !sequence.start_position;

		// Only log if the value actually changes to reduce noise
		if (this.shouldShowStartPositionPicker !== shouldShow) {
			console.log(
				`🎯 Start position picker: ${shouldShow ? 'show' : 'hide'} (has start_position: ${!!sequence?.start_position}, beats: ${sequence?.beats?.length || 0})`
			);
		}

		this.shouldShowStartPositionPicker = shouldShow;
	}

	// State management methods
	setActiveRightPanel(panel: ActiveRightPanel) {
		this.activeRightPanel = panel;
	}

	setGridMode(mode: GridMode) {
		this.gridMode = mode;
	}

	setTransitioning(isTransitioning: boolean) {
		this.isTransitioning = isTransitioning;
	}

	setSubTabTransition(isActive: boolean, transitionId: string | null = null) {
		this.isSubTabTransitionActive = isActive;
		this.currentSubTabTransition = transitionId;
	}

	setError(message: string | null) {
		this.errorMessage = message;
	}

	clearError() {
		this.errorMessage = null;
	}

	// Derived state getters
	get currentSequence() {
		return getCurrentSequence();
	}

	get hasError() {
		return this.errorMessage !== null;
	}

	get isInBuildMode() {
		return this.activeRightPanel === 'build';
	}

	get isInGenerateMode() {
		return this.activeRightPanel === 'generate';
	}

	get isInEditMode() {
		return this.activeRightPanel === 'edit';
	}

	get isInExportMode() {
		return this.activeRightPanel === 'export';
	}
}

// Create and export the singleton instance
export const constructTabState = new ConstructTabState();

// Export convenience functions for common operations
export function setActivePanel(panel: ActiveRightPanel) {
	constructTabState.setActiveRightPanel(panel);
}

export function setGridMode(mode: GridMode) {
	constructTabState.setGridMode(mode);
}

export function setTransitioning(isTransitioning: boolean) {
	constructTabState.setTransitioning(isTransitioning);
}

export function setError(message: string | null) {
	constructTabState.setError(message);
}

export function clearError() {
	constructTabState.clearError();
}

// Export state accessors
export function getActivePanel(): ActiveRightPanel {
	return constructTabState.activeRightPanel;
}

export function getGridMode(): GridMode {
	return constructTabState.gridMode;
}

export function isTransitioning(): boolean {
	return constructTabState.isTransitioning;
}

export function hasError(): boolean {
	return constructTabState.hasError;
}

export function getErrorMessage(): string | null {
	return constructTabState.errorMessage;
}

export function shouldShowStartPositionPicker(): boolean {
	return constructTabState.shouldShowStartPositionPicker;
}
