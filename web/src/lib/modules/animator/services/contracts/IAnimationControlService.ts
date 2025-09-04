/**
 * Animation Control Service Interface
 *
 * Interface for controlling animation playback.
 * Handles play, pause, stop, seek, and speed control.
 */

export interface IAnimationControlService {
  play(): void;
  pause(): void;
  stop(): void;
  seek(position: number): void;
  setSpeed(speed: number): void;
}
