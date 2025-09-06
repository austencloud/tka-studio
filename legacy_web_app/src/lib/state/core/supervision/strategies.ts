// src/lib/state/core/supervision/strategies.ts
/**
 * Actor Supervision System – Strategies (clean single‑definition, v6)
 *
 * Contains the four built‑in supervision strategies:
 *  • RestartStrategy
 *  • EscalateStrategy
 *  • StopStrategy
 *  • ResumeStrategy
 *
 * No duplicate declarations; strict‑mode friendly.
 */

import { LogLevel, log } from '../logger';
import type {
	SupervisedActor,
	Supervisor,
	RestartStrategyOptions,
	EscalateStrategyOptions,
	StopStrategyOptions,
	ResumeStrategyOptions,
	SupervisionStrategy
} from './types';
import { SupervisionStrategyType, BackoffType } from './types';

/* -------------------------------------------------------------------------- */
/*  Base                                                                      */
/* -------------------------------------------------------------------------- */
abstract class BaseStrategy implements SupervisionStrategy {
	abstract readonly type: SupervisionStrategyType;
	abstract handleError(
		supervisor: Supervisor,
		actor: SupervisedActor<any>,
		error: Error
	): Promise<void>;

	protected logError(type: SupervisionStrategyType, actorId: string, error: Error): void {
		log(actorId, LogLevel.ERROR, `[${type}] error:`, error.message);
	}
}

/* -------------------------------------------------------------------------- */
/*  Restart                                                                   */
/* -------------------------------------------------------------------------- */
export class RestartStrategy extends BaseStrategy {
	readonly type = SupervisionStrategyType.RESTART;

	private readonly opts: Required<RestartStrategyOptions>;
	private readonly failures = new Map<string, number[]>();
	private readonly resetTimers = new Map<string, NodeJS.Timeout>();

	constructor(options: RestartStrategyOptions = {}) {
		super();
		this.opts = {
			maxRestarts: options.maxRestarts ?? 10,
			withinTimeWindow: options.withinTimeWindow ?? 60_000,
			backoffType: options.backoffType ?? BackoffType.EXPONENTIAL,
			initialDelay: options.initialDelay ?? 0,
			maxDelay: options.maxDelay ?? 30_000,
			factor: options.factor ?? 2,
			resetTimeout: options.resetTimeout ?? 300_000,
			preserveState: options.preserveState ?? true
		} as const;
	}

	async handleError(
		supervisor: Supervisor,
		actor: SupervisedActor<any>,
		error: Error
	): Promise<void> {
		this.logError(this.type, actor.id, error);

		/* track failures inside window */
		const now = Date.now();
		const list = this.failures.get(actor.id) ?? [];
		list.push(now);
		const start = now - this.opts.withinTimeWindow;
		this.failures.set(
			actor.id,
			list.filter((t) => t >= start)
		);

		if (list.length > this.opts.maxRestarts) {
			log(actor.id, LogLevel.WARN, `[${this.type}] restart limit exceeded – stopping actor`);
			await actor.stop();
			return;
		}

		const delay = this.calcBackoff(list.length);
		if (delay) await new Promise((r) => setTimeout(r, delay));
		await actor.restart(this.opts.preserveState);

		/* schedule failure‑count reset */
		if (!this.resetTimers.has(actor.id)) {
			const timer = setTimeout(() => {
				this.failures.delete(actor.id);
				this.resetTimers.delete(actor.id);
			}, this.opts.resetTimeout);
			(timer as NodeJS.Timeout).unref?.();
			this.resetTimers.set(actor.id, timer);
		}
	}

	private calcBackoff(attempt: number): number {
		switch (this.opts.backoffType) {
			case BackoffType.NONE:
				return 0;
			case BackoffType.LINEAR:
				return Math.min(this.opts.initialDelay * attempt, this.opts.maxDelay);
			case BackoffType.EXPONENTIAL:
				return Math.min(
					this.opts.initialDelay * Math.pow(this.opts.factor, attempt - 1),
					this.opts.maxDelay
				);
			case BackoffType.RANDOM: {
				const max = Math.min(
					this.opts.initialDelay * Math.pow(this.opts.factor, attempt - 1),
					this.opts.maxDelay
				);
				return Math.floor(Math.random() * max);
			}
			default:
				return this.opts.initialDelay;
		}
	}

