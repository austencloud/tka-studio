// src/lib/components/backgrounds/systems/nightSky/SpaceshipSystem.ts
import { NightSkyUtils } from "./NightSkyUtils";
import type {
  AccessibilitySettings,
  Dimensions,
  EasterEggState,
  Spaceship,
  QualityLevel,
} from "$lib/domain/background/BackgroundTypes";

export interface SpaceshipConfig {
  size: number;
  speedPercent: number;
  color: string;
  enabledOnQuality: QualityLevel[];
}

export class SpaceshipSystem {
  private spaceshipState: EasterEggState<Spaceship>;
  private config: SpaceshipConfig;

  constructor(config: SpaceshipConfig) {
    this.config = config;
    this.spaceshipState = {
      element: null,
      timer: 0,
      interval: NightSkyUtils.randInt(15000, 30000),
    };
  }

  update(dim: Dimensions, a11y: AccessibilitySettings, quality: QualityLevel) {
    if (!this.config.enabledOnQuality.includes(quality)) {
      this.spaceshipState.element = null;
      return;
    }

    const effectiveSpeed = a11y.reducedMotion ? 0.2 : 1;

    if (!this.spaceshipState.element) {
      this.spaceshipState.timer++;
      if (this.spaceshipState.timer >= this.spaceshipState.interval) {
        const dir = Math.random() > 0.5 ? 1 : -1;
        this.spaceshipState.element = {
          x: dir > 0 ? -this.config.size : dim.width + this.config.size,
          y: Math.random() * dim.height * 0.4 + dim.height * 0.1, // Upper part of sky
          width: this.config.size,
          height: this.config.size / 2,
          speed: this.config.speedPercent * dim.width * effectiveSpeed,
          active: true,
          direction: dir,
          opacity: 1.0,
        };
        this.spaceshipState.timer = 0;
        this.spaceshipState.interval = NightSkyUtils.randInt(15000, 30000);
      }
    } else {
      const s = this.spaceshipState.element;
      s.x += s.direction * s.speed;
      if (s.x < -s.width || s.x > dim.width + s.width) {
        this.spaceshipState.element = null;
      }
    }
  }

  draw(ctx: CanvasRenderingContext2D, a11y: AccessibilitySettings) {
    const s = this.spaceshipState.element;
    if (!s) return;

    ctx.globalAlpha = s.opacity * (a11y.reducedMotion ? 0.7 : 1);
    ctx.fillStyle = a11y.highContrast ? "#FFFFFF" : this.config.color;

    // Simple spaceship shape
    ctx.beginPath();
    ctx.ellipse(s.x, s.y, s.width / 2, s.height / 2, 0, 0, 2 * Math.PI);
    ctx.fill();

    // Add navigation lights
    ctx.fillStyle = s.direction > 0 ? "#FF0000" : "#00FF00"; // Red/green navigation lights
    ctx.beginPath();
    ctx.arc(
      s.x + s.direction * s.width * 0.3,
      s.y,
      Math.max(1, s.width * 0.1),
      0,
      2 * Math.PI
    );
    ctx.fill();

    ctx.globalAlpha = 1;
  }

  cleanup() {
    this.spaceshipState = {
      element: null,
      timer: 0,
      interval: NightSkyUtils.randInt(15000, 30000),
    };
  }
}
