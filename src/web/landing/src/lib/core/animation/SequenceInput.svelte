<script lang="ts">
	import type { MessageType } from './types.js';

	interface Props {
		onSequenceLoad: (sequenceData: string) => void;
	}

	let { onSequenceLoad }: Props = $props();
	
	let sequenceInput = $state('');
	let message = $state('');
	let messageType: MessageType = $state('success');
	let showMessage = $state(false);

	function handleLoadSequence() {
		if (!sequenceInput.trim()) {
			displayMessage('error', 'Textarea is empty.');
			return;
		}
		
		// Clear previous messages and call parent handler
		showMessage = false;
		onSequenceLoad(sequenceInput.trim());
	}

	function displayMessage(type: MessageType, text: string) {
		messageType = type;
		message = text;
		showMessage = true;
	}

	// Expose the displayMessage function to parent
	export function showLoadMessage(type: MessageType, text: string) {
		displayMessage(type, text);
		if (type === 'success') {
			sequenceInput = '';
		}
	}
</script>

<div class="input-section">
	<label for="sequenceInput" class="input-label">Paste Sequence JSON:</label>
	<textarea 
		bind:value={sequenceInput}
		id="sequenceInput" 
		placeholder="Paste your sequence JSON array here..."
		class="sequence-textarea"
	></textarea>
	<button onclick={handleLoadSequence} class="load-button">
		Load Sequence
	</button>
</div>

{#if showMessage}
	<div class="message {messageType}">
		{message}
	</div>
{/if}

<style>
	.input-section {
		background: rgba(255, 255, 255, 0.1);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 1rem;
		padding: 1.5rem;
		width: 100%;
		max-width: 600px;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.input-label {
		font-size: 0.875rem;
		font-weight: 500;
		color: rgba(255, 255, 255, 0.9);
		margin-bottom: 0.5rem;
	}

	.sequence-textarea {
		width: 100%;
		min-height: 120px;
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 0.5rem;
		padding: 0.75rem;
		font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
		font-size: 0.8rem;
		background: rgba(0, 0, 0, 0.2);
		color: white;
		resize: vertical;
	}

	.sequence-textarea::placeholder {
		color: rgba(255, 255, 255, 0.5);
	}

	.load-button {
		align-self: flex-end;
		padding: 0.75rem 1.5rem;
		background: rgba(59, 130, 246, 0.8);
		color: white;
		border: 1px solid rgba(59, 130, 246, 0.6);
		border-radius: 0.5rem;
		cursor: pointer;
		font-weight: 600;
		transition: all 0.2s ease-in-out;
	}

	.load-button:hover {
		background: rgba(37, 99, 235, 0.9);
		transform: translateY(-1px);
	}

	.message {
		width: 100%;
		max-width: 600px;
		padding: 1rem;
		border-radius: 0.5rem;
		font-size: 0.875rem;
		text-align: center;
		font-weight: 500;
	}

	.message.error {
		color: #fca5a5;
		background: rgba(220, 38, 38, 0.2);
		border: 1px solid rgba(220, 38, 38, 0.4);
	}

	.message.success {
		color: #86efac;
		background: rgba(34, 197, 94, 0.2);
		border: 1px solid rgba(34, 197, 94, 0.4);
	}
</style>
