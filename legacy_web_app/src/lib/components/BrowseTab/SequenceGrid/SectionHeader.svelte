<!-- src/lib/components/BrowseTab/SequenceGrid/SectionHeader.svelte -->
<script lang="ts">
  export let title: string;
</script>

<div class="section-header">
  <h3>{title}</h3>
  <div class="divider"></div>
</div>

<style>
  .section-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.5rem;
  }

  h3 {
    margin: 0;
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--text-color-emphasis, #ffffff);
    white-space: nowrap;
  }

  .divider {
    flex: 1;
    height: 1px;
    background-color: var(--border-color, #333333);
  }
</style>
