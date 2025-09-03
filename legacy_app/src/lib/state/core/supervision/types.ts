/**
 * Actor Supervision System - Type Definitions
 *
 * This file contains TypeScript interfaces and types for the supervision system.
 */

import type {
	AnyStateMachine,
	Actor,
	ActorOptions,
	SnapshotFrom,
	Snapshot,
	ActorRefFrom
} from 'xstate';

/**
 * Supervision strategy types that determine how to handle actor failures
 */
export enum SupervisionStrategyType {
	RESTART = 'restart',
	STOP = 'stop',
	ESCALATE = 'escalate',
	RESUME = 'resume'
}

/**
 * Backoff strategy types for restart strategies
 */
export enum BackoffType {
	NONE = 'none',
	LINEAR = 'linear',
	EXPONENTIAL = 'exponential',
	RANDOM = 'random'
}

/**
 * Base interface for all supervision strategies
 */
export interface SupervisionStrategy {
	/**
	 * The type of strategy
	 */
	type: SupervisionStrategyType;

	/**
	 * Handle an error that occurred in a supervised actor
	 * @param supervisor The supervisor handling the error
	 * @param actor The actor that experienced the error
	 * @param error The error that occurred
	 * @returns A promise that resolves when the strategy has been applied
	 */
	handleError(supervisor: Supervisor, actor: SupervisedActor<any>, error: Error): Promise<void>;
}

/**
 * Options for the restart strategy
 */
export interface RestartStrategyOptions {
	/**
	 * Maximum number of restarts allowed within the time window
	 * If exceeded, the actor will be stopped
	 */
	maxRestarts?: number;

	/**
	 * Time window in milliseconds for counting restarts
	 */
	withinTimeWindow?: number;

	/**
	 * Type of backoff to use between restart attempts
	 */
	backoffType?: BackoffType;

	/**
	 * Initial delay in milliseconds before restarting
	 */
	initialDelay?: number;

	/**
	 * Maximum delay in milliseconds for backoff
	 */
	maxDelay?: number;

	/**
	 * Factor to use for exponential backoff
	 */
	factor?: number;

	/**
	 * Time in milliseconds after which to reset the failure count
	 */
	resetTimeout?: number;

	/**
	 * Whether to preserve the actor's state when restarting
	 * If true, the actor will be restarted with its last snapshot
	 * If false, the actor will be restarted with its initial state
	 */
	preserveState?: boolean;
}

/**
 * Options for the escalate strategy
 */
export interface EscalateStrategyOptions {
	/**
	 * Whether to stop the actor before escalating
	 */
	stopActor?: boolean;

	/**
	 * Transform the error before escalating
	 */
	transformError?: (error: Error, actor: SupervisedActor<any>) => Error;
}

/**
 * Options for the stop strategy
 */
export interface StopStrategyOptions {
	/**
	 * Whether to notify the supervisor of the stop
	 */
	notifySupervisor?: boolean;

	/**
	 * Custom cleanup function to run before stopping
	 */
	cleanup?: (actor: SupervisedActor<any>) => Promise<void> | void;
}

/**
 * Options for the resume strategy
 */
export interface ResumeStrategyOptions {
	/**
	 * Maximum number of errors to ignore before changing strategy
	 */
	maxErrors?: number;

	/**
	 * Time window in milliseconds for counting errors
	 */
	withinTimeWindow?: number;

	/**
	 * Strategy to use when max errors is exceeded
	 */
	fallbackStrategy?: SupervisionStrategy;

	/**
	 * Whether to log the error even though it's being ignored
	 */
	logError?: boolean;
}

/**
 * Health status of a supervised actor
 */
export enum ActorHealthStatus {
	HEALTHY = 'healthy',
	DEGRADED = 'degraded',
	UNHEALTHY = 'unhealthy',
	STOPPED = 'stopped'
}

/**
 * Health metrics for a supervised actor
 */
export interface ActorHealthMetrics {
	/**
	 * Current health status
	 */
	status: ActorHealthStatus;

	/**
	 * Number of errors that have occurred
	 */
	errorCount: number;

	/**
	 * Number of restarts that have occurred
	 */
	restartCount: number;

	/**
	 * Timestamp of the last error
	 */
	lastErrorTime?: number;

	/**
	 * Timestamp of the last restart
	 */
	lastRestartTime?: number;

	/**
	 * The last error that occurred
	 */
	lastError?: Error;

	/**
	 * Time the actor has been running in milliseconds
	 */
	uptime: number;

	/**
	 * Timestamp when the actor was created
	 */
	createdAt: number;
}

/**
 * Error information for supervision
 */
export interface SupervisionError {
	/**
	 * The error that occurred
	 */
	error: Error;

	/**
	 * The actor that experienced the error
	 */
	actorId: string;

	/**
	 * Timestamp when the error occurred
	 */
	timestamp: number;

	/**
	 * The state of the actor when the error occurred
	 */
	actorState?: any;

	/**
	 * Additional context about the error
	 */
	context?: Record<string, any>;
}

/**
 * Options for creating a supervised actor
 */
