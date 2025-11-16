import { inject, injectable } from "inversify";
import type {
  AccessibilitySettings,
  Dimensions,
  IBackgroundSystem,
  PerformanceMetrics,
  QualityLevel,
} from "../../shared";
import { TYPES } from "$shared/inversify/types";
import type { DeepOceanState } from "../domain/models/DeepOceanModels";
import type { IBubblePhysics, IMarineLifeAnimator, IParticleSystem, IOceanRenderer, ILightRayCalculator } from "./contracts";
import {  } from "./contracts";
/**
 * Deep Ocean Background Orchestrator
 *
 * Thin coordinator that delegates to focused services.
 * Replaces the 792-line monolithic DeepOceanBackgroundSystem.
 */
@injectable()
export class DeepOceanBackgroundOrchestrator implements IBackgroundSystem {
  private state: DeepOceanState;
  private quality: QualityLevel = "medium";
  private accessibility: AccessibilitySettings = {
    reducedMotion: false,
    highContrast: false,
    visibleParticleSize: 1,
  };
  private animationTime = 0;
  private thumbnailMode: boolean = false;

  constructor(
    @inject(TYPES.IBubblePhysics)
    private bubblePhysics: IBubblePhysics,

    @inject(TYPES.IMarineLifeAnimator)
    private marineLifeAnimator: IMarineLifeAnimator,

    @inject(TYPES.IParticleSystem)
    private particleSystem: IParticleSystem,

    @inject(TYPES.IOceanRenderer)
    private oceanRenderer: IOceanRenderer,

    @inject(TYPES.ILightRayCalculator)
    private lightRayCalculator: ILightRayCalculator
  ) {
    this.state = {
      bubbles: [],
      marineLife: [],
      particles: [],
      currentGradient: {
        top: "#0d2d47", // Rich ocean blue
        bottom: "#091a2b", // Darker ocean depth
      },
      lightRays: [],
      pendingSpawns: [],
    };
  }

  async initialize(
    dimensions: Dimensions,
    quality: QualityLevel
  ): Promise<void> {
    this.quality = quality;
    this.animationTime = 0;

    // Delegate initialization to focused services
    const bubbleCount = this.bubblePhysics.getBubbleCount(quality);
    this.state.bubbles = this.bubblePhysics.initializeBubbles(
      dimensions,
      bubbleCount
    );

    // MarineLifeAnimator handles sprite preloading internally
    const marineLifeCount = this.marineLifeAnimator.getMarineLifeCount(quality);
    const fishCount = Math.ceil(marineLifeCount * 0.7); // 70% fish
    const jellyfishCount = Math.floor(marineLifeCount * 0.3); // 30% jellyfish
    this.state.marineLife = await this.marineLifeAnimator.initializeMarineLife(
      dimensions,
      fishCount,
      jellyfishCount
    );

    const particleCount = this.particleSystem.getParticleCount(quality);
    this.state.particles = this.particleSystem.initializeParticles(
      dimensions,
      particleCount
    );

    const lightRayCount = this.lightRayCalculator.getLightRayCount(quality);
    this.state.lightRays = this.lightRayCalculator.initializeLightRays(
      dimensions,
      lightRayCount
    );

    // Pre-populate for smooth initial animation
    this.prePopulateElements(dimensions);

    console.log(
      `🌊 Deep Ocean background initialized with ${this.state.bubbles.length} bubbles, ${this.state.marineLife.length} marine life`
    );
  }

  private prePopulateElements(dimensions: Dimensions): void {
    // Spread bubbles across full height (instead of starting at bottom)
    this.state.bubbles.forEach((bubble) => {
      bubble.y = Math.random() * dimensions.height;
    });

    // Spread particles across full height
    this.state.particles.forEach((particle) => {
      particle.y = Math.random() * dimensions.height;
    });

    // Randomize animation time so light rays appear mid-animation
    this.animationTime = Math.random() * 1000;
  }

  update(dimensions: Dimensions, frameMultiplier: number = 1.0): void {
    // Apply accessibility-aware timing
    const accessibilityMultiplier = this.accessibility.reducedMotion
      ? 0.3
      : 1.0;
    const effectiveFrameMultiplier = frameMultiplier * accessibilityMultiplier;

    // Accumulate delta time for consistent animation speed across all refresh rates
    // 0.016 represents one frame at 60fps (1/60 second), matching the original monolith
    this.animationTime += 0.016 * effectiveFrameMultiplier;

    // Delegate updates to focused services with accessibility-aware timing
    this.state.bubbles = this.bubblePhysics.updateBubbles(
      this.state.bubbles,
      dimensions,
      effectiveFrameMultiplier,
      this.animationTime
    );

    this.state.marineLife = this.marineLifeAnimator.updateMarineLife(
      this.state.marineLife,
      dimensions,
      effectiveFrameMultiplier,
      this.animationTime
    );

    this.state.particles = this.particleSystem.updateParticles(
      this.state.particles,
      dimensions,
      effectiveFrameMultiplier
    );

    this.state.lightRays = this.lightRayCalculator.updateLightRays(
      this.state.lightRays,
      effectiveFrameMultiplier
    );

    // Process any pending marine life spawns
    const newMarineLife = this.marineLifeAnimator.processPendingSpawns(
      dimensions,
      this.animationTime
    );
    this.state.marineLife.push(...newMarineLife);
  }

  draw(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
    // Delegate all rendering to the focused renderer
    this.oceanRenderer.drawOceanGradient(ctx, dimensions);
    this.oceanRenderer.drawLightRays(
      ctx,
      dimensions,
      this.state.lightRays,
      this.quality
    );
    this.oceanRenderer.drawParticles(ctx, this.state.particles);
    this.oceanRenderer.drawBubbles(ctx, this.state.bubbles);
    this.oceanRenderer.drawMarineLife(ctx, this.state.marineLife);
  }

  setQuality(quality: QualityLevel): void {
    this.quality = quality;
  }

  setAccessibilitySettings(settings: AccessibilitySettings): void {
    this.accessibility = settings;
  }

  setThumbnailMode(enabled: boolean): void {
    this.thumbnailMode = enabled;
    // Update gradient for thumbnail mode
    if (enabled) {
      this.state.currentGradient = {
        top: "#1d4d77", // Lighter ocean blue
        bottom: "#194a5b", // Lighter ocean depth
      };
    } else {
      this.state.currentGradient = {
        top: "#0d2d47", // Rich ocean blue
        bottom: "#091a2b", // Darker ocean depth
      };
    }
  }

  getMetrics(): PerformanceMetrics {
    return {
      fps: 60, // TODO: Calculate actual FPS
      warnings: [],
      particleCount:
        this.state.bubbles.length +
        this.state.marineLife.length +
        this.state.particles.length,
      renderTime: 0, // TODO: Measure if needed
      memoryUsage: 0, // TODO: Calculate if needed
    };
  }

  cleanup(): void {
    // Clear all state
    this.state.bubbles = [];
    this.state.marineLife = [];
    this.state.particles = [];
    this.state.lightRays = [];
    this.state.pendingSpawns = [];
  }

  dispose(): void {
    this.cleanup();
  }
}
