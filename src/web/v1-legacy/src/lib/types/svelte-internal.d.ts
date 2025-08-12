/**
 * Type definitions for Svelte internal modules
 */

declare module 'svelte/internal' {
  /**
   * Lifecycle function that runs when a component is mounted to the DOM
   */
  export function onMount(fn: () => void | (() => void)): void;
  
  /**
   * Lifecycle function that runs before a component is unmounted
   */
  export function onDestroy(fn: () => void): void;
  
  /**
   * Lifecycle function that runs after the component is first rendered to the DOM
   */
  export function afterUpdate(fn: () => void): void;
  
  /**
   * Lifecycle function that runs before the component is updated
   */
  export function beforeUpdate(fn: () => void): void;
  
  /**
   * Creates a writable store
   */
  export function writable<T>(value: T): {
    set: (value: T) => void;
    update: (updater: (value: T) => T) => void;
    subscribe: (run: (value: T) => void) => () => void;
  };
  
  /**
   * Creates a readable store
   */
  export function readable<T>(value: T): {
    subscribe: (run: (value: T) => void) => () => void;
  };
  
  /**
   * Creates a derived store
   */
  export function derived<T, U>(
    store: { subscribe: (run: (value: T) => void) => () => void },
    fn: (value: T) => U
  ): {
    subscribe: (run: (value: U) => void) => () => void;
  };
}
