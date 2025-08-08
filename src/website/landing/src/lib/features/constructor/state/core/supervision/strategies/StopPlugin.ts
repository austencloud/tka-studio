import type { SupervisionStrategyPlugin, StopStrategyOptions, SupervisionStrategy } from '../types.js';
import { SupervisionStrategyType } from '../types.js';
import { StopStrategy } from './StopStrategy.js';

export const StopPlugin: SupervisionStrategyPlugin<StopStrategyOptions> = {
	type: SupervisionStrategyType.STOP,

	defaultConfig: {
		notifySupervisor: true,
		cleanup: undefined
	},

	createStrategy(config?: Partial<StopStrategyOptions>): SupervisionStrategy {
		return new StopStrategy({
			...this.defaultConfig,
			...config
		});
	}
};
