<script lang="ts">
  import { setContext } from "svelte";
  import SequenceActionsSheet from "../../lib/modules/create/workspace-panel/shared/components/SequenceActionsSheet.svelte";

  let show = $state(true);

  // Provide mock CreateModule context
  setContext("createModuleContext", {
    layout: {
      shouldUseSideBySideLayout: false,
      isMobilePortrait: () => false
    }
  });
</script>

<div style="width: 100vw; height: 100vh; background: #0a0e14;">
  <SequenceActionsSheet
    {show}
    hasSequence={true}
    combinedPanelHeight={300}
    onMirror={() => console.log("Mirror clicked")}
    onRotate={() => console.log("Rotate clicked")}
    onColorSwap={() => console.log("Color swap clicked")}
    onReverse={() => console.log("Reverse clicked")}
    onCopyJSON={() => console.log("Copy JSON clicked")}
    onClose={() => { show = false; console.log("Close clicked"); }}
  />
</div>
