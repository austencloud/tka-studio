// src/lib/components/Backgrounds/deepOcean/EnvironmentManager.ts

import type { Dimensions, QualityLevel, AccessibilitySettings } from '../types/types';
import type { OceanConfig } from './OceanConfiguration';

export interface CoralFormation {
	x: number;
	y: number;
	width: number;
	height: number;
	branches: Array<{
		x: number;
		y: number;
		angle: number;
		length: number;
		sway: number;
	}>;
	color: string;
	glowIntensity: number;
}

export interface LightRay {
	x: number;
	startY: number;
	endY: number;
	width: number;
	opacity: number;
	sway: number;
	color: string;
}

export class EnvironmentManager {
	private coral: CoralFormation[] = [];
	private lightRays: LightRay[] = [];
	private causticOffset = 0;
	private config: OceanConfig;

	constructor(config: OceanConfig) {
		this.config = config;
	}

	public initialize(dimensions: Dimensions, quality: QualityLevel): void {
		this.initializeCoral(dimensions, quality);
		this.initializeLightRays(dimensions, quality);
	}

	private initializeCoral(dimensions: Dimensions, quality: QualityLevel): void {
		const count = this.config.coral.count[quality];
		this.coral = [];

		for (let i = 0; i < count; i++) {
			const x = Math.random() * dimensions.width;
			const y = dimensions.height * 0.8 + Math.random() * dimensions.height * 0.2;
			const width = Math.random() * 80 + 40;
			const height = Math.random() * 120 + 60;

			const branches = [];
			const branchCount = Math.floor(Math.random() * 8) + 5;
			for (let b = 0; b < branchCount; b++) {
				branches.push({
					x: x + (Math.random() - 0.5) * width,
					y: y - Math.random() * height,
					angle: Math.random() * Math.PI * 0.5 - Math.PI * 0.25,
					length: Math.random() * height * 0.6 + 20,
					sway: Math.random() * Math.PI * 2
				});
			}

			this.coral.push({
				x,
				y,
				width,
				height,
				branches,
				color:
					this.config.coral.colors[Math.floor(Math.random() * this.config.coral.colors.length)],
				glowIntensity: Math.random() * 0.5 + 0.3
			});
		}
	}

	private initializeLightRays(dimensions: Dimensions, quality: QualityLevel): void {
		if (quality === 'low') return;

		this.lightRays = [];
		const rayCount = quality === 'high' ? 6 : 4;

		for (let i = 0; i < rayCount; i++) {
			this.lightRays.push({
				x: (i / rayCount) * dimensions.width + Math.random() * 100 - 50,
				startY: 0,
				endY: dimensions.height * 0.6,
				width: Math.random() * 30 + 20,
				opacity: Math.random() * 0.3 + 0.1,
				sway: Math.random() * Math.PI * 2,
				color: `rgba(255, 255, 255, ${Math.random() * 0.2 + 0.1})`
			});
		}
	}

	public update(dimensions: Dimensions, speedMultiplier: number): void {
		this.updateCoral(speedMultiplier);
		this.updateLightRays(speedMultiplier);
		this.causticOffset += 0.01 * speedMultiplier;
	}

	private updateCoral(speedMultiplier: number): void {
		this.coral.forEach((coral) => {
			coral.branches.forEach((branch) => {
				branch.sway += 0.02 * speedMultiplier;
			});
			coral.glowIntensity = 0.3 + 0.2 * Math.sin(Date.now() * 0.003);
		});
	}

	private updateLightRays(speedMultiplier: number): void {
		this.lightRays.forEach((ray) => {
			ray.sway += 0.01 * speedMultiplier;
			ray.x += Math.sin(ray.sway) * 0.5;
		});
	}

	public draw(
		ctx: CanvasRenderingContext2D,
		dimensions: Dimensions,
		accessibility: AccessibilitySettings,
		quality: QualityLevel
	): void {
		this.drawLightRays(ctx, accessibility, quality);
		this.drawCoral(ctx, accessibility);
		this.drawCaustics(ctx, dimensions, quality);
	}

	private drawLightRays(
		ctx: CanvasRenderingContext2D,
		accessibility: AccessibilitySettings,
		quality: QualityLevel
	): void {
		if (quality === 'low') return;

		this.lightRays.forEach((ray) => {
			const gradient = ctx.createLinearGradient(ray.x, ray.startY, ray.x, ray.endY);
			gradient.addColorStop(0, ray.color);
			gradient.addColorStop(0.5, `rgba(255, 255, 255, ${ray.opacity * 0.3})`);
			gradient.addColorStop(1, 'transparent');

			ctx.fillStyle = gradient;
			ctx.beginPath();
			ctx.moveTo(ray.x - ray.width / 2, ray.startY);
			ctx.lineTo(ray.x + ray.width / 2, ray.startY);
			ctx.lineTo(ray.x + ray.width / 3 + Math.sin(ray.sway) * 10, ray.endY);
			ctx.lineTo(ray.x - ray.width / 3 + Math.sin(ray.sway) * 10, ray.endY);
			ctx.closePath();
			ctx.fill();
		});
	}

	private drawCoral(ctx: CanvasRenderingContext2D, accessibility: AccessibilitySettings): void {
		this.coral.forEach((coral) => {
			ctx.strokeStyle = accessibility.highContrast ? '#FFFFFF' : coral.color;
			ctx.lineWidth = 3;
			ctx.lineCap = 'round';

			coral.branches.forEach((branch) => {
				ctx.globalAlpha = coral.glowIntensity;
				ctx.beginPath();
				ctx.moveTo(branch.x, branch.y);

				const swayX = Math.sin(branch.sway) * 10;
				const endX = branch.x + Math.cos(branch.angle) * branch.length + swayX;
				const endY = branch.y + Math.sin(branch.angle) * branch.length;

				ctx.quadraticCurveTo(
					branch.x + Math.cos(branch.angle) * branch.length * 0.5 + swayX * 0.5,
					branch.y + Math.sin(branch.angle) * branch.length * 0.5,
					endX,
					endY
				);
				ctx.stroke();
			});
		});
		ctx.globalAlpha = 1;
	}

	private drawCaustics(
		ctx: CanvasRenderingContext2D,
		dimensions: Dimensions,
		quality: QualityLevel
	): void {
		if (quality === 'low') return;

		ctx.globalCompositeOperation = 'overlay';
		ctx.globalAlpha = 0.1;

		const causticSize = 100;
		for (let x = 0; x < dimensions.width; x += causticSize) {
			for (let y = 0; y < dimensions.height; y += causticSize) {
				const intensity =
					Math.sin(x * 0.01 + this.causticOffset) * Math.cos(y * 0.008 + this.causticOffset * 0.7);

				if (intensity > 0.3) {
					ctx.fillStyle = `rgba(255, 255, 255, ${intensity * 0.5})`;
					ctx.beginPath();
					ctx.arc(x + causticSize / 2, y + causticSize / 2, causticSize / 4, 0, Math.PI * 2);
					ctx.fill();
				}
			}
		}

		ctx.globalCompositeOperation = 'source-over';
		ctx.globalAlpha = 1;
	}

	public cleanup(): void {
		this.coral = [];
		this.lightRays = [];
	}
}
