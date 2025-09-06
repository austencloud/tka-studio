<script lang="ts">
	import { actStore } from '../../stores/actStore';

	let isEditing = false;
	let titleInput: HTMLInputElement;
	let currentTitle = '';

	// Subscribe to the act title
	$: currentTitle = $actStore.act.title;

	function startEditing() {
		isEditing = true;

		// Focus the input after the DOM updates
		setTimeout(() => {
			if (titleInput) {
				titleInput.focus();
				titleInput.select();
			}
		}, 0);
	}

	function saveTitle() {
		if (currentTitle.trim() === '') {
			currentTitle = 'Untitled Act';
		}

		actStore.updateTitle(currentTitle);
		isEditing = false;
	}

	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			saveTitle();
		} else if (event.key === 'Escape') {
			// Revert to the original title
			currentTitle = $actStore.act.title;
			isEditing = false;
		}
	}

	function handleBlur() {
		saveTitle();
	}
</script>

<div class="title-label">
	{#if isEditing}
		<input
			bind:this={titleInput}
			bind:value={currentTitle}
			on:keydown={handleKeyDown}
			on:blur={handleBlur}
			class="title-input"
			type="text"
			placeholder="Enter act title"
		/>
	{:else}
		<button class="title-text" on:click={startEditing} aria-label="Edit act title" type="button">
			{currentTitle || 'Untitled Act'}
		</button>
	{/if}
</div>

<style>
	.title-label {
		position: relative;
	}

	.title-text {
		font-size: 1.5rem;
		font-weight: 600;
		margin: 0;
		padding: 0.25rem 0.5rem;
		border-radius: 4px;
		cursor: text;
		transition: background-color 0.2s;
		background: none;
		border: none;
		color: inherit;
		text-align: left;
		font-family: inherit;
		width: 100%;
	}

	.title-text:hover {
		background-color: rgba(255, 255, 255, 0.1);
	}

	.title-input {
		font-size: 1.5rem;
		font-weight: 600;
		width: 100%;
		padding: 0.25rem 0.5rem;
		background-color: #333;
		color: #fff;
		border: 1px solid #555;
		border-radius: 4px;
		outline: none;
	}

	.title-input:focus {
		border-color: #3498db;
		box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.3);
	}
</style>
