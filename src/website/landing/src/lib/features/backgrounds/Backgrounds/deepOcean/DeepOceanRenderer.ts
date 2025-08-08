// src/lib/components/Backgrounds/deepOcean/DeepOceanRenderer.ts

import type {
	BackgroundSystem,
	Dimensions,
	QualityLevel,
	AccessibilitySettings,
	PerformanceMetrics
} from '../types/types';
import { drawBackgroundGradient } from '../snowfall/utils/backgroundUtils';
import { PerformanceTracker } from '../core/PerformanceTracker';
import { OceanConfiguration } from './OceanConfiguration';
import { ParticleManager } from './ParticleManager';
import { MarineLifeManager } from './MarineLifeManager';
import { EnvironmentManager } from './EnvironmentManager';
import { OceanAnimationController } from './OceanAnimationController';

export class DeepOceanRenderer implements BackgroundSystem {
	private quality: QualityLevel = 'medium';
	private performanceTracker: PerformanceTracker;
	private accessibility: AccessibilitySettings = {
		reducedMotion: false,
		highContrast: false,
		visibleParticleSize: 2
	};

	// Managers
	private configuration: OceanConfiguration;
	private particleManager: ParticleManager;
	private marineLifeManager: MarineLifeManager;
	private environmentManager: EnvironmentManager;
	private animationController: OceanAnimationController;

	constructor() {
		this.performanceTracker = PerformanceTracker.getInstance();
		this.configuration = OceanConfiguration.getInstance();

		const config = this.configuration.getConfig();
		this.particleManager = new ParticleManager(config);
		this.marineLifeManager = new MarineLifeManager(config);
		this.environmentManager = new EnvironmentManager(config);
		this.animationController = new OceanAnimationController();
	}

	public initialize(dimensions: Dimensions, quality: QualityLevel): void {
		this.quality = quality;
		this.particleManager.initialize(dimensions, quality);
		this.marineLifeManager.initialize(dimensions, quality);
		this.environmentManager.initialize(dimensions, quality);
	}

	public update(dimensions: Dimensions): void {
		this.animationController.update(this.accessibility);
		const speedMultiplier = this.animationController.getSpeedMultiplier(this.accessibility);

		this.particleManager.update(dimensions, speedMultiplier);
		this.marineLifeManager.update(dimensions, speedMultiplier);
		this.environmentManager.update(dimensions, speedMultiplier);
	}

	public draw(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
		this.drawBackground(ctx, dimensions);
		this.environmentManager.draw(ctx, dimensions, this.accessibility, this.quality);
		this.particleManager.draw(ctx, this.accessibility);
		this.marineLifeManager.draw(ctx, this.accessibility, this.quality);
	}

	private drawBackground(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
		const gradientStops = this.accessibility.highContrast
			? [
					{ position: 0, color: '#000033' },
					{ position: 1, color: '#000066' }
				]
			: this.configuration.getConfig().background.gradientStops;
		drawBackgroundGradient(ctx, dimensions, gradientStops);
	}

	public setQuality(quality: QualityLevel): void {
		if (this.quality === quality) return;
		this.quality = quality;
		// Re-initialize with new quality settings
		// This could be optimized to only update what's necessary
	}

	public setAccessibility(settings: AccessibilitySettings): void {
		this.accessibility = settings;
	}

	public cleanup(): void {
		this.particleManager.cleanup();
		this.marineLifeManager.cleanup();
		this.environmentManager.cleanup();
	}

	public getMetrics(): PerformanceMetrics {
		const perfStatus = this.performanceTracker.getPerformanceStatus();
		return {
			fps: perfStatus.fps,
			warnings: perfStatus.warnings,
			particleCount:
				this.particleManager.getParticleCount() + this.marineLifeManager.getMarineLifeCount()
		};
	}
}
