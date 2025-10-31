/**
 * Deep Ocean Background System
 *
 * Creates an immersive underwater environment with:
 * - Floating bubbles with realistic physics
 * - Marine life (fish sprites, jellyfish)
 * - Particle effects for depth
 * - Dynamic light rays from surface
 * - Ocean gradient background
 */

import type {
  AccessibilitySettings,
  Dimensions,
  IBackgroundSystem,
  PerformanceMetrics,
  QualityLevel,
} from "../../shared";
import type {
  Bubble,
  DeepOceanState,
  FishMarineLife,
  FishSprite,
  JellyfishMarineLife,
  MarineLife,
  MarineLifeType,
  OceanParticle,
} from "../domain/models/DeepOceanModels";

export class DeepOceanBackgroundSystem implements IBackgroundSystem {
  private state: DeepOceanState;
  private quality: QualityLevel = "medium";
  private accessibility: AccessibilitySettings = {
    reducedMotion: false,
    highContrast: false,
    visibleParticleSize: 1,
  };
  private animationTime = 0;
  private readonly fishSprites: FishSprite[] = [
    { name: "Blue", path: "/assets/background/fish/kenney/fish_blue.png" },
    { name: "Orange", path: "/assets/background/fish/kenney/fish_orange.png" },
    { name: "Green", path: "/assets/background/fish/kenney/fish_green.png" },
    {
      name: "Grey Long",
      path: "/assets/background/fish/kenney/fish_grey_long_a.png",
    },
  ];
  private fishSpriteCache = new Map<
    string,
    { sprite: FishSprite; image: HTMLImageElement; ready: boolean }
  >();

