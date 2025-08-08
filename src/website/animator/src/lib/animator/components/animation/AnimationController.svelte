<script module lang="ts">
	export interface AnimationState {
		isPlaying: boolean;
		speed: number;
		currentBeat: number;
		totalBeats: number;
		sequenceWord: string;
		sequenceAuthor: string;
		shouldLoop: boolean;
	}
</script>

<script lang="ts">
	import type { SequenceData, PropState, SequenceStep } from '../../types/core.js';
	import { SimplifiedAnimationEngine } from '../../core/engine/simplified-animation-engine.js';
	import { AnimatorErrorHandler } from '../../utils/error/error-handler.js';
	import { InputValidator } from '../../utils/validation/input-validator.js';
	import SequenceControlPanel from '../controls/SequenceControlPanel.svelte';

	// Props
	let {
		sequenceData = $bindable(),
		blueProp = $bindable(),
		redProp = $bindable(),
		onSequenceLoad,
		onError,
		onSuccess,
		renderControls = true
	}: {
		sequenceData: SequenceData | null;
		blueProp: PropState;
		redProp: PropState;
		onSequenceLoad?: (_data: SequenceData) => void;
		onError?: (_message: string) => void;
		onSuccess?: (_message: string) => void;
		renderControls?: boolean;
	} = $props();

	// Animation state
	let isPlaying = $state(false);
	let speed = $state(1.0);
	let currentBeat = $state(0);
	let totalBeats = $state(0);
	let sequenceWord = $state('');
	let sequenceAuthor = $state('');
	let shouldLoop = $state(false); // Will be determined automatically

	// Animation frame reference
	let animationFrameId: number | null = null;
	let lastTimestamp: number | null = null;

	// Setup engine
	const engine = new SimplifiedAnimationEngine();

	// Clean up on component destroy
	$effect(() => {
		return () => {
			if (animationFrameId !== null) {
				cancelAnimationFrame(animationFrameId);
			}
		};
	});

	// Handle sequence load
	function handleLoadSequence(data: SequenceData): void {
		try {
			// Validate sequence data first
			const validation = InputValidator.validateSequenceData(data);
			if (!validation.isValid) {
				onError?.(`Invalid sequence data: ${validation.errors.join(', ')}`);
				return;
			}

			// Log warnings if any
			if (validation.warnings.length > 0) {
				console.info('Sequence warnings:', validation.warnings.join(', '));
			}

			// Initialize engine with data
			if (engine.initialize(data)) {
				// Load sequence data
				sequenceData = data;
				const metadata = engine.getMetadata();
				totalBeats = metadata.totalBeats;
				sequenceWord = metadata.word;
				sequenceAuthor = metadata.author;

				// Automatically detect if sequence should loop (ends in start position)
				shouldLoop = detectAutoLoop(data);

				// Reset animation state
				currentBeat = 0;
				isPlaying = false;

				// Update prop states
				updatePropStates();

				onSuccess?.('Sequence loaded successfully!');
				onSequenceLoad?.(data);
			} else {
				const error = AnimatorErrorHandler.handleEngineError(
					new Error('Failed to initialize sequence')
				);
				onError?.(AnimatorErrorHandler.formatForUser(error));
			}
		} catch (err) {
			const error = AnimatorErrorHandler.handleSequenceError(
				err instanceof Error ? err : new Error(String(err))
			);
			onError?.(AnimatorErrorHandler.formatForUser(error));
		}
	}

	// Update prop states from engine
	function updatePropStates(): void {
		blueProp = engine.getBluePropState();
		redProp = engine.getRedPropState();
	}

	// Detect if sequence should automatically loop (ends in start position)
	function detectAutoLoop(data: SequenceData): boolean {
		if (data.length < 3) return false; // Need at least metadata, start, and one step

		const startPosition = data[1] as SequenceStep;
		const lastStep = data[data.length - 1] as SequenceStep;

		// Check if both props end in their start positions
		const blueLoops = startPosition.blue_attributes.start_loc === lastStep.blue_attributes.end_loc;
		const redLoops = startPosition.red_attributes.start_loc === lastStep.red_attributes.end_loc;

		return blueLoops && redLoops;
	}

	// Animation loop
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
		// Animation runs from beat 0 through totalBeats+1 to allow final step to complete
		// For N steps: beat 0 (start) → beat 1-N (steps) → beat N+1 (completion)
		const animationEndBeat = totalBeats + 1;

		if (newBeat > animationEndBeat) {
			if (shouldLoop) {
				// Loop back to start
				currentBeat = 0;
				lastTimestamp = null;

				// Make sure the engine is reset properly for the next loop
				engine.reset();
			} else {
				// Stop at end - hold final frame at totalBeats (not totalBeats+1)
				currentBeat = totalBeats;
				isPlaying = false;
			}
		} else {
			currentBeat = newBeat;
		}

		// Calculate state for current beat
		engine.calculateState(currentBeat);

		// Update props from engine state
		updatePropStates();

		// Request next frame if still playing
		if (isPlaying) {
			animationFrameId = requestAnimationFrame(animationLoop);
		}
	}

	// Handle play/pause
	function handlePlayPause(): void {
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

	// Handle reset
	function handleReset(): void {
		currentBeat = 0;
		isPlaying = false;

		if (animationFrameId !== null) {
			cancelAnimationFrame(animationFrameId);
			animationFrameId = null;
		}

		engine.reset();
		updatePropStates();
	}

	// Handle speed change
	function handleSpeedChange(value: number): void {
		speed = Math.max(0.1, Math.min(3.0, value));
	}

	// Auto-play functionality
	function autoPlay(): void {
		if (sequenceData && totalBeats > 0 && !isPlaying) {
			handlePlayPause();
		}
	}

	// Expose public methods
	export function loadSequence(data: SequenceData): void {
		handleLoadSequence(data);
	}

	export function playSequence(): void {
		autoPlay();
	}

	export function getAnimationState() {
		return {
			isPlaying,
			speed,
			currentBeat,
			totalBeats,
			sequenceWord,
			sequenceAuthor,
			shouldLoop
		};
	}

	export function changeSpeed(value: number): void {
		handleSpeedChange(value);
	}

	export function togglePlayPause(): void {
		handlePlayPause();
	}

	export function resetAnimation(): void {
		handleReset();
	}

	export function jumpToBeat(beatNumber: number): void {
		// Stop any current animation
		isPlaying = false;
		if (animationFrameId !== null) {
			cancelAnimationFrame(animationFrameId);
			animationFrameId = null;
		}

		// Set the current beat
		currentBeat = Math.max(0, Math.min(beatNumber, totalBeats));

		// Calculate state for this specific beat
		engine.calculateState(currentBeat);
		updatePropStates();
	}
</script>

{#if sequenceData && renderControls}
	<SequenceControlPanel
		{isPlaying}
		{speed}
		{currentBeat}
		{totalBeats}
		onPlayPause={handlePlayPause}
		onReset={handleReset}
		onSpeedChange={handleSpeedChange}
	/>
{/if}
