<!-- src/lib/components/ConstructTab/OptionPicker/components/OptionPickerHeader/ScrollIndicator.svelte -->
<script lang="ts">
	// Props
	const props = $props();
</script>

{#if props.show}
	<div class="scroll-indicator"></div>
{/if}

<style>
	/* Scroll indicator */
	.scroll-indicator {
		position: absolute;
		right: 0;
		top: 0;
		bottom: 0;
		width: 20px;
		background: linear-gradient(to right, transparent, rgba(15, 23, 42, 0.8) 40%);
		pointer-events: none; /* Allow clicks to pass through */
		z-index: 1;
	}
</style>
