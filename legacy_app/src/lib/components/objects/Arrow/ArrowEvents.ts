/**
 * Type definitions for Arrow component events
 */

/**
 * Interface for the error event detail
 */
export interface ArrowErrorEventDetail {
  message: string;
}

/**
 * Interface for the loaded event detail
 */
export interface ArrowLoadedEventDetail {
  timeout?: boolean;
}

/**
 * Type for the Arrow component's custom events
 */
export interface ArrowEvents {
  error: CustomEvent<ArrowErrorEventDetail>;
  loaded: CustomEvent<ArrowLoadedEventDetail>;
  imageLoaded: CustomEvent<void>;
}
