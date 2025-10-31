// src/lib/components/backgrounds/systems/nightSky/MoonSystem.ts

// Removed resolve import - calculation service now injected via constructor
import type {
  AccessibilitySettings,
  Dimensions,
  QualityLevel,
} from "../../shared";
import type { Moon } from "../domain";
import type { INightSkyCalculationService } from "./contracts/INightSkyCalculationService";

export interface MoonConfig {
  radiusPercent: number;
  maxRadiusPx: number;
  color: string;
  position: { x: number; y: number };
  driftSpeed: number;
  enabledOnQuality: QualityLevel[];
}

export interface BackgroundGradientStop {
  position: number;
  color: string;
}

export class MoonSystem {
  private Moon: Moon | null = null;
  private config: MoonConfig;
  private gradientStops: BackgroundGradientStop[];
  private lastDimensions: Dimensions | null = null;
  private calculationService: INightSkyCalculationService;

  constructor(
    config: MoonConfig,
    gradientStops: BackgroundGradientStop[],
    calculationService: INightSkyCalculationService
  ) {
    this.config = config;
    this.gradientStops = gradientStops;
    this.calculationService = calculationService;
  }

  initialize(
    dim: Dimensions,
    quality: QualityLevel,
    a11y: AccessibilitySettings
  ): Moon | null {
    if (!this.config.enabledOnQuality.includes(quality)) {
      this.Moon = null;
      return null;
    }

    const baseSize = Math.min(dim.width, dim.height);
    const radius = Math.min(
      baseSize * this.config.radiusPercent,
      this.config.maxRadiusPx
    );

    const moonIlluminationData = this.calculationService.getMoonIllumination(
      new Date()
    );

    this.Moon = {
      x: dim.width * this.config.position.x,
      y: dim.height * this.config.position.y,
      radius: radius,
      color: a11y.highContrast ? "#FFFFFF" : this.config.color,
      driftX: (Math.random() - 0.5) * this.config.driftSpeed * dim.width,
      driftY: (Math.random() - 0.5) * this.config.driftSpeed * dim.height,
      illumination: {
        fraction: moonIlluminationData.fraction,
        phaseValue: moonIlluminationData.phase,
        angle: moonIlluminationData.angle,
      },
    };

    // Set lastDimensions so future updates can detect changes
    this.lastDimensions = dim;

    return this.Moon;
  }

  update(
    dim: Dimensions,
    a11y: AccessibilitySettings,
    frameMultiplier: number = 1.0
  ) {
    if (!this.Moon) return;

    // Handle dimension changes smoothly
    if (
      this.lastDimensions &&
      (dim.width !== this.lastDimensions.width ||
        dim.height !== this.lastDimensions.height)
    ) {
      this.handleResize(this.lastDimensions, dim);
      this.lastDimensions = dim;
      return;
    }

    // Regular animation updates (drift movement)
    const b = this.Moon;
    const effectiveDriftSpeed =
      frameMultiplier * (a11y.reducedMotion ? 0.1 : 1);
    b.x = (b.x + (b.driftX || 0) * effectiveDriftSpeed + dim.width) % dim.width;
    b.y =
      (b.y + (b.driftY || 0) * effectiveDriftSpeed + dim.height * 1.5) %
      (dim.height * 1.5);

    if (b.y > dim.height + b.radius) {
      // Reset if goes too far below
      b.y = -b.radius;
      b.x = Math.random() * dim.width;
    }
  }

  /**
   * Handle canvas resize by scaling the celestial body position proportionally
   */
  private handleResize(oldDim: Dimensions, newDim: Dimensions) {
    if (!this.Moon) return;

    const scaleX = newDim.width / oldDim.width;
    const scaleY = newDim.height / oldDim.height;

    // Scale the celestial body position proportionally
    this.Moon.x = this.Moon.x * scaleX;
    this.Moon.y = this.Moon.y * scaleY;

    // Update drift values for new dimensions
    this.Moon.driftX = (this.Moon.driftX || 0) * scaleX;
    this.Moon.driftY = (this.Moon.driftY || 0) * scaleY;

    // Recalculate radius based on new dimensions
    const baseSize = Math.min(newDim.width, newDim.height);
    this.Moon.radius = Math.min(
      baseSize * this.config.radiusPercent,
      this.config.maxRadiusPx
    );
  }

