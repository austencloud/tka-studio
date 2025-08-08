import type {
	SupervisionStrategyPlugin,
	RestartStrategyOptions,
	SupervisionStrategy
} from '../types.js';
import { SupervisionStrategyType, BackoffType } from '../types.js';
import { RestartStrategy } from './RestartStrategy.js';

export const RestartPlugin: SupervisionStrategyPlugin<RestartStrategyOptions> = {
	type: SupervisionStrategyType.RESTART,

	defaultConfig: {
		maxRestarts: 5,
		withinTimeWindow: 60_000,
		backoffType: BackoffType.EXPONENTIAL,
		initialDelay: 100,
		maxDelay: 30_000,
		factor: 2,
		resetTimeout: 300_000,
		preserveState: true
	},

	createStrategy(config?: Partial<RestartStrategyOptions>): SupervisionStrategy {
		return new RestartStrategy({
			...this.defaultConfig,
			...config
		});
	}
};
