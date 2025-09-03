/**
 * Modern State Management with Svelte 5 Runes
 *
 * This module provides utilities for modern state management using Svelte 5 runes.
 * This file has a .svelte.ts extension to enable runes support.
 */

/**
 * Creates a simple state object with a getter using Svelte 5 runes
 *
 * @param initialState The initial state
 * @returns An object with a state getter
 */
export function createStateWithRunes<T>(initialState: T): { state: T } {
  const state = $state(initialState);

  return {
    get state() { return state; }
  };
}

/**
 * Creates a simple derived state object with a getter using Svelte 5 runes
 *
 * @param fn A function that computes the derived value
 * @returns An object with a state getter
 */
export function createDerivedStateWithRunes<T>(fn: () => T): { state: T } {
  const state = $derived(fn());

  return {
    get state() { return state; }
  };
}
