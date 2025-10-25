<!--
CardHeader.svelte - Shared card header component
Reusable header for all card types with consistent styling
-->
<script lang="ts">
  let { 
    title, 
    headerFontSize = "9px" 
  } = $props<{
    title: string;
    headerFontSize?: string;
  }>();
</script>

<div class="card-header">
  <div class="card-title" style="font-size: {headerFontSize}">
    {title}
  </div>
</div>

<style>
  .card-header {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 0.25rem; /* 4px → rem for accessibility */
    width: 100%;
    flex-shrink: 0;
    justify-content: center;
    padding: clamp(3px, 0.8cqh, 6px) clamp(6px, 1.5cqw, 10px);
  }

  .card-title {
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    text-align: center;
    letter-spacing: 0.2px;
    text-transform: uppercase;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
  }
</style>

