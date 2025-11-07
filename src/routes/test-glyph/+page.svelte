<script lang="ts">
  import { onMount } from 'svelte';

  let canvas: HTMLCanvasElement;
  let testResults = $state<string[]>([]);

  function log(message: string) {
    testResults.push(message);
    console.log('[TEST]', message);
  }

  async function testDirectSVGToCanvas() {
    log('=== Test 1: Direct SVG to Canvas ===');
    
    // Create a simple SVG with a letter
    const svgString = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
        <rect x="10" y="10" width="80" height="80" fill="blue" />
        <text x="50" y="60" font-size="40" text-anchor="middle" fill="white">S</text>
      </svg>
    `;

    try {
      const blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      
      const img = new Image();
      img.onload = () => {
        log('✅ Simple SVG loaded successfully');
        const ctx = canvas.getContext('2d');
        if (ctx) {
          ctx.fillStyle = 'white';
          ctx.fillRect(0, 0, canvas.width, canvas.height);
          ctx.drawImage(img, 0, 0, 100, 100);
          log('✅ Simple SVG drawn to canvas');
        }
        URL.revokeObjectURL(url);
      };
      img.onerror = (e) => {
        log('❌ Simple SVG failed to load: ' + e);
      };
      img.src = url;
    } catch (error) {
      log('❌ Error: ' + error);
    }
  }

  async function testExternalSVGFetch() {
    log('=== Test 2: Fetch External SVG ===');
    
    try {
      const response = await fetch('/images/letters_trimmed/Type1/S.svg');
      const svgText = await response.text();
      log('✅ Fetched external SVG: ' + svgText.substring(0, 100) + '...');
      
      // Try to render it
      const blob = new Blob([svgText], { type: 'image/svg+xml;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      
      const img = new Image();
      img.onload = () => {
        log('✅ External SVG loaded as image');
        const ctx = canvas.getContext('2d');
        if (ctx) {
          ctx.fillStyle = 'lightgray';
          ctx.fillRect(120, 0, 100, 100);
          ctx.drawImage(img, 120, 0, 100, 100);
          log('✅ External SVG drawn to canvas at (120, 0)');
        }
        URL.revokeObjectURL(url);
      };
      img.onerror = (e) => {
        log('❌ External SVG failed to load as image: ' + e);
      };
      img.src = url;
    } catch (error) {
      log('❌ Error fetching external SVG: ' + error);
    }
  }

  async function testInlinedSVG() {
    log('=== Test 3: SVG with Inlined External Content ===');
    
    try {
      // Fetch the external SVG
      const response = await fetch('/images/letters_trimmed/Type1/S.svg');
      const svgText = await response.text();
      
      // Parse it
      const parser = new DOMParser();
      const externalSvgDoc = parser.parseFromString(svgText, 'image/svg+xml');
      const externalSvgRoot = externalSvgDoc.documentElement;
      
      // Get viewBox
      const viewBox = externalSvgRoot.getAttribute('viewBox');
      log('External SVG viewBox: ' + viewBox);
      
      // Create a new SVG with the content inlined
      const inlinedSvg = `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
          <g transform="translate(10, 10) scale(0.8)">
            ${externalSvgRoot.innerHTML}
          </g>
        </svg>
      `;
      
      log('Inlined SVG length: ' + inlinedSvg.length);
      
      const blob = new Blob([inlinedSvg], { type: 'image/svg+xml;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      
      const img = new Image();
      img.onload = () => {
        log('✅ Inlined SVG loaded as image');
        const ctx = canvas.getContext('2d');
        if (ctx) {
          ctx.fillStyle = 'lightyellow';
          ctx.fillRect(240, 0, 100, 100);
          ctx.drawImage(img, 240, 0, 100, 100);
          log('✅ Inlined SVG drawn to canvas at (240, 0)');
        }
        URL.revokeObjectURL(url);
      };
      img.onerror = (e) => {
        log('❌ Inlined SVG failed to load as image: ' + e);
      };
      img.src = url;
    } catch (error) {
      log('❌ Error with inlined SVG: ' + error);
    }
  }

  async function testDataURL() {
    log('=== Test 4: Data URL (like AnimatorCanvas uses) ===');
    
    try {
      const response = await fetch('/images/letters_trimmed/Type1/S.svg');
      const svgText = await response.text();
      
      // Use data URL instead of blob URL
      const dataUrl = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svgText)}`;
      
      const img = new Image();
      img.onload = () => {
        log('✅ Data URL SVG loaded');
        const ctx = canvas.getContext('2d');
        if (ctx) {
          ctx.fillStyle = 'lightblue';
          ctx.fillRect(360, 0, 100, 100);
          ctx.drawImage(img, 360, 0, 100, 100);
          log('✅ Data URL SVG drawn to canvas at (360, 0)');
        }
      };
      img.onerror = (e) => {
        log('❌ Data URL SVG failed: ' + e);
      };
      img.src = dataUrl;
    } catch (error) {
      log('❌ Error with data URL: ' + error);
    }
  }

  onMount(async () => {
    await testDirectSVGToCanvas();
    await new Promise(resolve => setTimeout(resolve, 500));
    
    await testExternalSVGFetch();
    await new Promise(resolve => setTimeout(resolve, 500));
    
    await testInlinedSVG();
    await new Promise(resolve => setTimeout(resolve, 500));
    
    await testDataURL();
  });
</script>

<div style="padding: 20px; font-family: monospace;">
  <h1>Glyph Rendering Debug Test</h1>
  
  <div style="margin: 20px 0;">
    <h2>Canvas Output:</h2>
    <canvas bind:this={canvas} width="500" height="120" style="border: 2px solid black; background: white;"></canvas>
    <p style="font-size: 12px; color: #666;">
      Test 1 (0,0): Simple SVG | Test 2 (120,0): External SVG | Test 3 (240,0): Inlined | Test 4 (360,0): Data URL
    </p>
  </div>

  <div style="margin: 20px 0;">
    <h2>Test Results:</h2>
    <div style="background: #f5f5f5; padding: 10px; border-radius: 4px; max-height: 400px; overflow-y: auto;">
      {#each testResults as result}
        <div style="padding: 4px 0; border-bottom: 1px solid #ddd;">
          {result}
        </div>
      {/each}
    </div>
  </div>
</div>

