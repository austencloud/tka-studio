import { get } from 'svelte/store';
import { performanceMetrics, qualityMode } from '../store';

export const createPerformanceMonitor = () => {
	let lastTime = 0;
	let frameCount = 0;
	let fps = 60;
	let warnings: string[] = [];
	let particleCount = 0;
	let reportCallback: ((fps: number, particleCount: number) => void) | null = null;

	const update = (): void => {
		const now = performance.now();

		frameCount++;

		if (now >= lastTime + 1000) {
			fps = frameCount;
			frameCount = 0;
			lastTime = now;

			if (fps < 40) {
				warnings.push(`Low FPS detected: ${fps}`);

				if (warnings.length > 5) warnings.shift();

				if (fps < 30 && get(qualityMode) !== 'low') {
					qualityMode.update((current) => (current === 'high' ? 'medium' : 'low'));
				}
			} else if (fps > 55) {
				qualityMode.update((current) =>
					current === 'low' ? 'medium' : current === 'medium' ? 'high' : current
				);
			}

			performanceMetrics.set({ fps, warnings });

			if (reportCallback) {
				reportCallback(fps, particleCount);
			}
		}
	};

	const start = (callback?: (fps: number, particleCount: number) => void): void => {
		lastTime = performance.now();
		frameCount = 0;

		if (callback) {
			reportCallback = callback;
		}
	};

	const stop = (): void => {
		reportCallback = null;
	};

	const setParticleCount = (count: number): void => {
		particleCount = count;
	};

	return {
		update,
		start,
		stop,
		setParticleCount
	};
};
