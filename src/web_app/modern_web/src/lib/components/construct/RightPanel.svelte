<!--
	RightPanel.svelte
	
	Right panel component extracted from ConstructTab.
	Contains the 4-tab interface with navigation and content areas.
-->
<script lang="ts">
	import TabNavigation from './TabNavigation.svelte';
	import BuildTabContent from './BuildTabContent.svelte';
	import GeneratePanel from './GeneratePanel.svelte';
	import GraphEditor from '$components/graph-editor/GraphEditor.svelte';
	import ExportPanel from '$components/export/ExportPanel.svelte';
	import { constructTabState } from '$stores/constructTabState.svelte';
	import { constructTabEventService } from '$services/implementations/ConstructTabEventService';
	import { constructTabTransitionService } from '$services/implementations/ConstructTabTransitionService';

	// Reactive state from store
	let activeRightPanel = $derived(constructTabState.activeRightPanel);
	let isSubTabTransitionActive = $derived(constructTabState.isSubTabTransitionActive);

	// Get transition functions
	const transitions = constructTabTransitionService.getSubTabTransitions();

	// Event handlers for child components
	function handleBeatModified(beatIndex: number, beatData: any) {
		constructTabEventService.handleBeatModified(beatIndex, beatData);
	}

	function handleArrowSelected(arrowData: any) {
		constructTabEventService.handleArrowSelected(arrowData);
	}

	function handleGraphEditorVisibilityChanged(isVisible: boolean) {
		constructTabEventService.handleGraphEditorVisibilityChanged(isVisible);
	}

	function handleExportSettingChanged(event: CustomEvent) {
		constructTabEventService.handleExportSettingChanged(event);
	}

	function handlePreviewUpdateRequested(event: CustomEvent) {
		constructTabEventService.handlePreviewUpdateRequested(event);
	}

	function handleExportRequested(event: CustomEvent) {
		constructTabEventService.handleExportRequested(event);
	}
</script>

<div class="right-panel" data-testid="right-panel">
	<!-- Tab Navigation -->
	<TabNavigation />

	<!-- Tab Content with Fade Transitions -->
	<div class="tab-content">
		{#if activeRightPanel === 'build'}
			<div
				class="sub-tab-content"
				data-sub-tab="build"
				in:transitions.in
				out:transitions.out
			>
				<BuildTabContent />
			</div>
		{:else if activeRightPanel === 'generate'}
			<div class="sub-tab-content" data-sub-tab="generate">
				<GeneratePanel />
			</div>
		{:else if activeRightPanel === 'edit'}
			<div
				class="sub-tab-content"
				data-sub-tab="edit"
				in:transitions.in
				out:transitions.out
			>
				<div class="panel-header">
					<h2>Graph Editor</h2>
					<p>Advanced sequence editing tools</p>
				</div>
				<div class="panel-content graph-editor-content">
					<GraphEditor
						onBeatModified={handleBeatModified}
						onArrowSelected={handleArrowSelected}
						onVisibilityChanged={handleGraphEditorVisibilityChanged}
					/>
				</div>
			</div>
		{:else if activeRightPanel === 'export'}
			<div
				class="sub-tab-content"
				data-sub-tab="export"
				in:transitions.in
				out:transitions.out
			>
				<ExportPanel
					on:settingChanged={handleExportSettingChanged}
					on:previewUpdateRequested={handlePreviewUpdateRequested}
					on:exportRequested={handleExportRequested}
				/>
			</div>
		{/if}

		<!-- Debug sub-tab transition state -->
		{#if isSubTabTransitionActive}
			<div class="sub-tab-transition-debug">🎨 Sub-tab transitioning...</div>
		{/if}
	</div>
</div>

<style>
	.right-panel {
		flex: 1;
		display: flex;
		flex-direction: column;
		/* Transparent background to show beautiful background without blur */
		background: rgba(255, 255, 255, 0.05);
		/* backdrop-filter: blur(20px); - REMOVED to show background */
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: var(--border-radius);
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
		overflow: hidden;
	}

	.tab-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		position: relative;
	}

	.sub-tab-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		position: relative;
		height: 100%;
		width: 100%;
	}

	.panel-header {
		flex-shrink: 0;
		padding: var(--spacing-lg);
		background: var(--muted) / 30;
		border-bottom: 1px solid var(--border);
		text-align: center;
	}

	.panel-header h2 {
		margin: 0 0 var(--spacing-sm) 0;
		color: var(--foreground);
		font-size: var(--font-size-xl);
		font-weight: 500;
	}

	.panel-header p {
		margin: 0;
		color: var(--muted-foreground);
		font-size: var(--font-size-sm);
	}

	.panel-content {
		flex: 1;
		overflow: auto;
		padding: var(--spacing-lg);
	}

	.graph-editor-content {
		padding: 0;
		flex: 1;
		display: flex;
		flex-direction: column;
		min-height: 0;
	}

	.sub-tab-transition-debug {
		position: absolute;
		top: 60px;
		right: 20px;
		background: rgba(138, 43, 226, 0.9);
		color: white;
		padding: 6px 12px;
		border-radius: 15px;
		font-size: 12px;
		font-weight: 600;
		z-index: 999;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
		pointer-events: none;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.panel-header {
			padding: var(--spacing-md);
		}
	}
</style>
