<!-- Styled Border Overlay stub -->
<script lang="ts">
  export let isSelected = false;
  export let isHovered = false;
</script>

<div class="border-overlay" class:selected={isSelected} class:hovered={isHovered}></div>

<style>
  .border-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border: 2px solid transparent;
    border-radius: 4px;
    pointer-events: none;
  }

  .selected {
    border-color: gold;
  }

  .hovered {
    border-color: blue;
  }
</style>
