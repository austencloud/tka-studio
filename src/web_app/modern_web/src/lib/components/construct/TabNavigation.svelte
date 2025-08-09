<!--
	TabNavigation.svelte

	Tab navigation component extracted from ConstructTab.
	Handles the 4-tab navigation (Build/Generate/Edit/Export) with active state management.
-->
<script lang="ts">
	import { constructTabState, type ActiveRightPanel } from '$stores/constructTabState.svelte';
	import { constructTabTransitionService } from '$services/implementations/ConstructTabTransitionService';

	// Reactive state from store
	let activeRightPanel = $derived(constructTabState.activeRightPanel);

	async function handleTabClick(targetTab: ActiveRightPanel) {
		await constructTabTransitionService.handleMainTabTransition(targetTab);
	}
</script>

<div class="main-tab-navigation" data-testid="tab-navigation">
	<button
		type="button"
		class="main-tab-btn"
		class:active={activeRightPanel === 'build'}
		onclick={() => handleTabClick('build')}
	>
		🔨 Build
	</button>
	<button
		type="button"
		class="main-tab-btn"
		class:active={activeRightPanel === 'generate'}
		onclick={() => handleTabClick('generate')}
	>
		🤖 Generate
	</button>
	<button
		type="button"
		class="main-tab-btn"
		class:active={activeRightPanel === 'edit'}
		onclick={() => handleTabClick('edit')}
	>
		🔧 Edit
	</button>
	<button
		type="button"
		class="main-tab-btn"
		class:active={activeRightPanel === 'export'}
		onclick={() => handleTabClick('export')}
	>
		🔤 Export
	</button>
</div>

<style>
	.main-tab-navigation {
		flex-shrink: 0;
		display: flex;
		background: var(--muted) / 20;
		border-bottom: 1px solid var(--border);
	}

	.main-tab-btn {
		flex: 1;
		padding: var(--spacing-md);
		border: none;
		background: transparent;
		color: var(--muted-foreground);
		cursor: pointer;
		transition: all 0.2s ease;
		font-size: var(--font-size-sm);
		font-weight: 600;
		border-bottom: 3px solid transparent;
	}

	.main-tab-btn:hover {
		background: var(--muted) / 30;
		color: var(--foreground);
	}

	.main-tab-btn.active {
		background: var(--background);
		color: var(--primary);
		border-bottom-color: var(--primary);
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.main-tab-navigation {
			flex-wrap: wrap;
		}

		.main-tab-btn {
			flex: 1 1 50%;
			padding: var(--spacing-sm);
			font-size: var(--font-size-xs);
		}
	}
</style>
