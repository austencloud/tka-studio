import type { Motion } from '../../objects/Motion/Motion';
import type { ArrowData } from './ArrowData';
import ArrowSvgMirrorManager from './ArrowSvgMirrorManager';

export function createArrowData(motion: Motion): ArrowData {
	const arrowData: ArrowData = {
		id: generateUniqueId(), // ✅ Generate unique ID
		motionId: motion.id, // ✅ Store motion ID, not full motion object
		color: motion.color,
		coords: { x: 0, y: 0 },
		loc: motion.startLoc, // ✅ Use motion start location
		rotAngle: 0,
		svgMirrored: false,
		svgCenter: { x: 0, y: 0 },
		svgLoaded: false,
		svgData: null,
		motionType: motion.motionType, // ✅ Store motion properties separately
		startOri: motion.startOri,
		turns: motion.turns,
		propRotDir: motion.propRotDir,
		endOri: motion.endOri
	};

	const mirrorManager = new ArrowSvgMirrorManager(arrowData);
	mirrorManager.updateMirror();

	return arrowData;
}
export function generateUniqueId(): string {
    return crypto.randomUUID ? crypto.randomUUID() : `id-${Math.random().toString(36).substr(2, 9)}`;
}
