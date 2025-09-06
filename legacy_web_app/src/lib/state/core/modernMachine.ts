/**
 * Modern state machine utilities
 *
 * This module provides utilities for working with XState v5 in a way that's
 * compatible with our new state management approach using Svelte stores.
 */

import {
	createMachine as xstateCreateMachine,
	setup,
	createActor,
	type AnyActorRef,
	type AnyStateMachine,
	type ActorOptions,
	type SnapshotFrom
} from 'xstate';
import { stateRegistry } from './registry';
import { createContainer, createEffect } from './container';

/**
 * Creates an XState machine with improved ergonomics
 *
 * @param options Machine configuration options
 * @returns An XState machine
 */
export function createModernMachine<
	TContext extends Record<string, any>,
	TEvent extends { type: string }
>(options: {
	id: string;
	initial: string;
	context: TContext;
	states: Record<string, any>;
	actions?: Record<string, any>;
	services?: Record<string, any>;
	guards?: Record<string, any>;
}) {
	return setup({
		types: {} as {
			context: TContext;
			events: TEvent;
		},
		actions: options.actions || {},
		actors: options.services || {},
		guards: options.guards || {}
	}).createMachine({
		id: options.id,
		initial: options.initial,
		context: options.context,
		states: options.states
	});
}

/**
 * Creates a state container from an XState machine
 *
 * This provides a unified API for working with state machines that's
 * compatible with our container-based approach using Svelte stores.
 *
 * @param machine An XState machine
 * @param options Actor options
 * @returns A state container wrapping the machine
 */
export function createMachineContainer<
	TMachine extends AnyStateMachine,
	TEvent extends { type: string } = any
>(machine: TMachine, options: ActorOptions<TMachine> = {}): any {
	// Create the actor
	const actor = createActor(machine, options);

	// Start the actor
	actor.start();

	// Get the initial snapshot
	const initialSnapshot = actor.getSnapshot();

	// Create a safe initial state object
	const initialState = {
		value: undefined as any,
		context: undefined as any,
		status: undefined as any,
		nextEvents: undefined as any
	};

	// Copy properties from snapshot if they exist
	if (initialSnapshot) {
		// Use a try-catch to handle any potential errors
		try {
			const snapshot = initialSnapshot as any;
			if (snapshot && typeof snapshot === 'object') {
				if ('value' in snapshot) initialState.value = snapshot.value;
				if ('context' in snapshot) initialState.context = snapshot.context;
				if ('status' in snapshot) initialState.status = snapshot.status;
				if ('nextEvents' in snapshot) initialState.nextEvents = snapshot.nextEvents;
			}
		} catch (error) {
			console.error('Error copying properties from snapshot:', error);
		}
	}

	// Create a container with the state and actions
	return createContainer(initialState, (state, update) => {
		// Set up subscription to update state
		const subscription = actor.subscribe((snapshotInput) => {
			update(() => {
				// Use a try-catch to handle any potential errors
				try {
					const snapshot = snapshotInput as any;
					if (snapshot && typeof snapshot === 'object') {
						if ('value' in snapshot) state.value = snapshot.value;
						if ('context' in snapshot) state.context = snapshot.context;
						if ('status' in snapshot) state.status = snapshot.status;
						if ('nextEvents' in snapshot) state.nextEvents = snapshot.nextEvents;
					}
				} catch (error) {
					console.error('Error updating state from snapshot:', error);
				}
			});
		});

		// Create unsubscribe function
		const unsubscribe = () => {
			if (subscription && typeof subscription.unsubscribe === 'function') {
				subscription.unsubscribe();
			}
		};

		// Return actions and helper methods
		return {
			send: (event: TEvent) => actor.send(event as any),
			getSnapshot: () => actor.getSnapshot(),
			stop: () => {
				unsubscribe();
				actor.stop();
			},
			// Add helper methods for better ergonomics
			can: (eventType: string) => (actor.getSnapshot() as any).can({ type: eventType } as any),
			matches: (stateValue: string) => (actor.getSnapshot() as any).matches(stateValue),
			hasTag: (tag: string) => (actor.getSnapshot() as any).hasTag(tag),
			getActor: () => actor
		};
	});
}

/**
 * Registers a machine with the state registry
 *
 * @param id The ID to register the machine under
 * @param machine The XState machine
 * @param options Registration options
 * @returns The actor
 */
export function registerModernMachine<TMachine extends AnyStateMachine>(
	id: string,
	machine: TMachine,
	options: {
		persist?: boolean;
		description?: string;
		actorOptions?: ActorOptions<TMachine>;
	} = {}
): AnyActorRef {
	// Create the actor
	const actor = createActor(machine, options.actorOptions);

	// Start the actor
	actor.start();

	// Register with the registry
	stateRegistry.registerMachine(id, machine, {
		persist: options.persist,
		description: options.description
	});

	return actor;
}
