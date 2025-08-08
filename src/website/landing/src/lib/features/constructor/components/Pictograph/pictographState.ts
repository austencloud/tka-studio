// src/lib/constructor/components/Pictograph/pictographState.ts
import { writable, type Writable } from 'svelte/store';
import type { PictographData } from '$lib/constructor/types/PictographData.js';

export interface PictographStateData {
	status: 'idle' | 'initializing' | 'grid_loading' | 'props_loading' | 'arrows_loading' | 'complete' | 'error';
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

export function createPictographState(initialData?: PictographData): PictographStateData {
	return {
		status: 'idle',
		data: initialData || null,
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
}
