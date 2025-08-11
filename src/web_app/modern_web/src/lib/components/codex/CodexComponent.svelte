<!--
	Codex Component - Reference sidebar for browsing pictographs
	
	Matches desktop CodexComponent functionality with collapsible sections,
	pictograph browsing, and filtering capabilities.
-->
<script lang="ts">
	import type { PictographData } from '$lib/domain/PictographData';
	import { createCodexState } from '$lib/state/codex-state.svelte';
	
	// Props
	interface Props {
		isVisible?: boolean;
		onPictographSelected?: (pictograph: PictographData) => void;
		onToggleVisibility?: () => void;
	}
	
	let {
		isVisible = true,
		onPictographSelected,
		onToggleVisibility
	}: Props = $props();
	
	// Create codex state using runes
	const codexState = createCodexState();
	
	// Reactive values
	let filteredPictographs = $derived(codexState.filteredPictographs);
	let isLoading = $derived(codexState.isLoading);
	let searchTerm = $derived(codexState.searchTerm);
	let error = $derived(codexState.error);
	
	// Codex is simply an alphabetical reference of all pictographs
	
	// Methods
	function handleSearchChange(event: Event) {
		const target = event.target as HTMLInputElement;
		codexState.setSearchTerm(target.value);
	}
	
	function handlePictographClick(pictograph: PictographData) {
		onPictographSelected?.(pictograph);
	}
	
	function toggleCollapse() {
		onToggleVisibility?.();
	}
</script>

