/**
 * Custom Fade Transitions for TKA Web App
 * Ported and adapted from desktop app fade manager
 */

import { cubicOut, quintOut } from 'svelte/easing';
import type { TransitionConfig, CrossfadeConfig } from './fadeTypes';

// Default fade configuration matching desktop app behavior
const DEFAULT_FADE_CONFIG = {
	duration: 250,
	delay: 0,
	easing: cubicOut,
	opacity: {
		start: 0,
		end: 1
	}
};

/**
 * Enhanced fade transition with more control than built-in fade
 * Mimics desktop app's widget fader behavior
 */
export function enhancedFade(node: Element, config: TransitionConfig = {}) {
	const {
		duration = DEFAULT_FADE_CONFIG.duration,
		delay = DEFAULT_FADE_CONFIG.delay,
		easing = DEFAULT_FADE_CONFIG.easing,
		opacity = DEFAULT_FADE_CONFIG.opacity,
		direction = 'both'
	} = config;

	// Get current opacity from computed styles
	const computedStyle = getComputedStyle(node as HTMLElement);
	const currentOpacity = parseFloat(computedStyle.opacity);
	
	const startOpacity = direction === 'out' ? currentOpacity : opacity.start!;
	const endOpacity = direction === 'out' ? opacity.start! : opacity.end!;

	return {
		duration,
		delay,
		easing,
		css: (t: number) => {
			const opacityValue = startOpacity + (endOpacity - startOpacity) * t;
			return `opacity: ${opacityValue}`;
		}
	};
}

/**
 * Crossfade transition for smooth tab switching
 * Adapted from Svelte's crossfade but with TKA-specific behavior
 */
export function createTabCrossfade(options: Partial<CrossfadeConfig> = {}) {
	const {
		duration = 300,
		delay = 0,
		easing = quintOut,
		fallback = enhancedFade
	} = options;

	const transitions = new Map();
	
	function crossfadeTransition(
		node: Element, 
		params: CrossfadeConfig & { key: string }
	) {
		const {
			key,
			duration: paramDuration = duration,
			delay: paramDelay = delay,
			easing: paramEasing = easing
		} = params;

		// This is the deferred transition pattern
		return () => {
			const other = transitions.get(key);
			
			if (other) {
				// Remove the other transition so it's not reused
				transitions.delete(key);
				
				// Get rects for both elements
				const rect = node.getBoundingClientRect();
				const otherRect = other.getBoundingClientRect();
				
				// Calculate transform deltas
				const deltaX = otherRect.left - rect.left;
				const deltaY = otherRect.top - rect.top;
				const deltaWidth = otherRect.width / rect.width;
				const deltaHeight = otherRect.height / rect.height;

				return {
					duration: paramDuration,
					delay: paramDelay,
					easing: paramEasing,
					css: (t: number, u: number) => {
						// Interpolate position and scale
						const x = deltaX * u;
						const y = deltaY * u;
						const scaleX = 1 + (deltaWidth - 1) * u;
						const scaleY = 1 + (deltaHeight - 1) * u;
						
						return `
							transform: translate(${x}px, ${y}px) scale(${scaleX}, ${scaleY});
							opacity: ${t};
						`;
					}
				};
			}
			
			// Store this node's rect for potential matching
			transitions.set(key, node.getBoundingClientRect());
			
			// Return fallback transition if no match
			return fallback(node, params);
		};
	}

	return [
		(node: Element, params: CrossfadeConfig) => crossfadeTransition(node, { ...params }),
		(node: Element, params: CrossfadeConfig) => crossfadeTransition(node, { ...params })
	];
}

/**
 * Slide fade transition - slides and fades simultaneously
 * Perfect for tab content switching
 */
