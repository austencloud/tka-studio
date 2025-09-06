import type {
	SupervisionStrategyPlugin,
	EscalateStrategyOptions,
	SupervisionStrategy
} from '../types';
import { SupervisionStrategyType } from '../types';
import { EscalateStrategy } from './EscalateStrategy';

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
