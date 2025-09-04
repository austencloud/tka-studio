// src/lib/components/backgrounds/aurora/AuroraBackgroundSystem.ts
import type {
  AccessibilitySettings,
  Dimensions,
  PerformanceMetrics,
  QualityLevel,
} from "$domain";
import type { IBackgroundSystem } from "$services";

interface Blob {
  x: number;
  y: number;
  size: number;
  opacity: number;
  dx: number;
  dy: number;
  dsize: number;
  dopacity: number;
}

interface Sparkle {
  x: number;
  y: number;
  size: number;
  opacity: number;
  pulseSpeed: number;
}

export class AuroraBackgroundSystem implements IBackgroundSystem {
  private quality: QualityLevel = "medium";
  private accessibility: AccessibilitySettings = {
    reducedMotion: false,
    highContrast: false,
    visibleParticleSize: 2,
  };

  // Animation state
  private gradientShift = 0;
  private colorShift = 0;
  private wavePhase = 0;

  // Animated elements
  private blobs: Blob[] = [];
  private sparkles: Sparkle[] = [];

  private isInitialized = false;

  public initialize(_dimensions: Dimensions, quality: QualityLevel): void {
    this.quality = quality;
    this.isInitialized = true;

    // Initialize blobs based on quality
    const numBlobs = this.getNumBlobs();
    this.blobs = this.createBlobs(numBlobs);

    // Initialize sparkles based on quality
    const numSparkles = this.getNumSparkles();
    this.sparkles = this.createSparkles(numSparkles);
  }

  public update(_dimensions: Dimensions): void {
    if (!this.isInitialized) return;

    // Update animation phases - much slower for relaxed pace
    this.gradientShift += 0.005;
    this.colorShift = (this.colorShift + 0.2) % 360; // Much slower color cycling
    this.wavePhase += 0.01;

    // Update blobs
    this.updateBlobs();

    // Update sparkles
    this.updateSparkles();
  }

  public draw(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
    if (!this.isInitialized) return;

    // Draw wavy gradient background
    this.drawWavyGradient(ctx, dimensions);

    // Draw blobs
    this.drawBlobs(ctx, dimensions);

    // Draw sparkles
    this.drawSparkles(ctx, dimensions);
  }

  public setQuality(quality: QualityLevel): void {
    this.quality = quality;
    if (this.isInitialized) {
      // Reinitialize with new quality
      const numBlobs = this.getNumBlobs();
      const numSparkles = this.getNumSparkles();

      // Adjust existing arrays
      while (this.blobs.length > numBlobs) this.blobs.pop();
      while (this.blobs.length < numBlobs) this.blobs.push(this.createBlob());

      while (this.sparkles.length > numSparkles) this.sparkles.pop();
      while (this.sparkles.length < numSparkles)
        this.sparkles.push(this.createSparkle());
    }
  }

  public setAccessibility(settings: AccessibilitySettings): void {
    this.accessibility = settings;
  }

  public cleanup(): void {
    this.blobs = [];
    this.sparkles = [];
    this.isInitialized = false;
  }

  public getMetrics(): PerformanceMetrics {
    return {
      fps: 60, // Estimated
      warnings: [],
      particleCount: this.blobs.length + this.sparkles.length,
    };
  }

  private getNumBlobs(): number {
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

  private createBlobs(count: number): Blob[] {
    const blobs: Blob[] = [];
    for (let i = 0; i < count; i++) {
      blobs.push(this.createBlob());
    }
    return blobs;
  }

  private createBlob(): Blob {
    return {
      x: Math.random(),
      y: Math.random(),
      size: 50 + Math.random() * 100,
      opacity: 0.1 + Math.random() * 0.3,
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

  private updateBlobs(): void {
    for (const blob of this.blobs) {
      blob.x += blob.dx;
      blob.y += blob.dy;
      blob.size += blob.dsize;
      blob.opacity += blob.dopacity;

      // Keep within bounds and reverse direction if necessary
      if (blob.x < 0 || blob.x > 1) blob.dx *= -1;
      if (blob.y < 0 || blob.y > 1) blob.dy *= -1;
      if (blob.size < 50 || blob.size > 250) blob.dsize *= -1;
      if (blob.opacity < 0.1 || blob.opacity > 0.5) blob.dopacity *= -1;
    }
  }

  private updateSparkles(): void {
    for (const sparkle of this.sparkles) {
      sparkle.opacity += sparkle.pulseSpeed;
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

  private drawBlobs(
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions
  ): void {
    for (const blob of this.blobs) {
      const x = blob.x * dimensions.width;
      const y = blob.y * dimensions.height;

      ctx.save();
      ctx.globalAlpha = blob.opacity;
      ctx.fillStyle = `rgba(255, 255, 255, ${blob.opacity})`;

      ctx.beginPath();
      ctx.ellipse(x, y, blob.size / 2, blob.size / 2, 0, 0, 2 * Math.PI);
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
