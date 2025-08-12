<!-- SequenceCardContent.svelte - Content area displaying sequence cards in grid -->
<script lang="ts">
	import { onMount } from 'svelte';
	import type { SequenceData } from '$services/interfaces';
	import SequenceCard from './SequenceCard.svelte';

	interface Props {
		sequences?: SequenceData[];
		columnCount?: number;
		isLoading?: boolean;
		selectedLength?: number;
	}

	let {
		sequences = [],
		columnCount = 2,
		isLoading = false,
		selectedLength = 16,
	}: Props = $props();

	let contentElement: HTMLElement;
	let scrollPosition = $state(0);

	// Grid columns based on column count
	let gridColumns = $derived(`repeat(${columnCount}, 1fr)`);

	// Loading states for progressive loading simulation
	let loadedCardIds = $state(new Set<string>());
	let loadingProgress = $state(0);

	// Simulate progressive loading like desktop app
	$effect(() => {
		if (sequences.length > 0 && !isLoading) {
			loadedCardIds.clear();
			loadingProgress = 0;

			// Simulate progressive loading
			sequences.forEach((sequence, index) => {
				setTimeout(() => {
					loadedCardIds.add(sequence.id || sequence.name || `${index}`);
					loadingProgress = ((index + 1) / sequences.length) * 100;
				}, index * 100); // Stagger loading by 100ms
			});
		}
	});

	// Handle scroll position restoration
	function saveScrollPosition() {
		if (contentElement) {
			scrollPosition = contentElement.scrollTop;
		}
	}

	function restoreScrollPosition() {
		if (contentElement && scrollPosition > 0) {
			contentElement.scrollTop = scrollPosition;
		}
	}

	// Restore scroll position after sequences change
	$effect(() => {
		if (sequences.length > 0) {
			setTimeout(restoreScrollPosition, 100);
		}
	});

	onMount(() => {
		console.log('SequenceCardContent mounted');
	});
</script>

