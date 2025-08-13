<!--
Animation Panel - Main Container

Refactored into smaller sub-components for better maintainability.
Handles data loading, animation engine, and state management.
-->
<script lang="ts">
	import { onDestroy } from 'svelte';
	import type { BrowseSequenceMetadata } from '$lib/domain/browse';
	import { resolve } from '$lib/services/bootstrap';
	import type { ISequenceService } from '$lib/services/interfaces';
	import { StandalonePortedEngine, AnimatorCanvas, ensureStandaloneFormat } from '$lib/animator';
	import type { PropState } from '$lib/animator';
	import type { PanelStateManager } from '$lib/state/panel-state.svelte';

	// Sub-components
	import AnimationPanelHeader from './animation/AnimationPanelHeader.svelte';
	import AnimationStates from './animation/AnimationStates.svelte';
	import SequenceInfo from './animation/SequenceInfo.svelte';
	import AnimationControls from './animation/AnimationControls.svelte';
	import BeatSelector from './animation/BeatSelector.svelte';
	import CurrentBeatDisplay from './animation/CurrentBeatDisplay.svelte';

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
	<AnimationPanelHeader 
		{isCollapsed}
		onToggle={handleToggle}
		onClose={handleClose}
	/>

	<!-- Panel Content -->
	{#if !isCollapsed}
		<div class="panel-content">
			<!-- Loading/Error/Empty States -->
			<AnimationStates 
				{loading}
				{error}
				hasSequence={!!sequence}
				onRetry={loadSequenceData}
			/>

			<!-- Sequence Content -->
			{#if sequenceData && !loading && !error}
				<SequenceInfo {sequenceData} />

				<AnimationControls
					{isPlaying}
					{speed}
					{currentBeat}
					totalBeats={totalBeats || sequenceData.beats?.length || 0}
					onPlay={handlePlay}
					onStop={handleStop}
					onSpeedChange={handleSpeedChange}
				/>

				<BeatSelector
					beats={sequenceData.beats}
					{currentBeat}
					onBeatChange={handleBeatChange}
				/>

				<CurrentBeatDisplay
					{currentBeat}
					{sequenceData}
				/>

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

	/* Responsive design */
	@media (max-width: 768px) {
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
		.animation-panel {
			border-left-color: rgba(255, 255, 255, 0.5);
		}
	}

	/* Reduced motion support */
	@media (prefers-reduced-motion: reduce) {
		.animation-panel {
			transition: none;
		}
	}
</style>
