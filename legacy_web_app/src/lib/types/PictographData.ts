import type { ArrowData } from '$lib/components/objects/Arrow/ArrowData.js';
import type { GridData } from '$lib/components/objects/Grid/GridData.js';
import type { Motion } from '$lib/components/objects/Motion/Motion.js';
import type { MotionData } from '$lib/components/objects/Motion/MotionData.js';
import type { PropData } from '$lib/components/objects/Prop/PropData.js';
import type { Letter } from './Letter.js';
import type { TKAPosition } from './TKAPosition.js';
import type { GridMode, VTGDir, VTGTiming } from './Types.js';

export interface PictographData {
	// TKA
	letter: Letter | null;
	startPos: TKAPosition | null;
	endPos: TKAPosition | null;

	// VTG
	timing: VTGTiming | null;
	direction: VTGDir | null;

	// Grid
	gridMode: GridMode;
	gridData: GridData | null;

	// Motion
	blueMotionData: MotionData | null;
	redMotionData: MotionData | null;

	motions?: Motion[] | undefined;
	redMotion?: Motion | null;
	blueMotion?: Motion | null;

	// Props
	redPropData: PropData | null;
	bluePropData: PropData | null;
	props?: PropData[];

	// Arrows
	redArrowData: ArrowData | null;
	blueArrowData: ArrowData | null;

	grid: string;

	// Special flag to mark this as a start position
	isStartPosition?: boolean;
}
