<script lang="ts">
	import { onMount } from 'svelte';
	import { fade, fly } from 'svelte/transition';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { browser } from '$app/environment';

	export let message: string;
	export let type: 'success' | 'error' | 'info' | 'warning' = 'info';
	export let duration: number = 5000; // Duration in milliseconds
	export let showCloseButton: boolean = true;
	export let action: { label: string; onClick: () => void } | null = null;

	let visible = true;
	let timeoutId: ReturnType<typeof setTimeout>;

	onMount(() => {
		if (duration > 0) {
			timeoutId = setTimeout(() => {
				visible = false;
			}, duration);
		}

		return () => {
			if (timeoutId) clearTimeout(timeoutId);
		};
	});

	function close() {
		// Provide haptic feedback when closing the toast
		if (browser && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('selection');
		}

		visible = false;
		if (timeoutId) clearTimeout(timeoutId);
	}

	function handleAction() {
		if (action && action.onClick) {
			action.onClick();
		}
	}

	// Get icon based on type
	$: icon = {
		success:
			'<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>',
		error:
			'<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>',
		warning:
			'<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
		info: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'
	}[type];
</script>

{#if visible}
	<div
		class="toast-container {type}"
		in:fly={{ y: 20, duration: 300 }}
		out:fade={{ duration: 200 }}
	>
		<div class="toast-icon" aria-hidden="true">
			{@html icon}
		</div>

		<div class="toast-content">
			<div class="toast-message">{message}</div>

			{#if action}
				<button class="toast-action" on:click={handleAction}>
					{action.label}
				</button>
			{/if}
		</div>

		{#if showCloseButton}
			<button class="toast-close" on:click={close} aria-label="Close notification">
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
					<line x1="18" y1="6" x2="6" y2="18"></line>
					<line x1="6" y1="6" x2="18" y2="18"></line>
				</svg>
			</button>
		{/if}
	</div>
{/if}

<style>
	.toast-container {
		display: flex;
		align-items: flex-start;
		gap: 0.75rem;
		padding: 1rem;
		border-radius: 6px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		max-width: 400px;
		width: 100%;
		box-sizing: border-box;
		background-color: #2a2a2a;
		color: #e0e0e0;
		border-left: 4px solid;
	}

	.toast-container.success {
		border-left-color: #2ecc71;
	}

	.toast-container.error {
		border-left-color: #e74c3c;
	}

	.toast-container.warning {
		border-left-color: #f39c12;
	}

	.toast-container.info {
		border-left-color: #3498db;
	}

	.toast-icon {
		flex-shrink: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #e0e0e0;
	}

	.toast-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.toast-message {
		font-size: 0.875rem;
		line-height: 1.4;
	}

	.toast-action {
		align-self: flex-start;
		background: none;
		border: none;
		color: #3498db;
		font-size: 0.875rem;
		font-weight: 500;
		padding: 0.25rem 0;
		cursor: pointer;
		text-decoration: underline;
	}

	.toast-action:hover {
		color: #2980b9;
	}

	.toast-close {
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

	.toast-close:hover {
		color: #fff;
		background-color: rgba(255, 255, 255, 0.1);
	}
</style>
