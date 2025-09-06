import type { Dimensions, QualityLevel } from '../types/types';
import { PerformanceTracker } from './PerformanceTracker';

export abstract class AnimationComponent {
	protected performanceTracker: PerformanceTracker;
	protected initialized: boolean = false;
	protected quality: QualityLevel = 'medium';
	constructor() {
		this.performanceTracker = PerformanceTracker.getInstance();
	}
	abstract initialize(dimensions: Dimensions, quality: QualityLevel): void;
	abstract update(dimensions: Dimensions): void;
	abstract draw(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void;
	abstract cleanup(): void;
	setQuality(quality: QualityLevel): void {
		this.quality = quality;
	}
	protected shouldRender(): boolean {
		const status = this.performanceTracker.getPerformanceStatus();
		return status.fps > 40;
	}
	protected randomInt(min: number, max: number): number {
		return Math.floor(Math.random() * (max - min + 1)) + min;
	}
	protected randomFloat(min: number, max: number): number {
		return Math.random() * (max - min) + min;
	}
}
