<script lang="ts">
	import { uiStore } from '../stores/uiStore';
	import { fade } from 'svelte/transition';

	export let isOpen: boolean = false;

	function handleClose() {
		isOpen = false;
	}
</script>

{#if isOpen}
	<div
		class="settings-backdrop"
		on:click|self={handleClose}
		on:keydown={(e) => e.key === 'Escape' && handleClose()}
		role="dialog"
		tabindex="-1"
		aria-modal="true"
		aria-labelledby="settings-title"
		transition:fade={{ duration: 200 }}
	>
		<div class="settings-panel" transition:fade={{ duration: 150 }}>
			<div class="settings-header">
				<h2 id="settings-title">Settings</h2>
				<button class="close-button" on:click={handleClose} aria-label="Close settings">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="20"
						height="20"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					>
						<line x1="18" y1="6" x2="6" y2="18"></line>
						<line x1="6" y1="6" x2="18" y2="18"></line>
					</svg>
				</button>
			</div>

			<div class="settings-content">
				<section class="settings-section">
					<h3>Confirmation Dialogs</h3>

					<div class="setting-item">
						<label class="toggle-switch">
							<input
								type="checkbox"
								checked={$uiStore.preferences.confirmDeletions}
								on:change={() => uiStore.toggleConfirmDeletions()}
							/>
							<span class="toggle-slider"></span>
						</label>
						<div class="setting-description">
							<span>Confirm before deleting</span>
							<small
								>Show confirmation dialogs when erasing beats, sequences, or the entire act</small
							>
						</div>
					</div>
				</section>
			</div>
		</div>
	</div>
{/if}

<style>
	.settings-backdrop {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000;
	}

	.settings-panel {
		background-color: #2a2a2a;
		border-radius: 8px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
		width: 90%;
		max-width: 500px;
		max-height: 90vh;
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	.settings-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem;
		border-bottom: 1px solid #333;
	}

	.settings-header h2 {
		margin: 0;
		font-size: 1.25rem;
		color: #e0e0e0;
	}

	.close-button {
		background: none;
		border: none;
		color: #999;
		cursor: pointer;
		padding: 0.25rem;
		border-radius: 4px;
		display: flex;
		align-items: center;
		justify-content: center;
		transition:
			color 0.2s,
			background-color 0.2s;
	}

	.close-button:hover {
		color: #fff;
		background-color: rgba(255, 255, 255, 0.1);
	}

	.settings-content {
		padding: 1rem;
		overflow-y: auto;
	}

	.settings-section {
		margin-bottom: 1.5rem;
	}

	.settings-section h3 {
		font-size: 1rem;
		color: #e0e0e0;
		margin-top: 0;
		margin-bottom: 1rem;
		padding-bottom: 0.5rem;
		border-bottom: 1px solid #333;
	}

	.setting-item {
		display: flex;
		align-items: center;
		gap: 1rem;
		margin-bottom: 1rem;
	}

	.setting-description {
		display: flex;
		flex-direction: column;
	}

	.setting-description span {
		font-size: 0.875rem;
		color: #e0e0e0;
	}

	.setting-description small {
		font-size: 0.75rem;
		color: #999;
		margin-top: 0.25rem;
	}

	/* Toggle Switch Styles */
	.toggle-switch {
		position: relative;
		display: inline-block;
		width: 44px;
		height: 24px;
		flex-shrink: 0;
	}

	.toggle-switch input {
		opacity: 0;
		width: 0;
		height: 0;
	}

	.toggle-slider {
		position: absolute;
		cursor: pointer;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: #444;
		transition: 0.4s;
		border-radius: 24px;
	}

	.toggle-slider:before {
		position: absolute;
		content: '';
		height: 18px;
		width: 18px;
		left: 3px;
		bottom: 3px;
		background-color: white;
		transition: 0.4s;
		border-radius: 50%;
	}

	input:checked + .toggle-slider {
		background-color: #3498db;
	}

	input:focus + .toggle-slider {
		box-shadow: 0 0 1px #3498db;
	}

	input:checked + .toggle-slider:before {
		transform: translateX(20px);
	}
</style>
