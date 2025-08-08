// src/lib/components/Backgrounds/systems/SnowflakeSystem.ts
import type { Dimensions, Snowflake } from '../types/types';
import { SnowfallConfig } from '../config';

export const createSnowflakeSystem = () => {
	const config = SnowfallConfig;
	let windStrength = 0;
	let windChangeTimer = 0;
	let currentQuality = 'medium'; // Add missing variable declaration

	const generateSnowflakeShape = (size: number): Path2D => {
		const path = new Path2D();
		const spikes = 6 + Math.floor(Math.random() * 4);

		for (let i = 0; i < spikes; i++) {
			const angle = (i * Math.PI * 2) / spikes;
			const outerX = Math.cos(angle) * size;
			const outerY = Math.sin(angle) * size;
			path.lineTo(outerX, outerY);

			const innerX = Math.cos(angle + Math.PI / spikes) * size * 0.2;
			const innerY = Math.sin(angle + Math.PI / spikes) * size * 0.2;
			path.lineTo(innerX, innerY);
		}
		path.closePath();
		return path;
	};

	const randomSnowflakeColor = (): string => {
		return config.snowflake.colors[Math.floor(Math.random() * config.snowflake.colors.length)];
	};

	const createSnowflake = (width: number, height: number): Snowflake => {
		const size =
			Math.random() * (config.snowflake.maxSize - config.snowflake.minSize) +
			config.snowflake.minSize;
		return {
			x: Math.random() * width,
			y: Math.random() * height,
			speed:
				Math.random() * (config.snowflake.maxSpeed - config.snowflake.minSpeed) +
				config.snowflake.minSpeed,
			size,
			sway: Math.random() * 1 - 0.5,
			opacity: Math.random() * 0.8 + 0.2,
			shape: generateSnowflakeShape(size),
			color: randomSnowflakeColor()
		};
	};

	const initialize = ({ width, height }: Dimensions, quality: string): Snowflake[] => {
		currentQuality = quality;
		let adjustedDensity = config.snowflake.density;

		const screenSizeFactor = Math.min(1, (width * height) / (1920 * 1080));
		adjustedDensity *= screenSizeFactor;

		// Apply quality density adjustments
		if (quality === 'low') {
			adjustedDensity *= 0.5;
		} else if (quality === 'medium') {
			adjustedDensity *= 0.75;
		}

		const count = Math.floor(width * height * adjustedDensity);
		return Array.from({ length: count }, () => createSnowflake(width, height));
	};

	const update = (flakes: Snowflake[], { width, height }: Dimensions): Snowflake[] => {
		windChangeTimer++;
		if (windChangeTimer >= config.snowflake.windChangeInterval) {
			windChangeTimer = 0;
			windStrength = (Math.random() * 0.5 - 0.25) * width * 0.00005;
		}

		return flakes.map((flake) => {
			const newX = flake.x + flake.sway + windStrength;
			const newY = flake.y + flake.speed;

			if (newY > height) {
				return {
					...flake,
					y: Math.random() * -20,
					x: Math.random() * width
				};
			}

			if (newX > width || newX < 0) {
				return {
					...flake,
					x: Math.random() * width
				};
			}

			return { ...flake, x: newX, y: newY };
		});
	};

	const draw = (
		flakes: Snowflake[],
		ctx: CanvasRenderingContext2D,
		{ width, height }: Dimensions
	): void => {
		if (!ctx) return;
		ctx.globalAlpha = 1.0;

		const colorGroups = new Map<string, Snowflake[]>();

		flakes.forEach((flake) => {
			if (!colorGroups.has(flake.color)) {
				colorGroups.set(flake.color, []);
			}
			colorGroups.get(flake.color)!.push(flake);
		});

		colorGroups.forEach((groupFlakes, color) => {
			ctx.fillStyle = color;

			groupFlakes.forEach((flake) => {
				ctx.save();
				ctx.translate(flake.x, flake.y);
				ctx.globalAlpha = flake.opacity;
				ctx.fill(flake.shape);
				ctx.restore();
			});
		});
	};

	const adjustToResize = (
		flakes: Snowflake[],
		oldDimensions: Dimensions,
		newDimensions: Dimensions,
		quality: string
	): Snowflake[] => {
		const targetCount = Math.floor(
			newDimensions.width *
				newDimensions.height *
				config.snowflake.density *
				(quality === 'low' ? 0.5 : quality === 'medium' ? 0.75 : 1)
		);

		const currentCount = flakes.length;

		if (targetCount > currentCount) {
			return [
				...flakes,
				...Array.from({ length: targetCount - currentCount }, () =>
					createSnowflake(newDimensions.width, newDimensions.height)
				)
			];
		} else if (targetCount < currentCount) {
			return flakes.slice(0, targetCount);
		}

		return flakes;
	};

	const setQuality = (_quality: string): void => {
		// Quality setting functionality can be implemented here if needed
	};

	return {
		initialize,
		update,
		draw,
		adjustToResize,
		setQuality
	};
};
