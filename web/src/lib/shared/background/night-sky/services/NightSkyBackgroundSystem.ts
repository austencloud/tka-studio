import { container } from "$shared/inversify";
import { BackgroundTypes } from "$shared/inversify/types";
import {
  createShootingStarSystem,
  type AccessibilitySettings,
  type Dimensions,
  type IBackgroundConfigurationService,
  type IBackgroundRenderingService,
  type IBackgroundSystem,
  type QualityLevel,
  type QualitySettings,
} from "../../shared";
import { NightSkyConfig } from "../domain/constants/nightSky";
import { CometSystem } from "./CometSystem";
import { ConstellationSystem } from "./ConstellationSystem";
import { MoonSystem } from "./MoonSystem";
import { NebulaSystem } from "./NebulaSystem";
import { ParallaxStarSystem } from "./ParallaxStarSystem";
import { SpaceshipSystem } from "./SpaceshipSystem";

// TODO: Fix this - ShootingStarState should be imported from proper location
interface ShootingStarState {
  star: {
    x: number;
    y: number;
    dx: number;
    dy: number;
    size: number;
    speed: number;
    tail: Array<{ x: number; y: number; size: number; color: string }>;
    prevX: number;
    prevY: number;
    tailLength: number;
    opacity: number;
    offScreen: boolean;
    color: string;
    twinkle: boolean;
  } | null;
  timer: number;
  interval: number;
}

export class NightSkyBackgroundSystem implements IBackgroundSystem {
  // core state -------------------------------------------------------------
  private quality: QualityLevel = "medium";
  private isInitialized: boolean = false;

  // Services
  private renderingService: IBackgroundRenderingService;
  private configurationService: IBackgroundConfigurationService;

  // Modular systems
  private parallaxStarSystem: ParallaxStarSystem;
  private nebulaSystem: NebulaSystem;
  private constellationSystem: ConstellationSystem;
  private moonSystem: MoonSystem;
  private spaceshipSystem: SpaceshipSystem;
  private cometSystem: CometSystem;
  private shootingStarSystem = createShootingStarSystem();
  private shootingStarState: ShootingStarState;

  // config handles ---------------------------------------------------------
  private cfg: typeof NightSkyConfig;
  private Q: QualitySettings;
  private a11y: AccessibilitySettings = {
    reducedMotion: false,
    highContrast: false,
    visibleParticleSize: 2,
  };

  constructor() {
    // Inject services
    this.renderingService = container.get<IBackgroundRenderingService>(
      BackgroundTypes.IBackgroundRenderingService
    );
    this.configurationService = container.get<IBackgroundConfigurationService>(
      BackgroundTypes.IBackgroundConfigurationService
    );

    // Initialize configuration after services are injected
    const optimized = this.getOptimizedConfig(this.quality);
    this.cfg = optimized.config.nightSky as typeof NightSkyConfig;
    this.Q = optimized.qualitySettings;

    this.shootingStarState = this.shootingStarSystem.initialState;

    // Initialize all modular systems
    this.parallaxStarSystem = new ParallaxStarSystem(
      this.cfg.parallax,
      this.cfg.stars,
      this.Q
    );

    this.nebulaSystem = new NebulaSystem(this.cfg.nebula);

    this.constellationSystem = new ConstellationSystem(this.cfg.constellations);

    this.moonSystem = new MoonSystem(
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
    this.moonSystem.initialize(dim, this.quality, this.a11y);

    this.isInitialized = true;
  }

  /* UPDATE */
  public update(dim: Dimensions) {
    // TEMPORARILY DISABLED ALL SYSTEMS FOR TESTING - finding diagonal beam source
    // this.parallaxStarSystem.update(dim, this.a11y);
    // this.nebulaSystem.update(this.a11y);
    // this.constellationSystem.update(
    //   this.parallaxStarSystem.getNearStars(),
    //   this.quality,
    //   this.a11y
    // );
    // this.moonSystem.update(dim, this.a11y);

    // TEMPORARILY DISABLED FOR TESTING - shooting stars suspected as diagonal beam source
    // if (this.Q.enableShootingStars)
    //   this.shootingStarState = this.shootingStarSystem.update(
    //     this.shootingStarState,
    //     dim
    //   );

    // TEMPORARILY DISABLED FOR TESTING - spaceship system suspected as diagonal beam source
    // this.spaceshipSystem.update(dim, this.a11y, this.quality);
    // TEMPORARILY DISABLED FOR TESTING - comet system suspected as diagonal beam source
    // this.cometSystem.update(dim, this.a11y, this.quality);
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
    this.renderingService.drawGradient(ctx, dim, gradientStops);

    // Only draw other elements if properly initialized
    if (this.isInitialized) {
      // TEMPORARILY DISABLED ALL SYSTEMS FOR TESTING - finding diagonal beam source
      // this.nebulaSystem.draw(ctx, this.a11y);
      // this.parallaxStarSystem.draw(ctx, this.a11y);
      // this.constellationSystem.draw(ctx, this.a11y);
      // this.moonSystem.draw(ctx, this.a11y);

      // TEMPORARILY DISABLED FOR TESTING - shooting stars suspected as diagonal beam source
      // if (this.Q.enableShootingStars)
      //   this.shootingStarSystem.draw(this.shootingStarState, ctx);

      // TEMPORARILY DISABLED FOR TESTING - spaceship system suspected as diagonal beam source
      // this.spaceshipSystem.draw(ctx, this.a11y);
      // TEMPORARILY DISABLED FOR TESTING - comet system suspected as diagonal beam source  
      // this.cometSystem.draw(ctx, this.a11y);
    }
  }

  /* QUALITY / A11Y */
  public setQuality(q: QualityLevel) {
    if (this.quality === q) return;
    this.quality = q;
    // Re-fetch optimized config when quality changes
    const optimized = this.getOptimizedConfig(q);
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
    this.moonSystem = new MoonSystem(
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
    this.moonSystem.cleanup();
    this.spaceshipSystem.cleanup();
    this.cometSystem.cleanup();
  }

  // Helper methods
  private getOptimizedConfig(quality: QualityLevel) {
    return this.configurationService.getOptimizedConfig(quality);
  }
}
