<!--
AnimationPanel Component - Phase 3 Integration

Right-side panel for animating sequences in the browse tab.
Integrates the animator module directly into the browse experience.
-->
<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import type { BrowseSequenceMetadata } from '$lib/domain/browse';
	import { resolve } from '$lib/services/bootstrap';
	import type { ISequenceService } from '$lib/services/interfaces';

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	const {
		sequence = null,
		isVisible = false,
		onClose = () => {},
	} = $props<{
		sequence?: BrowseSequenceMetadata | null;
		isVisible?: boolean;
		onClose?: () => void;
	}>();

	// Services
	const sequenceService = resolve('ISequenceService') as ISequenceService;

	// State
	let animatorContainer: HTMLDivElement;
	let sequenceData: any = $state(null);
	let loading = $state(false);
	let error = $state<string | null>(null);

	// For Phase 3, we'll create a simple sequence viewer
	// In Phase 4, we'll integrate the full animator
	let currentBeat = $state(0);
	let isPlaying = $state(false);
	let playInterval: number | null = null;

	// Load sequence data when sequence changes
	$effect(async () => {
		if (sequence && isVisible) {
			await loadSequenceData();
		}
	});

	async function loadSequenceData() {
		if (!sequence) return;

		loading = true;
		error = null;

		try {
			console.log('🎬 Loading sequence for animation:', sequence.id);
			const fullSequence = await sequenceService.getSequence(sequence.id);
			
			if (!fullSequence) {
				throw new Error(`Sequence not found: ${sequence.id}`);
			}

			sequenceData = fullSequence;
			currentBeat = 0;
			console.log('✅ Sequence loaded for animation:', sequenceData);
		} catch (err) {
			console.error('❌ Failed to load sequence:', err);
			error = err instanceof Error ? err.message : 'Failed to load sequence';
		} finally {
			loading = false;
		}
	}

	function handlePlay() {
		if (!sequenceData?.beats) return;

		if (isPlaying) {
			// Stop playing
			if (playInterval) {
				clearInterval(playInterval);
				playInterval = null;
			}
			isPlaying = false;
		} else {
			// Start playing
			isPlaying = true;
			playInterval = setInterval(() => {
				currentBeat = (currentBeat + 1) % sequenceData.beats.length;
			}, 1000); // 1 second per beat
		}
	}

	function handleStop() {
		if (playInterval) {
			clearInterval(playInterval);
			playInterval = null;
		}
		isPlaying = false;
		currentBeat = 0;
	}

	function handleBeatChange(beat: number) {
		currentBeat = beat;
	}

	onDestroy(() => {
		if (playInterval) {
			clearInterval(playInterval);
		}
	});
</script>

