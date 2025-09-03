import type { ArrowData } from './ArrowData';

export default class ArrowSvgManager {
	constructor(private arrowData: ArrowData) {}

	getSvgPath(): string {
		const basePath = '/images/arrows';
		const motionType = this.arrowData.motionType.toLowerCase();
		const turns = this.arrowData.turns;
		const radialPath =
			this.arrowData.startOri === 'out' || this.arrowData.startOri === 'in'
				? 'from_radial'
				: 'from_nonradial';
		if (turns === 'fl' && motionType === 'float') {
			return `${basePath}/float.svg`;
		} else {
			return `${basePath}/${motionType}/${radialPath}/${motionType}_${Number(turns).toFixed(1)}.svg`;
		}
	}
}
