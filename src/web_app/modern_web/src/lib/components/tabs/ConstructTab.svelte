<!-- ConstructTab.svelte - Reorganized to match desktop app layout -->
<script lang="ts">
	// Import runes-based state and components
	import { onMount } from 'svelte';
	import {
		getCurrentSequence,
		getSequences,
		getIsLoading,
		state as sequenceState,
	} from '$stores/sequenceState.svelte';
	import StartPositionPicker from '$components/construct/StartPositionPicker.svelte';
	import OptionPicker from '$components/construct/OptionPicker.svelte';
	import GeneratePanel from '$components/construct/GeneratePanel.svelte';
	import Workbench from '$components/workbench/Workbench.svelte';
	import GraphEditor from '$components/graph-editor/GraphEditor.svelte';
	import ExportPanel from '$components/export/ExportPanel.svelte';
	import type { BeatData, PictographData, SequenceData } from '$services/interfaces';
	import { IConstructTabCoordinationService, ISequenceService } from '$services/interfaces';
	import { resolve } from '$services/bootstrap';

	// Import fade transitions for sub-tabs
	import {
		fluidTransition,
		transitionToSubTab,
		completeSubTabTransition,
		isSubTabTransitioning,
		getSubTabTransition,
		type ConstructSubTabId,
	} from '$services/ui/animation';

	// Props using runes
	const { isGenerateMode = false } = $props<{ isGenerateMode?: boolean }>();

	// Modern services - resolved when container is ready
	let constructCoordinator = $state<IConstructTabCoordinationService | null>(null);
	let sequenceService = $state<ISequenceService | null>(null);

	// Runes-based state following desktop app pattern
	let activeRightPanel = $state<'build' | 'generate' | 'edit' | 'export'>('build');
	let gridMode = $state<'diamond' | 'box'>('diamond');
	let isTransitioning = $state(false);
	let errorMessage = $state<string | null>(null);
	let isSubTabTransitionActive = $state(false);
	let currentSubTabTransition = $state<string | null>(null);

	// Derived state: automatically determine what to show in Build tab
	// Use a reactive variable instead of $derived to fix Svelte 5 reactivity issues
	let shouldShowStartPositionPicker = $state(true);

	// Use $effect to watch for sequence state changes and update the reactive variable
	$effect(() => {
		const sequence = sequenceState.currentSequence;
		const shouldShow = !sequence || !sequence.beats || sequence.beats.length === 0;

		console.log('🎯 ConstructTab shouldShowStartPositionPicker effect triggered:', {
			hasSequence: !!sequence,
			sequenceId: sequence?.id,
			hasBeats: !!sequence?.beats,
			beatCount: sequence?.beats?.length || 0,
			shouldShow: shouldShow,
			currentValue: shouldShowStartPositionPicker,
		});

		// Update the reactive variable
		shouldShowStartPositionPicker = shouldShow;

		console.log('🎯 Updated shouldShowStartPositionPicker to:', shouldShowStartPositionPicker);
	});

	// Reactive current sequence for template
	let currentSequence = $derived(getCurrentSequence());

	// Resolve services when container is ready
	$effect(() => {
		try {
			if (!constructCoordinator) {
				constructCoordinator = resolve(IConstructTabCoordinationService);
			}
			if (!sequenceService) {
				sequenceService = resolve(ISequenceService);
			}
		} catch (error) {
			console.error('ConstructTab: Failed to resolve services:', error);
			// Services will remain null and component will handle gracefully
		}
	});

	// Handle start position selection
	async function handleStartPositionSelected(startPosition: BeatData) {
		try {
			console.log('🎭 Start position selected in ConstructTab:', startPosition.pictograph_data?.id);
			isTransitioning = true;

			// Use coordination service to handle the selection
			if (constructCoordinator) {
				await constructCoordinator.handleStartPositionSet(startPosition);
			}

			// Transition will happen automatically via shouldShowStartPositionPicker
			// when the sequence gets updated with the start position
			errorMessage = null;

			console.log('✅ Transitioned to option picker within Build tab');
		} catch (error) {
			console.error('❌ Error handling start position selection:', error);
			errorMessage = error instanceof Error ? error.message : 'Failed to set start position';
		} finally {
			isTransitioning = false;
		}
	}

	// Handle option selection
	async function handleOptionSelected(option: PictographData) {
		try {
			console.log('🎭 Option selected in ConstructTab:', option.id);
			isTransitioning = true;

			// Create beat data from option
			const beatData: BeatData = {
				beat: getCurrentSequence()?.beats.length || 1,
				pictograph_data: option,
			};

			// Use coordination service to handle beat addition
			if (constructCoordinator) {
				await constructCoordinator.handleBeatAdded(beatData);
			}

			// Stay on option picker to continue building sequence
			errorMessage = null;

			console.log('✅ Beat added to sequence');
		} catch (error) {
			console.error('❌ Error handling option selection:', error);
			errorMessage = error instanceof Error ? error.message : 'Failed to add option to sequence';
		} finally {
			isTransitioning = false;
		}
	}

	// Handle main tab transitions with fade
	async function handleMainTabTransition(targetTab: 'build' | 'generate' | 'edit' | 'export') {
		const currentTab = activeRightPanel;

		if (currentTab === targetTab) {
			return; // Already on this tab
		}

		try {
			// Start sub-tab transition
			const transitionId = await transitionToSubTab(
				currentTab as ConstructSubTabId,
				targetTab as ConstructSubTabId
			);

			if (transitionId) {
				isSubTabTransitionActive = true;
				currentSubTabTransition = transitionId;

				// Update active panel for reactive state
				activeRightPanel = targetTab;

				// Complete transition after brief delay
				setTimeout(() => {
					completeSubTabTransition(transitionId, currentTab, targetTab);
					isSubTabTransitionActive = false;
					currentSubTabTransition = null;
				}, 50);

				console.log(`🎭 Sub-tab transition: ${currentTab} → ${targetTab}`);
			} else {
				// Fallback to immediate switch
				activeRightPanel = targetTab;
			}
		} catch (error) {
			console.warn('Sub-tab transition failed, falling back to immediate switch:', error);
			activeRightPanel = targetTab;
		}
		// Build tab content automatically determined by shouldShowStartPositionPicker
	}

	// Sub-tab transition functions - direct transition functions
	const subTabInTransition = (node: Element) => ({
		duration: 250,
		css: (t: number) => `opacity: ${t}`,
	});

	const subTabOutTransition = (node: Element) => ({
		duration: 200,
		css: (t: number) => `opacity: ${1 - t}`,
	});

	// Graph Editor event handlers
	function handleBeatModified(beatIndex: number, beatData: BeatData) {
		console.log('ConstructTab: Beat modified in graph editor', beatIndex, beatData);
		// Handle beat modifications from graph editor
		// This could update the sequence through the coordination service
		if (constructCoordinator) {
			constructCoordinator.handleBeatModified?.(beatIndex, beatData);
		}
	}

	function handleArrowSelected(arrowData: any) {
		console.log('ConstructTab: Arrow selected in graph editor', arrowData);
		// Handle arrow selection events from graph editor
		// This could be used for highlighting or additional UI feedback
	}

	function handleGraphEditorVisibilityChanged(isVisible: boolean) {
		console.log('ConstructTab: Graph editor visibility changed', isVisible);
		// Handle graph editor visibility changes if needed
	}

	// Export Panel event handlers
	function handleExportSettingChanged(event: CustomEvent) {
		const { setting, value } = event.detail;
		console.log('ConstructTab: Export setting changed', setting, value);
		// Handle export setting changes - could save to settings service
	}

	function handlePreviewUpdateRequested(event: CustomEvent) {
		const settings = event.detail;
		console.log('ConstructTab: Preview update requested', settings);
		// Handle preview update requests
	}

	function handleExportRequested(event: CustomEvent) {
		const { type, config } = event.detail;
		console.log('ConstructTab: Export requested', type, config);

		// Handle export requests
		if (type === 'current') {
			console.log('Exporting current sequence:', config.sequence?.name);
			// TODO: Implement actual export service call
			alert(
				`Exporting sequence "${config.sequence?.name || 'Untitled'}" with ${config.sequence?.beats?.length || 0} beats`
			);
		} else if (type === 'all') {
			console.log('Exporting all sequences');
			// TODO: Implement actual export all service call
			alert('Exporting all sequences in library');
		}
	}

	// Setup component coordination on mount
	onMount(() => {
		console.log('🎭 ConstructTab mounted, setting up coordination');

		// Register this component with the coordination service
		if (constructCoordinator) {
			constructCoordinator.setupComponentCoordination({
				constructTab: {
					handleEvent: (eventType: string, data: any) => {
						switch (eventType) {
							case 'ui_transition':
								// Handle legacy transition events if needed
								break;
							default:
								console.log(`ConstructTab received event: ${eventType}`, data);
						}
					},
				},
			});
		}
	});
