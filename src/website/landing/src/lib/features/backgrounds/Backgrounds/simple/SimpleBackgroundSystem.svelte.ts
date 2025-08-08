// src/lib/components/Backgrounds/simple/SimpleBackgroundSystem.svelte.ts
// Lightweight Canvas 2D background system to replace Three.js implementation
// Eliminates Svelte 5 reactive loop issues while maintaining visual appeal

import type { Dimensions } from '../types/types.js';

export type BackgroundType = 'snowfall' | 'nightSky' | 'deepOcean' | 'static';
export type QualityLevel = 'high' | 'medium' | 'low';

interface Particle {
	x: number;
	y: number;
	vx: number;
	vy: number;
	size: number;
	opacity: number;
	color: string;
	life?: number;
	maxLife?: number;
}

interface BackgroundConfig {
	gradient: { position: number; color: string }[];
	particles: {
		count: number;
		minSize: number;
		maxSize: number;
		colors: string[];
		speed: { min: number; max: number };
		opacity: { min: number; max: number };
	};
	effects?: {
		twinkle?: boolean;
		drift?: boolean;
		fade?: boolean;
	};
}

const BACKGROUND_CONFIGS: Record<BackgroundType, BackgroundConfig> = {
	snowfall: {
		gradient: [
			{ position: 0, color: '#1a2332' },
			{ position: 0.5, color: '#2d3748' },
			{ position: 1, color: '#4a5568' }
		],
		particles: {
			count: 50,
			minSize: 2,
			maxSize: 6,
			colors: ['#FFFFFF', '#E2E8F0', '#CBD5E0'],
			speed: { min: 0.5, max: 2 },
			opacity: { min: 0.3, max: 0.8 }
		},
		effects: { drift: true, fade: true }
	},
	nightSky: {
		gradient: [
			{ position: 0, color: '#0A0E2C' },
			{ position: 0.3, color: '#1A2151' },
			{ position: 0.6, color: '#2A3270' },
			{ position: 1, color: '#4A5490' }
		],
		particles: {
			count: 80,
			minSize: 1,
			maxSize: 3,
			colors: ['#FFFFFF', '#E0E0FF', '#FFDDEE', '#D0E0FF'],
			speed: { min: 0, max: 0.1 },
			opacity: { min: 0.4, max: 1.0 }
		},
		effects: { twinkle: true }
	},
	deepOcean: {
		gradient: [
			{ position: 0, color: '#001122' },
			{ position: 0.3, color: '#002244' },
			{ position: 0.7, color: '#003366' },
			{ position: 1, color: '#004488' }
		],
		particles: {
			count: 30,
			minSize: 3,
			maxSize: 8,
			colors: ['#87CEEB', '#B0E0E6', '#AFEEEE', '#E0FFFF'],
			speed: { min: 0.2, max: 1.0 },
			opacity: { min: 0.2, max: 0.6 }
		},
		effects: { drift: true, fade: true }
	},
	static: {
		gradient: [
			{ position: 0, color: '#1a1a2e' },
			{ position: 1, color: '#16213e' }
		],
		particles: { count: 0, minSize: 0, maxSize: 0, colors: [], speed: { min: 0, max: 0 }, opacity: { min: 0, max: 0 } }
	}
};

export class SimpleBackgroundSystem {
	private canvas: HTMLCanvasElement | null = null;
	private ctx: CanvasRenderingContext2D | null = null;
	private animationId: number | null = null;
	private particles: Particle[] = [];
	private lastTime = 0;

	// Non-reactive state - captured once to avoid Svelte reactivity issues
	private config!: BackgroundConfig;
	private dimensions: Dimensions;
	private quality: QualityLevel;
	private isActive = true;

	constructor(
		backgroundType: BackgroundType = 'nightSky',
		quality: QualityLevel = 'medium'
	) {
		this.quality = quality;
		this.dimensions = { width: 0, height: 0 };
		this.setBackgroundType(backgroundType);
	}

