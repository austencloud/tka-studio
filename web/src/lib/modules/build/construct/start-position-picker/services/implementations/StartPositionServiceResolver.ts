/**
 * StartPositionServiceResolver.ts - Service dependency resolution for start position picker
 */

import { resolve, TYPES } from "$shared";
import { renderPictograph } from "../../../../../../shared/pictograph/shared/utils/pictograph-rendering-utils";
import type { IStartPositionService } from "../contracts";

/**
 * Resolves and manages service dependencies for start position functionality
 */
export class StartPositionServiceResolver {
  private startPositionService: IStartPositionService | null = null;
  private resolutionAttempted = false;

  /**
   * Resolve all required services
   */
  public async resolveServices(): Promise<{
    startPositionService: IStartPositionService | null;
    renderPictograph: typeof renderPictograph;
    isResolved: boolean;
  }> {
    if (this.resolutionAttempted) {
      return {
        startPositionService: this.startPositionService,
        renderPictograph,
        isResolved: this.isServicesResolved(),
      };
    }

    this.resolutionAttempted = true;

    try {
      // Resolve start position service
      this.startPositionService = await this.resolveStartPositionService();

      console.log("🔧 StartPositionServiceResolver: Services resolved", {
        startPositionService: !!this.startPositionService,
        renderPictograph: "Available via utility function",
      });

      return {
        startPositionService: this.startPositionService,
        renderPictograph,
        isResolved: this.isServicesResolved(),
      };
    } catch (error) {
      console.error(
        "❌ StartPositionServiceResolver: Failed to resolve services",
        error
      );
      return {
        startPositionService: null,
        renderPictograph,
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
   * Get pictograph rendering function (direct utility access)
   */
  public getRenderPictograph(): typeof renderPictograph {
    return renderPictograph;
  }

  /**
   * Check if all services are resolved
   */
  public isServicesResolved(): boolean {
    return !!this.startPositionService;
  }

  /**
   * Reset services (for testing or re-initialization)
   */
  public resetServices(): void {
    this.startPositionService = null;
    this.resolutionAttempted = false;
  }

  /**
   * Resolve start position service
   */
  private async resolveStartPositionService(): Promise<IStartPositionService | null> {
    try {
      const service = resolve(
        TYPES.IStartPositionService
      ) as IStartPositionService;

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
}

/**
 * Create a new service resolver instance
 */
export function createStartPositionServiceResolver(): StartPositionServiceResolver {
  return new StartPositionServiceResolver();
}
