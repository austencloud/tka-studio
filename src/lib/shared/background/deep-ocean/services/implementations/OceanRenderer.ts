import { injectable } from "inversify";
import type { Dimensions } from "$shared";
import type {
  MarineLife,
  Bubble,
  OceanParticle,
  FishMarineLife,
  JellyfishMarineLife,
} from "../../domain/models/DeepOceanModels";
import type { IOceanRenderer } from "../contracts";

@injectable()
export class OceanRenderer implements IOceanRenderer {
  drawOceanGradient(
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions
  ): void {
    // Create ocean gradient background
    const gradient = ctx.createLinearGradient(0, 0, 0, dimensions.height);
    gradient.addColorStop(0, "#0d2d47"); // Rich ocean blue
    gradient.addColorStop(0.3, "#1a3a4a"); // Mid-depth
    gradient.addColorStop(0.7, "#0f2535"); // Deeper
    gradient.addColorStop(1, "#091a2b"); // Darker ocean depth

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, dimensions.width, dimensions.height);
  }

  drawLightRays(
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions,
    lightRays: Array<{
      x: number;
      opacity: number;
      width: number;
      angle: number;
      phase: number;
      speed: number;
    }>,
    quality: string
  ): void {
    if (quality === "minimal") return;

    ctx.save();
    for (const ray of lightRays) {
      ctx.save();
      ctx.translate(ray.x, 0);
      ctx.rotate((ray.angle * Math.PI) / 180); // Convert degrees to radians

      const gradient = ctx.createLinearGradient(
        0,
        0,
        0,
        dimensions.height * 0.6
      );
      gradient.addColorStop(0, `rgba(135, 206, 250, ${ray.opacity})`); // Light blue from surface
      gradient.addColorStop(0.4, `rgba(100, 149, 237, ${ray.opacity * 0.7})`); // Dimmer blue
      gradient.addColorStop(1, `rgba(70, 130, 180, 0)`); // Fade to transparent

      ctx.fillStyle = gradient;
      ctx.fillRect(-ray.width / 2, 0, ray.width, dimensions.height * 0.6);
      ctx.restore();
    }
    ctx.restore();
  }

  drawBubbles(ctx: CanvasRenderingContext2D, bubbles: Bubble[]): void {
    ctx.save();
    for (const bubble of bubbles) {
      ctx.globalAlpha = bubble.opacity;
      ctx.beginPath();
      ctx.arc(bubble.x, bubble.y, bubble.radius, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(173, 216, 230, 0.6)"; // Light blue bubbles
      ctx.fill();

      // Add subtle highlight
      ctx.beginPath();
      ctx.arc(
        bubble.x - bubble.radius * 0.3,
        bubble.y - bubble.radius * 0.3,
        bubble.radius * 0.3,
        0,
        Math.PI * 2
      );
      ctx.fillStyle = "rgba(255, 255, 255, 0.3)";
      ctx.fill();
    }
    ctx.restore();
  }

  drawMarineLife(
    ctx: CanvasRenderingContext2D,
    marineLife: MarineLife[]
  ): void {
    ctx.save();
    marineLife.forEach((marine) => {
      ctx.save();
      ctx.globalAlpha = marine.opacity;

      if (marine.type === "fish") {
        this.drawFish(ctx, marine as FishMarineLife);
      } else {
        this.drawJellyfish(ctx, marine as JellyfishMarineLife);
      }

      ctx.restore();
    });
    ctx.restore();
  }

  private drawFish(ctx: CanvasRenderingContext2D, fish: FishMarineLife): void {
    ctx.translate(fish.x, fish.y);
    ctx.scale(fish.direction, 1);

    const image = fish.image;
    const ready = image?.complete ?? false;

    if (image && ready) {
      ctx.drawImage(
        image,
        -fish.width / 2,
        -fish.height / 2,
        fish.width,
        fish.height
      );
    } else {
      // Fallback simple shape while sprite loads
      const fallbackWidth = fish.width;
      const fallbackHeight = fish.height * 0.6;
      ctx.fillStyle = "#7dd3fc";
      ctx.beginPath();
      ctx.ellipse(
        0,
        0,
        fallbackWidth * 0.5,
        fallbackHeight * 0.5,
        0,
        0,
        Math.PI * 2
      );
      ctx.fill();
      ctx.beginPath();
      ctx.moveTo(fallbackWidth * 0.5, 0);
      ctx.lineTo(fallbackWidth * 0.65, -fallbackHeight * 0.25);
      ctx.lineTo(fallbackWidth * 0.65, fallbackHeight * 0.25);
      ctx.closePath();
      ctx.fill();
    }
  }

  private drawJellyfish(
    ctx: CanvasRenderingContext2D,
    jelly: JellyfishMarineLife
  ): void {
    ctx.translate(jelly.x, jelly.y);

    const radius = jelly.size * 0.55;
    const pulse = 1 + Math.sin(jelly.animationPhase * 0.9) * 0.05;
    const bellRadius = radius * pulse;

    const gradient = ctx.createRadialGradient(0, 0, 0, 0, 0, bellRadius);
    gradient.addColorStop(0, this.lightenColor(jelly.color, 0.4));
    gradient.addColorStop(0.65, jelly.color);
    gradient.addColorStop(1, this.darkenColor(jelly.color, 0.25));

    ctx.shadowColor = this.lightenColor(jelly.color, 0.5);
    ctx.shadowBlur = jelly.glowIntensity * 35;
    ctx.beginPath();
    ctx.fillStyle = gradient;
    ctx.arc(0, 0, bellRadius, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;

    const tentacleOriginY = bellRadius * 0.4;
    ctx.lineWidth = Math.max(1.4, jelly.size * 0.08);
    ctx.lineCap = "round";
    ctx.strokeStyle = this.lightenColor(jelly.color, 0.2);

    jelly.tentacleSeeds.forEach((seed, index) => {
      const offset =
        jelly.tentacleSeeds.length === 1
          ? 0
          : index / (jelly.tentacleSeeds.length - 1) - 0.5;
      const sway =
        Math.sin(jelly.animationPhase + seed) * jelly.waveAmplitude * 0.6;
      const startX = offset * bellRadius * 0.9;
      const length =
        jelly.size * (1.2 + Math.sin(jelly.animationPhase + seed) * 0.15);

      ctx.beginPath();
      ctx.moveTo(startX, tentacleOriginY);
      ctx.bezierCurveTo(
        startX + sway * 0.4,
        tentacleOriginY + length * 0.35,
        startX - sway * 0.25,
        tentacleOriginY + length * 0.7,
        startX + sway,
        tentacleOriginY + length
      );
      ctx.stroke();
    });
  }

  private lightenColor(color: string, amount: number): string {
    // Parse hex color
    const hex = color.replace("#", "");
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);

    // Lighten by moving towards white
    const nr = Math.min(255, Math.round(r + (255 - r) * amount));
    const ng = Math.min(255, Math.round(g + (255 - g) * amount));
    const nb = Math.min(255, Math.round(b + (255 - b) * amount));

    return `#${nr.toString(16).padStart(2, "0")}${ng.toString(16).padStart(2, "0")}${nb.toString(16).padStart(2, "0")}`;
  }

  private darkenColor(color: string, amount: number): string {
    // Parse hex color
    const hex = color.replace("#", "");
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);

    // Darken by moving towards black
    const nr = Math.max(0, Math.round(r * (1 - amount)));
    const ng = Math.max(0, Math.round(g * (1 - amount)));
    const nb = Math.max(0, Math.round(b * (1 - amount)));

    return `#${nr.toString(16).padStart(2, "0")}${ng.toString(16).padStart(2, "0")}${nb.toString(16).padStart(2, "0")}`;
  }

  drawParticles(
    ctx: CanvasRenderingContext2D,
    particles: OceanParticle[]
  ): void {
    ctx.save();
    for (const particle of particles) {
      ctx.globalAlpha = particle.opacity;
      ctx.fillStyle = particle.color;
      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  }
}
