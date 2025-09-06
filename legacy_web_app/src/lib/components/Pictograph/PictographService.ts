// src/lib/services/PictographService.ts (Updated)
import type { PictographData } from '$lib/types/PictographData';
import type { PropData } from '$lib/components/objects/Prop/PropData';
import type { ArrowData } from '$lib/components/objects/Arrow/ArrowData';
import type { GridData } from '$lib/components/objects/Grid/GridData';
import type { MotionData } from '$lib/components/objects/Motion/MotionData';
import { PropType, type Color, type Loc } from '$lib/types/Types';

import { Motion } from '$lib/components/objects/Motion/Motion';
import { RED, BLUE, DASH } from '$lib/types/Constants';

import { PictographChecker } from './services/PictographChecker';
import { pictographContainer } from '$lib/state/stores/pictograph/pictographContainer';
import ArrowLocationManager from '$lib/components/objects/Arrow/ArrowLocationManager';
import ArrowRotAngleManager from '$lib/components/objects/Arrow/ArrowRotAngleManager';
import { LetterConditions } from './constants/LetterConditions';
import { ArrowPlacementManager } from '../objects/Arrow/ArrowPlacementManager';
import { BetaPropPositioner } from '../objects/Prop/PropPlacementManager/BetaPropPositioner';
import { LetterType } from '$lib/types/LetterType';

export class PictographService {
	private data: PictographData;
	private checker: PictographChecker;

	constructor(pictographData: PictographData) {
		this.data = pictographData;
		this.checker = new PictographChecker(pictographData);
		this.initialize();
	}

	private initialize(): void {
		try {
			this.initializeMotions();

			// Create a safe copy of the data without any Promise objects
			const safeData = this.createSafeDataCopy(this.data);

			// Update the container with the safe data
			pictographContainer.setData(safeData);
		} catch (error) {
			const errorMessage =
				error instanceof Error ? error.message : 'Pictograph initialization failed';
			pictographContainer.setError(errorMessage, 'initialization');
		}
	}

	/**
	 * Creates a safe copy of the data without any non-cloneable objects
	 * This prevents the DataCloneError when using structuredClone()
	 */
	private createSafeDataCopy(data: PictographData): PictographData {
		// Create a shallow copy first
		const safeCopy = { ...data };

		// Explicitly set Motion objects to null as they can't be cloned
		safeCopy.redMotion = null;
		safeCopy.blueMotion = null;

		// Handle any SVG data that might be present in arrow data
		if (safeCopy.redArrowData?.svgData) {
			// Create a safe copy of svgData without DOM elements
			const originalSvgData = safeCopy.redArrowData.svgData;
			// Use type assertion to handle properties that might not be in the type definition
			safeCopy.redArrowData.svgData = {
				...originalSvgData
			} as any;

			// Remove DOM elements and other non-serializable properties
			if ((safeCopy.redArrowData.svgData as any).element) {
				(safeCopy.redArrowData.svgData as any).element = null;
			}
			if ((safeCopy.redArrowData.svgData as any).paths) {
				(safeCopy.redArrowData.svgData as any).paths = null;
			}
		}

		if (safeCopy.blueArrowData?.svgData) {
			// Create a safe copy of svgData without DOM elements
			const originalSvgData = safeCopy.blueArrowData.svgData;
			// Use type assertion to handle properties that might not be in the type definition
			safeCopy.blueArrowData.svgData = {
				...originalSvgData
			} as any;

			// Remove DOM elements and other non-serializable properties
			if ((safeCopy.blueArrowData.svgData as any).element) {
				(safeCopy.blueArrowData.svgData as any).element = null;
			}
			if ((safeCopy.blueArrowData.svgData as any).paths) {
				(safeCopy.blueArrowData.svgData as any).paths = null;
			}
		}

		// Return the safe copy
		return safeCopy;
	}

	private initializeMotions(): void {
		if (this.data.redMotionData && !this.data.redMotion) {
			this.data.redMotion = new Motion(this.data, this.data.redMotionData);
		}
		if (this.data.blueMotionData && !this.data.blueMotion) {
			this.data.blueMotion = new Motion(this.data, this.data.blueMotionData);
		}
	}

