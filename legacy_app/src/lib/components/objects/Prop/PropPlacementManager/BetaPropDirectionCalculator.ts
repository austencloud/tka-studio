import { Letter } from '$lib/types/Letter';
import {
	NORTH,
	EAST,
	SOUTH,
	WEST,
	NORTHEAST,
	SOUTHEAST,
	SOUTHWEST,
	NORTHWEST,
	RED,
	BLUE,
	RADIAL,
	NONRADIAL,
	IN,
	OUT,
	CLOCK,
	COUNTER,
	LEFT,
	RIGHT,
	UP,
	DOWN,
	UPRIGHT,
	UPLEFT,
	DOWNRIGHT,
	DOWNLEFT,
	PRO,
	ANTI,
	FLOAT,
	DIAMOND,
	BOX
} from '$lib/types/Constants';
import type { BoxLoc, Color, DiamondLoc, Direction, Loc } from '$lib/types/Types';
import type { PictographData } from '$lib/types/PictographData';
import type { PropData } from '$lib/components/objects/Prop/PropData';
import type { MotionData } from '$lib/components/objects/Motion/MotionData';

export class BetaPropDirectionCalculator {
	// Special case maps for Letter I
	private directionMapRadialI: Record<Loc, Record<Color, Direction>> = {
		[NORTH]: { [RED]: RIGHT, [BLUE]: LEFT },
		[EAST]: { [RED]: DOWN, [BLUE]: UP },
		[SOUTH]: { [RED]: LEFT, [BLUE]: RIGHT },
		[WEST]: { [RED]: DOWN, [BLUE]: UP },
		[NORTHEAST]: { [RED]: DOWNRIGHT, [BLUE]: UPLEFT },
		[SOUTHEAST]: { [RED]: UPRIGHT, [BLUE]: DOWNLEFT },
		[SOUTHWEST]: { [RED]: DOWNRIGHT, [BLUE]: UPLEFT },
		[NORTHWEST]: { [RED]: UPRIGHT, [BLUE]: DOWNLEFT }
	};

	private directionMapNonRadialI: Record<Loc, Record<Color, Direction>> = {
		[NORTH]: { [RED]: UP, [BLUE]: DOWN },
		[EAST]: { [RED]: RIGHT, [BLUE]: LEFT },
		[SOUTH]: { [RED]: DOWN, [BLUE]: UP },
		[WEST]: { [RED]: RIGHT, [BLUE]: LEFT },
		[NORTHEAST]: { [RED]: UPRIGHT, [BLUE]: DOWNLEFT },
		[SOUTHEAST]: { [RED]: DOWNRIGHT, [BLUE]: UPLEFT },
		[SOUTHWEST]: { [RED]: UPRIGHT, [BLUE]: DOWNLEFT },
		[NORTHWEST]: { [RED]: DOWNRIGHT, [BLUE]: UPLEFT }
	};

	// Shift direction maps
	private directionMapRadialShift: Record<Loc, Partial<Record<Loc, Direction>>> = {
		[EAST]: { [NORTH]: RIGHT, [SOUTH]: RIGHT },
		[WEST]: { [NORTH]: LEFT, [SOUTH]: LEFT },
		[NORTH]: { [EAST]: UP, [WEST]: UP },
		[SOUTH]: { [EAST]: DOWN, [WEST]: DOWN },
		[NORTHEAST]: { [NORTHWEST]: UPRIGHT, [SOUTHEAST]: UPRIGHT },
		[SOUTHEAST]: { [NORTHEAST]: DOWNRIGHT, [SOUTHWEST]: DOWNRIGHT },
		[SOUTHWEST]: { [NORTHWEST]: DOWNLEFT, [SOUTHEAST]: DOWNLEFT },
		[NORTHWEST]: { [NORTHEAST]: UPLEFT, [SOUTHWEST]: UPLEFT }
	};

