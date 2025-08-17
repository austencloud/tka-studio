<!-- Motion Tester Route - MISSING FILE FIX -->
<script lang="ts">
  import { onMount } from "svelte";
  import { switchTab } from "$lib/state/app-state.svelte";
  import MainApplication from "$components/MainApplication.svelte";

  onMount(async () => {
    // Navigate to motion-tester tab
    switchTab("motion-tester");
  });
</script>

<svelte:head>
  <title
    >Motion Tester - TKA Development Tool | Flow Arts Animation Testing</title
  >
  <meta
    name="description"
    content="Development tool for testing motion parameters and animation sequences in TKA. Debug flow arts movements and kinetic patterns."
  />
  <meta property="og:title" content="Motion Tester - TKA Development Tool" />
  <meta
    property="og:description"
    content="Test and debug motion parameters for flow arts animations with TKA's motion testing interface."
  />
  <meta property="og:type" content="website" />
  <link rel="canonical" href="https://thekineticalphabet.com/motion-tester" />
</svelte:head>

<MainApplication />