	createPropData(motionData: MotionData, color: Color): PropData {
		// Find the corresponding motion object
		const motion = color === 'red' ? this.data.redMotion : this.data.blueMotion;

		// Use the motion's calculated end orientation
		const endOri = motion ? motion.calculateFinalEndOrientation() : motionData.endOri;
		const propData: PropData = {
			id: crypto.randomUUID(),
			motionId: motionData.id,
			color,
			propType: PropType.STAFF,
			ori: endOri,
			radialMode: ['in', 'out'].includes(endOri) ? 'radial' : 'nonradial',
			coords: { x: 0, y: 0 },
			loc: motionData.endLoc,
			rotAngle: 0
		};

		pictographContainer.updatePropData(color, propData);
		return propData;
	}
	createArrowData(motionData: MotionData, color: Color): ArrowData {
		const motion = color === 'red' ? this.data.redMotion : this.data.blueMotion;

		// Special handling for Type 3 motions with dash
		const letterType = this.data.letter ? LetterType.getLetterType(this.data.letter) : null;
		const isType3 = letterType === LetterType.Type3;
		const isDash = motionData.motionType === DASH;

		// Ensure the gridMode is set
		if (motion && !motion.gridMode && this.data.gridMode) {
			motion.gridMode = this.data.gridMode;
		}

		let arrowLoc;

		if (isType3 && isDash && motion) {
			// For Type 3 motions with dash, calculate the location based on the shift motion
			const locationManager = new ArrowLocationManager(this);



			arrowLoc =
				locationManager.getArrowLocation(
					motion,
					(m) => this.getOtherMotion(m),
					() => this.getShiftMotion(),
					this.data.letter
				) || motionData.endLoc;

		} else {
			// For other motions, use the standard calculation
			arrowLoc = motion
				? this.calculateArrowLocation(motion, motionData.endLoc)
				: motionData.endLoc;
		}

		const arrowData: ArrowData = {
			id: crypto.randomUUID(),
			motionId: motionData.id,
			color,
			coords: { x: 0, y: 0 },
			loc: arrowLoc,
			rotAngle: 0,
			svgMirrored: false,
			svgCenter: { x: 0, y: 0 },
			svgLoaded: false,
			svgData: null,
			...(({ id: _id, color: _color, ...rest }) => rest)(motionData)
		};

		pictographContainer.updateArrowData(color, arrowData);
		return arrowData;
	}

	private calculateArrowLocation(motion: Motion | null, defaultLoc: Loc): Loc {
		if (!motion) return defaultLoc;
		try {
			const locationManager = new ArrowLocationManager(this);
			return (
				locationManager.getArrowLocation(
					motion,
					(m) => this.getOtherMotion(m),
					() => this.getShiftMotion(),
					this.data.letter
				) ?? defaultLoc
			);
		} catch (error) {
			console.warn('Arrow location calculation failed:', error);
			return defaultLoc;
		}
	}

	positionComponents(
		redProp: PropData | null,
		blueProp: PropData | null,
		redArrow: ArrowData | null,
		blueArrow: ArrowData | null,
		grid: GridData
	): void {
		try {
			if (redProp) this.positionProp(redProp, grid);
			if (blueProp) this.positionProp(blueProp, grid);

			if (redProp && blueProp && this.checker.checkLetterCondition(LetterConditions.BETA_ENDING)) {
				new BetaPropPositioner(this.data).reposition([redProp, blueProp]);
			}

			this.positionArrows(redArrow, blueArrow, grid);
		} catch (error) {
			const errorMessage = error instanceof Error ? error.message : 'Component positioning failed';
			pictographContainer.setError(errorMessage, 'positioning');
		}
	}

	private positionProp(prop: PropData, grid: GridData): void {
		const pointName = `${prop.loc}_${this.data.gridMode}_hand_point`;
		prop.coords =
			grid.allHandPointsNormal?.[pointName]?.coordinates ?? this.getFallbackPosition(prop.loc);
	}

