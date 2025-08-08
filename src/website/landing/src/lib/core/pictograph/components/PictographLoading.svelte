<!--
  PictographLoading Component

  Shows loading state for pictograph components.
-->
<script lang="ts">
	import { fade } from 'svelte/transition';

	export let status = 'loading';
	export let progress = 0;
	export let debug = false;
	export let animationDuration = 300;

	$: statusText = getStatusText(status);

	function getStatusText(status: string): string {
		switch (status) {
			case 'initializing':
				return 'Initializing...';
			case 'grid_loading':
				return 'Loading grid...';
			case 'props_loading':
				return 'Loading props...';
			case 'arrows_loading':
				return 'Loading arrows...';
			default:
				return 'Loading...';
		}
	}
</script>

<div class="pictograph-loading" class:debug transition:fade={{ duration: animationDuration }}>
	<div class="loading-spinner">
		<svg viewBox="0 0 950 950" xmlns="http://www.w3.org/2000/svg">
			<circle cx="475" cy="475" r="40" fill="none" stroke="#e2e8f0" stroke-width="8" />
			<path
				d="M475 435 A40 40 0 0 1 515 475"
				fill="none"
				stroke="#4299e1"
				stroke-width="8"
				stroke-linecap="round"
			>
				<animateTransform
					attributeName="transform"
					type="rotate"
					from="0 475 475"
					to="360 475 475"
					dur="1s"
					repeatCount="indefinite"
				/>
			</path>
		</svg>
	</div>

	{#if debug}
		<div class="loading-info">
			<div class="status">{statusText}</div>
			<div class="progress">{Math.round(progress)}%</div>
		</div>
	{/if}
</div>

<style>
	.pictograph-loading {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
		background: rgba(255, 255, 255, 0.9);
		border-radius: 8px;
	}

	.loading-spinner {
		width: 60px;
		height: 60px;
	}

	.loading-spinner svg {
		width: 100%;
		height: 100%;
	}

	.loading-info {
		margin-top: 12px;
		text-align: center;
		font-size: 12px;
		color: #64748b;
	}

	.status {
		margin-bottom: 4px;
	}

	.progress {
		font-weight: 600;
		color: #4299e1;
	}

	.pictograph-loading.debug {
		border: 2px dashed #fbbf24;
		background: rgba(254, 243, 199, 0.9);
	}
</style>
