<script lang="ts">
	import PanelLeftClose from 'lucide-svelte/icons/panel-left-close';
	import PanelLeftOpen from 'lucide-svelte/icons/panel-left-open';
	import SplitSquareHorizontal from 'lucide-svelte/icons/split-square-horizontal';

	// Props
	let {
		onSetSidebar50,
		onSetSidebar75,
		onSetSidebar25
	}: {
		onSetSidebar50?: () => void;
		onSetSidebar75?: () => void;
		onSetSidebar25?: () => void;
	} = $props();

	function handleSet50(): void {
		onSetSidebar50?.();
	}

	function handleSet75(): void {
		onSetSidebar75?.();
	}

	function handleSet25(): void {
		onSetSidebar25?.();
	}
</script>

<div class="sidebar-controls">
	<span class="controls-label">Quick Layout:</span>
	<div class="controls-buttons">
		<button
			type="button"
			class="control-button"
			onclick={handleSet75}
			title="Set sidebar to 75% width"
			aria-label="Set sidebar to 75% width"
		>
			<PanelLeftOpen size={16} />
			75%
		</button>
		<button
			type="button"
			class="control-button"
			onclick={handleSet50}
			title="Set sidebar to 50% width"
			aria-label="Set sidebar to 50% width"
		>
			<SplitSquareHorizontal size={16} />
			50%
		</button>
		<button
			type="button"
			class="control-button"
			onclick={handleSet25}
			title="Set sidebar to 25% width"
			aria-label="Set sidebar to 25% width"
		>
			<PanelLeftClose size={16} />
			25%
		</button>
	</div>
</div>

<style>
	.sidebar-controls {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.5rem 0;
		border-top: 1px solid var(--color-border);
		background: var(--color-surface);
		flex-shrink: 0;
	}

	.controls-label {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		font-weight: 500;
		white-space: nowrap;
	}

	.controls-buttons {
		display: flex;
		gap: 0.25rem;
	}

	.control-button {
		background: var(--color-background);
		border: 1px solid var(--color-border);
		color: var(--color-text-primary);
		padding: 0.375rem 0.5rem;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.75rem;
		font-weight: 500;
		transition: all 0.2s ease;
		display: flex;
		align-items: center;
		gap: 0.25rem;
		min-width: fit-content;
	}

	.control-button:hover {
		background: var(--color-primary);
		border-color: var(--color-primary);
		color: white;
		transform: translateY(-1px);
		box-shadow: 0 2px 4px rgba(var(--color-primary-rgb), 0.2);
	}

	.control-button:active {
		transform: translateY(0);
		box-shadow: 0 1px 2px rgba(var(--color-primary-rgb), 0.2);
	}

	/* Mobile responsive */
	@media (max-width: 1024px) {
		.sidebar-controls {
			display: none;
		}
	}
</style>
