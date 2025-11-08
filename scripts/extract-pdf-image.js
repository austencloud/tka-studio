import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { createCanvas } from "canvas";
import * as pdfjsLib from "pdfjs-dist/legacy/build/pdf.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configure PDF.js worker
pdfjsLib.GlobalWorkerOptions.workerSrc =
  "pdfjs-dist/legacy/build/pdf.worker.mjs";

async function extractFirstImage() {
  try {
    console.log("Starting PDF image extraction...");

    // Read the PDF file
    const pdfPath = path.join(__dirname, "..", "static", "Level 1.pdf");
    const pdfData = new Uint8Array(fs.readFileSync(pdfPath));

    // Load the PDF document
    const loadingTask = pdfjsLib.getDocument({ data: pdfData });
    const pdfDoc = await loadingTask.promise;

    console.log(`PDF loaded successfully - ${pdfDoc.numPages} pages`);

    // Get the first page
    const page = await pdfDoc.getPage(1);
    console.log("First page loaded");

    // Get page viewport
    const viewport = page.getViewport({ scale: 2.0 }); // Higher scale for better quality

    console.log(`Page dimensions: ${viewport.width} x ${viewport.height}`);

    // Create canvas
    const canvas = createCanvas(viewport.width, viewport.height);
    const context = canvas.getContext("2d");

    // Render page to canvas
    const renderContext = {
      canvasContext: context,
      viewport: viewport,
    };

    console.log("Rendering page to canvas...");
    await page.render(renderContext).promise;

    // Save as PNG
    const outputPath = path.join(
      __dirname,
      "..",
      "static",
      "level-1-first-page.png"
    );
    const buffer = canvas.toBuffer("image/png");
    fs.writeFileSync(outputPath, buffer);

    console.log(`\n✅ Success! Image extracted to: ${outputPath}`);
    console.log(`Image size: ${viewport.width} x ${viewport.height} pixels`);
    console.log(`File size: ${(buffer.length / 1024).toFixed(2)} KB`);
  } catch (error) {
    console.error("❌ Error extracting image:", error);
    console.error(error.stack);
  }
}

extractFirstImage();
