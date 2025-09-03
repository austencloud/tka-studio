import type { Dimensions, GradientStop } from '../../types/types';

export function drawBackgroundGradient(
	ctx: CanvasRenderingContext2D,
	dimensions: Dimensions,
	gradientStops: GradientStop[]
): void {
	const gradient = ctx.createLinearGradient(0, 0, 0, dimensions.height);

	gradientStops.forEach((stop) => {
		gradient.addColorStop(stop.position, stop.color);
	});

	ctx.fillStyle = gradient;
	ctx.fillRect(0, 0, dimensions.width, dimensions.height);
}

export function calculateParticleCount(
	dimensions: Dimensions,
	baseDensity: number,
	quality: 'high' | 'medium' | 'low'
): number {
	let adjustedDensity = baseDensity;

	const screenSizeFactor = Math.min(1, (dimensions.width * dimensions.height) / (1920 * 1080));
	adjustedDensity *= screenSizeFactor;

	if (quality === 'low') {
		adjustedDensity *= 0.5;
	} else if (quality === 'medium') {
		adjustedDensity *= 0.75;
	}

	return Math.floor(dimensions.width * dimensions.height * adjustedDensity);
}

export function shouldEnableSeasonalFeatures(): boolean {
	const date = new Date();
	const month = date.getMonth();
	const day = date.getDate();

	return month === 11 || (month === 0 && day <= 7);
}
