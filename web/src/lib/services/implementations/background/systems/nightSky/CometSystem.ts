// src/lib/components/backgrounds/systems/nightSky/CometSystem.ts
import { NightSkyUtils, type StarConfig } from "./NightSkyUtils";
import type {
  AccessibilitySettings,
  Dimensions,
  EasterEggState,
  Star,
  QualityLevel,
} from "$lib/domain/background/BackgroundTypes";

export interface CometConfig {
  size: number;
  speed: number;
  color: string;
  tailLength: number;
  interval: number;
  enabledOnQuality: QualityLevel[];
}

// Augment Star type with direction for comet movement
type CometStar = Star & { _direction?: number };

export class CometSystem {
  private cometState: EasterEggState<CometStar>;
  private config: CometConfig;
  private starConfig: StarConfig;

  constructor(config: CometConfig, starConfig: StarConfig) {
    this.config = config;
    this.starConfig = starConfig;
    this.cometState = {
      element: null,
      timer: 0,
      interval: config.interval,
    };
  }

  update(dim: Dimensions, a11y: AccessibilitySettings, quality: QualityLevel) {
    if (!this.config.enabledOnQuality.includes(quality)) {
      this.cometState.element = null;
      return;
    }

    const effectiveSpeed = a11y.reducedMotion ? 0.3 : 1;

    if (!this.cometState.element) {
      this.cometState.timer++;
      if (this.cometState.timer >= this.cometState.interval) {
        const dir = Math.random() > 0.5 ? 1 : -1;
        const comet = NightSkyUtils.makeStar(
          dim,
          this.starConfig,
          a11y
        ) as CometStar;
        comet.x = dir > 0 ? -this.config.size : dim.width + this.config.size;
        comet.y = Math.random() * dim.height * 0.3; // Upper sky
        comet.radius = this.config.size;
        comet.color = this.config.color;
        comet._direction = -dir; // Tail direction opposite to movement
        this.cometState.element = comet;
        this.cometState.timer = 0;
        this.cometState.interval = this.config.interval;
      }
    } else {
      const c = this.cometState.element;
      c.x += (c._direction || 1) * this.config.speed * effectiveSpeed;
      if (c.x < -this.config.size || c.x > dim.width + this.config.size) {
        this.cometState.element = null;
      }
    }
  }

  draw(ctx: CanvasRenderingContext2D, a11y: AccessibilitySettings) {
    const comet = this.cometState.element;
    if (!comet || !comet._direction) return;

    const tailLength = this.config.tailLength;
    const headX = comet.x;
    const headY = comet.y;

    ctx.globalAlpha = comet.currentOpacity * (a11y.reducedMotion ? 0.6 : 1);

    // Draw tail
    const tailEndX = headX + comet._direction * tailLength;
    const tailEndY = headY; // Simple horizontal tail

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

    // Draw head
    ctx.fillStyle = comet.color;
    ctx.beginPath();
    ctx.arc(headX, headY, comet.radius, 0, Math.PI * 2);
    ctx.fill();

    ctx.globalAlpha = 1;
  }

  cleanup() {
    this.cometState = {
      element: null,
      timer: 0,
      interval: this.config.interval,
    };
  }
}
