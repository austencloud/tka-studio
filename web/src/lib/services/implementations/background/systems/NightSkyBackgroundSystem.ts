// src/lib/services/implementations/background/systems/NightSkyBackgroundSystem.ts
import { getOptimizedConfig } from "$lib/domain/background/configs/config";
import { NightSkyConfig } from "$lib/domain/background/configs/nightSky";
import { drawBackgroundGradient } from "$lib/utils/background/backgroundUtils";
import { createShootingStarSystem } from "./core/ShootingStarSystem";

// Import our new modular systems
import { ParallaxStarSystem } from "../systems/nightSky/ParallaxStarSystem";
import { NebulaSystem } from "../systems/nightSky/NebulaSystem";
import { ConstellationSystem } from "../systems/nightSky/ConstellationSystem";
import { MoonSystem } from "../systems/nightSky/MoonSystem";
import { SpaceshipSystem } from "../systems/nightSky/SpaceshipSystem";
import { CometSystem } from "../systems/nightSky/CometSystem";

import type {
  AccessibilitySettings,
  BackgroundSystem,
  Dimensions,
  QualityLevel,
  ShootingStarState,
} from "$lib/domain/background/BackgroundTypes";

export class NightSkyBackgroundSystem implements BackgroundSystem {
  // core state -------------------------------------------------------------
  private quality: QualityLevel = "medium";
  private isInitialized: boolean = false;

  // Modular systems
  private parallaxStarSystem: ParallaxStarSystem;
  private nebulaSystem: NebulaSystem;
  private constellationSystem: ConstellationSystem;
  private MoonSystem: MoonSystem;
  private spaceshipSystem: SpaceshipSystem;
  private cometSystem: CometSystem;
  private shootingStarSystem = createShootingStarSystem();
  private shootingStarState: ShootingStarState;

  // config handles ---------------------------------------------------------
  private cfg: typeof NightSkyConfig = getOptimizedConfig(this.quality).config
    .nightSky as typeof NightSkyConfig;
  private Q = getOptimizedConfig(this.quality).qualitySettings;
  private a11y: AccessibilitySettings = {
    reducedMotion: false,
    highContrast: false,
    visibleParticleSize: 2,
  };

  constructor() {
    this.shootingStarState = this.shootingStarSystem.initialState;

    // Initialize all modular systems
    this.parallaxStarSystem = new ParallaxStarSystem(
      this.cfg.parallax,
      this.cfg.stars,
      this.Q
    );

    this.nebulaSystem = new NebulaSystem(this.cfg.nebula);

    this.constellationSystem = new ConstellationSystem(this.cfg.constellations);

    this.MoonSystem = new MoonSystem(
      this.cfg.Moon,
      this.cfg.background?.gradientStops || [
        { position: 0, color: "#0c0c1e" },
        { position: 0.3, color: "#1a1a2e" },
        { position: 0.7, color: "#16213e" },
        { position: 1, color: "#0f3460" },
      ]
    );

    this.spaceshipSystem = new SpaceshipSystem(this.cfg.spaceship);

    this.cometSystem = new CometSystem(this.cfg.comet, this.cfg.stars);
  }

  // ------------------------------------------------------------------------
  /* INITIALISE */
  public initialize(dim: Dimensions, q: QualityLevel) {
    this.setQuality(q); // Sets this.cfg and this.Q

    // Initialize all modular systems
    this.parallaxStarSystem.initialize(dim, this.a11y);
    this.nebulaSystem.initialize(dim, this.quality);
    this.MoonSystem.initialize(dim, this.quality, this.a11y);

    this.isInitialized = true;
  }

  /* UPDATE */
  public update(dim: Dimensions) {
    this.parallaxStarSystem.update(dim, this.a11y);
    this.nebulaSystem.update(this.a11y);
    this.constellationSystem.update(
      this.parallaxStarSystem.getNearStars(),
      this.quality,
      this.a11y
    );
    this.MoonSystem.update(dim, this.a11y);

    if (this.Q.enableShootingStars)
      this.shootingStarState = this.shootingStarSystem.update(
        this.shootingStarState,
        dim
      );

    this.spaceshipSystem.update(dim, this.a11y, this.quality);
    this.cometSystem.update(dim, this.a11y, this.quality);
  }

  /* DRAW */
  public draw(ctx: CanvasRenderingContext2D, dim: Dimensions) {
    // Always draw the background gradient first
    const gradientStops = this.cfg.background?.gradientStops || [
      { position: 0, color: "#0c0c1e" },
      { position: 0.3, color: "#1a1a2e" },
      { position: 0.7, color: "#16213e" },
      { position: 1, color: "#0f3460" },
    ];
    drawBackgroundGradient(ctx, dim, gradientStops);

    // Only draw other elements if properly initialized
    if (this.isInitialized) {
      this.nebulaSystem.draw(ctx, this.a11y);
      this.parallaxStarSystem.draw(ctx, this.a11y);
      this.constellationSystem.draw(ctx, this.a11y);
      this.MoonSystem.draw(ctx, this.a11y);

      if (this.Q.enableShootingStars)
        this.shootingStarSystem.draw(this.shootingStarState, ctx);

      this.spaceshipSystem.draw(ctx, this.a11y);
      this.cometSystem.draw(ctx, this.a11y);
    }
  }

  /* RESIZE HANDLING */
  public handleResize(oldDimensions: Dimensions, newDimensions: Dimensions) {
    // Let the parallax star system handle the smooth resize
    this.parallaxStarSystem.update(newDimensions, this.a11y);

    // Update other systems that need dimension changes
    this.nebulaSystem.update(this.a11y);
    this.MoonSystem.update(newDimensions, this.a11y);
    this.spaceshipSystem.update(newDimensions, this.a11y, this.quality);
    this.cometSystem.update(newDimensions, this.a11y, this.quality);
  }

  /* QUALITY / A11Y */
  public setQuality(q: QualityLevel) {
    if (this.quality === q) return;
    this.quality = q;
    // Re-fetch optimized config when quality changes
    const optimized = getOptimizedConfig(q);
    this.cfg = optimized.config.nightSky as typeof NightSkyConfig;
    this.Q = optimized.qualitySettings;

    // Update all systems with new config
    this.parallaxStarSystem = new ParallaxStarSystem(
      this.cfg.parallax,
      this.cfg.stars,
      this.Q
    );
    this.nebulaSystem = new NebulaSystem(this.cfg.nebula);
    this.constellationSystem = new ConstellationSystem(this.cfg.constellations);
    this.MoonSystem = new MoonSystem(
      this.cfg.Moon,
      this.cfg.background?.gradientStops || [
        { position: 0, color: "#0c0c1e" },
        { position: 0.3, color: "#1a1a2e" },
        { position: 0.7, color: "#16213e" },
        { position: 1, color: "#0f3460" },
      ]
    );
    this.spaceshipSystem = new SpaceshipSystem(this.cfg.spaceship);
    this.cometSystem = new CometSystem(this.cfg.comet, this.cfg.stars);
  }

  public setAccessibility(s: AccessibilitySettings) {
    this.a11y = s;
    // Accessibility settings are passed to systems during update/draw calls
  }

  /* CLEANUP */
  public cleanup() {
    this.isInitialized = false;
    this.parallaxStarSystem.cleanup();
    this.nebulaSystem.cleanup();
    this.constellationSystem.cleanup();
    this.MoonSystem.cleanup();
    this.spaceshipSystem.cleanup();
    this.cometSystem.cleanup();
  }
}
