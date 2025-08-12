/**
 * Type definitions for $app/environment
 */

declare module '$app/environment' {
  /**
   * Whether the app is running in a browser
   */
  export const browser: boolean;
  
  /**
   * Whether the app is running in development mode
   */
  export const dev: boolean;
  
  /**
   * Whether the app is building for production
   */
  export const building: boolean;
  
  /**
   * Whether the app is running on the server
   */
  export const server: boolean;
}
