<script lang="ts">
	import { createEventDispatcher, onMount } from 'svelte';
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import CategoryButton from './CategoryButton.svelte';

	export let title: string;
	export let type: string;
	export let options: any[];
	export let sections: any[][] = [];
	export let isActive: boolean = false;
	export let isExpanded: boolean = false;

	const dispatch = createEventDispatcher();

	let contentElement: HTMLDivElement;

	// Handle header click to request expansion/collapse
	function toggleExpansion() {
		dispatch('expansionRequested', { type, title });
	}

	// Handle filter selection from category buttons
	function handleFilterSelection(event: CustomEvent) {
		const value = event.detail;
		dispatch('filterSelected', { type, value });
	}

	// Handle letter selection (for starting letter type)
	function handleLetterSelection(letter: string) {
		dispatch('filterSelected', { type, value: letter });
	}
</script>

<div class="accordion-section" class:expanded={isExpanded} class:active={isActive}>
	<!-- Accordion Header -->
	<button
		class="accordion-header"
		class:expanded={isExpanded}
		on:click={toggleExpansion}
		type="button"
	>
		<div class="header-content">
			<span class="header-title">{title}</span>
			{#if isActive}
				<span class="active-indicator">●</span>
			{/if}
		</div>
		<div class="header-icon" class:rotated={isExpanded}>
			<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
				<path
					d="M5 7.5L10 12.5L15 7.5"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
			</svg>
		</div>
	</button>

	<!-- Accordion Content -->
	{#if isExpanded}
		<div
			class="accordion-content"
			bind:this={contentElement}
			transition:slide={{ duration: 300, easing: cubicInOut }}
		>
			<div class="content-inner">
				{#if type === 'starting_letter'}
					<!-- Special letter grid layout for Starting Letter section -->
					<div class="letter-grid-container">
						{#each sections as row}
							<div class="letter-row">
								{#each row as letter}
									<button
										class="letter-button"
										on:click={() => handleLetterSelection(letter)}
										type="button"
									>
										{letter}
									</button>
								{/each}
							</div>
						{/each}
					</div>
				{:else if type === 'starting_position' || type === 'difficulty' || type === 'grid_mode'}
					<!-- Image-based content for visual filters -->
					<div class="options-grid visual-grid">
						{#each options as option}
							<CategoryButton
								{option}
								visualType={type}
								on:selected={handleFilterSelection}
							/>
						{/each}
					</div>
				{:else}
					<!-- Standard button grid for other filters -->
					<div class="options-grid standard-grid">
						{#each options as option}
							<CategoryButton {option} on:selected={handleFilterSelection} />
						{/each}
					</div>
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	.accordion-section {
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 12px;
		margin: 4px;
		padding: 0px;
		overflow: hidden;
		transition: all var(--transition-normal);
	}

	.accordion-section:hover {
		background: rgba(255, 255, 255, 0.15);
		border: 1px solid rgba(255, 255, 255, 0.3);
	}

	.accordion-section.expanded {
		background: rgba(255, 255, 255, 0.15);
		border: 1px solid rgba(255, 255, 255, 0.3);
	}

	.accordion-section.active {
		border-color: var(--accent-color);
		background: rgba(6, 182, 212, 0.1);
	}

	/* Accordion Header */
	.accordion-header {
		width: 100%;
		padding: 12px 16px;
		background: transparent;
		border: none;
		cursor: pointer;
		display: flex;
		justify-content: space-between;
		align-items: center;
		transition: all var(--transition-fast);
		color: rgba(255, 255, 255, 0.9);
		font-family: inherit;
		border-radius: 12px;
	}

	.accordion-header:hover {
		background: rgba(255, 255, 255, 0.05);
	}

	.accordion-header.expanded {
		background: rgba(255, 255, 255, 0.05);
	}

	.header-content {
		display: flex;
		align-items: center;
		gap: var(--spacing-sm);
	}

	.header-title {
		font-size: 11pt;
		font-weight: 500;
		margin: 0;
		color: rgba(255, 255, 255, 0.9);
	}

	.active-indicator {
		color: var(--accent-color);
		font-size: var(--font-size-sm);
		animation: pulse 2s ease-in-out infinite;
	}

	.header-icon {
		display: flex;
		align-items: center;
		justify-content: center;
		transition: transform var(--transition-normal);
		color: var(--muted-foreground);
	}

	.header-icon.rotated {
		transform: rotate(180deg);
		color: var(--primary-color);
	}

	/* Accordion Content */
	.accordion-content {
		overflow: hidden;
	}

	.content-inner {
		padding: var(--spacing-lg);
		padding-top: var(--spacing-md);
	}

	/* Options Grid */
	.options-grid {
		display: grid;
		gap: var(--spacing-sm);
	}

	.standard-grid {
		grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
	}

	.visual-grid {
		grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
		gap: var(--spacing-xl);
		justify-items: center;
		max-width: 100%;
	}

	/* Letter Grid Layout for Starting Letter Section */
	.letter-grid-container {
		display: flex;
		flex-direction: column;
		gap: var(--spacing-sm);
		width: 100%;
		padding: var(--spacing-sm);
	}

	.letter-row {
		display: flex;
		gap: var(--spacing-xs);
		justify-content: center;
		flex-wrap: nowrap;
		margin-bottom: var(--spacing-xs);
	}

	.letter-button {
		min-width: 36px;
		height: 36px;
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 6px;
		background: rgba(255, 255, 255, 0.1);
		color: var(--foreground);
		font-size: var(--font-size-md);
		font-weight: 600;
		cursor: pointer;
		transition: all var(--transition-fast);
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
		flex: 1;
		max-width: 45px;
	}

	.letter-button:hover {
		background: rgba(255, 255, 255, 0.2);
		border-color: rgba(255, 255, 255, 0.5);
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}

	.letter-button:active {
		transform: translateY(0);
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
	}

	/* Animations */
	@keyframes pulse {
		0%,
		100% {
			opacity: 1;
		}
		50% {
			opacity: 0.5;
		}
	}

	/* Responsive Design */
	@media (max-width: 768px) {
		.accordion-header {
			padding: var(--spacing-md);
		}

		.content-inner {
			padding: var(--spacing-md);
		}

		.standard-grid {
			grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
		}

		.visual-grid {
			grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
			gap: var(--spacing-lg);
		}

		.header-title {
			font-size: var(--font-size-base);
		}

		.letter-button {
			min-width: 35px;
			height: 35px;
			font-size: var(--font-size-base);
		}
	}
</style>
