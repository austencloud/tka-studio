<script lang="ts">
  /**
   * CAP Coordinator Component
   *
   * Manages CAP selection modal state at BuildTab level.
   * Extracts CAP modal logic from CAPCard for proper stacking context.
   *
   * Domain: Build Module - CAP Panel Coordination
   */

  import { resolve, TYPES } from "$shared";
  import type { ICAPTypeService } from "$shared";
  import CAPSelectionModal from "../../../generate/components/modals/CAPSelectionModal.svelte";
  import type { PanelCoordinationState } from "../../state/panel-coordination-state.svelte";

  // Props
  let {
    panelState,
  }: {
    panelState: PanelCoordinationState;
  } = $props();

  let capTypeService: ICAPTypeService = resolve<ICAPTypeService>(TYPES.ICAPTypeService);

  // Local pending state - tracks changes before applying
  let pendingComponents = $state<Set<any> | null>(null);

  // Use pending components if available, otherwise use the original
  const displayComponents = $derived(
    pendingComponents || panelState.capSelectedComponents || new Set()
  );

  // Event handlers
  function handleConfirm() {
    // Apply pending changes if any
    if (pendingComponents && panelState.capOnChange) {
      // Check if the combination is implemented
      const isImplemented = capTypeService.isImplemented(pendingComponents);

      if (!isImplemented) {
        // Show "Coming Soon" message
        const componentNames = Array.from(pendingComponents)
          .map(c => c.charAt(0) + c.slice(1).toLowerCase())
          .join(' + ');

        alert(`${componentNames} combination is coming soon! This combination hasn't been implemented yet, but we're working on it.`);
        return; // Don't close the panel, let user select a different combination
      }

      const finalCAPType = capTypeService.generateCAPType(pendingComponents);
      panelState.capOnChange(finalCAPType);
    }

    // Reset state and close
    pendingComponents = null;
    panelState.closeCAPPanel();
  }

  function handleClose() {
    // Discard pending changes without applying them
    pendingComponents = null;
    panelState.closeCAPPanel();
  }

  function handleToggleComponent(component: any) {
    // Initialize pending if not set
    if (!pendingComponents) {
      pendingComponents = new Set(panelState.capSelectedComponents || new Set());
    }

    // Toggle the component
    if (pendingComponents.has(component)) {
      pendingComponents.delete(component);
    } else {
      pendingComponents.add(component);
    }

    // Trigger reactivity
    pendingComponents = new Set(pendingComponents);
  }

  // Reset pending state when panel closes
  $effect(() => {
    if (!panelState.isCAPPanelOpen) {
      pendingComponents = null;
    }
  });
</script>

<CAPSelectionModal
  isOpen={panelState.isCAPPanelOpen}
  selectedComponents={displayComponents}
  onToggleComponent={handleToggleComponent}
  onConfirm={handleConfirm}
  onClose={handleClose}
/>
