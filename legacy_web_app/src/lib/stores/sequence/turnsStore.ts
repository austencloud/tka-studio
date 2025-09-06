// src/lib/stores/turnsStore.ts
import { writable, derived, type Readable } from 'svelte/store';

// Define clear types
export type TurnsValue = number | 'fl';
export type Direction = 'clockwise' | 'counterclockwise' | null;

// Define state interface
export interface TurnsSide {
	turns: TurnsValue;
	direction: Direction;
}

export interface TurnsState {
	blue: TurnsSide;
	red: TurnsSide;
}

// Initial state
const initialState: TurnsState = {
	blue: { turns: 0, direction: null },
	red: { turns: 0, direction: null }
};

// Create the main store with type
const turnsState = writable<TurnsState>(initialState);

// Pure utility functions
export const parseTurnsValue = (value: TurnsValue): number => {
	return value === 'fl' ? -0.5 : Number(value);
};

export const displayTurnsValue = (n: number): TurnsValue => {
	return n === -0.5 ? 'fl' : n;
};

export const isMinTurns = (value: TurnsValue): boolean => {
	return parseTurnsValue(value) <= -0.5;
};

export const isMaxTurns = (value: TurnsValue): boolean => {
	return parseTurnsValue(value) >= 3;
};

// Derived stores for convenient access
export const blueTurns: Readable<TurnsSide> = derived(turnsState, ($state) => $state.blue);
export const redTurns: Readable<TurnsSide> = derived(turnsState, ($state) => $state.red);

// Action creators for immutable state updates
export const turnsStore = {
	// Set turns value for a side
	setTurns: (color: 'blue' | 'red', turns: TurnsValue) => {
		turnsState.update((state) => ({
			...state,
			[color]: { ...state[color], turns }
		}));
	},

	// Set rotation direction for a side
	setDirection: (color: 'blue' | 'red', direction: Direction) => {
		turnsState.update((state) => ({
			...state,
			[color]: { ...state[color], direction }
		}));
	},

	// Increment turns value for a side by 0.5 (or custom step)
	incrementTurns: (color: 'blue' | 'red', step: number = 0.5) => {
		turnsState.update((state) => {
			const currentValue = state[color].turns;
			const numericValue = parseTurnsValue(currentValue);
			const newValue = Math.min(3, numericValue + step);
			return {
				...state,
				[color]: {
					...state[color],
					turns: displayTurnsValue(newValue)
				}
			};
		});
	},

	// Decrement turns value for a side by 0.5 (or custom step)
	decrementTurns: (color: 'blue' | 'red', step: number = 0.5) => {
		turnsState.update((state) => {
			const currentValue = state[color].turns;
			const numericValue = parseTurnsValue(currentValue);
			const newValue = Math.max(-0.5, numericValue - step);
			return {
				...state,
				[color]: {
					...state[color],
					turns: displayTurnsValue(newValue)
				}
			};
		});
	},

	// Reset both sides to initial state
	reset: () => {
		turnsState.set(initialState);
	},

	// Set both sides to the same values
	setSameValues: (turns: TurnsValue, direction: Direction = null) => {
		turnsState.update((state) => ({
			blue: { ...state.blue, turns, direction },
			red: { ...state.red, turns, direction }
		}));
	},

	// Get raw state (for testing or debugging)
	getState: (): Readable<TurnsState> => turnsState
};
