export class PerformanceTracker {
	private static instance: PerformanceTracker;
	private fps: number = 60;
	private frameCount: number = 0;
	private lastTime: number = 0;
	private particleCount: number = 0;
	private warnings: string[] = [];

	private constructor() {
		this.lastTime = performance.now();
	}

	public static getInstance(): PerformanceTracker {
		if (!PerformanceTracker.instance) {
			PerformanceTracker.instance = new PerformanceTracker();
		}
		return PerformanceTracker.instance;
	}

	public update(): void {
		const now = performance.now();
		this.frameCount++;

		if (now >= this.lastTime + 1000) {
			this.fps = this.frameCount;
			this.frameCount = 0;
			this.lastTime = now;

			if (this.fps < 30) {
				this.warnings.push(`Low FPS detected: ${this.fps}`);

				if (this.warnings.length > 5) this.warnings.shift();
			} else {
				if (this.warnings.length > 0) {
					this.warnings = [];
				}
			}
		}
	}

	public getPerformanceStatus(): {
		fps: number;
		particleCount: number;
		warnings: string[];
	} {
		return {
			fps: this.fps,
			particleCount: this.particleCount,
			warnings: this.warnings
		};
	}

	public setParticleCount(count: number): void {
		this.particleCount = count;
	}

	public reset(): void {
		this.fps = 60;
		this.frameCount = 0;
		this.lastTime = performance.now();
		this.particleCount = 0;
		this.warnings = [];
	}
}