	private positionArrows(
		redArrow: ArrowData | null,
		blueArrow: ArrowData | null,
		grid: GridData
	): void {
		// Create a rotation angle manager once to be reused
		const rotAngleManager = new ArrowRotAngleManager(this.data, this);
		const locationManager = new ArrowLocationManager(this);

		// First, determine the arrow locations
		if (redArrow && this.data.redMotion) {
			// Recalculate the arrow location for Type 3 motions
			const letterType = this.data.letter ? LetterType.getLetterType(this.data.letter) : null;
			const isType3 = letterType === LetterType.Type3;

			if (isType3 && this.data.redMotion.motionType === DASH) {
				try {
					// For Type 3 dash motions, recalculate the location
					const arrowLoc = locationManager.getArrowLocation(
						this.data.redMotion,
						(m) => this.getOtherMotion(m),
						() => this.getShiftMotion(),
						this.data.letter
					);

					if (arrowLoc) {
						redArrow.loc = arrowLoc;
					} else {
						console.warn(
							'Failed to recalculate Type 3 red dash arrow location, keeping original location'
						);
					}
				} catch (error) {
					console.error('Error recalculating Type 3 red dash arrow location:', error);
				}
			}
		}

		if (blueArrow && this.data.blueMotion) {
			// Recalculate the arrow location for Type 3 motions
			const letterType = this.data.letter ? LetterType.getLetterType(this.data.letter) : null;
			const isType3 = letterType === LetterType.Type3;

			if (isType3 && this.data.blueMotion.motionType === DASH) {
				try {
					// For Type 3 dash motions, recalculate the location
					const arrowLoc = locationManager.getArrowLocation(
						this.data.blueMotion,
						(m) => this.getOtherMotion(m),
						() => this.getShiftMotion(),
						this.data.letter
					);

					if (arrowLoc) {
						blueArrow.loc = arrowLoc;
					} else {
						console.warn(
							'Failed to recalculate Type 3 blue dash arrow location, keeping original location'
						);
					}
				} catch (error) {
					console.error('Error recalculating Type 3 blue dash arrow location:', error);
				}
			}
		}

		// Next, update arrow placements
		if (redArrow || blueArrow) {
			try {
				const placementManager = new ArrowPlacementManager({
					pictographData: this.data,
					gridData: grid,
					checker: this.checker
				});

				const arrows = [redArrow, blueArrow].filter(Boolean) as ArrowData[];

				placementManager.updateArrowPlacements(arrows);

				// After updating placements, recalculate rotation angles
				// This ensures the angles are correct after any layout shifts
				if (redArrow && this.data.redMotion && redArrow.loc) {
					redArrow.rotAngle = rotAngleManager.calculateRotationAngle(
						this.data.redMotion,
						redArrow.loc
					);
				}

				if (blueArrow && this.data.blueMotion && blueArrow.loc) {
					blueArrow.rotAngle = rotAngleManager.calculateRotationAngle(
						this.data.blueMotion,
						blueArrow.loc
					);
				}
			} catch (error) {
				console.warn('Advanced arrow placement failed:', error);

				// Even if placement fails, still try to calculate rotation angles
				if (redArrow && this.data.redMotion && redArrow.loc) {
					redArrow.rotAngle = rotAngleManager.calculateRotationAngle(
						this.data.redMotion,
						redArrow.loc
					);
				}

				if (blueArrow && this.data.blueMotion && blueArrow.loc) {
					blueArrow.rotAngle = rotAngleManager.calculateRotationAngle(
						this.data.blueMotion,
						blueArrow.loc
					);
				}
			}
		}
	}

	private getFallbackPosition(loc?: string): { x: number; y: number } {
		const fallbackPositions: Record<string, { x: number; y: number }> = {
			n: { x: 475, y: 330 },
			e: { x: 620, y: 475 },
			s: { x: 475, y: 620 },
			w: { x: 330, y: 475 },
			ne: { x: 620, y: 330 },
			se: { x: 620, y: 620 },
			sw: { x: 330, y: 620 },
			nw: { x: 330, y: 330 }
		};

		return loc && fallbackPositions[loc] ? fallbackPositions[loc] : { x: 475, y: 475 };
	}

