/**
 * Simple, Reliable Fade System - Gold Standard Implementation
 * Replaces the over-engineered animation directory entirely
 */

import { cubicOut } from 'svelte/easing';

// ============================================================================
// CORE TRANSITIONS - Simple and bulletproof
// ============================================================================

export function fade(node: Element, { duration = 300, delay = 0, easing = cubicOut } = {}) {
	return {
		duration,
		delay,
		easing,
		css: (t: number) => `opacity: ${t}`,
	};
}

export function slideInFade(
	node: Element,
	{ duration = 300, delay = 0, easing = cubicOut, direction = 'right' } = {}
) {
	const offsets = {
		right: 'translateX(20px)',
		left: 'translateX(-20px)',
		up: 'translateY(-20px)',
		down: 'translateY(20px)',
	};

	return {
		duration,
		delay,
		easing,
		css: (t: number) => `
            opacity: ${t};
            transform: ${t < 1 ? offsets[direction] : 'none'};
        `,
	};
}

// ============================================================================
// CROSSFADE - Simple implementation that actually works
// ============================================================================

export function createCrossfade(duration = 300) {
	const crossfadeMap = new Map();

	function crossfade(node: Element, { key }: { key: string }) {
		return () => {
			const other = crossfadeMap.get(key);
			crossfadeMap.delete(key);

			if (other) {
				return fade(node, { duration });
			}

			crossfadeMap.set(key, node);
			return fade(node, { duration });
		};
	}

	return [crossfade, crossfade];
}

// ============================================================================
// PRESETS - Common transition patterns
// ============================================================================

export const fastFade = (node: Element) => fade(node, { duration: 200 });
export const normalFade = (node: Element) => fade(node, { duration: 300 });
export const slowFade = (node: Element) => fade(node, { duration: 400 });

export const slideLeft = (node: Element) => slideInFade(node, { direction: 'left' });
export const slideRight = (node: Element) => slideInFade(node, { direction: 'right' });
export const slideUp = (node: Element) => slideInFade(node, { direction: 'up' });
export const slideDown = (node: Element) => slideInFade(node, { direction: 'down' });

// ============================================================================
// TAB TRANSITIONS - Specific for main interface
// ============================================================================

export const [tabSend, tabReceive] = createCrossfade(300);

export function createTabTransitions() {
	return {
		in: (node: Element) =>
			slideInFade(node, {
				duration: 300,
				direction: 'right',
			}),
		out: (node: Element) =>
			fade(node, {
				duration: 250,
			}),
	};
}

// ============================================================================
// SETTINGS - Simple animation control
// ============================================================================

let animationsEnabled = true;

export function setAnimationsEnabled(enabled: boolean) {
	animationsEnabled = enabled;
}

export function isAnimationsEnabled() {
	return animationsEnabled;
}

// Wrapper that respects animation settings
export function conditionalTransition(transitionFn: Function) {
	return (node: Element, params?: any) => {
		if (!animationsEnabled) {
			return { duration: 0 };
		}
		return transitionFn(node, params);
	};
}
