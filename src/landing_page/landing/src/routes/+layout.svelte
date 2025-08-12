<script lang="ts">
    import '../app.css';
    import NavBar from '../components/NavBar.svelte';
    import Footer from '../components/Footer.svelte';
    import BackgroundProvider from '$lib/features/backgrounds/Backgrounds/BackgroundProvider.svelte';
    import BackgroundCanvas from '$lib/features/backgrounds/Backgrounds/BackgroundCanvas.svelte';
    import { onMount } from 'svelte';
    import type { LayoutData } from './$types.js';
    import { browser } from '$app/environment';
  import { initializePictographData } from '$lib/features/constructor/stores/pictograph/pictographStore.js';

    // Props from layout server
    export let data: LayoutData;

    // Default to night sky background - full system with constellations and moon
    let currentBackground: 'deepOcean' | 'snowfall' | 'nightSky' = 'nightSky';
    let initialized = false;

    function handleBackgroundChange(background: string) {
      if (background === 'deepOcean' || background === 'snowfall' || background === 'nightSky') {
        currentBackground = background;
      }
    }

    onMount(() => {
        if (browser && !initialized) {
            // Check if the load function returned data successfully
            if (data?.csvData && !data.error) {
                try {
                    initializePictographData(data.csvData);
                    initialized = true; // Mark as initialized
                } catch (initError) {
                    console.error('Layout onMount: Error calling initializePictographData:', initError);
                    // Optionally display an error message to the user here
                }
            } else if (data?.error) {
                console.error('Layout onMount: Error from server load function:', data.error);
                // Optionally display an error message to the user here
            } else {
                console.warn('Layout onMount: No CSV data received from server');
            }
        }
    });
  </script>

  <!-- Background System -->
  <BackgroundProvider backgroundType={currentBackground}>
    <BackgroundCanvas backgroundType={currentBackground} />

    <!-- App Content with Dynamic Background -->
    <div class="app-content" data-background={currentBackground}>

    <header>
      <NavBar {currentBackground} onBackgroundChange={handleBackgroundChange} />
    </header>

    <main>
      <slot />  <!-- This is where child pages will be rendered -->
    </main>

    <footer>
      <Footer />
    </footer>
  </div>
  </BackgroundProvider>

  <style>
    .app-content {
      position: relative;
      z-index: 1; /* Ensure content is above background */
      min-height: 100vh;
      width: 100%;
      display: flex;
      flex-direction: column;
    }

    header {
      /* Remove background to let NavBar handle its own styling */
      width: 100%;
      padding: 0;
      color: white;
      position: relative;
      z-index: 10; /* Ensure navbar is above everything */
    }

    main {
      width: 100%;
      padding: var(--container-padding);
      min-height: 80vh;
      flex: 1;
      position: relative;
    }

    footer {
      width: 100%;
      margin-top: 20px;
      position: relative;
    }
  </style>
