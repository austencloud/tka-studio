<script lang="ts">
	import { getContext } from 'svelte';
	import { fade } from 'svelte/transition';
	import { LAYOUT_CONTEXT_KEY, type LayoutContext } from '../layoutContext';
	import { uiState } from '../store'; // To get selectedTab, showAllActive etc.

	// Extend the uiState type to include the missing properties
	type ExtendedUIState = typeof $uiState & {
		showAllActive?: boolean;
		reversalFilter?: string;
	};

	// Cast uiState to extended type for the template
	$: extendedUiState = $uiState as ExtendedUIState;

	// Consume context
	const layoutContext = getContext<LayoutContext>(LAYOUT_CONTEXT_KEY);

	// Panel state
	let isDebugExpanded = false;

	// Panel toggle handler
	const toggleDebugPanel = () => (isDebugExpanded = !isDebugExpanded);

	// Derived values from context and store
	$: layout = $layoutContext.layoutConfig; // Get layout config from context
</script>

<div class="debug-container" data-testid="debug-panel">
	<div class="debug-bar">
		<span class="debug-info">
			Device: {$layoutContext.deviceType}
			{$layoutContext.isMobile ? '📱' : $layoutContext.isTablet ? '📟' : '💻'}
		</span>
		<span class="debug-info">
			{$layoutContext.isPortrait ? 'Portrait 📸' : 'Landscape 🌄'}
		</span>
		<span class="debug-info">
			Container: {$layoutContext.containerWidth}×{$layoutContext.containerHeight}px ({$layoutContext.containerAspect})
		</span>

		<div class="spacer"></div>

		<button
			class="debug-button toggle-button"
			on:click={toggleDebugPanel}
			aria-expanded={isDebugExpanded}
			aria-controls="debug-details"
		>
			{isDebugExpanded ? 'Hide Details ▲' : 'Show Details ▼'}
		</button>
	</div>

	{#if isDebugExpanded}
		<div id="debug-details" class="debug-details" transition:fade={{ duration: 200 }}>
			<section class="debug-section">
				<h4>UI State</h4>
				<div class="grid">
					<div>Show All:</div>
					<div>{extendedUiState.showAllActive ? 'Yes' : 'No (Default)'}</div>
					<div>Sort By:</div>
					<div>{$uiState.sortMethod}</div>
					<div>Reversal Filter:</div>
					<div>{extendedUiState.reversalFilter || 'None'}</div>
				</div>
			</section>

			<section class="debug-section">
				<h4>Calculated Layout</h4>
				<div class="grid">
					<div>Columns:</div>
					<div>{layout.gridColumns}</div>
					<div>Option Size:</div>
					<div>{layout.optionSize}</div>
					<div>Grid Gap:</div>
					<div>{layout.gridGap}</div>
					<div>Item Scale:</div>
					<div>{layout.scaleFactor.toFixed(2)}</div>
					<div>Grid Class:</div>
					<div>{layout.gridClass || 'N/A'}</div>
					<div>Aspect Class:</div>
					<div>{layout.aspectClass || 'N/A'}</div>
				</div>
			</section>
		</div>
	{/if}
</div>

<style>
	.debug-container {
		position: absolute;
		top: 10px;
		left: 10px;
		right: 10px;
		z-index: 1000;
		background-color: #f8fafcee;
		box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
		border-radius: 4px;
		border: 1px dashed #94a3b8;
		overflow: hidden;
		font-size: 11px; /* Slightly smaller */
		font-family: ui-monospace, monospace;
		max-width: calc(100% - 20px);
		color: #334155;
	}
	.debug-bar {
		display: flex;
		padding: 5px 8px; /* Adjust padding */
		background-color: #f1f5f9;
		gap: 8px; /* Adjust gap */
		flex-wrap: wrap;
		align-items: center;
	}

	.debug-info {
		background-color: #e0f2fe;
		color: #0c4a6e;
		border-radius: 3px;
		padding: 3px 6px;
		white-space: nowrap;
	}

	.debug-button {
		/* Keep for toggle */
		background-color: #2563eb;
		color: white;
		border: none;
		border-radius: 4px;
		padding: 4px 8px;
		font-size: 11px;
		cursor: pointer;
		transition: background-color 0.2s;
		white-space: nowrap;
	}

	.debug-button:hover {
		background-color: #1d4ed8;
	}

	.toggle-button {
		background-color: #0891b2;
	}

	.toggle-button:hover {
		background-color: #0e7490;
	}

	.spacer {
		flex-grow: 1;
		min-width: 10px; /* Ensure spacer takes space */
	}

	.debug-details {
		padding: 10px;
		max-height: 40vh;
		overflow-y: auto;
	}

	.debug-section {
		margin-bottom: 12px;
	}

	.debug-section h4 {
		margin: 0 0 6px 0;
		padding-bottom: 3px;
		border-bottom: 1px solid #e2e8f0;
		font-size: 12px;
		color: #334155;
		font-weight: 600;
	}

	.grid {
		display: grid;
		grid-template-columns: 110px 1fr; /* Adjust column width */
		gap: 4px 8px; /* Row and column gap */
		align-items: center;
	}

	.grid > div:nth-child(odd) {
		font-weight: 500; /* Slightly less bold */
		color: #475569;
		text-align: right; /* Align labels right */
		padding-right: 5px;
	}

	.grid > div:nth-child(even) {
		color: #0369a1;
		font-weight: 500;
	}

	@media (max-width: 700px) {
		/* Adjust breakpoint */
		.debug-bar {
			flex-direction: column;
			align-items: stretch;
		}
		.debug-info {
			margin-bottom: 4px;
			text-align: center;
		}
		.spacer {
			display: none;
		} /* Hide spacer on small screens */
		.toggle-button {
			margin-top: 4px;
		}
	}
	@media (max-width: 480px) {
		.debug-container {
			top: 5px;
			left: 5px;
			right: 5px;
			max-width: calc(100% - 10px);
			font-size: 10px;
		}
		.grid {
			grid-template-columns: 90px 1fr;
		}
	}
</style>
