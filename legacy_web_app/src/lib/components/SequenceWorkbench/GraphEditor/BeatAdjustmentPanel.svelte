<script lang="ts">
  export let onAdjustBeat: (adjustment: number) => void;

  const handleDecrement = () => {
    onAdjustBeat(-1);
  };

  const handleIncrement = () => {
    onAdjustBeat(1);
  };
</script>

<style>
  .beat-adjustment-panel {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
  }

  .button {
    padding: 10px 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: white;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .button:hover {
    background-color: #f0f0f0;
  }
</style>

<div class="beat-adjustment-panel">
  <button class="button" on:click={handleDecrement}>-</button>
  <button class="button" on:click={handleIncrement}>+</button>
</div>
