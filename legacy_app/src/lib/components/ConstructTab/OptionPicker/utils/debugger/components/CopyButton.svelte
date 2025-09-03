<!-- src/lib/components/OptionPicker/utils/debugger/components/CopyButton.svelte -->
<script lang="ts">
	import { onDestroy } from 'svelte';
	import { writable } from 'svelte/store';

	export let text: string = '';
	export let iconOnly: boolean = false;
	export let className: string = 'copy-button';
	export let smallIcon: boolean = false;
	export let onClick: () => Promise<string>; // Function to get text to copy

	// Button state
	type CopyStatus = 'idle' | 'copying' | 'copied' | 'error';
	let status = writable<CopyStatus>('idle');
	let error = writable<string | null>(null);
	let timeoutId: ReturnType<typeof setTimeout> | null = null;

	async function handleClick() {
		// Clear previous timeout
		if (timeoutId) clearTimeout(timeoutId);

		// Check for Clipboard API availability
		if (!navigator.clipboard) {
			error.set('Clipboard API not available.');
			status.set('error');
			console.error('Clipboard API not available.');
			resetStatusAfterDelay();
			return;
		}

		// Set initial state for copying
		status.set('copying');
		error.set(null);

		try {
			// Get the text to copy by calling the function
			const textToCopy = await onClick();
			await navigator.clipboard.writeText(textToCopy);
			status.set('copied'); // Success
		} catch (err) {
			error.set('Failed to copy.'); // Set specific error
			status.set('error'); // Set error state
			console.error('Failed to copy text: ', err);
		} finally {
			// Always reset the status after a delay
			resetStatusAfterDelay();
		}
	}

	function resetStatusAfterDelay(delay = 2000) {
		// Create the timeout
		timeoutId = setTimeout(() => {
			status.set('idle');
			error.set(null);
			timeoutId = null;
		}, delay);
	}

	// Clean up on component destruction
	onDestroy(() => {
		if (timeoutId) clearTimeout(timeoutId);
	});
</script>

<button
	class="copy-button-base {className}"
	class:copying={$status === 'copying'}
	class:copied={$status === 'copied'}
	class:error={$status === 'error'}
	on:click={handleClick}
	disabled={$status !== 'idle'}
	aria-live="polite"
	title={text || 'Copy to clipboard'}
	aria-label={text || 'Copy to clipboard'}
>
	{#if $status === 'idle'}
		<svg
			xmlns="http://www.w3.org/2000/svg"
			width={smallIcon ? '12' : '14'}
			height={smallIcon ? '12' : '14'}
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			stroke-width="2"
			stroke-linecap="round"
			stroke-linejoin="round"
			><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path
				d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"
			></path></svg
		>
		{#if !iconOnly}
			<span>{text}</span>
		{/if}
	{:else if $status === 'copying'}
		<span class="spinner"></span>
		{#if !iconOnly}
			<span>Copying...</span>
		{/if}
	{:else if $status === 'copied'}
		<svg
			xmlns="http://www.w3.org/2000/svg"
			width={smallIcon ? '12' : '14'}
			height={smallIcon ? '12' : '14'}
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			stroke-width="3"
			stroke-linecap="round"
			stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg
		>
		{#if !iconOnly}
			<span>Copied!</span>
		{/if}
	{:else if $status === 'error'}
		<svg
			xmlns="http://www.w3.org/2000/svg"
			width={smallIcon ? '12' : '14'}
			height={smallIcon ? '12' : '14'}
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			stroke-width="2"
			stroke-linecap="round"
			stroke-linejoin="round"
			><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg
		>
		{#if !iconOnly}
			<span>Error</span>
		{/if}
	{/if}
</button>

{#if $error && $status === 'error'}
	<span class="copy-error-message">{$error}</span>
{/if}

<style>
	/* --- Base Copy Button Styles --- */
	.copy-button-base {
		display: inline-flex;
		align-items: center;
		gap: 5px;
		border: 1px solid #475569;
		padding: 6px 10px;
		border-radius: 4px;
		cursor: pointer;
		font-weight: 500;
		transition: all 0.2s ease-out;
		overflow: hidden;
		position: relative;
		white-space: nowrap;
	}

	.copy-button-base svg {
		flex-shrink: 0;
	}

	.copy-button-base:not(:disabled):hover {
		border-color: #64748b;
		color: #e2e8f0;
		transform: translateY(-1px);
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
	}

	.copy-button-base:disabled {
		cursor: default;
		opacity: 0.7;
	}

	/* --- Copy Button States (shared by base class) --- */
	.copy-button-base.copying {
		background-color: #475569;
	}

	.copy-button-base.copied {
		background-color: #16a34a;
		border-color: #16a34a;
		color: white;
		animation: pulse-success 0.5s ease-out;
	}

	.copy-button-base.error {
		background-color: #dc2626;
		border-color: #dc2626;
		color: white;
		animation: shake-error 0.5s ease-out;
	}

	/* --- Copy Error Message --- */
	.copy-error-message {
		color: #fb7185;
		font-size: 10px;
		flex-grow: 1;
		text-align: right;
		margin-right: 5px;
	}

	/* --- Animations --- */
	@keyframes pulse-success {
		0% {
			transform: scale(1);
		}
		50% {
			transform: scale(1.05);
		}
		100% {
			transform: scale(1);
		}
	}

	@keyframes shake-error {
		0%,
		100% {
			transform: translateX(0);
		}
		25% {
			transform: translateX(-3px);
		}
		50% {
			transform: translateX(3px);
		}
		75% {
			transform: translateX(-3px);
		}
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	.spinner {
		display: inline-block;
		border: 2px solid rgba(255, 255, 255, 0.3);
		border-left-color: currentColor;
		border-radius: 50%;
		width: 12px;
		height: 12px;
		animation: spin 1s linear infinite;
	}
</style>
