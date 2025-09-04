/**
 * Deep Ocean Background System
 *
 * Creates an immersive underwater environment with:
 * - Floating bubbles with realistic physics
 * - Marine life (fish, jellyfish, seaweed)
 * - Particle effects for depth
 * - Dynamic light rays from surface
 * - Ocean gradient background
 */

import type {
  AccessibilitySettings,
  Bubble,
  DeepOceanState,
  Dimensions,
  MarineLife,
  OceanParticle,
  PerformanceMetrics,
  QualityLevel,
} from "$domain";
import type { IBackgroundSystem } from "$services";

export class DeepOceanBackgroundSystem implements IBackgroundSystem {
  private state: DeepOceanState;
  private quality: QualityLevel = "medium";
  private accessibility: AccessibilitySettings = {
    reducedMotion: false,
    highContrast: false,
    visibleParticleSize: 1,
  };
  private animationTime = 0;

  constructor() {
    this.state = {
      bubbles: [],
      marineLife: [],
      particles: [],
      currentGradient: {
        top: "#001122",
        bottom: "#000511",
      },
      lightRays: [],
    };
  }

  initialize(dimensions: Dimensions, quality: QualityLevel): void {
    this.quality = quality;
    this.animationTime = 0;

    // Initialize bubbles
    this.initializeBubbles(dimensions);

    // Initialize marine life
    this.initializeMarineLife(dimensions);

    // Initialize particles
    this.initializeParticles(dimensions);

    // Initialize light rays
    this.initializeLightRays(dimensions);

    console.log(
      `🌊 Deep Ocean background initialized with ${this.state.bubbles.length} bubbles, ${this.state.marineLife.length} marine life`
    );
  }

  private initializeBubbles(dimensions: Dimensions): void {
    const bubbleCount = this.getBubbleCount();
    this.state.bubbles = [];

    for (let i = 0; i < bubbleCount; i++) {
      this.state.bubbles.push(this.createBubble(dimensions));
    }
  }

  private initializeMarineLife(dimensions: Dimensions): void {
    const marineCount = this.getMarineLifeCount();
    this.state.marineLife = [];

    for (let i = 0; i < marineCount; i++) {
      this.state.marineLife.push(this.createMarineLife(dimensions));
    }
  }

  private initializeParticles(dimensions: Dimensions): void {
    const particleCount = this.getParticleCount();
    this.state.particles = [];

    for (let i = 0; i < particleCount; i++) {
      this.state.particles.push(this.createParticle(dimensions));
    }
  }

  private initializeLightRays(dimensions: Dimensions): void {
    const rayCount =
      this.quality === "high" ? 8 : this.quality === "medium" ? 5 : 3;
    this.state.lightRays = [];

    for (let i = 0; i < rayCount; i++) {
      this.state.lightRays.push({
        x:
          (dimensions.width / rayCount) * i +
          Math.random() * (dimensions.width / rayCount),
        opacity: 0.1 + Math.random() * 0.15,
        width: 20 + Math.random() * 40,
        angle: -5 + Math.random() * 10,
      });
    }
  }

  private createBubble(dimensions: Dimensions): Bubble {
    return {
      x: Math.random() * dimensions.width,
      y: dimensions.height + Math.random() * 100,
      radius: 2 + Math.random() * 8,
      speed: 0.5 + Math.random() * 2,
      sway: 0.5 + Math.random() * 1.5,
      opacity: 0.3 + Math.random() * 0.4,
      swayOffset: Math.random() * Math.PI * 2,
      startY: dimensions.height + Math.random() * 100,
    };
  }

