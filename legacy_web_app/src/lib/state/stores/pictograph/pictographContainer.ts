/**
 * Pictograph Container
 *
 * This module provides an implementation of the pictograph state using
 * the container-based approach with Svelte 5 runes.
 */

import { createContainer } from '$lib/state/core/container';
import { createDerived } from '$lib/state/core/container';
import type { PictographData } from '$lib/types/PictographData';
import type { ArrowData } from '$lib/components/objects/Arrow/ArrowData';
import type { GridData } from '$lib/components/objects/Grid/GridData';
import type { PropData } from '$lib/components/objects/Prop/PropData';
import { defaultPictographData } from '$lib/components/Pictograph/utils/defaultPictographData';

/**
 * Interface for the pictograph container state
 */
export interface PictographState {
	status:
		| 'idle'
		| 'initializing'
		| 'grid_loading'
		| 'props_loading'
		| 'arrows_loading'
		| 'complete'
		| 'error';
	data: PictographData | null;
	error: { message: string; component?: string; timestamp: number } | null;
	loadProgress: number;
	components: {
		grid: boolean;
		redProp: boolean;
		blueProp: boolean;
		redArrow: boolean;
		blueArrow: boolean;
	};
	stateHistory: {
		from: string;
		to: string;
		reason?: string;
		timestamp: number;
	}[];
}

/**
 * Initial state for the pictograph container
 */
const initialState: PictographState = {
	status: 'idle',
	data: defaultPictographData, // Initialize with default data instead of null
	error: null,
	loadProgress: 0,
	components: {
		grid: false,
		redProp: false,
		blueProp: false,
		redArrow: false,
		blueArrow: false
	},
	stateHistory: []
};

/**
 * Helper function to calculate progress
 */
function calculateProgress(components: PictographState['components']): number {
	const total = Object.keys(components).length;
	const loaded = Object.values(components).filter(Boolean).length;
	return Math.floor((loaded / Math.max(total, 1)) * 100);
}

/**
 * Creates a pictograph container with the given initial state
 */
function createPictographContainer() {
	return createContainer<
		PictographState,
		{
			setData: (data: PictographData) => void;
			updateComponentLoaded: (component: keyof PictographState['components']) => void;
			setError: (message: string, component?: string) => void;
			updateGridData: (gridData: GridData) => void;
			updatePropData: (color: 'red' | 'blue', propData: PropData) => void;
			updateArrowData: (color: 'red' | 'blue', arrowData: ArrowData) => void;
			reset: () => void;
			transitionTo: (newState: PictographState['status'], reason?: string) => void;
		}
	>(initialState, (state, update) => {
		// Helper function to transition between states
		function transitionTo(newState: PictographState['status'], reason?: string) {
			update((state) => {
				if (state.status === newState) return;

				const newTransition = {
					from: state.status,
					to: newState,
					reason,
					timestamp: Date.now()
				};

				state.status = newState;
				state.stateHistory = [...state.stateHistory, newTransition].slice(-10);
			});
		}

		return {
			setData: (data: PictographData) => {
				transitionTo('initializing', 'Starting to load pictograph');
				update((state) => {
					state.data = data;
					state.status = 'grid_loading';
				});
			},

			updateComponentLoaded: (component: keyof PictographState['components']) => {
				update((state) => {
					state.components[component] = true;
					state.loadProgress = calculateProgress(state.components);

					const allLoaded = Object.values(state.components).every(Boolean);
					if (allLoaded && state.status !== 'complete') {
						transitionTo('complete', 'All components loaded');
					}
				});
			},

			setError: (message: string, component?: string) => {
				update((state) => {
					state.status = 'error';
					state.error = {
						message,
						component,
						timestamp: Date.now()
					};
					state.loadProgress = 0;
				});
			},

			updateGridData: (gridData: GridData) => {
				update((state) => {
					if (!state.data) return;

					state.data = { ...state.data, gridData };
					state.components.grid = true;
					transitionTo('props_loading', 'Grid data loaded');
				});
			},

			updatePropData: (color: 'red' | 'blue', propData: PropData) => {
				update((state) => {
					if (!state.data) return;

					const key = color === 'red' ? 'redPropData' : 'bluePropData';
					const componentKey = color === 'red' ? 'redProp' : 'blueProp';

					state.data = { ...state.data, [key]: propData };
					state.components[componentKey] = true;
					transitionTo('arrows_loading', `${color} prop loaded`);
				});
			},

			updateArrowData: (color: 'red' | 'blue', arrowData: ArrowData) => {
				update((state) => {
					if (!state.data) return;

					const key = color === 'red' ? 'redArrowData' : 'blueArrowData';
					const componentKey = color === 'red' ? 'redArrow' : 'blueArrow';

					state.data = { ...state.data, [key]: arrowData };
					state.components[componentKey] = true;
				});
			},

			reset: () => {
				update((state) => {
					state.status = 'idle';
					state.data = defaultPictographData; // Use default data instead of null
					state.error = null;
					state.loadProgress = 0;
					state.components = {
						grid: false,
						redProp: false,
						blueProp: false,
						redArrow: false,
						blueArrow: false
					};
					state.stateHistory = [];
				});
			},

			transitionTo
		};
	});
}

// Create the pictograph container instance
export const pictographContainer = createPictographContainer();

// Create derived values
export const pictographData = createDerived(() => pictographContainer.state.data);

export const pictographStatus = createDerived(() => pictographContainer.state.status);

export const pictographError = createDerived(() => pictographContainer.state.error);

export const pictographLoadProgress = createDerived(() => pictographContainer.state.loadProgress);

export const isLoading = createDerived(() =>
	['initializing', 'grid_loading', 'props_loading', 'arrows_loading'].includes(
		pictographContainer.state.status
	)
);

export const isComplete = createDerived(() => pictographContainer.state.status === 'complete');

export const hasError = createDerived(() => pictographContainer.state.status === 'error');
