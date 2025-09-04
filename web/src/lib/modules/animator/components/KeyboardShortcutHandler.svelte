<!--
KeyboardShortcutHandler.svelte - Keyboard shortcut handling

Single responsibility: Handle keyboard shortcuts for animation controls.
This is a headless component that only handles events - no UI rendering.
-->
<script lang="ts">
  interface Props {
    onPlayToggle: () => void;
    onReset: () => void;
  }

  let { onPlayToggle, onReset }: Props = $props();

  function handleKeyDown(event: KeyboardEvent) {
    // Space bar for play/pause
    if (event.code === "Space" && event.target === event.currentTarget) {
      event.preventDefault();
      onPlayToggle();
    }
    // R key for reset
    if (event.key === "r" || event.key === "R") {
      event.preventDefault();
      onReset();
    }
  }
</script>

<!-- Headless component - no template needed -->

<!-- No styles needed for headless component -->
