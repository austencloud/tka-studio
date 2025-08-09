<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { slide, fade } from 'svelte/transition';

	export let sequence: any = null;

	const dispatch = createEventDispatcher();

	let currentVariationIndex = 0;
	let isImageLoading = false;

	// Handle navigation back to browser
	function handleBackToBrowser() {
		dispatch('backToBrowser');
	}

	// Handle sequence actions
	function handleAction(action: string) {
		dispatch('sequenceAction', { action, sequence });
	}

	// Handle variation navigation
	function nextVariation() {
		if (
			sequence &&
			sequence.variations &&
			currentVariationIndex < sequence.variations.length - 1
		) {
			currentVariationIndex++;
		}
	}

	function prevVariation() {
		if (currentVariationIndex > 0) {
			currentVariationIndex--;
		}
	}

	// Reset variation index when sequence changes
	$: if (sequence) {
		currentVariationIndex = 0;
	}

	// Get current variation
	$: currentVariation = sequence?.variations?.[currentVariationIndex] || sequence;

	function getDifficultyColor(difficulty: number) {
		const colors = {
			1: '#10b981', // green
			2: '#f59e0b', // yellow
			3: '#ef4444', // red
			4: '#8b5cf6', // purple
		};
		return colors[difficulty] || '#6366f1';
	}

	function getDifficultyLabel(difficulty: number) {
		const labels = {
			1: 'Beginner',
			2: 'Intermediate',
			3: 'Advanced',
			4: 'Expert',
		};
		return labels[difficulty] || 'Unknown';
	}

	function formatDate(date: Date) {
		return date.toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'long',
			day: 'numeric',
		});
	}
</script>

