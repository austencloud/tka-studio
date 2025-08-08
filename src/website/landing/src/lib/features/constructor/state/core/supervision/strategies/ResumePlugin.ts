import type {
	SupervisionStrategyPlugin,
	ResumeStrategyOptions,
	SupervisionStrategy
} from '../types.js';
import { SupervisionStrategyType } from '../types.js';
import { ResumeStrategy } from './ResumeStrategy.js';
import { StopStrategy } from './StopStrategy.js';

export const ResumePlugin: SupervisionStrategyPlugin<ResumeStrategyOptions> = {
	type: SupervisionStrategyType.RESUME,

	defaultConfig: {
		maxErrors: Number.MAX_SAFE_INTEGER,
		withinTimeWindow: 60_000,
		fallbackStrategy: new StopStrategy({
			notifySupervisor: true,
			cleanup: undefined
		}),
		logError: true
	},

	createStrategy(config?: Partial<ResumeStrategyOptions>): SupervisionStrategy {
		return new ResumeStrategy({
			...this.defaultConfig,
			...config
		});
	}
};
