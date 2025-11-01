<script lang="ts">
  /**
   * ProfileManager
   * Domain: User Profile Management
   *
   * Responsibilities:
   * - Manage profile sheet visibility
   * - Listen for profile sheet toggle events
   * - Render ProfileSheet component
   */
  import { onMount } from "svelte";
  import ProfileSheet from "../navigation/components/ProfileSheet.svelte";

  let showProfileSheet = $state(false);

  onMount(() => {
    if (typeof window === "undefined") {
      return;
    }

    // Listen for custom event to toggle profile sheet
    const handleProfileSheetToggle = () => {
      showProfileSheet = !showProfileSheet;
    };
    window.addEventListener("profile-sheet-toggle", handleProfileSheetToggle);

    return () => {
      window.removeEventListener(
        "profile-sheet-toggle",
        handleProfileSheetToggle
      );
    };
  });

  function handleClose() {
    showProfileSheet = false;
  }
</script>

<!-- Profile Sheet - rendered at root level for proper positioning -->
<ProfileSheet
  isOpen={showProfileSheet}
  onClose={handleClose}
/>
