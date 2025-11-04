import type { AccessibilitySettings } from "../../shared/domain/models/background-models";
import type {
  Dimensions,
  PerformanceMetrics,
  QualityLevel,
} from "../../shared/domain/types/background-types";
import type { IBackgroundSystem } from "../../shared/services/contracts/IBackgroundSystem";
import type { LensFlare, Sparkle } from "../domain";

export class AuroraBackgroundSystem implements IBackgroundSystem {
  private quality: QualityLevel = "medium";
  private accessibility: AccessibilitySettings = {
    reducedMotion: false,
    highContrast: false,
    visibleParticleSize: 2,
  };
  private thumbnailMode: boolean = false;

  // Animation state
  private gradientShift = 0;
  private colorShift = 0;
  private wavePhase = 0;

  // Animated elements
  private lensFlares: LensFlare[] = [];
  private sparkles: Sparkle[] = [];

  private isInitialized = false;

  public initialize(_dimensions: Dimensions, quality: QualityLevel): void {
    this.quality = quality;
    this.isInitialized = true;

    // Initialize lens flares based on quality
    const numLensFlares = this.getNumLensFlares();
    this.lensFlares = this.createLensFlares(numLensFlares);

    // Initialize sparkles based on quality
    const numSparkles = this.getNumSparkles();
    this.sparkles = this.createSparkles(numSparkles);

    // Pre-populate: Randomize animation phases so aurora appears mid-animation
    this.gradientShift = Math.random() * Math.PI * 2;
    this.colorShift = Math.random() * 360;
    this.wavePhase = Math.random() * Math.PI * 2;
  }

  public update(_dimensions: Dimensions, frameMultiplier: number = 1.0): void {
    if (!this.isInitialized) return;

    // Update animation phases - much slower for relaxed pace, with frame rate compensation
    this.gradientShift += 0.005 * frameMultiplier;
    this.colorShift = (this.colorShift + 0.2 * frameMultiplier) % 360; // Much slower color cycling
    this.wavePhase += 0.01 * frameMultiplier;

    // Update lens flares
    this.updateLensFlares(frameMultiplier);

    // Update sparkles
    this.updateSparkles(frameMultiplier);
  }

  public draw(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
    if (!this.isInitialized) return;

    // Draw wavy gradient background
    this.drawWavyGradient(ctx, dimensions);

    // Draw lens flares
    this.drawLensFlares(ctx, dimensions);

    // Draw sparkles
    this.drawSparkles(ctx, dimensions);
  }

  public setQuality(quality: QualityLevel): void {
    this.quality = quality;
    if (this.isInitialized) {
      // Reinitialize with new quality
      const numLensFlares = this.getNumLensFlares();
      const numSparkles = this.getNumSparkles();

      // Adjust existing arrays
      while (this.lensFlares.length > numLensFlares) this.lensFlares.pop();
      while (this.lensFlares.length < numLensFlares) this.lensFlares.push(this.createLensFlare());

      while (this.sparkles.length > numSparkles) this.sparkles.pop();
      while (this.sparkles.length < numSparkles)
        this.sparkles.push(this.createSparkle());
    }
  }

  public setAccessibility(settings: AccessibilitySettings): void {
    this.accessibility = settings;
  }

  public setThumbnailMode(enabled: boolean): void {
    this.thumbnailMode = enabled;
  }

  public cleanup(): void {
    this.lensFlares = [];
    this.sparkles = [];
    this.isInitialized = false;
  }

  public getMetrics(): PerformanceMetrics {
    return {
      fps: 60, // Estimated
      warnings: [],
      particleCount: this.lensFlares.length + this.sparkles.length,
    };
  }

  private getNumLensFlares(): number {
    switch (this.quality) {
      case "high":
        return 5;
      case "medium":
        return 3;
      case "low":
        return 2;
      case "minimal":
        return 1;
      default:
        return 3;
    }
  }

  private getNumSparkles(): number {
    if (this.accessibility.reducedMotion) return 0;

    switch (this.quality) {
      case "high":
        return 50;
      case "medium":
        return 30;
      case "low":
        return 15;
      case "minimal":
        return 5;
      default:
        return 30;
    }
  }

  private createLensFlares(count: number): LensFlare[] {
    const lensFlares: LensFlare[] = [];
    for (let i = 0; i < count; i++) {
      lensFlares.push(this.createLensFlare());
    }
    return lensFlares;
  }

  private createLensFlare(): LensFlare {
    // In thumbnail mode, make lens flares much larger and more opaque
    const baseSize = this.thumbnailMode ? 150 : 50;
    const sizeRange = this.thumbnailMode ? 200 : 100;
    const baseOpacity = this.thumbnailMode ? 0.4 : 0.1;
    const opacityRange = this.thumbnailMode ? 0.3 : 0.3;

    return {
      x: Math.random(),
      y: Math.random(),
      size: baseSize + Math.random() * sizeRange,
      opacity: baseOpacity + Math.random() * opacityRange,
      dx: (Math.random() - 0.5) * 0.002,
      dy: (Math.random() - 0.5) * 0.002,
      dsize: (Math.random() - 0.5) * 0.5,
      dopacity: (Math.random() - 0.5) * 0.005,
    };
  }

  private createSparkles(count: number): Sparkle[] {
    const sparkles: Sparkle[] = [];
    for (let i = 0; i < count; i++) {
      sparkles.push(this.createSparkle());
    }
    return sparkles;
  }

  private createSparkle(): Sparkle {
    return {
      x: Math.random(),
      y: Math.random(),
      size: 2 + Math.random() * 2,
      opacity: 0.5 + Math.random() * 0.5,
      pulseSpeed: 0.005 + Math.random() * 0.01,
    };
  }

