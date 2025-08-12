// src/lib/components/backgrounds/bubbles/BubblesBackgroundSystem.ts
import type {
	AccessibilitySettings,
	BackgroundSystem,
	Dimensions,
	PerformanceMetrics,
	QualityLevel,
} from '../types/types';

interface Bubble {
	x: number;
	y: number;
	size: number;
	speed: number;
	opacity: number;
	color: { r: number; g: number; b: number };
	wobble: number;
	wobbleSpeed: number;
	life: number;
	maxLife: number;
}

export class BubblesBackgroundSystem implements BackgroundSystem {
	private quality: QualityLevel = 'medium';
	private accessibility: AccessibilitySettings = {
		reducedMotion: false,
		highContrast: false,
		visibleParticleSize: 2,
	};

	// Animation state
	private bubbles: Bubble[] = [];
	private animationTime = 0;
	private isInitialized = false;

	// Bubble configuration
	private readonly bubbleColors = [
		{ r: 100, g: 200, b: 255 }, // Light blue
		{ r: 150, g: 255, b: 200 }, // Light green
		{ r: 255, g: 200, b: 150 }, // Light orange
		{ r: 200, g: 150, b: 255 }, // Light purple
		{ r: 255, g: 255, b: 150 }, // Light yellow
		{ r: 255, g: 150, b: 200 }, // Light pink
	];

	public initialize(dimensions: Dimensions, quality: QualityLevel): void {
		this.quality = quality;
		this.isInitialized = true;

		// Initialize bubbles based on quality
		const numBubbles = this.getNumBubbles();
		this.bubbles = this.createBubbles(numBubbles, dimensions);
	}

	public update(dimensions: Dimensions): void {
		if (!this.isInitialized) return;

		this.animationTime += 0.016; // Approximate 60fps

		// Update existing bubbles
		for (let i = this.bubbles.length - 1; i >= 0; i--) {
			const bubble = this.bubbles[i];
			if (!bubble) continue; // Skip if bubble is undefined

			// Update position
			if (!this.accessibility.reducedMotion) {
				bubble.y -= bubble.speed;
				bubble.x += Math.sin(bubble.wobble) * 0.5;
				bubble.wobble += bubble.wobbleSpeed;
			}

			// Update life and opacity
			bubble.life++;
			const lifeRatio = bubble.life / bubble.maxLife;
			bubble.opacity = Math.sin(lifeRatio * Math.PI) * 0.6; // Fade in and out

			// Remove bubbles that are off-screen or expired
			if (bubble.y < -bubble.size || bubble.life >= bubble.maxLife) {
				this.bubbles.splice(i, 1);
			}
		}

		// Add new bubbles periodically
		if (this.bubbles.length < this.getNumBubbles() && Math.random() < 0.1) {
			this.bubbles.push(this.createBubble(dimensions));
		}
	}

	public draw(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
		if (!this.isInitialized) return;

		// Draw underwater background
		this.drawUnderwaterBackground(ctx, dimensions);

		// Draw bubbles
		this.drawBubbles(ctx, dimensions);

		// Draw light rays for high quality
		if (this.quality === 'high') {
			this.drawLightRays(ctx, dimensions);
		}
	}

	public setQuality(quality: QualityLevel): void {
		this.quality = quality;
		// Bubble count will naturally adjust through the update cycle
	}

	public setAccessibility(settings: AccessibilitySettings): void {
		this.accessibility = settings;
	}

	public cleanup(): void {
		this.bubbles = [];
		this.isInitialized = false;
	}

	public getMetrics(): PerformanceMetrics {
		return {
			fps: 60, // Estimated
			warnings: [],
			particleCount: this.bubbles.length,
		};
	}

	private getNumBubbles(): number {
		switch (this.quality) {
			case 'high':
				return 40;
			case 'medium':
				return 25;
			case 'low':
				return 15;
			case 'minimal':
				return 8;
			default:
				return 25;
		}
	}

	private createBubbles(count: number, dimensions: Dimensions): Bubble[] {
		const bubbles: Bubble[] = [];
		for (let i = 0; i < count; i++) {
			bubbles.push(this.createBubble(dimensions));
		}
		return bubbles;
	}

	private createBubble(dimensions: Dimensions): Bubble {
		const colorIndex = Math.floor(Math.random() * this.bubbleColors.length);
		const size = 10 + Math.random() * 30;

		// Ensure we always have a valid color
		const selectedColor = this.bubbleColors[colorIndex] ?? { r: 100, g: 200, b: 255 };

		return {
			x: Math.random() * dimensions.width,
			y: dimensions.height + size,
			size: size,
			speed: 0.5 + Math.random() * 2,
			opacity: 0.3 + Math.random() * 0.4,
			color: selectedColor,
			wobble: Math.random() * Math.PI * 2,
			wobbleSpeed: 0.02 + Math.random() * 0.03,
			life: 0,
			maxLife: 300 + Math.random() * 200,
		};
	}

