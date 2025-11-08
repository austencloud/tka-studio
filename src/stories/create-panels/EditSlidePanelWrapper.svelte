<script lang="ts">
  import { setContext } from "svelte";
  import EditSlidePanel from "../../lib/modules/create/edit/components/EditSlidePanel.svelte";

  // Mock beat data
  let mockBeatData = {
    red_arrow: { angle: 45, length: 100 },
    blue_arrow: { angle: 135, length: 100 },
    red_prop: { rotation_angle: 0, orientation: "in" },
    blue_prop: { rotation_angle: 0, orientation: "out" },
    isBlank: false
  };

  let isOpen = $state(true);
  let selectedBeatNumber = $state(1);

  // Provide mock CreateModule context
  setContext("createModuleContext", {
    layout: {
      shouldUseSideBySideLayout: false,
      isMobilePortrait: () => false
    }
  });
</script>

<div style="width: 100vw; height: 100vh; background: #0a0e14;">
  <EditSlidePanel
    {isOpen}
    {selectedBeatNumber}
    selectedBeatData={mockBeatData}
    selectedBeatsData={null}
    combinedPanelHeight={300}
    isSideBySideLayout={false}
    onClose={() => { isOpen = false; console.log("Close clicked"); }}
    onOrientationChanged={(color, orientation) => console.log("Orientation changed:", color, orientation)}
    onTurnAmountChanged={(color, turnAmount) => console.log("Turn changed:", color, turnAmount)}
    onRemoveBeat={(beatNumber) => console.log("Remove beat:", beatNumber)}
  />
</div>
