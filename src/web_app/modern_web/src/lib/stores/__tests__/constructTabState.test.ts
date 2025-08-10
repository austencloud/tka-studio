/**
 * ConstructTabState Store Tests
 *
 * Tests for the centralized state management store
 */

import { beforeEach, describe, expect, it, vi } from 'vitest';
import {
	clearError,
	constructTabState,
	setActivePanel,
	setError,
	setGridMode,
} from '../constructTabState.svelte';

// Mock the sequence state
const mockSequenceState = {
	currentSequence: null,
};

vi.mock('../sequenceState.svelte', () => ({
	getCurrentSequence: () => mockSequenceState.currentSequence,
	state: {
		get currentSequence() {
			return mockSequenceState.currentSequence;
		},
	},
}));

describe('ConstructTabState', () => {
	beforeEach(() => {
		// Reset state to defaults
		constructTabState.activeRightPanel = 'build';
		constructTabState.gridMode = 'diamond';
		constructTabState.isTransitioning = false;
		constructTabState.isSubTabTransitionActive = false;
		constructTabState.currentSubTabTransition = null;
		constructTabState.errorMessage = null;
		mockSequenceState.currentSequence = null;
	});

	describe('Initial State', () => {
		it('should have correct default values', () => {
			expect(constructTabState.activeRightPanel).toBe('build');
			expect(constructTabState.gridMode).toBe('diamond');
			expect(constructTabState.isTransitioning).toBe(false);
			expect(constructTabState.isSubTabTransitionActive).toBe(false);
			expect(constructTabState.currentSubTabTransition).toBe(null);
			expect(constructTabState.errorMessage).toBe(null);
		});

		it('should show start position picker when no sequence', () => {
			mockSequenceState.currentSequence = null;
			expect(constructTabState.shouldShowStartPositionPicker).toBe(true);
		});

		it('should show start position picker when sequence has no beats', () => {
			mockSequenceState.currentSequence = {
				id: 'test',
				name: 'Test Sequence',
				word: 'test',
				beats: [],
				thumbnails: [],
				is_favorite: false,
				is_circular: false,
				tags: [],
				metadata: {},
			} as any;
			expect(constructTabState.shouldShowStartPositionPicker).toBe(true);
		});

		it('should not show start position picker when sequence has beats', () => {
			mockSequenceState.currentSequence = {
				id: 'test',
				name: 'Test Sequence',
				word: 'test',
				beats: [{ beat_number: 1 } as any],
				thumbnails: [],
				is_favorite: false,
				is_circular: false,
				tags: [],
				metadata: {},
			} as any;
			expect(constructTabState.shouldShowStartPositionPicker).toBe(false);
		});
	});

	describe('State Management Methods', () => {
		it('should update active right panel', () => {
			constructTabState.setActiveRightPanel('generate');
			expect(constructTabState.activeRightPanel).toBe('generate');

			constructTabState.setActiveRightPanel('edit');
			expect(constructTabState.activeRightPanel).toBe('edit');

			constructTabState.setActiveRightPanel('export');
			expect(constructTabState.activeRightPanel).toBe('export');
		});

		it('should update grid mode', () => {
			constructTabState.setGridMode('box');
			expect(constructTabState.gridMode).toBe('box');

			constructTabState.setGridMode('diamond');
			expect(constructTabState.gridMode).toBe('diamond');
		});

		it('should update transitioning state', () => {
			constructTabState.setTransitioning(true);
			expect(constructTabState.isTransitioning).toBe(true);

			constructTabState.setTransitioning(false);
			expect(constructTabState.isTransitioning).toBe(false);
		});

		it('should update sub-tab transition state', () => {
			constructTabState.setSubTabTransition(true, 'test-transition-id');
			expect(constructTabState.isSubTabTransitionActive).toBe(true);
			expect(constructTabState.currentSubTabTransition).toBe('test-transition-id');

			constructTabState.setSubTabTransition(false, null);
			expect(constructTabState.isSubTabTransitionActive).toBe(false);
			expect(constructTabState.currentSubTabTransition).toBe(null);
		});

		it('should update error message', () => {
			constructTabState.setError('Test error message');
			expect(constructTabState.errorMessage).toBe('Test error message');

			constructTabState.clearError();
			expect(constructTabState.errorMessage).toBe(null);
		});
	});

	describe('Derived State Getters', () => {
		it('should return current sequence', () => {
			const testSequence = {
				id: 'test',
				name: 'Test Sequence',
				word: 'test',
				beats: [],
				thumbnails: [],
				is_favorite: false,
				is_circular: false,
				tags: [],
				metadata: {},
			} as any;
			mockSequenceState.currentSequence = testSequence;
			expect(constructTabState.currentSequence).toBe(testSequence);
		});

		it('should return hasError correctly', () => {
			expect(constructTabState.hasError).toBe(false);

			constructTabState.setError('Some error');
			expect(constructTabState.hasError).toBe(true);

			constructTabState.clearError();
			expect(constructTabState.hasError).toBe(false);
		});

		it('should return mode checks correctly', () => {
			constructTabState.setActiveRightPanel('build');
			expect(constructTabState.isInBuildMode).toBe(true);
			expect(constructTabState.isInGenerateMode).toBe(false);
			expect(constructTabState.isInEditMode).toBe(false);
			expect(constructTabState.isInExportMode).toBe(false);

			constructTabState.setActiveRightPanel('generate');
			expect(constructTabState.isInBuildMode).toBe(false);
			expect(constructTabState.isInGenerateMode).toBe(true);
			expect(constructTabState.isInEditMode).toBe(false);
			expect(constructTabState.isInExportMode).toBe(false);

			constructTabState.setActiveRightPanel('edit');
			expect(constructTabState.isInBuildMode).toBe(false);
			expect(constructTabState.isInGenerateMode).toBe(false);
			expect(constructTabState.isInEditMode).toBe(true);
			expect(constructTabState.isInExportMode).toBe(false);

			constructTabState.setActiveRightPanel('export');
			expect(constructTabState.isInBuildMode).toBe(false);
			expect(constructTabState.isInGenerateMode).toBe(false);
			expect(constructTabState.isInEditMode).toBe(false);
			expect(constructTabState.isInExportMode).toBe(true);
		});
	});

	describe('Convenience Functions', () => {
		it('should work with setActivePanel function', () => {
			setActivePanel('generate');
			expect(constructTabState.activeRightPanel).toBe('generate');
		});

		it('should work with setGridMode function', () => {
			setGridMode('box');
			expect(constructTabState.gridMode).toBe('box');
		});

		it('should work with setError and clearError functions', () => {
			setError('Test error');
			expect(constructTabState.errorMessage).toBe('Test error');

			clearError();
			expect(constructTabState.errorMessage).toBe(null);
		});
	});
});