	private directionMapNonRadialShift: Record<Loc, Partial<Record<Loc, Direction>>> = {
		[EAST]: { [NORTH]: UP, [SOUTH]: UP },
		[WEST]: { [NORTH]: DOWN, [SOUTH]: DOWN },
		[NORTH]: { [EAST]: RIGHT, [WEST]: RIGHT },
		[SOUTH]: { [EAST]: LEFT, [WEST]: LEFT },
		[NORTHEAST]: { [SOUTHEAST]: UPLEFT, [NORTHWEST]: DOWNRIGHT },
		[SOUTHEAST]: { [NORTHEAST]: UPRIGHT, [SOUTHWEST]: DOWNLEFT },
		[SOUTHWEST]: { [NORTHWEST]: UPRIGHT, [SOUTHEAST]: DOWNRIGHT },
		[NORTHWEST]: { [SOUTHWEST]: UPLEFT, [NORTHEAST]: DOWNLEFT }
	};

	// Static/dash maps
	private diamondMapRadial: Record<DiamondLoc, Record<Color, Direction>> = {
		[NORTH]: { [RED]: RIGHT, [BLUE]: LEFT },
		[EAST]: { [RED]: DOWN, [BLUE]: UP },
		[SOUTH]: { [RED]: RIGHT, [BLUE]: LEFT },
		[WEST]: { [RED]: DOWN, [BLUE]: UP }
	};

	private diamondMapNonRadial: Record<DiamondLoc, Record<Color, Direction>> = {
		[NORTH]: { [RED]: UP, [BLUE]: DOWN },
		[EAST]: { [RED]: RIGHT, [BLUE]: LEFT },
		[SOUTH]: { [RED]: DOWN, [BLUE]: UP },
		[WEST]: { [RED]: RIGHT, [BLUE]: LEFT }
	};

	private boxMapRadial: Record<BoxLoc, Record<Color, Direction>> = {
		[NORTHEAST]: { [RED]: DOWNRIGHT, [BLUE]: UPLEFT },
		[SOUTHEAST]: { [RED]: UPRIGHT, [BLUE]: DOWNLEFT },
		[SOUTHWEST]: { [RED]: DOWNRIGHT, [BLUE]: UPLEFT },
		[NORTHWEST]: { [RED]: UPRIGHT, [BLUE]: DOWNLEFT }
	};

	private boxMapNonRadial: Record<BoxLoc, Record<Color, Direction>> = {
		[NORTHEAST]: { [RED]: UPRIGHT, [BLUE]: DOWNLEFT },
		[SOUTHEAST]: { [RED]: DOWNRIGHT, [BLUE]: UPLEFT },
		[SOUTHWEST]: { [RED]: UPRIGHT, [BLUE]: DOWNLEFT },
		[NORTHWEST]: { [RED]: DOWNRIGHT, [BLUE]: UPLEFT }
	};

	constructor(private pictographData: PictographData) {}

	getDirection(prop: PropData): Direction | null {
		// Special handling for G and H letters

		if (this.pictographData.letter === Letter.G || this.pictographData.letter === Letter.H) {
			const redMotion = this.pictographData.redMotionData;

			// Only do special handling for the red and blue props
			if (redMotion && (prop.color === RED || prop.color === BLUE)) {

				// Get direction from red motion, not from prop
				let motionDirection: Direction | null = null;

				if ([PRO, ANTI, FLOAT].includes(redMotion.motionType)) {
					const isRadial = this.endsWithRadialOrientation();
					motionDirection = this.getShiftDirection(isRadial, redMotion.startLoc, redMotion.endLoc);
				} else {
					// For static/dash motion
					const loc = redMotion.startLoc;
					const propColor = redMotion.color;
					const isDiamond = ['n', 's', 'e', 'w'].includes(loc);
					const isRadial = this.endsWithRadialOrientation();

					if (isDiamond) {
						const map = isRadial ? this.diamondMapRadial : this.diamondMapNonRadial;
						motionDirection = map[loc as DiamondLoc][propColor as Color];
					} else {
						const map = isRadial ? this.boxMapRadial : this.boxMapNonRadial;
						motionDirection = map[loc as BoxLoc][propColor as Color];
					}
				}

				if (!motionDirection) {
					console.warn('Could not determine motion direction for G/H');
					return null;
				}

				// For red prop, return the motion direction
				// For blue prop, return the opposite direction
				return prop.color === RED ? motionDirection : this.getOppositeDirection(motionDirection);
			}
		}


		// Default behavior for other letters
		const motionData = this.getMotionDataForProp(prop);
		if (!motionData) {
			console.error(`No motion data found for prop ${prop.id}`);
			return null;
		}

		if ([PRO, ANTI, FLOAT].includes(motionData.motionType)) {
			return this.handleShiftMotion(prop, motionData);
		}
		return this.handleStaticDashMotion(prop);
	}