  constructor() {
    this.state = {
      bubbles: [],
      marineLife: [],
      particles: [],
      currentGradient: {
        top: "#0d2d47", // Rich ocean blue
        bottom: "#091a2b", // Darker ocean depth
      },
      lightRays: [],
      pendingSpawns: [],
    };

    this.preloadFishSprites();
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

    // Pre-populate: Distribute elements across viewport so animation appears already running
    // Spread bubbles across full height (instead of starting at bottom)
    this.state.bubbles.forEach((bubble) => {
      bubble.y = Math.random() * dimensions.height;
    });

    // Spread particles across full height
    this.state.particles.forEach((particle) => {
      particle.y = Math.random() * dimensions.height;
    });

    // Randomize animation time so light rays appear mid-animation
    this.animationTime = Math.random() * 1000;

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
    const total = this.getMarineLifeCount();
    const fishCount = Math.max(2, Math.round(total * 0.65));
    const jellyCount = Math.max(1, total - fishCount);

    const school: MarineLife[] = [];
    for (let i = 0; i < fishCount; i++) {
      school.push(this.createFish(dimensions));
    }
    for (let i = 0; i < jellyCount; i++) {
      school.push(this.createJellyfish(dimensions));
    }

    this.state.marineLife = school;
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
        opacity: 0.08 + Math.random() * 0.1, // Subtler but visible: 0.08-0.18
        width: 20 + Math.random() * 40,
        angle: -5 + Math.random() * 10,
        phase: Math.random() * Math.PI * 2,
        speed: 0.003 + Math.random() * 0.004, // Slower: 0.003-0.007 instead of 0.006-0.012
      });
    }
  }

  private createBubble(dimensions: Dimensions): Bubble {
    return {
      x: Math.random() * dimensions.width,
      y: dimensions.height + Math.random() * 100,
      radius: 2 + Math.random() * 5, // Moderately smaller bubbles: 2-7 instead of 2-10
      speed: 0.2 + Math.random() * 0.6, // Much slower: 0.2-0.8 instead of 0.5-2.5
      sway: 0.3 + Math.random() * 0.8, // Gentler sway: 0.3-1.1 instead of 0.5-2
      opacity: 0.3 + Math.random() * 0.4,
      swayOffset: Math.random() * Math.PI * 2,
      startY: dimensions.height + Math.random() * 100,
    };
  }

  private preloadFishSprites(): void {
    if (typeof window === "undefined") return;

    this.fishSprites.forEach((sprite) => {
      if (this.fishSpriteCache.has(sprite.path)) return;

      const image = new Image();
      const cacheEntry = { sprite, image, ready: image.complete };

      image.onload = () => {
        this.fishSpriteCache.set(sprite.path, {
          sprite,
          image,
          ready: true,
        });
      };

      image.onerror = () => {
        console.warn(`Failed to load fish sprite: ${sprite.path}`);
        this.fishSpriteCache.delete(sprite.path);
      };

      image.src = sprite.path;
      this.fishSpriteCache.set(sprite.path, cacheEntry);
    });
  }

  private getRandomFishSpriteEntry() {
    if (this.fishSprites.length === 0) return undefined;
    const sprite =
      this.fishSprites[Math.floor(Math.random() * this.fishSprites.length)];
    const entry = this.fishSpriteCache.get(sprite.path);
    return entry ?? undefined;
  }

  private createFish(dimensions: Dimensions): FishMarineLife {
    const entry = this.getRandomFishSpriteEntry();
    const sprite = entry?.sprite ?? this.fishSprites[0];
    const direction: 1 | -1 = Math.random() > 0.5 ? 1 : -1;
    const baseWidth = entry?.image?.naturalWidth ?? 96;
    const baseHeight = entry?.image?.naturalHeight ?? 64;
    const scale = 0.35 + Math.random() * 0.25; // Moderately smaller: 35-60% instead of 55-90%
    const width = baseWidth * scale;
    const height = baseHeight * scale;
    const depthBand = {
      min: 90,
      max: Math.max(240, dimensions.height - 180),
    };
    const maxOffset = Math.max(140, dimensions.width * 0.2);

    const startX =
      direction === 1
        ? -width - Math.random() * maxOffset
        : dimensions.width + width + Math.random() * maxOffset;
    const baseY =
      depthBand.min +
      Math.random() * Math.max(60, depthBand.max - depthBand.min);

    return {
      type: "fish",
      sprite,
      image: entry?.image,
      width,
      height,
      direction,
      speed: 12 + Math.random() * 15, // Much slower: 12-27 instead of 35-80
      verticalDrift: (Math.random() - 0.5) * 6, // Gentler drift: ±3 instead of ±9
      bobAmplitude: 3 + Math.random() * 4, // Subtler bob: 3-7 instead of 6-15
      bobSpeed: 0.01 + Math.random() * 0.015, // Slower bob: 0.01-0.025 instead of 0.02-0.05
      depthBand,
      x: startX,
      baseY,
      y: baseY,
      opacity: 0.35 + Math.random() * 0.15,
      animationPhase: Math.random() * Math.PI * 2,
    };
  }

  private createJellyfish(dimensions: Dimensions): JellyfishMarineLife {
    const size = 18 + Math.random() * 15; // Moderately smaller: 18-33px instead of 28-52px
    const baseY =
      dimensions.height * 0.25 + Math.random() * (dimensions.height * 0.45);
    const tentacleSeeds = Array.from(
      { length: 5 + Math.floor(Math.random() * 3) },
      () => Math.random() * Math.PI * 2
    );

    return {
      type: "jellyfish",
      size,
      color: this.getMarineLifeColor("jellyfish"),
      horizontalSpeed: (Math.random() - 0.5) * 8, // Slower: ±4 instead of ±10
      verticalSpeed: -6 - Math.random() * 6, // Slower upward: -6 to -12 instead of -18 to -32
      waveAmplitude: 4 + Math.random() * 4, // Gentler wave: 4-8 instead of 10-18
      waveFrequency: 0.008 + Math.random() * 0.012, // Slower wave: 0.008-0.02 instead of 0.015-0.04
      glowIntensity: 0.15 + Math.random() * 0.15, // Subtler glow: 0.15-0.3 instead of 0.35-0.65
      tentacleSeeds,
      baseY,
      x: 60 + Math.random() * (dimensions.width - 120),
      y: baseY,
      opacity: 0.45 + Math.random() * 0.35,
      animationPhase: Math.random() * Math.PI * 2,
    };
  }

  private createParticle(dimensions: Dimensions): OceanParticle {
    return {
      x: Math.random() * dimensions.width,
      y: Math.random() * dimensions.height,
      vx: (Math.random() - 0.5) * 0.2, // Slower horizontal: ±0.1 instead of ±0.25
      vy: -0.05 - Math.random() * 0.15, // Slower upward: -0.05 to -0.2 instead of -0.1 to -0.4
      size: 0.8 + Math.random() * 2, // Smaller: 0.8-2.8 instead of 1-4
      opacity: 0.15 + Math.random() * 0.25, // More subtle opacity for dark particles
      color: this.getParticleColor(),
      life: 0,
      maxLife: 100 + Math.random() * 200,
    };
  }

  private getMarineLifeColor(type: "fish" | "jellyfish"): string {
    if (type === "fish") {
      // Ocean fish in nice teals and blues
      return ["#3d7a8c", "#4a8fa3", "#548da0", "#4b8599"][
        Math.floor(Math.random() * 4)
      ];
    }

    // Jellyfish in soft purples and pinks
    return ["#7d5a7a", "#8b6d88", "#946f91", "#866783"][
      Math.floor(Math.random() * 4)
    ];
  }

  private getParticleColor(): string {
    // Light, visible particles in ocean water
    const colors = ["#a8d5e2", "#b3dde8", "#9ec9d8", "#aad3df"];
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
        return 2;
      case "medium":
        return 2;
      case "low":
        return 1;
      case "minimal":
        return 1;
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

  update(dimensions: Dimensions, frameMultiplier: number = 1.0): void {
    this.animationTime += 0.016 * frameMultiplier; // Normalize to 60fps equivalent

    const motionFactor = this.accessibility.reducedMotion ? 0.25 : 1;
    const adjustedFrame = frameMultiplier * motionFactor;

    // Update bubbles
    this.updateBubbles(dimensions, adjustedFrame);

    // Update marine life
    this.updateMarineLife(dimensions, adjustedFrame);

    // Check and spawn pending marine life
    this.processPendingSpawns(dimensions);

    // Update particles
    this.updateParticles(dimensions, adjustedFrame);

    // Update light rays
    this.updateLightRays(adjustedFrame);
  }

  private updateBubbles(
    dimensions: Dimensions,
    frameMultiplier: number = 1.0
  ): void {
    for (let i = this.state.bubbles.length - 1; i >= 0; i--) {
      const bubble = this.state.bubbles[i];

      // Update position
      bubble.y -= bubble.speed * frameMultiplier;
      bubble.x +=
        Math.sin(this.animationTime * bubble.sway + bubble.swayOffset) *
        0.5 *
        frameMultiplier;

      // Remove if off screen and create new one
      if (bubble.y < -bubble.radius * 2) {
        this.state.bubbles[i] = this.createBubble(dimensions);
      }
    }
  }

  private updateMarineLife(
    dimensions: Dimensions,
    frameMultiplier: number = 1.0
  ): void {
    for (let i = this.state.marineLife.length - 1; i >= 0; i--) {
      const marine = this.state.marineLife[i];

      switch (marine.type) {
        case "fish": {
          const fish = marine as FishMarineLife;
          const deltaSeconds = 0.016 * frameMultiplier;
          fish.animationPhase += fish.bobSpeed * frameMultiplier;
          fish.x += fish.direction * fish.speed * deltaSeconds;
          fish.baseY += fish.verticalDrift * deltaSeconds;
          fish.baseY = Math.max(
            fish.depthBand.min,
            Math.min(fish.depthBand.max, fish.baseY)
          );
          const bob = Math.sin(fish.animationPhase) * fish.bobAmplitude;
          fish.y = fish.baseY + bob;

          const offRight =
            fish.direction === 1 &&
            fish.x > dimensions.width + fish.width * 1.5;
          const offLeft = fish.direction === -1 && fish.x < -fish.width * 1.5;

          if (offRight || offLeft) {
            // Remove fish and schedule a new spawn with delay
            this.state.marineLife.splice(i, 1);
            this.scheduleMarineLifeSpawn("fish");
          }
          break;
        }
        case "jellyfish": {
          const jelly = marine as JellyfishMarineLife;
          const deltaSeconds = 0.016 * frameMultiplier;
          jelly.animationPhase += jelly.waveFrequency * frameMultiplier;
          jelly.x += jelly.horizontalSpeed * deltaSeconds;
          jelly.baseY += jelly.verticalSpeed * deltaSeconds;
          jelly.y =
            jelly.baseY + Math.sin(jelly.animationPhase) * jelly.waveAmplitude;

          const wrappedLeft = jelly.x < -jelly.size * 2;
          const wrappedRight = jelly.x > dimensions.width + jelly.size * 2;
          const wrappedTop = jelly.y < -jelly.size * 2;
          const wrappedBottom = jelly.y > dimensions.height + jelly.size * 2;

          if (wrappedLeft || wrappedRight || wrappedTop || wrappedBottom) {
            // Remove jellyfish and schedule a new spawn with delay
            this.state.marineLife.splice(i, 1);
            this.scheduleMarineLifeSpawn("jellyfish");
          }
          break;
        }
      }
    }
  }

  private updateParticles(
    dimensions: Dimensions,
    frameMultiplier: number = 1.0
  ): void {
    for (let i = this.state.particles.length - 1; i >= 0; i--) {
      const particle = this.state.particles[i];

      // Update position
      particle.x += particle.vx * frameMultiplier;
      particle.y += particle.vy * frameMultiplier;
      particle.life += frameMultiplier;

      // Update opacity based on life
      particle.opacity = Math.max(0, 1 - particle.life / particle.maxLife);

      // Remove if dead and create new one
      if (particle.life >= particle.maxLife || particle.y < -10) {
        this.state.particles[i] = this.createParticle(dimensions);
      }
    }
  }

  private updateLightRays(frameMultiplier: number = 1.0): void {
    const motionScale = this.accessibility.reducedMotion ? 0.3 : 1;
    this.state.lightRays.forEach((ray) => {
      ray.phase += ray.speed * frameMultiplier;
      const sway = Math.sin(ray.phase * 0.65) * motionScale;
      ray.opacity = 0.05 + Math.sin(ray.phase) * 0.05 * motionScale;
      ray.angle = -4 + sway * 8;
    });
  }

  private scheduleMarineLifeSpawn(type: MarineLifeType): void {
    // Schedule spawn with 3-5 second delay
    const delaySeconds = 3 + Math.random() * 2;
    const spawnTime = this.animationTime + delaySeconds;
    this.state.pendingSpawns.push({ type, spawnTime });
  }

  private processPendingSpawns(dimensions: Dimensions): void {
    // Check if any pending spawns are ready
    for (let i = this.state.pendingSpawns.length - 1; i >= 0; i--) {
      const spawn = this.state.pendingSpawns[i];
      if (this.animationTime >= spawn.spawnTime) {
        // Spawn the marine life
        if (spawn.type === "fish") {
          this.state.marineLife.push(this.createFish(dimensions));
        } else if (spawn.type === "jellyfish") {
          this.state.marineLife.push(this.createJellyfish(dimensions));
        }
        // Remove from pending spawns
        this.state.pendingSpawns.splice(i, 1);
      }
    }
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
    gradient.addColorStop(0, this.state.currentGradient.top); // #0d2d47 - Rich ocean blue
    gradient.addColorStop(0.25, "#0f3854"); // Medium-light ocean
    gradient.addColorStop(0.5, "#0b2a42"); // Mid ocean
    gradient.addColorStop(0.75, "#0a2136"); // Deeper ocean
    gradient.addColorStop(1, this.state.currentGradient.bottom); // #091a2b - Ocean depth

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

      // Gentle, visible light rays filtering through water
      gradient.addColorStop(0, `rgba(100, 150, 180, ${ray.opacity})`);
      gradient.addColorStop(0.3, `rgba(70, 120, 150, ${ray.opacity * 0.6})`);
      gradient.addColorStop(1, "rgba(40, 90, 120, 0)");

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
      // Nice visible bubbles
      ctx.fillStyle = `rgba(200, 230, 245, 0.5)`;
      ctx.fill();

      // Bright highlight
      ctx.beginPath();
      ctx.arc(
        bubble.x - bubble.radius * 0.3,
        bubble.y - bubble.radius * 0.3,
        bubble.radius * 0.3,
        0,
        Math.PI * 2
      );
      ctx.fillStyle = `rgba(240, 250, 255, 0.7)`;
      ctx.fill();
    });
    ctx.restore();
  }

  private drawMarineLife(ctx: CanvasRenderingContext2D): void {
    ctx.save();
    this.state.marineLife.forEach((marine) => {
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

    const cacheEntry = this.fishSpriteCache.get(fish.sprite.path);
    const image = cacheEntry?.image ?? fish.image;
    const ready = cacheEntry?.ready ?? image?.complete ?? false;

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

  private lightenColor(color: string, amount: number): string {
    return this.adjustColor(color, Math.abs(amount));
  }

  private darkenColor(color: string, amount: number): string {
    return this.adjustColor(color, -Math.abs(amount));
  }

  private adjustColor(color: string, amount: number): string {
    let hex = color.replace("#", "");
    if (hex.length === 3) {
      hex = hex
        .split("")
        .map((c) => c + c)
        .join("");
    }

    const num = parseInt(hex, 16);
    let r = (num >> 16) & 0xff;
    let g = (num >> 8) & 0xff;
    let b = num & 0xff;

    const delta = Math.round(255 * amount);
    r = Math.min(255, Math.max(0, r + delta));
    g = Math.min(255, Math.max(0, g + delta));
    b = Math.min(255, Math.max(0, b + delta));

    return (
      "#" +
      [r, g, b].map((channel) => channel.toString(16).padStart(2, "0")).join("")
    );
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
    this.state.pendingSpawns = [];
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
