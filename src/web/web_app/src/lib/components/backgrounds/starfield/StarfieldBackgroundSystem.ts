// src/lib/components/backgrounds/starfield/StarfieldBackgroundSystem.ts
import type {
	AccessibilitySettings,
	BackgroundSystem,
	Dimensions,
	PerformanceMetrics,
	QualityLevel,
} from '../types/types';

interface Star {
	x: number;
	y: number;
	z: number;
	size: number;
	brightness: number;
	twinklePhase: number;
	twinkleSpeed: number;
}

export class StarfieldBackgroundSystem implements BackgroundSystem {
	private quality: QualityLevel = 'medium';
	private accessibility: AccessibilitySettings = {
		reducedMotion: false,
		highContrast: false,
		visibleParticleSize: 2,
	};

	// Animation state
	private stars: Star[] = [];
	private animationTime = 0;
	private isInitialized = false;

	// Starfield configuration
	private readonly starColors = [
		{ r: 255, g: 255, b: 255 }, // White
		{ r: 255, g: 240, b: 200 }, // Warm white
		{ r: 200, g: 220, b: 255 }, // Cool white
		{ r: 255, g: 200, b: 200 }, // Reddish
		{ r: 200, g: 255, b: 200 }, // Greenish
		{ r: 200, g: 200, b: 255 }, // Bluish
	];

	public initialize(dimensions: Dimensions, quality: QualityLevel): void {
		this.quality = quality;
		this.isInitialized = true;

		// Initialize stars based on quality
		const numStars = this.getNumStars();
		this.stars = this.createStars(numStars, dimensions);
	}

	public update(_dimensions: Dimensions): void {
		if (!this.isInitialized) return;

		this.animationTime += 0.016; // Approximate 60fps

		// Update star twinkling
		for (const star of this.stars) {
			star.twinklePhase += star.twinkleSpeed;
			if (star.twinklePhase > 2 * Math.PI) {
				star.twinklePhase -= 2 * Math.PI;
			}

			// Update brightness based on twinkle
			star.brightness = 0.3 + 0.7 * (Math.sin(star.twinklePhase) * 0.5 + 0.5);
		}

		// Slowly move stars for depth effect (if not reduced motion)
		if (!this.accessibility.reducedMotion) {
			for (const star of this.stars) {
				star.z -= 0.5;
				if (star.z <= 0) {
					// Reset star to back of field
					star.z = 1000;
					star.x = (Math.random() - 0.5) * 2000;
					star.y = (Math.random() - 0.5) * 2000;
				}
			}
		}
	}

	public draw(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
		if (!this.isInitialized) return;

		// Draw space background
		this.drawSpaceBackground(ctx, dimensions);

		// Draw stars
		this.drawStars(ctx, dimensions);

		// Draw nebula effect for high quality
		if (this.quality === 'high') {
			this.drawNebulaEffect(ctx, dimensions);
		}
	}

	public setQuality(quality: QualityLevel): void {
		this.quality = quality;
		if (this.isInitialized) {
			// Adjust number of stars based on quality
			const numStars = this.getNumStars();
			while (this.stars.length > numStars) this.stars.pop();
			while (this.stars.length < numStars) {
				this.stars.push(this.createStar());
			}
		}
	}

	public setAccessibility(settings: AccessibilitySettings): void {
		this.accessibility = settings;
	}

	public cleanup(): void {
		this.stars = [];
		this.isInitialized = false;
	}

	public getMetrics(): PerformanceMetrics {
		return {
			fps: 60, // Estimated
			warnings: [],
			particleCount: this.stars.length,
		};
	}

	private getNumStars(): number {
		switch (this.quality) {
			case 'high':
				return 300;
			case 'medium':
				return 200;
			case 'low':
				return 100;
			case 'minimal':
				return 50;
			default:
				return 200;
		}
	}

	private createStars(count: number, _dimensions: Dimensions): Star[] {
		const stars: Star[] = [];
		for (let i = 0; i < count; i++) {
			stars.push(this.createStar());
		}
		return stars;
	}

	private createStar(): Star {
		return {
			x: (Math.random() - 0.5) * 2000,
			y: (Math.random() - 0.5) * 2000,
			z: Math.random() * 1000,
			size: 0.5 + Math.random() * 2,
			brightness: 0.3 + Math.random() * 0.7,
			twinklePhase: Math.random() * 2 * Math.PI,
			twinkleSpeed: 0.02 + Math.random() * 0.03,
		};
	}

