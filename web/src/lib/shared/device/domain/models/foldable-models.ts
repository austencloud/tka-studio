// ============================================================================
// FOLDABLE DEVICE TYPES
// ============================================================================

export interface FoldableDeviceSpec {
  models: string[];
  foldedDimensions: {
    width: { min: number; max: number };
    height: { min: number; max: number };
  };
  unfoldedDimensions: {
    width: { min: number; max: number };
    height: { min: number; max: number };
  };
}

export interface FoldableDetectionResult {
  isFoldable: boolean;
  isUnfolded: boolean;
  detectedDevice: string | null;
  confidence: number;
  aspectRatio: number;
  foldableType?: "zfold" | "other" | "unknown";
  detectionMethod?: string;
  debugInfo?: {
    userAgent: string;
    dimensions: { width: number; height: number };
    matchedSpecs?: string[];
  };
}
