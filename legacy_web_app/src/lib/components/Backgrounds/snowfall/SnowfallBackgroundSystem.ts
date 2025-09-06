// src/lib/components/Backgrounds/snowfall/SnowfallBackgroundSystem.ts
import { createSnowflakeSystem } from '../systems/SnowflakeSystem';
import { createShootingStarSystem } from '../systems/ShootingStarSystem';
import type {
	BackgroundSystem,
	Dimensions,
	QualityLevel,
	ShootingStarState,
	Snowflake
} from '../types/types';
import { drawBackgroundGradient } from './utils/backgroundUtils';
import { getOptimizedConfig } from '../config';

export class SnowfallBackgroundSystem implements BackgroundSystem {
	private snowflakeSystem = createSnowflakeSystem();
	private shootingStarSystem = createShootingStarSystem();

	private snowflakes: Snowflake[] = [];
	private shootingStarState: ShootingStarState;

	private quality: QualityLevel = 'medium';
	private isDecember: boolean = false;
	private accessibilitySettings: { reducedMotion: boolean; highContrast: boolean } = {
		reducedMotion: false,
		highContrast: false
	};
	private isInitialized: boolean = false;

	constructor() {
		this.shootingStarState = this.shootingStarSystem.initialState;
		this.isDecember = new Date().getMonth() === 11;
		this.isInitialized = false;
	}

	public initialize(dimensions: Dimensions, quality: QualityLevel): void {
		this.quality = quality;
		this.snowflakes = this.snowflakeSystem.initialize(dimensions, quality);
		this.shootingStarState = this.shootingStarSystem.initialState;
		this.isInitialized = true;
	}

	public update(dimensions: Dimensions): void {
		if (dimensions && dimensions.width > 0 && dimensions.height > 0) {
			// If not initialized, or if initialized but snowflakes are unexpectedly empty (e.g. after temporary invalid dimensions)
			// and we have valid dimensions, (re-)initialize.
			if (!this.isInitialized || this.snowflakes.length === 0) {
				this.initialize(dimensions, this.quality);
			}
		}

		if (this.isInitialized) {
			this.snowflakes = this.snowflakeSystem.update(this.snowflakes, dimensions);
			const { qualitySettings } = getOptimizedConfig(this.quality);
			if (qualitySettings.enableShootingStars) {
				this.shootingStarState = this.shootingStarSystem.update(this.shootingStarState, dimensions);
			}
		}
	}

	public draw(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
		const { config, qualitySettings } = getOptimizedConfig(this.quality);

		drawBackgroundGradient(ctx, dimensions, config.core.background.gradientStops);

		if (this.isInitialized) {
			this.snowflakeSystem.draw(this.snowflakes, ctx, dimensions);
			if (qualitySettings.enableShootingStars) {
				this.shootingStarSystem.draw(this.shootingStarState, ctx);
			}
		}
	}

	public setQuality(quality: QualityLevel): void {
		this.quality = quality;
		if (this.snowflakeSystem.setQuality) {
			this.snowflakeSystem.setQuality(quality);
		}
	}

	public setAccessibility(settings: { reducedMotion: boolean; highContrast: boolean }): void {
		this.accessibilitySettings = settings;
	}

	public handleResize(oldDimensions: Dimensions, newDimensions: Dimensions): void {
		this.snowflakes = this.snowflakeSystem.adjustToResize(
			this.snowflakes,
			oldDimensions,
			newDimensions,
			this.quality
		);

		this.shootingStarState = this.shootingStarSystem.initialState;
	}

	public cleanup(): void {
		// Clean up any resources if needed
	}
}
