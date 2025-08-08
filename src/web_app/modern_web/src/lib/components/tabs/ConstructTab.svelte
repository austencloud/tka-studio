<!-- ConstructTab.svelte - Modern implementation following desktop app layout -->
<script lang="ts">
	// Import runes-based state and components
	import { onMount } from 'svelte';
	import { getCurrentSequence, getSequences, getIsLoading } from '$stores/sequenceState.svelte';
	import StartPositionPicker from '$components/construct/StartPositionPicker.svelte';
	import OptionPicker from '$components/construct/OptionPicker.svelte';
	import Workbench from '$components/workbench/Workbench.svelte';
	import type { BeatData, PictographData, SequenceData } from '$services/interfaces';
	import { IConstructTabCoordinationService, ISequenceService } from '$services/interfaces';
	import { resolve } from '$services/bootstrap';

	// Props using runes
	const { isGenerateMode = false } = $props<{ isGenerateMode?: boolean }>();

	// Modern services - resolved when container is ready
	let constructCoordinator = $state<IConstructTabCoordinationService | null>(null);
	let sequenceService = $state<ISequenceService | null>(null);

	// Runes-based state (replacing legacy workbenchStore)
	let activeRightPanel = $state<'start_position' | 'option_picker' | 'graph_editor' | 'generate'>('start_position');
	let gridMode = $state<'diamond' | 'box'>('diamond');
	let isTransitioning = $state(false);
	let errorMessage = $state<string | null>(null);

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

			// Transition to option picker
			activeRightPanel = 'option_picker';
			errorMessage = null;

			console.log('✅ Transitioned to option picker');
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

			// For now, stay on option picker to continue building sequence
			// In the future, this could transition to workbench view
			errorMessage = null;

			console.log('✅ Beat added to sequence');
		} catch (error) {
			console.error('❌ Error handling option selection:', error);
			errorMessage = error instanceof Error ? error.message : 'Failed to add option to sequence';
		} finally {
			isTransitioning = false;
		}
	}

	// Handle view transitions (triggered by coordination service)
	function handleViewTransition(targetView: string) {
		switch (targetView) {
			case 'start_position_picker':
				activeRightPanel = 'start_position';
				break;
			case 'option_picker':
				activeRightPanel = 'option_picker';
				break;
			case 'graph_editor':
				activeRightPanel = 'graph_editor';
				break;
			case 'generate':
				activeRightPanel = 'generate';
				break;
			default:
				console.warn('Unknown view transition:', targetView);
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
								handleViewTransition(data.targetPanel);
								break;
							default:
								console.log(`ConstructTab received event: ${eventType}`, data);
						}
					}
				}
			});
		}

		// Listen for transition events
		const handleTransitionEvent = (event: CustomEvent) => {
			handleViewTransition(event.detail.targetPanel);
		};

		document.addEventListener('construct-tab-transition', handleTransitionEvent as EventListener);

		return () => {
			document.removeEventListener('construct-tab-transition', handleTransitionEvent as EventListener);
		};
	});

	// Determine initial view based on sequence state
	$effect(() => {
		const sequence = getCurrentSequence();
		if (sequence && sequence.beats && sequence.beats.length > 0) {
			// Has beats, show option picker
			activeRightPanel = 'option_picker';
		} else {
			// No beats, show start position picker
			activeRightPanel = 'start_position';
		}
	});
</script>

