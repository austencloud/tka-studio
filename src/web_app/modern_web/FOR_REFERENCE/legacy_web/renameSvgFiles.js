// renameSvgFiles.js

const fs = require("fs");
const path = require("path");
const { Letter } = require("./src/lib/types/Letter"); // Adjust the path as necessary

// Mapping from Letter enum to ASCII filenames
const letterFilenameMap = {
  // ASCII letters remain unchanged

  // Greek letters
  Σ: "Sigma",
  Δ: "Delta",
  θ: "theta",
  Ω: "Omega",
  Φ: "Phi",
  Ψ: "Psi",
  Λ: "Lambda",
  α: "alpha",
  β: "beta",
  Γ: "Gamma",

  // Greek letters with dash
  "W-": "WDash",
  "X-": "XDash",
  "Y-": "YDash",
  "Z-": "ZDash",
  "Σ-": "SigmaDash",
  "Δ-": "DeltaDash",
  "θ-": "thetaDash",
  "Ω-": "OmegaDash",
  "Φ-": "PhiDash",
  "Ψ-": "PsiDash",
  "Λ-": "LambdaDash",

  // Additional letters
  τ: "tau",
  "⊕": "terra",
  ζ: "zeta",
  η: "eta",
  μ: "mu",
  ν: "nu",
  // Add any other necessary mappings
};

/**
 * Returns the ASCII-safe filename for a given Letter.
 * @param {string} letter - The Letter enum value.
 * @returns {string} - The ASCII-safe filename without the .svg extension.
 */
function safeAsciiName(letter) {
  return letterFilenameMap[letter] || letter;
}

/**
 * Renames SVG files in the specified directory based on the mapping.
 * @param {string} typeFolder - The Type folder (e.g., Type1, Type2).
 */
function renameFilesInTypeFolder(typeFolder) {
  const folderPath = path.join(
    __dirname,
    "images",
    "letters_trimmed",
    typeFolder,
  );
  if (!fs.existsSync(folderPath)) {
    console.warn(`Folder ${folderPath} does not exist. Skipping...`);
    return;
  }

  const files = fs.readdirSync(folderPath);

  files.forEach((file) => {
    if (file.toLowerCase().endsWith(".svg")) {
      const baseName = path.basename(file, ".svg");
      const letter = baseName; // Assuming baseName matches Letter enum values

      const newFilename = safeAsciiName(letter);
      if (newFilename !== baseName) {
        const oldPath = path.join(folderPath, file);
        const newPath = path.join(folderPath, `${newFilename}.svg`);

        if (fs.existsSync(newPath)) {
          console.error(
            `Cannot rename ${file} to ${newFilename}.svg because it already exists.`,
          );
          return;
        }

        fs.renameSync(oldPath, newPath);
      }
    }
  });
}

// Main function to iterate through all Type folders
function main() {
  const typeFolders = [
    "Type1",
    "Type2",
    "Type3",
    "Type4",
    "Type5",
    "Type6",
    "Type7",
    "Type8",
    "Type9",
  ];

  typeFolders.forEach((typeFolder) => {
    renameFilesInTypeFolder(typeFolder);
  });
}

main();
