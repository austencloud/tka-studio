<script lang="ts">
	import { browser } from '$app/environment';
	import { fade, scale } from 'svelte/transition';
	import { userContainer } from '$lib/state/stores/user/UserContainer';
	import { useContainer } from '$lib/state/core/svelte5-integration.svelte';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';

	// Use the user container with Svelte 5 runes
	const user = useContainer(userContainer);

	// Local state
	let username = $state(user.currentUser || '');
	let isVisible = $state(userContainer.isFirstVisit());

	// Function to show the dialog
	export function showDialog() {
		isVisible = true;
	}

	// Handle close button click
	function handleClose() {
		// Provide haptic feedback
		if (browser && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('success');
		}

		// Save the entered username (even if empty)
		userContainer.setUsername(username);
		userContainer.completeSetup();

		// Hide the dialog
		isVisible = false;
	}

	// Handle input change
	function handleInputChange(event: Event) {
		const input = event.target as HTMLInputElement;
		username = input.value;
	}

	// Handle keydown event for Enter key
	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			handleClose();
		} else if (event.key === 'Escape') {
			handleClose();
		}
	}
</script>

{#if isVisible}
	<div class="overlay" transition:fade={{ duration: 200 }}>
		<div class="dialog" transition:scale={{ duration: 200, start: 0.95 }}>
			<div class="dialog-header">
				<h2>The Kinetic Constructor</h2>
				<button class="close-button" onclick={handleClose} aria-label="Close dialog"> × </button>
			</div>

			<div class="dialog-content">
				<p class="welcome">Kinetic Fire 2025 software pre-release!</p>

				<div class="compact-info">
					<p>

            <strong><br/>Note:</strong> This is an alpha version.<br />
            For bugs or feature requests, email<br />
            <a href="mailto:austencloud@gmail.com" class="email-link">austencloud@gmail.com</a>
					</p>

					<div class="donation-section">
						<p><strong>Support:</strong> If you find this tool useful, consider a donation:</p>
						<div class="donation-links">
							<a
								href="https://paypal.me/austencloud"
								target="_blank"
								rel="noopener noreferrer"
								class="donation-link paypal"
							>
								PayPal
							</a>
							<a
								href="https://venmo.com/austencloud"
								target="_blank"
								rel="noopener noreferrer"
								class="donation-link venmo"
							>
								Venmo
							</a>
						</div>
					</div>
				</div>

				<div class="input-group">
					<label for="username-input">Your Name (Optional)</label>
					<input
						type="text"
						id="username-input"
						value={username}
						oninput={handleInputChange}
						onkeydown={handleKeydown}
						placeholder="Enter your name (or leave blank)"
						maxlength="50"
						autocomplete="name"
					/>
					<p class="input-help">Used only when exporting sequences.</p>
				</div>
			</div>

			<div class="dialog-footer">
				<button class="close-button-large" onclick={handleClose}>Close</button>
			</div>
		</div>
	</div>
{/if}

<style>
	.overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.7);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
		backdrop-filter: blur(4px);
	}

	.dialog {
		background: linear-gradient(to bottom, #2a2a35, #1f1f25);
		border-radius: 12px;
		box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
		width: 90%;
		max-width: 500px;
		max-height: 90vh; /* Limit height to prevent overflow */
		overflow-y: auto; /* Add vertical scrolling if needed */
		overflow-x: hidden; /* Prevent horizontal scrolling */
		display: flex;
		flex-direction: column;
		border: 1px solid rgba(108, 156, 233, 0.3);
	}

	.dialog-header {
		padding: 1rem;
		background: linear-gradient(to right, #167bf4, #329bff);
		color: white;
		position: relative;
		flex-shrink: 0;
	}

	.dialog-header h2 {
		margin: 0;
		font-size: 1.3rem;
		font-weight: 600;
	}

	.close-button {
		position: absolute;
		top: 0.75rem;
		right: 0.75rem;
		width: 28px;
		height: 28px;
		border-radius: 50%;
		background: rgba(255, 255, 255, 0.2);
		border: none;
		color: white;
		font-size: 1.25rem;
		line-height: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.close-button:hover {
		background: rgba(255, 255, 255, 0.3);
		transform: scale(1.05);
	}

	.close-button:active {
		background: rgba(255, 255, 255, 0.1);
		transform: scale(0.95);
	}

	.dialog-content {
		padding: 1rem;
		color: var(--color-text-primary, white);
		flex: 1;
		overflow-y: auto;
		overflow-x: hidden;
		word-wrap: break-word;
		word-break: break-word;
	}

	.dialog-content p {
		margin: 0 0 0.75rem 0;
		line-height: 1.4;
		font-size: 0.95rem;
	}

	.welcome {
		font-size: 1.1rem;
		font-weight: 500;
		margin-bottom: 1rem !important;
	}

	.compact-info {
		margin-bottom: 1rem;
	}

	.input-group {
		margin-bottom: 0.75rem;
	}

	.input-group label {
		display: block;
		margin-bottom: 0.3rem;
		font-weight: 500;
		color: var(--color-text-primary, white);
		font-size: 0.95rem;
	}

	.input-group input {
		width: 100%;
		padding: 0.6rem;
		border-radius: 6px;
		background: linear-gradient(to bottom, #1f1f24, #2a2a30);
		border: 1px solid rgba(108, 156, 233, 0.3);
		color: var(--color-text-primary, white);
		font-size: 0.95rem;
		transition: all 0.2s ease;
		box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
	}

	.input-group input:focus {
		border-color: #167bf4;
		box-shadow: 0 0 0 2px rgba(22, 123, 244, 0.3);
		outline: none;
	}

	.input-help {
		margin-top: 0.3rem;
		font-size: 0.8rem;
		color: rgba(255, 255, 255, 0.7);
		line-height: 1.3;
	}

	.dialog-footer {
		padding: 0.75rem;
		display: flex;
		justify-content: center;
		gap: 1rem;
		border-top: 1px solid rgba(255, 255, 255, 0.1);
		flex-shrink: 0;
	}

	.close-button-large {
		padding: 0.6rem 1.5rem;
		border-radius: 6px;
		background: linear-gradient(to bottom, #167bf4, #1068d9);
		color: white;
		border: none;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
		min-width: 100px;
		font-size: 0.95rem;
	}

	.close-button-large:hover {
		background: linear-gradient(to bottom, #1d86ff, #1271ea);
		transform: translateY(-2px);
		box-shadow: 0 4px 10px rgba(22, 123, 244, 0.3);
	}

	.close-button-large:active {
		transform: translateY(0);
		background: linear-gradient(to bottom, #0f65d1, #0a54b3);
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
	}

	.donation-section {
		margin-bottom: 1rem;
		padding: 0.75rem;
		background: rgba(22, 123, 244, 0.1);
		border-radius: 8px;
		border: 1px solid rgba(22, 123, 244, 0.2);
	}

	.donation-section p {
		margin-bottom: 0.5rem !important;
	}

	.donation-links {
		display: flex;
		gap: 0.75rem;
		flex-wrap: wrap;
		width: 100%;
		max-width: 100%;
	}

	.donation-link {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0.5rem 0.75rem;
		border-radius: 6px;
		text-decoration: none;
		font-weight: 600;
		transition: all 0.2s ease;
		color: white;
		flex: 1 1 0;
		min-width: 100px;
		text-align: center;
		letter-spacing: 0.5px;
		font-size: 0.9rem;
	}

	.email-link {
		color: #7dd3fc; /* Light blue color */
		text-decoration: underline;
		transition: color 0.2s ease;
		word-wrap: break-word;
		word-break: break-all;
	}

	.email-link:hover {
		color: #38bdf8; /* Slightly darker blue on hover */
		text-decoration: underline;
	}

	.donation-link.paypal {
		background: linear-gradient(to bottom, #0079c1, #00457c);
	}

	.donation-link.venmo {
		background: linear-gradient(to bottom, #3d95ce, #0074de);
	}

	.donation-link:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
	}

	.donation-link:active {
		transform: translateY(0);
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
	}

	/* Mobile optimizations */
	@media (max-width: 480px) {
		.dialog {
			max-height: 85vh;
			width: 95%;
			min-width: 280px; /* Ensure minimum width for very small screens */
		}

		.dialog-header {
			padding: 0.75rem;
		}

		.dialog-header h2 {
			font-size: 1.1rem;
		}

		.dialog-content {
			padding: 0.75rem;
		}

		.welcome {
			font-size: 1rem;
		}

		.dialog-content p {
			font-size: 0.9rem;
			margin-bottom: 0.5rem;
		}

		.donation-section {
			padding: 0.5rem;
		}

		.donation-links {
			gap: 0.5rem;
		}

		.donation-link {
			padding: 0.4rem 0.5rem;
			font-size: 0.85rem;
			min-width: 70px;
		}

		.input-group input {
			padding: 0.5rem;
		}
	}
</style>
