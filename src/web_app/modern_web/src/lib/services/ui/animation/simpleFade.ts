/**
 * Simple Fade Transition - Fixed Implementation
 * 
 * Uses {#key} blocks to ensure proper single-element transitions
 */

import { cubicOut } from 'svelte/easing';

/**
 * Simple fade transition that works properly with Svelte's reactivity
 */
export function simpleFade(node: Element, { 
	duration = 300, 
	delay = 0,
	easing = cubicOut 
} = {}) {
	return {
		duration,
		delay,
		easing,
		css: (t: number) => `opacity: ${t}`
	};
}

/**
 * Slide fade transition for tab switching
 */
export function slideInFade(node: Element, { 
	duration = 300, 
	delay = 0,
	easing = cubicOut,
	direction = 'right'
} = {}) {
	const directions = {
		right: 'translateX(30px)',
		left: 'translateX(-30px)',
		up: 'translateY(-20px)', 
		down: 'translateY(20px)'
	};
	
	const transform = directions[direction] || directions.right;
	
	return {
		duration,
		delay,
		easing,
		css: (t: number) => `
			opacity: ${t};
			transform: ${t === 1 ? 'none' : transform};
		`
	};
}

/**
 * Quick fade for fast transitions
 */
export function quickFade(node: Element) {
	return simpleFade(node, { duration: 200 });
}

/**
 * Slow fade for deliberate transitions
 */
export function slowFade(node: Element) {
	return simpleFade(node, { duration: 400 });
}
