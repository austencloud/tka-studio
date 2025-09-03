/**
 * Actor Supervision System - Circuit Breaker
 *
 * This file contains the implementation of the circuit breaker pattern
 * to prevent cascading failures in the actor system.
 */

import { debug, warn } from '../logger/logging';
import type { CircuitBreaker, CircuitBreakerOptions } from './types';
import { CircuitBreakerState } from './types';

export class DefaultCircuitBreaker implements CircuitBreaker {
	private failures: number[] = [];
	private successes = 0;
	private _state = CircuitBreakerState.CLOSED;
	private lastTransition = Date.now();
	private readonly id: string;

	constructor(
		id: string,
		private readonly options: Required<CircuitBreakerOptions>
	) {
		this.id = id;
		debug('circuit-breaker', `Created circuit breaker ${id}`, options);
	}

	get state(): CircuitBreakerState {
		return this._state;
	}

	recordSuccess(): void {
		const now = Date.now();

		if (this._state === CircuitBreakerState.HALF_OPEN) {
			this.successes++;
			debug('circuit-breaker', `Success recorded in HALF-OPEN state`, {
				id: this.id,
				successes: this.successes,
				threshold: this.options.successThreshold
			});

			if (this.successes >= this.options.successThreshold) {
				this.transitionTo(CircuitBreakerState.CLOSED);
			}
		}

		this.failures = this.failures.filter((time) => time >= now - this.options.failureWindowMs);
	}

	recordFailure(err: Error): void {
		const now = Date.now();

		if (this._state === CircuitBreakerState.CLOSED) {
			this.failures.push(now);
			this.failures = this.failures.filter((time) => time >= now - this.options.failureWindowMs);

			if (this.failures.length >= this.options.failureThreshold) {
				warn('circuit-breaker', `Failure threshold exceeded`, {
					id: this.id,
					failures: this.failures.length,
					threshold: this.options.failureThreshold,
					error: err.message
				});
				this.transitionTo(CircuitBreakerState.OPEN);
			}
		} else if (this._state === CircuitBreakerState.HALF_OPEN) {
			warn('circuit-breaker', `Failure in HALF-OPEN state`, {
				id: this.id,
				error: err.message
			});
			this.transitionTo(CircuitBreakerState.OPEN);
		}
	}

	isAllowed(): boolean {
		const now = Date.now();

		if (
			this._state === CircuitBreakerState.OPEN &&
			now - this.lastTransition >= this.options.resetTimeoutMs
		) {
			this.transitionTo(CircuitBreakerState.HALF_OPEN);
		}

		return this._state !== CircuitBreakerState.OPEN;
	}

	reset(): void {
		this.failures = [];
		this.successes = 0;
		this.transitionTo(CircuitBreakerState.CLOSED);
		debug('circuit-breaker', `Circuit breaker reset`, { id: this.id });
	}

	private transitionTo(newState: CircuitBreakerState): void {
		const oldState = this._state;
		this._state = newState;
		this.lastTransition = Date.now();
		this.successes = 0;

		debug('circuit-breaker', `State transition`, {
			id: this.id,
			from: oldState,
			to: newState
		});
	}
}
