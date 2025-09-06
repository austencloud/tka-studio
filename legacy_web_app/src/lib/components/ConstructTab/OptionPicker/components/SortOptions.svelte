<script lang="ts">
	import { getContext } from 'svelte'; // Import getContext
	import { fade } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { clickOutside } from '$lib/actions/clickOutside';
	import type { SortMethod } from '../config';
	import { actions, uiState } from '../store';
	import { LAYOUT_CONTEXT_KEY, type LayoutContext } from '../layoutContext'; // Import context key and type

	// Props - None needed related to layout
	// REMOVED: export let isMobileDevice: boolean = false;

	// Consume context
	const layoutContext = getContext<LayoutContext>(LAYOUT_CONTEXT_KEY);
	$: isMobileDevice = $layoutContext.isMobile; // Get from context

	// Component state
	let isOpen = false;
	let buttonRef: HTMLElement;

	// Sort options (remains the same)
	const sortOptions = [
		{ value: 'type', label: 'Sort by Type', icon: '📁' },
		{ value: 'endPosition', label: 'Sort by End Position', icon: '🏁' },
		{ value: 'reversals', label: 'Sort by Reversals', icon: '🔄' }
	] as const;

	// Derived values
	$: selectedOption =
		sortOptions.find((opt) => opt.value === $uiState.sortMethod) || sortOptions[0];

	// Event handlers
	const toggleDropdown = () => (isOpen = !isOpen);
	const closeDropdown = () => isOpen && (isOpen = false);

	function handleSort(method: SortMethod) {
		actions.setSortMethod(method);
		closeDropdown();
	}
</script>

<div class="sort-options" use:clickOutside={closeDropdown} data-testid="sort-options">
	<button
		class="sort-button"
		class:mobile={isMobileDevice}
		bind:this={buttonRef}
		on:click={toggleDropdown}
		aria-label="Change sorting method"
		aria-expanded={isOpen}
		aria-haspopup="listbox"
	>
		<span class="sort-icon" aria-hidden="true">{selectedOption.icon}</span>
		{#if !isMobileDevice}
			<span class="sort-text">Sort</span>
		{/if}
		<span class="dropdown-arrow" aria-hidden="true">{isOpen ? '▲' : '▼'}</span>
	</button>

	{#if isOpen}
		<div
			class="dropdown"
			class:mobile={isMobileDevice}
			transition:fade={{ duration: 150, easing: quintOut }}
			role="listbox"
			aria-label="Sorting options"
		>
			{#each sortOptions as option (option.value)}
				<button
					class="dropdown-item"
					class:selected={$uiState.sortMethod === option.value}
					on:click={() => handleSort(option.value)}
					role="option"
					aria-selected={$uiState.sortMethod === option.value}
				>
					<span class="option-icon" aria-hidden="true">{option.icon}</span>
					<span class="option-text">{option.label}</span>
				</button>
			{/each}
		</div>
	{/if}
</div>

<style>
	/* Styles remain the same */
	.sort-options {
		display: inline-block;
		position: relative;
	}
	.sort-button {
		display: flex;
		align-items: center;
		gap: clamp(4px, 1vw, 6px);
		background-color: #ffffff;
		border: 1px solid #e2e8f0;
		border-radius: 6px;
		padding: clamp(6px, 1.4vw, 10px) clamp(10px, 2vw, 14px);
		font-size: clamp(0.8rem, 2.2vw, 0.95rem);
		font-weight: 500;
		color: #374151;
		cursor: pointer;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
		transition:
			background-color 0.2s ease,
			box-shadow 0.2s ease;
		white-space: nowrap;
	}
	.sort-button:hover {
		background-color: #f9fafb;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
	}
	.sort-button:focus-visible {
		outline: 2px solid #4299e1;
		outline-offset: 1px;
	}
	.sort-icon {
		font-size: 1.2em;
		line-height: 1;
	}
	.dropdown-arrow {
		font-size: 0.7em;
		opacity: 0.7;
		margin-left: auto;
		padding-left: 4px;
	}
	.dropdown {
		position: absolute;
		top: calc(100% + 6px);
		right: 0;
		background-color: white;
		border-radius: 6px;
		border: 1px solid #e2e8f0;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
		min-width: 180px;
		width: max-content;
		z-index: 100;
		overflow: hidden;
	}
	.dropdown-item {
		display: flex;
		align-items: center;
		gap: 8px;
		width: 100%;
		text-align: left;
		padding: 10px 14px;
		border: none;
		background: none;
		cursor: pointer;
		font-size: 0.9rem;
		color: #374151;
		transition: background-color 0.15s ease;
	}
	.dropdown-item:hover {
		background-color: #f1f5f9;
	}
	.dropdown-item.selected {
		background-color: #e5e7eb;
		font-weight: 600;
		color: #1f2937;
	}
	.dropdown-item:focus-visible {
		background-color: #f1f5f9;
		outline: none;
	}
	.option-icon {
		font-size: 1.1rem;
		width: 1.2em;
		text-align: center;
		line-height: 1;
	}
	.option-text {
		flex-grow: 1;
	}
</style>
