<!--
GridConceptExperience - Simple 3-page grid learning flow
Page 1: Side-by-side Box and Diamond grids
Page 2: Grids overlay to show 8-point
Page 3: Location labels (N/E/S/W for Diamond, NE/SE/SW/NW for Box)
-->
<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";

  let { onComplete } = $props<{
    onComplete?: () => void;
  }>();

  const hapticService = resolve<IHapticFeedbackService>(
    TYPES.IHapticFeedbackService
  );

  let currentPage = $state(1);

  function handleNext() {
    hapticService?.trigger("selection");
    if (currentPage < 3) {
      currentPage++;
    } else {
      onComplete?.();
    }
  }

  // Simple grid point data
  const diamondPoints = [
    { x: 50, y: 15 }, // N
    { x: 85, y: 50 }, // E
    { x: 50, y: 85 }, // S
    { x: 15, y: 50 }, // W
    { x: 50, y: 50 }, // Center
  ];

  const boxPoints = [
    { x: 25, y: 25 }, // NW
    { x: 75, y: 25 }, // NE
    { x: 75, y: 75 }, // SE
    { x: 25, y: 75 }, // SW
    { x: 50, y: 50 }, // Center
  ];
</script>

<div class="grid-experience">
  {#if currentPage === 1}
    <!-- Page 1: Side-by-side grids -->
    <div class="page">
      <h2>The Grid</h2>

      <p>The Kinetic Alphabet is based on a 4-point grid.</p>
      <p>
        There are two 4-point grids: <strong>box mode</strong> and
        <strong>diamond mode</strong>.
      </p>
      <p>This guide is written in diamond, but everything translates to box.</p>

      <div class="grids-container">
        <!-- Diamond Grid -->
        <div class="grid-item">
          <h3>Diamond</h3>
          <svg viewBox="0 0 100 100" class="grid-svg">
            <line
              x1="50"
              y1="15"
              x2="50"
              y2="85"
              stroke="white"
              stroke-width="0.5"
              opacity="0.3"
            />
            <line
              x1="15"
              y1="50"
              x2="85"
              y2="50"
              stroke="white"
              stroke-width="0.5"
              opacity="0.3"
            />
            {#each diamondPoints as point}
              <circle cx={point.x} cy={point.y} r="2.5" fill="white" />
            {/each}
          </svg>
        </div>

        <!-- Box Grid -->
        <div class="grid-item">
          <h3>Box</h3>
          <svg viewBox="0 0 100 100" class="grid-svg">
            <line
              x1="25"
              y1="25"
              x2="75"
              y2="75"
              stroke="white"
              stroke-width="0.5"
              opacity="0.3"
            />
            <line
              x1="75"
              y1="25"
              x2="25"
              y2="75"
              stroke="white"
              stroke-width="0.5"
              opacity="0.3"
            />
            {#each boxPoints as point}
              <circle cx={point.x} cy={point.y} r="2.5" fill="white" />
            {/each}
          </svg>
        </div>
      </div>

      <button class="next-button" onclick={handleNext}>Next</button>
    </div>
  {:else if currentPage === 2}
    <!-- Page 2: Overlay animation -->
    <div class="page">
      <h2>The 8-Point Grid</h2>

      <p>Together, diamond and box form an <strong>8-point grid</strong>:</p>

      <div class="merged-grid-container">
        <svg viewBox="0 0 100 100" class="grid-svg merged">
          <!-- Diamond lines -->
          <line
            x1="50"
            y1="15"
            x2="50"
            y2="85"
            stroke="white"
            stroke-width="0.5"
            opacity="0.3"
          />
          <line
            x1="15"
            y1="50"
            x2="85"
            y2="50"
            stroke="white"
            stroke-width="0.5"
            opacity="0.3"
          />
          <!-- Box lines -->
          <line
            x1="25"
            y1="25"
            x2="75"
            y2="75"
            stroke="white"
            stroke-width="0.5"
            opacity="0.3"
          />
          <line
            x1="75"
            y1="25"
            x2="25"
            y2="75"
            stroke="white"
            stroke-width="0.5"
            opacity="0.3"
          />
          <!-- All points -->
          <circle cx="50" cy="15" r="2.5" fill="white" />
          <circle cx="75" cy="25" r="2.5" fill="white" />
          <circle cx="85" cy="50" r="2.5" fill="white" />
          <circle cx="75" cy="75" r="2.5" fill="white" />
          <circle cx="50" cy="85" r="2.5" fill="white" />
          <circle cx="25" cy="75" r="2.5" fill="white" />
          <circle cx="15" cy="50" r="2.5" fill="white" />
          <circle cx="25" cy="25" r="2.5" fill="white" />
          <circle cx="50" cy="50" r="2.5" fill="#FFD700" />
        </svg>
      </div>

      <p>We'll use <strong>diamond mode</strong> to learn each concept.</p>

      <button class="next-button" onclick={handleNext}>Next</button>
    </div>
  {:else if currentPage === 3}
    <!-- Page 3: Location labels -->
    <div class="page">
      <h2>Grid Locations</h2>

      <div class="grids-container">
        <!-- Diamond with N/E/S/W -->
        <div class="grid-item">
          <h3>Diamond</h3>
          <svg viewBox="0 0 100 100" class="grid-svg">
            <line
              x1="50"
              y1="15"
              x2="50"
              y2="85"
              stroke="white"
              stroke-width="0.5"
              opacity="0.3"
            />
            <line
              x1="15"
              y1="50"
              x2="85"
              y2="50"
              stroke="white"
              stroke-width="0.5"
              opacity="0.3"
            />
            {#each diamondPoints as point}
              <circle cx={point.x} cy={point.y} r="2.5" fill="white" />
            {/each}
            <!-- Labels -->
            <text
              x="50"
              y="10"
              text-anchor="middle"
              fill="white"
              font-size="8"
              class="label">N</text
            >
            <text
              x="90"
              y="52"
              text-anchor="start"
              fill="white"
              font-size="8"
              class="label">E</text
            >
            <text
              x="50"
              y="95"
              text-anchor="middle"
              fill="white"
              font-size="8"
              class="label">S</text
            >
            <text
              x="10"
              y="52"
              text-anchor="end"
              fill="white"
              font-size="8"
              class="label">W</text
            >
          </svg>
        </div>

        <!-- Box with NE/SE/SW/NW -->
        <div class="grid-item">
          <h3>Box</h3>
          <svg viewBox="0 0 100 100" class="grid-svg">
            <line
              x1="25"
              y1="25"
              x2="75"
              y2="75"
              stroke="white"
              stroke-width="0.5"
              opacity="0.3"
            />
            <line
              x1="75"
              y1="25"
              x2="25"
              y2="75"
              stroke="white"
              stroke-width="0.5"
              opacity="0.3"
            />
            {#each boxPoints as point}
              <circle cx={point.x} cy={point.y} r="2.5" fill="white" />
            {/each}
            <!-- Labels -->
            <text
              x="75"
              y="20"
              text-anchor="middle"
              fill="white"
              font-size="8"
              class="label">NE</text
            >
            <text
              x="80"
              y="77"
              text-anchor="start"
              fill="white"
              font-size="8"
              class="label">SE</text
            >
            <text
              x="25"
              y="83"
              text-anchor="middle"
              fill="white"
              font-size="8"
              class="label">SW</text
            >
            <text
              x="20"
              y="27"
              text-anchor="end"
              fill="white"
              font-size="8"
              class="label">NW</text
            >
          </svg>
        </div>
      </div>

      <button class="next-button" onclick={handleNext}>Done</button>
    </div>
  {/if}
</div>

<style>
  .grid-experience {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 2rem;
    overflow-y: auto;
  }

  .page {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    max-width: 800px;
    margin: 0 auto;
    width: 100%;
  }

  h2 {
    font-size: 2rem;
    font-weight: 700;
    color: white;
    margin: 0;
    text-align: center;
  }

  h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: white;
    margin: 0;
    text-align: center;
  }

  p {
    font-size: 1.125rem;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.9);
    margin: 0;
  }

  .grids-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
    margin: 1rem 0;
  }

  .grid-item {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .grid-svg {
    width: 100%;
    max-width: 300px;
    height: auto;
    aspect-ratio: 1;
    margin: 0 auto;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 12px;
    border: 2px solid rgba(255, 255, 255, 0.1);
  }

  .grid-svg.merged {
    max-width: 400px;
  }

  .merged-grid-container {
    display: flex;
    justify-content: center;
    margin: 1rem 0;
  }

  .label {
    animation: fadeIn 0.6s ease-in-out;
    font-weight: 700;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  .next-button {
    align-self: center;
    padding: 1rem 3rem;
    background: rgba(74, 158, 255, 0.2);
    border: 2px solid rgba(74, 158, 255, 0.5);
    border-radius: 12px;
    color: white;
    font-size: 1.125rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
    min-height: 56px;
    margin-top: 1rem;
  }

  .next-button:hover {
    background: rgba(74, 158, 255, 0.3);
    border-color: rgba(74, 158, 255, 0.7);
    transform: translateY(-2px);
  }

  @media (max-width: 768px) {
    .grid-experience {
      padding: 1rem;
    }

    .grids-container {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }

    h2 {
      font-size: 1.5rem;
    }

    p {
      font-size: 1rem;
    }
  }
</style>
