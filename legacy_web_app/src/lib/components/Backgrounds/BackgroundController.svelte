<script lang="ts">
	import { onMount, onDestroy, createEventDispatcher } from 'svelte';
	import { backgroundContainer } from '$lib/state/stores/background/BackgroundContainer';
	import { useContainer } from '$lib/state/core/svelte5-integration.svelte';
	import { getService } from '$lib/core/di/serviceContext';
	import { SERVICE_TOKENS } from '$lib/core/di/ServiceTokens';
	import type { BackgroundService } from '$lib/core/services/BackgroundService';
	import { ErrorSeverity, type ErrorHandler } from '$lib/core/services/ErrorHandling';
	import type {
		BackgroundSystem,
		BackgroundType,
		QualityLevel,
		Dimensions
	} from '$lib/components/Backgrounds/types/types';

	// Use the background container with Svelte 5 runes
	const background = useContainer(backgroundContainer);

	// Props using Svelte 5 runes
	const dimensions = $props() as Dimensions;
	dimensions.width = dimensions.width || 0;
	dimensions.height = dimensions.height || 0;

	// Event dispatcher
	const dispatch = createEventDispatcher<{
		ready: undefined;
		error: { message: string };
		performanceReport: { fps: number };
	}>();

	// Services (initialized in onMount)
	let backgroundService: BackgroundService;
	let errorHandler: ErrorHandler;

	// Component state
	let backgroundSystem: BackgroundSystem | null = null;
	let canvas: HTMLCanvasElement;
	let animationFrameId: number | null = null;
	let isActive = $state(true);

	// Reactive updates based on container state
	$effect(() => {
		if (backgroundSystem && background.quality) {
			backgroundSystem.setQuality(background.quality);
		}
	});

	$effect(() => {
		if (backgroundSystem && dimensions.width && dimensions.height) {
			updateDimensions(dimensions);
		}
	});

	$effect(() => {
		if (backgroundSystem && !background.isVisible) {
			stopAnimationLoop();
		} else if (backgroundSystem && background.isVisible && !animationFrameId) {
			startAnimationLoop();
		}
	});

	onMount(async () => {
		try {
			// Get services from DI container
			backgroundService = getService<BackgroundService>(SERVICE_TOKENS.BACKGROUND_SERVICE);
			errorHandler = getService<ErrorHandler>(SERVICE_TOKENS.ERROR_HANDLER);

			// Load background
			await loadBackground(background.currentBackground);

			// Set initial dimensions if provided
			if (dimensions.width > 0 && dimensions.height > 0) {
				backgroundService.updateDimensions(dimensions);
			}

			// Start animation loop if visible
			if (background.isVisible) {
				startAnimationLoop();
			}

			// Update ready state
			backgroundContainer.setReady(true);
			dispatch('ready');
		} catch (error) {
			handleError('Failed to initialize background', error);
		}
	});

	onDestroy(() => {
		stopAnimationLoop();
		if (backgroundSystem) {
			backgroundSystem.cleanup();
			backgroundSystem = null;
		}
	});

	// Watch for background type changes
	$effect(() => {
		if (backgroundSystem && background.currentBackground) {
			loadBackground(background.currentBackground);
		}
	});

	async function loadBackground(type: BackgroundType): Promise<void> {
		try {
			// Set ready state to false while loading
			backgroundContainer.setReady(false);

			// Clean up previous background if exists
			if (backgroundSystem) {
				backgroundSystem.cleanup();
			}

			// Load new background
			backgroundSystem = await backgroundService.loadBackground(type);

			// Set ready state to true when loaded
			backgroundContainer.setReady(true);
		} catch (error) {
			handleError(`Failed to load background: ${type}`, error);
		}
	}

	function updateDimensions(newDimensions: Dimensions): void {
		if (backgroundService) {
			backgroundService.updateDimensions(newDimensions);
		}
	}

	function startAnimationLoop(): void {
		if (!backgroundSystem || !canvas) return;

		const ctx = canvas.getContext('2d');
		if (!ctx) {
			handleError('Failed to get canvas context', null);
			return;
		}

		const animate = () => {
			if (!backgroundSystem || !isActive || !background.isVisible) return;

			// Clear canvas
			ctx.clearRect(0, 0, dimensions.width, dimensions.height);

			// Update and draw
			backgroundSystem.update(dimensions);
			backgroundSystem.draw(ctx, dimensions);

			// Report performance if available
			if (backgroundSystem.getMetrics) {
				const metrics = backgroundSystem.getMetrics();
				backgroundContainer.updatePerformanceMetrics(metrics);
				dispatch('performanceReport', { fps: metrics.fps });
			}

			// Schedule next frame
			animationFrameId = requestAnimationFrame(animate);
		};

		// Start the loop
		animationFrameId = requestAnimationFrame(animate);
	}

	function stopAnimationLoop(): void {
		if (animationFrameId) {
			cancelAnimationFrame(animationFrameId);
			animationFrameId = null;
		}
	}

	function handleError(message: string, error: any): void {
		const errorObj = error instanceof Error ? error : new Error(message);

		errorHandler.log({
			source: 'BackgroundController',
			message,
			severity: ErrorSeverity.ERROR,
			context: { error }
		});

		backgroundContainer.setError(errorObj);
		dispatch('error', { message });
	}
</script>

<canvas
	bind:this={canvas}
	width={dimensions.width || 300}
	height={dimensions.height || 150}
	class="background-canvas"
	class:hidden={!background.isVisible}
></canvas>

<style>
	.background-canvas {
		display: block;
		width: 100%;
		height: 100%;
		transition: opacity 0.3s ease;
	}

	.hidden {
		opacity: 0;
	}
</style>
