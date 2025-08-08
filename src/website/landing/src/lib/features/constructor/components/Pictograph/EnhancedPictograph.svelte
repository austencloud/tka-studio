<!--
🎨 ENHANCED PICTOGRAPH COMPONENT

Enterprise-grade pictograph component with full rendering capabilities.
Integrates with the sophisticated pictograph service architecture.

Based on: Modern desktop app pictograph patterns + TKA enterprise DI system
-->

<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { ApplicationFactory } from '$lib/shared/di/ApplicationFactory.js';
  import type {
    IPictographRenderer,
    IPictographOrchestrator,
    RendererVisibilityOptions
  } from '$lib/shared/pictograph/interfaces/IPictographRenderer.js';
  import type { PictographData } from '@tka/domain';

  // ============================================================================
  // COMPONENT PROPS
  // ============================================================================

  export let pictographData: PictographData | null = null;
  export let width: number = 300;
  export let height: number = 300;
  export let showGrid: boolean = true;
  export let showArrows: boolean = true;
  export let showProps: boolean = true;
  export let showGlyphs: boolean = true;
  export let isInteractive: boolean = false;
  export let isSelected: boolean = false;
  export let className: string = '';

  // ============================================================================
  // COMPONENT STATE
  // ============================================================================

  let containerElement: HTMLDivElement;
  let svgElement: SVGElement | null = null;
  let pictographRenderer: IPictographRenderer | null = null;
  let pictographOrchestrator: IPictographOrchestrator | null = null;
  let isLoading: boolean = true;
  let error: string | null = null;

  // ============================================================================
  // LIFECYCLE METHODS
  // ============================================================================

  onMount(async () => {
    try {
      await initializePictographServices();
      await renderPictograph();
    } catch (err) {
      console.error('Failed to initialize pictograph:', err);
      error = err instanceof Error ? err.message : 'Unknown error';
    } finally {
      isLoading = false;
    }
  });

  onDestroy(() => {
    cleanup();
  });

  // ============================================================================
  // SERVICE INITIALIZATION
  // ============================================================================

  async function initializePictographServices(): Promise<void> {
    try {
      // Create application container
      const container = ApplicationFactory.createProductionApp();

      // Resolve pictograph services
      pictographRenderer = container.resolve('IPictographRenderer');
      pictographOrchestrator = container.resolve('IPictographOrchestrator');

      // Configure visibility options
      const visibilityOptions: RendererVisibilityOptions = {
        grid: showGrid,
        arrows: showArrows,
        props: showProps,
        tka: showGlyphs,
        vtg: showGlyphs,
        elemental: showGlyphs,
        positions: showGlyphs,
        blueMotion: true,
        redMotion: true
      };

      pictographRenderer.setVisibility(visibilityOptions);

    } catch (error) {
      console.error('Failed to initialize pictograph services:', error);
      throw error;
    }
  }

  // ============================================================================
  // RENDERING METHODS
  // ============================================================================

  async function renderPictograph(): Promise<void> {
    if (!pictographRenderer || !containerElement) {
      return;
    }

    try {
      // Clear existing content
      clearPictograph();

      // Create pictograph data if not provided
      const dataToRender = pictographData || createDefaultPictograph();

      // Render pictograph
      svgElement = await pictographRenderer.renderPictograph(dataToRender);

      // Configure SVG element
      configureSVGElement(svgElement);

      // Add to container
      containerElement.appendChild(svgElement);

    } catch (error) {
      console.error('Failed to render pictograph:', error);
      renderErrorState();
    }
  }

  function createDefaultPictograph(): PictographData {
    if (!pictographOrchestrator) {
      throw new Error('Pictograph orchestrator not initialized');
    }

    return pictographOrchestrator.createPictograph();
  }

  function configureSVGElement(svg: SVGElement): void {
    // Set dimensions
    svg.setAttribute('width', width.toString());
    svg.setAttribute('height', height.toString());
    svg.setAttribute('viewBox', '0 0 950 950');

    // Set styling
    svg.style.maxWidth = '100%';
    svg.style.maxHeight = '100%';
    svg.style.display = 'block';

    // Add interaction classes
    if (isInteractive) {
      svg.classList.add('pictograph-interactive');
    }

    if (isSelected) {
      svg.classList.add('pictograph-selected');
    }

    // Add custom classes
    if (className) {
      svg.classList.add(...className.split(' '));
    }
  }

  function clearPictograph(): void {
    if (containerElement) {
      containerElement.innerHTML = '';
    }
    svgElement = null;
  }

  function renderErrorState(): void {
    if (!containerElement) return;

    const errorDiv = document.createElement('div');
    errorDiv.className = 'pictograph-error';
    errorDiv.innerHTML = `
      <div class="error-content">
        <div class="error-icon">⚠️</div>
        <div class="error-message">Failed to render pictograph</div>
        <div class="error-details">${error || 'Unknown error'}</div>
      </div>
    `;

    containerElement.appendChild(errorDiv);
  }

  function renderLoadingState(): void {
    if (!containerElement) return;

    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'pictograph-loading';
    loadingDiv.innerHTML = `
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <div class="loading-message">Loading pictograph...</div>
      </div>
    `;

    containerElement.appendChild(loadingDiv);
  }

  // ============================================================================
  // REACTIVE UPDATES
  // ============================================================================

  $: if (pictographData && pictographRenderer && !isLoading) {
    renderPictograph();
  }

  $: if (pictographRenderer && !isLoading) {
    const visibilityOptions: RendererVisibilityOptions = {
      grid: showGrid,
      arrows: showArrows,
      props: showProps,
      tka: showGlyphs,
      vtg: showGlyphs,
      elemental: showGlyphs,
      positions: showGlyphs,
      blueMotion: true,
      redMotion: true
    };

    pictographRenderer.setVisibility(visibilityOptions);
    renderPictograph();
  }

  // ============================================================================
  // CLEANUP
  // ============================================================================

  function cleanup(): void {
    clearPictograph();
    pictographRenderer = null;
    pictographOrchestrator = null;
  }

  // ============================================================================
  // EVENT HANDLERS
  // ============================================================================

  function handleClick(event: MouseEvent): void {
    if (!isInteractive) return;

    // Dispatch custom event for parent components
    const detail = {
      pictographData,
      svgElement,
      clickPosition: { x: event.offsetX, y: event.offsetY }
    };

    const customEvent = new CustomEvent('pictographClick', { detail });
    containerElement?.dispatchEvent(customEvent);
  }

  function handleMouseEnter(): void {
    if (!isInteractive || !svgElement) return;

    svgElement.classList.add('pictograph-hover');
  }

  function handleMouseLeave(): void {
    if (!isInteractive || !svgElement) return;

    svgElement.classList.remove('pictograph-hover');
  }
