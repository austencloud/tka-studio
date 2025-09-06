<!-- src/lib/components/SequenceWorkbench/GraphEditor/GraphEditorToggleTab.svelte -->
<script lang="ts">
	import { createEventDispatcher, onMount } from 'svelte';

	// Props
	export let isExpanded: boolean;
	export let animationDuration: number;
	export let graphEditorHeight: number;

	// Create event dispatcher
	const dispatch = createEventDispatcher<{
	  click: void; // No payload needed
	}>();

	// Label derived from state
	$: label = isExpanded ? 'Collapse' : 'Expand';

	// Update CSS custom properties when values change
	$: if (typeof window !== 'undefined') {
	  document.documentElement.style.setProperty('--graph-editor-offset', `${graphEditorHeight}px`);
	  document.documentElement.style.setProperty('--animation-duration', `${animationDuration}ms`);
	}

	// Set initial values on mount
	onMount(() => {
	  document.documentElement.style.setProperty('--graph-editor-offset', `${graphEditorHeight}px`);
	  document.documentElement.style.setProperty('--animation-duration', `${animationDuration}ms`);
	});

	// Event handler
	function handleClick() {
	  dispatch('click');
	}
  </script>

  <button
	class="toggle-tab"
	on:click={handleClick}
	aria-expanded={isExpanded}
	aria-label={label}
  >
	<span class="icon" class:expanded={isExpanded}>▲</span>
	{label}
  </button>

  <style>
	.toggle-tab {
	  position: absolute;
	  bottom: var(--graph-editor-offset, 0px);
	  left: 0;
	  width: 20%;
	  text-align: center;
	  padding: 10px 20px;
	  background: linear-gradient(135deg, #6a11cb, #2575fc);
	  color: white;
	  font-size: 1rem;
	  font-weight: bold;
	  cursor: pointer;
	  border-radius: 10px 10px 0 0;
	  border: 1px solid #555;
	  transition:
		bottom var(--animation-duration) ease-in-out,
		transform var(--animation-duration) ease-in-out;
	  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
	}

	.toggle-tab:hover {
	  box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);
	}

	.icon {
	  display: inline-block;
	  transition: transform var(--animation-duration) ease-in-out;
	}

	.icon.expanded {
	  transform: rotate(180deg);
	}
  </style>