<div class="sequence-card-content" bind:this={contentElement} onscroll={saveScrollPosition}>
	{#if isLoading}
		<!-- Loading State -->
		<div class="loading-state">
			<div class="loading-spinner"></div>
			<p class="loading-text">Loading sequences...</p>
		</div>
	{:else if sequences.length === 0}
		<!-- Empty State -->
		<div class="empty-state">
			<div class="empty-content">
				<div class="empty-icon">📋</div>
				<h3 class="empty-title">No sequences to display</h3>
				<p class="empty-description">
					{#if selectedLength === 0}
						No sequences are available in your library.
					{:else}
						No sequences found with {selectedLength} beats.<br />
						Try selecting a different length or "All" to see available sequences.
					{/if}
				</p>
			</div>
		</div>
	{:else}
		<!-- Sequence Cards Grid -->
		<div class="cards-container">
			<!-- Loading Progress Bar -->
			{#if loadingProgress < 100}
				<div class="loading-progress">
					<div class="progress-bar">
						<div class="progress-fill" style:width="{loadingProgress}%"></div>
					</div>
					<span class="progress-text"
						>Loading cards... {Math.round(loadingProgress)}%</span
					>
				</div>
			{/if}

			<!-- Cards Grid -->
			<div class="cards-grid" style:grid-template-columns={gridColumns}>
				{#each sequences as sequence, index (sequence.id || sequence.name || index)}
					<div class="card-slot">
						{#if loadedCardIds.has(sequence.id || sequence.name || `${index}`)}
							<SequenceCard {sequence} />
						{:else}
							<!-- Card Placeholder -->
							<div class="card-placeholder">
								<div class="placeholder-spinner"></div>
								<span class="placeholder-text">Loading...</span>
							</div>
						{/if}
					</div>
				{/each}
			</div>

			<!-- Footer with sequence count -->
			<div class="content-footer">
				<p class="sequence-count">
					Displaying {sequences.length} sequence{sequences.length === 1 ? '' : 's'}
					{#if selectedLength > 0}
						with {selectedLength} beats
					{/if}
				</p>
			</div>
		</div>
	{/if}
</div>

<style>
	.sequence-card-content {
	height: 100%;
	overflow-y: auto;
	background: transparent;
	border-radius: 8px;
	padding: 0;
}

	/* Loading State */
	.loading-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
		gap: 20px;
		color: var(--muted-foreground);
	}

	.loading-spinner {
		width: 48px;
		height: 48px;
		border: 4px solid var(--muted);
		border-top: 4px solid var(--primary);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	.loading-text {
		margin: 0;
		font-size: 18px;
		font-weight: 500;
	}

	/* Empty State */
	.empty-state {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100%;
		padding: 40px;
	}

	.empty-content {
	text-align: center;
	background: var(--surface-glass);
	backdrop-filter: var(--glass-backdrop);
	border: 2px dashed rgba(255, 255, 255, 0.2);
	border-radius: 16px;
	padding: 48px 32px;
	max-width: 500px;
	box-shadow: var(--shadow-glass);
}

	.empty-icon {
		font-size: 64px;
		margin-bottom: 16px;
		opacity: 0.7;
	}

	.empty-title {
		margin: 0 0 12px 0;
		color: rgba(255, 255, 255, 0.9);
		font-size: 24px;
		font-weight: 600;
	}

	.empty-description {
		margin: 0;
		color: rgba(255, 255, 255, 0.7);
		font-size: 16px;
		line-height: 1.5;
		font-style: italic;
	}

	/* Cards Container */
	.cards-container {
	padding: 16px;
	display: flex;
	flex-direction: column;
	gap: 16px;
	min-height: 100%;
	background: transparent;
}

	/* Loading Progress */
	.loading-progress {
	display: flex;
	align-items: center;
	gap: 12px;
	background: var(--surface-glass);
	backdrop-filter: var(--glass-backdrop);
	border: var(--glass-border);
	border-radius: 12px;
	padding: 12px 16px;
	margin-bottom: 8px;
	box-shadow: var(--shadow-glass);
}

	.progress-bar {
	flex: 1;
	height: 8px;
	background: rgba(0, 0, 0, 0.2);
	border-radius: 4px;
	overflow: hidden;
	box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);
}

	.progress-fill {
	height: 100%;
	background: var(--gradient-primary);
	border-radius: 4px;
	transition: width var(--transition-normal);
	box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

	.progress-text {
	color: rgba(255, 255, 255, 0.8);
	font-size: 12px;
	font-weight: 500;
	min-width: 120px;
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

	/* Cards Grid */
	.cards-grid {
		display: grid;
		gap: 16px;
		grid-template-columns: repeat(2, 1fr); /* Default, overridden by inline style */
		align-items: start;
	}

	.card-slot {
		display: flex;
		flex-direction: column;
	}

	/* Card Placeholder */
	.card-placeholder {
	background: var(--surface-glass);
	backdrop-filter: var(--glass-backdrop);
	border: 2px dashed rgba(255, 255, 255, 0.2);
	border-radius: 12px;
	padding: 40px 20px;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 12px;
	min-height: 200px;
	justify-content: center;
	box-shadow: var(--shadow-glass);
}

	.placeholder-spinner {
		width: 24px;
		height: 24px;
		border: 2px solid var(--muted);
		border-top: 2px solid var(--primary);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	.placeholder-text {
	color: rgba(255, 255, 255, 0.7);
	font-size: 14px;
	font-weight: 500;
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

	/* Footer */
	.content-footer {
	margin-top: auto;
	padding: 16px 0;
	text-align: center;
	border-top: 1px solid rgba(255, 255, 255, 0.1);
	background: var(--surface-glass);
	backdrop-filter: var(--glass-backdrop);
}

	.sequence-count {
	margin: 0;
	color: rgba(255, 255, 255, 0.7);
	font-size: 14px;
	font-style: italic;
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

	/* Scrollbar Styling */
	.sequence-card-content::-webkit-scrollbar {
		width: 8px;
	}

	.sequence-card-content::-webkit-scrollbar-track {
		background: rgba(0, 0, 0, 0.1);
		border-radius: 4px;
	}

	.sequence-card-content::-webkit-scrollbar-thumb {
		background: rgba(0, 0, 0, 0.3);
		border-radius: 4px;
	}

	.sequence-card-content::-webkit-scrollbar-thumb:hover {
		background: rgba(0, 0, 0, 0.5);
	}

	/* Animations */
	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	/* Responsive Design */
	@media (max-width: 1200px) {
		.cards-grid {
			grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		}
	}

	@media (max-width: 768px) {
		.cards-container {
			padding: 12px;
			gap: 12px;
		}

		.cards-grid {
			grid-template-columns: 1fr;
			gap: 12px;
		}

		.empty-content {
			padding: 32px 24px;
		}

		.empty-icon {
			font-size: 48px;
		}

		.empty-title {
			font-size: 20px;
		}

		.empty-description {
			font-size: 14px;
		}

		.loading-progress {
			flex-direction: column;
			gap: 8px;
			text-align: center;
		}
	}
</style>
