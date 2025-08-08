// src/lib/utils/turnsUtils.ts

export type TurnsValue = number | 'fl';

/**
 * Converts a TurnsValue to its internal numeric representation
 * - "fl" is represented as -0.5 internally
 * - numbers are returned as-is
 */
export function parseTurnsValue(value: TurnsValue): number {
	return value === 'fl' ? -0.5 : Number(value);
}

/**
 * Formats a numeric value to its display representation
 * - -0.5 is displayed as "fl" (flutter)
 * - other numbers are converted to strings
 */
export function displayTurnsValue(n: number): TurnsValue {
	return n === -0.5 ? 'fl' : n;
}

/**
 * Adjusts turns by the given delta, clamping to valid range
 * @param currentValue Current turns value
 * @param delta Amount to adjust by (typically +/- 0.5)
 * @returns New turns value constrained to valid range
 */
export function adjustTurns(currentValue: TurnsValue, delta: number): TurnsValue {
	const numericValue = parseTurnsValue(currentValue);
	const newValue = Math.max(-0.5, Math.min(3, numericValue + delta));
	return displayTurnsValue(newValue);
}

/**
 * Returns whether a turns value is at minimum allowed value
 */
export function isMinTurns(value: TurnsValue): boolean {
	return parseTurnsValue(value) <= -0.5;
}

/**
 * Returns whether a turns value is at maximum allowed value
 */
export function isMaxTurns(value: TurnsValue): boolean {
	return parseTurnsValue(value) >= 3;
}
