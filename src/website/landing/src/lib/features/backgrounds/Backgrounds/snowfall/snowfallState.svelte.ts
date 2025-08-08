// src/lib/components/Backgrounds/snowfall/store.svelte.ts
// Svelte 5 runes-based snowfall store

import type { Dimensions, PerformanceMetrics } from '../types/types';

// Create reactive state using Svelte 5 runes
export const snowfallState = {
	dimensions: $state<Dimensions>({ width: 0, height: 0 }),
	performanceMetrics: $state<PerformanceMetrics>({ fps: 60, warnings: [] }),
	isActive: $state<boolean>(true),
	isDecember: $state<boolean>(false),
	qualityMode: $state<'high' | 'medium' | 'low'>('high')
};

// Derived state as function (Svelte 5 requirement)
export function shouldRender() {
	return snowfallState.isActive && snowfallState.performanceMetrics.fps > 30;
}

// Export getter functions for components that need to access the state
export function getSnowfallState() {
	return snowfallState;
}

// Export individual state getters for backward compatibility
export function getDimensions() {
	return snowfallState.dimensions;
}

export function getPerformanceMetrics() {
	return snowfallState.performanceMetrics;
}

export function getIsActive() {
	return snowfallState.isActive;
}

export function getIsDecember() {
	return snowfallState.isDecember;
}

export function getQualityMode() {
	return snowfallState.qualityMode;
}

// Export setter functions
export function setDimensions(dimensions: Dimensions) {
	snowfallState.dimensions = dimensions;
}

export function setPerformanceMetrics(metrics: PerformanceMetrics) {
	snowfallState.performanceMetrics = metrics;
}

export function setIsActive(active: boolean) {
	snowfallState.isActive = active;
}

export function setIsDecember(isDecember: boolean) {
	snowfallState.isDecember = isDecember;
}

export function setQualityMode(mode: 'high' | 'medium' | 'low') {
	snowfallState.qualityMode = mode;
}

// Compatibility layer for old store API
export const dimensions = {
	get value() {
		return snowfallState.dimensions;
	},
	set: setDimensions,
	update: (fn: (value: Dimensions) => Dimensions) => {
		snowfallState.dimensions = fn(snowfallState.dimensions);
	}
};

export const performanceMetrics = {
	get value() {
		return snowfallState.performanceMetrics;
	},
	set: setPerformanceMetrics,
	update: (fn: (value: PerformanceMetrics) => PerformanceMetrics) => {
		snowfallState.performanceMetrics = fn(snowfallState.performanceMetrics);
	}
};

export const isActive = {
	get value() {
		return snowfallState.isActive;
	},
	set: setIsActive,
	update: (fn: (value: boolean) => boolean) => {
		snowfallState.isActive = fn(snowfallState.isActive);
	}
};

export const isDecember = {
	get value() {
		return snowfallState.isDecember;
	},
	set: setIsDecember,
	update: (fn: (value: boolean) => boolean) => {
		snowfallState.isDecember = fn(snowfallState.isDecember);
	}
};

export const qualityMode = {
	get value() {
		return snowfallState.qualityMode;
	},
	set: setQualityMode,
	update: (fn: (value: 'high' | 'medium' | 'low') => 'high' | 'medium' | 'low') => {
		snowfallState.qualityMode = fn(snowfallState.qualityMode);
	}
};
