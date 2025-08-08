<script lang="ts">
	import type { PropDebugInfo } from '../../types/debug.js';

	// Props
	let {
		propData = null
	}: {
		propData?: PropDebugInfo | null;
	} = $props();

	function formatAngle(angle: number): string {
		return `${((angle * 180) / Math.PI).toFixed(1)}°`;
	}
</script>

<div class="interpretation-section">
	<h4>🔍 Interpretation Analysis</h4>
	<div class="interpretation-grid">
		<div class="interpretation-item">
			<span class="label">Calculation Method:</span>
			<span class="value">{propData?.interpretation.calculationMethod}</span>
		</div>

		<div class="interpretation-item">
			<span class="label">Start Orientation Angle:</span>
			<span class="value">{formatAngle(propData?.interpretation.startOriAngle || 0)}</span>
		</div>

		<div class="interpretation-item">
			<span class="label">End Orientation Angle:</span>
			<span class="value">{formatAngle(propData?.interpretation.endOriAngle || 0)}</span>
		</div>

		<div class="interpretation-item">
			<span class="label">Total Rotation:</span>
			<span class="value">{formatAngle(propData?.interpretation.totalRotation || 0)}</span>
		</div>

		<div class="interpretation-item">
			<span class="label">Is Float:</span>
			<span class="value">{propData?.interpretation.isFloat ? 'Yes' : 'No'}</span>
		</div>

		<div class="interpretation-item">
			<span class="label">Staff Rotation Angle:</span>
			<span class="value">{formatAngle(propData?.staffRotationAngle || 0)}</span>
		</div>
	</div>
</div>

<style>
	.interpretation-section {
		background: var(--color-surface-elevated);
		border-radius: 8px;
		padding: 1rem;
		border: 1px solid var(--color-border);
	}

	.interpretation-section h4 {
		margin: 0 0 1rem 0;
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.interpretation-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 0.75rem;
	}

	.interpretation-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.5rem;
		background: var(--color-surface);
		border-radius: 4px;
		border: 1px solid var(--color-border);
		font-size: 0.875rem;
	}

	.interpretation-item .label {
		color: var(--color-text-secondary);
		font-weight: 500;
	}

	.interpretation-item .value {
		color: var(--color-text);
		font-weight: 600;
		font-family: monospace;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.interpretation-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
