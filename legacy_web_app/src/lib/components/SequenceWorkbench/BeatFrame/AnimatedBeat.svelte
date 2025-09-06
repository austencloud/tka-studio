<script lang="ts">
	import { onMount } from 'svelte';
	import Beat from './Beat.svelte';
	import SelectionBorderOverlay from './SelectionBorderOverlay.svelte';
	import type { BeatData } from './BeatData';

	const props = $props<{
		beat: BeatData;
		onClick: () => void;
		isSelected?: boolean;
		animationDelay?: number;
	}>();

	const isSelected = $derived(props.isSelected ?? false);

	let shouldAnimate = $state(true);
	let hasAnimated = $state(false);
	let isVisible = $state(false);

	// Start animation immediately on mount
	onMount(() => {
		// Use requestAnimationFrame for smoother animation start
		requestAnimationFrame(() => {
			isVisible = true;
		});
	});

	function handleAnimationEnd() {
		if (!hasAnimated && shouldAnimate) {
			hasAnimated = true;
		}
	}
</script>

<div
	class="animated-beat-container"
	class:animate={shouldAnimate && !hasAnimated && isVisible}
	class:visible={isVisible}
	onanimationend={handleAnimationEnd}
>
	<Beat beat={props.beat} onClick={props.onClick} />

	{#if isSelected}
		<SelectionBorderOverlay pictographData={props.beat.pictographData} {isSelected} />
	{/if}
</div>

<style>
	.animated-beat-container {
		width: 100%;
		height: 100%;
		position: relative;
		transform: scale(0.8);
		transition: transform 0.2s ease;
		/* Ensure proper aspect ratio */
		aspect-ratio: 1 / 1;
		/* Prevent any layout shifts during animation */
		will-change: transform;
	}

	.visible {
		transform: scale(1);
	}

	.animate {
		/* Faster animation for more responsive feel */
		animation: scaleIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
	}

	@keyframes scaleIn {
		0% {
			transform: scale(0.6);
			opacity: 0.7;
		}
		50% {
			transform: scale(1.05);
			opacity: 1;
		}
		100% {
			transform: scale(1);
			opacity: 1;
		}
	}

	/* Selection indicator replaced with SelectionBorderOverlay component */
</style>
