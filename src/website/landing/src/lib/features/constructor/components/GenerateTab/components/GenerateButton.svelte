<!-- Generate Button stub -->
<script lang="ts">
  export let onClick = () => {};
</script>

<button class="generate-button" on:click={onClick}>
  Generate
</button>

<style>
  .generate-button {
    padding: 10px 20px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
</style>