import { bench, describe, beforeEach } from 'vitest';
import type { BenchFunction } from 'vitest';
import { createMachine } from 'xstate';
import { wrapBenchWithBudget, type PerformanceBudget } from './utils';
import { createSupervisedMachine } from '../machine';
import { RestartStrategy, EscalateStrategy } from '../supervision/strategies';
import { RootSupervisor } from '../supervision/RootSupervisor';
import { stateRegistry } from '../registry';

interface BenchContext {
	task: (fn: () => void) => Promise<void>;
}

// Stricter budgets for critical state operations
const actorBudget: PerformanceBudget = {
	mean: 0.5, // 0.5ms mean time budget for actor operations
	p95: 0.02,
	margin: process.env.CI ? 5 : 10
};

describe('State Management Performance', () => {
	beforeEach(() => {
		RootSupervisor.resetInstance();
		stateRegistry.clear();
	});

	describe('Actor Creation', () => {
		const testMachine = createMachine({
			id: 'test',
			initial: 'idle',
			states: { idle: {} }
		});

		bench('create supervised actor', wrapBenchWithBudget(function(this: BenchFunction, ctx: BenchContext) {
			return ctx.task(() => {
				createSupervisedMachine('bench-actor', testMachine, {
					strategy: new RestartStrategy()
				});
			});
		}));
	});

	describe('Actor Operations', () => {
		const actor = createSupervisedMachine(
			'bench-ops',
			createMachine({
				id: 'ops',
				initial: 'idle',
				states: {
					idle: { on: { NEXT: 'active' } },
					active: { on: { PREV: 'idle' } }
				}
			})
		);

		bench('send event', wrapBenchWithBudget(function(this: BenchFunction, ctx: BenchContext) {
			return ctx.task(() => {
				actor.send({ type: 'NEXT' });
				actor.send({ type: 'PREV' });
			});
		}, actorBudget));

		bench('get snapshot', wrapBenchWithBudget(function(this: BenchFunction, ctx: BenchContext) {
			return ctx.task(() => {
				actor.getSnapshot();
			});
		}, actorBudget));
	});

	describe('Registry Operations', () => {
		bench('register and unregister', wrapBenchWithBudget(function(this: BenchFunction, ctx: BenchContext) {
			return ctx.task(() => {
				const actor = createSupervisedMachine(
					'bench-reg',
					createMachine({
						id: 'reg',
						initial: 'idle',
						states: { idle: {} }
					})
				);
				stateRegistry.unregister('bench-reg');
			});
		}));
	});

	describe('Error Handling', () => {
		const actor = createSupervisedMachine(
			'bench-error',
			createMachine({
				id: 'error',
				initial: 'idle',
				states: { idle: {} }
			}),
			{
				strategy: new EscalateStrategy()
			}
		);

		bench('error reporting', wrapBenchWithBudget(function(this: BenchFunction, ctx: BenchContext) {
			return ctx.task(() => {
				actor.reportError(new Error('Benchmark error'));
			});
		}));
	});
});
