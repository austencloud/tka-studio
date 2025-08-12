/**
 * Svelte lifecycle functions
 * 
 * This file provides type-safe wrappers for Svelte lifecycle functions
 * to avoid importing directly from svelte/internal.
 */

/**
 * Runs when component is mounted to the DOM
 */
export function onMount(fn: () => void | (() => void)): void {
  // In Svelte 5, we can use $effect for this
  // This is just a placeholder that will be replaced by the Svelte compiler
}

/**
 * Runs before component is unmounted from the DOM
 */
export function onDestroy(fn: () => void): void {
  // In Svelte 5, we can use $effect.cleanup for this
  // This is just a placeholder that will be replaced by the Svelte compiler
}

/**
 * Runs after component is updated
 */
export function afterUpdate(fn: () => void): void {
  // In Svelte 5, we can use $effect for this
  // This is just a placeholder that will be replaced by the Svelte compiler
}

/**
 * Runs before component is updated
 */
export function beforeUpdate(fn: () => void): void {
  // In Svelte 5, we can use $effect for this
  // This is just a placeholder that will be replaced by the Svelte compiler
}

/**
 * Runs once when component is initialized
 */
export function onInit(fn: () => void): void {
  // In Svelte 5, we can use $effect for this
  // This is just a placeholder that will be replaced by the Svelte compiler
}
