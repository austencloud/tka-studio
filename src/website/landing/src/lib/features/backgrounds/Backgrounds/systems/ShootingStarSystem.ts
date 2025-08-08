// src/lib/components/Backgrounds/systems/ShootingStarSystem.ts
import type { Dimensions, ShootingStar, ShootingStarState } from '../types/types';
import { SnowfallConfig } from '../config';

export const createShootingStarSystem = () => {
	const config = SnowfallConfig.shootingStar;

	function getRandomInterval(): number {
		return (
			Math.floor(Math.random() * (config.maxInterval - config.minInterval + 1)) + config.minInterval
		);
	}

	function randomFloat(min: number, max: number): number {
		return Math.random() * (max - min) + min;
	}

	function getRandomColor(): string {
		return config.colors[Math.floor(Math.random() * config.colors.length)];
	}

	const spawnShootingStar = ({ width, height }: Dimensions): ShootingStar => {
		const middleY = height / 2;

		const startOptions = [
			{ x: -0.1 * width, y: randomFloat(0.2, 0.8) * height },
			{ x: 1.1 * width, y: randomFloat(0.2, 0.8) * height }
		];
		const startPos = startOptions[Math.floor(Math.random() * startOptions.length)];

		let dx = randomFloat(0.3, 0.5) * (startPos.x > 0 ? -1 : 1);
		let dy = Math.random() < 0.5 ? -randomFloat(0.05, 0.2) : randomFloat(0.05, 0.2);

		if (startPos.y > middleY) dy -= randomFloat(0.02, 0.05);
		else dy += randomFloat(0.02, 0.05);

		const norm = Math.sqrt(dx * dx + dy * dy);
		dx /= norm;
		dy /= norm;

		return {
			x: startPos.x,
			y: startPos.y,
			dx,
			dy,
			size: randomFloat(config.minSize, config.maxSize),
			speed: randomFloat(config.minSpeed, config.maxSpeed),
			tail: [],
			prevX: startPos.x,
			prevY: startPos.y,
			tailLength: Math.floor(randomFloat(config.tailLength.min, config.tailLength.max)),
			opacity: 1.0,
			offScreen: false,
			color: getRandomColor(),
			twinkle: Math.random() < config.twinkleChance
		};
	};

	const updateShootingStar = (
		star: ShootingStar | null,
		{ width, height }: Dimensions
	): ShootingStar | null => {
		if (!star) return null;

		const newX = star.x + star.dx * star.speed * width;
		const newY = star.y + star.dy * star.speed * height;

		const steps = 5;
		const newTail = [...star.tail];

		for (let i = 0; i < steps; i++) {
			const interpX = star.prevX + (newX - star.prevX) * (i / steps);
			const interpY = star.prevY + (newY - star.prevY) * (i / steps);
			newTail.push({
				x: interpX,
				y: interpY,
				size: star.size * 0.8,
				color: star.color
			});
		}

		if (newTail.length > star.tailLength * steps) {
			newTail.splice(0, steps);
		}

		const offScreen =
			newX < -width * 0.1 || newX > width * 1.1 || newY < -height * 0.1 || newY > height * 1.1;

		let opacity = star.opacity;
		if (offScreen) {
			opacity -= config.fadeRate;
			if (opacity <= 0) return null;
		}

		return {
			...star,
			x: newX,
			y: newY,
			prevX: star.x,
			prevY: star.y,
			tail: newTail,
			offScreen,
			opacity
		};
	};

	const drawShootingStar = (star: ShootingStar | null, ctx: CanvasRenderingContext2D): void => {
		if (!star || !ctx) return;

		ctx.save();
		const tailLength = star.tail.length;

		star.tail.forEach((segment, index) => {
			const fadeFactor = 5;
			const opacity = Math.max(0, ((index + 1) / tailLength) ** fadeFactor * star.opacity);

			ctx.globalAlpha = opacity;
			ctx.beginPath();
			ctx.arc(segment.x, segment.y, segment.size, 0, Math.PI * 2);
			ctx.fillStyle = segment.color;
			ctx.fill();
		});

		ctx.globalAlpha = star.opacity;
		ctx.beginPath();
		ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
		ctx.fillStyle = star.color;

		if (star.twinkle && Math.random() > 0.5) {
			ctx.shadowColor = star.color;
			ctx.shadowBlur = star.size / 2;
		}

		ctx.fill();
		ctx.restore();
	};

	const update = (state: ShootingStarState, dimensions: Dimensions): ShootingStarState => {
		const timer = state.timer + 1;

		if (!state.star && timer >= state.interval) {
			return {
				star: spawnShootingStar(dimensions),
				timer: 0,
				interval: getRandomInterval()
			};
		}

		return {
			star: updateShootingStar(state.star, dimensions),
			timer: state.star ? timer : 0,
			interval: state.interval
		};
	};

	return {
		initialState: { star: null, timer: 0, interval: getRandomInterval() },
		update,
		draw: (state: ShootingStarState, ctx: CanvasRenderingContext2D): void => {
			if (state.star && ctx) drawShootingStar(state.star, ctx);
		}
	};
};