<div class="codex-component" class:collapsed={!isVisible}>
	<!-- Header with toggle -->
	<div class="codex-header">
		<button class="collapse-button" onclick={toggleCollapse}>
			{isVisible ? '◀' : '▶'}
		</button>
		<h3 class="codex-title">Codex</h3>
	</div>
	
	{#if isVisible}
		<!-- Search bar -->
		<div class="search-section">
			<input
				type="text"
				class="search-input"
				placeholder="Search pictographs..."
				value={searchTerm}
				oninput={handleSearchChange}
			/>
		</div>
		
		<!-- Content area -->
		<div class="codex-content">
			{#if error}
				<div class="error-state">
					<div class="error-icon">⚠️</div>
					<p class="error-message">{error}</p>
					<button class="retry-button" onclick={() => codexState.refreshPictographs()}>
						Retry
					</button>
				</div>
			{:else if isLoading}
				<div class="loading-state">
					<div class="loading-spinner"></div>
					<p>Loading pictographs...</p>
				</div>
			{:else if filteredPictographs.length === 0}
				<div class="empty-state">
					<p>No pictographs found</p>
				</div>
			{:else}
				<div class="pictograph-grid">
					{#each filteredPictographs as pictograph (pictograph.id)}
						<button
							class="pictograph-item"
							onclick={() => handlePictographClick(pictograph)}
							title={pictograph.letter || 'Pictograph'}
						>
							<!-- Pictograph preview would go here -->
							<div class="pictograph-preview">
								<span class="letter-label">{pictograph.letter || '?'}</span>
							</div>
							<span class="pictograph-label">{pictograph.letter}</span>
						</button>
					{/each}
				</div>
			{/if}
		</div>
	{/if}
</div>

<style>
	@import '$lib/styles/desktop-theme.css';
	
	.codex-component {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 300px;
		min-width: 250px;
		background: var(--desktop-bg-secondary);
		border-radius: var(--desktop-border-radius);
		border: 1px solid var(--desktop-border-secondary);
		backdrop-filter: blur(10px);
		transition: all var(--desktop-transition-slow);
	}
	
	.codex-component.collapsed {
		width: 60px;
		min-width: 60px;
	}
	
	.codex-header {
		display: flex;
		align-items: center;
		padding: var(--desktop-spacing-lg);
		border-bottom: 1px solid var(--desktop-border-tertiary);
		gap: var(--desktop-spacing-md);
	}
	
	.collapse-button {
		background: var(--desktop-bg-tertiary);
		border: 1px solid var(--desktop-border-secondary);
		border-radius: var(--desktop-border-radius-xs);
		color: var(--desktop-text-primary);
		width: 32px;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		font-size: var(--desktop-font-size-sm);
		transition: all var(--desktop-transition-normal);
	}
	
	.collapse-button:hover {
		background: var(--desktop-bg-secondary);
		border-color: var(--desktop-border-primary);
	}
	
	.codex-title {
		color: var(--desktop-text-primary);
		font-family: var(--desktop-font-family);
		font-size: var(--desktop-font-size-lg);
		font-weight: bold;
		margin: 0;
		text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
	}
	
	.collapsed .codex-title {
		display: none;
	}

	
	.search-section {
		padding: var(--desktop-spacing-lg);
		border-bottom: 1px solid var(--desktop-border-tertiary);
	}
	
	.collapsed .search-section {
		display: none;
	}
	
	.search-input {
		width: 100%;
		padding: var(--desktop-spacing-sm) var(--desktop-spacing-md);
		background: var(--desktop-bg-tertiary);
		border: 1px solid var(--desktop-border-secondary);
		border-radius: var(--desktop-border-radius-xs);
		color: var(--desktop-text-primary);
		font-size: var(--desktop-font-size-sm);
		outline: none;
		transition: all var(--desktop-transition-normal);
	}
	
	.search-input::placeholder {
		color: var(--desktop-text-disabled);
	}
	
	.search-input:focus {
		border-color: var(--desktop-primary-blue-border);
		background: var(--desktop-bg-secondary);
	}
	
	.codex-content {
		flex: 1;
		padding: var(--desktop-spacing-lg);
		overflow-y: auto;
	}
	
	.collapsed .codex-content {
		display: none;
	}
	
	.loading-state,
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 200px;
		color: var(--desktop-text-muted);
		text-align: center;
		gap: var(--desktop-spacing-lg);
	}
	
	.error-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 200px;
		color: var(--desktop-progress-poor);
		text-align: center;
		gap: var(--desktop-spacing-lg);
	}
	
	.error-icon {
		font-size: 2rem;
	}
	
	.error-message {
		margin: 0;
		font-size: var(--desktop-font-size-sm);
		color: var(--desktop-text-muted);
	}
	
	.retry-button {
		padding: var(--desktop-spacing-sm) var(--desktop-spacing-lg);
		background-color: var(--desktop-restart-blue);
		border: 1px solid var(--desktop-restart-blue-border);
		border-radius: var(--desktop-border-radius-xs);
		color: var(--desktop-text-primary);
		font-size: var(--desktop-font-size-sm);
		font-weight: 500;
		cursor: pointer;
		transition: all var(--desktop-transition-normal);
	}
	
	.retry-button:hover {
		background-color: var(--desktop-restart-blue-hover);
		border-color: var(--desktop-restart-blue-hover-border);
	}
	
	.loading-spinner {
		width: 32px;
		height: 32px;
		border: 3px solid var(--desktop-border-tertiary);
		border-left: 3px solid var(--desktop-primary-blue);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}
	
	.pictograph-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
		gap: var(--desktop-spacing-md);
	}
	
	.pictograph-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--desktop-spacing-sm);
		padding: var(--desktop-spacing-md);
		background: var(--desktop-bg-tertiary);
		border: 1px solid var(--desktop-border-tertiary);
		border-radius: var(--desktop-border-radius-sm);
		cursor: pointer;
		transition: all var(--desktop-transition-normal);
		min-height: 80px;
	}
	
	.pictograph-item:hover {
		background: var(--desktop-bg-secondary);
		border-color: var(--desktop-border-primary);
		transform: translateY(-2px);
	}
	
	.pictograph-preview {
		width: 40px;
		height: 40px;
		background: var(--desktop-bg-secondary);
		border-radius: var(--desktop-border-radius-xs);
		display: flex;
		align-items: center;
		justify-content: center;
		color: var(--desktop-text-primary);
		font-weight: bold;
		font-size: var(--desktop-font-size-xl);
	}
	
	.pictograph-label {
		color: var(--desktop-text-secondary);
		font-size: var(--desktop-font-size-xs);
		font-weight: 500;
		text-align: center;
	}
	
	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}
	
	/* Responsive design */
	@media (max-width: 768px) {
		.codex-component {
			width: 250px;
			min-width: 200px;
		}
		
		.pictograph-grid {
			grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
			gap: var(--desktop-spacing-sm);
		}
		
		.pictograph-item {
			padding: var(--desktop-spacing-sm);
			min-height: 60px;
		}
		
		.pictograph-preview {
			width: 32px;
			height: 32px;
			font-size: var(--desktop-font-size-base);
		}
	}
</style>