<div class="animation-panel" class:visible={isVisible}>
	<div class="panel-header">
		<h3>🎬 Animation</h3>
		<button class="close-button" onclick={onClose} aria-label="Close animation panel">
			✕
		</button>
	</div>

	<div class="panel-content">
		{#if loading}
			<div class="loading-state">
				<div class="loading-spinner"></div>
				<p>Loading sequence...</p>
			</div>
		{:else if error}
			<div class="error-state">
				<p>❌ {error}</p>
				<button onclick={() => loadSequenceData()}>Retry</button>
			</div>
		{:else if !sequence}
			<div class="empty-state">
				<p>🎬 Select a sequence to animate</p>
				<p class="hint">Click the animate button (🎬) on any sequence card</p>
			</div>
		{:else if sequenceData}
			<div class="sequence-info">
				<h4>{sequenceData.name || sequenceData.word}</h4>
				<p class="author">{sequenceData.metadata?.author || 'Unknown Author'}</p>
			</div>

			<div class="animation-controls">
				<button class="control-button" onclick={handlePlay}>
					{isPlaying ? '⏸️' : '▶️'}
				</button>
				<button class="control-button" onclick={handleStop}>
					⏹️
				</button>
				<div class="beat-info">
					Beat {currentBeat + 1} of {sequenceData.beats?.length || 0}
				</div>
			</div>

			{#if sequenceData.beats && sequenceData.beats.length > 0}
				<div class="beat-selector">
					{#each sequenceData.beats as beat, index}
						<button 
							class="beat-button" 
							class:active={index === currentBeat}
							onclick={() => handleBeatChange(index)}
						>
							{index + 1}
						</button>
					{/each}
				</div>

				<div class="current-beat-display">
					{@const currentBeatData = sequenceData.beats[currentBeat]}
					{#if currentBeatData}
						<h5>Beat {currentBeat + 1}: {currentBeatData.pictograph_data?.letter || ''}</h5>
						
						{#if currentBeatData.pictograph_data?.motions}
							<div class="motions-display">
								<div class="motion blue-motion">
									<h6>Blue Prop</h6>
									<div class="motion-info">
										<span class="location">
											{currentBeatData.pictograph_data.motions.blue?.start_loc} → 
											{currentBeatData.pictograph_data.motions.blue?.end_loc}
										</span>
										<span class="motion-type">
											{currentBeatData.pictograph_data.motions.blue?.motion_type}
										</span>
									</div>
								</div>
								
								<div class="motion red-motion">
									<h6>Red Prop</h6>
									<div class="motion-info">
										<span class="location">
											{currentBeatData.pictograph_data.motions.red?.start_loc} → 
											{currentBeatData.pictograph_data.motions.red?.end_loc}
										</span>
										<span class="motion-type">
											{currentBeatData.pictograph_data.motions.red?.motion_type}
										</span>
									</div>
								</div>
							</div>
						{/if}
					{/if}
				</div>

				<div class="animation-placeholder">
					<div class="placeholder-content">
						<h6>🚧 Visual Animation Coming Soon</h6>
						<p>Full 3D animation will be available in Phase 4</p>
						<p>Currently showing sequence data and beat progression</p>
					</div>
				</div>
			{/if}
		{/if}
	</div>
</div>

<style>
	.animation-panel {
		width: 400px;
		height: 100%;
		background: var(--color-surface);
		border-left: 1px solid var(--color-border);
		display: flex;
		flex-direction: column;
		transform: translateX(100%);
		transition: transform 0.3s ease;
		overflow: hidden;
	}

	.animation-panel.visible {
		transform: translateX(0);
	}

	.panel-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 1rem;
		border-bottom: 1px solid var(--color-border);
		background: var(--color-surface-elevated);
	}

	.panel-header h3 {
		margin: 0;
		font-size: 1.125rem;
		font-weight: 600;
		color: var(--color-text-primary);
	}

	.close-button {
		background: none;
		border: none;
		font-size: 1.25rem;
		cursor: pointer;
		color: var(--color-text-secondary);
		padding: 0.25rem;
		border-radius: 0.25rem;
		transition: background-color 0.2s;
	}

	.close-button:hover {
		background: var(--color-surface-hover);
		color: var(--color-text-primary);
	}

	.panel-content {
		flex: 1;
		padding: 1rem;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.loading-state,
	.error-state,
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		text-align: center;
		padding: 2rem;
		color: var(--color-text-secondary);
	}

	.loading-spinner {
		width: 32px;
		height: 32px;
		border: 3px solid var(--color-border);
		border-top: 3px solid var(--color-primary);
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 1rem;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	.sequence-info h4 {
		margin: 0 0 0.25rem 0;
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-text-primary);
	}

	.sequence-info .author {
		margin: 0;
		font-size: 0.875rem;
		color: var(--color-text-secondary);
	}

	.animation-controls {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.75rem;
		background: var(--color-surface-elevated);
		border-radius: 0.5rem;
	}

	.control-button {
		background: var(--color-primary);
		color: white;
		border: none;
		padding: 0.5rem;
		border-radius: 0.375rem;
		cursor: pointer;
		font-size: 1rem;
		transition: background-color 0.2s;
	}

	.control-button:hover {
		background: var(--color-primary-hover);
	}

	.beat-info {
		margin-left: auto;
		font-size: 0.875rem;
		color: var(--color-text-secondary);
	}

	.beat-selector {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem;
		padding: 0.5rem;
		background: var(--color-surface-elevated);
		border-radius: 0.5rem;
	}

	.beat-button {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		padding: 0.375rem 0.75rem;
		border-radius: 0.25rem;
		cursor: pointer;
		font-size: 0.875rem;
		transition: all 0.2s;
	}

	.beat-button:hover {
		background: var(--color-surface-hover);
	}

	.beat-button.active {
		background: var(--color-primary);
		color: white;
		border-color: var(--color-primary);
	}

	.current-beat-display {
		background: var(--color-surface-elevated);
		padding: 1rem;
		border-radius: 0.5rem;
	}

	.current-beat-display h5 {
		margin: 0 0 0.75rem 0;
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-text-primary);
	}

	.motions-display {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.motion {
		padding: 0.75rem;
		border-radius: 0.375rem;
		border-left: 4px solid;
	}

	.blue-motion {
		background: rgba(59, 130, 246, 0.1);
		border-left-color: #3b82f6;
	}

	.red-motion {
		background: rgba(239, 68, 68, 0.1);
		border-left-color: #ef4444;
	}

	.motion h6 {
		margin: 0 0 0.5rem 0;
		font-size: 0.875rem;
		font-weight: 600;
	}

	.motion-info {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		font-size: 0.8125rem;
	}

	.location {
		font-weight: 500;
	}

	.motion-type {
		color: var(--color-text-secondary);
		text-transform: capitalize;
	}

	.animation-placeholder {
		margin-top: auto;
		padding: 1.5rem;
		background: var(--color-surface-elevated);
		border-radius: 0.5rem;
		border: 2px dashed var(--color-border);
		text-align: center;
	}

	.placeholder-content h6 {
		margin: 0 0 0.5rem 0;
		font-size: 0.875rem;
		font-weight: 600;
		color: var(--color-text-primary);
	}

	.placeholder-content p {
		margin: 0.25rem 0;
		font-size: 0.8125rem;
		color: var(--color-text-secondary);
	}

	.hint {
		font-style: italic;
		color: var(--color-text-tertiary);
	}
</style>
