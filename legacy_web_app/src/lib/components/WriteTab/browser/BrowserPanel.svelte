<script lang="ts">
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import ThumbnailBox from './ThumbnailBox.svelte';
	import { uiStore } from '../stores/uiStore';

	// Mock data for favorite sequences - in a real implementation, this would come from a store
	let favorites: { id: string; word: string; thumbnails: string[] }[] = [];
	let isLoading = true;

	onMount(async () => {
		// Simulate loading favorites
		await new Promise((resolve) => setTimeout(resolve, 500));

		// Mock data - in a real implementation, this would be loaded from a service
		favorites = [
			{
				id: '1',
				word: 'Butterfly',
				thumbnails: ['/images/sequences/butterfly.png']
			},
			{
				id: '2',
				word: 'Weave',
				thumbnails: ['/images/sequences/weave.png']
			},
			{
				id: '3',
				word: 'Cascade',
				thumbnails: ['/images/sequences/cascade.png']
			},
			{
				id: '4',
				word: 'Fountain',
				thumbnails: ['/images/sequences/fountain.png']
			}
		];

		isLoading = false;
	});
</script>

<div
	class="browser-panel"
	transition:fade={{ duration: 200 }}
	style="width: {$uiStore.browserPanelWidth}px;"
>
	<div class="browser-header">
		<h2 class="text-xl font-semibold">Sequence Browser</h2>
		<button
			class="close-button"
			on:click={() => uiStore.setBrowserPanelOpen(false)}
			aria-label="Close browser panel"
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				width="24"
				height="24"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			>
				<line x1="18" y1="6" x2="6" y2="18"></line>
				<line x1="6" y1="6" x2="18" y2="18"></line>
			</svg>
		</button>
	</div>

	<div class="browser-content">
		{#if isLoading}
			<div class="loading-state">
				<div class="spinner"></div>
				<p>Loading favorites...</p>
			</div>
		{:else if favorites.length === 0}
			<div class="empty-state">
				<p>No favorite sequences found.</p>
				<p>Add favorites from the Browse tab.</p>
			</div>
		{:else}
			<div class="thumbnail-grid">
				{#each favorites as favorite (favorite.id)}
					<ThumbnailBox word={favorite.word} thumbnails={favorite.thumbnails} />
				{/each}
			</div>
		{/if}
	</div>
</div>

<style>
	.browser-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		background-color: #1e1e1e;
		color: #e0e0e0;
		border-left: 1px solid #333;
		position: relative; /* For positioning the resize handle */
		min-width: 200px;
		max-width: 1200px;
	}

	.browser-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem;
		border-bottom: 1px solid #333;
	}

	.close-button {
		background: none;
		border: none;
		color: #999;
		cursor: pointer;
		padding: 0.25rem;
		border-radius: 4px;
		transition:
			color 0.2s,
			background-color 0.2s;
	}

	.close-button:hover {
		color: #fff;
		background-color: rgba(255, 255, 255, 0.1);
	}

	.browser-content {
		flex: 1;
		overflow-y: auto;
		padding: 1rem;
	}

	.thumbnail-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr); /* Always show exactly 2 columns */
		gap: 1rem;
	}

	.loading-state,
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
		text-align: center;
		color: #999;
	}

	.spinner {
		border: 4px solid rgba(255, 255, 255, 0.1);
		border-radius: 50%;
		border-top: 4px solid #3498db;
		width: 40px;
		height: 40px;
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
</style>
