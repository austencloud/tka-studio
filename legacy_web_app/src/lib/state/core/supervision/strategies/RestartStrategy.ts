import type { SupervisionStrategy, SupervisedActor, RestartStrategyOptions } from '../types';
import { SupervisionStrategyType, BackoffType } from '../types';
import type { Supervisor } from '../Supervisor';

export class RestartStrategy implements SupervisionStrategy {
	readonly type = SupervisionStrategyType.RESTART;
	private lastRestartTime?: number;
	private restartCount = 0;

	constructor(private readonly config: RestartStrategyOptions) {}

	async handleError(
		supervisor: Supervisor,
		actor: SupervisedActor<any>,
		error: Error
	): Promise<void> {
		const now = Date.now();
		this.restartCount++;

		if (this.config.maxRestarts !== undefined && this.config.withinTimeWindow !== undefined) {
			if (this.lastRestartTime && now - this.lastRestartTime > this.config.withinTimeWindow) {
				this.restartCount = 1;
			}

			if (this.restartCount > this.config.maxRestarts) {
				throw error;
			}
		}

		const delay = this.calculateBackoffDelay();
		if (delay > 0) {
			await new Promise((resolve) => setTimeout(resolve, delay));
		}

		await actor.restart(this.config.preserveState);
		this.lastRestartTime = now;
	}

	private calculateBackoffDelay(): number {
		if (!this.config.backoffType || this.config.backoffType === BackoffType.NONE) {
			return 0;
		}

		const baseDelay = this.config.initialDelay ?? 1000;
		const maxDelay = this.config.maxDelay ?? 30000;
		const factor = this.config.factor ?? 2;

		switch (this.config.backoffType) {
			case BackoffType.LINEAR:
				return Math.min(baseDelay * this.restartCount, maxDelay);

			case BackoffType.EXPONENTIAL:
				return Math.min(baseDelay * Math.pow(factor, this.restartCount - 1), maxDelay);

			case BackoffType.RANDOM:
				const max = Math.min(baseDelay * this.restartCount, maxDelay);
				return Math.random() * max;

			default:
				return 0;
		}
	}
}
