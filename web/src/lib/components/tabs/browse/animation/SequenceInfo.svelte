<!--
Sequence Info Component

Displays sequence name and author information.
-->
<script lang="ts">
  // Props
  const { sequenceData = null } = $props<{
    sequenceData?: any;
  }>();
</script>

{#if sequenceData}
  <div class="sequence-info">
    <h4>{sequenceData.name || sequenceData.word}</h4>
    <p class="author">{sequenceData.metadata?.author || "Unknown Author"}</p>
  </div>
{/if}

<style>
  .sequence-info h4 {
    margin: 0 0 0.5rem 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .sequence-info .author {
    margin: 0;
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.6);
  }
</style>