	cleanup(): void {
		for (const t of this.resetTimers.values()) clearTimeout(t);
		this.resetTimers.clear();
		this.failures.clear();
	}
}

/* -------------------------------------------------------------------------- */
/*  Escalate                                                                  */
/* -------------------------------------------------------------------------- */
export class EscalateStrategy extends BaseStrategy {
	readonly type = SupervisionStrategyType.ESCALATE;

	private readonly opts: Required<EscalateStrategyOptions>;
	constructor(options: EscalateStrategyOptions = {}) {
		super();
		this.opts = {
			stopActor: options.stopActor ?? false,
			transformError: options.transformError ?? ((e) => e)
		} as const;
	}

	async handleError(
		supervisor: Supervisor,
		actor: SupervisedActor<any>,
		error: Error
	): Promise<void> {
		this.logError(this.type, actor.id, error);
		const transformed = this.opts.transformError(error, actor);

		if (this.opts.stopActor) await actor.stop();

		if (supervisor.parent) {
			log(actor.id, LogLevel.INFO, `[${this.type}] escalating to ${supervisor.parent.id}`);
			await supervisor.escalateError(actor, transformed);
		} else {
			/* reached root — stop the actor so that upstream code (and our tests)
         can deterministically observe the failure being handled */
			log(actor.id, LogLevel.WARN, `[${this.type}] reached root supervisor – stopping actor`);
			await actor.stop();
		}
	}
}

/* -------------------------------------------------------------------------- */
/*  Stop                                                                      */
/* -------------------------------------------------------------------------- */
export class StopStrategy extends BaseStrategy {
	readonly type = SupervisionStrategyType.STOP;

	private readonly opts: Required<StopStrategyOptions>;
	constructor(options: StopStrategyOptions = {}) {
		super();
		this.opts = {
			notifySupervisor: options.notifySupervisor ?? true,
			cleanup: options.cleanup ?? (() => Promise.resolve())
		} as const;
	}

	async handleError(
		supervisor: Supervisor,
		actor: SupervisedActor<any>,
		error: Error
	): Promise<void> {
		this.logError(this.type, actor.id, error);
		try {
			await this.opts.cleanup(actor);
		} catch {
			/* ignore cleanup errors */
		}
		await actor.stop();
		if (this.opts.notifySupervisor) supervisor.unregisterActor(actor.id);
	}
}

/* -------------------------------------------------------------------------- */
/*  Resume                                                                    */
/* -------------------------------------------------------------------------- */
export class ResumeStrategy extends BaseStrategy {
	readonly type = SupervisionStrategyType.RESUME;

	private readonly opts: Required<ResumeStrategyOptions>;
	private readonly errors = new Map<string, number[]>();

	constructor(options: ResumeStrategyOptions = {}) {
		super();
		this.opts = {
			maxErrors: options.maxErrors ?? Number.MAX_SAFE_INTEGER,
			withinTimeWindow: options.withinTimeWindow ?? 60_000,
			fallbackStrategy: options.fallbackStrategy ?? new StopStrategy(),
			logError: options.logError ?? true
		} as const;
	}

	async handleError(
		supervisor: Supervisor,
		actor: SupervisedActor<any>,
		error: Error
	): Promise<void> {
		if (this.opts.logError) this.logError(this.type, actor.id, error);

		const now = Date.now();
		const list = this.errors.get(actor.id) ?? [];
		list.push(now);
		const start = now - this.opts.withinTimeWindow;
		this.errors.set(
			actor.id,
			list.filter((t) => t >= start)
		);

		if (list.length > this.opts.maxErrors) {
			await this.opts.fallbackStrategy.handleError(supervisor, actor, error);
		}
	}

	cleanup(): void {
		this.errors.clear();
	}
}
