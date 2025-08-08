<script lang="ts">
	// Props
	let {
		scrollProgress = 0,
		showIndicator = false
	}: {
		scrollProgress?: number;
		showIndicator?: boolean;
	} = $props();
</script>

{#if showIndicator}
	<!-- Scroll progress indicator -->
	<div class="scroll-indicator">
		<div class="scroll-progress" style:width="{scrollProgress * 100}%"></div>
	</div>
{/if}

{#if showIndicator && scrollProgress < 0.95}
	<!-- Bottom fade indicator -->
	<div class="scroll-fade"></div>
{/if}

<style>
	/* Scroll indicators */
	.scroll-indicator {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 3px;
		background: var(--color-surface);
		z-index: 10;
		border-radius: 0 0 2px 2px;
	}

	.scroll-progress {
		height: 100%;
		background: var(--color-primary);
		border-radius: 0 0 2px 2px;
		transition: width 0.1s ease;
	}

	.scroll-fade {
		position: absolute;
		bottom: 0;
		left: 0;
		right: 0;
		height: 20px;
		background: linear-gradient(transparent, var(--color-background));
		pointer-events: none;
		z-index: 5;
		border-radius: 0 0 8px 8px;
	}
</style>
