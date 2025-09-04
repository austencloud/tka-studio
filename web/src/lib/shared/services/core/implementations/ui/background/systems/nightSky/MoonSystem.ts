// src/lib/components/backgrounds/systems/nightSky/MoonSystem.ts
import type {
  AccessibilitySettings,
  Dimensions,
  Moon,
  QualityLevel,
} from "$domain";
import { NightSkyUtils } from "./NightSkyUtils";

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

  constructor(config: MoonConfig, gradientStops: BackgroundGradientStop[]) {
    this.config = config;
    this.gradientStops = gradientStops;
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

    const moonIlluminationData = NightSkyUtils.getMoonIllumination(new Date());

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

  update(dim: Dimensions, a11y: AccessibilitySettings) {
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
    const effectiveDriftSpeed = a11y.reducedMotion ? 0.1 : 1;
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

    // 1. Draw the base illuminated moon disk
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, R, 0, 2 * Math.PI);
    ctx.fill();

    // Apply shadow for phases other than full moon
    if (fraction < 0.99) {
      // Calculate relative position of the moon in the sky
      const relativeYPosition = y / ctx.canvas.height;

      // Find appropriate gradient color based on moon's position
      let shadowBaseColor = "#0A0E2C"; // Default dark sky color

      if (this.gradientStops.length >= 2) {
        let lowerStop = this.gradientStops[0];
        let upperStop = this.gradientStops[this.gradientStops.length - 1];

        for (let i = 0; i < this.gradientStops.length - 1; i++) {
          const currentStop = this.gradientStops[i];
          const nextStop = this.gradientStops[i + 1];
          if (
            currentStop?.position !== undefined &&
            nextStop?.position !== undefined &&
            currentStop.position <= relativeYPosition &&
            nextStop.position >= relativeYPosition
          ) {
            lowerStop = currentStop;
            upperStop = nextStop;
            break;
          }
        }

        if (
          lowerStop &&
          upperStop &&
          lowerStop.position !== undefined &&
          upperStop.position !== undefined
        ) {
          shadowBaseColor =
            Math.abs(relativeYPosition - lowerStop.position) <
            Math.abs(relativeYPosition - upperStop.position)
              ? lowerStop.color
              : upperStop.color;
        }
      } else if (this.gradientStops.length === 1) {
        const firstStop = this.gradientStops[0];
        if (firstStop) {
          shadowBaseColor = firstStop.color;
        }
      }

      const shadowColor = a11y.highContrast ? "#000000" : shadowBaseColor;
      ctx.fillStyle = shadowColor;

      const phaseAngleForShadow = (phaseValue - 0.5) * 2 * Math.PI;
      const shadowDiscCenterX = x - R * Math.cos(phaseAngleForShadow);

      // Create clipping path for moon circle
      ctx.save();
      ctx.beginPath();
      ctx.arc(x, y, R, 0, 2 * Math.PI);
      ctx.clip();

      // Draw shadow circle
      ctx.beginPath();
      ctx.arc(shadowDiscCenterX, y, R, 0, 2 * Math.PI);
      ctx.fill();

      ctx.restore(); // Remove clipping
    }

    // Optional outline for new moon
    if (fraction < 0.03 && !a11y.highContrast && fraction < 0.98) {
      ctx.strokeStyle = "rgba(100, 100, 120, 0.3)";
      ctx.lineWidth = Math.max(0.5, R * 0.02);
      ctx.beginPath();
      ctx.arc(x, y, R, 0, 2 * Math.PI);
      ctx.stroke();
    }

    ctx.restore();
  }

  getMoon(): Moon | null {
    return this.Moon;
  }

  cleanup() {
    this.Moon = null;
  }
}
