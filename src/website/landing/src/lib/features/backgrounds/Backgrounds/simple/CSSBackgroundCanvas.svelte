<!-- src/lib/components/Backgrounds/simple/CSSBackgroundCanvas.svelte -->
<!-- Pure CSS animated background - ultimate fallback with zero JavaScript -->
<!-- Completely eliminates any potential for Svelte reactive loops -->

<script lang="ts">
	import type { BackgroundType, QualityLevel } from './SimpleBackgroundSystem.svelte.ts';

	// Props using Svelte 5 runes
	const props = $props<{
		backgroundType?: BackgroundType;
		quality?: QualityLevel;
		appIsLoading?: boolean;
	}>();

	// Reactive background class based on type
	const backgroundClass = $derived(`css-background css-background--${props.backgroundType || 'nightSky'}`);
	const qualityClass = $derived(`css-background--${props.quality || 'medium'}`);
</script>

<div class="{backgroundClass} {qualityClass}">
	<!-- Animated particles using pure CSS -->
	{#if props.backgroundType === 'snowfall'}
		<!-- Snowfall particles -->
		{#each Array(20) as _, i}
			<div class="snowflake" style="--delay: {i * 0.5}s; --duration: {3 + Math.random() * 2}s; --size: {2 + Math.random() * 4}px;"></div>
		{/each}
	{:else if props.backgroundType === 'nightSky'}
		<!-- Twinkling stars -->
		{#each Array(30) as _, i}
			<div class="star" style="--delay: {i * 0.3}s; --x: {Math.random() * 100}%; --y: {Math.random() * 100}%; --size: {1 + Math.random() * 2}px;"></div>
		{/each}
	{:else if props.backgroundType === 'deepOcean'}
		<!-- Floating bubbles -->
		{#each Array(15) as _, i}
			<div class="bubble" style="--delay: {i * 0.7}s; --duration: {4 + Math.random() * 3}s; --size: {3 + Math.random() * 5}px;"></div>
		{/each}
	{/if}
</div>

<style>
	.css-background {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: -1;
		pointer-events: none;
		overflow: hidden;
	}

	/* Background gradients */
	.css-background--snowfall {
		background: linear-gradient(180deg, #1a2332 0%, #2d3748 50%, #4a5568 100%);
	}

	.css-background--nightSky {
		background: linear-gradient(180deg, #0A0E2C 0%, #1A2151 30%, #2A3270 60%, #4A5490 100%);
	}

	.css-background--deepOcean {
		background: linear-gradient(180deg, #001122 0%, #002244 30%, #003366 70%, #004488 100%);
	}

	.css-background--static {
		background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
	}

	/* Snowfall particles */
	.snowflake {
		position: absolute;
		top: -10px;
		left: var(--x, 50%);
		width: var(--size, 4px);
		height: var(--size, 4px);
		background: rgba(255, 255, 255, 0.8);
		border-radius: 50%;
		animation: snowfall var(--duration, 4s) linear infinite;
		animation-delay: var(--delay, 0s);
		--x: calc(var(--i, 0) * 5%);
	}

	@keyframes snowfall {
		0% {
			transform: translateY(-10px) translateX(0px);
			opacity: 0;
		}
		10% {
			opacity: 1;
		}
		90% {
			opacity: 1;
		}
		100% {
			transform: translateY(100vh) translateX(20px);
			opacity: 0;
		}
	}

	/* Twinkling stars */
	.star {
		position: absolute;
		top: var(--y, 50%);
		left: var(--x, 50%);
		width: var(--size, 2px);
		height: var(--size, 2px);
		background: rgba(255, 255, 255, 0.9);
		border-radius: 50%;
		animation: twinkle 2s ease-in-out infinite;
		animation-delay: var(--delay, 0s);
	}

	@keyframes twinkle {
		0%, 100% {
			opacity: 0.3;
			transform: scale(1);
		}
		50% {
			opacity: 1;
			transform: scale(1.2);
		}
	}

	/* Ocean bubbles */
	.bubble {
		position: absolute;
		bottom: -10px;
		left: var(--x, 50%);
		width: var(--size, 6px);
		height: var(--size, 6px);
		background: rgba(135, 206, 235, 0.4);
		border: 1px solid rgba(135, 206, 235, 0.6);
		border-radius: 50%;
		animation: bubble-rise var(--duration, 5s) linear infinite;
		animation-delay: var(--delay, 0s);
		--x: calc(var(--i, 0) * 7%);
	}

	@keyframes bubble-rise {
		0% {
			transform: translateY(10px) translateX(0px);
			opacity: 0;
		}
		10% {
			opacity: 0.6;
		}
		90% {
			opacity: 0.6;
		}
		100% {
			transform: translateY(-100vh) translateX(-15px);
			opacity: 0;
		}
	}

	/* Quality level adjustments */
	.css-background--low .snowflake:nth-child(n+11),
	.css-background--low .star:nth-child(n+16),
	.css-background--low .bubble:nth-child(n+8) {
		display: none;
	}

	.css-background--medium .snowflake:nth-child(n+16),
	.css-background--medium .star:nth-child(n+21),
	.css-background--medium .bubble:nth-child(n+11) {
		display: none;
	}

	/* Reduced motion support */
	@media (prefers-reduced-motion: reduce) {
		.snowflake,
		.star,
		.bubble {
			animation-duration: 10s;
			animation-iteration-count: 1;
		}

		.star {
			animation: none;
			opacity: 0.6;
		}
	}

	/* Performance optimizations */
	.snowflake,
	.star,
	.bubble {
		will-change: transform, opacity;
		backface-visibility: hidden;
		transform: translateZ(0);
	}
</style>
