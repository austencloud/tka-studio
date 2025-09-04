/**
 * Application Initialization Service Interface
 *
 * Interface for application initialization and startup service.
 * Handles the startup sequence and initialization of the application.
 */

/**
 * Application initialization and startup service
 */
export interface IApplicationInitializer {
  /**
   * Initialize the application
   * Performs startup sequence including settings load, persistence setup, and startup checks
   */
  initialize(): Promise<void>;

  /**
   * Get initialization status
   * Returns current initialization state and metadata
   */
  getInitializationStatus(): {
    isInitialized: boolean;
    version: string;
    timestamp: string;
  };
}
