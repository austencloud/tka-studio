<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import AccordionSection from './AccordionSection.svelte';
	import QuickAccessSection from './QuickAccessSection.svelte';

	const dispatch = createEventDispatcher();

	// Filter configuration matching desktop app exactly
	const filterSections = [
		{
			title: '📝 Starting Letter',
			type: 'starting_letter',
			options: [
				// A-Z alphabet options (fallback - would be populated from data in real app)
				{ label: 'A', value: 'A' },
				{ label: 'B', value: 'B' },
				{ label: 'C', value: 'C' },
				{ label: 'D', value: 'D' },
				{ label: 'E', value: 'E' },
				{ label: 'F', value: 'F' },
				{ label: 'G', value: 'G' },
				{ label: 'H', value: 'H' },
				{ label: 'I', value: 'I' },
				{ label: 'J', value: 'J' },
				{ label: 'K', value: 'K' },
				{ label: 'L', value: 'L' },
				{ label: 'M', value: 'M' },
				{ label: 'N', value: 'N' },
				{ label: 'O', value: 'O' },
				{ label: 'P', value: 'P' },
				{ label: 'Q', value: 'Q' },
				{ label: 'R', value: 'R' },
				{ label: 'S', value: 'S' },
				{ label: 'T', value: 'T' },
				{ label: 'U', value: 'U' },
				{ label: 'V', value: 'V' },
				{ label: 'W', value: 'W' },
				{ label: 'X', value: 'X' },
				{ label: 'Y', value: 'Y' },
				{ label: 'Z', value: 'Z' }
			]
		},
		{
			title: '📏 Length',
			type: 'length',
			options: [
				// Common sequence lengths (fallback - would be populated from data in real app)
				{ label: '3', value: '3' },
				{ label: '4', value: '4' },
				{ label: '5', value: '5' },
				{ label: '6', value: '6' },
				{ label: '7', value: '7' },
				{ label: '8', value: '8' },
				{ label: '9', value: '9' },
				{ label: '10', value: '10' },
				{ label: '11', value: '11' },
				{ label: '12', value: '12' }
			]
		},
		{
			title: '📊 Difficulty',
			type: 'difficulty',
			options: [
				{ label: '🟢 Beginner', value: 'beginner' },
				{ label: '🟡 Intermediate', value: 'intermediate' },
				{ label: '🔴 Advanced', value: 'advanced' }
			]
		},
		{
			title: '🎯 Start Position',
			type: 'starting_position',
			options: [
				// Common starting positions (fallback - would be populated from data in real app)
				{ label: 'Alpha', value: 'Alpha' },
				{ label: 'Beta', value: 'Beta' },
				{ label: 'Gamma', value: 'Gamma' }
			]
		},
		{
			title: '👤 Author',
			type: 'author',
			options: [
				// Demo authors (fallback - would be populated from data in real app)
				{ label: 'Demo Author', value: 'Demo Author' },
				{ label: 'Test User', value: 'Test User' },
				{ label: 'Sample Creator', value: 'Sample Creator' }
			]
		},
		{
			title: '🎨 Grid Style',
			type: 'grid_mode',
			options: [
				{ label: '💎 Diamond', value: 'diamond' },
				{ label: '⬜ Box', value: 'box' },
				{ label: '🎭 Mixed', value: 'mixed' }
			]
		}
	];

	// Track active filter state
	let activeFilter: { type: string; value: any } | null = null;

	// Track which accordion section is currently expanded
	// Auto-open the first section (Starting Position) like desktop app
	let currentExpandedSection: string | null = filterSections[0]?.type || null;

	function handleFilterSelection(event: CustomEvent) {
		const { type, value } = event.detail;
		activeFilter = { type, value };

		// Emit filter selected event
		dispatch('filterSelected', { type, value });
	}

	function handleQuickAccess(event: CustomEvent) {
		const { type, value } = event.detail;
		activeFilter = { type, value };

		// Emit filter selected event
		dispatch('filterSelected', { type, value });
	}

	function handleExpansionRequest(event: CustomEvent) {
		const { type } = event.detail;

		// If the requested section is already expanded, collapse it
		if (currentExpandedSection === type) {
			currentExpandedSection = null;
			return;
		}

		// Otherwise, expand the requested section (this will collapse others)
		currentExpandedSection = type;
	}
