<script lang="ts">
  import MainApplication from "$components/MainApplication.svelte";
  import { switchTab } from "$lib/state/app-state.svelte";
  import { onMount } from "svelte";

  onMount(async () => {
    // Check for tab parameter in URL (from SEO redirects)
    const urlParams = new URLSearchParams(window.location.search);
    const tabParam = urlParams.get("tab");
    const sectionParam = urlParams.get("section");

    if (tabParam) {
      // Switch to the specified tab - validate it's a valid tab ID
      const validTabs = [
        "construct",
        "browse",
        "sequence_card",
        "write",
        "learn",
        "about",
      ];
      if (validTabs.includes(tabParam)) {
        switchTab(
          tabParam as
            | "construct"
            | "browse"
            | "sequence_card"
            | "write"
            | "learn"
            | "about"
        );
      }

      // If there's a section parameter, scroll to it after a delay
      if (sectionParam) {
        setTimeout(() => {
          const element = document.getElementById(sectionParam);
          if (element) {
            element.scrollIntoView({ behavior: "smooth", block: "start" });
          }
        }, 500); // Allow time for tab to load
      }

      // Clean up URL parameters for cleaner UX
      window.history.replaceState({}, "", "/");
    } else {
      // Default behavior - go to constructor tab on startup
      switchTab("construct");
    }
  });
</script>

<svelte:head>
  <title>TKA - The Kinetic Constructor</title>
</svelte:head>

<MainApplication />
