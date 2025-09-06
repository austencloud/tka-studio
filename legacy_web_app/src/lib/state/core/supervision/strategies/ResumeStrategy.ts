import type { SupervisionStrategy, SupervisedActor, ResumeStrategyOptions } from '../types';
import { SupervisionStrategyType } from '../types';
import type { Supervisor } from '../Supervisor';

export class ResumeStrategy implements SupervisionStrategy {
	readonly type = SupervisionStrategyType.RESUME;
	private errorCount = 0;
	private lastErrorTime?: number;

	constructor(private readonly config: ResumeStrategyOptions) {}

	async handleError(
		supervisor: Supervisor,
		actor: SupervisedActor<any>,
		error: Error
	): Promise<void> {
		const now = Date.now();
		this.errorCount++;

		if (this.config.maxErrors !== undefined && this.config.withinTimeWindow !== undefined) {
			if (this.lastErrorTime && now - this.lastErrorTime > this.config.withinTimeWindow) {
				this.errorCount = 1;
			}

			if (this.errorCount > this.config.maxErrors && this.config.fallbackStrategy) {
				return this.config.fallbackStrategy.handleError(supervisor, actor, error);
			}
		}

		if (this.config.logError) {
			console.error(`[${actor.id}] Error handled by resume strategy:`, error);
		}

		this.lastErrorTime = now;
	}
}
