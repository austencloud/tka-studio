<!--
GeneratePanel.svelte - Backward compatibility wrapper

This file has been refactored for better maintainability. The original functionality
has been split into simple, focused components:

- generateConfigState.svelte.ts: Simple configuration state management
- generateActionsState.svelte.ts: Simple generation actions
- generateDeviceState.svelte.ts: Simple device detection state
- GeneratePanelContainer.svelte: Clean UI component with all functionality

This wrapper maintains backward compatibility while providing the new architecture.
-->
<script lang="ts">
	import GeneratePanelContainer from './generate/GeneratePanelContainer.svelte';
	// No props needed - the container handles everything
</script>

<!--
   Delegate to the new GeneratePanelContainer.
   This maintains exact backward compatibility while using the new architecture.
-->
<GeneratePanelContainer />