  private updateLensFlares(frameMultiplier: number = 1.0): void {
    for (const lensFlare of this.lensFlares) {
      lensFlare.x += lensFlare.dx * frameMultiplier;
      lensFlare.y += lensFlare.dy * frameMultiplier;
      lensFlare.size += lensFlare.dsize * frameMultiplier;
      lensFlare.opacity += lensFlare.dopacity * frameMultiplier;

      // Keep within bounds and reverse direction if necessary
      if (lensFlare.x < 0 || lensFlare.x > 1) lensFlare.dx *= -1;
      if (lensFlare.y < 0 || lensFlare.y > 1) lensFlare.dy *= -1;
      if (lensFlare.size < 50 || lensFlare.size > 250) {
        lensFlare.dsize *= -1;
        // Clamp size to prevent negative values
        lensFlare.size = Math.max(50, Math.min(250, lensFlare.size));
      }
      if (lensFlare.opacity < 0.1 || lensFlare.opacity > 0.5) {
        lensFlare.dopacity *= -1;
        // Clamp opacity to prevent out of range values
        lensFlare.opacity = Math.max(0.1, Math.min(0.5, lensFlare.opacity));
      }
    }
  }

  private updateSparkles(frameMultiplier: number = 1.0): void {
    for (const sparkle of this.sparkles) {
      sparkle.opacity += sparkle.pulseSpeed * frameMultiplier;
      if (sparkle.opacity > 1.0 || sparkle.opacity < 0.5) {
        sparkle.pulseSpeed *= -1; // Reverse the pulse direction
      }
    }
  }

  private drawWavyGradient(
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions
  ): void {
    // Create wavy gradient background similar to desktop version
    const gradient = ctx.createLinearGradient(
      0,
      dimensions.height,
      dimensions.width,
      0
    );

    const colors = [
      { r: 255, g: 0, b: 255, a: 0.4 }, // Magenta
      { r: 0, g: 255, b: 255, a: 0.4 }, // Cyan
      { r: 255, g: 255, b: 0, a: 0.4 }, // Yellow
    ];

    for (let i = 0; i < colors.length; i++) {
      const color = colors[i];
      if (!color) continue;

      // Calculate hue shift for color cycling
      const hue = (this.colorShift + i * 120) % 360;
      const hslColor = this.hsvToRgb(hue / 360, 1, 1);

      // Apply sine wave to adjust gradient positioning
      const waveShift =
        0.1 * Math.sin(this.wavePhase + (i * 2 * Math.PI) / colors.length);
      const position = Math.min(Math.max(i / colors.length + waveShift, 0), 1);

      gradient.addColorStop(
        position,
        `rgba(${hslColor.r}, ${hslColor.g}, ${hslColor.b}, ${color.a ?? 1})`
      );
    }

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, dimensions.width, dimensions.height);
  }

  private drawLensFlares(
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions
  ): void {
    for (let i = 0; i < this.lensFlares.length; i++) {
      const lensFlare = this.lensFlares[i];
      if (!lensFlare) continue;

      const x = lensFlare.x * dimensions.width;
      const y = lensFlare.y * dimensions.height;

      // Ensure size is always positive to prevent createRadialGradient errors
      const size = Math.max(0, lensFlare.size);

      ctx.save();

      // Create colorful radial gradients for lens flares
      const hue = (this.colorShift + i * 60) % 360;
      const color = this.hsvToRgb(hue / 360, 0.8, 1);

      const gradient = ctx.createRadialGradient(x, y, 0, x, y, size);
      gradient.addColorStop(
        0,
        `rgba(${color.r}, ${color.g}, ${color.b}, ${lensFlare.opacity})`
      );
      gradient.addColorStop(
        0.5,
        `rgba(${color.r}, ${color.g}, ${color.b}, ${lensFlare.opacity * 0.5})`
      );
      gradient.addColorStop(
        1,
        `rgba(${color.r}, ${color.g}, ${color.b}, 0)`
      );

      ctx.fillStyle = gradient;
      ctx.filter = "blur(20px)"; // Soft glow effect

      ctx.beginPath();
      ctx.ellipse(x, y, size, size, 0, 0, 2 * Math.PI);
      ctx.fill();

      ctx.restore();
    }
  }

  private drawSparkles(
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions
  ): void {
    for (const sparkle of this.sparkles) {
      const x = sparkle.x * dimensions.width;
      const y = sparkle.y * dimensions.height;

      ctx.save();
      ctx.globalAlpha = sparkle.opacity;
      ctx.fillStyle = `rgba(255, 255, 255, ${sparkle.opacity})`;

      ctx.beginPath();
      ctx.ellipse(x, y, sparkle.size / 2, sparkle.size / 2, 0, 0, 2 * Math.PI);
      ctx.fill();

      ctx.restore();
    }
  }

  // Helper function to convert HSV to RGB
  private hsvToRgb(
    h: number,
    s: number,
    v: number
  ): { r: number; g: number; b: number } {
    let r: number, g: number, b: number;

    const i = Math.floor(h * 6);
    const f = h * 6 - i;
    const p = v * (1 - s);
    const q = v * (1 - f * s);
    const t = v * (1 - (1 - f) * s);

    switch (i % 6) {
      case 0:
        r = v;
        g = t;
        b = p;
        break;
      case 1:
        r = q;
        g = v;
        b = p;
        break;
      case 2:
        r = p;
        g = v;
        b = t;
        break;
      case 3:
        r = p;
        g = q;
        b = v;
        break;
      case 4:
        r = t;
        g = p;
        b = v;
        break;
      case 5:
        r = v;
        g = p;
        b = q;
        break;
      default:
        r = g = b = 0;
    }

    return {
      r: Math.round(r * 255),
      g: Math.round(g * 255),
      b: Math.round(b * 255),
    };
  }
}
