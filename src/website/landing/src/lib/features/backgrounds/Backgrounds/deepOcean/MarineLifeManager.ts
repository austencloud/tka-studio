// src/lib/components/Backgrounds/deepOcean/MarineLifeManager.ts

import type { Dimensions, QualityLevel, AccessibilitySettings } from '../types/types';
import type { OceanConfig } from './OceanConfiguration';

export interface Jellyfish {
	x: number;
	y: number;
	size: number;
	pulsePhase: number;
	pulseSpeed: number;
	driftX: number;
	driftY: number;
	opacity: number;
	color: string;
	tentacles: Array<{
		x: number;
		y: number;
		length: number;
		sway: number;
	}>;
}

export interface Fish {
	x: number;
	y: number;
	size: number;
	speed: number;
	direction: number;
	schoolId: number;
	wiggle: number;
	color: string;
	opacity: number;
}

export interface Whale {
	x: number;
	y: number;
	size: number;
	direction: number;
	speed: number;
	opacity: number;
	breathTimer: number;
}

export class MarineLifeManager {
	private jellyfish: Jellyfish[] = [];
	private fishSchools: Fish[] = [];
	private whale: Whale | null = null;
	private whaleTimer = 0;
	private whaleInterval = 18000;
	private config: OceanConfig;

	constructor(config: OceanConfig) {
		this.config = config;
	}

	public initialize(dimensions: Dimensions, quality: QualityLevel): void {
		this.initializeJellyfish(dimensions, quality);
		this.initializeFishSchools(dimensions, quality);
	}

	private initializeJellyfish(dimensions: Dimensions, quality: QualityLevel): void {
		const count = this.config.jellyfish.count[quality];
		this.jellyfish = [];

		for (let i = 0; i < count; i++) {
			const size = Math.random() * 40 + 30;
			const x = Math.random() * dimensions.width;
			const y = Math.random() * dimensions.height * 0.8 + dimensions.height * 0.1;

			const tentacles = [];
			const tentacleCount = Math.floor(Math.random() * 6) + 4;
			for (let t = 0; t < tentacleCount; t++) {
				tentacles.push({
					x: x + (Math.random() - 0.5) * size * 0.8,
					y: y + size * 0.3,
					length: Math.random() * size * 1.5 + size * 0.5,
					sway: Math.random() * Math.PI * 2
				});
			}

			this.jellyfish.push({
				x,
				y,
				size,
				pulsePhase: Math.random() * Math.PI * 2,
				pulseSpeed: Math.random() * 0.02 + 0.01,
				driftX: (Math.random() - 0.5) * 0.1,
				driftY: (Math.random() - 0.5) * 0.05,
				opacity: Math.random() * 0.4 + 0.6,
				color:
					this.config.jellyfish.colors[
						Math.floor(Math.random() * this.config.jellyfish.colors.length)
					],
				tentacles
			});
		}
	}

	private initializeFishSchools(dimensions: Dimensions, quality: QualityLevel): void {
		const schoolCount = this.config.fish.schoolCount[quality];
		const schoolSize = this.config.fish.schoolSize[quality];
		this.fishSchools = [];

		for (let s = 0; s < schoolCount; s++) {
			const centerX = Math.random() * dimensions.width;
			const centerY = Math.random() * dimensions.height * 0.6 + dimensions.height * 0.2;
			const schoolColor =
				this.config.fish.colors[Math.floor(Math.random() * this.config.fish.colors.length)];

			for (let i = 0; i < schoolSize; i++) {
				this.fishSchools.push({
					x: centerX + (Math.random() - 0.5) * 100,
					y: centerY + (Math.random() - 0.5) * 50,
					size: Math.random() * 8 + 4,
					speed: Math.random() * 0.5 + 0.3,
					direction: Math.random() * Math.PI * 2,
					schoolId: s,
					wiggle: Math.random() * Math.PI * 2,
					color: schoolColor,
					opacity: Math.random() * 0.3 + 0.7
				});
			}
		}
	}

	public update(dimensions: Dimensions, speedMultiplier: number): void {
		this.updateJellyfish(dimensions, speedMultiplier);
		this.updateFishSchools(dimensions, speedMultiplier);
		this.updateWhale(dimensions, speedMultiplier);
	}

