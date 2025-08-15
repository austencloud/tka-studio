/**
 * Metadata Tester State Management
 *
 * Manages the state for the metadata testing interface including:
 * - Available thumbnail files
 * - Selected sequence/thumbnail
 * - Extracted metadata
 * - Loading states
 * - Error handling
 */

import { PngMetadataExtractor } from "$lib/utils/png-metadata-extractor";

export interface ThumbnailFile {
  name: string;
  path: string;
  word: string;
}

export interface MetadataTesterState {
  // Thumbnail management
  thumbnails: ThumbnailFile[];
  selectedThumbnail: ThumbnailFile | null;

  // Metadata extraction
  extractedMetadata: any | null;
  rawMetadata: string | null;

  // UI state
  isLoadingThumbnails: boolean;
  isExtractingMetadata: boolean;
  isBatchAnalyzing: boolean;

  // Error handling
  error: string | null;

  // Analysis data
  metadataStats: {
    // Basic counts
    totalBeats: number;
    sequenceLength: number;
    realBeatsCount: number;
    startPositionCount: number;

    // Author validation
    hasAuthor: boolean;
    authorName: string | null;
    authorMissing: boolean;
    authorInconsistent: boolean;

    // Level validation
    hasLevel: boolean;
    level: number | null;
    levelMissing: boolean;
    levelInconsistent: boolean;
    levelZero: boolean;

    // Start position validation
    hasStartPosition: boolean;
    startPositionMissing: boolean;
    startPositionInconsistent: boolean;
    startPositionValue: string | null;

    // Beat validation
    missingBeatNumbers: number[];
    missingLetters: number[];
    missingMotionData: number[];
    invalidMotionTypes: Array<{ beat: number; prop: string; type: string }>;

    // Data integrity issues
    duplicateBeats: number[];
    invalidBeatStructure: number[];
    missingRequiredFields: Array<{ beat: number; field: string }>;

    // Overall health
    hasErrors: boolean;
    hasWarnings: boolean;
    errorCount: number;
    warningCount: number;
    healthScore: number; // 0-100

    // Error and warning details for batch analysis
    errors?: string[];
    warnings?: string[];

    // Batch analysis support
    isBatchSummary?: boolean;
    batchSummary?: any;
  } | null;
}

