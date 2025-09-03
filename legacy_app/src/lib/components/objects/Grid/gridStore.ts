import { writable, derived, get } from 'svelte/store';
import type { GridData, GridLoadingState, GridMode, GridPoint, Coordinate } from './types';
import { parseGridCoordinates } from './gridUtils';

/**
 * Store for managing grid loading state
 */
export const gridLoadingState = writable<GridLoadingState>({ status: 'idle' });

/**
 * Store for current grid mode
 */
export const gridMode = writable<GridMode>('diamond');

/**
 * Store for grid data
 */
export const gridData = derived<[typeof gridLoadingState], GridData | null>(
	[gridLoadingState],
	([$gridLoadingState]) => {
		return $gridLoadingState.status === 'loaded' ? $gridLoadingState.data : null;
	}
);

/**
 * Store for debug mode
 */
export const gridDebugMode = writable<boolean>(false);

/**
 * Loads grid data for the specified mode
 */
export async function loadGridData(mode: GridMode): Promise<void> {
	// Update mode
	gridMode.set(mode);

	// Set loading state
	gridLoadingState.set({ status: 'loading' });

	try {
		// Parse the grid coordinates based on the mode
		const parsedData = parseGridCoordinates(mode);

		// Artificial delay for demo purposes (remove in production)
		await new Promise((resolve) => setTimeout(resolve, 100));

		// Set loaded state with data
		gridLoadingState.set({
			status: 'loaded',
			data: parsedData
		});
	} catch (error) {
		console.error(`Failed to load grid data for mode ${mode}:`, error);
		gridLoadingState.set({
			status: 'error',
			error: error instanceof Error ? error : new Error('Unknown error loading grid data')
		});
	}
}

/**
 * Finds closest grid point to given coordinates
 */
export function findClosestPoint(
	coords: Coordinate,
	pointType: 'hand' | 'layer2' | 'outer' | 'all' = 'hand',
	variant: 'normal' | 'strict' = 'normal'
): GridPoint | null {
	const state = get(gridLoadingState);
	if (state.status !== 'loaded') return null;

	const data = state.data;
	let points: GridPoint[] = [];

	// Collect points based on type
	if (pointType === 'hand' || pointType === 'all') {
		points = [...points, ...Object.values(data.handPoints[variant])];
	}

	if (pointType === 'layer2' || pointType === 'all') {
		points = [...points, ...Object.values(data.layer2Points[variant])];
	}

	if (pointType === 'outer' || pointType === 'all') {
		points = [...points, ...Object.values(data.outerPoints)];
	}

	if (points.length === 0) return null;

	// Find closest point
	let closestPoint: GridPoint | null = null;
	let minDistance = Infinity;

	for (const point of points) {
		const distance = calculateDistance(coords, point.coordinates);
		if (distance < minDistance) {
			minDistance = distance;
			closestPoint = point;
		}
	}

	return closestPoint;
}

/**
 * Calculates Euclidean distance between two coordinates
 */
function calculateDistance(a: Coordinate, b: Coordinate): number {
	return Math.sqrt(Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2));
}

/**
 * Get a specific grid point by its key identifier
 */
export function getGridPointByKey(key: string): GridPoint | null {
	const state = get(gridLoadingState);
	if (state.status !== 'loaded') return null;

	const data = state.data;

	// Search through all point collections
	for (const variant of ['normal', 'strict'] as const) {
		// Check hand points
		if (data.handPoints[variant][key]) {
			return data.handPoints[variant][key];
		}

		// Check layer2 points
		if (data.layer2Points[variant][key]) {
			return data.layer2Points[variant][key];
		}
	}

	// Check outer points
	if (data.outerPoints[key]) {
		return data.outerPoints[key];
	}

	// Check if it's the center point
	if (key === 'center') {
		return data.centerPoint;
	}

	return null;
}
