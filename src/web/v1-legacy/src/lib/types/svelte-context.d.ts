/**
 * Type definitions for Svelte context API
 */

declare module 'svelte' {
  /**
   * Gets a value from the context
   */
  export function getContext<T>(key: any): T;
  
  /**
   * Sets a value in the context
   */
  export function setContext<T>(key: any, value: T): void;
  
  /**
   * Checks if a key exists in the context
   */
  export function hasContext(key: any): boolean;
}