	private drawUnderwaterBackground(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
		// Create underwater gradient
		const gradient = ctx.createLinearGradient(0, 0, 0, dimensions.height);
		gradient.addColorStop(0, 'rgb(20, 50, 80)'); // Lighter blue at top
		gradient.addColorStop(0.5, 'rgb(10, 30, 60)'); // Medium blue
		gradient.addColorStop(1, 'rgb(5, 15, 40)'); // Darker blue at bottom

		ctx.fillStyle = gradient;
		ctx.fillRect(0, 0, dimensions.width, dimensions.height);

		// Add subtle wave patterns
		this.drawWavePatterns(ctx, dimensions);
	}

	private drawWavePatterns(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
		ctx.save();
		ctx.globalAlpha = 0.1;

		for (let i = 0; i < 3; i++) {
			const waveY = dimensions.height * (0.2 + i * 0.3);
			const amplitude = 20 + i * 10;
			const frequency = 0.01 + i * 0.005;

			ctx.beginPath();
			ctx.moveTo(0, waveY);

			for (let x = 0; x <= dimensions.width; x += 5) {
				const y = waveY + Math.sin(x * frequency + this.animationTime * 2) * amplitude;
				ctx.lineTo(x, y);
			}

			ctx.lineTo(dimensions.width, dimensions.height);
			ctx.lineTo(0, dimensions.height);
			ctx.closePath();

			ctx.fillStyle = `rgba(100, 150, 200, ${0.1 - i * 0.02})`;
			ctx.fill();
		}

		ctx.restore();
	}

	private drawBubbles(ctx: CanvasRenderingContext2D, _dimensions: Dimensions): void {
		for (const bubble of this.bubbles) {
			ctx.save();
			ctx.globalAlpha = bubble.opacity;

			// Create bubble gradient for 3D effect
			const bubbleGradient = ctx.createRadialGradient(
				bubble.x - bubble.size * 0.3,
				bubble.y - bubble.size * 0.3,
				0,
				bubble.x,
				bubble.y,
				bubble.size
			);

			bubbleGradient.addColorStop(
				0,
				`rgba(${bubble.color.r}, ${bubble.color.g}, ${bubble.color.b}, 0.8)`
			);
			bubbleGradient.addColorStop(
				0.7,
				`rgba(${bubble.color.r}, ${bubble.color.g}, ${bubble.color.b}, 0.3)`
			);
			bubbleGradient.addColorStop(
				1,
				`rgba(${bubble.color.r}, ${bubble.color.g}, ${bubble.color.b}, 0.1)`
			);

			// Draw bubble
			ctx.fillStyle = bubbleGradient;
			ctx.beginPath();
			ctx.arc(bubble.x, bubble.y, bubble.size, 0, 2 * Math.PI);
			ctx.fill();

			// Draw bubble highlight
			ctx.fillStyle = `rgba(255, 255, 255, ${bubble.opacity * 0.6})`;
			ctx.beginPath();
			ctx.arc(
				bubble.x - bubble.size * 0.3,
				bubble.y - bubble.size * 0.3,
				bubble.size * 0.3,
				0,
				2 * Math.PI
			);
			ctx.fill();

			// Draw bubble outline
			ctx.strokeStyle = `rgba(${bubble.color.r}, ${bubble.color.g}, ${bubble.color.b}, ${bubble.opacity * 0.5})`;
			ctx.lineWidth = 1;
			ctx.beginPath();
			ctx.arc(bubble.x, bubble.y, bubble.size, 0, 2 * Math.PI);
			ctx.stroke();

			ctx.restore();
		}
	}

	private drawLightRays(ctx: CanvasRenderingContext2D, dimensions: Dimensions): void {
		ctx.save();
		ctx.globalAlpha = 0.15;

		// Draw animated light rays from top
		for (let i = 0; i < 5; i++) {
			const rayX = dimensions.width * (0.1 + i * 0.2);
			const rayWidth = 30 + Math.sin(this.animationTime + i) * 10;
			const rayOpacity = 0.1 + Math.sin(this.animationTime * 0.5 + i) * 0.05;

			const rayGradient = ctx.createLinearGradient(
				rayX - rayWidth / 2,
				0,
				rayX + rayWidth / 2,
				0
			);
			rayGradient.addColorStop(0, `rgba(255, 255, 200, 0)`);
			rayGradient.addColorStop(0.5, `rgba(255, 255, 200, ${rayOpacity})`);
			rayGradient.addColorStop(1, `rgba(255, 255, 200, 0)`);

			ctx.fillStyle = rayGradient;
			ctx.fillRect(rayX - rayWidth / 2, 0, rayWidth, dimensions.height);
		}

		ctx.restore();
	}
}
