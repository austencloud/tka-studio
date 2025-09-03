import type {
	Color,
	HandRotDir,
	LeadState,
	Loc,
	MotionType,
	Orientation,
	PropRotDir,
	TKATurns
} from '../../../types/Types';

export interface MotionData {
	id: string;
	arrowId?: string | null;
	propId?: string | null;
	handRotDir?: HandRotDir | null;
	motionType: MotionType;
	startLoc: Loc;
	endLoc: Loc;
	startOri: Orientation;
	endOri: Orientation;
	propRotDir: PropRotDir;
	color: Color;
	turns: TKATurns;
	leadState: LeadState;
	prefloatMotionType: MotionType | null;
	prefloatPropRotDir: PropRotDir | null;
}

export const BlankMotionData: Partial<MotionData> = {
	id: '',
	arrowId: null,
	propId: null,
	handRotDir: null!,
	motionType: null!,
	startLoc: null!,
	endLoc: null!,
	startOri: null!,
	endOri: null!,
	propRotDir: null!,
	color: null!,
	turns: null!,
	leadState: null!
};

export interface ShiftMotionInterface extends MotionData {
	motionType: 'float';
	handRotDir: 'cw_shift' | 'ccw_shift';
}