	getShiftMotion(): Motion | null {
		const motions = [this.data.redMotion, this.data.blueMotion].filter((m): m is Motion => !!m);

		// Find the shift motion
		const shiftMotion =
			motions.find((m) => ['pro', 'anti', 'float'].includes(m.motionType)) ?? null;

		// Ensure the gridMode is set on the shift motion
		if (shiftMotion && !shiftMotion.gridMode && this.data.gridMode) {
			shiftMotion.gridMode = this.data.gridMode;
		}

		return shiftMotion;
	}

	getOtherMotion(motion: Motion): Motion | null {
		if (!motion) return null;
		const otherColor = motion.color === RED ? BLUE : RED;
		const otherMotion =
			otherColor === RED ? (this.data.redMotion ?? null) : (this.data.blueMotion ?? null);

		// Ensure the gridMode is set on the other motion
		if (otherMotion && !otherMotion.gridMode && this.data.gridMode) {
			otherMotion.gridMode = this.data.gridMode;
		}

		return otherMotion;
	}

	// Getter for the pictograph data
	getData(): PictographData {
		return this.data;
	}

	updateData(newData: PictographData): void {
		try {
			// Check if this is a layout shift update
			// We can detect this by looking at the stack trace for affected beats
			const stackTrace = new Error().stack || '';
			const isLayoutShift =
				stackTrace.includes('Beat 4') ||
				stackTrace.includes('Beat 5') ||
				stackTrace.includes('Beat 9') ||
				stackTrace.includes('Beat 10');

			// Also check for grid changes that indicate layout shifts
			// Use type assertion to avoid TypeScript errors since these properties might be added dynamically
			const oldGridData = this.data?.gridData as any;
			const newGridData = newData.gridData as any;
			const isGridChanged =
				oldGridData?.cellSize !== newGridData?.cellSize ||
				oldGridData?.width !== newGridData?.width ||
				oldGridData?.height !== newGridData?.height;

			// Combine both checks
			const shouldForceReset = isLayoutShift || isGridChanged;

			if (shouldForceReset) {


				// For layout shifts, we need to ensure the arrows are completely recreated
				// This is the key to fixing the issue
				if (newData.redArrowData) {
					// Force recalculation of rotation angle
					if (newData.redMotion) {
						const rotAngleManager = new ArrowRotAngleManager(newData, this);
						newData.redArrowData.rotAngle = rotAngleManager.calculateRotationAngle(
							newData.redMotion,
							newData.redArrowData.loc,
							newData.redArrowData.svgMirrored
						);
					}

					// Ensure the motion type is correct
					if (newData.redMotion && newData.redMotionData) {
						if (newData.redArrowData.motionType !== newData.redMotionData.motionType) {

							newData.redArrowData.motionType = newData.redMotionData.motionType;
						}
					}
				}

				if (newData.blueArrowData) {
					// Force recalculation of rotation angle
					if (newData.blueMotion) {
						const rotAngleManager = new ArrowRotAngleManager(newData);
						newData.blueArrowData.rotAngle = rotAngleManager.calculateRotationAngle(
							newData.blueMotion,
							newData.blueArrowData.loc,
							newData.blueArrowData.svgMirrored
						);

					}

					// Ensure the motion type is correct
					if (newData.blueMotion && newData.blueMotionData) {
						if (newData.blueArrowData.motionType !== newData.blueMotionData.motionType) {

							newData.blueArrowData.motionType = newData.blueMotionData.motionType;
						}
					}
				}
			} else {
				// Preserve motion types from the current data if they exist
				if (this.data) {
					// Preserve red motion type if it exists
					if (this.data.redMotionData?.motionType && newData.redMotionData) {
						newData.redMotionData.motionType = this.data.redMotionData.motionType;
					}

					// Preserve blue motion type if it exists
					if (this.data.blueMotionData?.motionType && newData.blueMotionData) {
						newData.blueMotionData.motionType = this.data.blueMotionData.motionType;
					}
				}
			}

			this.data = newData;
			this.checker = new PictographChecker(newData);
			this.initialize();
		} catch (error) {
			console.error('Error in PictographService.updateData:', error);

			// Handle the error gracefully
			const errorMessage =
				error instanceof Error ? error.message : 'Failed to update pictograph data';
			pictographContainer.setError(errorMessage, 'update');
		}
	}
}
