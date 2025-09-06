import type { SupervisionStrategyPlugin, StopStrategyOptions, SupervisionStrategy } from '../types';
import { SupervisionStrategyType } from '../types';
import { StopStrategy } from './StopStrategy';

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
