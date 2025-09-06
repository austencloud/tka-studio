<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { circleCoordinates } from './circleCoordinates';
	import type { GridData } from './GridData';
	import { settingsStore } from '$lib/state/stores/settings/settings.store';
	import type { GridMode } from './types';
	import type { GridErrorEventDetail, GridEvents } from './GridEvents';

	// Create event dispatcher for custom events
	const dispatch = createEventDispatcher<GridEvents>();

	// Props using Svelte 5 runes
	const props = $props<{
		gridMode?: GridMode;
		onPointsReady: (gridData: GridData) => void;
		debug?: boolean;
		onError?: (message: string) => void;
	}>();

	// State variables
	let gridError = $state(false);
	let gridErrorMessage = $state('');

	// Get values from settings store with fallbacks using derived values
	const effectiveGridMode = $derived(props.gridMode ?? $settingsStore.defaultGridMode);
	const effectiveDebug = $derived(props.debug ?? $settingsStore.showGridDebug);

	// Compute grid source based on mode
	let gridSrc = $state('');
	$effect(() => {
		gridSrc =
			effectiveGridMode === 'diamond'
				? '/images/grid/diamond_grid.svg'
				: '/images/grid/box_grid.svg';
	});

	/**
	 * Parses a string coordinate in the format "(x, y)" into a { x, y } object.
	 */
	function parseCoordinates(coordString: string): { x: number; y: number } | null {
		if (!coordString || coordString === 'None') return null;

		try {
			const [x, y] = coordString.replace(/[()]/g, '').split(', ').map(parseFloat);
			return { x, y };
		} catch (error) {
			console.error(`Failed to parse coordinates: "${coordString}"`, error);
			return null;
		}
	}

	function validateGridData(data: GridData): boolean {
		// Check essential properties
		if (!data.allHandPointsNormal || Object.keys(data.allHandPointsNormal).length === 0) {
			console.error('Invalid grid data: Missing hand points');
			return false;
		}

		if (!data.centerPoint || !data.centerPoint.coordinates) {
			console.error('Invalid grid data: Missing center point');
			return false;
		}

		// Check at least some points have valid coordinates
		const handPointKeys = Object.keys(data.allHandPointsNormal);
		const validPointsCount = handPointKeys.filter(
			(key) => data.allHandPointsNormal[key]?.coordinates !== null
		).length;

		if (validPointsCount === 0) {
			console.error('Invalid grid data: No valid hand points');
			return false;
		}

		return true;
	}

	// Generate fallback grid data if parsing fails
	function createFallbackGridData(): GridData {
		console.warn('Creating fallback grid data');

		const fallbackHandPoints: Record<string, { coordinates: { x: number; y: number } | null }> = {
			n_diamond_hand_point: { coordinates: { x: 475, y: 330 } },
			e_diamond_hand_point: { coordinates: { x: 620, y: 475 } },
			s_diamond_hand_point: { coordinates: { x: 475, y: 620 } },
			w_diamond_hand_point: { coordinates: { x: 330, y: 475 } },
			ne_diamond_hand_point: { coordinates: { x: 620, y: 330 } },
			se_diamond_hand_point: { coordinates: { x: 620, y: 620 } },
			sw_diamond_hand_point: { coordinates: { x: 330, y: 620 } },
			nw_diamond_hand_point: { coordinates: { x: 330, y: 330 } }
		};

		return {
			allHandPointsStrict: fallbackHandPoints,
			allHandPointsNormal: fallbackHandPoints,
			allLayer2PointsStrict: {},
			allLayer2PointsNormal: {},
			allOuterPoints: {},
			centerPoint: { coordinates: { x: 475, y: 475 } }
		};
	}

	// Flag to prevent multiple initializations
	let isInitialized = false;

	// Initialize grid data without using tick()
	function initializeGridData() {
		// Prevent multiple initializations
		if (isInitialized) return;
		isInitialized = true;

		try {
			// No need for tick() - just process the data directly
			if (
				!circleCoordinates ||
				!circleCoordinates[effectiveGridMode as keyof typeof circleCoordinates]
			) {
				throw new Error(`Invalid circle coordinates for grid mode: ${effectiveGridMode}`);
			}

			const modeData = circleCoordinates[effectiveGridMode as keyof typeof circleCoordinates];

			const parsePoints = (points: Record<string, string>) =>
				Object.fromEntries(
					Object.entries(points).map(([key, value]) => [
						key,
						{ coordinates: parseCoordinates(value) }
					])
				);

			// Convert raw data into structured `GridData`
			const gridData: GridData = {
				allHandPointsStrict: parsePoints(modeData.hand_points.strict),
				allHandPointsNormal: parsePoints(modeData.hand_points.normal),
				allLayer2PointsStrict: parsePoints(modeData.layer2_points.strict),
				allLayer2PointsNormal: parsePoints(modeData.layer2_points.normal),
				allOuterPoints: parsePoints(modeData.outer_points),
				centerPoint: { coordinates: parseCoordinates(modeData.center_point) }
			};

			// Validate before sending
			if (!validateGridData(gridData)) {
				throw new Error('Grid data validation failed');
			}

			// Use setTimeout to break potential reactive cycles
			setTimeout(() => {
				props.onPointsReady(gridData);
			}, 0);
		} catch (error) {
			console.error('Error initializing grid:', error);
			gridError = true;
			gridErrorMessage = error instanceof Error ? error.message : 'Unknown grid error';

			// Dispatch error event both ways for compatibility
			props.onError?.(gridErrorMessage);
			dispatch('error', { message: gridErrorMessage });

			// Create and return fallback grid data
			const fallbackData = createFallbackGridData();

			// Use setTimeout to break potential reactive cycles
			setTimeout(() => {
				props.onPointsReady(fallbackData);
			}, 0);
		}
	}

	// Call initialization on mount
	onMount(() => {
		initializeGridData();
	});

	function handleImageError() {
		console.error('Failed to load grid SVG image');
		gridError = true;
		gridErrorMessage = 'Failed to load grid image';

		// Dispatch error event both ways for compatibility
		props.onError?.(gridErrorMessage);
		dispatch('error', { message: gridErrorMessage });
	}
</script>

<!-- We always attempt to load the grid image -->
<image
	href={gridSrc}
	x="0"
	y="0"
	width="950"
	height="950"
	preserveAspectRatio="none"
	onerror={handleImageError}
/>

<!-- Error indicator (only visible when debugging) -->
{#if effectiveDebug && gridError}
	<text x="475" y="475" text-anchor="middle" fill="red" font-size="20">
		Grid Error: {gridErrorMessage}
	</text>
{/if}
