// Immediate SVG preloader - runs before anything else
(function() {
  'use strict';

  console.log('🚀 IMMEDIATE SVG PRELOADER STARTING...');

  // Generate all SVG paths
  const motionTypes = ['pro', 'anti', 'dash', 'static'];
  const orientations = ['from_radial', 'from_nonradial'];
  const turns = ['0.0', '0.5', '1.0', '1.5', '2.0', '2.5', '3.0'];

  const allSvgs = [];

  // Special arrows
  allSvgs.push('/images/arrows/float.svg', '/images/arrows/dash.svg', '/images/arrows/still.svg');

  // All arrow combinations
  for (const motionType of motionTypes) {
    for (const orientation of orientations) {
      for (const turn of turns) {
        allSvgs.push(`/images/arrows/${motionType}/${orientation}/${motionType}_${turn}.svg`);
      }
    }
  }

  // All props
  const props = [
    'bigbuugeng', 'bigfan', 'bigtriad', 'club', 'fan', 'hand', 'staff', 'triad',
    'bigdoublestar', 'bighoop', 'buugeng', 'doublestar', 'fractalgeng', 'minihoop',
    'staff_v2', 'ukulele', 'bigeightrings', 'bigstaff', 'chicken', 'eightrings',
    'guitar', 'quiad', 'sword'
  ];

  props.forEach(prop => {
    allSvgs.push(`/images/props/${prop}.svg`);
  });

  // Other essential SVGs
  allSvgs.push('/images/arrow.svg', '/images/blank.svg', '/images/dash.svg', '/images/same_opp_dot.svg');

  console.log(`📊 Preloading ${allSvgs.length} SVGs with aggressive caching...`);

  let loaded = 0;
  let errors = 0;

  // Create a cache object to store SVG content
  window.svgCache = window.svgCache || new Map();

  // More aggressive preloading with larger batches for instant loading
  async function preloadBatch(svgPaths, batchSize = 50) {
    for (let i = 0; i < svgPaths.length; i += batchSize) {
      const batch = svgPaths.slice(i, i + batchSize);

      await Promise.allSettled(batch.map(async (path) => {
        try {
          const response = await fetch(path, {
            headers: { 'Cache-Control': 'max-age=31536000' } // Cache for 1 year
          });

          if (response.ok) {
            const svgContent = await response.text();
            // Store in our cache AND let browser cache it
            window.svgCache.set(path, svgContent);
            loaded++;

            if (loaded % 25 === 0) {
              console.log(`✅ Cached ${loaded}/${allSvgs.length} SVGs...`);
            }
          } else {
            errors++;
            console.warn(`❌ Failed: ${path} (${response.status})`);
          }
        } catch (err) {
          errors++;
          console.warn(`❌ Error: ${path}`, err.message);
        }
      }));

      // NO DELAY - Load everything as fast as possible
    }
  }

  // Start preloading immediately
  preloadBatch(allSvgs).then(() => {
    console.log(`🎉 SVG PRELOAD COMPLETE! Loaded: ${loaded}, Errors: ${errors}`);
    console.log('🚀 ALL SVGS ARE NOW CACHED AND READY!');

    // Mark completion globally
    window.svgsPreloaded = true;
    window.svgPreloadComplete = true;

    // Dispatch event for components waiting for preload
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('svgsPreloaded', {
        detail: { loaded, errors, total: allSvgs.length }
      }));
    }
  });

})();
