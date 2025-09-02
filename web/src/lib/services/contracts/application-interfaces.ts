/**
 * Application Service Interfaces
 *
 * Consolidated interfaces for application-level services.
 * This file consolidates interfaces that were previously scattered.
 */

// Re-export from individual interface files
export type { IApplicationInitializer } from "./application/IApplicationInitializer";
export type { IDeviceDetector } from "./application/IDeviceDetector";
export type { ISettingsService } from "./application/ISettingsService";

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
