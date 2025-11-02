import { resolve, TYPES } from "../../../inversify";
import type {
  Dimensions,
  QualityLevel,
} from "../../shared/domain/types/background-types";
import type { IBackgroundConfigurationService } from "../../shared/services/contracts/IBackgroundConfigurationService";
import type { IBackgroundRenderingService } from "../../shared/services/contracts/IBackgroundRenderingService";
import type { IBackgroundSystem } from "../../shared/services/contracts/IBackgroundSystem";
import { createShootingStarSystem } from "../../shared/services/implementations/ShootingStarSystem";
import type {
  ShootingStarState,
  Snowflake,
} from "../domain/models/snowfall-models";
import { createSnowflakeSystem } from "./SnowflakeSystem";

export class SnowfallBackgroundSystem implements IBackgroundSystem {
  private snowflakeSystem = createSnowflakeSystem();
  private shootingStarSystem = createShootingStarSystem();

  // Services
  private renderingService: IBackgroundRenderingService;
  private configurationService: IBackgroundConfigurationService;

  private snowflakes: Snowflake[] = [];
  private shootingStarState: ShootingStarState;

  private quality: QualityLevel = "medium";
  private isInitialized: boolean = false;
  private thumbnailMode: boolean = false;

  constructor() {
    // Inject services
    this.renderingService = resolve<IBackgroundRenderingService>(
      TYPES.IBackgroundRenderingService
    );
    this.configurationService = resolve<IBackgroundConfigurationService>(
      TYPES.IBackgroundConfigurationService
    );

    this.shootingStarState = this.shootingStarSystem.initialState;
    this.isInitialized = false;
  }

  public initialize(dimensions: Dimensions, quality: QualityLevel): void {
    this.quality = quality;
    this.snowflakes = this.snowflakeSystem.initialize(dimensions, quality);

    // In thumbnail mode, increase snowflake density by 5x for better visibility
    if (this.thumbnailMode) {
      const set1 = this.snowflakeSystem.initialize(dimensions, quality);
      const set2 = this.snowflakeSystem.initialize(dimensions, quality);
      const set3 = this.snowflakeSystem.initialize(dimensions, quality);
      const set4 = this.snowflakeSystem.initialize(dimensions, quality);
      this.snowflakes = [...this.snowflakes, ...set1, ...set2, ...set3, ...set4];

      // Make snowflakes larger and brighter in thumbnail mode
      this.snowflakes.forEach((snowflake) => {
        snowflake.size *= 2.0; // Doubled from 1.5x
        snowflake.opacity = Math.min(snowflake.opacity * 1.3, 1.0); // Brighter
      });
    }

    this.shootingStarState = this.shootingStarSystem.initialState;
    this.isInitialized = true;

    // Pre-populate: Simulate animation already running
    // Distribute snowflakes across the entire viewport height
    this.snowflakes.forEach((snowflake) => {
      // Random Y position from 0 to full height (instead of starting at top)
      snowflake.y = Math.random() * dimensions.height;
      // Random progress through sway animation
      snowflake.x += Math.sin(Math.random() * Math.PI * 2) * snowflake.sway;
    });
  }

  public update(dimensions: Dimensions, frameMultiplier: number = 1.0): void {
    if (dimensions && dimensions.width > 0 && dimensions.height > 0) {
      // If not initialized, or if initialized but snowflakes are unexpectedly empty (e.g. after temporary invalid dimensions)
      // and we have valid dimensions, (re-)initialize.
      if (!this.isInitialized || this.snowflakes.length === 0) {
        this.initialize(dimensions, this.quality);
      }
    }

    if (this.isInitialized) {
      this.snowflakes = this.snowflakeSystem.update(
        this.snowflakes,
        dimensions,
        frameMultiplier
      );
      const { qualitySettings } = this.configurationService.getOptimizedConfig(
        this.quality
      );
      if (qualitySettings.enableShootingStars) {
        this.shootingStarState = this.shootingStarSystem.update(
          this.shootingStarState,
          dimensions,
          frameMultiplier
        );
      }
    }
  }

  public draw(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
    const { config, qualitySettings } =
      this.configurationService.getOptimizedConfig(this.quality);

    // Use lighter gradient in thumbnail mode for better visibility
    if (this.thumbnailMode) {
      const lightGradientStops = [
        { position: 0, color: "#2a3a5e" },
        { position: 0.5, color: "#1f2d4e" },
        { position: 1, color: "#1a4570" },
      ];
      this.renderingService.drawGradient(ctx, dimensions, lightGradientStops);
    } else {
      this.renderingService.drawGradient(
        ctx,
        dimensions,
        config.core.background.gradientStops
      );
    }

    if (this.isInitialized) {
      this.snowflakeSystem.draw(this.snowflakes, ctx, dimensions);
      if (qualitySettings.enableShootingStars) {
        this.shootingStarSystem.draw(this.shootingStarState, ctx);
      }
    }
  }

  public setQuality(quality: QualityLevel): void {
    this.quality = quality;
    if (this.snowflakeSystem.setQuality) {
      this.snowflakeSystem.setQuality(quality);
    }
  }

  public setAccessibility(_settings: {
    reducedMotion: boolean;
    highContrast: boolean;
  }): void {
    // Accessibility settings would be used for motion reduction, etc.
  }

  public setThumbnailMode(enabled: boolean): void {
    this.thumbnailMode = enabled;
  }

  public handleResize(
    oldDimensions: Dimensions,
    newDimensions: Dimensions
  ): void {
    this.snowflakes = this.snowflakeSystem.adjustToResize(
      this.snowflakes,
      oldDimensions,
      newDimensions,
      this.quality
    );

    this.shootingStarState = this.shootingStarSystem.initialState;
  }

  public cleanup(): void {
    // Clean up any resources if needed
  }
}
