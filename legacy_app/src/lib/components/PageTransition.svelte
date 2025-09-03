<!-- src/lib/components/PageTransition.svelte -->
<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { cubicInOut } from 'svelte/easing';

	export let active = false;
	export let direction = 'right'; // 'right' or 'left'

	let pageTransition: HTMLDivElement;
	let isAnimating = false;

	const dispatch = createEventDispatcher();

	onMount(() => {
		if (active && pageTransition) {
			startTransition();
		}
	});

	$: if (active && pageTransition && !isAnimating) {
		startTransition();
	}

	function startTransition() {
		isAnimating = true;

		// Reset any existing animations
		pageTransition.style.animation = 'none';

		// Force reflow
		void pageTransition.offsetWidth;

		// Start animation
		pageTransition.style.animation = `page-transition-${direction} 0.8s ${cubicInOut} forwards`;
		pageTransition.addEventListener('animationend', handleAnimationEnd, { once: true });

		// Dispatch animation start event
		dispatch('transitionstart');
	}

	function handleAnimationEnd() {
		isAnimating = false;
		dispatch('transitionend');
	}
</script>

<div class="page-transition" bind:this={pageTransition}></div>

<style>
	.page-transition {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: linear-gradient(135deg, #1e3c72 0%, #6c9ce9 100%);
		z-index: 100;
		pointer-events: none;
		transform: translateX(-100%);
	}

	@keyframes page-transition-right {
		0% {
			transform: translateX(-100%);
			opacity: 0.7;
		}
		100% {
			transform: translateX(100%);
			opacity: 0;
		}
	}

	@keyframes page-transition-left {
		0% {
			transform: translateX(100%);
			opacity: 0.7;
		}
		100% {
			transform: translateX(-100%);
			opacity: 0;
		}
	}
</style>
