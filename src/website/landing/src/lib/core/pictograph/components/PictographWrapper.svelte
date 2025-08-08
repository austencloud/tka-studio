<!--
  PictographWrapper Component

  This component provides the wrapper element for the pictograph.
-->
<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import type { PictographData } from '$lib/constructor/types/PictographData.js';
	import PictographSVG from './PictographSVG.svelte';

	// Props
	export let pictographData: PictographData;
	export let state: any;
	export let debug = false;

	const dispatch = createEventDispatcher();

	function handleClick() {
		if (pictographData) {
			dispatch('click', { pictographData });
		}
	}

	function handleError(error: any) {
		dispatch('error', error);
	}

	function handleStateChange(status: string, reason?: string) {
		dispatch('stateChange', { status, reason });
	}
</script>

<div
	class="pictograph-wrapper"
	class:debug
	role="button"
	tabindex="0"
	on:click={handleClick}
	on:keydown={(e) => {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			handleClick();
		}
	}}
	aria-label={pictographData?.letter ? `Pictograph for letter ${pictographData.letter}` : 'Pictograph'}
	data-state={state?.status || 'unknown'}
	data-letter={pictographData?.letter || 'none'}
>
	{#if pictographData}
		<PictographSVG
			{pictographData}
			{debug}
			on:error={handleError}
			on:stateChange={(e) => handleStateChange(e.detail.status, e.detail.reason)}
		/>
	{/if}
</div>

<style>
	.pictograph-wrapper {
		width: 100%;
		height: 100%;
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		box-sizing: border-box;
		aspect-ratio: 1;
		cursor: pointer;
		border-radius: 8px;
		transition: transform 0.2s ease-in-out;
	}

	.pictograph-wrapper:hover {
		transform: scale(1.02);
	}

	.pictograph-wrapper:focus {
		outline: 2px solid #007acc;
		outline-offset: 2px;
	}

	.pictograph-wrapper.debug {
		border: 2px dashed #ff6b6b;
	}
</style>
