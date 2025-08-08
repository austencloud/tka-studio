// Enhanced Canvas 2D background system with rich animations
// SSR-safe implementation with beautiful visual effects

import { browser } from '$app/environment';

export type BackgroundType = 'snowfall' | 'nightSky' | 'deepOcean' | 'static';
export type QualityLevel = 'high' | 'medium' | 'low';

interface Dimensions {
  width: number;
  height: number;
}

// Base particle interface
interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  opacity: number;
  color: string;
  life: number;
  maxLife: number;
}

// Specialized particle types
interface Star extends Particle {
  twinkleSpeed: number;
  twinklePhase: number;
  brightness: number;
}

interface Snowflake extends Particle {
  rotation: number;
  rotationSpeed: number;
  drift: number;
}

interface Fish extends Particle {
  angle: number;
  speed: number;
  turnSpeed: number;
  bodyLength: number;
  tailOffset: number;
}

interface Bubble extends Particle {
  wobble: number;
  wobbleSpeed: number;
}

export class EnhancedBackgroundSystem {
  private canvas: HTMLCanvasElement | null = null;
  private ctx: CanvasRenderingContext2D | null = null;
  private animationId: number | null = null;
  private lastTime = 0;
  private isActive = true;

  // Background-specific particles
  private stars: Star[] = [];
  private snowflakes: Snowflake[] = [];
  private fish: Fish[] = [];
  private bubbles: Bubble[] = [];
  private shootingStars: Star[] = [];

  // Configuration
  private backgroundType: BackgroundType = 'nightSky';
  private quality: QualityLevel = 'medium';
  private dimensions: Dimensions = { width: 0, height: 0 };

  constructor(backgroundType: BackgroundType = 'nightSky', quality: QualityLevel = 'medium') {
    this.backgroundType = backgroundType;
    this.quality = quality;
  }

  public initialize(canvas: HTMLCanvasElement, dimensions: Dimensions): void {
    if (!browser) return;

    console.log(`🎨 EnhancedBackgroundSystem: Initializing ${this.backgroundType} background`, dimensions);

    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.dimensions = { ...dimensions };

    if (this.ctx) {
      this.initializeParticles();
      this.startAnimation();
      console.log(`✨ EnhancedBackgroundSystem: ${this.backgroundType} animation started!`);
    }
  }

  public setBackgroundType(type: BackgroundType): void {
    this.backgroundType = type;
    this.initializeParticles();
  }

  public setQuality(quality: QualityLevel): void {
    this.quality = quality;
    this.initializeParticles();
  }

  public updateDimensions(dimensions: Dimensions): void {
    this.dimensions = { ...dimensions };
    if (this.canvas) {
      this.canvas.width = dimensions.width;
      this.canvas.height = dimensions.height;
    }
    this.initializeParticles();
  }

