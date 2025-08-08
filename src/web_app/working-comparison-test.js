/**
 * Working Start Position Comparison Test
 *
 * A simple test that compares the actual start position props found in both apps
 */

import { chromium } from 'playwright';

async function runComparison() {
  console.log('🚀 Starting working comparison test...');

  const browser = await chromium.launch({ headless: false });

  try {
    // Test Modern App
    console.log('\n📱 Extracting data from Modern App...');
    const modernContext = await browser.newContext();
    const modernPage = await modernContext.newPage();

    await modernPage.goto('http://localhost:5177', { timeout: 30000 });
    await modernPage.waitForTimeout(3000); // Wait for content to load

    const modernProps = await modernPage.evaluate(() => {
      const props = [];

      // Look for prop elements with data-prop-color
      const propElements = document.querySelectorAll('[data-prop-color]');
      propElements.forEach((el, index) => {
        const rect = el.getBoundingClientRect();
        const color = el.getAttribute('data-prop-color');
        const transform = el.getAttribute('transform') || '';
        const style = window.getComputedStyle(el);

        // Try to extract position from transform or coordinates
        let x = rect.x;
        let y = rect.y;
        let rotation = 0;

        // Parse SVG transform if available
        if (transform) {
          const translateMatch = transform.match(/translate\(([^)]+)\)/);
          if (translateMatch) {
            const coords = translateMatch[1].split(',').map(v => parseFloat(v.trim()));
            x = coords[0] || x;
            y = coords[1] || y;
          }

          const rotateMatch = transform.match(/rotate\(([^)]+)\)/);
          if (rotateMatch) {
            rotation = parseFloat(rotateMatch[1]) || 0;
          }
        }

        props.push({
          index,
          color,
          x: Math.round(x),
          y: Math.round(y),
          rotation,
          transform,
          rectX: Math.round(rect.x),
          rectY: Math.round(rect.y),
          tagName: el.tagName
        });
      });

      return props;
    });

    await modernPage.screenshot({ path: './test-results/modern-props.png', fullPage: true });
    await modernContext.close();

    console.log(`✅ Modern app: Found ${modernProps.length} props`);
    modernProps.forEach(prop => {
      console.log(`   ${prop.color}: (${prop.x}, ${prop.y}) rotation: ${prop.rotation}° transform: ${prop.transform}`);
    });

    // Test Legacy App (if available)
    console.log('\n📱 Attempting to extract data from Legacy App...');
    let legacyProps = [];

    try {
      const legacyContext = await browser.newContext();
      const legacyPage = await legacyContext.newPage();

      await legacyPage.goto('http://localhost:5175', { timeout: 10000 });
      await legacyPage.waitForTimeout(3000);

      legacyProps = await legacyPage.evaluate(() => {
        const props = [];

        // Look for various prop selectors in legacy
        const selectors = ['[data-prop-color]', '.prop', 'circle[data-color]', '[data-color]'];

        selectors.forEach(selector => {
          const elements = document.querySelectorAll(selector);
          elements.forEach((el, index) => {
            const rect = el.getBoundingClientRect();
            const color = el.getAttribute('data-prop-color') ||
                         el.getAttribute('data-color') ||
                         el.getAttribute('fill') || 'unknown';
            const transform = el.getAttribute('transform') || el.style.transform || '';

            if (rect.width > 0 && rect.height > 0) {
              let x = rect.x;
              let y = rect.y;
              let rotation = 0;

              // Parse transform
              if (transform && transform !== 'none') {
                const translateMatch = transform.match(/translate\(([^)]+)\)/);
                if (translateMatch) {
                  const coords = translateMatch[1].split(',').map(v => parseFloat(v.trim()));
                  x = coords[0] || x;
                  y = coords[1] || y;
                }

                const rotateMatch = transform.match(/rotate\(([^)]+)\)/);
                if (rotateMatch) {
                  rotation = parseFloat(rotateMatch[1]) || 0;
                }
              }

              props.push({
                selector,
                index,
                color,
                x: Math.round(x),
                y: Math.round(y),
                rotation,
                transform,
                rectX: Math.round(rect.x),
                rectY: Math.round(rect.y),
                tagName: el.tagName
              });
            }
          });
        });

        return props;
      });

      await legacyPage.screenshot({ path: './test-results/legacy-props.png', fullPage: true });
      await legacyContext.close();

      console.log(`✅ Legacy app: Found ${legacyProps.length} props`);
      legacyProps.forEach(prop => {
        console.log(`   ${prop.color}: (${prop.x}, ${prop.y}) rotation: ${prop.rotation}° transform: ${prop.transform}`);
      });

    } catch (error) {
      console.log(`⚠️ Legacy app not accessible: ${error.message}`);
    }

    // Perform Comparison
    console.log('\n📊 COMPARISON RESULTS:');
    console.log('='.repeat(50));

    if (legacyProps.length === 0) {
      console.log('⚠️ Cannot compare - legacy app data not available');
      console.log('📋 Modern app analysis only:');

      // Group modern props by color
      const modernByColor = modernProps.reduce((acc, prop) => {
        if (!acc[prop.color]) acc[prop.color] = [];
        acc[prop.color].push(prop);
        return acc;
      }, {});

      Object.keys(modernByColor).forEach(color => {
        const props = modernByColor[color];
        console.log(`\n🎨 ${color.toUpperCase()} props (${props.length}):`);
        props.forEach((prop, index) => {
          console.log(`   ${index + 1}: Position (${prop.x}, ${prop.y}), Rotation ${prop.rotation}°`);
        });

        if (props.length > 1) {
          const avgX = props.reduce((sum, p) => sum + p.x, 0) / props.length;
          const avgY = props.reduce((sum, p) => sum + p.y, 0) / props.length;
          console.log(`   📍 Average position: (${avgX.toFixed(1)}, ${avgY.toFixed(1)})`);
        }
      });

    } else {
      console.log('✅ Comparing legacy vs modern props:');

      // Simple comparison by color
      const legacyByColor = legacyProps.reduce((acc, prop) => {
        if (!acc[prop.color]) acc[prop.color] = [];
        acc[prop.color].push(prop);
        return acc;
      }, {});

      const modernByColor = modernProps.reduce((acc, prop) => {
        if (!acc[prop.color]) acc[prop.color] = [];
        acc[prop.color].push(prop);
        return acc;
      }, {});

      const allColors = new Set([...Object.keys(legacyByColor), ...Object.keys(modernByColor)]);

      allColors.forEach(color => {
        const legacyCount = legacyByColor[color]?.length || 0;
        const modernCount = modernByColor[color]?.length || 0;

        console.log(`\n🎨 ${color.toUpperCase()} props:`);
        console.log(`   Legacy: ${legacyCount}, Modern: ${modernCount}`);

        if (legacyCount > 0 && modernCount > 0) {
          const legacyAvg = {
            x: legacyByColor[color].reduce((sum, p) => sum + p.x, 0) / legacyCount,
            y: legacyByColor[color].reduce((sum, p) => sum + p.y, 0) / legacyCount
          };
          const modernAvg = {
            x: modernByColor[color].reduce((sum, p) => sum + p.x, 0) / modernCount,
            y: modernByColor[color].reduce((sum, p) => sum + p.y, 0) / modernCount
          };

          const diffX = Math.abs(legacyAvg.x - modernAvg.x);
          const diffY = Math.abs(legacyAvg.y - modernAvg.y);
          const distance = Math.sqrt(diffX * diffX + diffY * diffY);

          console.log(`   📍 Position difference: (${diffX.toFixed(1)}, ${diffY.toFixed(1)}) = ${distance.toFixed(1)} pixels`);

          if (distance < 5) {
            console.log(`   ✅ Positions are very close (within 5 pixels)`);
          } else if (distance < 20) {
            console.log(`   ⚠️ Positions have minor differences (${distance.toFixed(1)} pixels)`);
          } else {
            console.log(`   ❌ Positions have significant differences (${distance.toFixed(1)} pixels)`);
          }
        }
      });
    }

    // Save comparison data
    const comparisonData = {
      timestamp: new Date().toISOString(),
      modern: {
        propCount: modernProps.length,
        props: modernProps
      },
      legacy: {
        propCount: legacyProps.length,
        props: legacyProps
      }
    };

    import('fs').then(fs => {
      fs.default.writeFileSync('./test-results/comparison-data.json', JSON.stringify(comparisonData, null, 2));
      console.log('\n💾 Comparison data saved to ./test-results/comparison-data.json');
    });

  } finally {
    await browser.close();
  }

  console.log('\n✅ Comparison test completed');
}

// Create test-results directory
import fs from 'fs';
if (!fs.existsSync('./test-results')) {
  fs.mkdirSync('./test-results', { recursive: true });
}

runComparison().catch(console.error);
