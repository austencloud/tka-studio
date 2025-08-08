<script lang="ts">
	import type { PropDebugInfo } from '../../types/debug.js';

	// Props
	let {
		propData = null
	}: {
		propData?: PropDebugInfo | null;
	} = $props();

	function getValidationIcon(isValid: boolean): string {
		return isValid ? '✅' : '❌';
	}

	function getValidationClass(isValid: boolean): string {
		return isValid ? 'valid' : 'invalid';
	}
</script>

<div class="validation-section">
	<h4>✅ Validation Results</h4>
	<div class="validation-grid">
		<div class="validation-item {getValidationClass(propData?.validation.isValid || false)}">
			<span class="validation-icon">{getValidationIcon(propData?.validation.isValid || false)}</span
			>
			<span class="validation-label">Overall Valid</span>
		</div>

		<div
			class="validation-item {getValidationClass(
				propData?.validation.orientationContinuity.isValid || false
			)}"
		>
			<span class="validation-icon"
				>{getValidationIcon(propData?.validation.orientationContinuity.isValid || false)}</span
			>
			<span class="validation-label">Orientation Continuity</span>
		</div>

		<div
			class="validation-item {getValidationClass(
				propData?.validation.turnCountAccuracy.isValid || false
			)}"
		>
			<span class="validation-icon"
				>{getValidationIcon(propData?.validation.turnCountAccuracy.isValid || false)}</span
			>
			<span class="validation-label">Turn Count Accuracy</span>
		</div>
	</div>

	{#if propData?.validation?.warnings && propData.validation.warnings.length > 0}
		<div class="validation-messages warnings">
			<h5>⚠️ Warnings:</h5>
			<ul>
				{#each propData.validation.warnings as warning}
					<li>{warning}</li>
				{/each}
			</ul>
		</div>
	{/if}

	{#if propData?.validation?.errors && propData.validation.errors.length > 0}
		<div class="validation-messages errors">
			<h5>❌ Errors:</h5>
			<ul>
				{#each propData.validation.errors as error}
					<li>{error}</li>
				{/each}
			</ul>
		</div>
	{/if}
</div>

<style>
	.validation-section {
		background: var(--color-surface-elevated);
		border-radius: 8px;
		padding: 1rem;
		border: 1px solid var(--color-border);
	}

	.validation-section h4 {
		margin: 0 0 1rem 0;
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.validation-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 0.75rem;
	}

	.validation-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.5rem;
		background: var(--color-surface);
		border-radius: 4px;
		border: 1px solid var(--color-border);
		font-size: 0.875rem;
	}

	.validation-item.valid {
		border-color: #10b981;
		background: rgba(16, 185, 129, 0.1);
	}

	.validation-item.invalid {
		border-color: #ef4444;
		background: rgba(239, 68, 68, 0.1);
	}

	.validation-messages {
		margin-top: 1rem;
		padding: 1rem;
		border-radius: 6px;
		border: 1px solid var(--color-border);
	}

	.validation-messages.warnings {
		background: rgba(245, 158, 11, 0.1);
		border-color: #f59e0b;
	}

	.validation-messages.errors {
		background: rgba(239, 68, 68, 0.1);
		border-color: #ef4444;
	}

	.validation-messages h5 {
		margin: 0 0 0.5rem 0;
		font-size: 0.875rem;
		font-weight: 600;
	}

	.validation-messages ul {
		margin: 0;
		padding-left: 1.5rem;
		font-size: 0.875rem;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.validation-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