  private createMarineLife(dimensions: Dimensions): MarineLife {
    const types: Array<"fish" | "jellyfish" | "seaweed"> = [
      "fish",
      "jellyfish",
      "seaweed",
    ];
    const type = types[Math.floor(Math.random() * types.length)];
    const isMovingRight = Math.random() > 0.5;

    return {
      x: isMovingRight ? -50 : dimensions.width + 50,
      y: 100 + Math.random() * (dimensions.height - 200),
      dx: (isMovingRight ? 1 : -1) * (0.2 + Math.random() * 0.8),
      dy: (Math.random() - 0.5) * 0.2,
      size: 15 + Math.random() * 25,
      speed: 0.3 + Math.random() * 0.7,
      opacity: 0.4 + Math.random() * 0.4,
      type,
      animationPhase: Math.random() * Math.PI * 2,
      color: this.getMarineLifeColor(type),
    };
  }

  private createParticle(dimensions: Dimensions): OceanParticle {
    return {
      x: Math.random() * dimensions.width,
      y: Math.random() * dimensions.height,
      vx: (Math.random() - 0.5) * 0.5,
      vy: -0.1 - Math.random() * 0.3,
      size: 1 + Math.random() * 3,
      opacity: 0.2 + Math.random() * 0.3,
      color: this.getParticleColor(),
      life: 0,
      maxLife: 100 + Math.random() * 200,
    };
  }

  private getMarineLifeColor(type: "fish" | "jellyfish" | "seaweed"): string {
    switch (type) {
      case "fish":
        return ["#4a9eff", "#6fb7ff", "#85c1ff"][Math.floor(Math.random() * 3)];
      case "jellyfish":
        return ["#ff6b9d", "#ffa8cc", "#ffb3d1"][Math.floor(Math.random() * 3)];
      case "seaweed":
        return ["#2d5a2d", "#3d6b3d", "#4d7c4d"][Math.floor(Math.random() * 3)];
    }
  }

  private getParticleColor(): string {
    const colors = ["#ffffff", "#e6f3ff", "#cce7ff", "#b3dbff"];
    return colors[Math.floor(Math.random() * colors.length)];
  }

  private getBubbleCount(): number {
    switch (this.quality) {
      case "high":
        return 40;
      case "medium":
        return 25;
      case "low":
        return 15;
      case "minimal":
        return 8;
    }
  }

  private getMarineLifeCount(): number {
    switch (this.quality) {
      case "high":
        return 12;
      case "medium":
        return 8;
      case "low":
        return 5;
      case "minimal":
        return 3;
    }
  }

  private getParticleCount(): number {
    switch (this.quality) {
      case "high":
        return 60;
      case "medium":
        return 40;
      case "low":
        return 20;
      case "minimal":
        return 10;
    }
  }

  update(dimensions: Dimensions): void {
    this.animationTime += 0.016; // ~60fps

    if (this.accessibility.reducedMotion) return;

    // Update bubbles
    this.updateBubbles(dimensions);

    // Update marine life
    this.updateMarineLife(dimensions);

    // Update particles
    this.updateParticles(dimensions);

    // Update light rays
    this.updateLightRays();
  }

  private updateBubbles(dimensions: Dimensions): void {
    for (let i = this.state.bubbles.length - 1; i >= 0; i--) {
      const bubble = this.state.bubbles[i];

      // Update position
      bubble.y -= bubble.speed;
      bubble.x +=
        Math.sin(this.animationTime * bubble.sway + bubble.swayOffset) * 0.5;

      // Remove if off screen and create new one
      if (bubble.y < -bubble.radius * 2) {
        this.state.bubbles[i] = this.createBubble(dimensions);
      }
    }
  }

  private updateMarineLife(dimensions: Dimensions): void {
    for (let i = this.state.marineLife.length - 1; i >= 0; i--) {
      const marine = this.state.marineLife[i];

      // Update position
      marine.x += marine.dx * marine.speed;
      marine.y += marine.dy * marine.speed;
      marine.animationPhase += 0.05;

      // Add some vertical floating motion
      marine.y += Math.sin(marine.animationPhase) * 0.2;

      // Remove if off screen and create new one
      if (marine.x < -100 || marine.x > dimensions.width + 100) {
        this.state.marineLife[i] = this.createMarineLife(dimensions);
      }
    }
  }

