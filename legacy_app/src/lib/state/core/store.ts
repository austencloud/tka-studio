/**
 * Store Factory
 *
 * Provides factory functions for creating standardized Svelte stores.
 * These factories ensure consistent patterns and automatic registration with the state registry.
 */

import { writable, derived, get, type Writable, type Readable } from 'svelte/store';
import { stateRegistry, DataCorruptionError, StorageError } from './registry';

/**
 * Create a standard store with actions
 *
 * @param id Unique identifier for the store
 * @param initialState Initial state of the store
 * @param actions Object containing action methods that update the store
 * @param options Additional options for the store
 * @returns A store with actions and standard methods
 */
export function createStore<T, A extends Record<string, Function>>(
	id: string,
	initialState: T,
	actions: (set: (state: T) => void, update: (fn: (state: T) => T) => void, get: () => T) => A,
	options: {
		persist?: boolean;
		description?: string;
	} = {}
) {
	// Create the base writable store
	const { subscribe, set, update } = writable<T>(initialState);

	// Track subscriptions for cleanup
	const wrappedSubscribe = (run: (value: T) => void, invalidate?: (value?: T) => void) => {
		const unsubscribe = subscribe(run, invalidate);
		// Register the unsubscribe function with the registry
		stateRegistry.trackSubscription(id, unsubscribe);
		return unsubscribe;
	};

	// Create a getter function
	const getState = () => get({ subscribe });

	// Create the actions
	const storeActions = actions(set, update, getState);

	// Always include a reset action
	const resetAction = {
		reset: () => set(initialState)
	};

	// Combine everything into a single store object
	const store = {
		subscribe: wrappedSubscribe,
		getSnapshot: getState, // Add getSnapshot method for compatibility
		...storeActions,
		...resetAction
	};

	// Register with the state registry
	stateRegistry.registerStore(id, store, {
		persist: options.persist,
		description: options.description
	});

	return store;
}

/**
 * Create a slice of a larger store
 *
 * @param parentStore The parent store this is a slice of
 * @param options Additional options for the store
 * @returns A derived store that updates when the selected portion changes
 */
export function createSelector<T, S>(
	parentStore: Readable<T>,
	options: {
		id?: string;
		description?: string;
	} = {}
) {
	// In this case, parentStore is already a derived store with the selector applied
	const derivedStore = parentStore;

	// Wrap subscribe to track subscriptions if we have an ID
	const wrappedStore = options.id
		? {
				subscribe: (run: (value: T) => void, invalidate?: (value?: T) => void) => {
					const unsubscribe = derivedStore.subscribe(run, invalidate);
					stateRegistry.trackSubscription(options.id!, unsubscribe);
					return unsubscribe;
				}
			}
		: derivedStore;

	// Register with the registry if an ID is provided
	if (options.id) {
		stateRegistry.registerStore(options.id, wrappedStore, {
			persist: false, // Selectors should not be persisted directly
			description: options.description
		});
	}

	return wrappedStore;
}

/**
 * Create a store that combines multiple stores
 *
 * @param stores Object containing the stores to combine
 * @param options Additional options for the store
 * @returns A derived store that updates when any of the source stores change
 */
export function combineStores<T extends Record<string, Readable<any>>>(
	stores: T,
	options: {
		id?: string;
		description?: string;
	} = {}
): Readable<{ [K in keyof T]: T[K] extends Readable<infer U> ? U : never }> {
	// Extract the store keys
	const storeKeys = Object.keys(stores) as Array<keyof T>;

	// Create an array of stores for the derived store
	const storeArray = storeKeys.map((key) => stores[key]);

	// Create the derived store
	const combinedStore = derived(storeArray, (values) => {
		// Create an object with the same keys as the input stores
		return storeKeys.reduce((result, key, index) => {
			result[key as string] = values[index];
			return result;
		}, {} as any);
	});

	// Wrap subscribe to track subscriptions if we have an ID
	const wrappedStore = options.id
		? {
				subscribe: (run: (value: any) => void, invalidate?: (value?: any) => void) => {
					const unsubscribe = combinedStore.subscribe(run, invalidate);
					stateRegistry.trackSubscription(options.id!, unsubscribe);
					return unsubscribe;
				}
			}
		: combinedStore;

	// Register with the registry if an ID is provided
	if (options.id) {
		stateRegistry.registerStore(options.id, wrappedStore, {
			persist: false, // Combined stores should not be persisted directly
			description: options.description
		});
	}

	return wrappedStore;
}

