<!--
  DependencyWarning.svelte - Motion Dependency Warning

  Displays a warning when both motions are not visible,
  indicating that dependent glyphs cannot be shown.
-->
<script lang="ts">
  interface Props {
    show: boolean;
  }

  let { show }: Props = $props();
</script>

{#if show}
  <div class="dependency-warning">
    ⚠️ Dependent glyphs require both motions to be visible
  </div>
{/if}

<style>
  .dependency-warning {
    background: rgba(255, 193, 7, 0.1);
    border: 2px solid rgba(255, 193, 7, 0.3);
    border-radius: 8px;
    padding: 12px;
    color: rgba(255, 193, 7, 1);
    font-size: 13px;
    font-weight: 600;
    text-align: center;
  }

  /* Accessibility */
  @media (prefers-contrast: high) {
    .dependency-warning {
      border-width: 3px;
    }
  }
</style>
