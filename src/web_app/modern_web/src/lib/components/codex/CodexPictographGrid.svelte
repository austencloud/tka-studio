<!--
	Codex Pictograph Grid Component

	Organizes pictographs in rows/sections following the desktop layout.
	Matches desktop CodexPictographGrid functionality with proper row organization.
-->
<script lang="ts">
	import Pictograph from '$lib/components/pictograph/Pictograph.svelte';
	import type { PictographData } from '$lib/domain/PictographData';

	// Props
	interface Props {
		pictographsByLetter: Record<string, PictographData | null>;
		letterRows: string[][];
		pictographSize?: number;
		onPictographClick?: (pictograph: PictographData) => void;
	}

	let {
		pictographsByLetter,
		letterRows,
		pictographSize = 80,
		onPictographClick
	}: Props = $props();

	// Handle pictograph click
	function handlePictographClick(pictograph: PictographData) {
		onPictographClick?.(pictograph);
	}

	// Create placeholder for missing pictographs
	function createPlaceholder(letter: string) {
		return {
			id: `placeholder-${letter}`,
			letter: letter,
			// Add other required fields with default values
			start_position: 'alpha1',
			end_position: 'alpha3',
			grid_data: {},
			arrows: {},
			motions: {},
			props: {},
			metadata: { isPlaceholder: true }
		} as PictographData;
	}
</script>

<div class="codex-pictograph-grid">
	{#each letterRows as row, rowIndex}
		<div class="pictograph-row" data-row={rowIndex}>
			{#each row as letter}
				{@const pictograph = pictographsByLetter[letter] || createPlaceholder(letter)}
				{@const isPlaceholder = !pictographsByLetter[letter]}

				<button
					class="pictograph-item"
					class:placeholder={isPlaceholder}
					onclick={() => !isPlaceholder && handlePictographClick(pictograph)}
					title={letter}
					disabled={isPlaceholder}
				>
					{#if isPlaceholder}
						<!-- Placeholder for missing pictographs -->
						<div class="pictograph-placeholder" style="width: {pictographSize}px; height: {pictographSize}px;">
							<span class="placeholder-letter">{letter}</span>
						</div>
					{:else}
						<!-- Actual pictograph -->
						<div class="pictograph-container">
							<Pictograph
								pictographData={pictograph}
								width={pictographSize}
								height={pictographSize}
							/>
						</div>
					{/if}

					<!-- Letter label -->
					<span class="pictograph-label">{letter}</span>
				</button>
			{/each}
		</div>
	{/each}
</div>

<style>
	.codex-pictograph-grid {
		display: flex;
		flex-direction: column;
		gap: var(--desktop-spacing-lg);
		padding: var(--desktop-spacing-lg);
		background: transparent;
	}

	.pictograph-row {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--desktop-spacing-md);
		flex-wrap: wrap;
	}

	.pictograph-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--desktop-spacing-sm);
		padding: var(--desktop-spacing-sm);
		background: var(--desktop-bg-tertiary);
		border: 1px solid var(--desktop-border-tertiary);
		border-radius: var(--desktop-border-radius-sm);
		cursor: pointer;
		transition: all var(--desktop-transition-normal);
		min-width: fit-content;
		position: relative;
		overflow: hidden;
	}

	.pictograph-item:not(.placeholder):hover {
		background: var(--desktop-bg-secondary);
		border-color: var(--desktop-border-primary);
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
	}

	.pictograph-item:not(.placeholder):active {
		transform: translateY(0);
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
	}

	.pictograph-item.placeholder {
		cursor: default;
		opacity: 0.6;
		background: var(--desktop-bg-quaternary);
		border-style: dashed;
		border-color: var(--desktop-border-disabled);
	}

	.pictograph-container {
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--desktop-bg-secondary);
		border-radius: var(--desktop-border-radius-xs);
		padding: var(--desktop-spacing-xs);
	}

	.pictograph-placeholder {
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--desktop-bg-quaternary);
		border: 1px dashed var(--desktop-border-disabled);
		border-radius: var(--desktop-border-radius-xs);
		color: var(--desktop-text-disabled);
	}

	.placeholder-letter {
		font-weight: bold;
		font-size: var(--desktop-font-size-sm);
		color: var(--desktop-text-disabled);
	}

	.pictograph-label {
		color: var(--desktop-text-secondary);
		font-size: var(--desktop-font-size-xs);
		font-weight: 500;
		text-align: center;
		font-family: var(--desktop-font-family);
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
	}

	/* Row-specific styling */
	.pictograph-row[data-row="0"] .pictograph-item:hover {
		border-color: var(--desktop-primary-blue-border);
	}

	.pictograph-row[data-row="1"] .pictograph-item:hover {
		border-color: var(--desktop-primary-green-border);
	}

	.pictograph-row[data-row="2"] .pictograph-item:hover {
		border-color: var(--desktop-primary-purple-border);
	}

	.pictograph-row[data-row="3"] .pictograph-item:hover {
		border-color: var(--desktop-primary-orange-border);
	}

	.pictograph-row[data-row="4"] .pictograph-item:hover {
		border-color: var(--desktop-primary-red-border);
	}

	/* Animation for loading */
	.pictograph-item:not(.placeholder) {
		animation: fadeInUp 0.3s ease-out;
	}

	@keyframes fadeInUp {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.codex-pictograph-grid {
			padding: var(--desktop-spacing-md);
			gap: var(--desktop-spacing-md);
		}

		.pictograph-row {
			gap: var(--desktop-spacing-sm);
		}

		.pictograph-item {
			padding: var(--desktop-spacing-xs);
		}

		.pictograph-label {
			font-size: var(--desktop-font-size-xs);
		}
	}

	@media (max-width: 480px) {
		.pictograph-row {
			justify-content: center;
		}

		.pictograph-item {
			min-width: 60px;
		}
	}
</style>
