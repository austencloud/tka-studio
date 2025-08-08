import type { SupervisionStrategy, SupervisedActor, EscalateStrategyOptions } from '../types.js';
import { SupervisionStrategyType } from '../types.js';
import type { Supervisor } from '../Supervisor.js';

export class EscalateStrategy implements SupervisionStrategy {
	readonly type = SupervisionStrategyType.ESCALATE;

	constructor(private readonly config: EscalateStrategyOptions) {}

	async handleError(
		supervisor: Supervisor,
		actor: SupervisedActor<any>,
		error: Error
	): Promise<void> {
		const transformedError = this.config.transformError?.(error, actor) ?? error;

		if (this.config.stopActor) {
			await actor.stop();
		}

		throw transformedError;
	}
}
