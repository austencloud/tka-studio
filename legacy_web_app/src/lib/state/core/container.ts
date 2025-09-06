/**
 * Modern state container utility
 *
 * This module provides a simplified approach to state management using Svelte stores.
 * It's designed to replace the more complex store/registry pattern with a more direct
 * and ergonomic API.
 *
 * Note: This implementation uses Svelte stores which are compatible with both Svelte 4
 * and Svelte 5. For Svelte 5 runes integration, use the container in Svelte components.
 */

import { writable, get, type Writable } from 'svelte/store';

/**
 * Safely clones an object, handling non-cloneable objects like class instances,
 * circular references, and other objects that structuredClone can't handle.
 *
 * @param obj The object to clone
 * @returns A deep clone of the object with non-cloneable parts handled
 */
function safeClone<T>(obj: T): T {
	// Handle primitive types and null/undefined
	if (obj === null || obj === undefined || typeof obj !== 'object') {
		return obj;
	}

	// Use a WeakMap to track processed objects to avoid circular references
	// WeakMap is better than Set for object references as it doesn't prevent garbage collection
	const seen = new WeakMap<object, any>();

	// Check if we're in a browser environment
	const isBrowser = typeof window !== 'undefined' && typeof document !== 'undefined';

	// Helper to safely check instanceof for browser-specific objects
	const isInstanceOf = (obj: any, className: string): boolean => {
		if (!isBrowser) return false;
		try {
			// Check if the global object has this constructor
			const constructor = (window as any)[className];
			return constructor && obj instanceof constructor;
		} catch (e) {
			return false;
		}
	};

	// Check for DOM nodes using a more robust approach
	const isDomNode = (obj: any): boolean => {
		if (!isBrowser) return false;

		// Check for common DOM node properties
		return (
			obj &&
			typeof obj === 'object' &&
			// Has nodeType property (all DOM nodes have this)
			(typeof obj.nodeType === 'number' ||
				// Has common DOM element methods
				(typeof obj.appendChild === 'function' && typeof obj.getAttribute === 'function') ||
				// Check constructor name for common DOM types
				(obj.constructor && /^HTML.*Element$/.test(obj.constructor.name)))
		);
	};

	/**
	 * Helper function to check if an object is cloneable by structuredClone
	 * @param value The value to check
	 * @returns True if the value is likely to be cloneable by structuredClone
	 */
	function isCloneable(value: any): boolean {
		if (value === null || value === undefined || typeof value !== 'object') {
			return true; // Primitives are always cloneable
		}

		// Check for known non-cloneable types
		if (
			typeof value === 'function' ||
			isDomNode(value) ||
			isInstanceOf(value, 'Window') ||
			value instanceof Promise ||
			value instanceof Error ||
			value instanceof WeakMap ||
			value instanceof WeakSet ||
			// Check for custom class instances (not plain objects or arrays)
			(value.constructor &&
				value.constructor.name !== 'Object' &&
				value.constructor.name !== 'Array' &&
				value.constructor.name !== 'Date' &&
				value.constructor.name !== 'RegExp' &&
				value.constructor.name !== 'Map' &&
				value.constructor.name !== 'Set')
		) {
			return false;
		}

		// For objects and arrays, we need to check their properties recursively
		// But to avoid deep recursion and potential stack overflow, we'll just
		// return true here and let the actual cloning process handle any issues
		return true;
	}

	/**
	 * Deep clone function that handles circular references and non-cloneable objects
	 * @param value The value to clone
	 * @param path Current property path for debugging
	 * @returns Cloned value
	 */
	function deepClone(value: any, path: string[] = []): any {
		// Handle primitive types
		if (value === null || value === undefined || typeof value !== 'object') {
			return value;
		}

		// Check if we've already processed this object (circular reference)
		if (seen.has(value)) {
			// Return the already cloned version
			return seen.get(value);
		}

		// Handle non-cloneable objects
		if (!isCloneable(value)) {
			// For non-cloneable objects, return null or a placeholder
			// console.debug(`Replacing non-cloneable object at path: ${path.join('.')}`, value);

			// For DOM nodes, return null
			if (isDomNode(value) || isInstanceOf(value, 'Window')) {
				return null;
			}

			// For functions, return a no-op function
			if (typeof value === 'function') {
				return function noopReplacement() {
					return null;
				};
			}

			// For other non-cloneable objects, return an empty object
			return {};
		}

		// Handle Date objects
		if (value instanceof Date) {
			return new Date(value.getTime());
		}

		// Handle RegExp objects
		if (value instanceof RegExp) {
			return new RegExp(value.source, value.flags);
		}

		// Handle Map objects
		if (value instanceof Map) {
			const clonedMap = new Map();
			seen.set(value, clonedMap);
			value.forEach((val, key) => {
				clonedMap.set(deepClone(key, [...path, 'map-key']), deepClone(val, [...path, 'map-value']));
			});
			return clonedMap;
		}

		// Handle Set objects
		if (value instanceof Set) {
			const clonedSet = new Set();
			seen.set(value, clonedSet);
			value.forEach((val) => {
				clonedSet.add(deepClone(val, [...path, 'set-value']));
			});
			return clonedSet;
		}

		// Handle arrays
		if (Array.isArray(value)) {
			const clonedArray: any[] = [];
			// Store the clone in the seen map before we start populating it
			// This handles circular references that might point back to this array
			seen.set(value, clonedArray);

			for (let i = 0; i < value.length; i++) {
				clonedArray[i] = deepClone(value[i], [...path, i.toString()]);
			}
			return clonedArray;
		}

		// Handle plain objects
		const clonedObj: Record<string, any> = {};
		// Store the clone in the seen map before we start populating it
		// This handles circular references that might point back to this object
		seen.set(value, clonedObj);

		for (const key in value) {
			if (Object.prototype.hasOwnProperty.call(value, key)) {
				try {
					clonedObj[key] = deepClone(value[key], [...path, key]);
				} catch (err) {
					// If cloning a specific property fails, replace with null
					// console.debug(`Error cloning property ${key} at path: ${path.join('.')}`, err);
					clonedObj[key] = null;
				}
			}
		}

		return clonedObj;
	}

	// First try to use structuredClone for better performance if the object seems cloneable
	try {
		// Do a quick check if the object is likely to be cloneable
		let canUseStructuredClone = true;

		// Check a few top-level properties to see if they're cloneable
		// This is a heuristic to avoid trying structuredClone on objects that will definitely fail
		if (typeof obj === 'object' && obj !== null) {
			for (const key in obj) {
				if (Object.prototype.hasOwnProperty.call(obj, key)) {
					const value = (obj as any)[key];
					if (!isCloneable(value)) {
						canUseStructuredClone = false;
						break;
					}
				}
			}
		}

		if (canUseStructuredClone) {
			return structuredClone(obj);
		}
	} catch (error) {
		// If structuredClone fails, we'll fall back to our custom implementation
		// console.debug('structuredClone failed, using custom deep clone:', error);
	}

	// Fall back to custom deep clone
	return deepClone(obj) as T;
}

