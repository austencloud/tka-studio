import { MotionChecker } from './MotionChecker';
import { MotionOriCalculator } from './MotionOriCalculator';
import { HandpathCalculator as HandRotDirCalculator } from './HandpathCalculator';
import type { PictographData } from '../../../types/PictographData';
import { LeadStateDeterminer } from './LeadStateDeterminer';
import type {
	Color,
	GridMode,
	HandRotDir,
	LeadState,
	Loc,
	MotionType,
	Orientation,
	PropRotDir,
	TKATurns
} from '../../../types/Types';
import type { PropData } from '../Prop/PropData';
import type { Letter } from '$lib/types/Letter';
import type { ArrowData } from '../Arrow/ArrowData';
import type { MotionData } from './MotionData';

export class Motion implements MotionData {
	id: string;
	arrowId: string | null = null;
	propId: string | null = null;
	handRotDir: HandRotDir | null = null;
	motionType: MotionType;
	startLoc: Loc;
	endLoc: Loc;
	startOri: Orientation;
	endOri: Orientation;
	propRotDir: PropRotDir;
	color: Color;
	turns: TKATurns;
	leadState: LeadState;
	gridMode: GridMode;
	checker: MotionChecker;
	oriCalculator: MotionOriCalculator;
	handRotDirCalculator: HandRotDirCalculator;
	redMotionData: MotionData | null = null;
	blueMotionData: MotionData | null = null;
	letter: Letter | null = null;
	prefloatMotionType!: MotionType | null;
	prefloatPropRotDir!: PropRotDir | null;
	public readonly ready: Promise<void>;

	constructor(pictographData: PictographData, motionData: MotionData) {
		this.id = motionData.id;
		this.arrowId = motionData.arrowId ?? null;
		this.propId = motionData.propId ?? null;
		this.handRotDir = motionData.handRotDir ?? null;
		this.motionType = motionData.motionType;
		this.startLoc = motionData.startLoc;
		this.endLoc = motionData.endLoc;
		this.startOri = motionData.startOri;
		this.oriCalculator = new MotionOriCalculator(this);
		this.endOri = this.oriCalculator.calculateEndOri();
		this.propRotDir = motionData.propRotDir;
		this.color = motionData.color;
		this.turns = motionData.turns;
		this.leadState = motionData.leadState;
		this.gridMode = pictographData.gridMode;

		this.checker = new MotionChecker(this);
		this.oriCalculator = new MotionOriCalculator(this);
		this.handRotDirCalculator = new HandRotDirCalculator();

		this.ready = new Promise((resolve) => resolve());

		// Validate properties
		this.validatePrefloatProperties();
	}
	calculateFinalEndOrientation(): Orientation {
		return this.oriCalculator.calculateEndOri();
	}
	assignLeadStates(): void {
		const { redMotionData, blueMotionData } = this;

		if (redMotionData && blueMotionData) {
			const leadStateDeterminer = new LeadStateDeterminer(redMotionData, blueMotionData);
			const leadingMotion = leadStateDeterminer.getLeadingMotion();
			const trailingMotion = leadStateDeterminer.getTrailingMotion();

			leadingMotion.leadState = 'leading';
			trailingMotion.leadState = 'trailing';
		} else {
			throw new Error('Red or Blue motion data is null');
		}
	}

	attachComponents(prop: PropData, arrow: ArrowData): void {
		this.propId = prop.id;
		this.arrowId = arrow.id;
	}

	private validatePrefloatProperties(): void {
		if (this.motionType === 'float') {
			throw new Error("`motionType` cannot be 'float' unexpectedly");
		}
	}
}
