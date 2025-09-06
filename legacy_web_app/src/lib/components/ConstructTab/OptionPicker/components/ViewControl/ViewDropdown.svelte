<script lang="ts">
	import { fade } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import type { ViewOption } from './types';

	export let isOpen: boolean;
	export let selectedViewOption: ViewOption;
	export let viewOptions: readonly ViewOption[];
	export let onSelect: (option: ViewOption) => void;
	export let onKeydown: (event: KeyboardEvent) => void;

	// No need to track the dropdown reference
</script>

{#if isOpen}
	<div
		class="dropdown"
		transition:fade={{ duration: 200, easing: quintOut }}
		role="listbox"
		aria-label="View options"
		onkeydown={onKeydown}
		tabindex="-1"
	>
		{#each viewOptions as option (option.value)}
			<button
				class="dropdown-item"
				class:selected={selectedViewOption.value === option.value}
				onclick={() => onSelect(option)}
				role="option"
				aria-selected={selectedViewOption.value === option.value}
				title={option.description}
			>
				<span class="option-icon" aria-hidden="true">{option.icon}</span>
				<span class="option-text">{option.label}</span>
				{#if option.description}
					<span class="option-description">{option.description}</span>
				{/if}
			</button>
		{/each}
	</div>
{/if}

<style>
	.dropdown {
		position: absolute;
		top: calc(100% + 10px);
		right: 0; /* Changed from left: 0; */
		background-color: rgba(15, 23, 42, 0.95); /* Very dark blue with transparency */
		border-radius: 12px;
		border: 1px solid rgba(71, 85, 105, 0.6);
		box-shadow:
			0 10px 25px -5px rgba(0, 0, 0, 0.25),
			0 8px 10px -6px rgba(0, 0, 0, 0.15),
			0 0 0 1px rgba(255, 255, 255, 0.1);
		min-width: 220px;
		width: max-content;
		z-index: 100;
		overflow: hidden;
		backdrop-filter: blur(12px);
		-webkit-backdrop-filter: blur(12px);
		transform-origin: top right; /* Changed from top left */
		transition: box-shadow 0.2s ease;
	}

	/* Remove outline when dropdown is focused */
	.dropdown:focus {
		outline: none;
	}

	/* Add subtle glow when dropdown is focused */
	.dropdown:focus-visible {
		box-shadow:
			0 10px 25px -5px rgba(0, 0, 0, 0.25),
			0 8px 10px -6px rgba(0, 0, 0, 0.15),
			0 0 0 3px rgba(59, 130, 246, 0.3);
	}

	.dropdown-item {
		display: flex;
		align-items: center;
		gap: 12px;
		width: 100%;
		text-align: left;
		padding: 12px 16px;
		border: none;
		background: none;
		cursor: pointer;
		font-size: 1rem;
		color: #e2e8f0; /* Light gray text */
		transition: all 0.2s ease;
		position: relative;
		overflow: hidden;
	}

	/* Highlight effect for selected item */
	.dropdown-item.selected {
		background: linear-gradient(to right, rgba(59, 130, 246, 0.2), rgba(59, 130, 246, 0.1));
		font-weight: 600;
		color: #93c5fd; /* Light blue text */
	}

	/* Subtle hover effect with gradient - placed AFTER selected to have higher specificity */
	.dropdown-item:hover {
		background: linear-gradient(to right, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05));
		color: #f8fafc;
	}

	/* Ensure hover effect overrides selected state when hovering - using !important to guarantee precedence */
	.dropdown-item.selected:hover {
		background: linear-gradient(
			to right,
			rgba(59, 130, 246, 0.15),
			rgba(59, 130, 246, 0.07)
		) !important;
		color: #f8fafc !important;
	}

	/* Focus visible styling that doesn't interfere with hover states */
	.dropdown-item:focus-visible {
		outline: none;
		box-shadow: inset 0 0 0 2px rgba(59, 130, 246, 0.5);
	}

	/* Only apply background color when not hovering */
	.dropdown-item:focus-visible:not(:hover) {
		background-color: rgba(59, 130, 246, 0.15);
	}

	/* Subtle divider between items */
	.dropdown-item:not(:last-child)::after {
		content: '';
		position: absolute;
		bottom: 0;
		left: 16px;
		right: 16px;
		height: 1px;
		background: linear-gradient(to right, transparent, rgba(148, 163, 184, 0.2), transparent);
	}

	.option-icon {
		font-size: 1.4rem;
		width: 1.5em;
		height: 1.5em;
		display: flex;
		align-items: center;
		justify-content: center;
		text-align: center;
		line-height: 1;
		color: #94a3b8; /* Muted blue-gray */
		background: rgba(51, 65, 85, 0.4);
		border-radius: 8px;
		padding: 6px;
		transition: all 0.2s ease;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	/* Selected item icon styling */
	.dropdown-item.selected .option-icon {
		background: rgba(59, 130, 246, 0.3);
		color: #3b82f6; /* Bright blue */
		box-shadow:
			0 0 0 1px rgba(59, 130, 246, 0.5),
			0 2px 4px rgba(0, 0, 0, 0.2);
	}

	/* Hover icon styling - placed AFTER selected to have higher specificity */
	.dropdown-item:hover .option-icon {
		transform: scale(1.05);
		background: rgba(59, 130, 246, 0.2);
		color: #bfdbfe; /* Lighter blue */
	}

	/* Ensure hover effect overrides selected state for icons when hovering - using !important */
	.dropdown-item.selected:hover .option-icon {
		transform: scale(1.05) !important;
		background: rgba(59, 130, 246, 0.25) !important;
		color: #bfdbfe !important; /* Lighter blue */
		box-shadow:
			0 0 0 1px rgba(59, 130, 246, 0.4),
			0 2px 4px rgba(0, 0, 0, 0.15) !important;
	}

	.option-text {
		flex-grow: 1;
		font-weight: 500;
		letter-spacing: 0.01em;
	}

	/* Description styling */
	.option-description {
		display: block;
		font-size: 0.8rem;
		color: rgba(148, 163, 184, 0.9);
		margin-top: 4px;
		font-weight: normal;
		max-width: 90%;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	/* Selected item description styling */
	.dropdown-item.selected .option-description {
		color: rgba(147, 197, 253, 0.9);
	}

	/* Hover description styling - placed AFTER selected to have higher specificity */
	.dropdown-item:hover .option-description {
		color: rgba(191, 219, 254, 0.9);
	}

	/* Ensure hover effect overrides selected state for descriptions when hovering */
	.dropdown-item.selected:hover .option-description {
		color: rgba(191, 219, 254, 0.9);
	}

	/* Add a subtle indicator for the selected item */
	.dropdown-item.selected::before {
		content: '';
		position: absolute;
		left: 0;
		top: 0;
		bottom: 0;
		width: 3px;
		background: #3b82f6; /* Bright blue */
		box-shadow: 0 0 8px rgba(59, 130, 246, 0.6);
	}

	@media (max-width: 640px) {
		.dropdown {
			min-width: 180px;
		}

		.dropdown-item {
			padding: 8px 10px;
			font-size: 0.9rem;
		}

		.option-icon {
			font-size: 1.1rem;
			padding: 4px;
		}

		.option-description {
			display: none; /* Hide descriptions on mobile to save space */
		}
	}
</style>
