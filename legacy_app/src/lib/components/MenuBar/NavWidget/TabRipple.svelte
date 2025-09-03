<!-- src/lib/components/MenuBar/NavWidget/TabRipple.svelte -->
<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';

	export let active = false;
	export let index = 0;
	export let previousIndex = 0;

	let rippleElement: HTMLDivElement;
	let isAnimating = false;

	$: direction = index > previousIndex ? 'right' : 'left';

	onMount(() => {
		if (active && rippleElement) {
			startRipple();
		}
	});

	$: if (active && rippleElement && !isAnimating) {
		startRipple();
	}

	function startRipple() {
		isAnimating = true;

		// Reset any existing animations
		rippleElement.style.animation = 'none';

		// Force reflow to ensure animation reset
		void rippleElement.offsetWidth;

		// Set animation based on direction
		rippleElement.style.animation = `ripple-${direction} 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards`;

		// Add event listener for animation end
		rippleElement.addEventListener('animationend', handleAnimationEnd, { once: true });
	}

	function handleAnimationEnd() {
		isAnimating = false;
	}
</script>

<div class="tab-ripple-container" class:active>
	<div class="tab-ripple" bind:this={rippleElement}></div>
</div>

<style>
	.tab-ripple-container {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		pointer-events: none;
		overflow: hidden;
		z-index: 0;
	}

	.tab-ripple {
		position: absolute;
		background: radial-gradient(
			circle,
			rgba(108, 156, 233, 0.7) 0%,
			rgba(30, 60, 114, 0.3) 70%,
			transparent 100%
		);
		border-radius: 50%;
		transform: scale(0);
		top: 50%;
		left: 50%;
		width: 150%;
		height: 150%;
		transform-origin: center;
	}

	@keyframes ripple-right {
		0% {
			transform: scale(0) translate(0, -50%);
			opacity: 0.8;
		}
		100% {
			transform: scale(1) translate(0, -50%);
			opacity: 0;
		}
	}

	@keyframes ripple-left {
		0% {
			transform: scale(0) translate(0, -50%);
			opacity: 0.8;
		}
		100% {
			transform: scale(1) translate(0, -50%);
			opacity: 0;
		}
	}
</style>
