<script lang="ts">
	// Props
	let {
		originalAttributes = null,
		modifiedAttributes = null,
		isVisible = false
	}: {
		originalAttributes?: any;
		modifiedAttributes?: any;
		isVisible?: boolean;
	} = $props();
</script>

{#if isVisible && originalAttributes}
	<div class="comparison-section">
		<h4>🔍 Original vs Modified</h4>
		<div class="comparison-grid">
			{#each Object.keys(originalAttributes) as key}
				{#if originalAttributes[key] !== modifiedAttributes[key]}
					<div class="comparison-item changed">
						<div class="comparison-label">{key}:</div>
						<div class="comparison-values">
							<span class="original-value">{originalAttributes[key] || 'None'}</span>
							<span class="arrow">→</span>
							<span class="modified-value">{modifiedAttributes[key] || 'None'}</span>
						</div>
					</div>
				{/if}
			{/each}
		</div>
	</div>
{/if}

<style>
	.comparison-section {
		background: var(--color-surface-elevated);
		border-radius: 8px;
		padding: 1rem;
		border: 1px solid var(--color-border);
	}

	.comparison-section h4 {
		margin: 0 0 1rem 0;
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.comparison-grid {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.comparison-item {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 0.5rem;
		background: var(--color-surface);
		border-radius: 4px;
		border: 1px solid var(--color-border);
		font-size: 0.875rem;
	}

	.comparison-item.changed {
		border-color: #f59e0b;
		background: rgba(245, 158, 11, 0.1);
	}

	.comparison-label {
		font-weight: 600;
		color: var(--color-text);
		min-width: 120px;
	}

	.comparison-values {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.original-value {
		color: #ef4444;
		font-weight: 600;
		font-family: monospace;
	}

	.arrow {
		color: var(--color-text-secondary);
	}

	.modified-value {
		color: #10b981;
		font-weight: 600;
		font-family: monospace;
	}
</style>
