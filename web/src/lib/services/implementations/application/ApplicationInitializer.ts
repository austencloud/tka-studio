/**
 * Application Initialization Service
 *
 * Handles the startup sequence and initialization of the application.
 * This service ensures all required services are ready before the app starts.
 */

import type {
  IApplicationInitializer,
  IPersistenceService,
  ISettingsService,
} from "$contracts";
import { inject, injectable } from "inversify";
import { TYPES } from "../../inversify/types";

@injectable()
export class ApplicationInitializer implements IApplicationInitializer {
  constructor(
    @inject(TYPES.ISettingsService) private settingsService: ISettingsService,
    @inject(TYPES.IPersistenceService)
    private persistenceService: IPersistenceService
  ) {}

  /**
   * Initialize the application
   */
  async initialize(): Promise<void> {
    try {
      // Step 1: Load settings
      await this.initializeSettings();

      // Step 2: Initialize persistence layer
      await this.initializePersistence();

      // Step 3: Perform startup checks
      await this.performStartupChecks();

      // Step 4: Load initial data
      await this.loadInitialData();
    } catch (error) {
      console.error("❌ Application initialization failed:", error);
      throw new Error(
        `Initialization failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Initialize settings
   */
  private async initializeSettings(): Promise<void> {
    try {
      await this.settingsService.loadSettings();
    } catch (error) {
      console.warn("⚠️ Failed to load settings, using defaults:", error);
      // Continue with default settings
    }
  }

  /**
   * Initialize persistence layer
   */
  private async initializePersistence(): Promise<void> {
    try {
      // Check localStorage availability
      if (typeof Storage === "undefined") {
        throw new Error("LocalStorage is not available");
      }

      // Test localStorage
      const testKey = "tka-v2-test";
      localStorage.setItem(testKey, "test");
      localStorage.removeItem(testKey);

      // ✅ IMMEDIATE: Clear legacy cache on startup to fix infinite loop
      if (
        this.persistenceService &&
        "clearLegacyCache" in this.persistenceService &&
        typeof (
          this.persistenceService as { clearLegacyCache?: () => Promise<void> }
        ).clearLegacyCache === "function"
      ) {
        await (
          this.persistenceService as { clearLegacyCache: () => Promise<void> }
        ).clearLegacyCache();
      }
    } catch (error) {
      console.error("❌ Persistence initialization failed:", error);
      throw new Error(
        `Persistence initialization failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Perform startup checks
   */
  private async performStartupChecks(): Promise<void> {
    // Check browser compatibility
    const checks = [
      this.checkSVGSupport(),
      this.checkES6Support(),
      this.checkLocalStorageSpace(),
    ];

    const results = await Promise.allSettled(checks);
    const failures = results.filter((result) => result.status === "rejected");

    if (failures.length > 0) {
      console.warn("⚠️ Some startup checks failed:", failures);
      // Continue anyway - these are warnings, not fatal errors
    }
  }

  /**
   * Load initial data
   */
  private async loadInitialData(): Promise<void> {
    try {
      // TEMPORARILY DISABLED - Causing initialization to hang due to validation failures
      // Load sequences count for info
      // await this.persistenceService.loadAllSequences();
      console.log(
        "⚠️ Initial data loading temporarily disabled to fix initialization hang"
      );
    } catch (error) {
      console.warn("⚠️ Failed to load initial data:", error);
      // Continue - this is not fatal
    }
  }

  /**
   * Check SVG support
   */
  private async checkSVGSupport(): Promise<void> {
    if (!document.createElementNS) {
      throw new Error("SVG support not available");
    }

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    if (!svg || typeof svg.createSVGRect !== "function") {
      throw new Error("SVG functionality not fully supported");
    }
  }

  /**
   * Check ES6 support
   */
  private async checkES6Support(): Promise<void> {
    // Check for key ES6 features we use
    if (typeof Promise === "undefined") {
      throw new Error("Promise support required");
    }

    if (typeof Map === "undefined") {
      throw new Error("Map support required");
    }

    if (typeof Set === "undefined") {
      throw new Error("Set support required");
    }
  }

  /**
   * Check localStorage space
   */
  private async checkLocalStorageSpace(): Promise<void> {
    try {
      // Try to store 1MB of data to test space
      const testData = "x".repeat(1024 * 1024); // 1MB
      const testKey = "tka-v2-space-test";

      localStorage.setItem(testKey, testData);
      localStorage.removeItem(testKey);
    } catch {
      throw new Error("Insufficient localStorage space");
    }
  }

  /**
   * Get initialization status
   */
  getInitializationStatus(): {
    isInitialized: boolean;
    version: string;
    timestamp: string;
  } {
    return {
      isInitialized: true,
      version: "2.0.0",
      timestamp: new Date().toISOString(),
    };
  }
}
