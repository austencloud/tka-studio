/**
 * Application Service Interfaces
 *
 * Consolidated interfaces for application-level services.
 * This file consolidates interfaces that were previously scattered.
 */

// Re-export from individual interface files
export type { IApplicationInitializer } from "./application/IApplicationInitializer";
export type { ISettingsService } from "./application/ISettingsService";
export type { IDeviceDetector, ResponsiveSettings } from "./application/IDeviceDetector";

// Re-export domain types
export type { AppSettings } from "$domain/core/AppSettings";

// Additional interfaces that may be referenced
export interface ISequenceAnimationEngine {
  startAnimation(): void;
  stopAnimation(): void;
  pauseAnimation(): void;
  resumeAnimation(): void;
  setSpeed(speed: number): void;
  getCurrentFrame(): number;
  getTotalFrames(): number;
  isPlaying(): boolean;
}

export interface IStartPositionService {
  getAvailableStartPositions(): Promise<string[]>;
  getStartPositionData(position: string): Promise<any>;
  validateStartPosition(position: string): boolean;
}