  public cleanup(): void {
    this.isActive = false;
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  private initializeParticles(): void {
    if (!this.dimensions.width || !this.dimensions.height) return;

    const qualityMultiplier = this.quality === 'high' ? 1 : this.quality === 'medium' ? 0.7 : 0.4;

    // Clear all particles
    this.stars = [];
    this.snowflakes = [];
    this.fish = [];
    this.bubbles = [];
    this.shootingStars = [];

    switch (this.backgroundType) {
      case 'nightSky':
        this.initializeNightSky(qualityMultiplier);
        break;
      case 'snowfall':
        this.initializeSnowfall(qualityMultiplier);
        break;
      case 'deepOcean':
        this.initializeDeepOcean(qualityMultiplier);
        break;
    }
  }

  private initializeNightSky(qualityMultiplier: number): void {
    const starCount = Math.floor(150 * qualityMultiplier);
    console.log(`🌟 Creating ${starCount} stars for night sky`);

    // Create twinkling stars
    for (let i = 0; i < starCount; i++) {
      this.stars.push({
        x: Math.random() * this.dimensions.width,
        y: Math.random() * this.dimensions.height,
        vx: (Math.random() - 0.5) * 0.1,
        vy: (Math.random() - 0.5) * 0.1,
        size: Math.random() * 2 + 0.5,
        opacity: Math.random() * 0.8 + 0.2,
        color: ['#FFFFFF', '#E0E0FF', '#FFDDEE', '#D0E0FF'][Math.floor(Math.random() * 4)],
        life: 0,
        maxLife: 1000,
        twinkleSpeed: Math.random() * 0.02 + 0.01,
        twinklePhase: Math.random() * Math.PI * 2,
        brightness: Math.random() * 0.5 + 0.5
      });
    }

    // Create occasional shooting stars
    if (this.quality !== 'low') {
      for (let i = 0; i < 2; i++) {
        this.createShootingStar();
      }
    }
  }

  private initializeSnowfall(qualityMultiplier: number): void {
    const snowflakeCount = Math.floor(80 * qualityMultiplier);

    for (let i = 0; i < snowflakeCount; i++) {
      this.snowflakes.push({
        x: Math.random() * this.dimensions.width,
        y: Math.random() * this.dimensions.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: Math.random() * 2 + 0.5,
        size: Math.random() * 4 + 2,
        opacity: Math.random() * 0.6 + 0.4,
        color: ['#FFFFFF', '#E2E8F0', '#CBD5E0'][Math.floor(Math.random() * 3)],
        life: 0,
        maxLife: 1000,
        rotation: Math.random() * Math.PI * 2,
        rotationSpeed: (Math.random() - 0.5) * 0.02,
        drift: (Math.random() - 0.5) * 0.3
      });
    }
  }

  private initializeDeepOcean(qualityMultiplier: number): void {
    const fishCount = Math.floor(8 * qualityMultiplier);
    const bubbleCount = Math.floor(25 * qualityMultiplier);

    // Create swimming fish
    for (let i = 0; i < fishCount; i++) {
      this.fish.push({
        x: Math.random() * this.dimensions.width,
        y: Math.random() * this.dimensions.height,
        vx: 0,
        vy: 0,
        size: Math.random() * 15 + 10,
        opacity: Math.random() * 0.4 + 0.6,
        color: ['#87CEEB', '#B0E0E6', '#AFEEEE', '#E0FFFF'][Math.floor(Math.random() * 4)],
        life: 0,
        maxLife: 1000,
        angle: Math.random() * Math.PI * 2,
        speed: Math.random() * 0.5 + 0.3,
        turnSpeed: (Math.random() - 0.5) * 0.02,
        bodyLength: Math.random() * 20 + 15,
        tailOffset: 0
      });
    }

    // Create floating bubbles
    for (let i = 0; i < bubbleCount; i++) {
      this.bubbles.push({
        x: Math.random() * this.dimensions.width,
        y: Math.random() * this.dimensions.height,
        vx: (Math.random() - 0.5) * 0.2,
        vy: -(Math.random() * 1 + 0.5),
        size: Math.random() * 8 + 3,
        opacity: Math.random() * 0.3 + 0.2,
        color: '#87CEEB',
        life: 0,
        maxLife: 1000,
        wobble: 0,
        wobbleSpeed: Math.random() * 0.03 + 0.01
      });
    }
  }

  private createShootingStar(): void {
    if (Math.random() < 0.001) { // Very rare
      this.shootingStars.push({
        x: -50,
        y: Math.random() * this.dimensions.height * 0.3,
        vx: Math.random() * 8 + 5,
        vy: Math.random() * 2 - 1,
        size: 2,
        opacity: 1,
        color: '#FFFF88',
        life: 0,
        maxLife: 100,
        twinkleSpeed: 0,
        twinklePhase: 0,
        brightness: 1
      });
    }
  }

  private startAnimation(): void {
    if (!this.isActive || !browser) return;

    const animate = (currentTime: number) => {
      if (!this.isActive || !this.ctx) return;

      const deltaTime = currentTime - this.lastTime;
      this.lastTime = currentTime;

      this.render(deltaTime);
      this.animationId = requestAnimationFrame(animate);
    };

    this.animationId = requestAnimationFrame(animate);
  }

  private render(deltaTime: number): void {
    if (!this.ctx || !this.dimensions.width || !this.dimensions.height) return;

    // Clear canvas
    this.ctx.clearRect(0, 0, this.dimensions.width, this.dimensions.height);

    // Draw gradient background
    this.drawGradient();

    // Update and draw based on background type
    switch (this.backgroundType) {
      case 'nightSky':
        this.updateAndDrawNightSky(deltaTime);
        break;
      case 'snowfall':
        this.updateAndDrawSnowfall(deltaTime);
        break;
      case 'deepOcean':
        this.updateAndDrawDeepOcean(deltaTime);
        break;
    }
  }

  private drawGradient(): void {
    if (!this.ctx) return;

    const gradients = {
      nightSky: [
        { position: 0, color: '#0A0E2C' },
        { position: 0.3, color: '#1A2151' },
        { position: 0.6, color: '#2A3270' },
        { position: 1, color: '#4A5490' }
      ],
      snowfall: [
        { position: 0, color: '#1a2332' },
        { position: 0.5, color: '#2d3748' },
        { position: 1, color: '#4a5568' }
      ],
      deepOcean: [
        { position: 0, color: '#001122' },
        { position: 0.3, color: '#002244' },
        { position: 0.7, color: '#003366' },
        { position: 1, color: '#004488' }
      ],
      static: [
        { position: 0, color: '#1a1a2e' },
        { position: 1, color: '#16213e' }
      ]
    };

    const gradient = this.ctx.createLinearGradient(0, 0, 0, this.dimensions.height);
    const stops = gradients[this.backgroundType] || gradients.static;

    stops.forEach(stop => {
      gradient.addColorStop(stop.position, stop.color);
    });

    this.ctx.fillStyle = gradient;
    this.ctx.fillRect(0, 0, this.dimensions.width, this.dimensions.height);
  }

  private updateAndDrawNightSky(deltaTime: number): void {
    if (!this.ctx) return;

    const dt = deltaTime * 0.016;

    // Update and draw twinkling stars
    this.stars.forEach(star => {
      star.life += deltaTime;
      star.twinklePhase += star.twinkleSpeed;
      star.opacity = star.brightness * (0.3 + 0.7 * (Math.sin(star.twinklePhase) + 1) / 2);

      // Slight drift
      star.x += star.vx * dt;
      star.y += star.vy * dt;

      // Wrap around
      if (star.x < 0) star.x = this.dimensions.width;
      if (star.x > this.dimensions.width) star.x = 0;
      if (star.y < 0) star.y = this.dimensions.height;
      if (star.y > this.dimensions.height) star.y = 0;
    });

    // Draw stars with glow effect
    this.stars.forEach(star => {
      this.ctx!.save();
      this.ctx!.globalAlpha = star.opacity;

      // Create glow effect for brighter stars
      if (star.size > 1.5) {
        this.ctx!.shadowColor = star.color;
        this.ctx!.shadowBlur = star.size * 2;
      }

      this.ctx!.fillStyle = star.color;
      this.ctx!.beginPath();
      this.ctx!.arc(star.x, star.y, star.size, 0, Math.PI * 2);
      this.ctx!.fill();
      this.ctx!.restore();
    });

    // Update and draw shooting stars
    this.shootingStars = this.shootingStars.filter(star => {
      star.x += star.vx * dt;
      star.y += star.vy * dt;
      star.life += deltaTime;
      star.opacity = Math.max(0, 1 - star.life / star.maxLife);

      if (star.opacity > 0 && star.x < this.dimensions.width + 100) {
        // Draw shooting star with trail
        this.ctx!.save();
        this.ctx!.globalAlpha = star.opacity;
        this.ctx!.strokeStyle = star.color;
        this.ctx!.lineWidth = 2;
        this.ctx!.shadowColor = star.color;
        this.ctx!.shadowBlur = 10;

        this.ctx!.beginPath();
        this.ctx!.moveTo(star.x - star.vx * 5, star.y - star.vy * 5);
        this.ctx!.lineTo(star.x, star.y);
        this.ctx!.stroke();
        this.ctx!.restore();

        return true;
      }
      return false;
    });

    // Occasionally create new shooting stars
    this.createShootingStar();
  }

  private updateAndDrawSnowfall(deltaTime: number): void {
    if (!this.ctx) return;

    const dt = deltaTime * 0.016;

    // Update snowflakes
    this.snowflakes.forEach(snowflake => {
      snowflake.x += (snowflake.vx + snowflake.drift * Math.sin(snowflake.life * 0.001)) * dt;
      snowflake.y += snowflake.vy * dt;
      snowflake.rotation += snowflake.rotationSpeed * dt;
      snowflake.life += deltaTime;

      // Reset snowflake when it goes off screen
      if (snowflake.y > this.dimensions.height + 10) {
        snowflake.y = -10;
        snowflake.x = Math.random() * this.dimensions.width;
      }
      if (snowflake.x < -10) snowflake.x = this.dimensions.width + 10;
      if (snowflake.x > this.dimensions.width + 10) snowflake.x = -10;
    });

    // Draw snowflakes
    this.snowflakes.forEach(snowflake => {
      this.ctx!.save();
      this.ctx!.globalAlpha = snowflake.opacity;
      this.ctx!.translate(snowflake.x, snowflake.y);
      this.ctx!.rotate(snowflake.rotation);

      // Draw snowflake shape
      this.ctx!.strokeStyle = snowflake.color;
      this.ctx!.lineWidth = 1;
      this.ctx!.beginPath();

      // Simple 6-pointed snowflake
      for (let i = 0; i < 6; i++) {
        this.ctx!.moveTo(0, 0);
        this.ctx!.lineTo(0, -snowflake.size);
        this.ctx!.rotate(Math.PI / 3);
      }

      this.ctx!.stroke();
      this.ctx!.restore();
    });
  }

  private updateAndDrawDeepOcean(deltaTime: number): void {
    if (!this.ctx) return;

    const dt = deltaTime * 0.016;

    // Update fish
    this.fish.forEach(fish => {
      fish.angle += fish.turnSpeed * dt;
      fish.vx = Math.cos(fish.angle) * fish.speed;
      fish.vy = Math.sin(fish.angle) * fish.speed;

      fish.x += fish.vx * dt;
      fish.y += fish.vy * dt;
      fish.tailOffset += deltaTime * 0.01;

      // Boundary behavior - turn around when hitting edges
      if (fish.x < 0 || fish.x > this.dimensions.width) {
        fish.angle = Math.PI - fish.angle;
      }
      if (fish.y < 0 || fish.y > this.dimensions.height) {
        fish.angle = -fish.angle;
      }

      // Keep fish in bounds
      fish.x = Math.max(0, Math.min(this.dimensions.width, fish.x));
      fish.y = Math.max(0, Math.min(this.dimensions.height, fish.y));
    });

    // Draw fish
    this.fish.forEach(fish => {
      this.ctx!.save();
      this.ctx!.globalAlpha = fish.opacity;
      this.ctx!.translate(fish.x, fish.y);
      this.ctx!.rotate(fish.angle);

      // Draw fish body
      this.ctx!.fillStyle = fish.color;
      this.ctx!.beginPath();
      this.ctx!.ellipse(0, 0, fish.size, fish.size * 0.6, 0, 0, Math.PI * 2);
      this.ctx!.fill();

      // Draw tail
      const tailX = -fish.size * 1.2;
      const tailY = Math.sin(fish.tailOffset) * fish.size * 0.3;
      this.ctx!.beginPath();
      this.ctx!.moveTo(tailX, 0);
      this.ctx!.lineTo(tailX - fish.size * 0.5, tailY - fish.size * 0.3);
      this.ctx!.lineTo(tailX - fish.size * 0.5, tailY + fish.size * 0.3);
      this.ctx!.closePath();
      this.ctx!.fill();

      this.ctx!.restore();
    });

    // Update bubbles
    this.bubbles.forEach(bubble => {
      bubble.wobble += bubble.wobbleSpeed * dt;
      bubble.x += (bubble.vx + Math.sin(bubble.wobble) * 0.5) * dt;
      bubble.y += bubble.vy * dt;
      bubble.life += deltaTime;

      // Reset bubble when it reaches surface
      if (bubble.y < -10) {
        bubble.y = this.dimensions.height + 10;
        bubble.x = Math.random() * this.dimensions.width;
      }
    });

    // Draw bubbles
    this.bubbles.forEach(bubble => {
      this.ctx!.save();
      this.ctx!.globalAlpha = bubble.opacity;
      this.ctx!.strokeStyle = bubble.color;
      this.ctx!.lineWidth = 1;
      this.ctx!.beginPath();
      this.ctx!.arc(bubble.x, bubble.y, bubble.size, 0, Math.PI * 2);
      this.ctx!.stroke();
      this.ctx!.restore();
    });
  }
}