export interface SupervisedActorOptions<TMachine extends AnyStateMachine>
	extends ActorOptions<TMachine> {
	/**
	 * The supervision strategy to use
	 */
	strategy?: SupervisionStrategy;

	/**
	 * The supervisor for this actor
	 */
	supervisor?: Supervisor;

	/**
	 * Whether to persist the actor's state
	 */
	persist?: boolean;

	/**
	 * Description of the actor
	 */
	description?: string;

	/**
	 * Initial health status
	 */
	initialHealth?: ActorHealthStatus;

	/**
	 * Custom error handler
	 */
	onError?: (error: SupervisionError) => void;

	/**
	 * Function to call when the actor is restarted
	 */
	onRestart?: (actor: SupervisedActor<TMachine>) => void;

	/**
	 * Function to call when the actor is stopped
	 */
	onStop?: (actor: SupervisedActor<TMachine>) => void;
}

/**
 * Interface for a supervised actor
 * Extends Actor but adds supervision capabilities
 */ export interface SupervisedActor<TMachine extends AnyStateMachine> {
	/*  — structural contract — */
	readonly id: string;
	strategy: SupervisionStrategy;
	supervisor?: Supervisor;

	/** actor-like helpers */
	send: Actor<TMachine>['send'];
	subscribe: Actor<TMachine>['subscribe'];
	on: Actor<TMachine>['on'];
	getSnapshot: Actor<TMachine>['getSnapshot'];
	readonly ref: ActorRefFrom<TMachine>;

	/** lifecycle */
	start(): this;
	stop(): this;
	restart(preserveState?: boolean): Promise<void>;

	/** health & persistence */
	getHealthMetrics(): ActorHealthMetrics;
	getPersistedSnapshot(): SnapshotFrom<TMachine> | undefined;

	/** convenience */
	getMachine(): TMachine;
	getOptions(): SupervisedActorOptions<TMachine>;
	reportError(error: Error, context?: Record<string, any>): void;
}

/**
 * Interface for a supervisor
 */
export interface Supervisor {
	/**
	 * The unique ID of the supervisor
	 */
	id: string;

	/**
	 * The parent supervisor, if any
	 */
	parent?: Supervisor;

	/**
	 * The supervised actors managed by this supervisor
	 */
	actors: Map<string, SupervisedActor<any>>;

	/**
	 * The default strategy to use for actors that don't specify one
	 */
	defaultStrategy: SupervisionStrategy;

	/**
	 * Register an actor with this supervisor
	 */
	registerActor(actor: SupervisedActor<any>): void;

	/**
	 * Unregister an actor from this supervisor
	 */
	unregisterActor(actorId: string): void;

	/**
	 * Handle an error from a supervised actor
	 */
	handleActorError(
		actor: SupervisedActor<any>,
		error: Error,
		context?: Record<string, any>
	): Promise<void>;

	/**
	 * Escalate an error to the parent supervisor
	 */
	escalateError(
		actor: SupervisedActor<any>,
		error: Error,
		context?: Record<string, any>
	): Promise<void>;

	/**
	 * Stop all supervised actors
	 */
	stopAllActors(): Promise<void>;

	/**
	 * Get all supervised actors
	 */
	getAllActors(): SupervisedActor<any>[];

	/**
	 * Get a supervised actor by ID
	 */
	getActor(actorId: string): SupervisedActor<any> | undefined;
}

/**
 * Circuit breaker states
 */
export enum CircuitBreakerState {
	CLOSED = 'closed', // Normal operation, requests pass through
	OPEN = 'open', // Failure threshold exceeded, requests fail fast
	HALF_OPEN = 'half-open' // Testing if the system has recovered
}

/**
 * Options for a circuit breaker
 */
export interface CircuitBreakerOptions {
	/**
	 * Number of failures before opening the circuit
	 */
	failureThreshold: number;

	/**
	 * Time window in milliseconds for counting failures
	 */
	failureWindowMs: number;

	/**
	 * Time in milliseconds to keep the circuit open before trying half-open
	 */
	resetTimeoutMs: number;

	/**
	 * Number of successful operations in half-open state to close the circuit
	 */
	successThreshold: number;
}

/**
 * Interface for a circuit breaker
 */
export interface CircuitBreaker {
	/**
	 * Current state of the circuit breaker
	 */
	state: CircuitBreakerState;

	/**
	 * Record a successful operation
	 */
	recordSuccess(): void;

	/**
	 * Record a failed operation
	 */
	recordFailure(error: Error): void;

	/**
	 * Check if the circuit is closed (allowing operations)
	 */
	isAllowed(): boolean;

	/**
	 * Reset the circuit breaker to closed state
	 */
	reset(): void;
}

/**
 * Options for creating a root supervisor
 */
export interface RootSupervisorOptions {
	/**
	 * Default strategy to use for actors that don't specify one
	 */
	defaultStrategy?: SupervisionStrategy;

	/**
	 * Circuit breaker options
	 */
	circuitBreaker?: CircuitBreakerOptions;

	/**
	 * Global error handler
	 */
	onError?: (error: SupervisionError) => void;

	/**
	 * Whether to enable debug logging
	 */
	debug?: boolean;
}

/**
 * Plugin interface for custom supervision strategies
 */
export interface SupervisionStrategyPlugin<TConfig = unknown> {
	readonly type: string;
	readonly defaultConfig: TConfig;
	createStrategy(config?: Partial<TConfig>): SupervisionStrategy;
}

/**
 * Registry for supervision strategy plugins
 */
export interface StrategyRegistry {
	register<TConfig>(plugin: SupervisionStrategyPlugin<TConfig>): void;
	unregister(type: string): void;
	get(type: string): SupervisionStrategyPlugin | undefined;
	create(type: string, config?: unknown): SupervisionStrategy;
}
