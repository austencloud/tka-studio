// src/lib/components/backgrounds/systems/nightSky/ParallaxStarSystem.ts
import { NightSkyUtils, type StarConfig } from "./NightSkyUtils";
import type {
  AccessibilitySettings,
  Dimensions,
  Star,
} from "$lib/domain/background/BackgroundTypes";

export interface ParallaxConfig {
  far: { density: number; drift: number };
  mid: { density: number; drift: number };
  near: { density: number; drift: number };
}

export interface QualitySettings {
  densityMultiplier: number;
}

type ParallaxLayer = {
  stars: Star[];
  driftX: number;
  driftY: number;
};

export class ParallaxStarSystem {
  private layers: Record<"far" | "mid" | "near", ParallaxLayer> = {
    far: { stars: [], driftX: 0, driftY: 0 },
    mid: { stars: [], driftX: 0, driftY: 0 },
    near: { stars: [], driftX: 0, driftY: 0 },
  };

  private config: ParallaxConfig;
  private starConfig: StarConfig;
  private qualitySettings: QualitySettings;

  constructor(
    config: ParallaxConfig,
    starConfig: StarConfig,
    qualitySettings: QualitySettings
  ) {
    this.config = config;
    this.starConfig = starConfig;
    this.qualitySettings = qualitySettings;
  }

  initialize(dim: Dimensions, a11y: AccessibilitySettings) {
    const mkLayer = (key: "far" | "mid" | "near"): ParallaxLayer => {
      const pCfg = this.config[key];
      const density = pCfg.density * this.qualitySettings.densityMultiplier;
      const count = Math.floor(dim.width * dim.height * density);
      const stars: Star[] = Array.from({ length: count }).map(() =>
        NightSkyUtils.makeStar(dim, this.starConfig, a11y)
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

  update(dim: Dimensions, a11y: AccessibilitySettings) {
    if (!this.layers || Object.keys(this.layers).length === 0) {
      this.initialize(dim, a11y);
      return;
    }

    (["far", "mid", "near"] as Array<keyof typeof this.layers>).forEach(
      (key) => {
        const L = this.layers[key];
        if (L && L.stars && Array.isArray(L.stars)) {
          L.stars.forEach((s: Star) => {
            s.x =
              (s.x + L.driftX * (a11y.reducedMotion ? 0.3 : 1) + dim.width) %
              dim.width;
            s.y =
              (s.y + L.driftY * (a11y.reducedMotion ? 0.3 : 1) + dim.height) %
              dim.height;
            if (s.isTwinkling) {
              s.currentOpacity =
                s.baseOpacity *
                (0.7 +
                  0.3 *
                    Math.sin(
                      (s.twinklePhase +=
                        s.twinkleSpeed * (a11y.reducedMotion ? 0.3 : 1))
                    ));
            }
          });
        }
      }
    );
  }

  draw(ctx: CanvasRenderingContext2D, a11y: AccessibilitySettings) {
    if (!this.layers || Object.keys(this.layers).length === 0) return;

    (["far", "mid", "near"] as Array<keyof typeof this.layers>).forEach(
      (key) => {
        const L = this.layers[key];
        if (L && L.stars && Array.isArray(L.stars)) {
          const alphaMult = key === "far" ? 0.5 : key === "mid" ? 0.8 : 1;
          L.stars.forEach((star: Star) => {
            ctx.globalAlpha =
              star.currentOpacity * alphaMult * (a11y.reducedMotion ? 0.7 : 1);
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

  getNearStars(): Star[] {
    return this.layers.near?.stars || [];
  }

  cleanup() {
    this.layers = {
      far: { stars: [], driftX: 0, driftY: 0 },
      mid: { stars: [], driftX: 0, driftY: 0 },
      near: { stars: [], driftX: 0, driftY: 0 },
    };
  }
}