export function slideFade(
	node: Element,
	config: TransitionConfig & { 
		direction?: 'left' | 'right' | 'up' | 'down';
		distance?: number;
	} = {}
) {
	const {
		duration = 300,
		delay = 0,
		easing = quintOut,
		direction: slideDirection = 'right',
		distance = 100,
		opacity = DEFAULT_FADE_CONFIG.opacity
	} = config;

	const currentOpacity = parseFloat(getComputedStyle(node as HTMLElement).opacity);
	const startOpacity = opacity.start!;
	const endOpacity = opacity.end!;

	// Direction vectors
	const vectors = {
		left: [-distance, 0],
		right: [distance, 0],
		up: [0, -distance],
		down: [0, distance]
	};

	const [x, y] = vectors[slideDirection];

	return {
		duration,
		delay,
		easing,
		css: (t: number) => {
			const opacityValue = startOpacity + (endOpacity - startOpacity) * t;
			const transformX = x * (1 - t);
			const transformY = y * (1 - t);
			
			return `
				opacity: ${opacityValue};
				transform: translate(${transformX}px, ${transformY}px);
			`;
		}
	};
}

/**
 * Scale fade transition - scales and fades
 * Great for modal-like transitions
 */
export function scaleFade(
	node: Element,
	config: TransitionConfig & { 
		scale?: { start: number; end: number };
	} = {}
) {
	const {
		duration = 300,
		delay = 0,
		easing = quintOut,
		scale = { start: 0.8, end: 1.0 },
		opacity = DEFAULT_FADE_CONFIG.opacity
	} = config;

	return {
		duration,
		delay,
		easing,
		css: (t: number) => {
			const opacityValue = opacity.start! + (opacity.end! - opacity.start!) * t;
			const scaleValue = scale.start + (scale.end - scale.start) * t;
			
			return `
				opacity: ${opacityValue};
				transform: scale(${scaleValue});
				transform-origin: center;
			`;
		}
	};
}

/**
 * Fluid transition that combines multiple effects
 * Mimics the desktop app's sophisticated fade patterns
 */
export function fluidTransition(
	node: Element,
	config: TransitionConfig & {
		effects?: ('fade' | 'slide' | 'scale')[];
		slideDirection?: 'left' | 'right' | 'up' | 'down';
		scale?: { start: number; end: number };
		distance?: number;
	} = {}
) {
	const {
		duration = 350,
		delay = 0,
		easing = quintOut,
		effects = ['fade', 'slide'],
		slideDirection = 'right',
		scale = { start: 0.95, end: 1.0 },
		distance = 50,
		opacity = DEFAULT_FADE_CONFIG.opacity
	} = config;

	const vectors = {
		left: [-distance, 0],
		right: [distance, 0],
		up: [0, -distance],
		down: [0, distance]
	};

	const [x, y] = vectors[slideDirection];

	return {
		duration,
		delay,
		easing,
		css: (t: number) => {
			const styles: string[] = [];

			if (effects.includes('fade')) {
				const opacityValue = opacity.start! + (opacity.end! - opacity.start!) * t;
				styles.push(`opacity: ${opacityValue}`);
			}

			const transforms: string[] = [];

			if (effects.includes('slide')) {
				const transformX = x * (1 - t);
				const transformY = y * (1 - t);
				transforms.push(`translate(${transformX}px, ${transformY}px)`);
			}

			if (effects.includes('scale')) {
				const scaleValue = scale.start + (scale.end - scale.start) * t;
				transforms.push(`scale(${scaleValue})`);
			}

			if (transforms.length > 0) {
				styles.push(`transform: ${transforms.join(' ')}`);
				styles.push('transform-origin: center');
			}

			return styles.join('; ');
		}
	};
}

// Export commonly used transition instances
export const [tabSend, tabReceive] = createTabCrossfade({
	duration: 300,
	easing: quintOut
});

export const quickFade = (node: Element) => enhancedFade(node, { duration: 200 });
export const slowFade = (node: Element) => enhancedFade(node, { duration: 500 });

export const slideLeft = (node: Element) => slideFade(node, { 
	direction: 'left', 
	duration: 300 
});

export const slideRight = (node: Element) => slideFade(node, { 
	direction: 'right', 
	duration: 300 
});

export const slideUp = (node: Element) => slideFade(node, { 
	direction: 'up', 
	duration: 300 
});

export const slideDown = (node: Element) => slideFade(node, { 
	direction: 'down', 
	duration: 300 
});
