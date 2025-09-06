<!-- src/lib/components/GenerateTab/layout/GenerateTabHeader.svelte -->
<script lang="ts">
  import HeaderLabel from './HeaderLabel.svelte';
</script>

<div class="generate-tab-header">
  <HeaderLabel />
</div>

<style>
  .generate-tab-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
    position: relative;
    z-index: 1;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .generate-tab-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
  }
</style>
