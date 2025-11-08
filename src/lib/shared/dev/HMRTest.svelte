<script lang="ts">
  // HMR Test Component
  // This component is used to verify HMR is working correctly

  let count = $state(0);
  let testMessage = $state("HMR Test v2.0 - Text Changed!");

  function increment() {
    count += 5; // Changed from ++ to test HMR
  }
</script>

<div class="hmr-test">
  <h2>{testMessage}</h2>
  <p>Count: {count}</p>
  <button onclick={increment}>Increment</button>
  <p class="test-indicator">Background: Blue</p>
</div>

<style>
  .hmr-test {
    position: fixed;
    top: 10px;
    right: 10px;
    z-index: 9999;
    background: blue;
    color: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  }

  button {
    background: white;
    color: red;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
  }

  button:hover {
    opacity: 0.8;
  }

  .test-indicator {
    font-size: 0.8rem;
    margin-top: 0.5rem;
    opacity: 0.8;
  }
</style>
