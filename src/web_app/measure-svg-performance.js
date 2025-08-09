// Performance measurement test for SVG loading
const puppeteer = require('puppeteer');

async function measureSvgLoadingPerformance() {
  console.log('🔍 Starting SVG loading performance measurement...');

  const browser = await puppeteer.launch({
    headless: false,
    devtools: true
  });

  const page = await browser.newPage();

  // Enable console logging from the page
  page.on('console', msg => {
    const text = msg.text();
    if (text.includes('SVG') || text.includes('preload') || text.includes('🚀') || text.includes('✅') || text.includes('🎉')) {
      console.log(`[BROWSER] ${text}`);
    }
  });

  // Inject performance measurement script
  await page.evaluateOnNewDocument(() => {
    const startTime = performance.now();
    let preloadCompleteTime = null;
    let firstArrowTime = null;
    let firstPropTime = null;

    // Monitor preload completion
    window.addEventListener('svgsPreloaded', () => {
      preloadCompleteTime = performance.now();
      console.log(`🎯 Preload completed at: ${(preloadCompleteTime - startTime).toFixed(2)}ms`);
    });

    // Monitor when first arrow appears
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === 1) {
            // Check for arrows
            if (node.classList && node.classList.contains('arrow') && !firstArrowTime) {
              firstArrowTime = performance.now();
              console.log(`🏹 First arrow appeared at: ${(firstArrowTime - startTime).toFixed(2)}ms`);
            }

            // Check for props
            if (node.classList && node.classList.contains('prop') && !firstPropTime) {
              firstPropTime = performance.now();
              console.log(`🎯 First prop appeared at: ${(firstPropTime - startTime).toFixed(2)}ms`);
            }
          }
        });
      });
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });

    // Log overall timing after everything settles
    setTimeout(() => {
      const endTime = performance.now();
      console.log(`📊 TIMING SUMMARY:`);
      console.log(`   - Preload complete: ${preloadCompleteTime ? (preloadCompleteTime - startTime).toFixed(2) : 'N/A'}ms`);
      console.log(`   - First arrow: ${firstArrowTime ? (firstArrowTime - startTime).toFixed(2) : 'N/A'}ms`);
      console.log(`   - First prop: ${firstPropTime ? (firstPropTime - startTime).toFixed(2) : 'N/A'}ms`);
      console.log(`   - Total time: ${(endTime - startTime).toFixed(2)}ms`);

      if (firstArrowTime && firstPropTime) {
        const diff = Math.abs(firstArrowTime - firstPropTime);
        console.log(`   - Arrow/Prop timing difference: ${diff.toFixed(2)}ms`);
      }
    }, 5000);
  });

  console.log('🌐 Navigating to http://localhost:5175/...');
  await page.goto('http://localhost:5175/', { waitUntil: 'networkidle0' });

  console.log('🎯 Clicking on Construct tab...');
  await page.click('[data-tab="construct"]');

  // Wait a bit for tab to load
  await page.waitForTimeout(1000);

  console.log('🎯 Looking for start position options...');

  // Try to find and click a start position
  try {
    await page.waitForSelector('.startpos-option', { timeout: 5000 });
    await page.click('.startpos-option');
    console.log('✅ Clicked start position');

    // Wait a bit to see the options load
    await page.waitForTimeout(3000);

  } catch (e) {
    console.log('⚠️ Could not find start position options, trying alternative selectors...');

    // Try alternative approach
    const constructContent = await page.$('.construct-content, .start-picker, [data-testid*="start"], [class*="start"]');
    if (constructContent) {
      console.log('✅ Found construct content area');
    }
  }

  // Keep browser open for manual inspection
  console.log('🔍 Browser will stay open for manual inspection...');
  await page.waitForTimeout(30000);

  await browser.close();
}

measureSvgLoadingPerformance().catch(console.error);
