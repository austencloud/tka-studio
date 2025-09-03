// src/lib/components/Pictograph/pictographState.ts
import { writable, type Writable } from 'svelte/store';
import type { PictographData } from '$lib/types/PictographData';
import type { PropData } from '../objects/Prop/PropData';
import type { ArrowData } from '../objects/Arrow/ArrowData';
import type { GridData } from '../objects/Grid/GridData';
import type { PictographService } from './PictographService';
import { defaultPictographData } from './utils/defaultPictographData';
import type { PictographDataSnapshot } from './utils/dataComparison';

export interface IPictographState {
	pictographDataStore: Writable<PictographData>;
	currentState: Writable<string>; // Renamed from 'state' to avoid conflict
	errorMessage: Writable<string | null>;
	gridData: Writable<GridData | null>;
	redPropData: Writable<PropData | null>;
	bluePropData: Writable<PropData | null>;
	redArrowData: Writable<ArrowData | null>;
	blueArrowData: Writable<ArrowData | null>;
	loadedComponents: Writable<Set<string>>;
	requiredComponents: Writable<string[]>;
	totalComponentsToLoad: Writable<number>;
	componentsLoadedCount: Writable<number>; // Renamed from 'componentsLoaded'
	renderCount: Writable<number>;
	loadProgress: Writable<number>;
	service: Writable<PictographService | null>;
	lastDataSnapshot: Writable<PictographDataSnapshot | null>;
}

export function createPictographState(initialData?: PictographData): IPictographState {
	return {
		pictographDataStore: writable(initialData || defaultPictographData),
		currentState: writable('initializing'),
		errorMessage: writable(null),
		gridData: writable(null),
		redPropData: writable(null),
		bluePropData: writable(null),
		redArrowData: writable(null),
		blueArrowData: writable(null),
		loadedComponents: writable(new Set<string>()),
		requiredComponents: writable(['grid']),
		totalComponentsToLoad: writable(1),
		componentsLoadedCount: writable(0),
		renderCount: writable(0),
		loadProgress: writable(0),
		service: writable(null),
		lastDataSnapshot: writable(null)
	};
}

// It might be beneficial to also move functions that primarily interact with this state here.
// For example, functions to reset state, update specific parts of the state, etc.
// For now, we'll keep it focused on the state variables themselves.
