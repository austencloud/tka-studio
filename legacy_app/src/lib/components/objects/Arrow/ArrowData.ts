import type { Motion } from '../../objects/Motion/Motion';
import type {
	Color,
	Loc,
	MotionType,
	Orientation,
	PropRotDir,
	TKATurns
} from '../../../types/Types';
import type { ArrowSvgData } from '$lib/components/SvgManager/ArrowSvgData';

export interface ArrowData {
	id: string;
	motionId: string; // ✅ Parent reference
	color: Color;
	coords: { x: number; y: number };
	loc: Loc;
	rotAngle: number;
	svgMirrored: boolean;
	svgCenter: { x: number; y: number };
	svgLoaded: boolean;
	svgData: ArrowSvgData | null;
	motionType: MotionType;
	startOri: Orientation;
	endOri: Orientation;
	turns: TKATurns;
	propRotDir: PropRotDir;
}
