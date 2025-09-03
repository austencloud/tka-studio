<script lang="ts">
	import TitleLabel from './TitleLabel.svelte';
	import { actStore } from '../../stores/actStore';
	import { uiStore } from '../../stores/uiStore';
	import ConfirmationModal from '../../../shared/ConfirmationModal.svelte';
	import SettingsPanel from '../../settings/SettingsPanel.svelte';

	// Get current date in the format "Month Day, Year"
	const currentDate = new Date().toLocaleDateString('en-US', {
		month: 'long',
		day: 'numeric',
		year: 'numeric'
	});

	// Mock author name - in a real implementation, this would come from user settings
	const author = 'John Doe';

	// Modal states
	let isEraseActModalOpen = false;
	let isSettingsPanelOpen = false;

	// Handle erase act button click
	function handleEraseAct() {
		if ($uiStore.preferences.confirmDeletions) {
			isEraseActModalOpen = true;
		} else {
			actStore.eraseAct();
		}
	}

	// Handle confirmation from modal
	function confirmEraseAct() {
		actStore.eraseAct();
		isEraseActModalOpen = false;
	}

	// Toggle settings panel
	function toggleSettings() {
		isSettingsPanelOpen = !isSettingsPanelOpen;
	}
</script>

<div class="act-header">
	<div class="header-top">
		<TitleLabel />

		<div class="header-actions">
			<button
				class="settings-button"
				on:click={toggleSettings}
				aria-label="Open settings"
				title="Open settings"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="16"
					height="16"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<circle cx="12" cy="12" r="3"></circle>
					<path
						d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"
					></path>
				</svg>
				<span>Settings</span>
			</button>

			<button
				class="erase-act-button"
				on:click={handleEraseAct}
				aria-label="Erase entire act"
				title="Erase entire act"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="16"
					height="16"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<path d="M3 6h18"></path>
					<path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
					<path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
				</svg>
				<span>Erase Act</span>
			</button>
		</div>
	</div>

	<div class="metadata">
		<div class="date">{currentDate}</div>
		<div class="author">Choreography by {author}</div>
	</div>
</div>

<ConfirmationModal
	isOpen={isEraseActModalOpen}
	title="Erase Entire Act"
	message="Are you sure you want to erase the entire act? This will clear all sequences but keep the title and structure."
	confirmText="Erase Act"
	cancelText="Cancel"
	confirmButtonClass="danger"
	on:confirm={confirmEraseAct}
	on:close={() => (isEraseActModalOpen = false)}
/>

<SettingsPanel bind:isOpen={isSettingsPanelOpen} />

<style>
	.act-header {
		display: flex;
		flex-direction: column;
		padding: 1rem;
		background-color: #252525;
		border-bottom: 1px solid #333;
	}

	.header-top {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.metadata {
		display: flex;
		justify-content: space-between;
		margin-top: 0.5rem;
		font-size: 0.875rem;
		color: #999;
	}

	.header-actions {
		display: flex;
		gap: 0.5rem;
	}

	.settings-button,
	.erase-act-button {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 0.75rem;
		color: #e0e0e0;
		border: none;
		border-radius: 4px;
		font-size: 0.875rem;
		cursor: pointer;
		transition: background-color 0.2s;
	}

	.settings-button {
		background-color: rgba(52, 152, 219, 0.2);
	}

	.settings-button:hover {
		background-color: rgba(52, 152, 219, 0.5);
	}

	.erase-act-button {
		background-color: rgba(231, 76, 60, 0.2);
	}

	.erase-act-button:hover {
		background-color: rgba(231, 76, 60, 0.5);
	}

	@media (max-width: 640px) {
		.metadata {
			flex-direction: column;
			gap: 0.25rem;
		}
	}
</style>
