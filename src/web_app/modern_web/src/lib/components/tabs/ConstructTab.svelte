<!-- ConstructTab.svelte - Reorganized to match desktop app layout -->
<script lang="ts">
	// Import runes-based state and components
	import { onMount } from 'svelte';
	import { getCurrentSequence, getSequences, getIsLoading } from '$stores/sequenceState.svelte';
	import StartPositionPicker from '$components/construct/StartPositionPicker.svelte';
	import OptionPicker from '$components/construct/OptionPicker.svelte';
	import GeneratePanel from '$components/construct/GeneratePanel.svelte';
	import Workbench from '$components/workbench/Workbench.svelte';
	import type { BeatData, PictographData, SequenceData } from '$services/interfaces';
	import { IConstructTabCoordinationService, ISequenceService } from '$services/interfaces';
	import { resolve } from '$services/bootstrap';

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

	// Derived state: automatically determine what to show in Build tab
	let shouldShowStartPositionPicker = $derived(() => {
		const sequence = getCurrentSequence();
		// Show start position picker if no sequence or no beats
		return !sequence || !sequence.beats || sequence.beats.length === 0;
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
				pictograph_data: option
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

	// Handle main tab transitions
	function handleMainTabTransition(targetTab: 'build' | 'generate' | 'edit' | 'export') {
		activeRightPanel = targetTab;
		// Build tab content automatically determined by shouldShowStartPositionPicker
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
					}
				}
			});
		}
	});
</script>

<div class="construct-tab" data-testid="construct-tab">
	<!-- Error display -->
	{#if errorMessage}
		<div class="error-banner">
			<p>❌ {errorMessage}</p>
			<button onclick={() => errorMessage = null}>Dismiss</button>
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

			<!-- Tab Content -->
			<div class="tab-content">
				{#if activeRightPanel === 'build'}
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

				{:else if activeRightPanel === 'generate'}
					<GeneratePanel />

				{:else if activeRightPanel === 'edit'}
					<div class="panel-header">
						<h2>Graph Editor</h2>
						<p>Advanced sequence editing tools</p>
					</div>
					<div class="panel-content">
						<div class="placeholder-content">
							<p>Graph Editor coming soon...</p>
						</div>
					</div>

				{:else if activeRightPanel === 'export'}
					<div class="panel-header">
						<h2>Export Sequences</h2>
						<p>Export your sequences in various formats</p>
					</div>
					<div class="panel-content">
						<div class="placeholder-content">
							<p>Export panel coming soon...</p>
						</div>
					</div>
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
		background: var(--destructive)/10;
		color: var(--destructive);
		padding: var(--spacing-md) var(--spacing-lg);
		display: flex;
		justify-content: space-between;
		align-items: center;
		border-bottom: 1px solid var(--destructive)/20;
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
		background: var(--background);
		border: 1px solid var(--border);
		border-radius: var(--border-radius);
		overflow: hidden;
	}

	/* Right Panel: 4-Tab interface */
	.right-panel {
		flex: 1;
		display: flex;
		flex-direction: column;
		background: var(--background);
		border: 1px solid var(--border);
		border-radius: var(--border-radius);
		overflow: hidden;
	}

	/* Panel headers */
	.panel-header {
		flex-shrink: 0;
		padding: var(--spacing-lg);
		background: var(--muted)/30;
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
		background: var(--muted)/20;
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
		background: var(--muted)/30;
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
	}

	.panel-content {
		flex: 1;
		overflow: auto;
		padding: var(--spacing-lg);
	}

	.placeholder-content {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100%;
		color: var(--muted-foreground);
		font-size: var(--font-size-lg);
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
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
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
