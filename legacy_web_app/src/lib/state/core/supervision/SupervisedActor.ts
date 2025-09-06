/**
 * Actor Supervision System – Supervised Actor (v3)
 *
 * – removes `implements Actor<TMachine>` to avoid TS 2720 (cannot implement a *class*)
 * – `getPersistedSnapshot` now matches interface signature (returns `SnapshotFrom<TMachine> | undefined`)
 * – keeps `options` public to satisfy structural typing in tests
 */

import {
	createActor,
	type AnyStateMachine,
	type EventFromLogic,
	type Observer,
	type Subscription,
	type SnapshotFrom,
	type ActorRefFrom,
	type ActorOptions,
	type InspectionEvent,
	type InputFrom,
	type EmittedFrom
} from 'xstate';
import { debug } from '../logger/logging';
import type {
	SupervisedActor as ISupervisedActor,
	SupervisedActorOptions,
	ActorHealthMetrics,
	Supervisor,
	SupervisionStrategy
} from './types';
import { ActorHealthStatus } from './types';
import { RestartStrategy } from './strategies';

// Private storage using WeakMap
const actorStorage = new WeakMap<SupervisedActor<any>, ReturnType<typeof createActor>>();
const healthStorage = new WeakMap<SupervisedActor<any>, ActorHealthMetrics>();
const optionsStorage = new WeakMap<SupervisedActor<any>, SupervisedActorOptions<any>>();