</script>

<!-- ============================================================================ -->
<!-- COMPONENT TEMPLATE -->
<!-- ============================================================================ -->

<div
  class="pictograph-container {className}"
  class:interactive={isInteractive}
  class:selected={isSelected}
  class:loading={isLoading}
  class:error={error !== null}
  bind:this={containerElement}
  on:click={handleClick}
  on:mouseenter={handleMouseEnter}
  on:mouseleave={handleMouseLeave}
  style="width: {width}px; height: {height}px;"
>
  {#if isLoading}
    <div class="pictograph-loading">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <div class="loading-message">Loading pictograph...</div>
      </div>
    </div>
  {/if}

  {#if error}
    <div class="pictograph-error">
      <div class="error-content">
        <div class="error-icon">⚠️</div>
        <div class="error-message">Failed to render pictograph</div>
        <div class="error-details">{error}</div>
      </div>
    </div>
  {/if}
</div>

<!-- ============================================================================ -->
<!-- COMPONENT STYLES -->
<!-- ============================================================================ -->

<style>
  .pictograph-container {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background: white;
    border-radius: 8px;
    overflow: hidden;
    transition: all 0.2s ease;
  }

  .pictograph-container.interactive {
    cursor: pointer;
  }

  .pictograph-container.interactive:hover {
    transform: scale(1.02);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .pictograph-container.selected {
    border: 3px solid #007acc;
    box-shadow: 0 0 0 2px rgba(0, 122, 204, 0.2);
  }

  .pictograph-container.loading {
    background: #f8f9fa;
  }

  .pictograph-container.error {
    background: #fff5f5;
    border: 1px solid #fed7d7;
  }

  /* Loading State */
  .pictograph-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
  }

  .loading-content {
    text-align: center;
    color: #666;
  }

  .loading-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #007acc;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 8px;
  }

  .loading-message {
    font-size: 14px;
    font-weight: 500;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  /* Error State */
  .pictograph-error {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
  }

  .error-content {
    text-align: center;
    color: #e53e3e;
  }

  .error-icon {
    font-size: 32px;
    margin-bottom: 8px;
  }

  .error-message {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 4px;
  }

  .error-details {
    font-size: 12px;
    color: #a0a0a0;
  }

  /* Interactive States */
  :global(.pictograph-interactive:hover) {
    filter: brightness(1.05);
  }

  :global(.pictograph-selected) {
    filter: drop-shadow(0 0 8px rgba(0, 122, 204, 0.4));
  }

  :global(.pictograph-hover) {
    filter: brightness(1.1);
  }
</style>
