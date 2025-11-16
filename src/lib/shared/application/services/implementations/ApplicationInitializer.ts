import { injectable } from "inversify";
import { resolve, TYPES } from "../../../inversify";
import type { ISvgPreloadService } from "../../../pictograph/shared/services/contracts/ISvgPreloadService";
import type { IApplicationInitializer } from "../contracts/IApplicationInitializer";

/**
 * Application Initializer Implementation
 *
 * Handles application startup sequence and initialization.
 */
@injectable()
export class ApplicationInitializer implements IApplicationInitializer {
  private initialized = false;

  constructor() {}

  async initialize(): Promise<void> {
    try {
      // Step 1: Preload essential SVGs for lightning-fast prop rendering
      const svgPreloadService = resolve<ISvgPreloadService>(TYPES.ISvgPreloadService);
      await svgPreloadService.preloadEssentialSvgs();

      // TODO: Add other initialization logic
      // - Initialize settings
      // - Setup background services
      // - Load user preferences
      // - Initialize device detection

      this.initialized = true;
    } catch (error) {
      console.error("❌ ApplicationInitializer: Initialization failed:", error);
      throw error;
    }
  }

  isInitialized(): boolean {
    return this.initialized;
  }

  async shutdown(): Promise<void> {
    console.log("🔄 ApplicationInitializer: Shutting down application...");

    try {
      // TODO: Add cleanup logic
      // - Save state
      // - Close connections
      // - Clean up resources

      this.initialized = false;
      console.log("✅ ApplicationInitializer: Application shutdown complete");
    } catch (error) {
      console.error("❌ ApplicationInitializer: Shutdown failed:", error);
      throw error;
    }
  }
}
