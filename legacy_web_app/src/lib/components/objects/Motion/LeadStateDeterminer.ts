import type { MotionData } from './MotionData';
import { HandpathCalculator } from './HandpathCalculator';
import type { Loc } from '$lib/types/Types';

export class LeadStateDeterminer {
	private redMotionData: MotionData;
	private blueMotionData: MotionData;
	private handpathCalculator: HandpathCalculator;

	constructor(redMotionData: MotionData, blueMotionData: MotionData) {
		this.redMotionData = redMotionData;
		this.blueMotionData = blueMotionData;
		this.handpathCalculator = new HandpathCalculator();
	}

	private static CLOCKWISE_ORDER: Loc[] = ['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w'];

	private isClockwiseAhead(startA: Loc, startB: Loc): boolean {
		const idxA = LeadStateDeterminer.CLOCKWISE_ORDER.indexOf(startA);
		const idxB = LeadStateDeterminer.CLOCKWISE_ORDER.indexOf(startB);
		return (
			(idxA - idxB + LeadStateDeterminer.CLOCKWISE_ORDER.length) %
				LeadStateDeterminer.CLOCKWISE_ORDER.length >
			0
		);
	}

	private isCounterClockwiseAhead(startA: Loc, startB: Loc): boolean {
		const idxA = LeadStateDeterminer.CLOCKWISE_ORDER.indexOf(startA);
		const idxB = LeadStateDeterminer.CLOCKWISE_ORDER.indexOf(startB);
		return (
			(idxB - idxA + LeadStateDeterminer.CLOCKWISE_ORDER.length) %
				LeadStateDeterminer.CLOCKWISE_ORDER.length >
			0
		);
	}

	private determineMotionOrder(trailing: boolean): MotionData {
		const redStart = this.redMotionData.startLoc;
		const redEnd = this.redMotionData.endLoc;
		const blueStart = this.blueMotionData.startLoc;
		const blueEnd = this.blueMotionData.endLoc;

		const redHandpath = this.handpathCalculator.getHandRotDir(redStart, redEnd);
		const blueHandpath = this.handpathCalculator.getHandRotDir(blueStart, blueEnd);

		if (redHandpath !== blueHandpath) {
			throw new Error(
				'Motions have different directions and cannot determine lead/trailing state.'
			);
		}

		if (redEnd === blueStart) {
			return trailing ? this.redMotionData : this.blueMotionData;
		}

		if (blueEnd === redStart) {
			return trailing ? this.blueMotionData : this.redMotionData;
		}

		if (redHandpath === 'cw_shift') {
			return this.isClockwiseAhead(blueStart, redStart)
				? trailing
					? this.redMotionData
					: this.blueMotionData
				: trailing
					? this.blueMotionData
					: this.redMotionData;
		} else {
			return this.isCounterClockwiseAhead(blueStart, redStart)
				? trailing
					? this.redMotionData
					: this.blueMotionData
				: trailing
					? this.blueMotionData
					: this.redMotionData;
		}
	}

	getTrailingMotion(): MotionData {
		return this.determineMotionOrder(true);
	}

	getLeadingMotion(): MotionData {
		return this.determineMotionOrder(false);
	}
}
