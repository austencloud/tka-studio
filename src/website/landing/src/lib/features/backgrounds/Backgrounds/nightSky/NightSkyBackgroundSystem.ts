// src/lib/components/Backgrounds/nightSky/NightSkyBackgroundSystem.ts
import type {
  BackgroundSystem,
  Dimensions,
  QualityLevel,
  Star,
  CelestialBody,
  Spaceship,
  ShootingStarState,
  EasterEggState,
  AccessibilitySettings,
} from "../types/types.js";
import { drawBackgroundGradient } from "../snowfall/utils/backgroundUtils.js";
import { getOptimizedConfig } from "../config/index.js";
import { createShootingStarSystem } from "../systems/ShootingStarSystem.js";
import { NightSkyConfig } from "../config/nightSky.js";
import { browser } from "$app/environment";

type ParallaxLayer = { stars: Star[]; driftX: number; driftY: number };

export class NightSkyBackgroundSystem implements BackgroundSystem {
  // core state -------------------------------------------------------------
  private quality: QualityLevel = "medium";
  private layers: Record<"far" | "mid" | "near", ParallaxLayer> = {} as any;
  private nebulae: {
    x: number;
    y: number;
    baseR: number;
    phase: number;
    color: string;
  }[] = [];
  private constellationLines: {
    a: Star;
    b: Star;
    opacity: number;
    dir: number;
  }[] = [];
  private celestialBody: CelestialBody | null = null; // This will be our moon
  private shootingStarSystem = createShootingStarSystem();
  private shootingStarState: ShootingStarState;
  private spaceshipState: EasterEggState<Spaceship>;
  private cometState: EasterEggState<Star>; // treat comet head like Star

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
    this.spaceshipState = {
      element: null,
      timer: 0,
      interval: this.randInt(15000, 30000),
    };
    this.cometState = {
      element: null,
      timer: 0,
      interval: this.cfg.comet.interval,
    };
  }

  // ------------------------------------------------------------------------
  /* INITIALISE */
  public async initialize(dim: Dimensions, q: QualityLevel) {
    this.setQuality(q); // Sets this.cfg and this.Q
    this.initParallax(dim);
    this.initNebulae(dim);
    this.celestialBody = await this.initBody(dim); // Initialize the moon (celestialBody)
  }

  /* UPDATE */
  public update(dim: Dimensions) {
    this.updateParallax(dim);
    this.updateNebulae();
    this.updateConstellations();
    this.updateCelestialBody(dim); // Update moon's position
    if (this.Q.enableShootingStars)
      this.shootingStarState = this.shootingStarSystem.update(
        this.shootingStarState,
        dim
      );
    this.updateSpaceship(dim);
    this.updateComet(dim);
  }

  /* DRAW */
  public draw(ctx: CanvasRenderingContext2D, dim: Dimensions) {
    const gradientStops = this.cfg.background?.gradientStops || [
      { position: 0, color: "#0A0E2C" },
      { position: 1, color: "#4A5490" },
    ];
    drawBackgroundGradient(ctx, dim, gradientStops);

    this.drawNebulae(ctx);
    this.drawParallax(ctx);
    this.drawConstellations(ctx);
    this.drawCelestialBody(ctx); // Draw the moon with phase
    if (this.Q.enableShootingStars)
      this.shootingStarSystem.draw(this.shootingStarState, ctx);
    this.drawSpaceship(ctx);
    this.drawComet(ctx);
  }

  /* QUALITY / A11Y */
  public setQuality(q: QualityLevel) {
    if (this.quality === q) return;
    this.quality = q;
    // Re-fetch optimized config when quality changes
    const optimized = getOptimizedConfig(q);
    this.cfg = optimized.config.nightSky as typeof NightSkyConfig;
    this.Q = optimized.qualitySettings;
  }
  public setAccessibility(s: AccessibilitySettings) {
    this.a11y = s;
    // Potentially re-initialize or update elements if accessibility affects them significantly
  }

  /* CLEANUP */
  public cleanup() {
    this.layers = {} as any;
    this.nebulae = [];
    this.constellationLines = [];
    this.celestialBody = null;
  }

  /* RESIZE HANDLING */
  public handleResize(oldDim: Dimensions, newDim: Dimensions): void {
    // Calculate the size change to determine if we need full reinitialization
    const sizeChangeX = Math.abs(newDim.width - oldDim.width) / oldDim.width;
    const sizeChangeY = Math.abs(newDim.height - oldDim.height) / oldDim.height;
    const significantChange = sizeChangeX > 0.2 || sizeChangeY > 0.2; // 20% change threshold

    if (significantChange) {
      // For significant size changes, reinitialize to ensure proper distribution
      this.reinitializeForNewDimensions(newDim);
    } else {
      // For small changes, just update positions smoothly
      this.smoothResizeElements(oldDim, newDim);
    }
  }

  private reinitializeForNewDimensions(newDim: Dimensions): void {
    // Store current celestial body phase if it exists
    let moonPhase = null;
    if (this.celestialBody?.illumination) {
      moonPhase = {
        fraction: this.celestialBody.illumination.fraction,
        phaseValue: this.celestialBody.illumination.phaseValue,
        angle: this.celestialBody.illumination.angle,
      };
    }

    // Reinitialize all layers with proper distribution for new dimensions
    this.initParallax(newDim);
    this.initNebulae(newDim);

    // Reinitialize celestial body with preserved phase
    this.initBody(newDim).then((body) => {
      if (body && moonPhase) {
        body.illumination = moonPhase;
      }
      this.celestialBody = body;
    });

    // Reset dynamic elements
    this.spaceshipState = {
      element: null,
      timer: 0,
      interval: this.randInt(15000, 30000),
    };
    this.cometState = {
      element: null,
      timer: 0,
      interval: this.cfg.comet.interval,
    };
  }

  private smoothResizeElements(oldDim: Dimensions, newDim: Dimensions): void {
    // Calculate scaling factors for smooth transitions
    const scaleX = newDim.width / oldDim.width;
    const scaleY = newDim.height / oldDim.height;
    const uniformScale = Math.min(scaleX, scaleY);

    // Smoothly resize parallax layers
    Object.values(this.layers).forEach((layer) => {
      layer.stars.forEach((star) => {
        // Scale positions proportionally
        star.x = star.x * scaleX;
        star.y = star.y * scaleY;
        // Keep star size relative to screen size
        if (star.radius) {
          star.radius = star.radius * uniformScale;
        }
      });
    });

    // Resize nebulae proportionally
    this.nebulae.forEach((nebula) => {
      nebula.x = nebula.x * scaleX;
      nebula.y = nebula.y * scaleY;
      nebula.baseR = nebula.baseR * uniformScale;
    });

    // Update celestial body (moon) position and size
    if (this.celestialBody) {
      this.celestialBody.x = this.celestialBody.x * scaleX;
      this.celestialBody.y = this.celestialBody.y * scaleY;
      // Update radius based on new dimensions
      const bodyCfg = this.cfg.celestialBody;
      const devicePixelRatio =
        (typeof window !== "undefined" && window.devicePixelRatio) || 1;
      const baseSize = Math.min(newDim.width, newDim.height);
      this.celestialBody.radius =
        (Math.min(baseSize * bodyCfg.radiusPercent, bodyCfg.maxRadiusPx) /
          devicePixelRatio) *
        devicePixelRatio;
    }

    // Ensure background integrity after resize
    this.ensureBackgroundIntegrity(newDim);
  }

  // Add property to track last dimensions
  private lastDimensions: Dimensions | null = null;

  // ============ internal helpers =========================================
  // ---- parallax stars ----
  private initParallax(dim: Dimensions) {
    const mkLayer = (key: "far" | "mid" | "near"): ParallaxLayer => {
      const pCfg = this.cfg.parallax[key];
      const density = pCfg.density * this.Q.densityMultiplier;
      const count = Math.floor(dim.width * dim.height * density);
      const stars: Star[] = Array.from({ length: count }).map(() =>
        this.makeStar(dim)
      );
      return {
        stars,
        driftX: pCfg.drift * dim.width,
        driftY: pCfg.drift * dim.height,
      };
    };
    this.layers = {
      far: mkLayer("far"),
      mid: mkLayer("mid"),
      near: mkLayer("near"),
    };
  }

  private updateParallax(dim: Dimensions) {
    if (!this.layers || Object.keys(this.layers).length === 0) {
      this.initParallax(dim); // Initialize if not already
      return;
    }
    (["far", "mid", "near"] as Array<keyof typeof this.layers>).forEach(
      (key) => {
        const L = this.layers[key];
        if (L && L.stars && Array.isArray(L.stars)) {
          L.stars.forEach((s: Star) => {
            s.x =
              (s.x +
                L.driftX * (this.a11y.reducedMotion ? 0.3 : 1) +
                dim.width) %
              dim.width;
            s.y =
              (s.y +
                L.driftY * (this.a11y.reducedMotion ? 0.3 : 1) +
                dim.height) %
              dim.height;
            if (s.isTwinkling) {
              s.currentOpacity =
                s.baseOpacity *
                (0.7 +
                  0.3 *
                    Math.sin(
                      (s.twinklePhase +=
                        s.twinkleSpeed * (this.a11y.reducedMotion ? 0.3 : 1))
                    ));
            }
          });
        }
      }
    );
  }
  private drawParallax(ctx: CanvasRenderingContext2D) {
    if (!this.layers || Object.keys(this.layers).length === 0) return;

    (["far", "mid", "near"] as Array<keyof typeof this.layers>).forEach(
      (key) => {
        const L = this.layers[key];
        if (L && L.stars && Array.isArray(L.stars)) {
          const alphaMult = key === "far" ? 0.5 : key === "mid" ? 0.8 : 1;
          L.stars.forEach((star: Star) => {
            ctx.globalAlpha =
              star.currentOpacity *
              alphaMult *
              (this.a11y.reducedMotion ? 0.7 : 1);
            ctx.fillStyle = star.color;
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
            ctx.fill();
          });
        }
      }
    );
    ctx.globalAlpha = 1;
  }

  // ---- nebulae ----
  private initNebulae(dim: Dimensions) {
    if (!this.cfg.nebula.enabledOnQuality.includes(this.quality)) {
      this.nebulae = [];
      return;
    }
    this.nebulae = Array.from({ length: this.cfg.nebula.count }).map(() => {
      const r = this.randFloat(
        this.cfg.nebula.minRadius,
        this.cfg.nebula.maxRadius
      );
      return {
        x: Math.random() * dim.width,
        y: Math.random() * dim.height * 0.7, // Keep them mostly in upper part
        baseR: r,
        phase: Math.random() * Math.PI * 2,
        color: this.randItem(this.cfg.nebula.colors),
      };
    });
  }
  private updateNebulae() {
    if (!this.nebulae.length) return;
    const speedRange = this.cfg.nebula.pulseSpeed;
    const effectiveSpeed = this.a11y.reducedMotion ? 0.3 : 1;
    this.nebulae.forEach(
      (n) =>
        (n.phase +=
          this.randFloat(speedRange.min, speedRange.max) * effectiveSpeed)
    );
  }
  private drawNebulae(ctx: CanvasRenderingContext2D) {
    if (!this.nebulae.length) return;
    ctx.globalAlpha = this.a11y.reducedMotion ? 0.5 : 1;
    this.nebulae.forEach((n) => {
      const r = n.baseR * (0.9 + 0.1 * Math.sin(n.phase));
      const g = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, r);
      g.addColorStop(0, n.color);
      g.addColorStop(1, "transparent");
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.globalAlpha = 1;
  }

  // ---- constellations ----
  private updateConstellations() {
    if (!this.cfg.constellations.enabledOnQuality.includes(this.quality)) {
      this.constellationLines = [];
      return;
    }
    if (
      !this.layers.near ||
      !this.layers.near.stars ||
      this.layers.near.stars.length === 0
    )
      return;

    if (
      this.constellationLines.length === 0 &&
      this.layers.near.stars.length > 1
    ) {
      const nearStars = this.layers.near.stars;
      const numLines = Math.min(
        this.cfg.constellations.maxLines,
        Math.floor(nearStars.length / 2)
      );
      for (let i = 0; i < numLines; i++) {
        const aIndex = this.randInt(0, nearStars.length - 1);
        let bIndex = this.randInt(0, nearStars.length - 1);
        while (bIndex === aIndex) {
          // Ensure different stars
          bIndex = this.randInt(0, nearStars.length - 1);
        }
        this.constellationLines.push({
          a: nearStars[aIndex],
          b: nearStars[bIndex],
          opacity: Math.random() * this.cfg.constellations.opacity,
          dir: Math.random() > 0.5 ? 1 : -1,
        });
      }
    }
    const effectiveSpeed = this.a11y.reducedMotion ? 0.3 : 1;
    this.constellationLines.forEach((l) => {
      l.opacity +=
        l.dir * this.cfg.constellations.twinkleSpeed * effectiveSpeed;
      if (l.opacity > this.cfg.constellations.opacity || l.opacity < 0) {
        l.dir *= -1;
        l.opacity = Math.max(
          0,
          Math.min(this.cfg.constellations.opacity, l.opacity)
        );
      }
    });
  }
  private drawConstellations(ctx: CanvasRenderingContext2D) {
    if (!this.constellationLines.length) return;
    ctx.lineWidth = 0.7;
    const baseColor = this.a11y.highContrast ? "#FFFFFF" : "#89A7FF";
    this.constellationLines.forEach((l) => {
      if (!l.a || !l.b) return; // Guard against undefined stars if layers were reset
      ctx.globalAlpha = l.opacity * (this.a11y.reducedMotion ? 0.5 : 1);
      ctx.strokeStyle = baseColor;
      ctx.beginPath();
      ctx.moveTo(l.a.x, l.a.y);
      ctx.lineTo(l.b.x, l.b.y);
      ctx.stroke();
    });
    ctx.globalAlpha = 1;
  }

  // ---- celestial body (MOON) ----
  private async initBody(dim: Dimensions): Promise<CelestialBody | null> {
    const bodyCfg = this.cfg.celestialBody;
    if (!bodyCfg.enabledOnQuality.includes(this.quality)) return null;

    // Ensure perfectly round moon by using device pixel ratio
    const devicePixelRatio =
      (typeof window !== "undefined" && window.devicePixelRatio) || 1;
    const baseSize = Math.min(dim.width, dim.height);
    const radius =
      (Math.min(baseSize * bodyCfg.radiusPercent, bodyCfg.maxRadiusPx) /
        devicePixelRatio) *
      devicePixelRatio;

    let moonIlluminationData = {
      fraction: 0.5,
      phase: 0.5,
      angle: 0,
    };

    if (browser) {
      try {
        const SunCalc = await import("suncalc");
        moonIlluminationData = SunCalc.default.getMoonIllumination(new Date());
      } catch (error) {
        console.warn("Failed to load moon phase data, using default:", error);
      }
    }

    return {
      x: dim.width * bodyCfg.position.x,
      y: dim.height * bodyCfg.position.y,
      radius: radius,
      color: this.a11y.highContrast ? "#FFFFFF" : bodyCfg.color, // Use config color for illuminated part
      driftX: (Math.random() - 0.5) * bodyCfg.driftSpeed * dim.width,
      driftY: (Math.random() - 0.5) * bodyCfg.driftSpeed * dim.height,
      illumination: {
        fraction: moonIlluminationData.fraction, // How much is lit (0 to 1)
        phaseValue: moonIlluminationData.phase, // Phase cycle (0 new, 0.5 full, 1 new)
        angle: moonIlluminationData.angle, // Angle of bright limb
      },
    };
  }

  private updateCelestialBody(dim: Dimensions) {
    if (!this.celestialBody) return;
    const b = this.celestialBody;

    // Update radius on resize to maintain perfect roundness
    const bodyCfg = this.cfg.celestialBody;
    const devicePixelRatio =
      (typeof window !== "undefined" && window.devicePixelRatio) || 1;
    const baseSize = Math.min(dim.width, dim.height);
    b.radius =
      (Math.min(baseSize * bodyCfg.radiusPercent, bodyCfg.maxRadiusPx) /
        devicePixelRatio) *
      devicePixelRatio;

    const effectiveDriftSpeed = this.a11y.reducedMotion ? 0.1 : 1;
    b.x = (b.x + (b.driftX || 0) * effectiveDriftSpeed + dim.width) % dim.width;
    b.y =
      (b.y + (b.driftY || 0) * effectiveDriftSpeed + dim.height * 1.5) %
      (dim.height * 1.5); // Allow to go off screen a bit at bottom
    if (b.y > dim.height + b.radius) {
      // Reset if goes too far below
      b.y = -b.radius;
      b.x = Math.random() * dim.width;
    }
  }
  private drawCelestialBody(ctx: CanvasRenderingContext2D) {
    const b = this.celestialBody;
    if (!b || !b.illumination) return;

    // Ensure moon is drawn at exact pixel boundaries for perfect roundness
    const x = Math.round(b.x);
    const y = Math.round(b.y);
    const radius = Math.round(b.radius);
    const { color } = b;
    const { fraction, phaseValue } = b.illumination;
    const R = radius;

    ctx.save();

    // 1. Draw the base illuminated moon disk (color is the bright part of the moon)
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, R, 0, 2 * Math.PI);
    ctx.fill();

    // Apply shadow for phases other than full moon
    if (fraction < 0.99) {
      // If not almost full moon
      // Get background gradient colors
      const gradientStops = this.cfg.background?.gradientStops || [
        { position: 0, color: "#0A0E2C" },
        { position: 1, color: "#4A5490" },
      ];

      // Calculate relative position of the moon in the sky to determine which gradient color to use
      const relativeYPosition = y / ctx.canvas.height;

      // Find the appropriate color from the gradient based on moon's position
      let shadowBaseColor = "#0A0E2C"; // Default dark sky color

      // Simple interpolation between gradient stops based on moon's vertical position
      if (gradientStops.length >= 2) {
        // Find the two gradient stops that surround the moon's position
        let lowerStop = gradientStops[0];
        let upperStop = gradientStops[gradientStops.length - 1];

        for (let i = 0; i < gradientStops.length - 1; i++) {
          if (
            gradientStops[i].position <= relativeYPosition &&
            gradientStops[i + 1].position >= relativeYPosition
          ) {
            lowerStop = gradientStops[i];
            upperStop = gradientStops[i + 1];
            break;
          }
        }

        // Use the color closer to the moon's position for simplicity
        shadowBaseColor =
          Math.abs(relativeYPosition - lowerStop.position) <
          Math.abs(relativeYPosition - upperStop.position)
            ? lowerStop.color
            : upperStop.color;
      } else if (gradientStops.length === 1) {
        shadowBaseColor = gradientStops[0].color;
      }

      // Determine shadow color - use black for high contrast or calculated color
      const shadowColor = this.a11y.highContrast ? "#000000" : shadowBaseColor;

      ctx.fillStyle = shadowColor;

      const phaseAngleForShadow = (phaseValue - 0.5) * 2 * Math.PI;
      const shadowDiscCenterX = x - R * Math.cos(phaseAngleForShadow);

      // Create a clipping path that restricts drawing to only the moon's circle
      ctx.save();
      ctx.beginPath();
      ctx.arc(x, y, R, 0, 2 * Math.PI);
      ctx.clip();

      // Draw the shadow circle - now it will only be visible where it overlaps the moon
      ctx.beginPath();
      ctx.arc(shadowDiscCenterX, y, R, 0, 2 * Math.PI);
      ctx.fill();

      ctx.restore(); // Restore context to remove the clipping
    }

    // Optional: Add a very faint outline for the new moon if it's not high contrast mode
    // and it's nearly new but not full
    if (fraction < 0.03 && !this.a11y.highContrast && fraction < 0.98) {
      ctx.strokeStyle = "rgba(100, 100, 120, 0.3)"; // A very subtle grey
      ctx.lineWidth = Math.max(0.5, R * 0.02); // Make outline proportional but not too thick
      ctx.beginPath();
      ctx.arc(x, y, R, 0, 2 * Math.PI);
      ctx.stroke();
    }

    ctx.restore();
  }

  // ---- spaceship ----
  private updateSpaceship(dim: Dimensions) {
    if (!this.cfg.spaceship.enabledOnQuality.includes(this.quality)) {
      this.spaceshipState.element = null;
      return;
    }
    const sCfg = this.cfg.spaceship;
    const effectiveSpeed = this.a11y.reducedMotion ? 0.2 : 1;

    if (!this.spaceshipState.element) {
      this.spaceshipState.timer++;
      if (this.spaceshipState.timer >= this.spaceshipState.interval) {
        const dir = Math.random() > 0.5 ? 1 : -1;
        this.spaceshipState.element = {
          x: dir > 0 ? -sCfg.size : dim.width + sCfg.size,
          y: Math.random() * dim.height * 0.4 + dim.height * 0.1, // Upper part of sky
          width: sCfg.size,
          height: sCfg.size / 2,
          speed: sCfg.speedPercent * dim.width * effectiveSpeed,
          active: true,
          direction: dir,
          opacity: 1,
        };
        this.spaceshipState.timer = 0;
        this.spaceshipState.interval = this.randInt(
          sCfg.interval / 2,
          sCfg.interval * 1.5
        );
      }
    } else {
      const ship = this.spaceshipState.element;
      ship.x += ship.speed * ship.direction;
      if (
        (ship.direction > 0 && ship.x > dim.width + ship.width) ||
        (ship.direction < 0 && ship.x < -ship.width)
      ) {
        this.spaceshipState.element = null;
      }
    }
  }
  private drawSpaceship(ctx: CanvasRenderingContext2D) {
    const ship = this.spaceshipState.element;
    if (!ship) return;

    ctx.fillStyle = this.a11y.highContrast
      ? "#FFFFFF"
      : this.cfg.spaceship.color;
    ctx.globalAlpha = ship.opacity * (this.a11y.reducedMotion ? 0.6 : 1);
    ctx.beginPath();
    // Simple triangle shape for spaceship
    if (ship.direction > 0) {
      // Moving right
      ctx.moveTo(ship.x, ship.y);
      ctx.lineTo(ship.x - ship.width, ship.y - ship.height / 2);
      ctx.lineTo(ship.x - ship.width, ship.y + ship.height / 2);
    } else {
      // Moving left
      ctx.moveTo(ship.x, ship.y);
      ctx.lineTo(ship.x + ship.width, ship.y - ship.height / 2);
      ctx.lineTo(ship.x + ship.width, ship.y + ship.height / 2);
    }
    ctx.closePath();
    ctx.fill();

    // Thruster
    ctx.fillStyle = this.a11y.highContrast
      ? "#FFFF00"
      : this.cfg.spaceship.thrusterColor;
    const thrusterSize = ship.height / 1.5;
    const thrusterX =
      ship.direction > 0
        ? ship.x - ship.width - thrusterSize / 2
        : ship.x + ship.width + thrusterSize / 2;
    ctx.beginPath();
    ctx.arc(
      thrusterX,
      ship.y,
      thrusterSize * (0.5 + Math.random() * 0.5),
      0,
      Math.PI * 2
    );
    ctx.fill();

    ctx.globalAlpha = 1;
  }

  // ---- comet ----
  private updateComet(dim: Dimensions) {
    if (!this.cfg.comet.enabledOnQuality.includes(this.quality)) {
      this.cometState.element = null;
      return;
    }
    const cCfg = this.cfg.comet;
    const effectiveSpeed = this.a11y.reducedMotion ? 0.2 : 1;

    if (!this.cometState.element) {
      this.cometState.timer++;
      if (this.cometState.timer >= this.cometState.interval) {
        const dir = Math.random() > 0.5 ? 1 : -1; // Direction: 1 for right-to-left, -1 for left-to-right
        this.cometState.element = {
          x: dir > 0 ? dim.width + cCfg.radius * 5 : -cCfg.radius * 5, // Start off-screen
          y: Math.random() * dim.height * 0.5 + dim.height * 0.05, // Upper half
          radius: cCfg.radius,
          baseOpacity: 1,
          currentOpacity: 1,
          twinkleSpeed: 0,
          twinklePhase: 0,
          isTwinkling: false,
          color: this.a11y.highContrast ? "#FFFF00" : cCfg.color,
          // Store direction for comet movement
          _direction: dir,
          _speed: cCfg.speed * dim.width * effectiveSpeed,
        } as Star & { _direction: number; _speed: number }; // Augment Star type for comet
        this.cometState.timer = 0;
        this.cometState.interval = cCfg.interval * (0.5 + Math.random()); // Randomize next appearance
      }
    } else {
      const comet = this.cometState.element as Star & {
        _direction: number;
        _speed: number;
      };
      comet.x -= comet._direction * comet._speed; // Move based on stored direction

      // Fade out as it moves (optional, could be based on time or position)
      // comet.currentOpacity -= 0.001;

      // Check if off-screen
      if (
        (comet._direction > 0 && comet.x < -cCfg.tailLength) ||
        (comet._direction < 0 && comet.x > dim.width + cCfg.tailLength) ||
        comet.currentOpacity <= 0
      ) {
        this.cometState.element = null;
      }
    }
  }
  private drawComet(ctx: CanvasRenderingContext2D) {
    const comet = this.cometState.element as Star & { _direction?: number }; // Cast for augmented properties
    if (!comet || !comet._direction) return;

    const tailLength = this.cfg.comet.tailLength;
    const headX = comet.x;
    const headY = comet.y;

    ctx.globalAlpha =
      comet.currentOpacity * (this.a11y.reducedMotion ? 0.6 : 1);

    // Tail
    const tailEndX = headX + comet._direction * tailLength; // Tail goes opposite to direction of movement
    const tailEndY = headY; // Simple horizontal tail for now

    const gradient = ctx.createLinearGradient(headX, headY, tailEndX, tailEndY);
    gradient.addColorStop(0, comet.color); // Bright at head
    gradient.addColorStop(1, "transparent"); // Fades out

    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.moveTo(headX, headY - comet.radius / 2);
    ctx.lineTo(tailEndX, tailEndY - comet.radius / 8); // Narrower end
    ctx.lineTo(tailEndX, tailEndY + comet.radius / 8);
    ctx.lineTo(headX, headY + comet.radius / 2);
    ctx.closePath();
    ctx.fill();

    // Head
    ctx.fillStyle = comet.color;
    ctx.beginPath();
    ctx.arc(headX, headY, comet.radius, 0, Math.PI * 2);
    ctx.fill();

    ctx.globalAlpha = 1;
  }

  // ============ utils =====================================================
  private makeStar(dim: Dimensions): Star {
    const sCfg = this.cfg.stars;
    const r =
      this.randFloat(sCfg.minSize, sCfg.maxSize) *
      (this.a11y.visibleParticleSize > 2 ? 1.5 : 1);
    const tw = Math.random() < sCfg.twinkleChance;
    return {
      x: Math.random() * dim.width,
      y: Math.random() * dim.height,
      radius: r,
      baseOpacity: this.randFloat(sCfg.baseOpacityMin, sCfg.baseOpacityMax),
      currentOpacity: 1, // Will be set in updateParallax
      twinkleSpeed: tw
        ? this.randFloat(sCfg.minTwinkleSpeed, sCfg.maxTwinkleSpeed)
        : 0,
      twinklePhase: Math.random() * Math.PI * 2,
      isTwinkling: tw,
      color: this.a11y.highContrast ? "#FFFFFF" : this.randItem(sCfg.colors),
    };
  }
  private randFloat(m: number, M: number) {
    return Math.random() * (M - m) + m;
  }
  private randInt(m: number, M: number) {
    return Math.floor(Math.random() * (M - m + 1)) + m;
  }
  private randItem<T>(arr: T[]): T {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  // Additional safety method to ensure background integrity after resize
  private ensureBackgroundIntegrity(dim: Dimensions): void {
    // Verify all parallax layers have valid stars
    Object.values(this.layers).forEach((layer) => {
      layer.stars = layer.stars.filter(
        (star) =>
          !isNaN(star.x) &&
          !isNaN(star.y) &&
          star.x >= -star.radius &&
          star.x <= dim.width + star.radius &&
          star.y >= -star.radius &&
          star.y <= dim.height + star.radius
      );
    });

    // Verify nebulae are within reasonable bounds
    this.nebulae = this.nebulae.filter(
      (nebula) =>
        !isNaN(nebula.x) &&
        !isNaN(nebula.y) &&
        !isNaN(nebula.baseR) &&
        nebula.x >= -nebula.baseR &&
        nebula.x <= dim.width + nebula.baseR &&
        nebula.y >= -nebula.baseR &&
        nebula.y <= dim.height + nebula.baseR
    );

    // Verify celestial body is valid
    if (this.celestialBody) {
      if (
        isNaN(this.celestialBody.x) ||
        isNaN(this.celestialBody.y) ||
        isNaN(this.celestialBody.radius)
      ) {
        // Reinitialize if corrupted
        this.initBody(dim);
      }
    }
  }
}
