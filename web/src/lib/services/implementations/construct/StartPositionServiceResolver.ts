/**
 * StartPositionServiceResolver.ts - Service dependency resolution for start position picker
 */

import type { IStartPositionService } from "$services/interfaces/application-interfaces";
import type { IPictographRenderingService } from "$services/interfaces/pictograph-interfaces";
import { resolve } from "$services/bootstrap";

/**
 * Resolves and manages service dependencies for start position functionality
 */
export class StartPositionServiceResolver {
  private startPositionService: IStartPositionService | null = null;
  private pictographRenderingService: IPictographRenderingService | null = null;
  private resolutionAttempted = false;

  /**
   * Resolve all required services
   */
  public async resolveServices(): Promise<{
    startPositionService: IStartPositionService | null;
    pictographRenderingService: IPictographRenderingService | null;
    isResolved: boolean;
  }> {
    if (this.resolutionAttempted) {
      return {
        startPositionService: this.startPositionService,
        pictographRenderingService: this.pictographRenderingService,
        isResolved: this.isServicesResolved(),
      };
    }

    this.resolutionAttempted = true;

    try {
      // Resolve start position service
      this.startPositionService = await this.resolveStartPositionService();

      // Resolve pictograph rendering service
      this.pictographRenderingService =
        await this.resolvePictographRenderingService();

      console.log("🔧 StartPositionServiceResolver: Services resolved", {
        startPositionService: !!this.startPositionService,
        pictographRenderingService: !!this.pictographRenderingService,
      });

      return {
        startPositionService: this.startPositionService,
        pictographRenderingService: this.pictographRenderingService,
        isResolved: this.isServicesResolved(),
      };
    } catch (error) {
      console.error(
        "❌ StartPositionServiceResolver: Failed to resolve services",
        error
      );
      return {
        startPositionService: null,
        pictographRenderingService: null,
        isResolved: false,
      };
    }
  }

  /**
   * Get start position service (must call resolveServices first)
   */
  public getStartPositionService(): IStartPositionService | null {
    return this.startPositionService;
  }

  /**
   * Get pictograph rendering service (must call resolveServices first)
   */
  public getPictographRenderingService(): IPictographRenderingService | null {
    return this.pictographRenderingService;
  }

  /**
   * Check if all services are resolved
   */
  public isServicesResolved(): boolean {
    return !!(this.startPositionService && this.pictographRenderingService);
  }

  /**
   * Reset services (for testing or re-initialization)
   */
  public resetServices(): void {
    this.startPositionService = null;
    this.pictographRenderingService = null;
    this.resolutionAttempted = false;
  }

  /**
   * Resolve start position service
   */
  private async resolveStartPositionService(): Promise<IStartPositionService | null> {
    try {
      const service = resolve("IStartPositionService") as IStartPositionService;

      if (!service) {
        console.warn(
          "⚠️ StartPositionServiceResolver: IStartPositionService not found"
        );
        return null;
      }

      console.log(
        "✅ StartPositionServiceResolver: IStartPositionService resolved"
      );
      return service;
    } catch (error) {
      console.error(
        "❌ StartPositionServiceResolver: Failed to resolve IStartPositionService",
        error
      );
      return null;
    }
  }

  /**
   * Resolve pictograph rendering service
   */
  private async resolvePictographRenderingService(): Promise<IPictographRenderingService | null> {
    try {
      const service = resolve(
        "IPictographRenderingService"
      ) as IPictographRenderingService;

      if (!service) {
        console.warn(
          "⚠️ StartPositionServiceResolver: IPictographRenderingService not found"
        );
        return null;
      }

      console.log(
        "✅ StartPositionServiceResolver: IPictographRenderingService resolved"
      );
      return service;
    } catch (error) {
      console.error(
        "❌ StartPositionServiceResolver: Failed to resolve IPictographRenderingService",
        error
      );
      return null;
    }
  }
}

/**
 * Create a new service resolver instance
 */
export function createStartPositionServiceResolver(): StartPositionServiceResolver {
  return new StartPositionServiceResolver();
}