export function createMetadataTesterState() {
  const state = $state<MetadataTesterState>({
    thumbnails: [],
    selectedThumbnail: null,
    extractedMetadata: null,
    rawMetadata: null,
    isLoadingThumbnails: false,
    isExtractingMetadata: false,
    isBatchAnalyzing: false,
    error: null,
    metadataStats: null,
  });

  // Load available thumbnails on initialization
  async function loadThumbnails() {
    state.isLoadingThumbnails = true;
    state.error = null;

    try {
      const thumbnails: ThumbnailFile[] = [];

      // Try API first, fallback to manual discovery
      try {
        const response = await fetch("/api/sequences");
        if (response.ok) {
          const data = await response.json();
          if (data.success && Array.isArray(data.sequences)) {
            // Filter out test sequences like A_A
            const filteredSequences = data.sequences.filter(
              (seq: ThumbnailFile) =>
                seq.word !== "A_A" &&
                !seq.word.includes("_") &&
                seq.word.length > 0
            );
            state.thumbnails = filteredSequences;
            console.log(
              `✅ Loaded ${filteredSequences.length} sequences from API (${data.sequences.length - filteredSequences.length} filtered out)`
            );
            return;
          }
        }
      } catch {
        console.log("📡 API not available, using manual discovery...");
      }

      // Manual discovery - check known sequences
      const knownSequences = [
        "ABC",
        "A",
        "CAKE",
        "ALPHA",
        "EPSILON",
        "ETA",
        "MU",
        "B",
        "C",
        "DJ",
        "DJII",
        "DKIIEJII",
        "EJ",
        "EK",
        "FJ",
        "FL",
        "FLII",
        "G",
        "H",
        "I",
        "JD",
        "JGG",
        "KE",
        "LF",
        "MOON",
        "MP",
        "NQ",
        "OR",
        "OT",
        "PQV",
        "QT",
        "RT",
        "S",
        "T",
        "U",
        "V",
        "POSSUM",
        "OPOSSUM",
        "OPPOSSUM",
      ];

      // Filter out test/invalid sequences
      const validSequences = knownSequences.filter(
        (seq) =>
          !seq.includes("_") && // Exclude sequences with underscores (test sequences)
          seq !== "A_A" && // Specifically exclude A_A
          seq.length > 0
      );

      let foundCount = 0;

      // Check dictionary sequences first
      for (const sequenceName of validSequences) {
        const filePath = `/dictionary/${sequenceName}/${sequenceName}_ver1.png`;

        try {
          const response = await fetch(filePath, { method: "HEAD" });
          if (response.ok) {
            thumbnails.push({
              name: `${sequenceName}_ver1.png`,
              path: filePath,
              word: sequenceName,
            });
            foundCount++;
            console.log(`✅ Found: ${sequenceName}`);
          } else {
            console.log(`❌ Not found: ${sequenceName} (${response.status})`);
          }
        } catch (error) {
          console.log(`❌ Error checking ${sequenceName}:`, error);
        }
      }

      // Check static thumbnails directory (currently empty - add files that actually exist)
      const staticThumbnails: ThumbnailFile[] = [];

      for (const thumb of staticThumbnails) {
        try {
          const response = await fetch(thumb.path, { method: "HEAD" });
          if (response.ok) {
            thumbnails.push(thumb);
            foundCount++;
            console.log(`✅ Found thumbnail: ${thumb.word}`);
          }
        } catch {
          console.log(`❌ Thumbnail not found: ${thumb.word}`);
        }
      }

      // Sort by word name
      thumbnails.sort((a, b) => a.word.localeCompare(b.word));
      state.thumbnails = thumbnails;

      console.log(`🎯 Total sequences loaded: ${foundCount}`);

      if (foundCount === 0) {
        state.error =
          "No sequence files found. Please check that PNG files exist in the dictionary directories.";
      }
    } catch (error) {
      state.error = `Failed to load thumbnails: ${error}`;
      console.error("❌ Error loading thumbnails:", error);
    } finally {
      state.isLoadingThumbnails = false;
    }
  }

  // Extract metadata from selected thumbnail
  async function extractMetadata(thumbnail: ThumbnailFile) {
    state.isExtractingMetadata = true;
    state.error = null;
    state.selectedThumbnail = thumbnail;

    try {
      const metadata = await PngMetadataExtractor.extractMetadata(
        thumbnail.path
      );
      state.extractedMetadata = metadata;
      state.rawMetadata = JSON.stringify(metadata, null, 2);

      // Analyze the metadata
      analyzeMetadata(metadata);
    } catch (error) {
      state.error = `Failed to extract metadata: ${error}`;
      state.extractedMetadata = null;
      state.rawMetadata = null;
      state.metadataStats = null;
      console.error("Error extracting metadata:", error);
    } finally {
      state.isExtractingMetadata = false;
    }
  }

  // Analyze extracted metadata for useful information
  function analyzeMetadata(metadata: any) {
    if (!metadata || !Array.isArray(metadata)) {
      state.metadataStats = null;
      return;
    }

    console.log("🔍 Starting deep metadata analysis...");

    // Filter out start position entries and count actual beats
    const startPositionEntries = metadata.filter(
      (step: any) => step.sequence_start_position
    );
    const realBeats = metadata.filter(
      (step: any) => step.letter && !step.sequence_start_position
    );

    // Basic counts
    const totalBeats = realBeats.length;
    const sequenceLength = metadata.length;
    const realBeatsCount = realBeats.length;
    const startPositionCount = startPositionEntries.length;

    // Author analysis
    const firstStep = metadata[0] || {};
    const hasAuthor = !!firstStep.author;
    const authorName = firstStep.author || null;
    const authorMissing = !hasAuthor;

    // Check for author inconsistency across beats
    const authorsFound = new Set(
      metadata.map((step: any) => step.author).filter(Boolean)
    );
    const authorInconsistent = authorsFound.size > 1;

    // Level analysis
    const hasLevel = !!firstStep.level;
    const level = firstStep.level || null;
    const levelMissing = !hasLevel;
    const levelZero = level === 0;

    // Check for level inconsistency
    const levelsFound = new Set(
      metadata
        .map((step: any) => step.level)
        .filter((l) => l !== undefined && l !== null)
    );
    const levelInconsistent = levelsFound.size > 1;

    // Start position analysis
    const hasStartPosition = startPositionCount > 0;
    const startPositionMissing = !hasStartPosition;
    const startPositionValue =
      startPositionEntries[0]?.sequence_start_position || null;

    // Check for start position inconsistency
    const startPositionsFound = new Set(
      startPositionEntries.map((step: any) => step.sequence_start_position)
    );
    const startPositionInconsistent = startPositionsFound.size > 1;

    // Beat validation
    const missingBeatNumbers: number[] = [];
    const missingLetters: number[] = [];
    const missingMotionData: number[] = [];
    const invalidMotionTypes: Array<{
      beat: number;
      prop: string;
      type: string;
    }> = [];
    const duplicateBeats: number[] = [];
    const invalidBeatStructure: number[] = [];
    const missingRequiredFields: Array<{ beat: number; field: string }> = [];

    // Valid motion types (expand this list as needed)
    const validMotionTypes = [
      "pro",
      "anti",
      "static",
      "float",
      "dash",
      "bi_static",
      "shift",
      "kinetic_shift",
    ];

    // Check each real beat for issues
    const seenBeatNumbers = new Set<number>();
    realBeats.forEach((beat: any, index: number) => {
      const beatNumber = index + 1;

      // Check for missing letter
      if (!beat.letter) {
        missingLetters.push(beatNumber);
      }

      // Check for duplicate beat numbers (if they have beat_number field)
      if (beat.beat_number !== undefined) {
        if (seenBeatNumbers.has(beat.beat_number)) {
          duplicateBeats.push(beatNumber);
        }
        seenBeatNumbers.add(beat.beat_number);
      }

      // Check motion data
      if (!beat.blue_attributes && !beat.red_attributes) {
        missingMotionData.push(beatNumber);
      } else {
        // Check blue motion
        if (beat.blue_attributes) {
          const blueMotion = beat.blue_attributes.motion_type;
          if (!blueMotion) {
            missingRequiredFields.push({
              beat: beatNumber,
              field: "blue_attributes.motion_type",
            });
          } else if (!validMotionTypes.includes(blueMotion)) {
            invalidMotionTypes.push({
              beat: beatNumber,
              prop: "blue",
              type: blueMotion,
            });
          }
        }

        // Check red motion
        if (beat.red_attributes) {
          const redMotion = beat.red_attributes.motion_type;
          if (!redMotion) {
            missingRequiredFields.push({
              beat: beatNumber,
              field: "red_attributes.motion_type",
            });
          } else if (!validMotionTypes.includes(redMotion)) {
            invalidMotionTypes.push({
              beat: beatNumber,
              prop: "red",
              type: redMotion,
            });
          }
        }
      }

      // Check for basic beat structure
      if (!beat.letter && !beat.blue_attributes && !beat.red_attributes) {
        invalidBeatStructure.push(beatNumber);
      }
    });

    // Calculate health metrics
    let errorCount = 0;
    let warningCount = 0;

    // Count errors (critical issues)
    if (authorMissing) errorCount++;
    if (levelMissing) errorCount++;
    if (startPositionMissing) errorCount++;
    if (levelZero) errorCount++;
    errorCount += missingBeatNumbers.length;
    errorCount += missingLetters.length;
    errorCount += missingMotionData.length;
    errorCount += invalidBeatStructure.length;
    errorCount += missingRequiredFields.length;

    // Count warnings (non-critical issues)
    if (authorInconsistent) warningCount++;
    if (levelInconsistent) warningCount++;
    if (startPositionInconsistent) warningCount++;
    warningCount += duplicateBeats.length;
    warningCount += invalidMotionTypes.length;

    const hasErrors = errorCount > 0;
    const hasWarnings = warningCount > 0;

    // Calculate health score (0-100)
    const maxPossibleIssues = 10; // Adjust based on how many different types of issues we check
    const totalIssues = errorCount + warningCount * 0.5; // Warnings count as half
    const healthScore = Math.max(
      0,
      Math.round((1 - totalIssues / maxPossibleIssues) * 100)
    );

    // Generate error and warning arrays for batch analysis
    const errors: string[] = [];
    const warnings: string[] = [];

    // Critical errors
    if (authorMissing) errors.push("Missing author");
    if (levelMissing) errors.push("Missing level");
    if (startPositionMissing) errors.push("Missing start position");
    if (missingLetters.length > 0)
      errors.push(`Missing letters in ${missingLetters.length} beats`);
    if (missingMotionData.length > 0)
      errors.push(`Missing motion data in ${missingMotionData.length} beats`);
    if (invalidMotionTypes.length > 0)
      errors.push(`Invalid motion types in ${invalidMotionTypes.length} beats`);
    if (duplicateBeats.length > 0)
      errors.push(`Duplicate beats found: ${duplicateBeats.length}`);
    if (invalidBeatStructure.length > 0)
      errors.push(
        `Invalid beat structure in ${invalidBeatStructure.length} beats`
      );

    // Warnings
    if (authorInconsistent) warnings.push("Author inconsistent across beats");
    if (levelInconsistent) warnings.push("Level inconsistent across beats");
    if (levelZero) warnings.push("Level is zero (may be invalid)");
    if (startPositionInconsistent) warnings.push("Start position inconsistent");
    if (missingRequiredFields.length > 0)
      warnings.push(
        `Missing required fields in ${missingRequiredFields.length} beats`
      );
    if (realBeatsCount !== sequenceLength && sequenceLength > 0)
      warnings.push("Beat count mismatch with sequence length");

    state.metadataStats = {
      // Basic counts
      totalBeats,
      sequenceLength,
      realBeatsCount,
      startPositionCount,

      // Author validation
      hasAuthor,
      authorName,
      authorMissing,
      authorInconsistent,

      // Level validation
      hasLevel,
      level,
      levelMissing,
      levelInconsistent,
      levelZero,

      // Start position validation
      hasStartPosition,
      startPositionMissing,
      startPositionInconsistent,
      startPositionValue,

      // Beat validation
      missingBeatNumbers,
      missingLetters,
      missingMotionData,
      invalidMotionTypes,

      // Data integrity issues
      duplicateBeats,
      invalidBeatStructure,
      missingRequiredFields,

      // Overall health
      hasErrors,
      hasWarnings,
      errorCount,
      warningCount,
      healthScore,

      // Error and warning details for batch analysis
      errors,
      warnings,
    };

    // Log analysis results
    console.log("📊 Metadata Analysis Results:");
    console.log(`   Health Score: ${healthScore}/100`);
    console.log(`   Errors: ${errorCount}, Warnings: ${warningCount}`);
    console.log(`   Author: ${authorName || "MISSING"}`);
    console.log(`   Level: ${level !== null ? level : "MISSING"}`);
    console.log(`   Start Position: ${startPositionValue || "MISSING"}`);
    console.log(`   Beats: ${totalBeats}, Sequence Length: ${sequenceLength}`);

    if (hasErrors || hasWarnings) {
      console.log("⚠️ Issues found:");
      if (authorMissing) console.log("   - Missing author");
      if (levelMissing) console.log("   - Missing level");
      if (startPositionMissing) console.log("   - Missing start position");
      if (missingLetters.length)
        console.log(
          `   - Missing letters in beats: ${missingLetters.join(", ")}`
        );
      if (missingMotionData.length)
        console.log(
          `   - Missing motion data in beats: ${missingMotionData.join(", ")}`
        );
      if (invalidMotionTypes.length)
        console.log(
          `   - Invalid motion types: ${invalidMotionTypes.length} found`
        );
    }
  }

  // Clear current selection and metadata
  async function handleBatchAnalyze() {
    console.log("Starting batch metadata analysis...");
    state.isBatchAnalyzing = true;
    state.error = null;

    try {
      let analyzed = 0;
      let totalErrors = 0;
      let totalWarnings = 0;
      let healthySequences = 0;
      let totalHealthScore = 0;
      const sequenceResults: { [key: string]: any } = {};
      const errorPatterns: { [key: string]: number } = {};
      const warningPatterns: { [key: string]: number } = {};

      for (const thumbnail of state.thumbnails) {
        console.log(`Analyzing sequence: ${thumbnail.word}`);

        // Extract metadata for this sequence
        await extractMetadata(thumbnail);

        // Ensure we analyze the metadata to get errors/warnings
        if (state.metadataStats) {
          analyzeMetadata(state.extractedMetadata);
        }

        // Store results
        if (state.metadataStats) {
          const errorCount = state.metadataStats.errors?.length || 0;
          const warningCount = state.metadataStats.warnings?.length || 0;

          sequenceResults[thumbnail.word] = {
            healthScore: state.metadataStats.healthScore,
            errorCount: errorCount,
            warningCount: warningCount,
            isHealthy: state.metadataStats.healthScore >= 80,
            errors: state.metadataStats.errors || [],
            warnings: state.metadataStats.warnings || [],
          };

          totalErrors += errorCount;
          totalWarnings += warningCount;
          totalHealthScore += state.metadataStats.healthScore;
          if (state.metadataStats.healthScore >= 80) healthySequences++;

          // Track error patterns
          if (state.metadataStats.errors) {
            state.metadataStats.errors.forEach((error: string) => {
              errorPatterns[error] = (errorPatterns[error] || 0) + 1;
            });
          }

          // Track warning patterns
          if (state.metadataStats.warnings) {
            state.metadataStats.warnings.forEach((warning: string) => {
              warningPatterns[warning] = (warningPatterns[warning] || 0) + 1;
            });
          }
        }

        analyzed++;
      }

      const averageHealth = totalHealthScore / analyzed;

      // Create a comprehensive batch summary
      const batchSummary = {
        sequencesAnalyzed: analyzed,
        healthySequences: healthySequences,
        unhealthySequences: analyzed - healthySequences,
        averageHealthScore: Math.round(averageHealth * 10) / 10,
        totalErrors: totalErrors,
        totalWarnings: totalWarnings,
        commonErrors: Object.entries(errorPatterns)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 5),
        commonWarnings: Object.entries(warningPatterns)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 5),
        worstSequences: Object.entries(sequenceResults)
          .sort((a, b) => a[1].healthScore - b[1].healthScore)
          .slice(0, 5)
          .map(([seq, data]) => ({
            sequence: seq,
            healthScore: data.healthScore,
          })),
        bestSequences: Object.entries(sequenceResults)
          .sort((a, b) => b[1].healthScore - a[1].healthScore)
          .slice(0, 5)
          .map(([seq, data]) => ({
            sequence: seq,
            healthScore: data.healthScore,
          })),
      };

      // Clear individual selection to focus on batch results
      state.selectedThumbnail = null;

      // Update metadata stats to show batch summary
      state.metadataStats = {
        // Copy existing structure with defaults
        totalBeats: 0,
        sequenceLength: 0,
        realBeatsCount: 0,
        startPositionCount: 0,
        hasAuthor: false,
        authorName: null,
        authorMissing: true,
        authorInconsistent: false,
        hasLevel: false,
        level: null,
        levelMissing: true,
        levelInconsistent: false,
        levelZero: false,
        hasStartPosition: false,
        startPositionMissing: true,
        startPositionInconsistent: false,
        startPositionValue: null,
        missingBeatNumbers: [],
        missingLetters: [],
        missingMotionData: [],
        invalidMotionTypes: [],
        duplicateBeats: [],
        invalidBeatStructure: [],
        missingRequiredFields: [],
        hasErrors: totalErrors > 0,
        hasWarnings: totalWarnings > 0,
        errorCount: totalErrors,
        warningCount: totalWarnings,
        healthScore: averageHealth,
        errors: Object.keys(errorPatterns),
        warnings: Object.keys(warningPatterns),
        isBatchSummary: true,
        batchSummary,
      };

      console.log(`Batch Analysis Complete:`);
      console.log(`- Sequences Analyzed: ${analyzed}`);
      console.log(
        `- Healthy Sequences (80+ score): ${healthySequences} (${Math.round((healthySequences / analyzed) * 100)}%)`
      );
      console.log(
        `- Unhealthy Sequences: ${analyzed - healthySequences} (${Math.round(((analyzed - healthySequences) / analyzed) * 100)}%)`
      );
      console.log(`- Average Health Score: ${averageHealth.toFixed(1)}%`);
      console.log(`- Total Errors: ${totalErrors}`);
      console.log(`- Total Warnings: ${totalWarnings}`);
      console.log(`- Most Common Errors:`, batchSummary.commonErrors);
      console.log(`- Most Common Warnings:`, batchSummary.commonWarnings);
      console.log("Batch summary created:", batchSummary);
    } catch (error) {
      console.error("Batch analysis failed:", error);
      state.error = `Batch analysis failed: ${error}`;
    } finally {
      state.isBatchAnalyzing = false;
    }
  }

  function clearSelection() {
    state.selectedThumbnail = null;
    state.extractedMetadata = null;
    state.rawMetadata = null;
    state.metadataStats = null;
    state.error = null;
  }

  // Initialize by loading thumbnails
  loadThumbnails();

  return {
    get state() {
      return state;
    },
    loadThumbnails,
    extractMetadata,
    clearSelection,
    analyzeMetadata,
    handleBatchAnalyze,
  };
}