  private updateParticles(dimensions: Dimensions): void {
    for (let i = this.state.particles.length - 1; i >= 0; i--) {
      const particle = this.state.particles[i];

      // Update position
      particle.x += particle.vx;
      particle.y += particle.vy;
      particle.life += 1;

      // Update opacity based on life
      particle.opacity = Math.max(0, 1 - particle.life / particle.maxLife);

      // Remove if dead and create new one
      if (particle.life >= particle.maxLife || particle.y < -10) {
        this.state.particles[i] = this.createParticle(dimensions);
      }
    }
  }

  private updateLightRays(): void {
    this.state.lightRays.forEach((ray) => {
      // Subtle opacity animation
      ray.opacity = 0.05 + Math.sin(this.animationTime * 0.5) * 0.05;
    });
  }

  draw(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
    // Clear canvas
    ctx.clearRect(0, 0, dimensions.width, dimensions.height);

    // Draw ocean gradient background
    this.drawOceanGradient(ctx, dimensions);

    // Draw light rays
    this.drawLightRays(ctx, dimensions);

    // Draw particles (background layer)
    this.drawParticles(ctx, 0.3);

    // Draw marine life
    this.drawMarineLife(ctx);

    // Draw bubbles
    this.drawBubbles(ctx);

    // Draw particles (foreground layer)
    this.drawParticles(ctx, 1.0);
  }

