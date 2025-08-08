<!-- Circular Sequencer stub -->
<script lang="ts">
  export let onGenerate = () => {};
  export let settings = {};
</script>

<div class="circular-sequencer-placeholder">
  <h3>Circular Sequencer</h3>
  <p>Advanced sequence generation (Coming Soon)</p>
  <button class="generate-btn" on:click={onGenerate}>
    Generate Circular Sequence
  </button>
</div>

<style>
  .circular-sequencer-placeholder {
    padding: 20px;
    text-align: center;
    border: 2px dashed #ccc;
    border-radius: 8px;
    background: #f9f9f9;
  }

  .generate-btn {
    padding: 10px 20px;
    background: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 10px;
  }

  .generate-btn:hover {
    background: #218838;
  }
</style>