	private drawSpaceBackground(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
		// Create deep space gradient
		const gradient = ctx.createRadialGradient(
			dimensions.width / 2,
			dimensions.height / 2,
			0,
			dimensions.width / 2,
			dimensions.height / 2,
			Math.max(dimensions.width, dimensions.height) / 2
		);

		gradient.addColorStop(0, 'rgb(5, 5, 15)'); // Dark center
		gradient.addColorStop(0.5, 'rgb(2, 2, 8)'); // Darker middle
		gradient.addColorStop(1, 'rgb(0, 0, 3)'); // Very dark edges

		ctx.fillStyle = gradient;
		ctx.fillRect(0, 0, dimensions.width, dimensions.height);
	}

	private drawStars(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
		const centerX = dimensions.width / 2;
		const centerY = dimensions.height / 2;

		for (const star of this.stars) {
			// Project 3D position to 2D screen
			const scale = 200 / star.z;
			const x2d = centerX + star.x * scale;
			const y2d = centerY + star.y * scale;

			// Skip stars outside screen bounds
			if (
				x2d < -10 ||
				x2d > dimensions.width + 10 ||
				y2d < -10 ||
				y2d > dimensions.height + 10
			) {
				continue;
			}

			// Calculate star size and brightness based on distance
			const size = star.size * scale;
			const brightness = star.brightness * Math.min(1, scale);

			// Choose star color
			const colorIndex = Math.floor(star.x + star.y) % this.starColors.length;
			const color = this.starColors[Math.abs(colorIndex)] || { r: 255, g: 255, b: 255 };

			ctx.save();
			ctx.globalAlpha = brightness;

			// Draw star with glow effect
			if (size > 1) {
				// Larger stars get a glow
				const glowGradient = ctx.createRadialGradient(x2d, y2d, 0, x2d, y2d, size * 2);
				glowGradient.addColorStop(
					0,
					`rgba(${color.r}, ${color.g}, ${color.b}, ${brightness})`
				);
				glowGradient.addColorStop(
					0.5,
					`rgba(${color.r}, ${color.g}, ${color.b}, ${brightness * 0.3})`
				);
				glowGradient.addColorStop(1, `rgba(${color.r}, ${color.g}, ${color.b}, 0)`);

				ctx.fillStyle = glowGradient;
				ctx.beginPath();
				ctx.arc(x2d, y2d, size * 2, 0, 2 * Math.PI);
				ctx.fill();
			}

			// Draw the star core
			ctx.fillStyle = `rgba(${color.r}, ${color.g}, ${color.b}, ${brightness})`;
			ctx.beginPath();
			ctx.arc(x2d, y2d, Math.max(0.5, size), 0, 2 * Math.PI);
			ctx.fill();

			ctx.restore();
		}
	}

	private drawNebulaEffect(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
		// Add subtle nebula clouds for enhanced visual appeal
		ctx.save();
		ctx.globalAlpha = 0.1;

		const nebulaGradient = ctx.createRadialGradient(
			dimensions.width * 0.3,
			dimensions.height * 0.7,
			0,
			dimensions.width * 0.3,
			dimensions.height * 0.7,
			dimensions.width * 0.4
		);

		nebulaGradient.addColorStop(0, 'rgba(100, 50, 150, 0.3)');
		nebulaGradient.addColorStop(0.5, 'rgba(50, 100, 200, 0.2)');
		nebulaGradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

		ctx.fillStyle = nebulaGradient;
		ctx.fillRect(0, 0, dimensions.width, dimensions.height);

		// Add second nebula
		const nebula2Gradient = ctx.createRadialGradient(
			dimensions.width * 0.8,
			dimensions.height * 0.2,
			0,
			dimensions.width * 0.8,
			dimensions.height * 0.2,
			dimensions.width * 0.3
		);

		nebula2Gradient.addColorStop(0, 'rgba(150, 100, 50, 0.2)');
		nebula2Gradient.addColorStop(0.5, 'rgba(200, 150, 100, 0.1)');
		nebula2Gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

		ctx.fillStyle = nebula2Gradient;
		ctx.fillRect(0, 0, dimensions.width, dimensions.height);

		ctx.restore();
	}
}
