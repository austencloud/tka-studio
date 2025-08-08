/**
 * Svelte 5 Runes Utilities
 *
 * This module provides utilities for working with Svelte 5 runes,
 * particularly for state management and persistence.
 */

import { browser } from '$app/environment';

/**
 * Creates a persistent state variable that syncs with localStorage
 *
 * This version uses a proxy approach to avoid using $effect outside of component context
 *
 * @param key The localStorage key to use
 * @param initialValue The initial value if nothing is in localStorage
 * @param options Additional options
 * @returns A proxy that behaves like the state variable
 */
export function createPersistentState<T>(
	key: string,
	initialValue: T,
	options: {
		serialize?: (value: T) => string;
		deserialize?: (value: string) => T;
		debounceMs?: number;
		validateData?: (data: any) => boolean;
	} = {}
): T {
	// Default options
	const serialize = options.serialize || JSON.stringify;
	const deserialize = options.deserialize || JSON.parse;
	const debounceMs = options.debounceMs || 100;
	const validateData = options.validateData || (() => true);

	// Load initial value from localStorage if available
	let loadedValue = initialValue;
	if (browser) {
		try {
			const storedValue = localStorage.getItem(key);
			if (storedValue) {
				const parsedValue = deserialize(storedValue);
				if (validateData(parsedValue)) {
					loadedValue = parsedValue;
				}
			}
		} catch (error) {
			console.error(`Error loading state from localStorage (${key}):`, error);
		}
	}

	// For primitive values, we need to wrap them in an object
	const isPrimitive =
		typeof loadedValue === 'string' ||
		typeof loadedValue === 'number' ||
		typeof loadedValue === 'boolean' ||
		loadedValue === null ||
		loadedValue === undefined;

	// Create a container for our value
	const container = isPrimitive ? { value: loadedValue } : { ...(loadedValue as object) };

	// Create a debounced save function
	let saveTimeout: ReturnType<typeof setTimeout> | null = null;

	const saveToLocalStorage = () => {
		if (!browser) return;

		// Clear any existing timeout
		if (saveTimeout) {
			clearTimeout(saveTimeout);
		}

		// Set a new timeout
		saveTimeout = setTimeout(() => {
			try {
				const valueToSave = isPrimitive ? container.value : container;
				const serialized = serialize(valueToSave as T);
				localStorage.setItem(key, serialized);
			} catch (error) {
				console.error(`Error saving state to localStorage (${key}):`, error);
			}
		}, debounceMs);
	};

	// For primitive values, we need a special proxy
	if (isPrimitive) {
		// Create a special proxy for primitive values
		const handler = {
			get(target: any, prop: string | symbol) {
				if (prop === 'valueOf' || prop === 'toString' || prop === Symbol.toPrimitive) {
					return function () {
						return target.value;
					};
				}
				return target.value;
			},
			set(target: any, prop: string | symbol, value: any) {
				if (prop === 'value') {
					target.value = value;
					saveToLocalStorage();
				}
				return true;
			}
		};

		// Create a proxy that forwards operations to the primitive value
		return new Proxy(container, handler) as unknown as T;
	} else {
		// For objects, create a regular proxy
		const proxy = new Proxy(container, {
			get(target: any, prop: string | symbol) {
				return target[prop];
			},
			set(target: any, prop: string | symbol, value: any) {
				target[prop] = value;
				saveToLocalStorage();
				return true;
			}
		});

		return proxy as T;
	}
}

/**
 * Creates a persistent object state that syncs with localStorage
 * and allows selective persistence of fields
 *
 * This version uses a proxy approach to avoid using $effect outside of component context
 *
 * @param key The localStorage key to use
 * @param initialValue The initial value if nothing is in localStorage
 * @param options Additional options
 * @returns A proxy object that behaves like the state
 */
export function createPersistentObjectState<T extends object>(
	key: string,
	initialValue: T,
	options: {
		persistFields?: (keyof T)[];
		debounceMs?: number;
		validateData?: (data: any) => boolean;
	} = {}
): T {
	// Default options
	const debounceMs = options.debounceMs || 100;
	const persistFields = options.persistFields;
	const validateData = options.validateData || (() => true);

	// Load initial value from localStorage if available
	let loadedValue = { ...initialValue };
	if (browser) {
		try {
			const storedValue = localStorage.getItem(key);
			if (storedValue) {
				const parsedValue = JSON.parse(storedValue);
				if (validateData(parsedValue)) {
					// If we have specific fields to persist, only update those
					if (persistFields && persistFields.length > 0) {
						persistFields.forEach((field) => {
							if (field in parsedValue) {
								(loadedValue as any)[field] = parsedValue[field];
							}
						});
					} else {
						// Otherwise merge the entire object
						loadedValue = { ...initialValue, ...parsedValue };
					}
				}
			}
		} catch (error) {
			console.error(`Error loading state from localStorage (${key}):`, error);
		}
	}

	// Create a mutable state object
	let stateObj = { ...loadedValue };

	// Create a debounced save function
	let saveTimeout: ReturnType<typeof setTimeout> | null = null;
	let lastSavedJson: string | null = null;

	const saveToLocalStorage = () => {
		if (!browser) return;

		// Clear any existing timeout
		if (saveTimeout) {
			clearTimeout(saveTimeout);
		}

		// Set a new timeout
		saveTimeout = setTimeout(() => {
			try {
				let dataToStore: any;

				// If selective persistence is enabled
				if (persistFields && persistFields.length > 0) {
					// Only persist specified fields
					dataToStore = {};
					persistFields.forEach((field) => {
						if (field in stateObj) {
							dataToStore[field] = stateObj[field];
						}
					});
				} else {
					// Persist the entire state
					dataToStore = stateObj;
				}

				// Only persist if data has changed
				const currentJson = JSON.stringify(dataToStore);
				if (currentJson !== lastSavedJson) {
					localStorage.setItem(key, currentJson);
					lastSavedJson = currentJson;
				}
			} catch (error) {
				console.error(`Error saving state to localStorage (${key}):`, error);
			}
		}, debounceMs);
	};

	// Create a proxy to intercept property access and changes
	const proxy = new Proxy(stateObj, {
		get(target, prop) {
			return target[prop as keyof typeof target];
		},
		set(target, prop, value) {
			target[prop as keyof typeof target] = value;
			saveToLocalStorage();
			return true;
		}
	});

	return proxy as T;
}

/**
 * Creates a shared context value that can be accessed across components
 *
 * @param _key The context key (unused in this implementation)
 * @param initialValue The initial value
 * @returns The context value
 */
export function createSharedContext<T>(_key: symbol | string, initialValue: T): T {
	// Simply return the initial value - the actual context setting
	// should be done in a component using setContext
	return initialValue;
}
