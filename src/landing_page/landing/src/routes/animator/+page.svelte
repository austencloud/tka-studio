<script lang="ts">
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	// Import all animation types and functions
	import type {
		PropState,
		CanvasState,
		MessageType
	} from '$lib/core/animation/types';
	import {
		AnimationEngine,
		processSequenceData,
		loadAllImages,
		render as renderCanvas,
		drawErrorMessage,
		drawLoadingMessage,
		CANVAS_SIZE,
		defaultSequence,
		title,
		description
	} from '$lib/core/animation';

	// Import UI components
	import SequenceInput from '$lib/core/animation/SequenceInput.svelte';
	import AnimationCanvas from '$lib/core/animation/AnimationCanvas.svelte';
	import PlaybackControls from '$lib/core/animation/PlaybackControls.svelte';
	import SpeedControl from '$lib/core/animation/SpeedControl.svelte';
	import BeatControl from '$lib/core/animation/BeatControl.svelte';
	import LoopControl from '$lib/core/animation/LoopControl.svelte';
  	import InfoDisplay from '$lib/core/animation/InfoDisplay.svelte';

	// State using Svelte 5 runes
	let isClient = $state(false);
	let isLoading = $state(true);

	// Prop state
	let bluePropState: PropState = $state({ centerPathAngle: 0, staffRotationAngle: 0, x: 0, y: 0 });
	let redPropState: PropState = $state({ centerPathAngle: 0, staffRotationAngle: 0, x: 0, y: 0 });

	// Canvas state
	let canvasState: CanvasState = $state({
		ctx: null,
		imagesLoaded: false,
		canvasReady: false,
		gridImage: null,
		blueStaffImage: null,
		redStaffImage: null
	});

	// Animation state - will be managed by AnimationEngine
	let animationEngine: AnimationEngine | null = $state<AnimationEngine | null>(null);
	let currentSequence: any = $state(null);

	// Component references
	let sequenceInputComponent: SequenceInput | null = $state(null);
	let canvasElement: HTMLCanvasElement | null = $state(null);

	// Helper functions to safely access animation engine properties
	function getIsPlaying(): boolean {
		return animationEngine?.isPlaying ?? false;
	}

	function getCurrentBeat(): number {
		return animationEngine?.currentBeat ?? 0;
	}

	function getSpeed(): number {
		return animationEngine?.speed ?? 1.0;
	}

	function getContinuousLoop(): boolean {
		return animationEngine?.continuousLoop ?? false;
	}

	function getTotalBeats(): number {
		return animationEngine?.totalBeats ?? 0;
	}

	// Reactive getters for animation state
	const isPlaying: boolean = $derived(getIsPlaying());
	const currentBeat: number = $derived(getCurrentBeat());
	const speed: number = $derived(getSpeed());
	const continuousLoop: boolean = $derived(getContinuousLoop());
	const totalBeats: number = $derived(getTotalBeats());

	// Handle canvas ready callback
	function handleCanvasReady(canvas: HTMLCanvasElement) {
		console.log('🎯 CANVAS: Canvas element received from component', canvas);
		canvasElement = canvas;
	}

	// Initialize canvas when element is available
	$effect(() => {
		if (canvasElement && !canvasState.ctx && !isLoading) {
			console.log('🎯 EFFECT: Canvas element detected, starting initialization...');

			setTimeout(() => {
				console.log('🎯 CANVAS: Getting 2D context...');
				if (canvasElement) {
					canvasState.ctx = canvasElement.getContext('2d');
					if (canvasState.ctx) {
						canvasState.canvasReady = true;
						console.log('✅ CANVAS: Context created successfully!');

						// Test drawing to verify canvas works
						try {
							drawLoadingMessage(canvasState.ctx);
							console.log('✅ CANVAS: Test pattern drawn successfully!');
						} catch (error) {
							console.error('❌ CANVAS: Error drawing test pattern:', error);
						}

						loadImages();
					} else {
						console.error('❌ CANVAS: Failed to get 2D context');
						showMessage('error', 'Failed to initialize canvas. Please refresh the page.');
					}
				}
			}, 100);
		}
	});

	// Handle client-side hydration properly to avoid SSR issues
	$effect(() => {
		if (browser) {
			isClient = true;
			setTimeout(() => {
				isLoading = false;
			}, 100);
		}
	});

	// Initialize animation engine when canvas is ready
	$effect(() => {
		if (canvasState.ctx && canvasState.imagesLoaded && !animationEngine) {
			console.log('🎬 EFFECT: Initializing animation engine...');
			animationEngine = new AnimationEngine(
				bluePropState,
				redPropState,
				handleRender,
				handleUIUpdate,
				handleAnimationEnd
			);

			// Load default sequence
			loadDefaultSequence();
		}
	});

	// Image loading
	async function loadImages() {
		try {
			console.log('🖼️ IMAGES: Starting to load images...');
			const images = await loadAllImages();

			canvasState.gridImage = images.gridImage;
			canvasState.blueStaffImage = images.blueStaffImage;
			canvasState.redStaffImage = images.redStaffImage;
			canvasState.imagesLoaded = true;

			console.log('✅ IMAGES: All images loaded successfully!');
			handleRender(); // Initial render
		} catch (error) {
			console.error('❌ IMAGES: Failed to load images:', error);
			showMessage('error', 'Failed to load animation images. Please refresh the page.');
			if (canvasState.ctx) {
				drawErrorMessage(canvasState.ctx, 'Error loading images. Please refresh the page.');
			}
		}
	}

	// Animation callbacks
	function handleRender() {
		renderCanvas(canvasState, bluePropState, redPropState);
	}

	function handleUIUpdate() {
		// UI updates are handled reactively through derived state
	}

	function handleAnimationEnd() {
		// Optional: Handle animation end if needed
	}

	// Load default sequence
	function loadDefaultSequence() {
		if (!animationEngine) return;

		try {
			currentSequence = defaultSequence;
			const { parsedSteps, totalBeats } = processSequenceData(currentSequence);
			animationEngine.setParsedSteps(parsedSteps, totalBeats);
			animationEngine.initializeState();
			handleRender();
			console.log('Default sequence loaded successfully');
		} catch (e: any) {
			console.error('Error processing default sequence:', e);
			showMessage('error', `Failed to load default sequence: ${e.message}`);
		}
	}

	// Control handlers
	function handlePlayPause() {
		if (!animationEngine) return;
		if (isPlaying) {
			animationEngine.pause();
		} else {
			animationEngine.play();
		}
	}

	function handleReset() {
		if (!animationEngine) return;
		animationEngine.reset();
	}

	function handleSpeedChange(newSpeed: number) {
		if (!animationEngine) return;
		animationEngine.setSpeed(newSpeed);
	}

	function handleBeatChange(newBeat: number) {
		if (!animationEngine) return;
		if (isPlaying) animationEngine.pause();
		animationEngine.updateBeat(newBeat, true);
	}

	function handleLoopChange(loop: boolean) {
		if (!animationEngine) return;
		animationEngine.setContinuousLoop(loop);
	}

	// Sequence loading
	function handleSequenceLoad(jsonString: string) {
		if (!animationEngine || !sequenceInputComponent) return;

		try {
			const pastedData = JSON.parse(jsonString);
			animationEngine.pause();
			currentSequence = pastedData;
			const { parsedSteps, totalBeats } = processSequenceData(currentSequence);
			animationEngine.setParsedSteps(parsedSteps, totalBeats);
			animationEngine.updateBeat(0, true);
			animationEngine.initializeState();
			handleRender();
			sequenceInputComponent.showLoadMessage(
				'success',
				`Sequence "${currentSequence[0]?.word || 'Untitled'}" loaded successfully (${totalBeats} beats).`
			);
		} catch (e: any) {
			console.error('Failed to parse or process sequence:', e);
			sequenceInputComponent.showLoadMessage('error', `Error loading sequence: ${e.message}`);
		}
	}

	function showMessage(type: MessageType, text: string) {
		console.log('Showing message:', type, text);
		if (sequenceInputComponent) {
			sequenceInputComponent.showLoadMessage(type, text);
		}
	}
