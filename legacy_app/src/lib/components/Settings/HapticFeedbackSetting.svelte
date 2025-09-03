<script lang="ts">
	import { settingsStore } from '$lib/state/stores/settings/settings.store';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { browser } from '$app/environment';

	// Get the current haptic feedback setting
	const hapticFeedback = $derived(settingsStore.getSnapshot().hapticFeedback);

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
</script>

<div class="setting-container">
	<div class="setting-info">
		<h3>Haptic Feedback</h3>
		<p>Enable vibration feedback for touch interactions on mobile devices</p>
	</div>
	<div class="setting-control">
		<label class="switch">
			<input
				type="checkbox"
				checked={hapticFeedback}
				onchange={toggleHapticFeedback}
				aria-label="Toggle haptic feedback"
			>
			<span class="slider round"></span>
		</label>
	</div>
</div>

<style>
	.setting-container {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	}

	.setting-info {
		flex: 1;
	}

	h3 {
		margin: 0 0 0.5rem 0;
		font-size: 1rem;
		font-weight: 500;
		color: var(--color-text-primary, white);
	}

	p {
		margin: 0;
		font-size: 0.875rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
	}

	.setting-control {
		margin-left: 1rem;
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

	.slider.round {
		border-radius: 24px;
	}

	.slider.round:before {
		border-radius: 50%;
	}

	/* Responsive adjustments */
	@media (max-width: 480px) {
		.setting-container {
			padding: 0.75rem;
		}

		h3 {
			font-size: 0.9rem;
		}

		p {
			font-size: 0.8rem;
		}
	}
</style>
