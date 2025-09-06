/**
 * Machine Factory
 *
 * Provides factory functions for creating standardized XState machines.
 * These factories ensure consistent patterns and automatic registration with the state registry.
 */

import { createMachine, type AnyActorRef, type AnyStateMachine } from 'xstate';
import { stateRegistry } from './registry';
import {
  type SupervisedActorOptions,
  type Supervisor,
  type SupervisionStrategy,
  type SupervisedActor as SupervisedActorType
} from './supervision/types';
import { SupervisedActor } from './supervision/SupervisedActor';
import { RootSupervisor } from './supervision/RootSupervisor';

/**
 * Create and register a state machine
 *
 * @param id Unique identifier for the machine
 * @param machineConfig The XState machine configuration
 * @param options Additional options for the machine
 * @returns An actor reference for the machine
 */
export function createAppMachine<TMachine extends AnyStateMachine>(
  id: string,
  machine: TMachine,
  options: {
    persist?: boolean;
    description?: string;
  } = {}
): AnyActorRef {
  return stateRegistry.registerMachine(id, machine, {
    persist: options.persist,
    description: options.description
  });
}

/**
 * Create and register a supervised state machine
 *
 * This creates a machine with supervision capabilities for resilience and error recovery.
 *
 * @param id Unique identifier for the machine
 * @param machine The XState machine configuration
 * @param options Additional options for the machine including supervision options
 * @returns A supervised actor reference for the machine
 */
export function createSupervisedMachine<TMachine extends AnyStateMachine>(
  id: string,
  machine: TMachine,
  options: {
    persist?: boolean;
    description?: string;
    supervisor?: Supervisor;
    strategy?: SupervisionStrategy;
    onError?: (error: any) => void;
    onRestart?: (actor: SupervisedActorType<TMachine>) => void;
    onStop?: (actor: SupervisedActorType<TMachine>) => void;
  } = {}
): SupervisedActor<TMachine> {
  // Get or create the supervisor
  const supervisor = options.supervisor || RootSupervisor.getInstance();

  // Create supervised actor options
  const actorOptions: SupervisedActorOptions<TMachine> = {
    strategy: options.strategy,
    supervisor,
    persist: options.persist,
    description: options.description,
    onError: options.onError ? (error) => options.onError!(error.error) : undefined,
    onRestart: options.onRestart as any, // Safe to cast since we're using the correct type from types.ts
    onStop: options.onStop as any // Safe to cast since we're using the correct type from types.ts
  };

  // Create the supervised actor
  const actor = new SupervisedActor(id, machine, actorOptions, supervisor);

  // Register with the supervisor
  supervisor.registerActor(actor as any);

  /**
   * IMPORTANT TYPE FIX
   * -------------------
   * `stateRegistry.register` expects an `AnyActorRef | Readable`.
   * The internal _ref_ produced by XState (`actor.ref`) **is** an `AnyActorRef`
   * and already exposes the correct `getPersistedSnapshot()` signature.
   * We therefore register `actor.ref` (while still returning the full
   * `SupervisedActor` to callers) – this satisfies the compiler and keeps
   * supervision/registry behaviour unchanged.
   */
  stateRegistry.register(id, actor.ref, {
    type: 'machine',
    persist: options.persist,
    description: options.description
  });

  return actor;
}

/**
 * Create a standard async operation machine
 *
 * This is a common pattern for handling async operations with loading, success, and error states.
 *
 * @param id Unique identifier for the machine
 * @param asyncFn The async function to execute
 * @param options Additional options for the machine
 * @returns An actor reference for the machine
 */
export function createAsyncMachine<TData, TError = Error, TInput = void>(
  id: string,
  asyncFn: (input: TInput) => Promise<TData>,
  options: {
    persist?: boolean;
    description?: string;
    onSuccess?: (data: TData) => void;
    onError?: (error: TError) => void;
  } = {}
) {
  // Define the machine context type
  type AsyncContext = {
    data: TData | null;
    error: TError | null;
    input: TInput | null;
  };

  // Define the machine event types
  type AsyncEvents =
    | { type: 'FETCH'; input: TInput }
    | { type: 'RETRY' }
    | { type: 'SUCCESS'; data: TData }
    | { type: 'FAILURE'; error: TError };

  // Create the machine
  const asyncMachine = createMachine(
    {
      id: `${id}Machine`,
      types: {} as {
        context: AsyncContext;
        events: AsyncEvents;
      },
      context: {
        data: null,
        error: null,
        input: null
      },
      initial: 'idle',
      states: {
        idle: {
          on: {
            FETCH: {
              target: 'loading',
              actions: {
                type: 'assignInput'
              }
            }
          }
        },
        loading: {
          entry: {
            type: 'executeAsyncFn'
          },
          on: {
            SUCCESS: {
              target: 'success',
              actions: {
                type: 'assignData'
              }
            },
            FAILURE: {
              target: 'failure',
              actions: {
                type: 'assignError'
              }
            }
          }
        },
        success: {
          entry: {
            type: 'onSuccess'
          },
          on: {
            FETCH: {
              target: 'loading',
              actions: {
                type: 'assignInput'
              }
            }
          }
        },
        failure: {
          entry: {
            type: 'onError'
          },
          on: {
            RETRY: 'loading',
            FETCH: {
              target: 'loading',
              actions: {
                type: 'assignInput'
              }
            }
          }
        }
      }
    },
    {
      actions: {
        assignInput: ({ context, event }) => {
          if (event.type === 'FETCH') {
            context.input = event.input;
          }
        },
        assignData: ({ context, event }) => {
          if (event.type === 'SUCCESS') {
            context.data = event.data;
            context.error = null;
          }
        },
        assignError: ({ context, event }) => {
          if (event.type === 'FAILURE') {
            context.error = event.error;
          }
        },
        executeAsyncFn: ({ context, self }) => {
          if (context.input !== null) {
            asyncFn(context.input as TInput)
              .then((data) => {
                self.send({ type: 'SUCCESS', data });
              })
              .catch((error) => {
                self.send({ type: 'FAILURE', error });
              });
          }
        },
        onSuccess: ({ context }) => {
          if (options.onSuccess && context.data !== null) {
            options.onSuccess(context.data);
          }
        },
        onError: ({ context }) => {
          if (options.onError && context.error !== null) {
            options.onError(context.error);
          }
        }
      }
    }
  );

  // Register and return the machine
  return stateRegistry.registerMachine(id, asyncMachine, {
    persist: options.persist,
    description: options.description
  });
}
