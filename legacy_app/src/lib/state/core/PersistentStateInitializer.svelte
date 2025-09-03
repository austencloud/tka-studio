<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';

	/**
	 * This component initializes persistent state using Svelte 5 runes.
	 * It ensures that $effect is used in the proper component context.
	 */

	// Props
	const props = $props<{
		storeKey: string;
		initialState: any;
		onStateChange: (state: any) => void;
		debounceMs?: number;
		validateData?: (data: any) => boolean;
		persistFields?: string[];
	}>();

	// Default values
	const debounceMs = props.debounceMs || 100;
	const validateData = props.validateData || (() => true);
	const persistFields = props.persistFields;

	// Create the state variable
	let state = $state(loadInitialState());

	// Set up debounced persistence
	let debounceTimer: ReturnType<typeof setTimeout> | null = null;
	let lastPersistedJson: string | null = null;

	// Function to load initial state from localStorage
	function loadInitialState() {
		// Start with the provided initial state
		let loadedValue = { ...props.initialState };

		// Try to load from localStorage if in browser
		if (browser) {
			try {
				const storedValue = localStorage.getItem(props.storeKey);
				if (storedValue) {
					const parsedValue = JSON.parse(storedValue);
					if (validateData(parsedValue)) {
						// If we have specific fields to persist, only update those
						if (persistFields && persistFields.length > 0) {
							persistFields.forEach((field: string) => {
								if (field in parsedValue) {
									(loadedValue as any)[field] = parsedValue[field];
								}
							});
						} else {
							// Otherwise merge the entire object
							loadedValue = { ...props.initialState, ...parsedValue };
						}
					}
				}
			} catch (error) {
				console.error(`Error loading state from localStorage (${props.storeKey}):`, error);
			}
		}

		return loadedValue;
	}

	// Set up effect to save to localStorage when state changes
	$effect(() => {
		if (!browser) return;

		// Notify parent of state changes
		props.onStateChange(state);

		// Clear existing timer
		if (debounceTimer) {
			clearTimeout(debounceTimer);
		}

		// Set new timer
		debounceTimer = setTimeout(() => {
			try {
				let dataToStore: any;

				// If selective persistence is enabled
				if (persistFields && persistFields.length > 0) {
					// Only persist specified fields
					dataToStore = {};
					persistFields.forEach((field: string) => {
						if (field in state) {
							dataToStore[field] = state[field];
						}
					});
				} else {
					// Persist the entire state
					dataToStore = state;
				}

				// Only persist if data has changed
				const currentJson = JSON.stringify(dataToStore);
				if (currentJson !== lastPersistedJson) {
					localStorage.setItem(props.storeKey, currentJson);
					lastPersistedJson = currentJson;
				}
			} catch (error) {
				console.error(`Error saving state to localStorage (${props.storeKey}):`, error);
			}
		}, debounceMs);
	});

	// Expose the component's API to parent components
	export function updateState(newState: any) {
		state = { ...state, ...newState };
	}
</script>
