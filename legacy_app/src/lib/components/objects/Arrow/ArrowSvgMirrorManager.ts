// src/lib/components/objects/Arrow/ArrowSvgMirrorManager.ts
import { ANTI, CLOCKWISE, COUNTER_CLOCKWISE, NO_ROT, DASH, STATIC } from '$lib/types/Constants';
import type { ArrowData } from './ArrowData';

export default class ArrowSvgMirrorManager {
	private arrow: ArrowData;

	constructor(arrow: ArrowData) {
		this.arrow = arrow;
		this.updateMirror(); // Initialize mirroring state immediately
	}

	/**
	 * Updates the mirrored state of the arrow based on motion type and rotation direction.
	 * Also handles updating SVG center points for proper coordinate calculations.
	 */
	updateMirror(): void {
		// Skip mirroring for no rotation
		if (this.arrow.propRotDir === NO_ROT) {
			this.arrow.svgMirrored = false;
			return;
		}

		// Define mirror conditions lookup table
		const mirrorConditions: { [key: string]: { [key: string]: boolean } } = {
			[ANTI]: {
				[CLOCKWISE]: true,
				[COUNTER_CLOCKWISE]: false
			},
			// Default conditions for other motion types
			other: {
				[CLOCKWISE]: false,
				[COUNTER_CLOCKWISE]: true
			}
		};

		const motionType = this.arrow.motionType;
		const propRotDir = this.arrow.propRotDir;

		// Previous mirrored state - needed to detect changes
		const wasMirrored = this.arrow.svgMirrored;

		// Look up in the mirror conditions table
		if (motionType in mirrorConditions) {
			// If we have specific rules for this motion type, use them
			this.arrow.svgMirrored = mirrorConditions[motionType][propRotDir] || false;
		} else {
			// Otherwise use the default rules
			this.arrow.svgMirrored = mirrorConditions.other[propRotDir] || false;
		}

		// Special case handling for specific motion types when needed
		// ...

		// Update SVG center point when SVG data is available
		// This is critical for proper coordinate calculations when mirroring
		if (this.arrow.svgData) {
			if (this.arrow.svgMirrored) {
				// Store mirrored center for mirrored arrows
				this.arrow.svgCenter = {
					x: this.arrow.svgData.viewBox.width - this.arrow.svgData.center.x,
					y: this.arrow.svgData.center.y
				};
			} else {
				// Use original center for normal arrows
				this.arrow.svgCenter = { ...this.arrow.svgData.center };
			}
		}
	}
}
