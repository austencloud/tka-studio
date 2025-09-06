<script lang="ts">
	import { settingsStore } from '$lib/state/stores/settings/settings.store';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { browser } from '$app/environment';

	// Get the current haptic feedback setting
	const hapticFeedback = $derived(settingsStore.getSnapshot().hapticFeedback);

	// Check if haptic feedback is supported
	let isSupported = $state(false);

	// Initialize on mount
	$effect(() => {
		if (browser) {
			isSupported = hapticFeedbackService.isHapticFeedbackSupported();
		}
	});

	// Toggle haptic feedback
	function toggleHapticFeedback() {
		// Update the setting
		settingsStore.setHapticFeedback(!hapticFeedback);

		// If enabling, provide a sample haptic feedback
		if (!hapticFeedback && browser) {
			setTimeout(() => {
				hapticFeedbackService.trigger('success');
			}, 100);
		}
	}

	// Test different haptic feedback patterns
	function testHapticFeedback(type: 'selection' | 'success' | 'warning' | 'error' | 'navigation') {
		if (browser && hapticFeedback) {
			hapticFeedbackService.trigger(type);
		}
	}
</script>

<div class="haptic-tab">
	<div class="settings-section">
		<h3>Haptic Feedback</h3>

		{#if !isSupported}
			<div class="not-supported-message">
				<i class="fa-solid fa-exclamation-triangle"></i>
				<p>Haptic feedback is not supported on this device or browser.</p>
			</div>
		{/if}

		<div class="setting-item">
			<div class="setting-info">
				<span class="setting-label">Enable Haptic Feedback</span>
				<span class="setting-description">
					Vibration feedback for touch interactions on mobile devices
				</span>
			</div>
			<div class="setting-control">
				<label class="switch">
					<input
						type="checkbox"
						checked={hapticFeedback}
						onchange={toggleHapticFeedback}
						aria-label="Toggle haptic feedback"
						disabled={!isSupported}
					>
					<span class="slider round"></span>
				</label>
			</div>
		</div>

		{#if isSupported && hapticFeedback}
			<div class="test-section">
				<h4>Test Haptic Feedback</h4>
				<p class="test-description">Tap the buttons below to test different haptic feedback patterns</p>

				<div class="test-buttons">
					<button
						class="test-button"
						onclick={() => testHapticFeedback('selection')}
						aria-label="Test selection feedback"
					>
						<i class="fa-solid fa-hand-pointer"></i>
						<span>Selection</span>
					</button>

					<button
						class="test-button"
						onclick={() => testHapticFeedback('success')}
						aria-label="Test success feedback"
					>
						<i class="fa-solid fa-check-circle"></i>
						<span>Success</span>
					</button>

					<button
						class="test-button"
						onclick={() => testHapticFeedback('warning')}
						aria-label="Test warning feedback"
					>
						<i class="fa-solid fa-exclamation-triangle"></i>
						<span>Warning</span>
					</button>

					<button
						class="test-button"
						onclick={() => testHapticFeedback('error')}
						aria-label="Test error feedback"
					>
						<i class="fa-solid fa-times-circle"></i>
						<span>Error</span>
					</button>

					<button
						class="test-button"
						onclick={() => testHapticFeedback('navigation')}
						aria-label="Test navigation feedback"
					>
						<i class="fa-solid fa-arrow-right"></i>
						<span>Navigation</span>
					</button>
				</div>
			</div>
		{/if}
	</div>

	<div class="settings-section">
		<h3>When Haptic Feedback is Used</h3>
		<ul class="feedback-uses">
			<li><i class="fa-solid fa-hand-pointer"></i> When selecting pictographs</li>
			<li><i class="fa-solid fa-toggle-on"></i> When toggling settings</li>
			<li><i class="fa-solid fa-check-circle"></i> When completing a sequence</li>
			<li><i class="fa-solid fa-share-alt"></i> When sharing/exporting content</li>
			<li><i class="fa-solid fa-exchange-alt"></i> When navigating between sections</li>
			<li><i class="fa-solid fa-trash-alt"></i> When performing deletions</li>
		</ul>
	</div>
</div>

<style>
	.haptic-tab {
		padding: 1rem;
		overflow-y: auto;
		max-height: 60vh;
	}

	.settings-section {
		margin-bottom: 1.5rem;
	}

	h3 {
		margin: 0 0 1rem 0;
		font-size: 1.1rem;
		color: var(--color-text-primary, white);
		border-bottom: 1px solid rgba(108, 156, 233, 0.2);
		padding-bottom: 0.5rem;
	}

	h4 {
		margin: 1rem 0 0.5rem 0;
		font-size: 1rem;
		color: var(--color-text-primary, white);
	}

	.not-supported-message {
		display: flex;
		align-items: center;
		background-color: rgba(255, 193, 7, 0.2);
		border-left: 3px solid #ffc107;
		padding: 0.75rem;
		margin-bottom: 1rem;
		border-radius: 0.25rem;
	}

	.not-supported-message i {
		color: #ffc107;
		margin-right: 0.75rem;
		font-size: 1.25rem;
	}

	.not-supported-message p {
		margin: 0;
		color: var(--color-text-primary, white);
	}

	.setting-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem 0;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	}

	.setting-info {
		flex: 1;
	}

	.setting-label {
		display: block;
		font-weight: 500;
		margin-bottom: 0.25rem;
		color: var(--color-text-primary, white);
	}

	.setting-description {
		display: block;
		font-size: 0.85rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
	}

	.setting-control {
		margin-left: 1rem;
	}

	.test-description {
		font-size: 0.9rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
		margin-bottom: 1rem;
	}

	.test-buttons {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
		gap: 0.75rem;
	}

	.test-button {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 0.75rem;
		background-color: rgba(108, 156, 233, 0.1);
		border: 1px solid rgba(108, 156, 233, 0.3);
		border-radius: 0.5rem;
		color: var(--color-text-primary, white);
		transition: all 0.2s ease;
		cursor: pointer;
	}

	.test-button i {
		font-size: 1.25rem;
		margin-bottom: 0.5rem;
	}

	.test-button:hover {
		background-color: rgba(108, 156, 233, 0.2);
		transform: translateY(-2px);
	}

	.test-button:active {
		transform: translateY(0);
	}

	.feedback-uses {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.feedback-uses li {
		padding: 0.5rem 0;
		color: var(--color-text-primary, white);
		display: flex;
		align-items: center;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	}

	.feedback-uses li i {
		margin-right: 0.75rem;
		color: #6c9ce9;
		width: 20px;
		text-align: center;
	}

	/* Toggle Switch Styles */
	.switch {
		position: relative;
		display: inline-block;
		width: 50px;
		height: 24px;
	}

	.switch input {
		opacity: 0;
		width: 0;
		height: 0;
	}

	.slider {
		position: absolute;
		cursor: pointer;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: #ccc;
		transition: 0.3s;
	}

	.slider:before {
		position: absolute;
		content: "";
		height: 18px;
		width: 18px;
		left: 3px;
		bottom: 3px;
		background-color: white;
		transition: 0.3s;
	}

	input:checked + .slider {
		background-color: #4361ee;
	}

	input:focus + .slider {
		box-shadow: 0 0 1px #4361ee;
	}

	input:checked + .slider:before {
		transform: translateX(26px);
	}

	input:disabled + .slider {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.slider.round {
		border-radius: 24px;
	}

	.slider.round:before {
		border-radius: 50%;
	}
</style>
