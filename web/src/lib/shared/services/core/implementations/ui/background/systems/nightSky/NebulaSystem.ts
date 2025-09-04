// src/lib/components/backgrounds/systems/nightSky/NebulaSystem.ts
import type { AccessibilitySettings, Dimensions, QualityLevel } from "$domain";
import { NightSkyUtils } from "./NightSkyUtils";

export interface NebulaConfig {
  count: number;
  minRadius: number;
  maxRadius: number;
  colors: string[];
  pulseSpeed: {
    min: number;
    max: number;
  };
  enabledOnQuality: QualityLevel[];
}

interface Nebula {
  x: number;
  y: number;
  baseR: number;
  phase: number;
  color: string;
}

export class NebulaSystem {
  private nebulae: Nebula[] = [];
  private config: NebulaConfig;

  constructor(config: NebulaConfig) {
    this.config = config;
  }

  initialize(dim: Dimensions, quality: QualityLevel) {
    if (!this.config.enabledOnQuality.includes(quality)) {
      this.nebulae = [];
      return;
    }

    this.nebulae = Array.from({ length: this.config.count }).map(() => {
      const r = NightSkyUtils.randFloat(
        this.config.minRadius,
        this.config.maxRadius
      );
      return {
        x: Math.random() * dim.width,
        y: Math.random() * dim.height * 0.7, // Keep them mostly in upper part
        baseR: r,
        phase: Math.random() * Math.PI * 2,
        color: NightSkyUtils.randItem(this.config.colors),
      };
    });
  }

  update(a11y: AccessibilitySettings) {
    if (!this.nebulae.length) return;

    const speedRange = this.config.pulseSpeed;
    const effectiveSpeed = a11y.reducedMotion ? 0.3 : 1;
    this.nebulae.forEach(
      (n) =>
        (n.phase +=
          NightSkyUtils.randFloat(speedRange.min, speedRange.max) *
          effectiveSpeed)
    );
  }

  draw(ctx: CanvasRenderingContext2D, a11y: AccessibilitySettings) {
    if (!this.nebulae.length) return;

    ctx.globalAlpha = a11y.reducedMotion ? 0.5 : 1;
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

  cleanup() {
    this.nebulae = [];
  }
}