<div class="construct-tab" data-testid="construct-tab">
	<!-- Header -->
	<div class="construct-header">
		<h1>Construct</h1>
		<div class="construct-controls">
			<div class="mode-indicator">
				{isGenerateMode ? 'Generate Mode' : 'Construct Mode'}
			</div>
			<div class="grid-selector">
				<label>
					Grid:
					<select bind:value={gridMode}>
						<option value="diamond">Diamond</option>
						<option value="box">Box</option>
					</select>
				</label>
			</div>
		</div>
	</div>

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

		<!-- Right Panel: Tabbed interface -->
		<div class="right-panel">
			<!-- Tab Navigation -->
			<div class="tab-navigation">
				<button 
					class="tab-btn"
					class:active={activeRightPanel === 'start_position'}
					onclick={() => handleViewTransition('start_position_picker')}
				>
					Start Position
				</button>
				<button 
					class="tab-btn"
					class:active={activeRightPanel === 'option_picker'}
					onclick={() => handleViewTransition('option_picker')}
				>
					Option Picker
				</button>
				<button 
					class="tab-btn"
					class:active={activeRightPanel === 'graph_editor'}
					onclick={() => handleViewTransition('graph_editor')}
				>
					Graph Editor
				</button>
				<button 
					class="tab-btn"
					class:active={activeRightPanel === 'generate'}
					onclick={() => handleViewTransition('generate')}
				>
					Generate
				</button>
			</div>

			<!-- Tab Content -->
			<div class="tab-content">
				{#if activeRightPanel === 'start_position'}
					<div class="panel-header">
						<h2>Choose Start Position</h2>
						<p>Select a starting position for your sequence</p>
					</div>
					<div class="panel-content">
						<StartPositionPicker
							{gridMode}
							onStartPositionSelected={handleStartPositionSelected}
						/>
					</div>
				{:else if activeRightPanel === 'option_picker'}
					<div class="panel-header">
						<h2>Build Your Sequence</h2>
						<p>Choose the next move for your sequence</p>
					</div>
					<div class="panel-content">
						<OptionPicker 
							{currentSequence}
							difficulty="intermediate"
							onOptionSelected={handleOptionSelected}
						/>
					</div>
				{:else if activeRightPanel === 'graph_editor'}
					<div class="panel-header">
						<h2>Graph Editor</h2>
						<p>Advanced sequence editing tools</p>
					</div>
					<div class="panel-content">
						<div class="placeholder-content">
							<p>Graph Editor coming soon...</p>
						</div>
					</div>
				{:else if activeRightPanel === 'generate'}
					<div class="panel-header">
						<h2>Generate Sequences</h2>
						<p>AI-powered sequence generation</p>
					</div>
					<div class="panel-content">
						<div class="placeholder-content">
							<p>Generate panel coming soon...</p>
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

	.construct-header {
		flex-shrink: 0;
		background: var(--background);
		border-bottom: 1px solid var(--border);
		padding: var(--spacing-lg);
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: var(--spacing-md);
	}

	.construct-header h1 {
		margin: 0;
		color: var(--foreground);
		font-size: var(--font-size-2xl);
		font-weight: 600;
	}

	.construct-controls {
		display: flex;
		align-items: center;
		gap: var(--spacing-lg);
	}

	.mode-indicator {
		padding: var(--spacing-sm) var(--spacing-md);
		background: var(--primary)/10;
		color: var(--primary);
		border-radius: var(--border-radius);
		font-size: var(--font-size-sm);
		font-weight: 500;
	}

	.grid-selector label {
		display: flex;
		align-items: center;
		gap: var(--spacing-sm);
		color: var(--foreground);
		font-size: var(--font-size-sm);
	}

	.grid-selector select {
		padding: var(--spacing-xs) var(--spacing-sm);
		border: 1px solid var(--border);
		border-radius: var(--border-radius);
		background: var(--background);
		color: var(--foreground);
		cursor: pointer;
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

	/* Right Panel: Tabbed interface */
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

	/* Tab navigation */
	.tab-navigation {
		flex-shrink: 0;
		display: flex;
		background: var(--muted)/20;
		border-bottom: 1px solid var(--border);
	}

	.tab-btn {
		flex: 1;
		padding: var(--spacing-md);
		border: none;
		background: transparent;
		color: var(--muted-foreground);
		cursor: pointer;
		transition: all 0.2s ease;
		font-size: var(--font-size-sm);
		font-weight: 500;
		border-bottom: 2px solid transparent;
	}

	.tab-btn:hover {
		background: var(--muted)/30;
		color: var(--foreground);
	}

	.tab-btn.active {
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
		.construct-header {
			flex-direction: column;
			align-items: flex-start;
			gap: var(--spacing-md);
		}

		.construct-controls {
			width: 100%;
			justify-content: space-between;
		}

		.panel-header {
			padding: var(--spacing-md);
		}

		.tab-navigation {
			flex-wrap: wrap;
		}

		.tab-btn {
			flex: 1 1 50%;
			padding: var(--spacing-sm);
			font-size: var(--font-size-xs);
		}
	}
</style>
