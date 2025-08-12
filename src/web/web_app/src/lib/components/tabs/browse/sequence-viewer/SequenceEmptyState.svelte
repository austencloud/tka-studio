<!-- SequenceEmptyState.svelte - Empty state when no sequence is selected -->
<script lang="ts">
	import { fade } from 'svelte/transition';
</script>

<div class="empty-viewer" transition:fade>
	<div class="empty-content">
		<div class="empty-icon">👁️</div>
		<h3>Select a Sequence</h3>
		<p>Choose a sequence from the browser to view its details and pictograph.</p>
	</div>
</div>

<style>
	/* Empty State */
	.empty-viewer {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100%;
		padding: var(--spacing-xl);
	}

	.empty-content {
		text-align: center;
		max-width: 300px;
	}

	.empty-icon {
		font-size: 3rem;
		margin-bottom: var(--spacing-lg);
		opacity: 0.6;
	}

	.empty-content h3 {
		font-size: var(--font-size-xl);
		color: var(--foreground);
		margin: 0 0 var(--spacing-md) 0;
		font-weight: 600;
	}

	.empty-content p {
		color: var(--muted-foreground);
		line-height: 1.5;
		margin: 0;
	}
</style>
