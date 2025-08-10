<script lang="ts">
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';
	import CategoryButton from './CategoryButton.svelte';

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	const {
		title,
		type,
		options = [],
		sections = [],
		isActive = false,
		isExpanded = false,
		onExpansionRequested = () => {},
		onFilterSelected = () => {},
	} = $props<{
		title: string;
		type: string;
		options: unknown[];
		sections?: string[][];
		isActive?: boolean;
		isExpanded?: boolean;
		onExpansionRequested?: (data: { type: string; title: string }) => void;
		onFilterSelected?: (data: { type: string; value: unknown }) => void;
	}>();

	// ✅ PURE RUNES: State management with direct runes
	let contentElement = $state<HTMLDivElement | null>(null);
	let needsScroll = $state(false);
	let mounted = $state(false);

	// ✅ PURE RUNES: Simple overflow detection for automatic scrolling
	function checkIfScrollNeeded() {
		if (!contentElement) return;

		const contentHeight = contentElement.scrollHeight;
		const visibleHeight = contentElement.clientHeight;

		console.log(`Scroll check for ${type}:`, {
			contentHeight,
			visibleHeight,
			needsScroll: contentHeight > visibleHeight,
		});
		needsScroll = contentHeight > visibleHeight;
	}

	// ✅ PURE RUNES: Effect for scroll detection when expanded
	$effect(() => {
		if (isExpanded && contentElement) {
			// Immediate check
			checkIfScrollNeeded();
			// Small delay to allow content to render
			setTimeout(checkIfScrollNeeded, 50);
			// Additional check after a longer delay for complex layouts
			setTimeout(checkIfScrollNeeded, 200);
			// Final check after transition completes
			setTimeout(checkIfScrollNeeded, 350);
		}
	});

	// ✅ PURE RUNES: Mount effect for resize handling
	$effect(() => {
		if (!mounted) {
			mounted = true;

			// Setup resize observer for better detection
			const resizeObserver = new ResizeObserver(() => {
				if (isExpanded && contentElement) {
					setTimeout(checkIfScrollNeeded, 50);
				}
			});

			// Setup window resize listener as backup
			const handleResize = () => {
				if (isExpanded && contentElement) {
					setTimeout(checkIfScrollNeeded, 100);
				}
			};

			window.addEventListener('resize', handleResize);

			// Cleanup
			return () => {
				resizeObserver.disconnect();
				window.removeEventListener('resize', handleResize);
			};
		}
		// Return undefined for the else case
		return undefined;
	});

	// ✅ PURE RUNES: Effect to observe content element when it changes
	$effect(() => {
		if (contentElement && mounted) {
			const resizeObserver = new ResizeObserver(() => {
				if (isExpanded) {
					setTimeout(checkIfScrollNeeded, 50);
				}
			});

			resizeObserver.observe(contentElement);

			return () => {
				resizeObserver.disconnect();
			};
		}
		// Return undefined for the else case
		return undefined;
	});

	// ✅ PURE RUNES: Modern event handling without dispatchers
	function toggleExpansion() {
		onExpansionRequested({ type, title });
	}

	// ✅ PURE RUNES: Handle filter selection from category buttons
	function handleFilterSelection(data: { type: string; value: string }) {
		onFilterSelected(data);
	} // ✅ PURE RUNES: Modern letter selection handling
	function handleLetterSelection(letter: string) {
		onFilterSelected({ type, value: letter });
	}

	// ✅ PURE RUNES: Effect for resize handling
	$effect(() => {
		function handleResize() {
			if (isExpanded) {
				setTimeout(checkIfScrollNeeded, 100);
			}
		}

		window.addEventListener('resize', handleResize);

		return () => {
			window.removeEventListener('resize', handleResize);
		};
	});
</script>

<div class="accordion-section" class:expanded={isExpanded} class:active={isActive}>
	<!-- Accordion Header -->
	<button
		class="accordion-header"
		class:expanded={isExpanded}
		onclick={toggleExpansion}
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
		<div class="accordion-content" transition:slide={{ duration: 300, easing: cubicInOut }}>
			<div class="content-inner" class:needs-scroll={needsScroll} bind:this={contentElement}>
				{#if type === 'starting_letter'}
					<!-- Special letter grid layout for Starting Letter section -->
					<div class="letter-grid-container">
						{#each sections as row}
							<div class="letter-row">
								{#each row as letter}
									<button
										class="letter-button"
										onclick={() => handleLetterSelection(letter)}
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
								onSelected={(value) => handleFilterSelection({ type, value })}
							/>
						{/each}
					</div>
				{:else}
					<!-- Standard button grid for other filters -->
					<div class="options-grid standard-grid">
						{#each options as option}
							<CategoryButton
								{option}
								onSelected={(value) => handleFilterSelection({ type, value })}
							/>
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
		/* Default: allow content to expand naturally, no scrolling */
		max-height: none;
		overflow: visible;
	}

	/* Only add scrolling when needed */
	.content-inner.needs-scroll {
		max-height: min(60vh, 400px); /* More reasonable max height */
		overflow-y: auto;
		overflow-x: hidden;
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
		/* Let it expand naturally - scrolling handled by parent */
		overflow: visible;
		/* Smooth scrolling */
		scroll-behavior: smooth;
	}

	/* Stylized scrollbar for content when scrolling is needed */
	.content-inner.needs-scroll::-webkit-scrollbar {
		width: 8px;
	}

	.content-inner.needs-scroll::-webkit-scrollbar-track {
		background: rgba(255, 255, 255, 0.05);
		border-radius: 4px;
		margin: 4px 0;
	}

	.content-inner.needs-scroll::-webkit-scrollbar-thumb {
		background: rgba(255, 255, 255, 0.2);
		border-radius: 4px;
		transition: all var(--transition-fast);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.content-inner.needs-scroll::-webkit-scrollbar-thumb:hover {
		background: rgba(255, 255, 255, 0.35);
		border-color: rgba(255, 255, 255, 0.2);
		transform: scaleX(1.2);
	}

	.content-inner.needs-scroll::-webkit-scrollbar-thumb:active {
		background: rgba(255, 255, 255, 0.5);
	}

	/* Firefox scrollbar styling */
	.content-inner.needs-scroll {
		scrollbar-width: thin;
		scrollbar-color: rgba(255, 255, 255, 0.2) rgba(255, 255, 255, 0.05);
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

	@media (max-width: 480px) {
		.letter-button {
			min-width: 32px;
			height: 32px;
			font-size: var(--font-size-sm);
		}
	}
</style>
