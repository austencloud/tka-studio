// src/lib/components/backgrounds/auroraBorealis/AuroraBorealisBackgroundSystem.ts
import type {
  AccessibilitySettings,
  BackgroundSystem,
  Dimensions,
  PerformanceMetrics,
  QualityLevel,
} from "../types/types";

export class AuroraBorealisBackgroundSystem implements BackgroundSystem {
  private quality: QualityLevel = "medium";
  private accessibility: AccessibilitySettings = {
    reducedMotion: false,
    highContrast: false,
    visibleParticleSize: 2,
  };

  // Animation state
  private lightWaves: number[] = [];
  private isInitialized = false;

  // Aurora Borealis color palette
  private readonly auroraColors = [
    { r: 0, g: 25, b: 50, a: 0.4 }, // Deep blue
    { r: 0, g: 50, b: 100, a: 0.2 }, // Medium blue
    { r: 0, g: 100, b: 150, a: 0.1 }, // Light blue
    { r: 50, g: 150, b: 100, a: 0.15 }, // Blue-green
    { r: 100, g: 200, b: 150, a: 0.12 }, // Green
    { r: 150, g: 255, b: 200, a: 0.08 }, // Light green
  ];

  public initialize(_dimensions: Dimensions, quality: QualityLevel): void {
    this.quality = quality;
    this.isInitialized = true;

    // Initialize light waves with random phases for natural variation
    const numWaves = this.getNumWaves();
    this.lightWaves = [];
    for (let i = 0; i < numWaves; i++) {
      this.lightWaves.push(Math.random() * 2 * Math.PI);
    }
  }

  public update(_dimensions: Dimensions): void {
    if (!this.isInitialized) return;

    // Respect accessibility settings
    const animationSpeed = this.accessibility.reducedMotion ? 0.002 : 1.0;

    // Update light wave positions for smooth animation
    // Advance each wave at slightly different speeds for natural variation
    for (let i = 0; i < this.lightWaves.length; i++) {
      const currentWave = this.lightWaves[i];
      if (currentWave !== undefined) {
        const waveSpeed = (0.008 + i * 0.002) * animationSpeed; // Varying speeds with accessibility consideration
        this.lightWaves[i] = currentWave + waveSpeed;

        // Keep waves within reasonable bounds to prevent overflow
        const currentValue = this.lightWaves[i];
        if (currentValue !== undefined && currentValue > 4 * Math.PI) {
          this.lightWaves[i] = currentValue - 4 * Math.PI;
        }
      }
    }
  }

  public draw(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
    if (!this.isInitialized) return;

    // Draw base gradient from dark to lighter
    this.drawBaseGradient(ctx, dimensions);

    // Draw aurora light waves
    this.drawAuroraWaves(ctx, dimensions);
  }

  public setQuality(quality: QualityLevel): void {
    this.quality = quality;
    if (this.isInitialized) {
      // Adjust number of waves based on quality
      const numWaves = this.getNumWaves();
      while (this.lightWaves.length > numWaves) this.lightWaves.pop();
      while (this.lightWaves.length < numWaves) {
        this.lightWaves.push(Math.random() * 2 * Math.PI);
      }
    }
  }

  public setAccessibility(settings: AccessibilitySettings): void {
    this.accessibility = settings;
    // Note: Accessibility settings would be used to modify animation behavior
    // For example, reducing motion if settings.reducedMotion is true
  }

  public cleanup(): void {
    this.lightWaves = [];
    this.isInitialized = false;
  }

  public getMetrics(): PerformanceMetrics {
    return {
      fps: 60, // Estimated
      warnings: [],
      particleCount: this.lightWaves.length,
    };
  }

  private getNumWaves(): number {
    switch (this.quality) {
      case "high":
        return 12;
      case "medium":
        return 10;
      case "low":
        return 6;
      case "minimal":
        return 4;
      default:
        return 10;
    }
  }

  private drawBaseGradient(
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions,
  ): void {
    // Create base gradient from dark to lighter
    const baseGradient = ctx.createLinearGradient(
      0,
      0,
      dimensions.width,
      dimensions.height,
    );
    baseGradient.addColorStop(0, "rgb(5, 10, 25)"); // Very dark blue
    baseGradient.addColorStop(0.5, "rgb(10, 20, 40)"); // Dark blue
    baseGradient.addColorStop(1, "rgb(15, 30, 60)"); // Medium dark blue

    ctx.fillStyle = baseGradient;
    ctx.fillRect(0, 0, dimensions.width, dimensions.height);
  }

  private drawAuroraWaves(
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions,
  ): void {
    // Calculate wave positions for gradient
    const wavePositions: Array<[number, number]> = [];

    for (let i = 0; i < this.lightWaves.length; i++) {
      const wave = this.lightWaves[i];
      if (wave !== undefined) {
        const position = (Math.sin(wave) + 1) / 2; // Normalize to 0-1
        wavePositions.push([position, i]);
      }
    }

    // Sort positions to ensure proper gradient ordering
    wavePositions.sort((a, b) => a[0] - b[0]);

    // Create gradient with aurora colors
    const gradient = ctx.createLinearGradient(
      0,
      0,
      dimensions.width,
      dimensions.height,
    );

    for (const [pos, waveIndex] of wavePositions) {
      const colorIndex = waveIndex % this.auroraColors.length;
      const color = this.auroraColors[colorIndex];

      if (color && this.lightWaves[waveIndex] !== undefined) {
        // Add some dynamic intensity variation
        const waveValue = this.lightWaves[waveIndex];
        if (waveValue !== undefined) {
          const intensityFactor = (Math.sin(waveValue * 1.5) + 1) / 2;
          const alpha = color.a * intensityFactor;

          gradient.addColorStop(
            pos,
            `rgba(${color.r}, ${color.g}, ${color.b}, ${alpha})`,
          );
        }
      }
    }

    // Fill with the aurora gradient
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, dimensions.width, dimensions.height);

    // Add additional wave effects for more realism
    if (this.quality === "high") {
      this.drawAdditionalWaveEffects(ctx, dimensions);
    }
  }

  private drawAdditionalWaveEffects(
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions,
  ): void {
    // Add subtle vertical wave patterns for enhanced aurora effect
    ctx.save();

    for (let i = 0; i < this.lightWaves.length; i += 2) {
      const wave = this.lightWaves[i];
      if (wave !== undefined) {
        const x = ((Math.sin(wave * 0.5) + 1) / 2) * dimensions.width;
        const width = 20 + Math.sin(wave) * 10;

        const waveGradient = ctx.createLinearGradient(
          x - width / 2,
          0,
          x + width / 2,
          0,
        );
        const color = this.auroraColors[i % this.auroraColors.length];
        if (color) {
          const intensity = ((Math.sin(wave * 2) + 1) / 2) * 0.1;

          waveGradient.addColorStop(
            0,
            `rgba(${color.r}, ${color.g}, ${color.b}, 0)`,
          );
          waveGradient.addColorStop(
            0.5,
            `rgba(${color.r}, ${color.g}, ${color.b}, ${intensity})`,
          );
          waveGradient.addColorStop(
            1,
            `rgba(${color.r}, ${color.g}, ${color.b}, 0)`,
          );

          ctx.fillStyle = waveGradient;
          ctx.fillRect(x - width / 2, 0, width, dimensions.height);
        }
      }
    }

    ctx.restore();
  }
}
