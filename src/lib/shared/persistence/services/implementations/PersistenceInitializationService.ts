/**
 * Persistence Initialization Service
 *
 * This service handles the initialization of your persistence layer.
 * Call this when your app starts up to ensure the database is ready.
 */

import { injectable, inject } from "inversify";
import { TYPES } from "$shared/inversify/types";
import type { IPersistenceService } from "../contracts/IPersistenceService";
import type { IPersistenceInitializationService } from "../contracts";

@injectable()
export class PersistenceInitializationService
  implements IPersistenceInitializationService
{
  private isInitialized = false;
  private initializationError?: string;

  constructor(
    @inject(TYPES.IPersistenceService)
    private persistenceService: IPersistenceService
  ) {}

  async initialize(): Promise<void> {
    try {
      console.log(
        "🔄 PersistenceInitializationService: Starting initialization..."
      );

      // Check if IndexedDB is available
      if (!this.persistenceService.isAvailable()) {
        throw new Error("IndexedDB is not available in this environment");
      }

      // Initialize the persistence service
      await this.persistenceService.initialize();

      // Restore the last active tab
      await this.restoreApplicationState();

      this.isInitialized = true;
      delete this.initializationError;

      console.log(
        "✅ PersistenceInitializationService: Initialization complete"
      );
    } catch (error) {
      this.initializationError =
        error instanceof Error ? error.message : String(error);
      console.error(
        "❌ PersistenceInitializationService: Initialization failed:",
        error
      );
      throw error;
    }
  }

  isReady(): boolean {
    return this.isInitialized && !this.initializationError;
  }

  getStatus() {
    return {
      isInitialized: this.isInitialized,
      isAvailable: this.persistenceService.isAvailable(),
      ...(this.initializationError !== undefined && {
        error: this.initializationError,
      }),
    };
  }

  /**
   * Restore application state from persistence
   */
  private async restoreApplicationState(): Promise<void> {
    try {
      // Get the last active tab
      const activeTab = await this.persistenceService.getActiveTab();
      if (activeTab) {
        console.log(`🔄 Restored active tab: ${activeTab}`);
        // You could dispatch an event here or update a global state
        // For now, just log it
      }

      // Get storage info for debugging
      const storageInfo = await this.persistenceService.getStorageInfo();
      console.log("📊 Storage info:", storageInfo);
    } catch (error) {
      console.warn("⚠️ Failed to restore application state:", error);
      // Don't throw here - this is not critical for app startup
    }
  }
}
