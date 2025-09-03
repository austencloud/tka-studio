/**
 * Sequence Machine
 *
 * This is the main entry point for the sequence state machine. It re-exports
 * the sequence machine from the modern implementation, which provides backward
 * compatibility with the legacy machine API while using the new container-based
 * implementation.
 *
 * MIGRATION NOTE: This file maintains the same API as the original sequence machine
 * but uses the new container-based implementation under the hood. Components
 * should gradually migrate to using the container directly.
 */

// Import legacy dependencies for backward compatibility
import { stateRegistry } from '../../core/registry';
import { initializePersistence } from './persistence';
import { generateSequenceActor } from './actors';

// Re-export types from the legacy implementation for backward compatibility
export * from './types';

// Import from the modern implementation
import {
	modernSequenceMachine,
	modernSequenceContainer,
	sequenceSelectors as modernSequenceSelectors,
	sequenceActions as modernSequenceActions
} from './SequenceMachine';

// Re-export the modern machine as the legacy machine
export const sequenceMachine = modernSequenceMachine;

// Register the modern machine with the registry for backward compatibility
export const sequenceActor = stateRegistry.registerMachine('sequence', modernSequenceMachine, {
	persist: true,
	description: 'Manages sequence generation and related operations'
});


// Initialize persistence
if (typeof window !== 'undefined') {
	initializePersistence(sequenceActor);
}

// Re-export the modern selectors and actions
export const sequenceSelectors = modernSequenceSelectors;
export const sequenceActions = modernSequenceActions;

// Export the modern container for direct use
export const sequenceContainer = modernSequenceContainer;
