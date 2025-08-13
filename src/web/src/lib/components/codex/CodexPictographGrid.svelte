<!--
	Codex Pictograph Grid Component

	Organizes pictographs in rows/sections following the desktop layout.
	Matches desktop CodexPictographGrid functionality with proper row organization.
-->
<script lang="ts">
	import Pictograph from '$lib/components/pictograph/Pictograph.svelte';
	import type { PictographData } from '$lib/domain/PictographData';
	import { createGridData } from '$lib/domain/GridData';
	import { GridMode } from '$lib/domain/enums';

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
		onPictographClick,
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
			beat: 0,
			is_blank: true,
			is_mirrored: false,
			grid_data: createGridData({ grid_mode: GridMode.DIAMOND }),
			arrows: {},
			motions: {},
			props: {},
			metadata: { isPlaceholder: true },
		} as PictographData;
	}

	// Define letter type sections with their row ranges, descriptions, and colors
	// Based on the desktop LETTER_ROWS structure and OptionPickerSectionHeader colors
	const letterTypeSections = [
		{
			name: 'Type 1',
			description: 'Dual-Shift',
			startRow: 0,
			endRow: 3,
			primaryColor: '#36c3ff',
			secondaryColor: '#6F2DA8',
		}, // A-V (rows 0-3)
		{
			name: 'Type 2',
			description: 'Shift',
			startRow: 4,
			endRow: 5,
			primaryColor: '#6F2DA8',
			secondaryColor: '#6F2DA8',
		}, // W,X,Y,Z,Σ,Δ,θ,Ω (rows 4-5)
		{
			name: 'Type 3',
			description: 'Cross-Shift',
			startRow: 6,
			endRow: 7,
			primaryColor: '#26e600',
			secondaryColor: '#6F2DA8',
		}, // W-,X-,Y-,Z-,Σ-,Δ-,θ-,Ω- (rows 6-7)
		{
			name: 'Type 4',
			description: 'Dash',
			startRow: 8,
			endRow: 8,
			primaryColor: '#26e600',
			secondaryColor: '#26e600',
		}, // Φ,Ψ,Λ (row 8)
		{
			name: 'Type 5',
			description: 'Dual-Dash',
			startRow: 9,
			endRow: 9,
			primaryColor: '#00b3ff',
			secondaryColor: '#26e600',
		}, // Φ-,Ψ-,Λ- (row 9)
		{
			name: 'Type 6',
			description: 'Static',
			startRow: 10,
			endRow: 10,
			primaryColor: '#eb7d00',
			secondaryColor: '#eb7d00',
		}, // α,β,Γ (row 10)
	];

	// Function to get section for a given row index
	function getSectionForRow(rowIndex: number) {
		return letterTypeSections.find(
			(section) => rowIndex >= section.startRow && rowIndex <= section.endRow
		);
	}

	// Function to check if this is the first row of a section
	function isFirstRowOfSection(rowIndex: number) {
		return letterTypeSections.some((section) => section.startRow === rowIndex);
	}

	// Function to generate colored HTML text like desktop LetterTypeTextPainter
	function getColoredText(description: string): string {
		const colors = {
			Shift: '#6F2DA8',
			Dual: '#00b3ff',
			Dash: '#26e600',
			Cross: '#26e600',
			Static: '#eb7d00',
			'-': '#000000',
		};

		let coloredText = description;

		// Apply colors to each word
		Object.entries(colors).forEach(([word, color]) => {
			const regex = new RegExp(`\\b${word}\\b`, 'gi');
			coloredText = coloredText.replace(
				regex,
				`<span style="color: ${color};">${word}</span>`
			);
		});

		return coloredText;
	}
</script>

<div class="codex-pictograph-grid">
	{#each letterRows as row, rowIndex}
		<!-- Add section header if this is the first row of a section -->
		{#if isFirstRowOfSection(rowIndex)}
			{@const section = getSectionForRow(rowIndex)}
			{#if section}
				<div class="section-header">
					<div class="section-header-container">
						<span class="section-text">
							<span class="section-type">{section.name}:</span>
							{@html getColoredText(section.description)}
						</span>
					</div>
				</div>
			{/if}
		{/if}

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
						<span class="placeholder-letter">{letter}</span>
					{:else}
						<!-- Actual pictograph - simplified container structure -->
						<Pictograph
							pictographData={pictograph}
							width={pictographSize}
							height={pictographSize}
						/>
					{/if}
				</button>
			{/each}
		</div>
	{/each}
</div>

<style>
	.codex-pictograph-grid {
		display: flex;
		flex-direction: column;
		gap: var(--desktop-spacing-md); /* Slightly tighter spacing */
		padding: var(--desktop-spacing-lg);
		background: transparent;
	}

	.section-header {
		display: flex;
		justify-content: center;
		margin: var(--desktop-spacing-lg) 0 var(--desktop-spacing-md) 0;
	}

	.section-header:first-child {
		margin-top: 0;
	}

	.section-header-container {
		background: rgba(255, 255, 255, 0.2);
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: var(--desktop-border-radius);
		padding: var(--desktop-spacing-sm) var(--desktop-spacing-lg);
		backdrop-filter: blur(10px);
		box-shadow: var(--desktop-shadow-sm);
		transition: all var(--desktop-transition-normal);
	}

	.section-header-container:hover {
		background: rgba(255, 255, 255, 0.25);
		border: 1px solid rgba(255, 255, 255, 0.4);
		box-shadow: var(--desktop-shadow-md);
	}

	.section-text {
		display: inline-block;
		font-family: var(--desktop-font-family);
		font-size: var(--desktop-font-size-base);
		font-weight: 500;
		line-height: 1.2;
		white-space: nowrap;
	}

	.section-type {
		color: #000000; /* Black for "Type 1:" part */
		font-weight: bold;
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
		gap: var(--desktop-spacing-xs); /* Reduced gap */
		padding: var(--desktop-spacing-xs); /* Reduced padding */
		background: var(--desktop-bg-tertiary); /* Back to transparent background */
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

	.placeholder-letter {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
		background: var(--desktop-bg-quaternary);
		border: 1px dashed var(--desktop-border-disabled);
		border-radius: var(--desktop-border-radius-xs);
		color: var(--desktop-text-disabled);
		font-weight: bold;
		font-size: var(--desktop-font-size-sm);
	}

	/* Row-specific styling */
	.pictograph-row[data-row='0'] .pictograph-item:hover {
		border-color: var(--desktop-primary-blue-border);
	}

	.pictograph-row[data-row='1'] .pictograph-item:hover {
		border-color: var(--desktop-primary-green-border);
	}

	.pictograph-row[data-row='2'] .pictograph-item:hover {
		border-color: var(--desktop-primary-purple-border);
	}

	.pictograph-row[data-row='3'] .pictograph-item:hover {
		border-color: var(--desktop-primary-orange-border);
	}

	.pictograph-row[data-row='4'] .pictograph-item:hover {
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
