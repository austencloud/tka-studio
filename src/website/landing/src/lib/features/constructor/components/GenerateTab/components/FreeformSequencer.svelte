<!-- Freeform Sequencer stub -->
<script lang="ts">
  export let onGenerate = () => {};
  export let settings = {};
</script>

<div class="freeform-sequencer-placeholder">
  <h3>Freeform Sequencer</h3>
  <p>Custom sequence generation (Coming Soon)</p>
  <button class="generate-btn" on:click={onGenerate}>
    Generate Freeform Sequence
  </button>
</div>

<style>
  .freeform-sequencer-placeholder {
    padding: 20px;
    text-align: center;
    border: 2px dashed #ccc;
    border-radius: 8px;
    background: #f9f9f9;
  }

  .generate-btn {
    padding: 10px 20px;
    background: #17a2b8;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 10px;
  }

  .generate-btn:hover {
    background: #138496;
  }
</style>