</script>

<svelte:head>
	<title>{title}</title>
	<meta name="description" content={description} />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
</svelte:head>

<main class="animator-page">
	{#if !isClient}
		<div class="loading">
			<div class="loading-spinner"></div>
			<p>Loading animator...</p>
		</div>
	{:else if isLoading}
		<div class="loading">
			<div class="loading-spinner"></div>
			<p>Initializing pictograph animator...</p>
		</div>
	{:else}
		<div class="animator-container">
			<header class="animator-header">
				<h1>Step-by-Step Animator</h1>
				<p>Professional flow art sequence visualization</p>
			</header>

			<div class="animator-content">
				<SequenceInput
					bind:this={sequenceInputComponent}
					onSequenceLoad={handleSequenceLoad}
				/>

				<AnimationCanvas
					{canvasState}
					canvasSize={CANVAS_SIZE}
					onCanvasReady={handleCanvasReady}
				/>

				<div class="controls">
					<PlaybackControls
						{isPlaying}
						onPlayPause={handlePlayPause}
						onReset={handleReset}
					/>

					<SpeedControl
						{speed}
						onSpeedChange={handleSpeedChange}
					/>

					<BeatControl
						{currentBeat}
						{totalBeats}
						onBeatChange={handleBeatChange}
					/>

					<LoopControl
						{continuousLoop}
						onLoopChange={handleLoopChange}
					/>
				</div>

				<InfoDisplay
					{currentBeat}
					{totalBeats}
				/>

				<!-- Debug Panel - Remove this once working -->
				<div class="debug-panel">
					<h4>Debug Info</h4>
					<p>Canvas Ready: <span class:text-green={canvasState.canvasReady} class:text-red={!canvasState.canvasReady}>{canvasState.canvasReady ? 'Yes' : 'No'}</span></p>
					<p>Images Loaded: <span class:text-green={canvasState.imagesLoaded} class:text-red={!canvasState.imagesLoaded}>{canvasState.imagesLoaded ? 'Yes' : 'No'}</span></p>
					<p>Canvas Context: <span class:text-green={!!canvasState.ctx} class:text-red={!canvasState.ctx}>{canvasState.ctx ? 'Available' : 'Missing'}</span></p>
					<p>Total Beats: <span>{totalBeats}</span></p>
					<p>Sequence Loaded: <span class:text-green={!!currentSequence} class:text-red={!currentSequence}>{currentSequence ? 'Yes' : 'No'}</span></p>
					<p>Animation Playing: <span class:text-green={isPlaying} class:text-red={!isPlaying}>{isPlaying ? 'Yes' : 'No'}</span></p>
					<p>Current Beat: <span>{currentBeat.toFixed(2)}</span></p>
				</div>
			</div>
		</div>
	{/if}
</main>

<style>
	.animator-page {
		width: 100%;
		min-height: 100vh;
		background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 50%, #581c87 100%);
		display: flex;
		flex-direction: column;
		font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
	}

	.loading {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		min-height: 60vh;
		color: white;
		text-align: center;
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 4px solid rgba(255, 255, 255, 0.3);
		border-radius: 50%;
		border-top-color: white;
		animation: spin 1s ease-in-out infinite;
		margin-bottom: 1rem;
	}

	@keyframes spin {
		to { transform: rotate(360deg); }
	}

	.animator-container {
		flex: 1;
		max-width: 1000px;
		margin: 0 auto;
		padding: 2rem;
		color: white;
	}

	.animator-header {
		text-align: center;
		margin-bottom: 2rem;
	}

	.animator-header h1 {
		font-size: 2.5rem;
		margin: 0 0 0.5rem 0;
		font-weight: 700;
		background: linear-gradient(45deg, #fff, #a8edea);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.animator-header p {
		font-size: 1.1rem;
		opacity: 0.9;
		margin: 0;
		font-weight: 500;
	}

	.animator-content {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		align-items: center;
	}

	.controls {
		background: rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 1rem;
		padding: 1.5rem;
		display: flex;
		flex-wrap: wrap;
		gap: 1.5rem;
		align-items: center;
		justify-content: center;
		width: 100%;
		max-width: 600px;
	}

	.debug-panel {
		background: rgba(0, 0, 0, 0.8);
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 0.5rem;
		padding: 1rem;
		font-size: 0.75rem;
		color: white;
		max-width: 300px;
		margin-top: 1rem;
	}

	.debug-panel h4 {
		margin: 0 0 0.5rem 0;
		font-size: 0.875rem;
		color: #fbbf24;
	}

	.debug-panel p {
		margin: 0.25rem 0;
		font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
	}

	.text-green {
		color: #10b981 !important;
	}

	.text-red {
		color: #ef4444 !important;
	}

	@media (max-width: 768px) {
		.animator-container {
			padding: 1rem;
		}

		.animator-header h1 {
			font-size: 2rem;
		}

		.controls {
			flex-direction: column;
			gap: 1rem;
		}
	}

	@media (max-width: 480px) {
		.animator-header h1 {
			font-size: 1.75rem;
		}
	}
</style>
