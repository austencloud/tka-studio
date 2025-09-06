import { writable, derived, get } from 'svelte/store';
import { PerformanceTracker } from './PerformanceTracker';
import type { Dimensions, PerformanceMetrics, QualityLevel } from '../types/types';

export class BackgroundManager {
	public dimensions = writable<Dimensions>({ width: 0, height: 0 });
	public performanceMetrics = writable<PerformanceMetrics>({ fps: 60, warnings: [] });
	public isActive = writable<boolean>(true);
	public qualityMode = writable<QualityLevel>('high');
	public isLoading = writable<boolean>(false);

	private performanceTracker: PerformanceTracker;

	private canvas: HTMLCanvasElement | null = null;
	private ctx: CanvasRenderingContext2D | null = null;

	private animationFrameId: number | null = null;

	private reportCallback: ((metrics: PerformanceMetrics) => void) | null = null;

	public shouldRender = derived(
		[this.performanceMetrics, this.isActive],
		([$metrics, $isActive]) => $isActive && $metrics.fps > 30
	);

	constructor() {
		this.performanceTracker = PerformanceTracker.getInstance();
	}

	public initializeCanvas(canvas: HTMLCanvasElement, onReady?: () => void): void {
		this.canvas = canvas;

		this.ctx = canvas.getContext('2d');
		if (!this.ctx) {
			console.error('Failed to get canvas context');
			return;
		}

		const isBrowser = typeof window !== 'undefined';

		const initialWidth = isBrowser ? window.innerWidth : 1280;
		const initialHeight = isBrowser ? window.innerHeight : 720;

		this.dimensions.set({
			width: initialWidth,
			height: initialHeight
		});

		canvas.width = initialWidth;
		canvas.height = initialHeight;

		if (isBrowser) {
			window.addEventListener('resize', this.handleResize.bind(this));

			document.addEventListener('visibilitychange', this.handleVisibilityChange.bind(this));
		}

		if (onReady) {
			onReady();
		}
	}

	public startAnimation(
		renderFn: (ctx: CanvasRenderingContext2D, dimensions: Dimensions) => void,
		reportFn?: (metrics: PerformanceMetrics) => void
	): void {
		if (!this.ctx || !this.canvas) {
			console.error('Canvas not initialized');
			return;
		}

		if (reportFn) {
			this.reportCallback = reportFn;
		}

		this.performanceTracker.reset();

		const animate = () => {
			if (!this.ctx || !this.canvas) return;

			this.performanceTracker.update();

			const perfStatus = this.performanceTracker.getPerformanceStatus();
			this.performanceMetrics.set({
				fps: perfStatus.fps,
				warnings: perfStatus.warnings
			});

			if (this.reportCallback) {
				this.reportCallback(get(this.performanceMetrics));
			}

			const dimensions = get(this.dimensions);

			if (get(this.shouldRender)) {
				this.ctx.clearRect(0, 0, dimensions.width, dimensions.height);

				renderFn(this.ctx, dimensions);
			}

			this.animationFrameId = requestAnimationFrame(animate);
		};

		if (typeof window !== 'undefined') {
			this.animationFrameId = requestAnimationFrame(animate);
		}
	}

	public stopAnimation(): void {
		if (this.animationFrameId && typeof window !== 'undefined') {
			cancelAnimationFrame(this.animationFrameId);
			this.animationFrameId = null;
		}
	}

	public cleanup(): void {
		this.stopAnimation();

		if (typeof window !== 'undefined') {
			window.removeEventListener('resize', this.handleResize.bind(this));
			document.removeEventListener('visibilitychange', this.handleVisibilityChange.bind(this));
		}

		this.canvas = null;
		this.ctx = null;
	}

	public setQuality(quality: QualityLevel): void {
		this.qualityMode.set(quality);
	}

	public setLoading(isLoading: boolean): void {
		this.isLoading.set(isLoading);
	}

	private handleResize(): void {
		if (!this.canvas) return;

		if (typeof window === 'undefined') return;

		const newWidth = window.innerWidth;
		const newHeight = window.innerHeight;

		this.canvas.width = newWidth;
		this.canvas.height = newHeight;

		this.dimensions.set({ width: newWidth, height: newHeight });

		const currentQuality = get(this.qualityMode);
		this.qualityMode.set('low');

		setTimeout(() => {
			this.qualityMode.set(currentQuality);
		}, 500);
	}

	private handleVisibilityChange(): void {
		const isVisible = document.visibilityState === 'visible';
		this.isActive.set(isVisible);
	}
}

export function createBackgroundManager(): BackgroundManager {
	return new BackgroundManager();
}
