import { CLOCK, COUNTER, IN, OUT } from '$lib/types/Constants';
import type { PropData } from './PropData';

class PropChecker {
	prop: PropData;

	constructor(propData: PropData) {
		this.prop = propData;
	}

	isRadial(): boolean {
		return this.prop != null && [IN, OUT].includes(this.prop.ori);
	}

	isNonRadial(): boolean {
		return this.prop != null && [CLOCK, COUNTER].includes(this.prop.ori);
	}

	hasOutOri(): boolean {
		return this.prop != null && this.prop.ori === OUT;
	}

	hasInOri(): boolean {
		return this.prop != null && this.prop.ori === IN;
	}

	hasClockOri(): boolean {
		return this.prop != null && this.prop.ori === CLOCK;
	}

	hasCounterOri(): boolean {
		return this.prop != null && this.prop.ori === COUNTER;
	}
}

export { PropChecker };
