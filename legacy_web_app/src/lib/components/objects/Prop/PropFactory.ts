import type { Motion } from '../Motion/Motion';
import type { PropData } from './PropData';
import { PropType } from '../../../types/Types';

export function createPropData(motion: Motion): PropData {
	// Generate a unique ID
	const propId = generateUniqueId();


	// Create the prop with proper defaults
	const propData: PropData = {
		id: propId,
		propType: PropType.STAFF,
		color: motion.color,
		motionId: motion.id,
		coords: { x: 0, y: 0 }, // Will be positioned by the placement manager
		loc: motion.endLoc,
		ori: motion.endOri,
		radialMode: ['in', 'out'].includes(motion.endOri) ? 'radial' : 'nonradial',
		svgCenter: { x: 0, y: 0 },
		rotAngle: 0
	};

	return propData;
}

/**
 * Generate a unique ID for the prop
 */
export function generateUniqueId(): string {
    return crypto.randomUUID ? crypto.randomUUID() : `id-${Math.random().toString(36).substr(2, 9)}`;
}