	private updateJellyfish(dimensions: Dimensions, speedMultiplier: number): void {
		this.jellyfish.forEach((jelly) => {
			jelly.pulsePhase += jelly.pulseSpeed * speedMultiplier;
			jelly.x += jelly.driftX * speedMultiplier;
			jelly.y += jelly.driftY * speedMultiplier;

			// Update tentacles
			jelly.tentacles.forEach((tentacle) => {
				tentacle.sway += 0.03 * speedMultiplier;
			});

			// Wrap around screen
			if (jelly.x < -jelly.size) jelly.x = dimensions.width + jelly.size;
			if (jelly.x > dimensions.width + jelly.size) jelly.x = -jelly.size;
			if (jelly.y < -jelly.size) jelly.y = dimensions.height + jelly.size;
			if (jelly.y > dimensions.height + jelly.size) jelly.y = -jelly.size;
		});
	}

	private updateFishSchools(dimensions: Dimensions, speedMultiplier: number): void {
		// Group fish by school
		const schools = new Map<number, Fish[]>();
		this.fishSchools.forEach((fish) => {
			if (!schools.has(fish.schoolId)) schools.set(fish.schoolId, []);
			schools.get(fish.schoolId)!.push(fish);
		});

		// Update each school
		schools.forEach((school) => {
			// Calculate school center
			const centerX = school.reduce((sum, fish) => sum + fish.x, 0) / school.length;
			const centerY = school.reduce((sum, fish) => sum + fish.y, 0) / school.length;

			school.forEach((fish) => {
				// Schooling behavior
				const toCenterX = centerX - fish.x;
				const toCenterY = centerY - fish.y;
				const distanceToCenter = Math.sqrt(toCenterX * toCenterX + toCenterY * toCenterY);

				if (distanceToCenter > 50) {
					fish.direction += (Math.atan2(toCenterY, toCenterX) - fish.direction) * 0.1;
				}

				// Individual movement
				fish.wiggle += 0.1 * speedMultiplier;
				fish.direction += Math.sin(fish.wiggle) * 0.1;

				fish.x += Math.cos(fish.direction) * fish.speed * speedMultiplier;
				fish.y += Math.sin(fish.direction) * fish.speed * speedMultiplier;

				// Wrap around
				if (fish.x < -20) fish.x = dimensions.width + 20;
				if (fish.x > dimensions.width + 20) fish.x = -20;
				if (fish.y < 50) fish.y = dimensions.height - 50;
				if (fish.y > dimensions.height - 50) fish.y = 50;
			});
		});
	}

	private updateWhale(dimensions: Dimensions, speedMultiplier: number): void {
		this.whaleTimer++;

		if (!this.whale && this.whaleTimer >= this.whaleInterval) {
			// Spawn whale
			const direction = Math.random() > 0.5 ? 1 : -1;
			this.whale = {
				x: direction > 0 ? -this.config.whale.size : dimensions.width + this.config.whale.size,
				y: dimensions.height * 0.3 + Math.random() * dimensions.height * 0.3,
				size: this.config.whale.size,
				direction,
				speed: this.config.whale.speed * dimensions.width,
				opacity: 0,
				breathTimer: 0
			};
			this.whaleTimer = 0;
			this.whaleInterval = 15000 + Math.random() * 25000; // 4-10 minutes
		}

		if (this.whale) {
			this.whale.x += this.whale.direction * this.whale.speed * speedMultiplier;
			this.whale.breathTimer += speedMultiplier;

			// Fade in/out
			const distanceFromEdge = Math.min(
				Math.abs(this.whale.x),
				Math.abs(this.whale.x - dimensions.width)
			);
			this.whale.opacity = Math.min(1, distanceFromEdge / 200);

			// Remove when off screen
			if (
				(this.whale.direction > 0 && this.whale.x > dimensions.width + this.whale.size) ||
				(this.whale.direction < 0 && this.whale.x < -this.whale.size)
			) {
				this.whale = null;
			}
		}
	}

	public draw(
		ctx: CanvasRenderingContext2D,
		accessibility: AccessibilitySettings,
		quality: QualityLevel
	): void {
		this.drawJellyfish(ctx, accessibility, quality);
		this.drawFishSchools(ctx, accessibility);
		this.drawWhale(ctx, accessibility);
	}

