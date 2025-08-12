#!/usr/bin/env node
/**
 * Convert Grid SVGs to PNG Images
 *
 * This script converts the grid mode SVG files to PNG format so they can be treated
 * consistently with other image-based dropdowns like start position images.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { join } from 'path';

// Use puppeteer to convert SVG to PNG
async function convertSvgToPng() {
	try {
		// Dynamic import for ES modules
		const puppeteer = await import('puppeteer');

		const browser = await puppeteer.default.launch();
		const page = await browser.newPage();

		// Set viewport to consistent size (same as position images)
		await page.setViewport({ width: 400, height: 400 });

		const gridTypes = ['diamond', 'box', 'skewed'];
		const gridDir = './static/images/grid/';
		const outputDir = './static/images/grid_images/';

		// Create output directory if it doesn't exist
		if (!existsSync(outputDir)) {
			mkdirSync(outputDir, { recursive: true });
		}

		for (const gridType of gridTypes) {
			const svgPath = join(gridDir, `${gridType}_grid.svg`);

			if (existsSync(svgPath)) {
				console.log(`Converting ${gridType}_grid.svg to PNG...`);

				// Read SVG content
				const svgContent = readFileSync(svgPath, 'utf8');

				// Create HTML with SVG
				const html = `
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <style>
                            body {
                                margin: 0;
                                padding: 20px;
                                background: white;
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                width: 360px;
                                height: 360px;
                            }
                            svg {
                                max-width: 320px;
                                max-height: 320px;
                                width: 100%;
                                height: 100%;
                            }
                        </style>
                    </head>
                    <body>
                        ${svgContent}
                    </body>
                    </html>
                `;

				// Load HTML and capture screenshot
				await page.setContent(html);
				await page.waitForTimeout(100); // Wait for render

				const screenshot = await page.screenshot({
					type: 'png',
					clip: { x: 0, y: 0, width: 400, height: 400 },
				});

				// Save PNG file
				const outputPath = join(outputDir, `${gridType}.png`);
				writeFileSync(outputPath, screenshot);

				console.log(`✅ Created ${outputPath}`);
			} else {
				console.warn(`⚠️  SVG file not found: ${svgPath}`);
			}
		}

		await browser.close();
		console.log('🎉 Grid SVG to PNG conversion complete!');
	} catch (error) {
		console.error('❌ Error converting SVGs:', error);
		process.exit(1);
	}
}

// Run the conversion
convertSvgToPng();
