// HTML-based SVG preloader - generates link rel="preload" tags
(function() {
  'use strict';

  // Generate all SVG paths that need preloading
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

  // All props - most commonly used first for priority loading
  const props = [
    'staff', 'fan', 'club', 'hand', 'triad', 'sword',  // Most common
    'bigstaff', 'bigfan', 'bigtriad', 'staff_v2',      // Variants
    'buugeng', 'bigbuugeng', 'doublestar', 'bigdoublestar', // Specialty
    'eightrings', 'bigeightrings', 'minihoop', 'bighoop',   // Rings
    'fractalgeng', 'quiad', 'ukulele', 'guitar', 'chicken'  // Rare
  ];

  props.forEach(prop => {
    allSvgs.push(`/images/props/${prop}.svg`);
  });

  // Other essential SVGs
  allSvgs.push('/images/arrow.svg', '/images/blank.svg', '/images/dash.svg', '/images/same_opp_dot.svg');

  // Create preload link elements and insert into head
  const head = document.head || document.getElementsByTagName('head')[0];
  let linksAdded = 0;

  console.log(`🔗 Generating ${allSvgs.length} preload link tags...`);

  allSvgs.forEach((svgPath, index) => {
    const link = document.createElement('link');
    link.rel = 'preload';
    link.as = 'image';
    link.href = svgPath;

    // Add high priority for commonly used SVGs (first 50)
    if (index < 50) {
      link.setAttribute('fetchpriority', 'high');
    }

    // Error handling
    link.onerror = () => {
      console.warn(`❌ Failed to preload: ${svgPath}`);
    };

    link.onload = () => {
      linksAdded++;
      if (linksAdded % 25 === 0) {
        console.log(`✅ Preloaded ${linksAdded}/${allSvgs.length} SVGs via link tags`);
      }

      if (linksAdded === allSvgs.length) {
        console.log('🎉 ALL SVG PRELOAD LINKS PROCESSED!');

        // Mark as complete for any components that need to know
        window.svgsPreloaded = true;
        window.svgPreloadComplete = true;

        // Dispatch completion event
        window.dispatchEvent(new CustomEvent('svgsPreloaded', {
          detail: { loaded: linksAdded, total: allSvgs.length }
        }));
      }
    };

    head.appendChild(link);
  });

})();
