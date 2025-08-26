// src/lib/services/implementations/background/systems/NightSkyBackgroundSystem.ts
import { getOptimizedConfig } from "$lib/domain/background/configs/config";
import { NightSkyConfig } from "$lib/domain/background/configs/nightSky";
import { drawBackgroundGradient } from "$lib/utils/background/backgroundUtils";
import { createShootingStarSystem } from "./core/ShootingStarSystem";

// Import our new modular systems
import { ParallaxStarSystem } from "../systems/nightSky/ParallaxStarSystem";
import { NebulaSystem } from "../systems/nightSky/NebulaSystem";
import { ConstellationSystem } from "../systems/nightSky/ConstellationSystem";
import { CelestialBodySystem } from "../systems/nightSky/CelestialBodySystem";
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

  // Modular systems
  private parallaxStarSystem: ParallaxStarSystem;
  private nebulaSystem: NebulaSystem;
  private constellationSystem: ConstellationSystem;
  private celestialBodySystem: CelestialBodySystem;
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

    this.celestialBodySystem = new CelestialBodySystem(
      this.cfg.celestialBody,
      this.cfg.background?.gradientStops || [
        { position: 0, color: "#0A0E2C" },
        { position: 1, color: "#4A5490" },
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
    this.celestialBodySystem.initialize(dim, this.quality, this.a11y);
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
    this.celestialBodySystem.update(dim, this.a11y);

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
    const gradientStops = this.cfg.background?.gradientStops || [
      { position: 0, color: "#0A0E2C" },
      { position: 1, color: "#4A5490" },
    ];
    drawBackgroundGradient(ctx, dim, gradientStops);

    this.nebulaSystem.draw(ctx, this.a11y);
    this.parallaxStarSystem.draw(ctx, this.a11y);
    this.constellationSystem.draw(ctx, this.a11y);
    this.celestialBodySystem.draw(ctx, this.a11y);

    if (this.Q.enableShootingStars)
      this.shootingStarSystem.draw(this.shootingStarState, ctx);

    this.spaceshipSystem.draw(ctx, this.a11y);
    this.cometSystem.draw(ctx, this.a11y);
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
    this.celestialBodySystem = new CelestialBodySystem(
      this.cfg.celestialBody,
      this.cfg.background?.gradientStops || [
        { position: 0, color: "#0A0E2C" },
        { position: 1, color: "#4A5490" },
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
    this.parallaxStarSystem.cleanup();
    this.nebulaSystem.cleanup();
    this.constellationSystem.cleanup();
    this.celestialBodySystem.cleanup();
    this.spaceshipSystem.cleanup();
    this.cometSystem.cleanup();
  }
}
