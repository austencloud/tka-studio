<script lang="ts">
  import MainApplication from "$shared/MainApplication.svelte";
  import { switchTab } from "$shared/state";
  import { onMount } from "svelte";

  onMount(async () => {
    console.log("🚀 +page.svelte onMount started");
    // TEMPORARILY DISABLED - Testing for infinite loop
    // Check for tab parameter in URL (from SEO redirects)
    // const urlParams = new URLSearchParams(window.location.search);
    // const tabParam = urlParams.get("tab");
    // const sectionParam = urlParams.get("section");

    // if (tabParam) {
    //   // Switch to the specified tab - validate it's a valid tab ID
    //   const validTabs = [
    //     "build",
    //     "browse",
    //     "sequence_card",
    //     "write",
    //     "learn",
    //     "about",
    //   ];
    //   if (validTabs.includes(tabParam)) {
    //     switchTab(
    //       tabParam as
    //         | "build"
    //         | "browse"
    //         | "sequence_card"
    //         | "write"
    //         | "learn"
    //         | "about"
    //     );
    //   }

    //   // If there's a section parameter, scroll to it after a delay
    //   if (sectionParam) {
    //     setTimeout(() => {
    //       const element = document.getElementById(sectionParam);
    //       if (element) {
    //         element.scrollIntoView({ behavior: "smooth", block: "start" });
    //       }
    //     }, 500); // Allow time for tab to load
    //   }

    //   // Clean up URL parameters for cleaner UX
    //   window.history.replaceState({}, "", "/");
    // } else {
    //   // Default behavior - go to buildor tab on startup
    //   switchTab("build");
    // }
    console.log("✅ +page.svelte onMount completed (disabled)");
  });
</script>

<svelte:head>
  <title>TKA - The Kinetic Constructor</title>
</svelte:head>

<MainApplication />
