import type {
	SupervisionStrategyPlugin,
	EscalateStrategyOptions,
	SupervisionStrategy
} from '../types.js';
import { SupervisionStrategyType } from '../types.js';
import { EscalateStrategy } from './EscalateStrategy.js';

export const EscalatePlugin: SupervisionStrategyPlugin<EscalateStrategyOptions> = {
	type: SupervisionStrategyType.ESCALATE,

	defaultConfig: {
		stopActor: false,
		transformError: undefined
	},

	createStrategy(config?: Partial<EscalateStrategyOptions>): SupervisionStrategy {
		return new EscalateStrategy({
			...this.defaultConfig,
			...config
		});
	}
};