export class SupervisedActor<TMachine extends AnyStateMachine>
	implements ISupervisedActor<TMachine>
{
	public readonly id: string;
	private machine: TMachine;
	private isRestarting = false;

	// Required methods from ISupervisedActor interface with correct typing
	public send = (event: EventFromLogic<TMachine>): void => this.actor.send(event);

	public subscribe: {
		(observer: Observer<SnapshotFrom<TMachine>>): Subscription;
		(
			nextListener?: ((snapshot: SnapshotFrom<TMachine>) => void) | undefined,
			errorListener?: ((error: unknown) => void) | undefined,
			completeListener?: (() => void) | undefined
		): Subscription;
	} = (
		observerOrNext?:
			| Observer<SnapshotFrom<TMachine>>
			| ((snapshot: SnapshotFrom<TMachine>) => void),
		errorListener?: (error: unknown) => void,
		completeListener?: () => void
	): Subscription => {
		if (typeof observerOrNext === 'function' || observerOrNext === undefined) {
			return this.actor.subscribe(observerOrNext, errorListener, completeListener);
		} else {
			return this.actor.subscribe(observerOrNext);
		}
	};

	public on = <TType extends '*' | EmittedFrom<TMachine>['type']>(
		type: TType,
		handler: (
			emitted: EmittedFrom<TMachine> & (TType extends '*' ? unknown : { type: TType })
		) => void
	): Subscription => {
		return this.actor.on(type, handler as any);
	};

	public getSnapshot = (): SnapshotFrom<TMachine> => this.actor.getSnapshot();

	constructor(
		id: string,
		machine: TMachine,
		options: SupervisedActorOptions<TMachine> = {},
		supervisor?: Supervisor
	) {
		this.id = id;
		this.machine = machine;

		const actorOptions: ActorOptions<TMachine> = {
			...options,
			input: (options as any).input as InputFrom<TMachine>
		};

		const actor = createActor(machine, actorOptions) as ReturnType<typeof createActor<TMachine>>;
		actor.start();

		actorStorage.set(this, actor);
		optionsStorage.set(this, { ...options, supervisor });
		healthStorage.set(this, {
			status: options.initialHealth ?? ActorHealthStatus.HEALTHY,
			errorCount: 0,
			restartCount: 0,
			uptime: 0,
			createdAt: Date.now()
		});

		debug('actor', `Created actor ${id}`, { strategy: this.strategy.type });
	}

	async restart(preserveState = true): Promise<void> {
		if (this.isRestarting) return;
		this.isRestarting = true;

		try {
			debug('actor', `Restarting actor ${this.id}`, { preserveState });

			const snapshot = preserveState ? this.getSnapshot() : undefined;
			this.actor.stop();

			const opts = optionsStorage.get(this);
			if (!opts) throw new Error('Actor options not initialized');

			const actorOptions: ActorOptions<TMachine> = {
				...opts,
				snapshot,
				input: (opts as any).input as InputFrom<TMachine>
			};

			const actor = createActor(this.machine, actorOptions);
			actor.start();
			actorStorage.set(this, actor);

			const metrics = healthStorage.get(this);
			if (metrics) {
				metrics.restartCount++;
				metrics.lastRestartTime = Date.now();
			}

			(opts as any).onRestart?.(this as any);

			debug('actor', `Actor ${this.id} restarted successfully`);
		} finally {
			this.isRestarting = false;
		}
	}

	// Properties and methods with proper typing
	get strategy(): SupervisionStrategy {
		const opts = optionsStorage.get(this);
		return opts?.strategy ?? opts?.supervisor?.defaultStrategy ?? new RestartStrategy();
	}

	get supervisor(): Supervisor | undefined {
		return optionsStorage.get(this)?.supervisor;
	}

	get ref(): ActorRefFrom<TMachine> {
		return actorStorage.get(this) as unknown as ActorRefFrom<TMachine>;
	}

	private get actor(): ReturnType<typeof createActor<TMachine>> {
		const actor = actorStorage.get(this);
		if (!actor) throw new Error('Actor not initialized');
		return actor as ReturnType<typeof createActor<TMachine>>;
	}

	// Health metrics
	getHealthMetrics(): ActorHealthMetrics {
		const metrics = healthStorage.get(this);
		if (!metrics) throw new Error('Health metrics not initialized');
		metrics.uptime = Date.now() - metrics.createdAt;
		return { ...metrics };
	}

	// Lifecycle methods
	start(): this {
		this.actor.start();
		return this;
	}

	stop(): this {
		const metrics = healthStorage.get(this);
		if (metrics) {
			metrics.status = ActorHealthStatus.STOPPED;
		}

		const opts = optionsStorage.get(this);
		(opts as any).onStop?.(this as any);

		this.actor.stop();
		return this;
	}

	// Error handling with proper typing
	reportError(error: Error, context?: Record<string, any>): void {
		const metrics = healthStorage.get(this);
		if (metrics) {
			metrics.errorCount++;
			metrics.lastErrorTime = Date.now();
			metrics.lastError = error;
			metrics.status = ActorHealthStatus.DEGRADED;
		}

		const opts = optionsStorage.get(this);
		opts?.onError?.({
			error,
			actorId: this.id,
			timestamp: Date.now(),
			actorState: this.getSnapshot(),
			context
		});

		if (this.supervisor) {
			void this.supervisor.handleActorError(this as any, error, context);
		} else {
			void this.strategy.handleError(
				{
					id: 'anonymous',
					actors: new Map(),
					defaultStrategy: this.strategy,
					registerActor() {},
					unregisterActor() {},
					handleActorError: async () => {},
					escalateError: async () => {},
					stopAllActors: async () => {},
					getAllActors: () => [],
					getActor: () => undefined
				},
				this as any,
				error
			);
		}
	}

	// Getters with proper types
	getMachine(): TMachine {
		return this.machine;
	}

	getOptions(): SupervisedActorOptions<TMachine> {
		const opts = optionsStorage.get(this);
		return opts ? ({ ...opts } as SupervisedActorOptions<TMachine>) : {};
	}

	getPersistedSnapshot(): SnapshotFrom<TMachine> | undefined {
		return this.actor.getPersistedSnapshot?.() as SnapshotFrom<TMachine> | undefined;
	}

	// Observable interface
	get [Symbol.observable]() {
		return this.actor[Symbol.observable];
	}

	// System internals
	get sessionId() {
		return this.actor.sessionId;
	}

	get src() {
		return this.actor.src;
	}

	get system() {
		return this.actor.system;
	}

	toJSON() {
		return this.actor.toJSON();
	}
}
