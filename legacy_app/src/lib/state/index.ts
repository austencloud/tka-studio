/**
 * State Management System
 *
 * This is the main entry point for the state management system.
 * It exports all the necessary components for managing application state.
 */

// Export core utilities
export * from './core/store';
export * from './core/registry';

// Import at the top to avoid circular dependencies
import { stateRegistry } from './core/registry';
import { appService as appActor } from './machines/app/app.machine';
import { appActions } from './machines/app/app.actions';
import * as appSelectors from './machines/app/app.selectors';
import { sequenceActor, sequenceActions, sequenceSelectors } from './machines/sequenceMachine';

// Export state machines (excluding sequenceContainer to avoid ambiguity)
export { appMachine } from './machines';

// Export stores
export * from './stores/sequenceStore';
export * from './stores/uiStore';

// Re-export specific machines for convenience
export { appActions, appSelectors, appActor };
export { sequenceActions, sequenceSelectors, sequenceActor };

/**
 * Initialize the state management system
 * This should be called early in the application lifecycle
 */
export function initializeStateManagement(): void {
	// Verify actors are registered before adding dependencies
	const registeredContainers = stateRegistry.getAll().map((container) => container.id);
	const hasSequenceActor = registeredContainers.includes('sequenceActor');
	const hasAppActor = registeredContainers.includes('appActor');

	// If actors aren't registered yet, try to register them directly
	if (!hasSequenceActor || !hasAppActor) {
		try {
			// Check again after attempted registration
			const updatedContainers = stateRegistry.getAll().map((container) => container.id);
			const nowHasSequenceActor = updatedContainers.includes('sequenceActor');
			const nowHasAppActor = updatedContainers.includes('appActor');

			// Define dependencies between actors and stores if now registered
			if (nowHasSequenceActor && nowHasAppActor) {
				stateRegistry.addDependency('sequenceActor', 'appActor');
			}
		} catch (error) {
			console.error('Error registering actors:', error);
		}
	} else {
		// Both actors are already registered, add the dependency
		stateRegistry.addDependency('sequenceActor', 'appActor');
	}

	// Get the topologically sorted initialization order
	const initOrder = stateRegistry.getInitializationOrder();

	// Start actors in dependency order
	for (const id of initOrder) {
		const container = stateRegistry.get(id);
		// Check if it's an actor (has getSnapshot and start methods)
		if (container && 'getSnapshot' in container && typeof (container as any).start === 'function') {
			const actor = container as typeof appActor;
			if (actor.getSnapshot().status !== 'active') {
				actor.start();
			}
		}
	}

	// Explicitly start critical actors that must be running
	if (appActor && appActor.getSnapshot().status !== 'active') {
		appActor.start();
	}

	if (sequenceActor && sequenceActor.getSnapshot().status !== 'active') {
		sequenceActor.start();
	}

	// Signal that the background is ready to start the app initialization
	appActions.backgroundReady();

	// Add global access for debugging in development
	if (import.meta.env.DEV && typeof window !== 'undefined') {
		(window as any).__STATE__ = {
			registry: stateRegistry,
			appActor,
			sequenceActor,
			appActions,
			sequenceActions,
			getState: (id: string) => {
				const container = stateRegistry.get(id);
				if (!container) return undefined;

				if ('getSnapshot' in container) {
					return container.getSnapshot();
				} else if ('subscribe' in container) {
					// It's a store
					const { subscribe } = container as { subscribe: any };
					let value: any;
					const unsubscribe = subscribe((v: any) => {
						value = v;
					});
					unsubscribe();
					return value;
				}

				return undefined;
			}
		};
	}
}
