/**
 * Actor Supervision System - Root Supervisor
 *
 * This file contains the implementation of the root supervisor that acts as the
 * top-level supervisor for the entire application.
 */

import { debug, warn, error } from '../logger/logging';
import { Supervisor } from './Supervisor';
import { DefaultCircuitBreaker } from './CircuitBreaker';
import type {
	SupervisedActor,
	RootSupervisorOptions,
	CircuitBreaker,
	SupervisionError
} from './types';

let rootSupervisorInstance: RootSupervisor | null = null;

export class RootSupervisor extends Supervisor {
	private circuitBreaker?: CircuitBreaker;
	private errorHistory: SupervisionError[] = [];
	private readonly maxErrorHistory = 100;

	private constructor(options: RootSupervisorOptions = {}) {
		super('root', {
			defaultStrategy: options.defaultStrategy,
			onError: options.onError,
			debug: options.debug
		});

		if (options.circuitBreaker) {
			this.circuitBreaker = new DefaultCircuitBreaker('root', options.circuitBreaker);
			debug('root-supervisor', 'Initialized with circuit breaker', options.circuitBreaker);
		}

		debug('root-supervisor', 'Initialized as the top-level supervisor');
	}

	static getInstance(options?: RootSupervisorOptions): RootSupervisor {
		if (!rootSupervisorInstance) {
			rootSupervisorInstance = new RootSupervisor(options);
		}
		return rootSupervisorInstance;
	}

	static resetInstance(): void {
		if (rootSupervisorInstance) {
			rootSupervisorInstance.stopAllActors().catch((err) => {
				error('root-supervisor', 'Error stopping actors during reset:', err);
			});

			if (rootSupervisorInstance.circuitBreaker) {
				rootSupervisorInstance.circuitBreaker.reset();
			}

			rootSupervisorInstance = null;
			debug('root-supervisor', 'Root supervisor instance reset');
		}
	}

	async handleActorError(
		actor: SupervisedActor<any>,
		err: Error,
		context?: Record<string, any>
	): Promise<void> {
		const supervisionError: SupervisionError = {
			error: err,
			actorId: actor.id,
			timestamp: Date.now(),
			actorState: actor.getSnapshot(),
			context
		};

		this.errorHistory.unshift(supervisionError);

		if (this.errorHistory.length > this.maxErrorHistory) {
			this.errorHistory = this.errorHistory.slice(0, this.maxErrorHistory);
		}

		if (this.circuitBreaker) {
			if (!this.circuitBreaker.isAllowed()) {
				warn('root-supervisor', 'Circuit breaker is open, fast-failing actor', {
					actorId: actor.id,
					error: err.message
				});

				await actor.stop();
				return;
			}

			this.circuitBreaker.recordFailure(err);
		}

		try {
			await super.handleActorError(actor, err, context);
			this.circuitBreaker?.recordSuccess();
		} catch (handlingError) {
			error('root-supervisor', 'Error handling actor failure', {
				actorId: actor.id,
				originalError: err.message,
				handlingError
			});
			throw handlingError;
		}
	}

	getErrorHistory(): SupervisionError[] {
		return [...this.errorHistory];
	}

	clearErrorHistory(): void {
		this.errorHistory = [];
		debug('root-supervisor', 'Error history cleared');
	}

	getCircuitBreakerState(): string | undefined {
		return this.circuitBreaker?.state;
	}

	resetCircuitBreaker(): void {
		if (this.circuitBreaker) {
			this.circuitBreaker.reset();
			debug('root-supervisor', 'Circuit breaker reset');
		}
	}
}
