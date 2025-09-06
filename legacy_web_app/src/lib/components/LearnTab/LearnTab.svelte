<script lang="ts">
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';
	import { learnStore } from '$lib/state/stores/learn/learnStore';
	import LessonSelector from './LessonSelector.svelte';
	import LessonWidget from './LessonWidget.svelte';
	import LessonResults from './LessonResults.svelte';

	// Track whether this is the first render
	let isFirstRender = true;

	// Track the current view for transition effects
	let currentView = $learnStore.currentView;
	let previousView: string | null = null;

	// Handle view transitions
	$: if ($learnStore.currentView !== currentView) {
		previousView = currentView;
		currentView = $learnStore.currentView;
	}

	// After initial mount, set first render to false
	onMount(() => {
		setTimeout(() => {
			isFirstRender = false;
		}, 100);
	});

	// Determine transition direction
	$: transitionDirection = getTransitionDirection(previousView, currentView);

	function getTransitionDirection(from: string | null, to: string): 'forward' | 'backward' {
		if (!from) return 'forward';

		const viewOrder = ['selector', 'lesson', 'results'];
		const fromIndex = viewOrder.indexOf(from);
		const toIndex = viewOrder.indexOf(to);

		return toIndex > fromIndex ? 'forward' : 'backward';
	}
</script>

<div class="learn-tab">
	<div class="learn-tab-background"></div>

	<div class="learn-tab-content">
		{#if currentView === 'selector'}
			<div
				class="view-container"
				in:fly={{
					x: transitionDirection === 'backward' ? -300 : 300,
					duration: isFirstRender ? 0 : 400,
					easing: cubicOut
				}}
				out:fly={{
					x: transitionDirection === 'backward' ? 300 : -300,
					duration: 400,
					easing: cubicOut
				}}
			>
				<LessonSelector />
			</div>
		{:else if currentView === 'lesson'}
			<div
				class="view-container"
				in:fly={{
					x: transitionDirection === 'backward' ? -300 : 300,
					duration: isFirstRender ? 0 : 400,
					easing: cubicOut
				}}
				out:fly={{
					x: transitionDirection === 'backward' ? 300 : -300,
					duration: 400,
					easing: cubicOut
				}}
			>
				<LessonWidget />
			</div>
		{:else if currentView === 'results'}
			<div
				class="view-container"
				in:fly={{
					x: transitionDirection === 'backward' ? -300 : 300,
					duration: isFirstRender ? 0 : 400,
					easing: cubicOut
				}}
				out:fly={{
					x: transitionDirection === 'backward' ? 300 : -300,
					duration: 400,
					easing: cubicOut
				}}
			>
				<LessonResults />
			</div>
		{/if}
	</div>
</div>

<style>
	.learn-tab {
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		position: relative;
		overflow: hidden;
		/* Removed background-color to allow user's background to show through */
	}

	.learn-tab-background {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-image:
			radial-gradient(circle at 20% 30%, rgba(41, 98, 255, 0.03) 0%, transparent 50%),
			radial-gradient(circle at 80% 70%, rgba(41, 98, 255, 0.03) 0%, transparent 50%);
		z-index: 0;
		pointer-events: none;
		/* Add a subtle overlay to ensure content is readable regardless of background */
		background-color: rgba(0, 0, 0, 0.1);
	}

	.learn-tab-content {
		position: relative;
		z-index: 1;
		flex: 1;
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		overflow: hidden;
	}

	.view-container {
		flex: 1;
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		overflow-y: auto;
		scrollbar-width: thin;
		scrollbar-color: var(--color-accent, #3a7bd5) transparent;
	}

	.view-container::-webkit-scrollbar {
		width: 6px;
	}

	.view-container::-webkit-scrollbar-track {
		background: transparent;
	}

	.view-container::-webkit-scrollbar-thumb {
		background-color: var(--color-accent, #3a7bd5);
		border-radius: 3px;
	}

	/* Add a subtle animation to the background */
	@keyframes backgroundShift {
		0% {
			background-position: 0% 0%;
		}
		50% {
			background-position: 100% 100%;
		}
		100% {
			background-position: 0% 0%;
		}
	}

	.learn-tab-background {
		background-size: 200% 200%;
		animation: backgroundShift 30s ease infinite;
	}
</style>