  draw(ctx: CanvasRenderingContext2D, a11y: AccessibilitySettings) {
    const b = this.Moon;
    if (!b || !b.illumination) return;

    const { x, y, radius, color } = b;
    const { fraction, phaseValue } = b.illumination;
    const R = radius;

    ctx.save();

    // ENHANCEMENT 1: Outer glow/halo for ethereal beauty
    const glowGradient = ctx.createRadialGradient(x, y, R * 0.8, x, y, R * 2.5);
    glowGradient.addColorStop(0, "rgba(245, 245, 220, 0.15)"); // Soft beige glow
    glowGradient.addColorStop(0.4, "rgba(245, 245, 220, 0.08)");
    glowGradient.addColorStop(0.7, "rgba(200, 200, 255, 0.03)"); // Hint of blue at edges
    glowGradient.addColorStop(1, "rgba(200, 200, 255, 0)");

    ctx.fillStyle = glowGradient;
    ctx.beginPath();
    ctx.arc(x, y, R * 2.5, 0, 2 * Math.PI);
    ctx.fill();

    // ENHANCEMENT 2: Textured moon surface with radial gradient
    const moonGradient = ctx.createRadialGradient(
      x - R * 0.3,
      y - R * 0.3,
      R * 0.1, // Light source from upper-left
      x,
      y,
      R
    );
    moonGradient.addColorStop(0, "#fffef0"); // Bright highlight
    moonGradient.addColorStop(0.3, "#f5f5dc"); // Beige
    moonGradient.addColorStop(0.6, "#e8e8d0"); // Slightly darker
    moonGradient.addColorStop(0.85, "#d0d0b8"); // Edge darkening
    moonGradient.addColorStop(1, "#b8b8a0"); // Soft edge

    ctx.fillStyle = moonGradient;
    ctx.beginPath();
    ctx.arc(x, y, R, 0, 2 * Math.PI);
    ctx.fill();

    // ENHANCEMENT 3: Consistent, realistic crater positions (seeded by moon position)
    // Using deterministic positions based on moon's x/y so craters don't jump around
    const craters = [
      { offsetX: 0.3, offsetY: -0.2, size: 0.15 }, // Upper right
      { offsetX: -0.4, offsetY: 0.1, size: 0.12 }, // Left center
      { offsetX: 0.1, offsetY: 0.35, size: 0.18 }, // Lower center
      { offsetX: -0.15, offsetY: -0.3, size: 0.1 }, // Upper left
      { offsetX: 0.45, offsetY: 0.2, size: 0.08 }, // Right
      { offsetX: -0.25, offsetY: 0.4, size: 0.11 }, // Lower left
    ];

    ctx.globalAlpha = 0.08; // More subtle
    craters.forEach((crater) => {
      const craterX = x + crater.offsetX * R;
      const craterY = y + crater.offsetY * R;
      const craterR = R * crater.size;

      const craterGradient = ctx.createRadialGradient(
        craterX,
        craterY,
        0,
        craterX,
        craterY,
        craterR
      );
      craterGradient.addColorStop(0, "rgba(80, 80, 60, 0.6)");
      craterGradient.addColorStop(0.5, "rgba(80, 80, 60, 0.3)");
      craterGradient.addColorStop(1, "rgba(80, 80, 60, 0)");

      ctx.fillStyle = craterGradient;
      ctx.beginPath();
      ctx.arc(craterX, craterY, craterR, 0, 2 * Math.PI);
      ctx.fill();
    });
    ctx.globalAlpha = 1;

    // ENHANCEMENT 4: Add subtle noise/grain texture for organic feel
    ctx.globalAlpha = 0.03;
    for (let i = 0; i < 100; i++) {
      const noiseX = x + (Math.random() - 0.5) * R * 2;
      const noiseY = y + (Math.random() - 0.5) * R * 2;
      const distance = Math.sqrt((noiseX - x) ** 2 + (noiseY - y) ** 2);

      // Only draw noise inside moon circle
      if (distance < R) {
        ctx.fillStyle =
          Math.random() > 0.5
            ? "rgba(255, 255, 255, 0.3)"
            : "rgba(0, 0, 0, 0.3)";
        ctx.fillRect(noiseX, noiseY, 1, 1);
      }
    }
    ctx.globalAlpha = 1;

    // ENHANCEMENT 5: Darker, more dramatic phase shadow
    if (fraction < 0.99) {
      const phaseAngleForShadow = (phaseValue - 0.5) * 2 * Math.PI;
      const shadowDiscCenterX = x - R * Math.cos(phaseAngleForShadow);

      // Create clipping path for moon circle
      ctx.save();
      ctx.beginPath();
      ctx.arc(x, y, R, 0, 2 * Math.PI);
      ctx.clip();

      // Draw darker gradient shadow for better contrast
      const shadowGradient = ctx.createRadialGradient(
        shadowDiscCenterX,
        y,
        0,
        shadowDiscCenterX,
        y,
        R * 1.2
      );
      shadowGradient.addColorStop(0, "rgba(5, 5, 15, 0.95)"); // Very dark center
      shadowGradient.addColorStop(0.4, "rgba(8, 8, 20, 0.85)"); // Dark
      shadowGradient.addColorStop(0.7, "rgba(10, 10, 25, 0.6)"); // Medium dark
      shadowGradient.addColorStop(1, "rgba(15, 15, 30, 0.2)"); // Soft edge

      ctx.fillStyle = shadowGradient;
      ctx.beginPath();
      ctx.arc(shadowDiscCenterX, y, R * 1.2, 0, 2 * Math.PI);
      ctx.fill();

      ctx.restore(); // Remove clipping
    }

    // ENHANCEMENT 6: Subtle edge glow for depth
    ctx.globalAlpha = 0.3;
    ctx.strokeStyle = "rgba(255, 255, 240, 0.4)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(x, y, R, 0, 2 * Math.PI);
    ctx.stroke();
    ctx.globalAlpha = 1;

    ctx.restore();
  }

  getMoon(): Moon | null {
    return this.Moon;
  }

  cleanup() {
    this.Moon = null;
  }
}
