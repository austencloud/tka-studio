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

				// 🔍 [RAW DATA DEBUG] Extract and display raw sequence data
				console.log('🔍 [RAW DATA DEBUG] ===== FULL SEQUENCE DATA =====');
				console.log('🔍 [RAW DATA DEBUG] Sequence ID:', fullSequence.id);
				console.log('🔍 [RAW DATA DEBUG] Sequence Name:', fullSequence.name);
				console.log('🔍 [RAW DATA DEBUG] Number of beats:', fullSequence.beats.length);

				fullSequence.beats.forEach((beat, index) => {
					console.log(`🔍 [RAW DATA DEBUG] Beat ${index + 1}:`, {
						beat_number: beat.beat_number,
						letter: beat.pictograph_data?.letter,
						blue_motion_type: beat.pictograph_data?.motions?.blue?.motion_type,
						red_motion_type: beat.pictograph_data?.motions?.red?.motion_type,
						blue_motion_full: beat.pictograph_data?.motions?.blue,
						red_motion_full: beat.pictograph_data?.motions?.red
					});

					// Special focus on L and F letters
					if (beat.pictograph_data?.letter === 'L' || beat.pictograph_data?.letter === 'F') {
						console.log(`🚨 [CRITICAL] ${beat.pictograph_data.letter} letter motion types:`, {
							blue: beat.pictograph_data?.motions?.blue?.motion_type,
							red: beat.pictograph_data?.motions?.red?.motion_type,
							expected: 'Should have anti-motions!'
						});
					}
				});
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
		background: rgba(255, 255, 255, 0.03);
		backdrop-filter: blur(20px);
		border-left: 1px solid rgba(255, 255, 255, 0.1);
		overflow: hidden;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
	}

	.animation-panel.collapsed {
		/* Collapsed state - only show minimal header */
		overflow: visible;
		background: rgba(255, 255, 255, 0.02);
	}

	/* Panel Header */
	.panel-header {
		flex-shrink: 0;
		border-bottom: 1px solid rgba(255, 255, 255, 0.08);
		background: linear-gradient(135deg, 
			rgba(255, 255, 255, 0.08) 0%, 
			rgba(255, 255, 255, 0.04) 100%);
		backdrop-filter: blur(10px);
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
		background: rgba(255, 255, 255, 0.05);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.1);
		font-size: 1.5rem;
		cursor: pointer;
		color: rgba(255, 255, 255, 0.8);
		padding: 0.75rem;
		border-radius: 12px;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	}

	.expand-button:hover {
		background: rgba(255, 255, 255, 0.12);
		border-color: rgba(99, 102, 241, 0.3);
		color: #818cf8;
		transform: scale(1.05);
		box-shadow: 0 4px 16px rgba(99, 102, 241, 0.2);
	}

	/* Full Header */
	.full-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 1rem 1.25rem;
	}

	.full-header h3 {
		margin: 0;
		font-size: 1.125rem;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.95);
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.panel-controls {
		display: flex;
		gap: 0.5rem;
		align-items: center;
	}

	.toggle-button,
	.close-button {
		background: rgba(255, 255, 255, 0.05);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.1);
		font-size: 1.125rem;
		cursor: pointer;
		color: rgba(255, 255, 255, 0.7);
		padding: 0.5rem;
		border-radius: 8px;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		display: flex;
		align-items: center;
		justify-content: center;
		min-width: 36px;
		height: 36px;
	}

	.toggle-button:hover {
		background: rgba(255, 255, 255, 0.12);
		border-color: rgba(99, 102, 241, 0.3);
		color: #818cf8;
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
	}

	.close-button:hover {
		background: rgba(255, 255, 255, 0.12);
		border-color: rgba(239, 68, 68, 0.3);
		color: #f87171;
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(239, 68, 68, 0.15);
	}

	/* Panel Content */
	.panel-content {
		flex: 1;
		padding: 1.25rem;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		gap: 1.25rem;
		background: linear-gradient(135deg, 
			rgba(255, 255, 255, 0.02) 0%, 
			rgba(255, 255, 255, 0.01) 100%);
	}

	.loading-state,
	.error-state,
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		text-align: center;
		padding: 2.5rem 1.5rem;
		color: rgba(255, 255, 255, 0.7);
		background: rgba(255, 255, 255, 0.03);
		border: 1px solid rgba(255, 255, 255, 0.08);
		border-radius: 16px;
		backdrop-filter: blur(10px);
	}

	.loading-spinner {
		width: 36px;
		height: 36px;
		border: 3px solid rgba(255, 255, 255, 0.1);
		border-top: 3px solid #818cf8;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 1.25rem;
		box-shadow: 0 0 20px rgba(129, 140, 248, 0.3);
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
		margin: 0 0 0.5rem 0;
		font-size: 1.125rem;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.95);
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.sequence-info .author {
		margin: 0;
		font-size: 0.875rem;
		color: rgba(255, 255, 255, 0.6);
	}

	.animation-controls {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 1rem 1.25rem;
		background: linear-gradient(135deg, 
			rgba(255, 255, 255, 0.08) 0%, 
			rgba(255, 255, 255, 0.04) 100%);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 16px;
		flex-wrap: wrap;
		backdrop-filter: blur(15px);
		box-shadow: 
			0 4px 16px rgba(0, 0, 0, 0.1),
			inset 0 1px 0 rgba(255, 255, 255, 0.1);
	}

	.control-button {
		background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
		color: white;
		border: 1px solid rgba(255, 255, 255, 0.2);
		padding: 0.625rem 0.75rem;
		border-radius: 12px;
		cursor: pointer;
		font-size: 1.125rem;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		backdrop-filter: blur(10px);
		box-shadow: 
			0 2px 8px rgba(99, 102, 241, 0.3),
			inset 0 1px 0 rgba(255, 255, 255, 0.2);
		display: flex;
		align-items: center;
		justify-content: center;
		min-width: 44px;
		height: 44px;
	}

	.control-button:hover {
		background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
		transform: translateY(-2px);
		box-shadow: 
			0 6px 20px rgba(99, 102, 241, 0.4),
			inset 0 1px 0 rgba(255, 255, 255, 0.3);
	}

	.speed-control {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		min-width: 140px;
	}

	.speed-control label {
		font-size: 0.75rem;
		color: rgba(255, 255, 255, 0.8);
		font-weight: 500;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.speed-control input[type="range"] {
		width: 100%;
		height: 6px;
		background: linear-gradient(90deg, 
			rgba(255, 255, 255, 0.1) 0%, 
			rgba(255, 255, 255, 0.2) 100%);
		border-radius: 3px;
		outline: none;
		-webkit-appearance: none;
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.speed-control input[type="range"]::-webkit-slider-thumb {
		-webkit-appearance: none;
		width: 20px;
		height: 20px;
		background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
		border-radius: 50%;
		cursor: pointer;
		border: 2px solid rgba(255, 255, 255, 0.3);
		box-shadow: 
			0 2px 8px rgba(99, 102, 241, 0.4),
			inset 0 1px 0 rgba(255, 255, 255, 0.3);
		transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.speed-control input[type="range"]::-webkit-slider-thumb:hover {
		transform: scale(1.1);
		box-shadow: 
			0 4px 12px rgba(99, 102, 241, 0.6),
			inset 0 1px 0 rgba(255, 255, 255, 0.4);
	}

	.speed-control input[type="range"]::-moz-range-thumb {
		width: 20px;
		height: 20px;
		background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
		border-radius: 50%;
		cursor: pointer;
		border: 2px solid rgba(255, 255, 255, 0.3);
		box-shadow: 
			0 2px 8px rgba(99, 102, 241, 0.4),
			inset 0 1px 0 rgba(255, 255, 255, 0.3);
	}

	.beat-info {
		margin-left: auto;
		font-size: 0.875rem;
		color: rgba(255, 255, 255, 0.7);
		font-weight: 500;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.beat-selector {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		padding: 1rem;
		background: linear-gradient(135deg, 
			rgba(255, 255, 255, 0.06) 0%, 
			rgba(255, 255, 255, 0.03) 100%);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 16px;
		backdrop-filter: blur(15px);
	}

	.beat-button {
		background: rgba(255, 255, 255, 0.05);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.15);
		padding: 0.5rem 0.875rem;
		border-radius: 10px;
		cursor: pointer;
		font-size: 0.875rem;
		font-weight: 500;
		color: rgba(255, 255, 255, 0.8);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		min-width: 44px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.beat-button:hover {
		background: rgba(255, 255, 255, 0.12);
		border-color: rgba(255, 255, 255, 0.25);
		color: rgba(255, 255, 255, 0.95);
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}

	.beat-button.active {
		background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
		color: white;
		border-color: rgba(255, 255, 255, 0.3);
		box-shadow: 
			0 4px 16px rgba(99, 102, 241, 0.4),
			inset 0 1px 0 rgba(255, 255, 255, 0.2);
		transform: translateY(-1px);
	}

	.current-beat-display {
		background: linear-gradient(135deg, 
			rgba(255, 255, 255, 0.08) 0%, 
			rgba(255, 255, 255, 0.04) 100%);
		border: 1px solid rgba(255, 255, 255, 0.1);
		padding: 1.25rem;
		border-radius: 16px;
		backdrop-filter: blur(15px);
		box-shadow: 
			0 4px 16px rgba(0, 0, 0, 0.1),
			inset 0 1px 0 rgba(255, 255, 255, 0.1);
	}

	.current-beat-display h5 {
		margin: 0 0 1rem 0;
		font-size: 1.125rem;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.95);
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.motions-display {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.motion {
		padding: 1rem;
		border-radius: 12px;
		border-left: 4px solid;
		background: rgba(255, 255, 255, 0.04);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.08);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.motion:hover {
		background: rgba(255, 255, 255, 0.08);
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	}

	.blue-motion {
		border-left-color: #60a5fa;
		box-shadow: inset 4px 0 0 #60a5fa;
	}

	.red-motion {
		border-left-color: #f87171;
		box-shadow: inset 4px 0 0 #f87171;
	}

	.motion h6 {
		margin: 0 0 0.75rem 0;
		font-size: 0.875rem;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.9);
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.motion-info {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		font-size: 0.8125rem;
	}

	.location {
		font-weight: 500;
		color: rgba(255, 255, 255, 0.85);
	}

	.motion-type {
		color: rgba(255, 255, 255, 0.6);
		text-transform: capitalize;
		font-style: italic;
	}

	.animation-canvas-container {
		margin-top: auto;
		padding: 1.25rem;
		background: linear-gradient(135deg, 
			rgba(255, 255, 255, 0.06) 0%, 
			rgba(255, 255, 255, 0.03) 100%);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 16px;
		display: flex;
		justify-content: center;
		align-items: center;
		backdrop-filter: blur(15px);
		box-shadow: 
			0 4px 16px rgba(0, 0, 0, 0.1),
			inset 0 1px 0 rgba(255, 255, 255, 0.1);
	}

	.hint {
		font-style: italic;
		color: rgba(255, 255, 255, 0.5);
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.animation-controls {
			flex-direction: column;
			align-items: stretch;
			gap: 1rem;
		}

		.beat-info {
			margin-left: 0;
			text-align: center;
		}

		.animation-canvas-container {
			padding: 1rem;
		}

		.panel-content {
			padding: 1rem;
			gap: 1rem;
		}
	}

	/* Custom scrollbar for panel content */
	.panel-content::-webkit-scrollbar {
		width: 8px;
	}

	.panel-content::-webkit-scrollbar-track {
		background: rgba(255, 255, 255, 0.05);
		border-radius: 4px;
	}

	.panel-content::-webkit-scrollbar-thumb {
		background: rgba(255, 255, 255, 0.2);
		border-radius: 4px;
		border: 2px solid transparent;
		background-clip: content-box;
	}

	.panel-content::-webkit-scrollbar-thumb:hover {
		background: rgba(255, 255, 255, 0.3);
		background-clip: content-box;
	}

	/* High contrast mode */
	@media (prefers-contrast: high) {
		.expand-button,
		.toggle-button,
		.close-button {
			border: 2px solid currentColor;
		}

		.animation-panel {
			border-left-color: rgba(255, 255, 255, 0.5);
		}

		.panel-header {
			border-bottom-color: rgba(255, 255, 255, 0.3);
		}
	}

	/* Reduced motion support */
	@media (prefers-reduced-motion: reduce) {
		.animation-panel,
		.expand-button,
		.toggle-button,
		.close-button,
		.control-button,
		.beat-button,
		.motion {
			transition: none;
		}

		.loading-spinner {
			animation: none;
		}
	}

	/* Focus improvements for accessibility */
	.expand-button:focus-visible,
	.toggle-button:focus-visible,
	.close-button:focus-visible,
	.control-button:focus-visible,
	.beat-button:focus-visible {
		outline: 2px solid #818cf8;
		outline-offset: 2px;
	}
</style>
