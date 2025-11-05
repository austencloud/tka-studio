<!--
  GallerySection.svelte - Gallery view for saved sequences

  This is a wrapper around the existing SequencesView component
-->
<script lang="ts">
  import SequencesView from "../../library/components/SequencesView.svelte";
</script>

<div class="gallery-section">
  <SequencesView />
</div>

<style>
  .gallery-section {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }
</style>
