// src/routes/+layout.server.ts
import type { LayoutServerLoad } from './$types';

// Add a cache flag to prevent duplicate fetches
let dataCache: { diamondData: string; boxData: string } | null = null;

export const load: LayoutServerLoad = async ({ fetch: eventFetch }) => {
	// Return cached data if available
	if (dataCache) {
		return {
			csvData: dataCache,
			error: null
		};
	}

	// Fetch data silently without console logs
	try {
		// Use the event.fetch provided by SvelteKit
		const diamondResponse = await eventFetch('/DiamondPictographDataframe.csv');
		const boxResponse = await eventFetch('/BoxPictographDataframe.csv');

		if (!diamondResponse.ok || !boxResponse.ok) {
			// Return empty strings or handle error appropriately for the UI
			return {
				csvData: {
					diamondData: '',
					boxData: ''
				},
				error: 'Failed to load pictograph data files.'
			};
		}

		const diamondData = await diamondResponse.text();
		const boxData = await boxResponse.text();

		// Store in cache
		dataCache = { diamondData, boxData };

		return {
			csvData: dataCache,
			error: null // Indicate success
		};
	} catch (error) {
		console.error('Error loading CSV data:', error);
		return {
			csvData: {
				diamondData: '',
				boxData: ''
			},
			error: 'Failed to load pictograph data files.'
		};
	}
};
