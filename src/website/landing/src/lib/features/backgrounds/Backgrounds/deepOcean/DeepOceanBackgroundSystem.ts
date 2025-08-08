// src/lib/components/Backgrounds/deepOcean/DeepOceanBackgroundSystem.ts

import type {
	BackgroundSystem,
	Dimensions,
	QualityLevel,
	AccessibilitySettings,
	PerformanceMetrics
} from '../types/types';
import { DeepOceanRenderer } from './DeepOceanRenderer';

/**
 * Legacy wrapper for the DeepOceanBackgroundSystem that maintains backward compatibility
 * while using the new modular architecture internally.
 */
export class DeepOceanBackgroundSystem implements BackgroundSystem {
	private renderer: DeepOceanRenderer;

	constructor() {
		this.renderer = new DeepOceanRenderer();
	}

	public initialize(dimensions: Dimensions, quality: QualityLevel): void {
		this.renderer.initialize(dimensions, quality);
	}

	public update(dimensions: Dimensions): void {
		this.renderer.update(dimensions);
	}

	public draw(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
		this.renderer.draw(ctx, dimensions);
	}

	public setQuality(quality: QualityLevel): void {
		this.renderer.setQuality(quality);
	}

	public setAccessibility(settings: AccessibilitySettings): void {
		this.renderer.setAccessibility(settings);
	}

	public cleanup(): void {
		this.renderer.cleanup();
	}

	public getMetrics(): PerformanceMetrics {
		return this.renderer.getMetrics();
	}
}
