/**
 * Actor Supervision System - Tests
 *
 * This file contains tests for the supervision system.
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { createMachine } from 'xstate';
import { SupervisedActor } from '../core/supervision/SupervisedActor';
import { Supervisor } from '../core/supervision/Supervisor';
import { RootSupervisor } from '../core/supervision/RootSupervisor';
import { RestartStrategy, StopStrategy, EscalateStrategy, ResumeStrategy } from '../core/supervision/strategies';
import { ActorHealthStatus, SupervisionStrategyType } from '../core/supervision/types';

describe('Actor Supervision System', () => {
	// Reset the root supervisor before each test
	beforeEach(() => {
		RootSupervisor.resetInstance();
	});

	// Clean up after each test
	afterEach(() => {
		vi.restoreAllMocks();
	});

	describe('SupervisedActor', () => {
		it('should create a supervised actor', () => {
			// Create a simple machine
			const machine = createMachine({
				id: 'test',
				initial: 'idle',
				states: {
					idle: {},
					active: {}
				}
			});

			// Create a supervised actor
			const actor = new SupervisedActor('test', machine, {});

			// Check that the actor was created correctly
			expect(actor.id).toBe('test');
			expect(actor.getHealthMetrics().status).toBe(ActorHealthStatus.HEALTHY);
		});

		it('should report errors', () => {
			// Create a simple machine
			const machine = createMachine({
				id: 'test',
				initial: 'idle',
				states: {
					idle: {},
					active: {}
				}
			});

			// Create a mock error handler
			const onError = vi.fn();

			// Create a supervised actor
			const actor = new SupervisedActor('test', machine, { onError });

			// Report an error
			const error = new Error('Test error');
			actor.reportError(error);

			// Check that the error was reported
			expect(onError).toHaveBeenCalledTimes(1);
			expect(onError.mock.calls[0][0].error).toBe(error);

			// Check that the health metrics were updated
			const metrics = actor.getHealthMetrics();
			expect(metrics.errorCount).toBe(1);
			expect(metrics.status).toBe(ActorHealthStatus.DEGRADED);
			expect(metrics.lastError).toBe(error);
		});

		it('should restart the actor', async () => {
			// Create a simple machine
			const machine = createMachine({
				id: 'test',
				initial: 'idle',
				states: {
					idle: {},
					active: {}
				}
			});

			// Create a mock restart handler
			const onRestart = vi.fn();

			// Create a supervised actor
			const actor = new SupervisedActor('test', machine, { onRestart });

			// Restart the actor
			await actor.restart();

			// Check that the restart handler was called
			expect(onRestart).toHaveBeenCalledTimes(1);

			// Check that the health metrics were updated
			const metrics = actor.getHealthMetrics();
			expect(metrics.restartCount).toBe(1);
			expect(metrics.status).toBe(ActorHealthStatus.HEALTHY);
		});
	});

	describe('Supervisor', () => {
		it('should register and unregister actors', () => {
			// Create a supervisor
			const supervisor = new Supervisor('test-supervisor');

			// Create a simple machine
			const machine = createMachine({
				id: 'test',
				initial: 'idle',
				states: {
					idle: {},
					active: {}
				}
			});

			// Create a supervised actor
			const actor = new SupervisedActor('test', machine, {}, supervisor);

			// Register the actor
			supervisor.registerActor(actor);

			// Check that the actor was registered
			expect(supervisor.getActor('test')).toBe(actor);

			// Unregister the actor
			supervisor.unregisterActor('test');

			// Check that the actor was unregistered
			expect(supervisor.getActor('test')).toBeUndefined();
		});

		it('should handle actor errors', async () => {
			// Create a supervisor
			const supervisor = new Supervisor('test-supervisor');

			// Create a simple machine
			const machine = createMachine({
				id: 'test',
				initial: 'idle',
				states: {
					idle: {},
					active: {}
				}
			});

			// Create a mock error handler
			const onError = vi.fn();

			// Create a supervised actor with a restart strategy
			const actor = new SupervisedActor(
				'test',
				machine,
				{
					onError,
					strategy: new RestartStrategy()
				},
				supervisor
			);

			// Register the actor
			supervisor.registerActor(actor);

			// Mock the restart method
			const restartSpy = vi.spyOn(actor, 'restart');

			// Report an error directly to the actor
			const error = new Error('Test error');
			actor.reportError(error);

			// Check that the restart method was called
			expect(restartSpy).toHaveBeenCalledTimes(1);
		});
	});

	describe('RootSupervisor', () => {
		it('should be a singleton', () => {
			// Get the root supervisor
			const root1 = RootSupervisor.getInstance();
			const root2 = RootSupervisor.getInstance();

			// Check that they are the same instance
			expect(root1).toBe(root2);
		});

		it('should handle escalated errors', async () => {
			// Get the root supervisor
			const root = RootSupervisor.getInstance();

			// Create a child supervisor
			const child = new Supervisor('child', { parent: root });

			// Create a simple machine
			const machine = createMachine({
				id: 'test',
				initial: 'idle',
				states: {
					idle: {},
					active: {}
				}
			});

			// Create a supervised actor with an escalate strategy
			const actor = new SupervisedActor(
				'test',
				machine,
				{
					strategy: new EscalateStrategy()
				},
				child
			);

			// Register the actor
			child.registerActor(actor);

			// Mock the stop method
			const stopSpy = vi.spyOn(actor, 'stop');

			// Report an error directly to the actor
			const error = new Error('Test error');
			actor.reportError(error);

			// Wait for async operations to complete
			await new Promise((resolve) => setTimeout(resolve, 10));

			// Check that the stop method was called
			expect(stopSpy).toHaveBeenCalled();
		});
	});

	describe('Supervision Strategies', () => {
		it('should restart the actor with RestartStrategy', async () => {
			// Create a supervisor
			const supervisor = new Supervisor('test-supervisor');

			// Create a simple machine
			const machine = createMachine({
				id: 'test',
				initial: 'idle',
				states: {
					idle: {},
					active: {}
				}
			});

			// Create a supervised actor with a restart strategy
			const actor = new SupervisedActor(
				'test',
				machine,
				{
					strategy: new RestartStrategy()
				},
				supervisor
			);

			// Register the actor
			supervisor.registerActor(actor);

			// Mock the restart method
			const restartSpy = vi.spyOn(actor, 'restart');

			// Report an error
			const error = new Error('Test error');
			await supervisor.handleActorError(actor, error);

			// Check that the restart method was called
			expect(restartSpy).toHaveBeenCalledTimes(1);
		});

		it('should stop the actor with StopStrategy', async () => {
			// Create a supervisor
			const supervisor = new Supervisor('test-supervisor');

			// Create a simple machine
			const machine = createMachine({
				id: 'test',
				initial: 'idle',
				states: {
					idle: {},
					active: {}
				}
			});

			// Create a supervised actor with a stop strategy
			const actor = new SupervisedActor(
				'test',
				machine,
				{
					strategy: new StopStrategy()
				},
				supervisor
			);

			// Register the actor
			supervisor.registerActor(actor);

			// Mock the stop method
			const stopSpy = vi.spyOn(actor, 'stop');

			// Report an error
			const error = new Error('Test error');
			await supervisor.handleActorError(actor, error);

			// Check that the stop method was called
			expect(stopSpy).toHaveBeenCalledTimes(1);
		});

		it('should escalate the error with EscalateStrategy', async () => {
			// Create a root supervisor
			const root = new Supervisor('root');

			// Create a child supervisor
			const child = new Supervisor('child', { parent: root });

			// Create a simple machine
			const machine = createMachine({
				id: 'test',
				initial: 'idle',
				states: {
					idle: {},
					active: {}
				}
			});

			// Create a supervised actor with an escalate strategy
			const actor = new SupervisedActor(
				'test',
				machine,
				{
					strategy: new EscalateStrategy()
				},
				child
			);

			// Register the actor
			child.registerActor(actor);

			// Mock the handleActorError method of the root supervisor
			const handleErrorSpy = vi.spyOn(root, 'handleActorError');

			// Report an error directly to the actor
			const error = new Error('Test error');
			actor.reportError(error);

			// Wait for async operations to complete
			await new Promise((resolve) => setTimeout(resolve, 10));

			// Check that the handleActorError method of the root supervisor was called
			expect(handleErrorSpy).toHaveBeenCalled();
		});

		it('should ignore the error with ResumeStrategy', async () => {
			// Create a supervisor
			const supervisor = new Supervisor('test-supervisor');

			// Create a simple machine
			const machine = createMachine({
				id: 'test',
				initial: 'idle',
				states: {
					idle: {},
					active: {}
				}
			});

			// Create a supervised actor with a resume strategy
			const actor = new SupervisedActor(
				'test',
				machine,
				{
					strategy: new ResumeStrategy()
				},
				supervisor
			);

			// Register the actor
			supervisor.registerActor(actor);

			// Mock the restart and stop methods
			const restartSpy = vi.spyOn(actor, 'restart');
			const stopSpy = vi.spyOn(actor, 'stop');

			// Report an error
			const error = new Error('Test error');
			await supervisor.handleActorError(actor, error);

			// Check that neither restart nor stop was called
			expect(restartSpy).not.toHaveBeenCalled();
			expect(stopSpy).not.toHaveBeenCalled();
		});
	});
});
