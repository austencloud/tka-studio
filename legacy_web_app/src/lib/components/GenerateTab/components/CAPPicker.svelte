<script lang="ts" generics="T extends { id: string; label: string; description: string }">
	import CAPButton from './CAPButton.svelte';

	// Use Svelte 5 props rune
	const props = $props<{
		capTypes: T[];
		selectedCapId: string;
		onSelect?: (capId: string) => void;
	}>();

	function handleSelect(capId: string) {
		if (props.onSelect) {
			props.onSelect(capId);
		}
	}

	// Grouping logic using $derived rune
	const groupedCapTypes = $derived({
		mirror: props.capTypes.filter((cap: T) => cap.id.toLowerCase().includes('mirrored')),
		rotate: props.capTypes.filter((cap: T) => cap.id.toLowerCase().includes('rotated')),
		other: props.capTypes.filter(
			(cap: T) =>
				!cap.id.toLowerCase().includes('mirrored') && !cap.id.toLowerCase().includes('rotated')
		)
	});
</script>

<div class="cap-picker">
	{#each Object.entries(groupedCapTypes) as [groupName, typesInGroup]}
		{#if typesInGroup.length > 0}
			<div class="cap-group">
				<h5 class="group-title">{groupName.charAt(0).toUpperCase() + groupName.slice(1)} Types</h5>
				<div class="cap-buttons-list">
					{#each typesInGroup as capType (capType.id)}
						<CAPButton
							{capType}
							selected={props.selectedCapId === capType.id}
							onClick={() => handleSelect(capType.id)}
						/>
					{/each}
				</div>
			</div>
		{/if}
	{/each}
</div>

<style>
	.cap-picker {
		display: flex;
		flex-direction: column;
		gap: 1rem; /* Increased gap between groups */
	}
	.cap-group {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}
	.group-title {
		font-size: 0.875rem;
		font-weight: 500;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
		margin: 0;
		padding-bottom: 0.25rem;
		border-bottom: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
		text-transform: capitalize;
	}
	.cap-buttons-list {
		display: flex;
		flex-direction: column;
		gap: 0.375rem; /* Slightly reduced gap between buttons */
	}
	/* Removed unused CSS selectors as we're now using the CAPButton component */
</style>