	private drawJellyfish(
		ctx: CanvasRenderingContext2D,
		accessibility: AccessibilitySettings,
		quality: QualityLevel
	): void {
		this.jellyfish.forEach((jelly) => {
			const pulseFactor = 1 + 0.2 * Math.sin(jelly.pulsePhase);
			const currentSize = jelly.size * pulseFactor;

			ctx.globalAlpha = jelly.opacity * (accessibility.reducedMotion ? 0.7 : 1);

			// Draw tentacles
			ctx.strokeStyle = accessibility.highContrast ? '#FFFFFF' : jelly.color;
			ctx.lineWidth = 2;
			jelly.tentacles.forEach((tentacle) => {
				ctx.beginPath();
				ctx.moveTo(tentacle.x, tentacle.y);
				const endX = tentacle.x + Math.sin(tentacle.sway) * 20;
				const endY = tentacle.y + tentacle.length;
				ctx.quadraticCurveTo(
					tentacle.x + Math.sin(tentacle.sway * 2) * 15,
					tentacle.y + tentacle.length * 0.5,
					endX,
					endY
				);
				ctx.stroke();
			});

			// Draw bell
			ctx.fillStyle = accessibility.highContrast ? 'rgba(255,255,255,0.3)' : jelly.color;
			ctx.beginPath();
			ctx.ellipse(jelly.x, jelly.y, currentSize, currentSize * 0.7, 0, 0, Math.PI * 2);
			ctx.fill();

			// Glow effect
			if (quality === 'high' && !accessibility.highContrast) {
				ctx.shadowColor = jelly.color;
				ctx.shadowBlur = 20;
				ctx.beginPath();
				ctx.ellipse(jelly.x, jelly.y, currentSize * 0.5, currentSize * 0.35, 0, 0, Math.PI * 2);
				ctx.fill();
				ctx.shadowBlur = 0;
			}
		});
		ctx.globalAlpha = 1;
	}

	private drawFishSchools(
		ctx: CanvasRenderingContext2D,
		accessibility: AccessibilitySettings
	): void {
		this.fishSchools.forEach((fish) => {
			ctx.globalAlpha = fish.opacity;
			ctx.fillStyle = accessibility.highContrast ? '#FFFFFF' : fish.color;

			ctx.save();
			ctx.translate(fish.x, fish.y);
			ctx.rotate(fish.direction);

			// Simple fish shape
			ctx.beginPath();
			ctx.ellipse(0, 0, fish.size, fish.size * 0.6, 0, 0, Math.PI * 2);
			ctx.fill();

			// Tail
			ctx.beginPath();
			ctx.moveTo(-fish.size, 0);
			ctx.lineTo(-fish.size * 1.5, -fish.size * 0.5);
			ctx.lineTo(-fish.size * 1.5, fish.size * 0.5);
			ctx.closePath();
			ctx.fill();

			ctx.restore();
		});
		ctx.globalAlpha = 1;
	}

	private drawWhale(ctx: CanvasRenderingContext2D, accessibility: AccessibilitySettings): void {
		if (!this.whale) return;

		ctx.globalAlpha = this.whale.opacity;
		ctx.fillStyle = accessibility.highContrast ? '#666666' : this.config.whale.color;

		ctx.save();
		ctx.translate(this.whale.x, this.whale.y);
		if (this.whale.direction < 0) ctx.scale(-1, 1);

		// Whale body
		ctx.beginPath();
		ctx.ellipse(0, 0, this.whale.size, this.whale.size * 0.4, 0, 0, Math.PI * 2);
		ctx.fill();

		// Tail
		ctx.beginPath();
		ctx.moveTo(-this.whale.size * 0.8, 0);
		ctx.lineTo(-this.whale.size * 1.3, -this.whale.size * 0.3);
		ctx.lineTo(-this.whale.size * 1.5, 0);
		ctx.lineTo(-this.whale.size * 1.3, this.whale.size * 0.3);
		ctx.closePath();
		ctx.fill();

		// Breathing bubbles
		if (this.whale.breathTimer % 180 < 60) {
			for (let i = 0; i < 5; i++) {
				ctx.globalAlpha = this.whale.opacity * (1 - (this.whale.breathTimer % 60) / 60);
				ctx.beginPath();
				ctx.arc(
					this.whale.size * 0.3 + i * 10,
					-this.whale.size * 0.5 - i * 15,
					3 + i,
					0,
					Math.PI * 2
				);
				ctx.fill();
			}
		}

		ctx.restore();
		ctx.globalAlpha = 1;
	}

	public getMarineLifeCount(): number {
		return this.jellyfish.length + this.fishSchools.length + (this.whale ? 1 : 0);
	}

	public cleanup(): void {
		this.jellyfish = [];
		this.fishSchools = [];
		this.whale = null;
	}
}
