/**
 * Browse Metadata Types
 *
 * Essential metadata types needed for Browse tab functionality.
 * These are the core types needed for sequence discovery and metadata extraction.
 */

// ============================================================================
// ESSENTIAL BROWSE METADATA TYPES
// ============================================================================

export interface ThumbnailFile {
  name: string;
  path: string;
  size: number;
  lastModified: Date;
  metadata?: {
    word?: string;
    author?: string;
    difficulty?: number;
    tags?: string[];
  };
}

export interface SequenceFile {
  name: string;
  path: string;
  content: string;
  metadata: Record<string, unknown>;
  isValid: boolean;
}

export interface MetadataAnalysisResult {
  fileName: string;
  isValid: boolean;
  errors: string[];
  warnings: string[];
  extractedData: Record<string, unknown>;
  processingTime: number;
}

export interface BatchAnalysisResult {
  totalFiles: number;
  processedFiles: number;
  validFiles: number;
  invalidFiles: number;
  errors: string[];
  warnings: string[];
  results: MetadataAnalysisResult[];
  summary: {
    successRate: number;
    averageProcessingTime: number;
    commonErrors: string[];
    recommendations: string[];
  };
}
