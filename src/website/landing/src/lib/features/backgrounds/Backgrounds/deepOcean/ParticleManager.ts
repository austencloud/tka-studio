// src/lib/components/Backgrounds/deepOcean/ParticleManager.ts

import type { Dimensions, QualityLevel, AccessibilitySettings } from '../types/types';
import type { OceanConfig } from './OceanConfiguration';

export interface OceanParticle {
	x: number;
	y: number;
	z: number;
	size: number;
	opacity: number;
	color: string;
	speed: number;
	drift: number;
	type: 'bubble' | 'plankton' | 'debris';
}

export class ParticleManager {
	private particles: OceanParticle[] = [];
	private config: OceanConfig;

	constructor(config: OceanConfig) {
		this.config = config;
	}

	public initialize(dimensions: Dimensions, quality: QualityLevel): void {
		const count = Math.floor(dimensions.width * dimensions.height * this.config.particles.density);
		const qualityMultiplier = quality === 'high' ? 1 : quality === 'medium' ? 0.7 : 0.4;

		this.particles = [];
		for (let i = 0; i < count * qualityMultiplier; i++) {
			this.particles.push(this.createParticle(dimensions));
		}
	}

	private createParticle(dimensions: Dimensions): OceanParticle {
		const type = Math.random() < 0.6 ? 'bubble' : Math.random() < 0.8 ? 'plankton' : 'debris';
		const colors = this.getColorsForType(type);

		return {
			x: Math.random() * dimensions.width,
			y: Math.random() * dimensions.height,
			z: Math.random(),
			size: Math.random() * (type === 'bubble' ? 8 : type === 'plankton' ? 4 : 6) + 2,
			opacity: Math.random() * 0.8 + 0.2,
			color: colors[Math.floor(Math.random() * colors.length)],
			speed: Math.random() * (type === 'bubble' ? 0.5 : 0.2) + 0.1,
			drift: (Math.random() - 0.5) * 0.3,
			type
		};
	}

	private getColorsForType(type: 'bubble' | 'plankton' | 'debris'): string[] {
		switch (type) {
			case 'bubble':
				return this.config.particles.bubbleColors;
			case 'plankton':
				return this.config.particles.planktonColors;
			case 'debris':
				return this.config.particles.debrisColors;
		}
	}

	public update(dimensions: Dimensions, speedMultiplier: number): void {
		this.particles.forEach((particle) => {
			particle.y -= particle.speed * speedMultiplier;
			particle.x += particle.drift * speedMultiplier;

			if (particle.type === 'plankton') {
				particle.opacity = 0.4 + 0.4 * Math.sin(Date.now() * 0.005 + particle.x * 0.01);
			}

			// Wrap particles
			if (particle.y < -10) particle.y = dimensions.height + 10;
			if (particle.x < -10) particle.x = dimensions.width + 10;
			if (particle.x > dimensions.width + 10) particle.x = -10;
		});
	}

	public draw(ctx: CanvasRenderingContext2D, accessibility: AccessibilitySettings): void {
		this.particles.forEach((particle) => {
			ctx.globalAlpha = particle.opacity * (1 - particle.z * 0.5);
			ctx.fillStyle = accessibility.highContrast ? '#FFFFFF' : particle.color;

			if (particle.type === 'bubble') {
				ctx.beginPath();
				ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
				ctx.fill();
			} else if (particle.type === 'plankton') {
				ctx.fillRect(particle.x, particle.y, particle.size * 0.5, particle.size * 0.5);
			} else {
				ctx.fillRect(particle.x, particle.y, particle.size, particle.size * 0.3);
			}
		});
		ctx.globalAlpha = 1;
	}

	public getParticleCount(): number {
		return this.particles.length;
	}

	public cleanup(): void {
		this.particles = [];
	}
}
