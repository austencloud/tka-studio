<!-- src/lib/components/Pictograph/components/LoadingProgress.svelte -->
<script lang="ts">
	export let loadProgress = 0;
	export let showText = true;
</script>

<div class="loading-bar-container">
	<div class="loading-bar" style="width: {loadProgress}%"></div>
	{#if showText}
		<span class="loading-text">{loadProgress}%</span>
	{/if}
</div>

<style>
	.loading-bar-container {
		position: absolute;
		bottom: 10px;
		left: 10px;
		right: 10px;
		height: 4px;
		background-color: #edf2f7;
		border-radius: 2px;
		overflow: hidden;
		z-index: 5;
	}

	.loading-bar {
		height: 100%;
		background-color: #4299e1;
		transition: width 0.3s ease-out;
	}

	.loading-text {
		position: absolute;
		right: 0;
		top: -18px;
		font-size: 12px;
		color: #718096;
	}
</style>
