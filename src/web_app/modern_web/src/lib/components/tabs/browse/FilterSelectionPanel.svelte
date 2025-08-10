<script lang="ts">
	import AccordionSection from './AccordionSection.svelte';
	import QuickAccessSection from './QuickAccessSection.svelte';

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	const { onFilterSelected = () => {} } = $props<{
		onFilterSelected?: (data: { type: string; value: unknown }) => void;
	}>();

	// Filter configuration matching desktop app exactly
	const filterSections = [
		{
			title: '📝 Starting Letter',
			type: 'starting_letter',
			sections: [
				// Type 1 (A-Z, W-, X-, Y-, Z-)
				['A', 'B', 'C', 'D', 'E', 'F'],
				['G', 'H', 'I', 'J', 'K', 'L'],
				['M', 'N', 'O', 'P', 'Q', 'R'],
				['S', 'T', 'U', 'V'],
				['W', 'X', 'Y', 'Z'],
				['W-', 'X-', 'Y-', 'Z-'],
				// Type 2 (Shifted Greek)
				['Σ', 'Δ', 'θ', 'Ω'],
				// Type 3 (Cross-Shifted Latin/Greek)
				['Σ-', 'Δ-', 'θ-', 'Ω-'],
				// Type 4 (Phi, Psi, Lambda)
				['Φ', 'Ψ', 'Λ'],
				// Type 5 (Phi-, Psi-, Lambda-)
				['Φ-', 'Ψ-', 'Λ-'],
				// Type 6 (alpha, beta, Gamma)
				['α', 'β', 'Γ'],
			],
			options: [], // Will be populated from sections
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
				{ label: '12', value: '12' },
			],
		},
		{
			title: '📊 Difficulty',
			type: 'difficulty',
			options: [
				{ label: 'Beginner', value: 'beginner' },
				{ label: 'Intermediate', value: 'intermediate' },
				{ label: 'Advanced', value: 'advanced' },
			],
		},
		{
			title: '🎯 Start Position',
			type: 'starting_position',
			options: [
				{ label: 'Alpha', value: 'alpha' },
				{ label: 'Beta', value: 'beta' },
				{ label: 'Gamma', value: 'gamma' },
			],
		},
		{
			title: '👤 Author',
			type: 'author',
			options: [
				// Demo authors (fallback - would be populated from data in real app)
				{ label: 'Demo Author', value: 'Demo Author' },
				{ label: 'Test User', value: 'Test User' },
				{ label: 'Sample Creator', value: 'Sample Creator' },
			],
		},
		{
			title: '🎨 Grid Mode',
			type: 'grid_mode',
			options: [
				{ label: 'Diamond', value: 'diamond' },
				{ label: 'Box', value: 'box' },
				{ label: 'Skewed', value: 'skewed' },
			],
		},
	];

	// ✅ PURE RUNES: Track active filter state
	let activeFilter: { type: string; value: unknown } | null = $state(null);

	// ✅ PURE RUNES: Track which accordion section is currently expanded
	// Auto-open the first section (Starting Position) like desktop app
	let currentExpandedSection: string | null = $state(filterSections[0]?.type || null);

	function handleFilterSelection(data: { type: string; value: unknown }) {
		activeFilter = { type: data.type, value: data.value };

		// Call callback prop instead of dispatching event
		onFilterSelected({ type: data.type, value: data.value });
	}

	function handleQuickAccess(data: { type: string; value: unknown }) {
		activeFilter = { type: data.type, value: data.value };

		// Call callback prop instead of dispatching event
		onFilterSelected({ type: data.type, value: data.value });
	}

	function handleExpansionRequest(data: { type: string; title: string }) {
		const { type } = data;

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
					<QuickAccessSection onQuickAccess={handleQuickAccess} />
				</div>
			</div>

			<!-- Categories Section (expandable content area) -->
			<div class="categories-section">
				<!-- All Filter Sections using Accordion -->
				{#each filterSections as section}
					<AccordionSection
						title={section.title}
						type={section.type}
						options={section.options}
						sections={section.sections || []}
						isActive={activeFilter?.type === section.type}
						isExpanded={currentExpandedSection === section.type}
						onFilterSelected={handleFilterSelection}
						onExpansionRequested={handleExpansionRequest}
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
		gap: 6px;
		overflow-y: auto;
		padding-right: var(--spacing-xs);
		margin-top: 5px;
		padding-left: 15px;
		padding-right: 15px;
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
