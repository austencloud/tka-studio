<!--
OptionPickerSection.svelte - Individual section for each letter type

Matches the desktop version exactly:
- Section header with colored type button
- Grid layout for pictographs of this type
- Toggle functionality to show/hide section
- Responsive grid sizing
-->
<script lang="ts">
	import ModernPictograph from '$lib/components/pictograph/Pictograph.svelte';
	import type { PictographData } from '$lib/domain/PictographData';
	import OptionPickerSectionHeader from './OptionPickerSectionHeader.svelte';

	// Props
	const {
		letterType,
		pictographs = [],
		onPictographSelected = () => {},
		containerWidth = 800,
		isExpanded = true,
	} = $props<{
		letterType: string;
		pictographs?: PictographData[];
		onPictographSelected?: (pictograph: PictographData) => void;
		containerWidth?: number;
		isExpanded?: boolean;
	}>();

	// Section state using runes
	let sectionExpanded = $state(isExpanded);
	let selectedPictograph = $state<PictographData | null>(null);

	// Layout calculations (matches desktop grid layout)
	const layoutConfig = $derived(() => {
		const baseSize = 144; // Match desktop pictograph size
		const spacing = 8; // Grid spacing
		const minSize = 100;
		const maxSize = 200;

		// Calculate how many pictographs fit per row
		const availableWidth = containerWidth - 32; // Account for padding
		const optionsPerRow = Math.max(1, Math.floor(availableWidth / (baseSize + spacing)));

		// Calculate actual pictograph size
		const totalSpacing = (optionsPerRow - 1) * spacing;
		const availableForPictographs = availableWidth - totalSpacing;
		let pictographSize = availableForPictographs / optionsPerRow;

		// Apply size constraints
		pictographSize = Math.min(maxSize, Math.max(minSize, pictographSize));

		// Prefer 144px when close (desktop compatibility)
		if (pictographSize < 144 && pictographSize > 120) {
			pictographSize = 144;
		}

		return {
			optionsPerRow,
			pictographSize: Math.floor(pictographSize),
			spacing,
		};
	});

	// Toggle section visibility
	function toggleSection() {
		sectionExpanded = !sectionExpanded;
	}

	// Handle pictograph selection
	function handlePictographSelected(pictograph: PictographData) {
		selectedPictograph = pictograph;
		onPictographSelected(pictograph);
	}


	// Since pictographs are already filtered by OptionPickerScroll, just use them directly
	const sectionPictographs = $derived(() => {
		return pictographs;
	});
</script>

<div class="option-picker-section" class:expanded={sectionExpanded}>
	<!-- Section Header -->
	<OptionPickerSectionHeader {letterType} onToggle={toggleSection} />

	<!-- Pictograph Grid (only shown when expanded) -->
	{#if sectionExpanded && sectionPictographs().length > 0}
		<div class="pictograph-frame">
			<div
				class="pictographs-grid"
				style:grid-template-columns="repeat({layoutConfig().optionsPerRow}, 1fr)"
				style:gap="{layoutConfig().spacing}px"
			>
				{#each sectionPictographs() as pictograph (pictograph.id)}
					<div
						class="pictograph-container"
						class:selected={selectedPictograph?.id === pictograph.id}
						role="button"
						tabindex="0"
						onclick={() => handlePictographSelected(pictograph)}
						onkeydown={(e) => {
							if (e.key === 'Enter' || e.key === ' ') {
								e.preventDefault();
								handlePictographSelected(pictograph);
							}
						}}
						style:width="{layoutConfig().pictographSize}px"
						style:height="{layoutConfig().pictographSize}px"
					>
						<ModernPictograph
							pictographData={pictograph}
							width={layoutConfig().pictographSize}
							height={layoutConfig().pictographSize}
							showLoadingIndicator={false}
							debug={false}
						/>
					</div>
				{/each}
			</div>
		</div>
	{:else if sectionExpanded && sectionPictographs().length === 0}
		<div class="empty-section">
			<p>No options available for this type</p>
		</div>
	{/if}
</div>

<style>
	.option-picker-section {
		width: 100%;
		margin-bottom: 16px;
		background: transparent;
		border: none;
	}

	.pictograph-frame {
		width: 100%;
		padding: 0;
		border: none;
		background: transparent;
	}

	.pictographs-grid {
		display: grid;
		justify-items: center;
		align-items: center;
		width: 100%;
		padding: 8px 16px;
	}

	.pictograph-container {
		position: relative;
		cursor: pointer;
		border: 2px solid transparent;
		border-radius: 6px;
		padding: 4px;
		transition: all 0.2s ease;
		background: var(--background, white);
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.pictograph-container:hover {
		transform: translateY(-2px);
		border-color: var(--primary, #2563eb);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}

	.pictograph-container.selected {
		border-color: var(--primary, #2563eb);
		background: color-mix(in srgb, var(--primary, #2563eb) 10%, transparent);
	}

	.pictograph-container:focus {
		outline: 2px solid var(--primary, #2563eb);
		outline-offset: 2px;
	}

	.empty-section {
		padding: 24px;
		text-align: center;
		color: var(--muted-foreground, #666666);
		font-style: italic;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.pictographs-grid {
			padding: 6px 12px;
		}

		.pictograph-container {
			padding: 3px;
		}
	}

	@media (max-width: 480px) {
		.pictographs-grid {
			padding: 4px 8px;
		}

		.pictograph-container {
			padding: 2px;
		}
	}
</style>
