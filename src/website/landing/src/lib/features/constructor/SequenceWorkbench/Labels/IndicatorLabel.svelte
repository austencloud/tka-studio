<script lang="ts">
	import { onDestroy } from 'svelte';
	import { fade } from 'svelte/transition';

	export let text = ''; // Default to empty string
	export let width = 100; // Default width in pixels
	const minFontSize = 18; // Minimum font size in pixels

	// State variables
	let visible = false;
	let message = '';
	let timeoutId: number | null = null;

	$: fontSize = `${Math.max(width / 80, minFontSize)}px`; // Adjust the multiplier as needed

	// Watch for changes to the text prop
	$: if (text && text !== message) {
		showMessage(text);
	}

	// Function to show a message temporarily
	function showMessage(newMessage: string): void {
		// Clear any existing timeout
		if (timeoutId !== null) {
			clearTimeout(timeoutId);
		}

		// Update message and make visible
		message = newMessage;
		visible = true;

		// Set timeout to hide after 4 seconds
		timeoutId = window.setTimeout(() => {
			visible = false;
		}, 4000);
	}

	// Clean up on component destroy
	onDestroy(() => {
		if (timeoutId !== null) {
			clearTimeout(timeoutId);
		}
	});
</script>

{#if visible}
	<div class="indicator-label" style="font-size: {fontSize};" transition:fade={{ duration: 300 }}>
		{message}
	</div>
{:else}
	<div class="indicator-label-placeholder"></div>
{/if}

<style>
	.indicator-label {
		text-align: center;
		font-weight: bold;
		padding: 5px;
		transition: opacity 0.5s ease-out;
	}

	.indicator-label-placeholder {
		height: 30px; /* Maintain consistent height when empty */
	}
</style>