</script>

<div class="construct-tab" data-testid="construct-tab">
	<!-- Error display -->
	{#if errorMessage}
		<div class="error-banner">
			<p>❌ {errorMessage}</p>
			<button onclick={() => (errorMessage = null)}>Dismiss</button>
		</div>
	{/if}

	<!-- Main content area - Two panel layout like desktop app -->
	<div class="construct-content">
		<!-- Left Panel: Workbench (always visible) -->
		<div class="left-panel">
			<div class="panel-header">
				<h2>Sequence Workbench</h2>
				{#if currentSequence}
					<div class="sequence-info">
						<span class="sequence-name">{currentSequence.name}</span>
						<span class="beat-count">{currentSequence.beats.length} beats</span>
					</div>
				{/if}
			</div>
			<div class="workbench-container">
				<Workbench />
			</div>
		</div>

		<!-- Right Panel: 4-Tab interface matching desktop -->
		<div class="right-panel">
			<!-- Main Tab Navigation (matches desktop: Build/Generate/Edit/Export) -->
			<div class="main-tab-navigation">
				<button
					class="main-tab-btn"
					class:active={activeRightPanel === 'build'}
					onclick={() => handleMainTabTransition('build')}
				>
					🔨 Build
				</button>
				<button
					class="main-tab-btn"
					class:active={activeRightPanel === 'generate'}
					onclick={() => handleMainTabTransition('generate')}
				>
					🤖 Generate
				</button>
				<button
					class="main-tab-btn"
					class:active={activeRightPanel === 'edit'}
					onclick={() => handleMainTabTransition('edit')}
				>
					🔧 Edit
				</button>
				<button
					class="main-tab-btn"
					class:active={activeRightPanel === 'export'}
					onclick={() => handleMainTabTransition('export')}
				>
					🔤 Export
				</button>
			</div>

			<!-- Tab Content with Fade Transitions -->
			<div class="tab-content">
				{#if activeRightPanel === 'build'}
					<div
						class="sub-tab-content"
						data-sub-tab="build"
						in:subTabInTransition
						out:subTabOutTransition
					>
						<!-- Build Tab: Automatically shows Start Position OR Option Picker based on sequence state -->
						{#if shouldShowStartPositionPicker}
							<div class="panel-header">
								<h3>Choose Start Position</h3>
								<p>Select a starting position for your sequence</p>
							</div>
							<div class="panel-content">
								<StartPositionPicker
									{gridMode}
									onStartPositionSelected={handleStartPositionSelected}
								/>
							</div>
						{:else}
							<div class="panel-header">
								<h3>Build Your Sequence</h3>
								<p>Choose the next move for your sequence</p>
							</div>
							<div class="panel-content">
								<OptionPicker
									{currentSequence}
									difficulty="intermediate"
									onOptionSelected={handleOptionSelected}
								/>
							</div>
						{/if}
					</div>
				{:else if activeRightPanel === 'generate'}
					<div class="sub-tab-content" data-sub-tab="generate">
						<GeneratePanel />
					</div>
				{:else if activeRightPanel === 'edit'}
					<div
						class="sub-tab-content"
						data-sub-tab="edit"
						in:subTabInTransition
						out:subTabOutTransition
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
						in:subTabInTransition
						out:subTabOutTransition
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
	</div>

	<!-- Loading overlay -->
	{#if isTransitioning}
		<div class="loading-overlay">
			<div class="loading-spinner"></div>
			<p>Processing...</p>
		</div>
	{/if}
</div>

<style>
	.construct-tab {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		overflow: hidden;
		position: relative;
	}

	.error-banner {
		flex-shrink: 0;
		background: var(--destructive) / 10;
		color: var(--destructive);
		padding: var(--spacing-md) var(--spacing-lg);
		display: flex;
		justify-content: space-between;
		align-items: center;
		border-bottom: 1px solid var(--destructive) / 20;
	}

	.error-banner p {
		margin: 0;
		font-size: var(--font-size-sm);
	}

	.error-banner button {
		padding: var(--spacing-xs) var(--spacing-sm);
		background: var(--destructive);
		color: var(--destructive-foreground);
		border: none;
		border-radius: var(--border-radius-sm);
		cursor: pointer;
		font-size: var(--font-size-xs);
	}

	/* Main two-panel layout */
	.construct-content {
		flex: 1;
		display: flex;
		overflow: hidden;
		gap: 8px;
		padding: 8px;
	}

	/* Left Panel: Workbench */
	.left-panel {
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

	/* Right Panel: 4-Tab interface */
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

	/* Panel headers */
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

	.panel-header h3 {
		margin: 0 0 var(--spacing-sm) 0;
		color: var(--foreground);
		font-size: var(--font-size-lg);
		font-weight: 500;
	}

	.panel-header p {
		margin: 0;
		color: var(--muted-foreground);
		font-size: var(--font-size-sm);
	}

	.sequence-info {
		margin-top: var(--spacing-md);
		display: flex;
		justify-content: center;
		gap: var(--spacing-md);
		font-size: var(--font-size-sm);
	}

	.beat-count {
		padding: var(--spacing-xs) var(--spacing-sm);
		background: var(--primary);
		color: var(--primary-foreground);
		border-radius: var(--border-radius-sm);
		font-weight: 500;
	}

	.sequence-name {
		padding: var(--spacing-xs) var(--spacing-sm);
		background: var(--muted);
		color: var(--muted-foreground);
		border-radius: var(--border-radius-sm);
	}

	/* Workbench container */
	.workbench-container {
		flex: 1;
		overflow: auto;
		padding: var(--spacing-md);
	}

	/* Main tab navigation (4 main tabs) */
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

	/* Tab content */
	.tab-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		position: relative;
	}

	/* Sub-tab content styling for transitions */
	.sub-tab-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		position: relative;
		height: 100%;
		width: 100%;
	}

	/* Debug sub-tab transition indicator */
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

	/* Loading overlay */
	.loading-overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(255, 255, 255, 0.9);
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		z-index: 1000;
		backdrop-filter: blur(4px);
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 4px solid var(--muted);
		border-top: 4px solid var(--primary);
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: var(--spacing-md);
	}

	.loading-overlay p {
		color: var(--foreground);
		font-size: var(--font-size-lg);
		margin: 0;
		font-weight: 500;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	/* Responsive adjustments */
	@media (max-width: 1024px) {
		.construct-content {
			flex-direction: column;
		}

		.left-panel,
		.right-panel {
			flex: none;
			height: 50%;
		}
	}

	@media (max-width: 768px) {
		.panel-header {
			padding: var(--spacing-md);
		}

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