/**
 * Creates a state container with the given initial state and actions
 *
 * @param initialState The initial state object
 * @param actions A function that receives the state and returns action functions
 * @returns A state container with getters and actions
 */
export function createContainer<T extends object, A extends Record<string, Function>>(
	initialState: T,
	actions: (state: T, update: (fn: (state: T) => void) => void) => A
): { state: T } & A & { reset: () => void; subscribe: Writable<T>['subscribe'] } {
	// Create a writable store with a safe clone of the initial state
	const store = writable<T>(safeClone(initialState));

	// Function to update state immutably
	const update = (fn: (state: T) => void) => {
		store.update((currentState) => {
			// Use our safe clone function that handles non-cloneable objects
			const copy = safeClone(currentState);
			fn(copy);
			return copy;
		});
	};

	// Create actions with access to state via store.update
	const boundActions = actions(
		// Proxy that forwards property access to the store value
		new Proxy({} as T, {
			get: (_, prop: string) => {
				const value = get(store);
				return value[prop as keyof T];
			},
			set: (_, prop: string, value) => {
				store.update((state) => {
					const newState = { ...state };
					(newState as any)[prop] = value;
					return newState;
				});
				return true;
			}
		}),
		update
	);

	// Create a reset function
	const reset = () => {
		// Use our safe clone function
		store.set(safeClone(initialState));
	};

	// Create the container object with proper typing
	const container = {
		get state() {
			return get(store);
		},
		...boundActions,
		reset,
		// Add subscribe method for compatibility with Svelte stores
		subscribe: store.subscribe
	};

	// Return the container with proper type
	return container as typeof container & { subscribe: typeof store.subscribe };
}

/**
 * Creates a derived value from a state container
 *
 * @param fn A function that computes the derived value
 * @returns The derived value
 */
export function createDerived<T>(fn: () => T): { value: T; _update: () => void } {
	// Create a store that can be manually updated
	const store = writable<T>(fn());

	return {
		get value() {
			return get(store);
		},
		_update: () => {
			store.set(fn());
		}
	};
}

/**
 * Creates an effect that runs when dependencies change
 *
 * @param fn A function that performs side effects
 * @returns A cleanup function
 */
export function createEffect(fn: () => void | (() => void)): () => void {
	// Execute the function immediately
	const cleanup = fn();

	// Return a cleanup function if one was provided
	return typeof cleanup === 'function' ? cleanup : () => {};
}