	public initialize(canvas: HTMLCanvasElement, dimensions: Dimensions): void {
		this.canvas = canvas;
		this.ctx = canvas.getContext('2d');
		this.dimensions = { ...dimensions };

		if (this.ctx && this.config) {
			this.initializeParticles();
			this.startAnimation();
		}
	}

	public setBackgroundType(type: BackgroundType): void {
		if (!BACKGROUND_CONFIGS[type]) {
			console.warn(`Invalid background type: ${type}, falling back to nightSky`);
			type = 'nightSky';
		}
		this.config = BACKGROUND_CONFIGS[type];
		if (this.dimensions.width > 0 && this.dimensions.height > 0) {
			this.initializeParticles();
		}
	}

	public setQuality(quality: QualityLevel): void {
		this.quality = quality;
		this.initializeParticles();
	}

	public updateDimensions(dimensions: Dimensions): void {
		this.dimensions = { ...dimensions }; // Create non-reactive copy
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
		const particleCount = Math.floor(this.config.particles.count * qualityMultiplier);

		this.particles = [];

		for (let i = 0; i < particleCount; i++) {
			this.particles.push(this.createParticle());
		}
	}

	private createParticle(): Particle {
		const { particles } = this.config;

		return {
			x: Math.random() * this.dimensions.width,
			y: Math.random() * this.dimensions.height,
			vx: (Math.random() - 0.5) * (particles.speed.max - particles.speed.min) + particles.speed.min,
			vy: Math.random() * (particles.speed.max - particles.speed.min) + particles.speed.min,
			size: Math.random() * (particles.maxSize - particles.minSize) + particles.minSize,
			opacity: Math.random() * (particles.opacity.max - particles.opacity.min) + particles.opacity.min,
			color: particles.colors[Math.floor(Math.random() * particles.colors.length)],
			life: Math.random() * 1000,
			maxLife: 1000
		};
	}

	private startAnimation(): void {
		if (!this.isActive) return;

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

		// Update and draw particles
		this.updateParticles(deltaTime);
		this.drawParticles();
	}

	private drawGradient(): void {
		if (!this.ctx) return;

		const gradient = this.ctx.createLinearGradient(0, 0, 0, this.dimensions.height);

		this.config.gradient.forEach(stop => {
			gradient.addColorStop(stop.position, stop.color);
		});

		this.ctx.fillStyle = gradient;
		this.ctx.fillRect(0, 0, this.dimensions.width, this.dimensions.height);
	}

	private updateParticles(deltaTime: number): void {
		const dt = deltaTime * 0.016; // Normalize to ~60fps

		this.particles.forEach(particle => {
			// Update position
			particle.x += particle.vx * dt;
			particle.y += particle.vy * dt;

			// Handle effects
			if (this.config.effects?.twinkle && particle.life !== undefined) {
				particle.life += deltaTime;
				particle.opacity = 0.5 + 0.5 * Math.sin(particle.life * 0.005);
			}

			if (this.config.effects?.fade && particle.life !== undefined && particle.maxLife !== undefined) {
				particle.life += deltaTime;
				if (particle.life > particle.maxLife) {
					// Reset particle
					Object.assign(particle, this.createParticle());
				}
			}

			// Wrap around screen edges
			if (particle.x < 0) particle.x = this.dimensions.width;
			if (particle.x > this.dimensions.width) particle.x = 0;
			if (particle.y < 0) particle.y = this.dimensions.height;
			if (particle.y > this.dimensions.height) particle.y = 0;
		});
	}

	private drawParticles(): void {
		if (!this.ctx) return;

		this.particles.forEach(particle => {
			this.ctx!.save();
			this.ctx!.globalAlpha = particle.opacity;
			this.ctx!.fillStyle = particle.color;
			this.ctx!.beginPath();
			this.ctx!.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
			this.ctx!.fill();
			this.ctx!.restore();
		});
	}
}
