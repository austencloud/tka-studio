import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Base directory - adjust this path as needed
const baseDir = "./src/lib/components";

// Directory structure
const structure = {
  GenerateTab: {
    // Main component
    "GenerateTab.svelte": "",

    // UI components
    ui: {
      "GenerateButton.svelte": "",
      "HeaderLabel.svelte": "",
      "GeneratorToggle.svelte": "",
      "LengthSelector.svelte": "",
      "TurnIntensity.svelte": "",
      "PropContinuity.svelte": "",
      LevelSelector: {
        "LevelSelector.svelte": "",
        "LevelButton.svelte": "",
      },
    },

    // Circular generator feature
    circular: {
      "CircularSequencer.svelte": "",
      "createCircularSequence.ts": "",
      "capExecutors.ts": "",
      "validators.ts": "",
      "store.ts": "",
      CAPPicker: {
        "CAPPicker.svelte": "",
        "CAPButton.svelte": "",
      },
    },

    // Freeform generator feature
    freeform: {
      "FreeformSequencer.svelte": "",
      "createFreeformSequence.ts": "",
      "letterPatterns.ts": "",
      "store.ts": "",
      LetterPicker: {
        "LetterPicker.svelte": "",
        "LetterButton.svelte": "",
      },
    },

    // Shared utilities
    utils: {
      "orientationCalculator.ts": "",
      "sequenceHelpers.ts": "",
      "rotationDeterminer.ts": "",
      "positionMaps.ts": "",
    },

    // Shared state
    store: {
      "generator.ts": "",
      "settings.ts": "",
      "selection.ts": "",
    },
  },
};

function createDirectoryStructure(baseDir, structure) {
  if (!fs.existsSync(baseDir)) {
    fs.mkdirSync(baseDir, { recursive: true });
    console.log(`Created directory: ${baseDir}`);
  }

  if (structure) {
    Object.entries(structure).forEach(([name, content]) => {
      const fullPath = path.join(baseDir, name);

      if (typeof content === "object") {
        if (!fs.existsSync(fullPath)) {
          fs.mkdirSync(fullPath, { recursive: true });
          console.log(`Created directory: ${fullPath}`);
        }
        createDirectoryStructure(fullPath, content);
      } else {
        if (!fs.existsSync(fullPath)) {
          fs.writeFileSync(fullPath, content);
          console.log(`Created file: ${fullPath}`);
        } else {
          console.log(`File already exists: ${fullPath}`);
        }
      }
    });
  }
}

createDirectoryStructure(baseDir, structure);

console.log("Done creating directory structure!");
