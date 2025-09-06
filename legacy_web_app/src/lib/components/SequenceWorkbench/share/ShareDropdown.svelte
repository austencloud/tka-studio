<!-- src/lib/components/SequenceWorkbench/ShareDropdown.svelte -->
<script lang="ts">
	import { fly } from 'svelte/transition';
	import { clickOutside } from '$lib/utils/clickOutside';
	import { isWebShareSupported } from '$lib/components/SequenceWorkbench/share/utils/ShareUtils';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { browser } from '$app/environment';

	// Props
	export let onShare: () => void;
	export let onDownload: () => void;
	export let onClose: () => void;

	// Handle close with haptic feedback
	function handleClose() {
		// Provide haptic feedback when closing the dropdown
		if (browser && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('selection');
		}

		onClose();
	}
</script>

<div
	class="share-dropdown"
	transition:fly={{ y: 5, duration: 200 }}
	use:clickOutside={{ callback: onClose }}
>
	<div class="dropdown-header">
		<h3>Share Sequence</h3>
		<button class="close-button" on:click={handleClose} aria-label="Close">
			<i class="fa-solid fa-times"></i>
		</button>
	</div>

	<div class="dropdown-content">
		{#if isWebShareSupported()}
			<button class="share-option" on:click={onShare}>
				<i class="fa-solid fa-share-alt"></i>
				<span>Share</span>
			</button>
		{:else}
			<div class="share-unavailable">
				<i class="fa-solid fa-info-circle"></i>
				<span>Sharing not supported on this device</span>
			</div>
		{/if}

		<button class="share-option" on:click={onDownload}>
			<i class="fa-solid fa-download"></i>
			<span>Download as Image</span>
		</button>
	</div>
</div>

<style>
	.share-dropdown {
		position: relative;
		width: 220px;
		background-color: var(--tkc-button-panel-background, #2a2a2e);
		border-radius: 8px;
		box-shadow:
			0 4px 12px rgba(0, 0, 0, 0.2),
			0 2px 4px rgba(0, 0, 0, 0.1);
		z-index: 50;
		overflow: hidden;
	}

	.dropdown-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 12px 16px;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dropdown-header h3 {
		margin: 0;
		font-size: 14px;
		font-weight: 600;
		color: #ffffff;
	}

	.close-button {
		background: transparent;
		border: none;
		color: rgba(255, 255, 255, 0.6);
		cursor: pointer;
		padding: 4px;
		border-radius: 4px;
		transition: color 0.2s ease;
	}

	.close-button:hover {
		color: #ffffff;
	}

	.dropdown-content {
		padding: 8px 0;
	}

	.share-option {
		display: flex;
		align-items: center;
		width: 100%;
		padding: 10px 16px;
		background: transparent;
		border: none;
		color: #ffffff;
		cursor: pointer;
		text-align: left;
		transition: background-color 0.2s ease;
	}

	.share-option:hover {
		background-color: rgba(255, 255, 255, 0.1);
	}

	.share-option i {
		margin-right: 12px;
		width: 16px;
		text-align: center;
		color: var(--tkc-icon-color-share, #00bcd4);
	}

	.share-option span {
		font-size: 14px;
	}

	.share-unavailable {
		display: flex;
		align-items: center;
		width: 100%;
		padding: 10px 16px;
		background-color: rgba(255, 255, 255, 0.05);
		color: rgba(255, 255, 255, 0.7);
		text-align: left;
		font-style: italic;
		border-left: 3px solid rgba(255, 255, 255, 0.2);
	}

	.share-unavailable i {
		margin-right: 12px;
		width: 16px;
		text-align: center;
		color: rgba(255, 255, 255, 0.5);
	}

	.share-unavailable span {
		font-size: 13px;
	}
</style>
