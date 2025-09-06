export type Orientation = 'in' | 'out' | 'clock' | 'counter';
export type PropColor = 'blue' | 'red';
export type MotionType = 'pro' | 'anti' | 'float' | 'static' | 'dash';

export interface OrientationData {
	blue: Orientation;
	red: Orientation;
}

const ORIENTATION_TYPES: Orientation[] = ['in', 'out', 'clock', 'counter'];

export class OrientationCalculator {
	// Seed-based random for reproducibility
	private seededRandom(seed?: number): () => number {
		if (seed !== undefined) {
			let x = Math.sin(seed) * 10000;
			return () => {
				x = (x * 16807) % 2147483647;
				return (x - 1) / 2147483646;
			};
		}
		return Math.random;
	}

	generateOrientations(seed?: number): OrientationData {
		const randomFunc = this.seededRandom(seed);
		return {
			blue: this.randomOrientation(randomFunc),
			red: this.randomOrientation(randomFunc)
		};
	}

	private randomOrientation(randomFunc: () => number): Orientation {
		const index = Math.floor(randomFunc() * ORIENTATION_TYPES.length);
		return ORIENTATION_TYPES[index];
	}

	calculateEndOrientation(
		currentOrientation: OrientationData,
		motionType: MotionType,
		propColor: PropColor
	): Orientation {
		return this.transformOrientation(currentOrientation[propColor], motionType, propColor);
	}

	private transformOrientation(
		currentOrientation: Orientation,
		motionType: MotionType,
		propColor: PropColor
	): Orientation {
		switch (motionType) {
			case 'pro':
				return propColor === 'blue' ? 'clock' : 'counter';
			case 'anti':
				return propColor === 'blue' ? 'counter' : 'clock';
			case 'float':
				return 'in';
			case 'dash':
				return currentOrientation; // Maintain current orientation
			case 'static':
				return currentOrientation;
			default:
				return currentOrientation;
		}
	}

	mirrorOrientation(orientation: OrientationData): OrientationData {
		return {
			blue: this.mirrorSingleOrientation(orientation.blue),
			red: this.mirrorSingleOrientation(orientation.red)
		};
	}

	private mirrorSingleOrientation(orientation: Orientation): Orientation {
		const mirrorMap: Record<Orientation, Orientation> = {
			in: 'out',
			out: 'in',
			clock: 'counter',
			counter: 'clock'
		};
		return mirrorMap[orientation];
	}

	// Advanced: Complementary transformation
	complementOrientation(orientation: OrientationData): OrientationData {
		return {
			blue: this.complementSingleOrientation(orientation.blue),
			red: this.complementSingleOrientation(orientation.red)
		};
	}

	private complementSingleOrientation(orientation: Orientation): Orientation {
		const complementMap: Record<Orientation, Orientation> = {
			in: 'out',
			out: 'in',
			clock: 'counter',
			counter: 'clock'
		};
		return complementMap[orientation];
	}
}

export const orientationUtils = new OrientationCalculator();