/**
 * Create a persistent store that saves to localStorage
 *
 * @param id Unique identifier for the store
 * @param initialState Initial state of the store
 * @param options Additional options for the store
 * @returns A writable store that persists to localStorage
 */
export function createPersistentStore<T extends object>(
	id: string,
	initialState: T,
	options: {
		description?: string;
		storage?: Storage;
		persistFields?: string[]; // Fields to persist (if not specified, persist all)
		debounceTime?: number; // Milliseconds to wait before persisting changes
		validateData?: (data: any) => boolean; // Custom data validation function
	} = {}
): Writable<T> {
	// Use the provided storage or default to localStorage
	const storage = options.storage || (typeof localStorage !== 'undefined' ? localStorage : null);
	const debounceTime = options.debounceTime || 200; // Default debounce time
	const persistFields = options.persistFields; // Fields to persist selectively
	let debounceTimer: ReturnType<typeof setTimeout> | null = null;
	let lastPersistedState: Partial<T> | null = null;

	// Custom validation function or use a simple one
	const validateData =
		options.validateData || ((data: any) => data !== null && typeof data === 'object');

	// Create the store with the initial state
	const {
		subscribe: innerSubscribe,
		set: innerSet,
		update: innerUpdate
	} = writable<T>(initialState, (set) => {
		// Load the persisted state when the store is initialized
		if (storage) {
			try {
				const persisted = storage.getItem(id);
				if (persisted) {
					const parsed = JSON.parse(persisted);

					// Save this as the last persisted state for comparison
					lastPersistedState = parsed;

					// Validate the parsed data before using it
					if (validateData(parsed)) {
						if (persistFields) {
							// If we're using selective persistence, only apply specified fields
							innerUpdate((current) => {
								const result = { ...current };
								persistFields.forEach((field) => {
									if (field in parsed) {
										(result as any)[field] = parsed[field];
									}
								});
								return result;
							});
						} else {
							// Otherwise apply the entire state
							set(parsed);
						}
					} else {
						throw new DataCorruptionError(id);
					}
				}
			} catch (e) {
				console.error(`Error loading persisted state for ${id}:`, e);
				// Use initial state as fallback (already set)
			}
		}

		// Return the unsubscribe function
		return () => {
			if (debounceTimer) {
				clearTimeout(debounceTimer);
			}
		};
	});

	// Track subscriptions for cleanup
	const subscribe = (run: (value: T) => void, invalidate?: (value?: T) => void) => {
		const unsubscribe = innerSubscribe(run, invalidate);
		stateRegistry.trackSubscription(id, unsubscribe);
		return unsubscribe;
	};

	// Persist the value with selective fields and debouncing
	const persistValue = (value: T) => {
		// Clear existing debounce timer
		if (debounceTimer) {
			clearTimeout(debounceTimer);
		}

		// Set a new debounce timer
		debounceTimer = setTimeout(() => {
			if (!storage) return;

			try {
				let dataToStore: any;

				// If selective persistence is enabled
				if (persistFields && persistFields.length > 0) {
					// Only persist specified fields
					dataToStore = {};
					persistFields.forEach((field) => {
						if (field in value) {
							dataToStore[field] = (value as any)[field];
						}
					});
				} else {
					// Persist the entire state
					dataToStore = value;
				}

				// Only persist if data has changed
				const currentJson = JSON.stringify(dataToStore);
				const lastJson = lastPersistedState ? JSON.stringify(lastPersistedState) : null;

				if (currentJson !== lastJson) {
					storage.setItem(id, currentJson);
					lastPersistedState = dataToStore;
				}
			} catch (e) {
				const error = e instanceof Error ? e : new Error(String(e));
				console.error(`Error persisting state for ${id}:`, error);

				// Specific handling for quota errors
				if (e instanceof DOMException && e.name === 'QuotaExceededError') {
					console.warn(`Storage quota exceeded when saving state for ${id}`);
					stateRegistry.persistState(); // Trigger registry's quota handling
				}
			}
		}, debounceTime);
	};

	// Create a store object with persistence and subscription tracking
	const persistentStore = {
		subscribe,
		set: (value: T) => {
			innerSet(value);
			persistValue(value);
		},
		update: (updater: (value: T) => T) => {
			let updatedValue: T;
			innerUpdate((current) => {
				updatedValue = updater(current);
				return updatedValue!;
			});
			persistValue(updatedValue!);
		}
	};

	// Register with the state registry
	stateRegistry.registerStore(id, persistentStore, {
		persist: true,
		description: options.description,
		persistFields: options.persistFields
	});

	return persistentStore;
}
