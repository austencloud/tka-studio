<!-- Real Pictograph component from v1-legacy -->
<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import type { PictographData } from '$lib/constructor/types/PictographData.js';
	import PictographWrapper from './components/PictographWrapper.svelte';
	import PictographLoading from './components/PictographLoading.svelte';
	import PictographError from './components/PictographError.svelte';
	import { PictographLifecycle } from './managers/PictographLifecycle.js';
	import { PictographStateManager } from './managers/PictographStateManager.js';
	import { PictographLoadingManager } from './managers/PictographLoadingManager.js';
	import { PictographErrorHandler } from './handlers/PictographErrorHandler.js';
	import { PictographEventHandler } from './handlers/PictographEventHandler.js';
	import { createPictographState } from './pictographState.js';
	import { browser } from '$app/environment';

	// Props
	export let pictographData: PictographData;
	export let showLoadingIndicator = true;
	export let debug = false;
	export let size: number | undefined = undefined;
	export let width: number | undefined = undefined;
	export let height: number | undefined = undefined;

	// State management
	let state = createPictographState();
	let stateManager: PictographStateManager;
	let loadingManager: PictographLoadingManager;
	let errorHandler: PictographErrorHandler;
	let eventHandler: PictographEventHandler;
	let lifecycle: PictographLifecycle;

	// Component references
	let containerElement: HTMLElement;
	let wrapperComponent: PictographWrapper;

	// Reactive state
	$: isLoading = state.status === 'initializing' || state.status === 'grid_loading' ||
	               state.status === 'props_loading' || state.status === 'arrows_loading';
	$: hasError = state.status === 'error';
	$: isComplete = state.status === 'complete';

	// Initialize managers
	function initializeManagers() {
		if (!browser) return;

		stateManager = new PictographStateManager(state);
		loadingManager = new PictographLoadingManager(state, stateManager);
		errorHandler = new PictographErrorHandler(state, stateManager);
		eventHandler = new PictographEventHandler(state, stateManager);
		lifecycle = new PictographLifecycle(
			state,
			stateManager,
			loadingManager,
			errorHandler,
			eventHandler
		);
	}

	// Handle pictograph data changes
	$: if (pictographData && lifecycle) {
		lifecycle.updatePictographData(pictographData);
	}

	onMount(() => {
		if (browser) {
			initializeManagers();
			if (pictographData) {
				lifecycle.initialize(pictographData);
			}
		}
	});

	onDestroy(() => {
		if (lifecycle) {
			lifecycle.cleanup();
		}
	});

	// Expose methods for parent components
	export function refresh() {
		if (lifecycle && pictographData) {
			lifecycle.refresh(pictographData);
		}
	}

	export function getState() {
		return state;
	}
</script>

<div
	bind:this={containerElement}
	class="pictograph-container"
	class:loading={isLoading}
	class:error={hasError}
	class:complete={isComplete}
	style:width={width ? `${width}px` : size ? `${size}px` : '100%'}
	style:height={height ? `${height}px` : size ? `${size}px` : '100%'}
>
	{#if hasError}
		<PictographError
			error={state.error}
			on:retry={() => refresh()}
			{debug}
		/>
	{:else if isLoading && showLoadingIndicator}
		<PictographLoading
			status={state.status}
			progress={state.loadProgress}
			{debug}
		/>
	{:else if isComplete || !showLoadingIndicator}
		<PictographWrapper
			bind:this={wrapperComponent}
			{pictographData}
			{state}
			{debug}
			on:error={(e) => errorHandler?.handleError(e.detail)}
			on:stateChange={(e) => stateManager?.updateState(e.detail.status, e.detail.reason)}
		/>
	{/if}
</div>

<style>
	.pictograph-container {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
		min-width: 50px;
		min-height: 50px;
	}

	.pictograph-container.loading {
		background: rgba(0, 0, 0, 0.02);
	}

	.pictograph-container.error {
		background: rgba(255, 0, 0, 0.05);
	}

	.pictograph-container.complete {
		background: transparent;
	}
</style>
