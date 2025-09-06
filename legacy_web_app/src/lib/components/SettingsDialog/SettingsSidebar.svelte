<script context="module" lang="ts">
    // REMOVED: Lucide type import

    // Export the Section type - icon is now just a string for FA classes
	export type Section = {
		id: string;
		label: string;
		icon: string; // Changed from keyof typeof LucideIconTypes to string
	};
</script>

<script lang="ts">
    // Instance script
	import { createEventDispatcher } from 'svelte';
    // REMOVED: Lucide runtime import
    // Import the Section type for props

	// Props received from parent
	export let sections: Section[] = [];
	export let currentSectionId: string;

	// Dispatcher to notify parent of selection changes
	const dispatch = createEventDispatcher<{ sectionSelect: string }>();

	// Function called when a button is clicked
	function selectSection(id: string) {
		dispatch('sectionSelect', id);
	}

    // REMOVED: getIconComponent function
</script>

<nav class="w-48 flex-shrink-0 border-r border-slate-700 bg-slate-800/50 p-4">
	<ul class="space-y-1">
		{#each sections as section (section.id)}
			<li>
				<button
					on:click={() => selectSection(section.id)}
					class="flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-offset-2 focus:ring-offset-slate-900"
					class:bg-sky-600={currentSectionId === section.id}
					class:text-white={currentSectionId === section.id}
					class:text-slate-400={currentSectionId !== section.id}
					class:hover:bg-slate-700={currentSectionId !== section.id}
					class:hover:text-slate-200={currentSectionId !== section.id}
					aria-current={currentSectionId === section.id ? 'page' : undefined}
				>
					<i class="fa-solid {section.icon} w-5 text-center" aria-hidden="true"></i>
					<span>{section.label}</span>
				</button>
			</li>
		{/each}
	</ul>
</nav>