<div class="sequence-viewer-panel">
	{#if sequence}
		<div class="viewer-content" transition:slide={{ duration: 300 }}>
			<!-- Header -->
			<div class="viewer-header">
				<button class="back-button" on:click={handleBackToBrowser} type="button">
					<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
						<path
							d="M12.5 15L7.5 10L12.5 5"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
					Back
				</button>

				<div class="sequence-header-info">
					<h2 class="sequence-title">{sequence.word}</h2>
					<div
						class="difficulty-badge"
						style="--difficulty-color: {getDifficultyColor(sequence.difficulty)}"
					>
						{getDifficultyLabel(sequence.difficulty)}
					</div>
				</div>
			</div>

			<!-- Image Viewer -->
			<div class="image-viewer-section">
				<div class="image-container">
					{#if currentVariation?.imageUrl}
						<img
							src={currentVariation.imageUrl}
							alt="{sequence.word} - Variation {currentVariationIndex + 1}"
							class:loading={isImageLoading}
							on:load={() => (isImageLoading = false)}
							on:error={() => (isImageLoading = false)}
						/>
					{:else}
						<!-- Placeholder -->
						<div class="image-placeholder">
							<div class="placeholder-content">
								<div class="sequence-icon">🔄</div>
								<h3>{sequence.word}</h3>
								<p>Pictograph visualization</p>
								<div class="placeholder-details">
									<span>{sequence.gridMode} grid</span>
									<span>{sequence.startPosition} start</span>
								</div>
							</div>
						</div>
					{/if}

					{#if sequence.isFavorite}
						<div class="favorite-indicator">⭐</div>
					{/if}
				</div>

				<!-- Navigation Controls -->
				{#if sequence.variations && sequence.variations.length > 1}
					<div class="image-navigation">
						<button
							class="nav-button"
							class:disabled={currentVariationIndex === 0}
							on:click={prevVariation}
							disabled={currentVariationIndex === 0}
							type="button"
						>
							◀
						</button>

						<span class="variation-info">
							{currentVariationIndex + 1} / {sequence.variations.length}
						</span>

						<button
							class="nav-button"
							class:disabled={currentVariationIndex >= sequence.variations.length - 1}
							on:click={nextVariation}
							disabled={currentVariationIndex >= sequence.variations.length - 1}
							type="button"
						>
							▶
						</button>
					</div>
				{/if}
			</div>

			<!-- Sequence Details -->
			<div class="sequence-details">
				<h3>Details</h3>

				<div class="details-grid">
					<div class="detail-item">
						<span class="detail-label">Length</span>
						<span class="detail-value">{sequence.length} beats</span>
					</div>

					<div class="detail-item">
						<span class="detail-label">Start Position</span>
						<span class="detail-value">{sequence.startPosition}</span>
					</div>

					<div class="detail-item">
						<span class="detail-label">Grid Mode</span>
						<span class="detail-value">{sequence.gridMode}</span>
					</div>

					<div class="detail-item">
						<span class="detail-label">Author</span>
						<span class="detail-value">{sequence.author}</span>
					</div>

					<div class="detail-item">
						<span class="detail-label">Date Added</span>
						<span class="detail-value">{formatDate(sequence.dateAdded)}</span>
					</div>

					<div class="detail-item">
						<span class="detail-label">Difficulty</span>
						<span
							class="detail-value"
							style="color: {getDifficultyColor(sequence.difficulty)}"
						>
							{getDifficultyLabel(sequence.difficulty)}
						</span>
					</div>
				</div>

				{#if sequence.tags && sequence.tags.length > 0}
					<div class="tags-section">
						<h4>Tags</h4>
						<div class="tags-container">
							{#each sequence.tags as tag}
								<span class="tag">{tag}</span>
							{/each}
						</div>
					</div>
				{/if}
			</div>

			<!-- Action Buttons -->
			<div class="action-buttons">
				<button
					class="action-button primary"
					on:click={() => handleAction('edit')}
					type="button"
				>
					<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
						<path
							d="M12.1465 1.85355C12.3417 1.65829 12.6583 1.65829 12.8536 1.85355L14.1464 3.14645C14.3417 3.34171 14.3417 3.65829 14.1464 3.85355L5.35355 12.6464L2 13L2.35355 9.64645L11.1464 0.853553C11.3417 0.658291 11.6583 0.658291 11.8536 0.853553L12.1465 1.85355Z"
							stroke="currentColor"
							stroke-width="1.5"
						/>
					</svg>
					Edit
				</button>

				<button
					class="action-button secondary"
					on:click={() => handleAction('save')}
					type="button"
				>
					<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
						<path d="M13 2.5V13.5H3V2.5H13Z" stroke="currentColor" stroke-width="1.5" />
						<path d="M10 1V4H6V1" stroke="currentColor" stroke-width="1.5" />
					</svg>
					Save
				</button>

				<button
					class="action-button secondary"
					on:click={() => handleAction('fullscreen')}
					type="button"
				>
					<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
						<path
							d="M2 5V2H5M14 5V2H11M14 11V14H11M2 11V14H5"
							stroke="currentColor"
							stroke-width="1.5"
						/>
					</svg>
					Fullscreen
				</button>

				<button
					class="action-button danger"
					on:click={() => handleAction('delete')}
					type="button"
				>
					<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
						<path
							d="M2 4H14M6 4V2H10V4M12 4V14H4V4"
							stroke="currentColor"
							stroke-width="1.5"
						/>
					</svg>
					Delete
				</button>
			</div>
		</div>
	{:else}
		<!-- Empty State -->
		<div class="empty-viewer" transition:fade>
			<div class="empty-content">
				<div class="empty-icon">👁️</div>
				<h3>Select a Sequence</h3>
				<p>Choose a sequence from the browser to view its details and pictograph.</p>
			</div>
		</div>
	{/if}
</div>

<style>
	.sequence-viewer-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		background: rgba(255, 255, 255, 0.02);
		overflow: hidden;
	}

	.viewer-content {
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow-y: auto;
		padding: var(--spacing-lg);
		gap: var(--spacing-lg);
	}

	/* Header */
	.viewer-header {
		display: flex;
		align-items: center;
		gap: var(--spacing-md);
		padding-bottom: var(--spacing-md);
		border-bottom: var(--glass-border);
	}

	.back-button {
		display: flex;
		align-items: center;
		gap: var(--spacing-xs);
		padding: var(--spacing-sm);
		background: rgba(255, 255, 255, 0.1);
		border: var(--glass-border);
		border-radius: 8px;
		color: var(--foreground);
		font-family: inherit;
		font-size: var(--font-size-sm);
		cursor: pointer;
		transition: all var(--transition-fast);
		flex-shrink: 0;
	}

	.back-button:hover {
		background: rgba(255, 255, 255, 0.15);
		border-color: var(--primary-color);
		color: var(--primary-color);
	}

	.sequence-header-info {
		display: flex;
		align-items: center;
		gap: var(--spacing-md);
		flex: 1;
		min-width: 0;
	}

	.sequence-title {
		font-size: var(--font-size-xl);
		font-weight: 600;
		color: var(--foreground);
		margin: 0;
		flex: 1;
		min-width: 0;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.difficulty-badge {
		--difficulty-color: var(--primary-color);

		padding: var(--spacing-xs) var(--spacing-sm);
		background: var(--difficulty-color);
		color: white;
		border-radius: 12px;
		font-size: var(--font-size-xs);
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.5px;
		flex-shrink: 0;
	}

	/* Image Viewer */
	.image-viewer-section {
		flex-shrink: 0;
	}

	.image-container {
		position: relative;
		width: 100%;
		height: 200px;
		background: linear-gradient(
			135deg,
			rgba(99, 102, 241, 0.1),
			rgba(168, 85, 247, 0.1),
			rgba(6, 182, 212, 0.1)
		);
		border: var(--glass-border);
		border-radius: 12px;
		overflow: hidden;
		margin-bottom: var(--spacing-md);
	}

	.image-container img {
		width: 100%;
		height: 100%;
		object-fit: contain;
		transition: opacity var(--transition-fast);
	}

	.image-container img.loading {
		opacity: 0.5;
	}

	.image-placeholder {
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		color: white;
	}

	.placeholder-content {
		text-align: center;
		padding: var(--spacing-lg);
	}

	.sequence-icon {
		font-size: 2rem;
		margin-bottom: var(--spacing-sm);
	}

	.placeholder-content h3 {
		font-size: var(--font-size-lg);
		margin: 0 0 var(--spacing-xs) 0;
		color: white;
	}

	.placeholder-content p {
		color: rgba(255, 255, 255, 0.8);
		margin: 0 0 var(--spacing-sm) 0;
		font-size: var(--font-size-sm);
	}

	.placeholder-details {
		display: flex;
		gap: var(--spacing-sm);
		justify-content: center;
		font-size: var(--font-size-xs);
		opacity: 0.7;
	}

	.placeholder-details span {
		padding: 2px 6px;
		background: rgba(255, 255, 255, 0.2);
		border-radius: 4px;
		text-transform: capitalize;
	}

	.favorite-indicator {
		position: absolute;
		top: var(--spacing-sm);
		right: var(--spacing-sm);
		background: rgba(0, 0, 0, 0.5);
		border-radius: 50%;
		width: 32px;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
		backdrop-filter: blur(10px);
		font-size: var(--font-size-base);
	}

	.image-navigation {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--spacing-md);
		padding: var(--spacing-sm);
	}

	.nav-button {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 36px;
		height: 36px;
		background: rgba(255, 255, 255, 0.1);
		border: var(--glass-border);
		border-radius: 50%;
		color: var(--foreground);
		cursor: pointer;
		transition: all var(--transition-fast);
		font-size: var(--font-size-base);
	}

	.nav-button:hover:not(.disabled) {
		background: rgba(255, 255, 255, 0.2);
		border-color: var(--primary-color);
		color: var(--primary-color);
	}

	.nav-button.disabled {
		opacity: 0.3;
		cursor: not-allowed;
	}

	.variation-info {
		font-size: var(--font-size-sm);
		color: var(--muted-foreground);
		min-width: 60px;
		text-align: center;
	}

	/* Sequence Details */
	.sequence-details {
		flex: 1;
	}

	.sequence-details h3 {
		font-size: var(--font-size-lg);
		color: var(--foreground);
		margin: 0 0 var(--spacing-md) 0;
		font-weight: 600;
	}

	.details-grid {
		display: grid;
		gap: var(--spacing-sm);
		margin-bottom: var(--spacing-lg);
	}

	.detail-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: var(--spacing-sm);
		background: rgba(255, 255, 255, 0.05);
		border-radius: 8px;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.detail-label {
		font-size: var(--font-size-sm);
		color: var(--muted-foreground);
		font-weight: 500;
	}

	.detail-value {
		font-size: var(--font-size-sm);
		color: var(--foreground);
		font-weight: 600;
		text-align: right;
		text-transform: capitalize;
	}

	.tags-section h4 {
		font-size: var(--font-size-base);
		color: var(--foreground);
		margin: 0 0 var(--spacing-sm) 0;
		font-weight: 600;
	}

	.tags-container {
		display: flex;
		flex-wrap: wrap;
		gap: var(--spacing-xs);
	}

	.tag {
		padding: var(--spacing-xs) var(--spacing-sm);
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 12px;
		font-size: var(--font-size-xs);
		color: var(--muted-foreground);
		font-weight: 500;
	}

	/* Action Buttons */
	.action-buttons {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--spacing-sm);
		flex-shrink: 0;
	}

	.action-button {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--spacing-xs);
		padding: var(--spacing-md);
		border: var(--glass-border);
		border-radius: 8px;
		font-family: inherit;
		font-size: var(--font-size-sm);
		font-weight: 500;
		cursor: pointer;
		transition: all var(--transition-fast);
		backdrop-filter: var(--glass-backdrop);
	}

	.action-button.primary {
		background: var(--primary-color);
		color: white;
		border-color: var(--primary-color);
	}

	.action-button.primary:hover {
		background: var(--primary-light);
		transform: translateY(-1px);
		box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
	}

	.action-button.secondary {
		background: rgba(255, 255, 255, 0.1);
		color: var(--foreground);
	}

	.action-button.secondary:hover {
		background: rgba(255, 255, 255, 0.15);
		border-color: var(--primary-color);
		color: var(--primary-color);
	}

	.action-button.danger {
		background: rgba(239, 68, 68, 0.1);
		color: #ef4444;
		border-color: rgba(239, 68, 68, 0.3);
	}

	.action-button.danger:hover {
		background: #ef4444;
		color: white;
		border-color: #ef4444;
	}

	/* Empty State */
	.empty-viewer {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100%;
		padding: var(--spacing-xl);
	}

	.empty-content {
		text-align: center;
		max-width: 300px;
	}

	.empty-icon {
		font-size: 3rem;
		margin-bottom: var(--spacing-lg);
		opacity: 0.6;
	}

	.empty-content h3 {
		font-size: var(--font-size-xl);
		color: var(--foreground);
		margin: 0 0 var(--spacing-md) 0;
		font-weight: 600;
	}

	.empty-content p {
		color: var(--muted-foreground);
		line-height: 1.5;
		margin: 0;
	}

	/* Responsive Design */
	@media (max-width: 768px) {
		.viewer-content {
			padding: var(--spacing-md);
			gap: var(--spacing-md);
		}

		.sequence-header-info {
			flex-direction: column;
			align-items: flex-start;
			gap: var(--spacing-sm);
		}

		.sequence-title {
			font-size: var(--font-size-lg);
		}

		.image-container {
			height: 150px;
		}

		.action-buttons {
			grid-template-columns: 1fr;
		}
	}
</style>