</script>

<div class="filter-selection-panel">
	<div class="main-container">
		<div class="content-container">
			<!-- Header Section (fixed height) -->
			<div class="header-section">
				<!-- Header + Quick Access on same line -->
				<div class="header-row">
					<!-- Header on left -->
					<div class="header-content">
						<h1 class="header-title">Sequence Library</h1>
					</div>

					<!-- Stretch to push Quick Access to right -->
					<div class="header-spacer"></div>

					<!-- Quick Access buttons on right -->
					<QuickAccessSection on:quickAccess={handleQuickAccess} />
				</div>
			</div>

			<!-- Categories Section (expandable content area) -->
			<div class="categories-section">
				<!-- Section title -->
				<div class="section-title">Browse by Category</div>

				{#each filterSections as section}
					<AccordionSection
						title={section.title}
						type={section.type}
						options={section.options}
						isActive={activeFilter?.type === section.type}
						isExpanded={currentExpandedSection === section.type}
						on:filterSelected={handleFilterSelection}
						on:expansionRequested={handleExpansionRequest}
					/>
				{/each}
			</div>
		</div>
	</div>
</div>

<style>
	.filter-selection-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow: hidden;
	}

	/* Main container with centering */
	/* Main container takes full width */
	.main-container {
		display: flex;
		height: 100%;
		align-items: stretch;
		width: 100%;
	}

	/* Content container takes full available width */
	.content-container {
		width: 100%;
		display: flex;
		flex-direction: column;
		height: 100%;
		padding: 40px;
	}

	/* Header Section (fixed height) */
	.header-section {
		flex-shrink: 0;
		max-height: 120px;
		margin-bottom: 36px;
	}

	.header-row {
		display: flex;
		align-items: center;
		gap: var(--spacing-lg);
	}

	.header-content {
		flex: 0 0 auto;
	}

	.header-spacer {
		flex: 1;
	}

	.header-title {
		font-size: 28px;
		font-weight: 700;
		color: white;
		margin: 0;
		text-align: center;
	}

	/* Categories Section (expandable content area) */
	.categories-section {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: 8px;
		overflow-y: auto;
		padding-right: var(--spacing-xs);
		margin-top: 10px;
		padding-left: 20px;
		padding-right: 20px;
	}

	.section-title {
		text-align: center;
		font-size: 18px;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.9);
		margin-bottom: 16px;
	}

	/* Custom scrollbar */
	.categories-section::-webkit-scrollbar {
		width: 6px;
	}

	.categories-section::-webkit-scrollbar-track {
		background: rgba(255, 255, 255, 0.05);
		border-radius: 3px;
	}

	.categories-section::-webkit-scrollbar-thumb {
		background: rgba(255, 255, 255, 0.2);
		border-radius: 3px;
		transition: var(--transition-fast);
	}

	.categories-section::-webkit-scrollbar-thumb:hover {
		background: rgba(255, 255, 255, 0.3);
	}

	/* Responsive Design */
	@media (max-width: 1024px) {
		.content-container {
			min-width: 400px;
			max-width: 500px;
			padding: 30px;
		}
	}

	@media (max-width: 768px) {
		.content-container {
			min-width: 300px;
			max-width: 400px;
			padding: 20px;
		}

		.header-row {
			flex-direction: column;
			gap: var(--spacing-md);
			align-items: flex-start;
		}

		.header-spacer {
			display: none;
		}

		.header-title {
			font-size: 24px;
		}
	}
</style>
