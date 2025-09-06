<!-- src/lib/components/objects/Arrow/Arrow.svelte -->
<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import type { ArrowData } from './ArrowData';
	import type { ArrowSvgData } from '../../SvgManager/ArrowSvgData';
	import { ArrowSvgLoader } from './services/ArrowSvgLoader';
	import SvgManager from '../../SvgManager/SvgManager';
	import type { Motion } from '../Motion/Motion';
	import ArrowRotAngleManager from './ArrowRotAngleManager';
	import ArrowSvgMirrorManager from './ArrowSvgMirrorManager';
	import type { PictographService } from '$lib/components/Pictograph/PictographService';
	import type { PictographData } from '$lib/types/PictographData';
	import { sequenceStore } from '$lib/state/stores/sequenceStore';
	import { derived } from 'svelte/store';

	// Props - we support both direct arrowData and store-based approach
	export let arrowData: ArrowData | undefined = undefined;
	export let beatId: string | undefined = undefined;
	export let color: 'red' | 'blue' | undefined = undefined;
	export let motion: Motion | null = null;
	export let pictographData: PictographData | null = null;
	export let pictographService: PictographService | null = null;
	export let loadTimeoutMs = 1000; // Configurable timeout
	// Animation duration is passed from parent but not used directly in this component
	export const animationDuration = 200;

	// Get arrow data from the sequence store if beatId and color are provided
	const arrowDataFromStore = derived(sequenceStore, ($sequenceStore) => {
		if (!beatId || !color) return null;

		const beat = $sequenceStore.beats.find((b) => b.id === beatId);
		if (!beat) return null;

		return color === 'red' ? beat.redArrowData : beat.blueArrowData;
	});

	// Use either the arrow data from store or the directly provided arrow data
	$: effectiveArrowData = $arrowDataFromStore || arrowData;

	// Component state
	let svgData: ArrowSvgData | null = null;
	let transform = '';
	let isLoaded = false;
	let hasErrored = false;
	let loadTimeout: NodeJS.Timeout;
	let rotAngleManager: ArrowRotAngleManager | null = null;

	// Services
	const dispatch = createEventDispatcher();
	const svgManager = new SvgManager();
	const svgLoader = new ArrowSvgLoader(svgManager);

	// Create mirror manager only when we have arrow data
	$: mirrorManager = effectiveArrowData ? new ArrowSvgMirrorManager(effectiveArrowData) : null;

	// Initialize the rotation angle manager when pictograph data is available
	$: if (pictographData) {
		rotAngleManager = new ArrowRotAngleManager(pictographData, pictographService || undefined);
	}

	// Update mirror state whenever motion data or arrow data changes
	$: if (effectiveArrowData && mirrorManager) {
		mirrorManager.updateMirror();
	}

	// Calculate rotation angle (memoized)
	$: rotationAngle = getRotationAngle();

	// Transform calculation (memoized)
	$: if (svgData && effectiveArrowData?.coords) {
		// Apply transformations in the correct order
		const mirrorTransform = effectiveArrowData.svgMirrored ? 'scale(-1, 1)' : '';

		transform = `
			translate(${effectiveArrowData.coords.x}, ${effectiveArrowData.coords.y})
			rotate(${rotationAngle})
			${mirrorTransform}
		`.trim();
	}

	/**
	 * Helper function to detect mobile devices
	 */
	function isMobile(): boolean {
		return (
			typeof window !== 'undefined' &&
			(window.innerWidth <= 768 ||
				/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent))
		);
	}

	/**
	 * Simple in-memory component-level cache for SVG data
	 */
	const svgDataCache = new Map<string, ArrowSvgData>();

	/**
	 * Get cached SVG data if available
	 */
	function getCachedSvgData(key: string): ArrowSvgData | undefined {
		return svgDataCache.get(key);
	}

	/**
	 * Cache SVG data for future use
	 */
	function cacheSvgData(key: string, data: ArrowSvgData): void {
		svgDataCache.set(key, data);
		// Limit cache size to prevent memory issues
		if (svgDataCache.size > 50) {
			const firstKey = svgDataCache.keys().next().value;
			if (firstKey) {
				svgDataCache.delete(firstKey);
			}
		}
	}

	/**
	 * Loads the arrow SVG with error handling and timeout
	 */
	async function loadArrowSvg() {
		try {
			// Safety check
			if (!effectiveArrowData) {
				throw new Error('No arrow data available');
			}

			// Adjust timeout for mobile devices
			const timeoutDuration = isMobile() ? loadTimeoutMs * 2 : loadTimeoutMs;

			// Set safety timeout
			loadTimeout = setTimeout(() => {
				if (!isLoaded) {
					// Use less verbose logging in production
					if (import.meta.env.DEV) {
						console.warn(`Arrow loading timed out after ${timeoutDuration}ms`);
					}
					isLoaded = true;
					dispatch('loaded', { timeout: true });
				}
			}, timeoutDuration);

			// Update mirror state before loading SVG
			if (mirrorManager) {
				mirrorManager.updateMirror();
			}

			// Check component-level cache first
			const cacheKey = `arrow-${effectiveArrowData.motionType}-${effectiveArrowData.startOri}-${effectiveArrowData.turns}-${effectiveArrowData.color}-${effectiveArrowData.svgMirrored}`;
			const cachedData = getCachedSvgData(cacheKey);

			if (cachedData) {
				// Use cached data
				svgData = cachedData;
				clearTimeout(loadTimeout);
				isLoaded = true;
				dispatch('loaded');
				return;
			}

			// Load the SVG with current configuration
			const result = await svgLoader.loadSvg(
				effectiveArrowData.motionType,
				effectiveArrowData.startOri,
				effectiveArrowData.turns,
				effectiveArrowData.color,
				effectiveArrowData.svgMirrored
			);

			// Update state and notify
			svgData = result.svgData;

			// Cache the result for future use
			cacheSvgData(cacheKey, svgData);

			clearTimeout(loadTimeout);
			isLoaded = true;
			dispatch('loaded');
		} catch (error) {
			handleLoadError(error);
		}
	}

	/**
	 * Handles SVG loading errors with fallback
	 */
	function handleLoadError(error: unknown) {
		// Minimal logging in production
		if (import.meta.env.DEV) {
			console.error('Arrow load error:', error);
		} else {
			console.error('Arrow load error: ' + ((error as Error)?.message || 'Unknown error'));
		}

		hasErrored = true;
		svgData = svgLoader.getFallbackSvgData();
		clearTimeout(loadTimeout);
		isLoaded = true;
		dispatch('loaded', { error: true });
		dispatch('error', {
			message: (error as Error)?.message || 'Unknown error',
			component: 'Arrow',
			color: effectiveArrowData?.color || 'unknown'
		});
	}

	/**
	 * Calculates the arrow rotation angle using the manager
	 */
	function getRotationAngle(): number {
		if (motion && rotAngleManager && effectiveArrowData) {
			// Use the rotation angle manager directly
			return rotAngleManager.calculateRotationAngle(
				motion,
				effectiveArrowData.loc,
				effectiveArrowData.svgMirrored
			);
		}
		// Fall back to the arrow data's rotation angle
		return effectiveArrowData?.rotAngle || 0;
	}

	// Lifecycle hooks
	onMount(() => {
		if (effectiveArrowData?.motionType) {
			loadArrowSvg();
		} else {
			isLoaded = true;
			dispatch('loaded', { error: true });
		}

		// Cleanup
		return () => clearTimeout(loadTimeout);
	});

	// Reactive loading
	$: {
		if (effectiveArrowData?.motionType && !isLoaded && !hasErrored) {
			loadArrowSvg();
		}
	}
</script>

{#if svgData && isLoaded && effectiveArrowData}
	<g
		{transform}
		data-testid="arrow-{effectiveArrowData.color}"
		data-motion-type={effectiveArrowData.motionType}
		data-mirrored={effectiveArrowData.svgMirrored ? 'true' : 'false'}
		data-loc={effectiveArrowData.loc}
		data-rot-angle={rotationAngle}
	>
		<image
			href={svgData.imageSrc}
			width={svgData.viewBox.width}
			height={svgData.viewBox.height}
			x={-svgData.center.x}
			y={-svgData.center.y}
			aria-label="Arrow showing {effectiveArrowData.motionType} motion in {effectiveArrowData.color} direction"
			role="img"
			on:load={() => dispatch('imageLoaded')}
			on:error={() => dispatch('error', { message: 'Image failed to load' })}
		/>
	</g>
{/if}
