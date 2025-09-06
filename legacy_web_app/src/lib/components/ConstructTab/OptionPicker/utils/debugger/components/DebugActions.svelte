<!-- src/lib/components/OptionPicker/utils/debugger/components/DebugActions.svelte -->
<script lang="ts">
	import { debugActions } from '../stores/debugStore';
	import CopyButton from './CopyButton.svelte';

	// Add the layout context parameter
	export let layoutContext: any;

	// Helper function to make TypeScript happy with the return type
	async function copyAllInfo(): Promise<string> {
		// This function needs to return a string for the CopyButton to copy
		// Let's use the buildDebugInfoText function directly
		const debugInfo = await debugActions.getDebugInfoText(layoutContext);
		return debugInfo;
	}
</script>

<div class="edit-tip">
	Edit in: <code>src/lib/components/OptionPicker/utils/layoutConfig.ts</code>
</div>

<div class="actions-area">
	<CopyButton
		onClick={copyAllInfo}
		text="Copy All Info"
		className="copy-button"
	/>
</div>

<!-- No component-specific styles needed, using shared styles -->
