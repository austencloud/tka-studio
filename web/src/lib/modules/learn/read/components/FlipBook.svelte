<!--
FlipBook Component

The main adorable flipbook component that displays PDF pages with beautiful page-turning animations.
-->
<script lang="ts">
  import { resolve, TYPES } from "$shared";
  import { onDestroy, onMount } from "svelte";
  import type { FlipBookConfig } from "../domain";
  import type { IFlipBookService, IPDFService } from "../services/contracts";
  import { createReadState } from "../state";
  import PDFLoader from "./PDFLoader.svelte";

  // Props
  const { 
    pdfUrl = "/static/Level 1.pdf",
    config = {} 
  } = $props<{
    pdfUrl?: string;
    config?: Partial<FlipBookConfig>;
  }>();

  // Service resolution
  const pdfService = resolve(TYPES.IPDFService) as IPDFService;
  const flipBookService = resolve(TYPES.IFlipBookService) as IFlipBookService;

  // State
  const readState = createReadState(pdfService, flipBookService);
  
  // Flipbook container reference
  let flipBookContainer = $state<HTMLElement>();

  // Initialize on mount
  onMount(async () => {
    try {
      console.log("📚 FlipBook: Component mounted, loading PDF");

      // Start loading immediately
      const loadPromise = readState.loadPDF(pdfUrl);

      // Wait for both PDF loading and container to be ready
      await loadPromise;

      // Wait for container to be fully rendered and sized
      await new Promise(resolve => setTimeout(resolve, 300));

      // Ensure container has dimensions
      if (flipBookContainer) {
        const rect = flipBookContainer.getBoundingClientRect();
        console.log("📚 FlipBook: Container dimensions", {
          width: rect.width,
          height: rect.height,
          clientWidth: flipBookContainer.clientWidth,
          clientHeight: flipBookContainer.clientHeight
        });
      }

      // Initialize the flipbook once PDF is loaded
      if (readState.hasPages() && flipBookContainer) {
        await readState.initializeFlipBook(flipBookContainer, config);
      }
    } catch (error) {
      console.error("📚 FlipBook: Error during initialization", error);
    }
  });

  // Cleanup on destroy
  onDestroy(() => {
    readState.cleanup();
  });

  // Monitor visibility and restore page when component becomes visible
  let flipBookWrapper = $state<HTMLElement>();
  
  // Also trigger restoration when flipbook is ready
  $effect(() => {
    if (readState.isFlipBookInitialized && readState.isReady()) {
      console.log("📚 FlipBook: Flipbook is ready, attempting page restoration");
      setTimeout(() => {
        readState.restoreToSavedPage();
      }, 300);
    }
  });
  
  $effect(() => {
    if (!flipBookWrapper) return;
    
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && readState.isFlipBookInitialized) {
            console.log("📚 FlipBook: Component became visible, restoring page");
            // Small delay to ensure everything is ready
            setTimeout(() => {
              readState.restoreToSavedPage();
            }, 200);
          }
        });
      },
      { threshold: 0.1 }
    );
    
    observer.observe(flipBookWrapper);
    
    return () => {
      observer.disconnect();
    };
  });

  // Navigation functions
  function handlePreviousPage() {
    readState.previousPage();
  }

  function handleNextPage() {
    readState.nextPage();
  }

  function handleGoToPage(pageNumber: number) {
    readState.goToPage(pageNumber);
  }
</script>

<div class="flipbook-wrapper" bind:this={flipBookWrapper}>
  {#if readState.loadingState.isLoading || !readState.isReady()}
    <PDFLoader loadingState={readState.loadingState} />
  {:else}
    <div class="flipbook-container">
      <!-- Flipbook Display -->
      <div class="flipbook-display">
        <div
          bind:this={flipBookContainer}
          class="flipbook-element"
        ></div>
      </div>
    </div>
  {/if}

  <!-- Navigation Controls - always visible -->
  <div class="flipbook-controls">
    <button
      class="nav-button prev-button"
      onclick={handlePreviousPage}
      disabled={readState.currentPage <= 1 || readState.loadingState.isLoading}
    >
      ← Previous
    </button>

    <div class="page-info">
      <span class="current-page">{readState.currentPage}</span>
      <span class="page-separator">of</span>
      <span class="total-pages">{readState.totalPages()}</span>
    </div>

    <button
      class="nav-button next-button"
      onclick={handleNextPage}
      disabled={readState.currentPage >= readState.totalPages() || readState.loadingState.isLoading}
    >
      Next →
    </button>
  </div>

  <!-- Page Jump Controls - always visible -->
  <div class="page-jump">
    <label for="page-input">Go to page:</label>
    <input
      id="page-input"
      type="number"
      min="1"
      max={readState.totalPages()}
      value={readState.currentPage}
      disabled={readState.loadingState.isLoading}
      onchange={(e) => {
        const target = e.target as HTMLInputElement;
        const pageNumber = parseInt(target.value);
        if (pageNumber >= 1 && pageNumber <= readState.totalPages()) {
          handleGoToPage(pageNumber);
        }
      }}
    />
  </div>
</div>

<style>
  .flipbook-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    min-height: 100vh;
    padding: 1rem;
    box-sizing: border-box;
  }

  .flipbook-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    height: 100%;
    max-width: 1200px;
    flex: 1;
  }



  .flipbook-display {
    position: relative;
    flex: 1;
    width: 100%;
    height: 70vh; /* Reduced height to allow scrolling */
    max-height: 700px; /* Prevent it from being too tall */
    min-height: 500px; /* Ensure minimum height */
    margin-bottom: 2rem; /* More space at bottom */
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    overflow: visible;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .flipbook-element {
    width: 100%; /* Take full width of container */
    height: 100%; /* Take full height of container */
    min-width: 800px; /* Ensure minimum width for book */
    min-height: 600px; /* Ensure minimum height for book */
    display: flex;
    align-items: center;
    justify-content: center;
  }



  .flipbook-controls {
    display: flex;
    align-items: center;
    gap: 2rem;
    margin-bottom: 1rem;
  }

  .nav-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 500;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  }

  .nav-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
  }

  .nav-button:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  .page-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.1rem;
    color: #2c3e50;
    font-weight: 500;
  }

  .current-page {
    color: #667eea;
    font-weight: 600;
    font-size: 1.2rem;
  }

  .page-separator {
    color: #7f8c8d;
  }

  .total-pages {
    color: #2c3e50;
  }

  .page-jump {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #2c3e50;
  }

  .page-jump label {
    font-size: 0.9rem;
    color: #7f8c8d;
  }

  .page-jump input {
    width: 60px;
    padding: 0.25rem 0.5rem;
    border: 2px solid #ecf0f1;
    border-radius: 4px;
    text-align: center;
    font-size: 0.9rem;
  }

  .page-jump input:focus {
    outline: none;
    border-color: #667eea;
  }

  /* Responsive design */
  @media (max-width: 768px) {
    .flipbook-wrapper {
      padding: 0.5rem;
    }



    .flipbook-controls {
      flex-direction: column;
      gap: 1rem;
    }

    .nav-button {
      padding: 0.5rem 1rem;
      font-size: 0.9rem;
    }
  }
</style>