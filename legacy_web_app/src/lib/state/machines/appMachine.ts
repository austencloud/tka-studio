/*
 * App State Machine – XState v5 fully‑typed fix
 * --------------------------------------------
 * Resolves the type‑parameter mismatches (TS2558) by adopting the
 * v5 `types` declaration block. All context & event typing now lives
 * inside the machine config, so `createMachine`/`assign` don’t need the
 * long generic lists. This also ensures `event` is never nullable.
 */

import { createMachine, assign } from 'xstate';
import { stateRegistry } from '../core/registry';

// ─────────────────────────────────────────────────────────────
// Machine definition
// ─────────────────────────────────────────────────────────────

export const appMachine = createMachine({
	/**
	 * Inline type‑safety (XState v5 style)
	 */
	types: {} as {
		context: {
			currentTab: number;
			isLoading: boolean;
		};
		events: { type: 'LOADING' } | { type: 'LOADED' } | { type: 'CHANGE_TAB'; tab: number };
	},

	id: 'app',
	initial: 'loading',
	context: {
		currentTab: 0,
		isLoading: true
	},

	states: {
		/** Loading ------------------------------------------------*/
		loading: {
			entry: assign({
				isLoading: () => true
			}),
			on: {
				LOADED: 'ready'
			},
			after: {
				1000: 'ready'
			}
		},

		/** Ready --------------------------------------------------*/
		ready: {
			entry: assign({
				isLoading: () => false
			}),
			on: {
				LOADING: 'loading',
				CHANGE_TAB: {
					actions: assign({
						currentTab: ({ context, event }) =>
							event.type === 'CHANGE_TAB' ? event.tab : context.currentTab
					})
				}
			}
		}
	}
});

// ─────────────────────────────────────────────────────────────
// Actor registration
// ─────────────────────────────────────────────────────────────

export const appActor = stateRegistry.registerMachine('app', appMachine, {
	persist: true,
	description: 'Main application state'
});

// ─────────────────────────────────────────────────────────────
// Convenience helpers
// ─────────────────────────────────────────────────────────────

export const appActions = {
	changeTab: (tab: number) => appActor.send({ type: 'CHANGE_TAB', tab }),
	setLoading: (isLoading: boolean) => appActor.send({ type: isLoading ? 'LOADING' : 'LOADED' })
};

export const appSelectors = {
	isLoading: () => appActor.getSnapshot().context.isLoading,
	currentTab: () => appActor.getSnapshot().context.currentTab
};
