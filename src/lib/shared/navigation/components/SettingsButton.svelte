<!--
  Settings Button Component

  Simple settings button with icon that triggers the settings dialog.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { showSettingsDialog } from "../../application/state/app-state.svelte";

  let { navigationLayout = "top" } = $props<{
    navigationLayout?: "top" | "left";
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Handle settings button click
  function handleSettingsClick() {
    hapticService?.trigger("selection");
    showSettingsDialog();
  }
</script>

<button
  class="nav-action"
  class:layout-left={navigationLayout === "left"}
  onclick={handleSettingsClick}
  title="Settings (Ctrl+,)"
  aria-label="Open Settings"
>
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
    <path
      d="M12 15a3 3 0 100-6 3 3 0 000 6z"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
    <path
      d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
  </svg>
</button>

<style>
  .nav-action {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 48px; /* Minimum touch target width */
    height: 100%; /* Fill full navigation bar height */
    padding: 0 var(--spacing-sm); /* Add horizontal padding for larger touch target */
    background: rgba(100, 116, 139, 0.8);
    border: 1px solid rgba(148, 163, 184, 0.3);
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    color: #ffffff;
    cursor: pointer;
    transition: all var(--transition-normal, 0.3s cubic-bezier(0.4, 0, 0.2, 1));
  }

  .nav-action.layout-left {
    width: 48px;
    height: 48px;
    flex-shrink: 0;
    padding: 0; /* Reset padding for left layout */
  }

  .nav-action:hover {
    transform: scale(1.05);
    background: rgba(100, 116, 139, 0.9);
    border-color: rgba(148, 163, 184, 0.4);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    color: #ffffff;
  }

  .nav-action:focus-visible {
    outline: 2px solid var(--primary-light, #818cf8);
    outline-offset: 2px;
  }

  /* ACCESSIBILITY & MOTION */
  @media (prefers-reduced-motion: reduce) {
    .nav-action {
      transition: none;
    }
  }
</style>
