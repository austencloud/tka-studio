<!-- src/lib/components/GenerateTab/layout/WorkbenchPanel.svelte -->
<script lang="ts">
	import SequenceWidget from '$lib/components/SequenceWorkbench/SequenceWidget.svelte';
</script>

<div class="workbench-panel">
	<SequenceWidget />
</div>

<style>
	.workbench-panel {
		display: flex;
		flex-direction: column;
		background: var(--color-surface-800, rgba(20, 30, 50, 0.5));
		border-radius: 0.75rem;
		box-shadow:
			0 4px 12px rgba(0, 0, 0, 0.2),
			0 0 0 1px rgba(255, 255, 255, 0.05);
		overflow: hidden;
		transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		flex: 1;
		min-width: 0;
		animation: fadeIn 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
		animation-delay: 0.1s;
	}

	.workbench-panel:hover {
		box-shadow:
			0 8px 24px rgba(0, 0, 0, 0.3),
			0 0 0 1px rgba(255, 255, 255, 0.1);
		transform: translateY(-2px);
	}

	/* Animation for panel transitions */
	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(20px);
			filter: blur(5px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
			filter: blur(0);
		}
	}

	/* Responsive adjustments */
	@media (max-width: 1024px) {
		.workbench-panel {
			transition:
				transform 0.3s ease,
				box-shadow 0.3s ease;
		}

		.workbench-panel:hover {
			transform: translateY(-4px);
		}
	}
</style>
