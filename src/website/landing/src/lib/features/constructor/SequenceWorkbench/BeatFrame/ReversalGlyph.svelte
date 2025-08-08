<script lang="ts">
	// Props using Svelte 5 runes
	const { blueReversal = false, redReversal = false } = $props<{
		blueReversal?: boolean;
		redReversal?: boolean;
	}>();

	const blueStyle = 'background-color: blue; border-radius: 50%; width: 20px; height: 20px;';
	const redStyle = 'background-color: red; border-radius: 50%; width: 20px; height: 20px;';
</script>

<div class="reversal-glyphs">
	{#if blueReversal}
		<div class="reversal" style={blueStyle} title="Blue Reversal"></div>
	{/if}
	{#if redReversal}
		<div class="reversal" style={redStyle} title="Red Reversal"></div>
	{/if}
</div>

<style>
	.reversal-glyphs {
		display: flex;
		justify-content: center;
		gap: 5px;
	}
</style>
