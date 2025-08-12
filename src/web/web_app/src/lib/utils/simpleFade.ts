/**
 * Simple, Minimal Fade System
 * Just the basics: fade out, change content, fade in
 */

import { cubicOut } from 'svelte/easing';

/**
 * Basic fade transition
 */
export function fade(node: Element, { duration = 300, delay = 0 } = {}) {
	// Touch the node so parameter isn't flagged as unused and ensure initial opacity
	(node as HTMLElement).style.willChange = 'opacity';
	return {
		duration,
		delay,
		easing: cubicOut,
		css: (t: number) => `opacity: ${t}`,
	};
}

/**
 * Sequential fade out (no delay)
 */
export function fadeOut(
	node: Element,
	{
		duration = 250,
		settings,
	}: { duration?: number; settings?: { animationsEnabled?: boolean } } = {}
) {
	if (!shouldAnimate(settings)) {
		return { duration: 0 };
	}

	return fade(node, { duration, delay: 0 });
}

/**
 * Sequential fade in (with delay to wait for fade out)
 */
export function fadeIn(
	node: Element,
	{
		duration = 250,
		outDuration = 250,
		settings,
	}: { duration?: number; outDuration?: number; settings?: { animationsEnabled?: boolean } } = {}
) {
	if (!shouldAnimate(settings)) {
		return { duration: 0 };
	}

	return fade(node, { duration, delay: outDuration });
}

/**
 * Check if animations should be enabled based on user preferences
 */
export function shouldAnimate(settings?: { animationsEnabled?: boolean }): boolean {
	// Respect user's reduced motion preference
	if (typeof window !== 'undefined') {
		const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		if (prefersReducedMotion) return false;
	}

	// Respect app settings
	return settings?.animationsEnabled !== false;
}

/**
 * Conditional fade that respects settings
 */
export function conditionalFade(
	node: Element,
	params: { duration?: number; settings?: { animationsEnabled?: boolean } } = {}
) {
	const { duration = 300, settings } = params;

	if (!shouldAnimate(settings)) {
		return { duration: 0 };
	}

	return fade(node, { duration });
}
