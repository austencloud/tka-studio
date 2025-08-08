import type { PictographData } from './PictographData.js';

export interface Beat {
	id: string;
	beatNumber: number;
	pictographData: PictographData;
	filled: boolean;
	metadata?: {
		blueReversal?: boolean;
		redReversal?: boolean;
		letter?: string;
		startPos?: string;
		endPos?: string;
		tags?: string[];
	};
}
