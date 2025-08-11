/**
 * Codex State Management with Svelte 5 Runes
 *
 * Handles reactive state for the codex component including
 * search and pictograph data using the CodexService.
 */

import type { PictographData } from '$lib/domain/PictographData';
import { CodexService } from '$lib/services/codex/CodexService';

export function createCodexState() {
	// Initialize service
	const codexService = new CodexService();

	// Core reactive state using Svelte 5 runes
	let searchTerm = $state<string>('');
	let isLoading = $state<boolean>(false);
	let pictographs = $state<PictographData[]>([]);
	let error = $state<string | null>(null);

	// Derived reactive values
	const filteredPictographs = $derived(
		!searchTerm
			? pictographs
			: pictographs.filter((pictograph) => {
					const term = searchTerm.toLowerCase();
					const letter = pictograph.letter?.toLowerCase() || '';
					const id = pictograph.id?.toLowerCase() || '';

					return letter.includes(term) || id.includes(term) || letter.startsWith(term);
				})
	);

	// Load all pictographs alphabetically (this would come from a service in real implementation)
	$effect(() => {
		loadAllPictographs();
	});

	async function loadAllPictographs() {
		isLoading = true;
		error = null;

		try {
			// Load pictographs from service
			pictographs = await codexService.loadAllPictographs();
		} catch (err) {
			console.error('Failed to load pictographs:', err);
			error = 'Failed to load pictographs. Please try again.';
			pictographs = [];
		} finally {
			isLoading = false;
		}
	}

	// Public interface
	return {
		// Reactive getters
		get searchTerm() {
			return searchTerm;
		},
		get isLoading() {
			return isLoading;
		},
		get pictographs() {
			return pictographs;
		},
		get filteredPictographs() {
			return filteredPictographs;
		},
		get error() {
			return error;
		},

		// Methods
		setSearchTerm(term: string) {
			searchTerm = term;
		},

		async refreshPictographs() {
			await loadAllPictographs();
		},

		async searchPictographs(term: string) {
			searchTerm = term;
			// The derived value will automatically update the filtered list
		},

		async getPictographByLetter(letter: string) {
			return await codexService.getPictographByLetter(letter);
		},
	};
}