	// Helper method to get the associated motion data for a prop
	private getMotionDataForProp(prop: PropData): MotionData | null {
		if (prop.color === RED) {
			return this.pictographData.redMotionData;
		} else if (prop.color === BLUE) {
			return this.pictographData.blueMotionData;
		}
		return null;
	}

	endsWithRadialOrientation(): boolean {
		return (
			((this.pictographData.redMotionData?.endOri === IN ||
				this.pictographData.redMotionData?.endOri === OUT) &&
				this.pictographData.blueMotionData?.endOri === IN) ||
			this.pictographData.blueMotionData?.endOri === OUT
		);
	}

	endsWithNonRadialOrientation(): boolean {
		return (
			((this.pictographData.redMotionData?.endOri === CLOCK ||
				this.pictographData.redMotionData?.endOri === COUNTER) &&
				this.pictographData.blueMotionData?.endOri === CLOCK) ||
			this.pictographData.blueMotionData?.endOri === COUNTER
		);
	}

	private handleShiftMotion(prop: PropData, motionData: MotionData): Direction | null {
		if (this.pictographData.letter === Letter.I) {
			if (this.endsWithRadialOrientation()) {
				return this.directionMapRadialI[prop.loc as Loc][prop.color as Color];
			}
			if (this.endsWithNonRadialOrientation()) {
				return this.directionMapNonRadialI[prop.loc as Loc][prop.color as Color];
			}
		}

		const isRadial = prop.radialMode === RADIAL;
		return this.getShiftDirection(isRadial, motionData.startLoc, prop.loc);
	}

	private getShiftDirection(isRadial: boolean, startLoc: Loc, endLoc: Loc): Direction | null {
		const map = isRadial ? this.directionMapRadialShift : this.directionMapNonRadialShift;
		return map[startLoc]?.[endLoc] ?? null;
	}

	private handleStaticDashMotion(prop: PropData): Direction {
		const gridMode = [NORTH, SOUTH, EAST, WEST].includes(prop.loc) ? DIAMOND : BOX;
		const isRadial = prop.radialMode === RADIAL;

		if (gridMode === DIAMOND) {
			const map = isRadial ? this.diamondMapRadial : this.diamondMapNonRadial;
			return map[prop.loc as DiamondLoc][prop.color as Color];
		}

		const map = isRadial ? this.boxMapRadial : this.boxMapNonRadial;
		return map[prop.loc as BoxLoc][prop.color as Color];
	}

	getOppositeDirection(direction: Direction): Direction {
		const opposites: Record<Direction, Direction> = {
			[UP]: DOWN,
			[DOWN]: UP,
			[LEFT]: RIGHT,
			[RIGHT]: LEFT,
			[UPRIGHT]: DOWNLEFT,
			[DOWNLEFT]: UPRIGHT,
			[UPLEFT]: DOWNRIGHT,
			[DOWNRIGHT]: UPLEFT
		};
		return opposites[direction];
	}
	getDirectionFromMotion(motion: MotionData): Direction | null {
		if (!motion) return null;

		// For shift motions (pro, anti, float), we need to determine the direction
		// based on start and end locations
		if (['pro', 'anti', 'float'].includes(motion.motionType)) {
			const isRadial = this.endsWithRadialOrientation();
			return this.getShiftDirection(isRadial, motion.startLoc, motion.endLoc);
		}

		// For static/dash, determine based on the motion's location and color
		const propColor = motion.color;
		const loc = motion.startLoc; // Use startLoc for static/dash

		const isDiamond = ['n', 's', 'e', 'w'].includes(loc);
		const isRadial = this.endsWithRadialOrientation();

		if (isDiamond) {
			const map = isRadial ? this.diamondMapRadial : this.diamondMapNonRadial;
			return map[loc as DiamondLoc][propColor as Color];
		} else {
			const map = isRadial ? this.boxMapRadial : this.boxMapNonRadial;
			return map[loc as BoxLoc][propColor as Color];
		}
	}
}
