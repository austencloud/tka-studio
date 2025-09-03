// src/lib/components/MainWidget/utils/transitionHelpers.ts
import { fade, fly, scale, slide } from 'svelte/transition';
import { quintOut, elasticOut } from 'svelte/easing';

// Type for transition configuration
export type TransitionConfig = {
	fn: typeof fade | typeof fly | typeof scale | typeof slide;
	props: Record<string, any>;
};

// Pure function to map tab index to transition configuration
export function getTransitionProps(tabIndex: number, isSlideRight: boolean): TransitionConfig {
	const transitions: TransitionConfig[] = [
		{
			fn: slide,
			props: {
				duration: 500,
				easing: quintOut,
				x: isSlideRight ? 100 : -100
			}
		},
		{
			fn: scale,
			props: {
				duration: 500,
				easing: elasticOut,
				start: 0.8,
				opacity: 0.2
			}
		},
		{
			fn: fly,
			props: {
				duration: 600,
				x: isSlideRight ? 100 : -100,
				y: isSlideRight ? -50 : 50,
				opacity: 0.2
			}
		},
		{
			fn: fade,
			props: {
				duration: 400,
				delay: 100
			}
		},
		{
			fn: slide,
			props: {
				duration: 500,
				easing: quintOut,
				y: isSlideRight ? 100 : -100
			}
		}
	];

	return transitions[tabIndex % transitions.length];
}
