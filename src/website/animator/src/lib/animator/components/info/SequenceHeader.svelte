<script lang="ts">
	// Props
	let {
		sequenceWord = '',
		sequenceAuthor = ''
	}: {
		sequenceWord?: string;
		sequenceAuthor?: string;
	} = $props();
</script>

{#if sequenceWord || sequenceAuthor}
	<div class="sequence-header">
		{#if sequenceWord}
			<h3 class="sequence-title">{sequenceWord}</h3>
		{/if}
		{#if sequenceAuthor}
			<p class="sequence-author">by {sequenceAuthor}</p>
		{/if}
	</div>
{/if}

<style>
	.sequence-header {
		text-align: center;
		padding-bottom: 1rem;
		border-bottom: 1px solid var(--color-border);
	}

	.sequence-title {
		margin: 0 0 0.5rem;
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--color-primary);
		letter-spacing: -0.025em;
	}

	.sequence-author {
		margin: 0;
		font-size: 0.95rem;
		color: var(--color-text-secondary);
		font-style: italic;
	}

	/* Mobile responsive adjustments */
	@media (max-width: 768px) {
		.sequence-title {
			font-size: 1.25rem;
		}

		.sequence-author {
			font-size: 0.8rem;
		}
	}

	@media (max-width: 480px) {
		.sequence-title {
			font-size: 1.1rem;
		}
	}
</style>
