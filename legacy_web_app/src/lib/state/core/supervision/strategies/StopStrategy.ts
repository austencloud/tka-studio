import type { SupervisionStrategy, SupervisedActor, StopStrategyOptions } from '../types';
import { SupervisionStrategyType } from '../types';
import type { Supervisor } from '../Supervisor';

export class StopStrategy implements SupervisionStrategy {
	readonly type = SupervisionStrategyType.STOP;

	constructor(private readonly config: StopStrategyOptions) {}

	async handleError(
		supervisor: Supervisor,
		actor: SupervisedActor<any>,
		error: Error
	): Promise<void> {
		if (this.config.cleanup) {
			await this.config.cleanup(actor);
		}

		await actor.stop();

		if (this.config.notifySupervisor) {
			supervisor.unregisterActor(actor.id);
		}
	}
}
