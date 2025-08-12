<script lang="ts">
	interface Props {
		continuousLoop: boolean;
		onLoopChange: (loop: boolean) => void;
	}

	let { continuousLoop, onLoopChange }: Props = $props();

	function handleLoopChange(event: Event) {
		const checked = (event.target as HTMLInputElement).checked;
		onLoopChange(checked);
	}
</script>

<div class="control-group">
	<label for="loopCheckbox" class="checkbox-label">
		<input 
			type="checkbox" 
			id="loopCheckbox" 
			checked={continuousLoop}
			onchange={handleLoopChange}
		/>
		Loop
	</label>
</div>

<style>
	.control-group {
		display: flex;
		gap: 0.75rem;
		align-items: center;
	}

	.checkbox-label {
		cursor: pointer;
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 0.875rem;
		font-weight: 500;
		color: rgba(255, 255, 255, 0.9);
		white-space: nowrap;
	}

	input[type='checkbox'] {
		width: 18px;
		height: 18px;
		cursor: pointer;
		accent-color: rgba(59, 130, 246, 0.8);
	}
</style>
