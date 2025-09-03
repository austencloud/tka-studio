// src/lib/components/Pictograph/defaultPictographData.ts
import { DIAMOND } from '$lib/types/Constants';
import type { PictographData } from '$lib/types/PictographData';

export const defaultPictographData: PictographData = {
	letter: null,
	startPos: null,
	endPos: null,
	timing: null,
	direction: null,
	gridMode: DIAMOND,
	blueMotionData: null,
	redMotionData: null,
	motions: [],
	redMotion: null,
	blueMotion: null,
	props: [],
	redPropData: null,
	bluePropData: null,
	gridData: null,
	redArrowData: null,
	blueArrowData: null,
	grid: '',
	isStartPosition: false
};
