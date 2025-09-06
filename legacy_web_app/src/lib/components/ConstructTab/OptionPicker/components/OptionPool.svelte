<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import type { PictographData } from '$lib/types/PictographData';
	import Option from './Option.svelte';
	import { prefersReducedMotion } from '../utils/a11y';

	// Props using Svelte 5 runes
	const props = $props<{
		options: PictographData[];
		poolSize?: number;
		transitionDuration?: number;
		isPartOfTwoItems?: boolean;
		key?: string;
	}>();

	// Default values for optional props
	const poolSize = $derived(props.poolSize ?? 30); // Default pool size
	const transitionDuration = $derived(props.transitionDuration ?? 300);
	const isPartOfTwoItems = $derived(props.isPartOfTwoItems ?? false);
	const key = $derived(props.key ?? '');

	// State
	let pooledOptions = $state<
		Array<{ id: string; data: PictographData | null; visible: boolean; position: number }>
	>([]);
	let initialized = $state(false);
	let previousOptionsMap = $state<Map<string, { data: PictographData; position: number }>>(
		new Map()
	);
	let isTransitioning = $state(false);

	// Generate a unique ID for each option
	function getOptionId(option: PictographData, index: number): string {
		return `${option.letter || ''}-${option.startPos || ''}-${option.endPos || ''}-${index}-${key}`;
	}

	// Initialize the pool with empty options
	function initializePool() {
		const initialPool = [];
		for (let i = 0; i < poolSize; i++) {
			initialPool.push({
				id: `pool-item-${i}`,
				data: null,
				visible: false,
				position: -1
			});
		}
		pooledOptions = initialPool;
		initialized = true;
	}

	// Update the pool with new options
	function updatePool(newOptions: PictographData[]) {
		if (!initialized) {
			initializePool();
		}

		// Save current visible options for transition
		const currentOptionsMap = new Map();
		pooledOptions.forEach((item) => {
			if (item.visible && item.data) {
				currentOptionsMap.set(getOptionId(item.data, item.position), {
					data: item.data,
					position: item.position
				});
			}
		});

		// Start transition if we have previous options
		isTransitioning = pooledOptions.some((item) => item.visible);
		previousOptionsMap = currentOptionsMap;

		// Reset visibility for all options
		pooledOptions.forEach((item) => {
			item.visible = false;
		});

		// Update pool with new options
		newOptions.forEach((option, index) => {
			const optionId = getOptionId(option, index);

			// Find an existing pool item to reuse
			let poolItem = pooledOptions.find((item) => !item.visible);

			if (poolItem) {
				poolItem.id = optionId;
				poolItem.data = option;
				poolItem.visible = true;
				poolItem.position = index;
			} else {
				console.warn('Pool size exceeded, consider increasing poolSize');
			}
		});

		// After transition duration, clear the transition state
		if (isTransitioning) {
			setTimeout(
				() => {
					isTransitioning = false;
					previousOptionsMap = new Map();
				},
				$prefersReducedMotion ? 50 : transitionDuration
			);
		}
	}

	// Watch for changes in options and update the pool
	$effect(() => {
		if (props.options) {
			updatePool(props.options);
		}
	});

	// Initialize on mount
	onMount(() => {
		if (!initialized) {
			initializePool();
		}
		if (props.options.length > 0) {
			updatePool(props.options);
		}
	});

	// Calculate transition properties for an option
	function getTransitionProps(item: (typeof pooledOptions)[0]) {
		if (!isTransitioning || !item.data) return {};

		const optionId = getOptionId(item.data, item.position);
		const previousOption = previousOptionsMap.get(optionId);

		// If this option existed in the previous state, it's staying in place
		// If not, it's a new option that should fade in
		const isNewOption = !previousOption;

		return {
			duration: $prefersReducedMotion ? 50 : transitionDuration,
			delay: isNewOption ? 50 : 0,
			opacity: { from: isNewOption ? 0 : 1, to: 1 },
			transform: isNewOption
				? { from: 'scale(0.95)', to: 'scale(1)' }
				: { from: 'scale(1)', to: 'scale(1)' }
		};
	}
</script>

<div class="option-pool">
	{#each pooledOptions as item (item.id)}
		{#if item.visible && item.data}
			<div
				class="option-wrapper"
				style:opacity={isTransitioning ? getTransitionProps(item).opacity?.from : 1}
				style:transform={isTransitioning ? getTransitionProps(item).transform?.from : 'scale(1)'}
				style:transition={isTransitioning
					? `opacity ${getTransitionProps(item).duration}ms ease-out ${getTransitionProps(item).delay}ms,
					transform ${getTransitionProps(item).duration}ms ease-out ${getTransitionProps(item).delay}ms`
					: ''}
				data-position={item.position}
			>
				<Option pictographData={item.data} {isPartOfTwoItems} />
			</div>
		{/if}
	{/each}
</div>

<style>
	.option-pool {
		display: contents; /* This makes the container transparent to the grid layout */
	}

	.option-wrapper {
		width: var(--option-size, 100px);
		height: var(--option-size, 100px);
		aspect-ratio: 1 / 1;
		display: flex;
		justify-content: center;
		align-items: center;
		position: relative;
		z-index: 1;
		margin: 0px;
		transform-origin: center center;
		will-change: transform, opacity;
		backface-visibility: hidden;
	}

	.option-wrapper:hover {
		z-index: 10;
	}
</style>
