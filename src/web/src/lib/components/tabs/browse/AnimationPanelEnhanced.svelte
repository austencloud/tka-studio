<!--
Enhanced Animation Panel with Unified Collapse/Expand Logic

Integrates with panel management system for consistent behavior.
Shows collapsed state (60px width) with expand button when collapsed.
-->
<script lang="ts">
	import { onDestroy } from 'svelte';
	import type { BrowseSequenceMetadata } from '$lib/domain/browse';
	import { resolve } from '$lib/services/bootstrap';
	import type { ISequenceService } from '$lib/services/interfaces';
	import { StandalonePortedEngine, AnimatorCanvas, ensureStandaloneFormat } from '$lib/animator';
	import type { PropState } from '$lib/animator';
	import type { PanelStateManager } from '$lib/state/panel-state.svelte';

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	const {
		sequence = null,
		panelState,
		onClose = () => {},
	} = $props<{
		sequence?: BrowseSequenceMetadata | null;
		panelState: PanelStateManager;
		onClose?: () => void;
	}>();

	// Services
	const sequenceService = resolve('ISequenceService') as ISequenceService;

	// ✅ DERIVED RUNES: Panel state
	let isVisible = $derived(panelState.isAnimationVisible);
	let isCollapsed = $derived(panelState.isAnimationCollapsed);

	// State
	let sequenceData: any = $state(null);
	let loading = $state(false);
	let error = $state<string | null>(null);

	// Animation engine and state
	let animationEngine = new StandalonePortedEngine();
	let currentBeat = $state(0);
	let isPlaying = $state(false);
	let speed = $state(1.0);
	let totalBeats = $state(0);
	let sequenceWord = $state('');
	let sequenceAuthor = $state('');
	let shouldLoop = $state(false);

	// Animation frame reference
	let animationFrameId: number | null = null;
	let lastTimestamp: number | null = null;

	// Prop states for rendering
	let bluePropState = $state<PropState>({
		centerPathAngle: 0,
		staffRotationAngle: 0,
		x: 0,
		y: 0,
	});
	let redPropState = $state<PropState>({
		centerPathAngle: 0,
		staffRotationAngle: 0,
		x: 0,
		y: 0,
	});

	// Clean up on component destroy
	$effect(() => {
		return () => {
			if (animationFrameId !== null) {
				cancelAnimationFrame(animationFrameId);
			}
		};
	});

	// Load sequence data when sequence changes
	$effect(() => {
		if (sequence && isVisible) {
			loadSequenceData();
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

			// Convert web app data to standalone format and initialize engine
			const standaloneData = ensureStandaloneFormat(fullSequence);

			if (animationEngine.initialize(standaloneData)) {
				sequenceData = fullSequence;
				const metadata = animationEngine.getMetadata();
				totalBeats = metadata.totalBeats;
				sequenceWord = metadata.word;
				sequenceAuthor = metadata.author;

				// Reset animation state
				currentBeat = 0;
				isPlaying = false;

				// Update prop states
				updatePropStates();

				console.log('✅ Sequence loaded for animation:', sequenceData);
			} else {
				throw new Error('Failed to initialize animation engine');
			}
		} catch (err) {
			console.error('❌ Failed to load sequence:', err);
			error = err instanceof Error ? err.message : 'Failed to load sequence';
		} finally {
			loading = false;
		}
	}

	// Update prop states from engine
	function updatePropStates(): void {
		bluePropState = animationEngine.getBluePropState();
		redPropState = animationEngine.getRedPropState();
	}

	// Animation loop using StandalonePortedEngine
	function animationLoop(timestamp: number): void {
		if (!isPlaying) return;

		// Calculate deltaTime
		if (lastTimestamp === null) {
			lastTimestamp = timestamp;
		}
		const deltaTime = timestamp - lastTimestamp;
		lastTimestamp = timestamp;

		// Update current beat based on speed
		const beatDelta = (deltaTime / 1000) * speed;
		const newBeat = currentBeat + beatDelta;

		// Check if we've reached the end
		const animationEndBeat = totalBeats + 1;

		if (newBeat > animationEndBeat) {
			if (shouldLoop) {
				// Loop back to start
				currentBeat = 0;
				lastTimestamp = null;
				animationEngine.reset();
			} else {
				// Stop at end
				currentBeat = totalBeats;
				isPlaying = false;
			}
		} else {
			currentBeat = newBeat;
		}

		// Calculate state for current beat using StandalonePortedEngine
		animationEngine.calculateState(currentBeat);

		// Update props from engine state
		updatePropStates();

		// Request next frame if still playing
		if (isPlaying) {
			animationFrameId = requestAnimationFrame(animationLoop);
		}
	}

	function handlePlay() {
		if (isPlaying) {
			isPlaying = false;
			if (animationFrameId !== null) {
				cancelAnimationFrame(animationFrameId);
				animationFrameId = null;
			}
		} else {
			isPlaying = true;
			lastTimestamp = null;
			animationFrameId = requestAnimationFrame(animationLoop);
		}
	}

	function handleStop() {
		currentBeat = 0;
		isPlaying = false;

		if (animationFrameId !== null) {
			cancelAnimationFrame(animationFrameId);
			animationFrameId = null;
		}

		animationEngine.reset();
		updatePropStates();
	}

	function handleBeatChange(beat: number) {
		// Stop any current animation
		isPlaying = false;
		if (animationFrameId !== null) {
			cancelAnimationFrame(animationFrameId);
			animationFrameId = null;
		}

		// Set the current beat
		currentBeat = Math.max(0, Math.min(beat, totalBeats));

		// Calculate state for this specific beat
		animationEngine.calculateState(currentBeat);
		updatePropStates();
	}

	function handleSpeedChange(value: number) {
		speed = Math.max(0.1, Math.min(3.0, value));
	}

	// ✅ PANEL ACTIONS: Use panel state manager
	function handleToggle() {
		panelState.toggleAnimationCollapse();
	}

	function handleClose() {
		panelState.setAnimationVisible(false);
		onClose();
	}

	onDestroy(() => {
		if (animationFrameId !== null) {
			cancelAnimationFrame(animationFrameId);
		}
	});
</script>

<div class="animation-panel" class:collapsed={isCollapsed} class:visible={isVisible}>
	<!-- Panel Header -->
	<div class="panel-header">
		{#if isCollapsed}
			<!-- Collapsed header - minimal with expand button -->
			<div class="collapsed-header">
				<button 
					class="expand-button"
					onclick={handleToggle}
					title="Expand animation panel"
					aria-label="Expand animation panel"
				>
					🎬
				</button>
			</div>
		{:else}
			<!-- Full header -->
			<div class="full-header">
				<h3>🎬 Animation</h3>
				<div class="panel-controls">
					<button 
						class="toggle-button" 
						onclick={handleToggle} 
						title="Collapse animation panel"
						aria-label="Collapse animation panel"
					>
						▶
					</button>
					<button 
						class="close-button" 
						onclick={handleClose} 
						title="Close animation panel"
						aria-label="Close animation panel"
					>
						✕
					</button>
				</div>
			</div>
		{/if}
	</div>

	<!-- Panel Content -->
	{#if !isCollapsed}
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
					<button class="control-button" onclick={handleStop}> ⏹️ </button>
					<div class="speed-control">
						<label for="speed-slider">Speed: {speed.toFixed(1)}x</label>
						<input
							id="speed-slider"
							type="range"
							min="0.1"
							max="3.0"
							step="0.1"
							value={speed}
							oninput={(e) => handleSpeedChange(parseFloat((e.target as HTMLInputElement).value))}
						/>
					</div>
					<div class="beat-info">
						Beat {Math.floor(currentBeat) + 1} of {totalBeats || sequenceData.beats?.length || 0}
					</div>
				</div>

				{#if sequenceData.beats && sequenceData.beats.length > 0}
					<div class="beat-selector">
						{#each sequenceData.beats as _, index}
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
						{#if sequenceData.beats[currentBeat]}
							{@const currentBeatData = sequenceData.beats[currentBeat]}
							<h5>
								Beat {currentBeat + 1}: {currentBeatData.pictograph_data?.letter || ''}
							</h5>

							{#if currentBeatData.pictograph_data?.motions}
								<div class="motions-display">
									<div class="motion blue-motion">
										<h6>Blue Prop</h6>
										<div class="motion-info">
											<span class="location">
												{currentBeatData.pictograph_data.motions.blue
													?.start_loc} →
												{currentBeatData.pictograph_data.motions.blue?.end_loc}
											</span>
											<span class="motion-type">
												{currentBeatData.pictograph_data.motions.blue
													?.motion_type}
											</span>
										</div>
									</div>

									<div class="motion red-motion">
										<h6>Red Prop</h6>
										<div class="motion-info">
											<span class="location">
												{currentBeatData.pictograph_data.motions.red?.start_loc}
												→
												{currentBeatData.pictograph_data.motions.red?.end_loc}
											</span>
											<span class="motion-type">
												{currentBeatData.pictograph_data.motions.red
													?.motion_type}
											</span>
										</div>
									</div>
								</div>
							{/if}
						{/if}
					</div>

					<div class="animation-canvas-container">
						<AnimatorCanvas
							blueProp={bluePropState}
							redProp={redPropState}
							width={350}
							height={350}
							gridVisible={true}
						/>
					</div>
				{/if}
			{/if}
		</div>
	{/if}
</div>

<style>
	.animation-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		background: var(--color-surface);
		border-left: 1px solid var(--color-border);
		overflow: hidden;
		transition: all 0.3s ease;
	}

	.animation-panel.collapsed {
		/* Collapsed state - only show minimal header */
		overflow: visible;
	}

	/* Panel Header */
	.panel-header {
		flex-shrink: 0;
		border-bottom: 1px solid var(--color-border);
		background: var(--color-surface-elevated);
	}

	/* Collapsed Header */
	.collapsed-header {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0.5rem;
		height: 60px;
	}

	.expand-button {
		background: none;
		border: none;
		font-size: 1.5rem;
		cursor: pointer;
		color: var(--color-text-secondary);
		padding: 0.75rem;
		border-radius: 0.5rem;
		transition: all 0.2s;
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.expand-button:hover {
		background: var(--color-surface-hover);
		color: var(--color-primary);
		transform: scale(1.1);
	}

	/* Full Header */
	.full-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 1rem;
	}

	.full-header h3 {
		margin: 0;
		font-size: 1.125rem;
		font-weight: 600;
		color: var(--color-text-primary);
	}

	.panel-controls {
		display: flex;
		gap: 0.5rem;
		align-items: center;
	}

	.toggle-button,
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

	.toggle-button:hover {
		background: var(--color-surface-hover);
		color: var(--color-primary);
	}

	.close-button:hover {
		background: var(--color-surface-hover);
		color: var(--color-text-primary);
	}

	/* Panel Content */
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
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
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
		flex-wrap: wrap;
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

	.speed-control {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		min-width: 120px;
	}

	.speed-control label {
		font-size: 0.75rem;
		color: var(--color-text-secondary);
		font-weight: 500;
	}

	.speed-control input[type="range"] {
		width: 100%;
		height: 4px;
		background: var(--color-border);
		border-radius: 2px;
		outline: none;
		-webkit-appearance: none;
	}

	.speed-control input[type="range"]::-webkit-slider-thumb {
		-webkit-appearance: none;
		width: 16px;
		height: 16px;
		background: var(--color-primary);
		border-radius: 50%;
		cursor: pointer;
	}

	.speed-control input[type="range"]::-moz-range-thumb {
		width: 16px;
		height: 16px;
		background: var(--color-primary);
		border-radius: 50%;
		cursor: pointer;
		border: none;
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

	.animation-canvas-container {
		margin-top: auto;
		padding: 1rem;
		background: var(--color-surface-elevated);
		border-radius: 0.5rem;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.hint {
		font-style: italic;
		color: var(--color-text-tertiary);
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.animation-controls {
			flex-direction: column;
			align-items: stretch;
		}

		.beat-info {
			margin-left: 0;
			text-align: center;
		}

		.animation-canvas-container {
			padding: 0.5rem;
		}
	}

	/* High contrast mode */
	@media (prefers-contrast: high) {
		.expand-button,
		.toggle-button,
		.close-button {
			border: 1px solid currentColor;
		}
	}

	/* Reduced motion support */
	@media (prefers-reduced-motion: reduce) {
		.animation-panel,
		.expand-button,
		.toggle-button,
		.close-button {
			transition: none;
		}

		.loading-spinner {
			animation: none;
		}
	}
</style>
