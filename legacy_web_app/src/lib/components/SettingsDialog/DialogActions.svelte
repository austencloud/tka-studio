<script lang="ts">
	export let onClose: () => void;
</script>

<div class="dialog-actions" role="group" aria-label="Dialog actions">
	<button class="btn close-btn" on:click={onClose}>Close</button>
</div>

<style>
	.dialog-actions {
		display: flex;
		justify-content: flex-end;
		gap: 10px;
	}

	.close-btn {
		padding: 10px 20px;
		background: #ccc;
		border: none;
		cursor: pointer;
		border-radius: 4px;
	}
</style>
