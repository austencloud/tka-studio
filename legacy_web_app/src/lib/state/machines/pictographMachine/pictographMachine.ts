/**
 * Pictograph State Machine
 *
 * This module provides a state machine for managing pictograph state
 * using XState 5.
 */

import { createModernMachine, createMachineContainer } from '$lib/state/core/modernMachine';
import type { PictographData } from '$lib/types/PictographData';
import type { ArrowData } from '$lib/components/objects/Arrow/ArrowData';
import type { GridData } from '$lib/components/objects/Grid/GridData';
import type { PropData } from '$lib/components/objects/Prop/PropData';
import {
	setData,
	updateComponentLoaded,
	setError,
	updateGridData,
	updatePropData,
	updateArrowData,
	reset,
	checkAllComponentsLoaded
} from './actions';

/**
 * Interface for the pictograph machine context
 */
export interface PictographMachineContext {
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
 * Type for pictograph machine events
 */
export type PictographMachineEvent =
	| { type: 'SET_DATA'; data: PictographData }
	| { type: 'UPDATE_COMPONENT_LOADED'; component: keyof PictographMachineContext['components'] }
	| { type: 'SET_ERROR'; message: string; component?: string }
	| { type: 'UPDATE_GRID_DATA'; gridData: GridData }
	| { type: 'UPDATE_PROP_DATA'; color: 'red' | 'blue'; propData: PropData }
	| { type: 'UPDATE_ARROW_DATA'; color: 'red' | 'blue'; arrowData: ArrowData }
	| { type: 'RESET' };

/**
 * Create the modern pictograph machine
 */
export const pictographMachine = createModernMachine<
	PictographMachineContext,
	PictographMachineEvent
>({
	id: 'pictograph',
	initial: 'idle',
	context: {
		status: 'idle',
		data: null,
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
	},
	states: {
		idle: {
			on: {
				SET_DATA: {
					target: 'initializing',
					actions: 'setData'
				}
			}
		},
		initializing: {
			on: {
				SET_ERROR: {
					target: 'error',
					actions: 'setError'
				}
			},
			always: {
				target: 'grid_loading'
			}
		},
		grid_loading: {
			on: {
				UPDATE_GRID_DATA: {
					actions: ['updateGridData'],
					target: 'props_loading'
				},
				UPDATE_COMPONENT_LOADED: {
					actions: ['updateComponentLoaded', 'checkAllComponentsLoaded']
				},
				SET_ERROR: {
					target: 'error',
					actions: 'setError'
				}
			}
		},
		props_loading: {
			on: {
				UPDATE_PROP_DATA: {
					actions: ['updatePropData'],
					target: 'arrows_loading'
				},
				UPDATE_COMPONENT_LOADED: {
					actions: ['updateComponentLoaded', 'checkAllComponentsLoaded']
				},
				SET_ERROR: {
					target: 'error',
					actions: 'setError'
				}
			}
		},
		arrows_loading: {
			on: {
				UPDATE_ARROW_DATA: {
					actions: ['updateArrowData']
				},
				UPDATE_COMPONENT_LOADED: {
					actions: ['updateComponentLoaded', 'checkAllComponentsLoaded']
				},
				SET_ERROR: {
					target: 'error',
					actions: 'setError'
				}
			},
			always: {
				target: 'complete',
				guard: (context: PictographMachineContext) =>
					Object.values(context.components).every(Boolean)
			}
		},
		complete: {
			on: {
				SET_DATA: {
					target: 'initializing',
					actions: 'setData'
				},
				SET_ERROR: {
					target: 'error',
					actions: 'setError'
				},
				RESET: {
					target: 'idle',
					actions: 'reset'
				}
			}
		},
		error: {
			on: {
				SET_DATA: {
					target: 'initializing',
					actions: 'setData'
				},
				RESET: {
					target: 'idle',
					actions: 'reset'
				}
			}
		}
	},
	actions: {
		setData,
		updateComponentLoaded,
		setError,
		updateGridData,
		updatePropData,
		updateArrowData,
		reset,
		checkAllComponentsLoaded
	}
});

/**
 * Create the pictograph machine container
 */
export const pictographMachineContainer = createMachineContainer(pictographMachine, {
	inspect: import.meta.env.DEV
		? (event) => {
				if (event.type === '@xstate.snapshot') {
					console.log('Pictograph Machine State:', event.snapshot);
				}
			}
		: undefined
});
