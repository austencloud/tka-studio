// src/lib/components/Backgrounds/deepOcean/OceanAnimationController.ts

import type { AccessibilitySettings } from '../types/types';

export class OceanAnimationController {
	private waveOffset = 0;
	private currentDepth = 0;

	public update(accessibility: AccessibilitySettings): void {
		const speedMultiplier = accessibility.reducedMotion ? 0.3 : 1.0;

		this.waveOffset += 0.02 * speedMultiplier;
		this.currentDepth = 50 + 30 * Math.sin(this.waveOffset * 0.1);
	}

	public getSpeedMultiplier(accessibility: AccessibilitySettings): number {
		return accessibility.reducedMotion ? 0.3 : 1.0;
	}

	public getCurrentDepth(): number {
		return this.currentDepth;
	}

	public getWaveOffset(): number {
		return this.waveOffset;
	}
}