  private drawOceanGradient(
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions
  ): void {
    const gradient = ctx.createLinearGradient(0, 0, 0, dimensions.height);
    gradient.addColorStop(0, this.state.currentGradient.top);
    gradient.addColorStop(0.3, "#001a33");
    gradient.addColorStop(0.7, "#000e1a");
    gradient.addColorStop(1, this.state.currentGradient.bottom);

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, dimensions.width, dimensions.height);
  }

  private drawLightRays(
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions
  ): void {
    if (this.quality === "minimal") return;

    ctx.save();
    this.state.lightRays.forEach((ray) => {
      const gradient = ctx.createLinearGradient(
        ray.x,
        0,
        ray.x + Math.sin((ray.angle * Math.PI) / 180) * dimensions.height,
        dimensions.height
      );

      gradient.addColorStop(0, `rgba(135, 206, 235, ${ray.opacity})`);
      gradient.addColorStop(0.3, `rgba(135, 206, 235, ${ray.opacity * 0.5})`);
      gradient.addColorStop(1, "rgba(135, 206, 235, 0)");

      ctx.fillStyle = gradient;
      ctx.fillRect(ray.x - ray.width / 2, 0, ray.width, dimensions.height);
    });
    ctx.restore();
  }

  private drawBubbles(ctx: CanvasRenderingContext2D): void {
    ctx.save();
    this.state.bubbles.forEach((bubble) => {
      ctx.globalAlpha = bubble.opacity;
      ctx.beginPath();
      ctx.arc(bubble.x, bubble.y, bubble.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, 0.6)`;
      ctx.fill();

      // Add highlight
      ctx.beginPath();
      ctx.arc(
        bubble.x - bubble.radius * 0.3,
        bubble.y - bubble.radius * 0.3,
        bubble.radius * 0.3,
        0,
        Math.PI * 2
      );
      ctx.fillStyle = `rgba(255, 255, 255, 0.8)`;
      ctx.fill();
    });
    ctx.restore();
  }

  private drawMarineLife(ctx: CanvasRenderingContext2D): void {
    ctx.save();
    this.state.marineLife.forEach((marine) => {
      ctx.globalAlpha = marine.opacity;
      ctx.fillStyle = marine.color;

      ctx.save();
      ctx.translate(marine.x, marine.y);

      switch (marine.type) {
        case "fish":
          this.drawFish(ctx, marine);
          break;
        case "jellyfish":
          this.drawJellyfish(ctx, marine);
          break;
        case "seaweed":
          this.drawSeaweed(ctx, marine);
          break;
      }

      ctx.restore();
    });
    ctx.restore();
  }

  private drawFish(ctx: CanvasRenderingContext2D, marine: MarineLife): void {
    const size = marine.size;
    const flipX = marine.dx < 0 ? -1 : 1;

    ctx.scale(flipX, 1);

    // Fish body (ellipse)
    ctx.beginPath();
    ctx.ellipse(0, 0, size * 0.8, size * 0.4, 0, 0, Math.PI * 2);
    ctx.fill();

    // Fish tail
    ctx.beginPath();
    ctx.moveTo(size * 0.8, 0);
    ctx.lineTo(size * 1.2, -size * 0.3);
    ctx.lineTo(size * 1.2, size * 0.3);
    ctx.closePath();
    ctx.fill();
  }

  private drawJellyfish(
    ctx: CanvasRenderingContext2D,
    marine: MarineLife
  ): void {
    const size = marine.size;
    const pulse = Math.sin(marine.animationPhase) * 0.1 + 1;

    // Jellyfish bell
    ctx.beginPath();
    ctx.arc(0, 0, size * 0.5 * pulse, 0, Math.PI * 2);
    ctx.fill();

    // Tentacles
    ctx.lineWidth = 2;
    ctx.strokeStyle = marine.color;
    for (let i = 0; i < 4; i++) {
      const angle = (i / 4) * Math.PI * 2;
      const length = size * (0.8 + Math.sin(marine.animationPhase + i) * 0.2);
      ctx.beginPath();
      ctx.moveTo(Math.cos(angle) * size * 0.3, Math.sin(angle) * size * 0.3);
      ctx.lineTo(Math.cos(angle) * length, Math.sin(angle) * length);
      ctx.stroke();
    }
  }

  private drawSeaweed(ctx: CanvasRenderingContext2D, marine: MarineLife): void {
    const size = marine.size;
    const sway = Math.sin(marine.animationPhase) * 0.3;

    ctx.lineWidth = 4;
    ctx.strokeStyle = marine.color;
    ctx.lineCap = "round";

    // Seaweed stalk
    ctx.beginPath();
    ctx.moveTo(0, size);
    ctx.quadraticCurveTo(sway * 20, size * 0.5, sway * 30, 0);
    ctx.stroke();

    // Seaweed leaves
    for (let i = 0; i < 3; i++) {
      const y = size * (0.2 + i * 0.3);
      ctx.beginPath();
      ctx.ellipse(sway * (10 + i * 5), y, 8, 4, sway * 0.5, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  private drawParticles(
    ctx: CanvasRenderingContext2D,
    layerOpacity: number
  ): void {
    ctx.save();
    this.state.particles.forEach((particle) => {
      if (
        (layerOpacity > 0.5 && particle.size > 2) ||
        (layerOpacity <= 0.5 && particle.size <= 2)
      ) {
        ctx.globalAlpha = particle.opacity * layerOpacity;
        ctx.fillStyle = particle.color;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        ctx.fill();
      }
    });
    ctx.restore();
  }

  setQuality(quality: QualityLevel): void {
    this.quality = quality;
    // Reinitialize with new quality settings if needed
  }

  setAccessibility(settings: AccessibilitySettings): void {
    this.accessibility = { ...this.accessibility, ...settings };
  }

  cleanup(): void {
    this.state.bubbles = [];
    this.state.marineLife = [];
    this.state.particles = [];
    this.state.lightRays = [];
  }

  getMetrics(): PerformanceMetrics {
    const totalParticles =
      this.state.bubbles.length +
      this.state.marineLife.length +
      this.state.particles.length;

    return {
      fps: 60, // Estimated
      warnings:
        totalParticles > 100
          ? ["High particle count may impact performance"]
          : [],
      particleCount: totalParticles,
      renderTime: 16, // Estimated 16ms for 60fps
    };
  }
}
