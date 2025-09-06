<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { fade } from 'svelte/transition';
	import type { PictographData } from '$lib/types/PictographData';
	import { prefersReducedMotion } from '../utils/a11y';

	// Props
	export let options: PictographData[] = [];
	export let selectedTab: string | null = null;

	// Track if this is the initial render
	let initialRender = true;

	// Create a unique key that only changes when options meaningfully change
	let transitionKey = '';

	// Update key when options change meaningfully
	$: {
		if (!initialRender) {
			// Generate a simple signature for the options
			const newKey = options.length + '-' +
			      (options[0]?.letter || '') +
			      (options[0]?.startPos || '') +
			      (options[0]?.endPos || '');

			// Only update the key if it's different
			if (newKey !== transitionKey) {
				transitionKey = newKey;
			}
		}
	}

	onMount(() => {
		// After initial render, mark it as complete
		initialRender = false;

		// Set an initial key
		transitionKey = options.length + '-' +
			(options[0]?.letter || '') +
			(options[0]?.startPos || '') +
			(options[0]?.endPos || '');
	});
</script>

{#key transitionKey}
	<div
		class="options-container"
		in:fade={{ duration: initialRender ? 0 : ($prefersReducedMotion ? 50 : 200) }}
	>
		<slot {options} {selectedTab} />
	</div>
{/key}

<style>
	.options-container {
		width: 100%;
		height: 100%;
	}
</style>
