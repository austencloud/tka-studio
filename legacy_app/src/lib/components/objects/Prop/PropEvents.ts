/**
 * Type definitions for Prop component events
 */

/**
 * Interface for the error event detail
 */
export interface PropErrorEventDetail {
  message: string;
}

/**
 * Interface for the loaded event detail
 */
export interface PropLoadedEventDetail {
  timeout?: boolean;
}

/**
 * Type for the Prop component's custom events
 */
export interface PropEvents {
  error: CustomEvent<PropErrorEventDetail>;
  loaded: CustomEvent<PropLoadedEventDetail>;
}
