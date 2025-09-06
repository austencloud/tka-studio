/**
 * State Management Adapters with Svelte 5 Runes
 *
 * This module provides adapters between different state management approaches,
 * allowing for gradual migration from the old registry-based system to the new
 * container-based system.
 *
 * This file has a .svelte.ts extension to enable runes support.
 */

/**
 * Creates a derived container from another container using Svelte 5 runes
 *
 * @param container The source container
 * @param deriveFn A function that derives a new state from the source state
 * @returns A new container with the derived state
 */
export function deriveContainerWithRunes<T extends object, U extends object>(
  container: { state: T },
  deriveFn: (state: T) => U
): { state: U } {
  return {
    get state() {
      return $derived(deriveFn(container.state));
    }
  };
}
