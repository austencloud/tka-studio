/**
 * Actor Supervision System - Supervisor
 *
 * This file contains the implementation of the supervisor that manages supervised actors.
 */

import { debug, warn, error } from '../logger/logging';
import type {
	Supervisor as ISupervisor,
	SupervisedActor,
	SupervisionStrategy,
	SupervisionError
} from './types';
import { RestartStrategy } from './strategies';

/**
 * Implementation of a supervisor
 */
export class Supervisor implements ISupervisor {
	/**
	 * The unique ID of the supervisor
	 */
	public readonly id: string;

	/**
	 * The parent supervisor, if any
	 */
	public parent?: ISupervisor;

	/**
	 * The supervised actors managed by this supervisor
	 */
	public actors = new Map<string, SupervisedActor<any>>();

	/**
	 * The default strategy to use for actors that don't specify one
	 */
	public defaultStrategy: SupervisionStrategy;

	/**
	 * Error handler for supervision errors
	 */
	private onError?: (error: SupervisionError) => void;

	/**
	 * Whether to enable debug logging
	 */
	private debug: boolean;

	constructor(
		id: string,
		options: {
			parent?: ISupervisor;
			defaultStrategy?: SupervisionStrategy;
			onError?: (error: SupervisionError) => void;
			debug?: boolean;
		} = {}
	) {
		this.id = id;
		this.parent = options.parent;
		this.defaultStrategy = options.defaultStrategy || new RestartStrategy();
		this.onError = options.onError;
		this.debug = options.debug || false;

		if (this.debug) {
			debug('supervisor', `Created supervisor ${id}`, {
				parent: this.parent?.id || 'none',
				strategy: this.defaultStrategy.type
			});
		}
	}

	/**
	 * Register an actor with this supervisor
	 */
	registerActor(actor: SupervisedActor<any>): void {
		if (this.actors.has(actor.id)) {
			warn(
				'supervisor',
				`Actor ${actor.id} is already registered with supervisor ${this.id}. Overwriting.`
			);
		}

		this.actors.set(actor.id, actor);

		if (this.debug) {
			debug('supervisor', `Registered actor ${actor.id} with supervisor ${this.id}`);
		}
	}

	/**
	 * Unregister an actor from this supervisor
	 */
	unregisterActor(actorId: string): void {
		if (this.actors.has(actorId)) {
			this.actors.delete(actorId);

			if (this.debug) {
				debug('supervisor', `Unregistered actor ${actorId} from supervisor ${this.id}`);
			}
		} else {
			warn(
				'supervisor',
				`Attempted to unregister unknown actor ${actorId} from supervisor ${this.id}`
			);
		}
	}

	/**
	 * Handle an error from a supervised actor
	 */
	async handleActorError(
		actor: SupervisedActor<any>,
		err: Error,
		context?: Record<string, any>
	): Promise<void> {
		if (this.debug) {
			debug('supervisor', `Handling error for actor ${actor.id}`, {
				error: err.message,
				supervisor: this.id,
				context
			});
		}

		// Call error handler if provided
		if (this.onError) {
			try {
				this.onError({
					error: err,
					actorId: actor.id,
					timestamp: Date.now(),
					actorState: actor.getSnapshot(),
					context
				});
			} catch (handlerError) {
				error('supervisor', `Error in supervisor ${this.id} error handler`, handlerError);
			}
		}

		// Apply the actor's strategy
		try {
			await actor.strategy.handleError(this, actor, err);
		} catch (strategyError) {
			error('supervisor', `Error applying strategy for actor ${actor.id}`, strategyError);

			// If the strategy fails, escalate to parent if available
			if (this.parent) {
				await this.escalateError(actor, strategyError as Error, {
					originalError: err,
					...context
				});
			} else {
				// No parent to escalate to, log the error
				error(
					'supervisor',
					`No parent supervisor to escalate error to for actor ${actor.id}. Error will be unhandled.`
				);
				// Re-throw the error
				throw strategyError;
			}
		}
	}

	/**
	 * Escalate an error to the parent supervisor
	 */
	async escalateError(
		actor: SupervisedActor<any>,
		err: Error,
		context?: Record<string, any>
	): Promise<void> {
		if (this.parent) {
			if (this.debug) {
				debug(
					'supervisor',
					`Escalating error for actor ${actor.id} to parent supervisor ${this.parent.id}`,
					{
						error: err.message,
						context
					}
				);
			}

			await this.parent.handleActorError(actor, err, {
				escalatedFrom: this.id,
				...context
			});
		} else {
			error('supervisor', `Cannot escalate error: no parent supervisor for ${this.id}`);

			// Re-throw the error
			throw err;
		}
	}

	/**
	 * Stop all supervised actors
	 */
	async stopAllActors(): Promise<void> {
		const stopPromises: Promise<void>[] = [];

		for (const actor of this.actors.values()) {
			stopPromises.push(
				(async () => {
					try {
						await actor.stop();
					} catch (err) {
						error('supervisor', `Error stopping actor ${actor.id}`, err);
					}
				})()
			);
		}

		await Promise.all(stopPromises);
		this.actors.clear();

		if (this.debug) {
			debug('supervisor', `Stopped all actors in supervisor ${this.id}`);
		}
	}

	/**
	 * Get all supervised actors
	 */
	getAllActors(): SupervisedActor<any>[] {
		return Array.from(this.actors.values());
	}

	/**
	 * Get a supervised actor by ID
	 */
	getActor(actorId: string): SupervisedActor<any> | undefined {
		return this.actors.get(actorId);
	}
}
