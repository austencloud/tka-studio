/**
 * Swipe Detection Service Implementation
 *
 * Converts raw touch/pointer events into semantic hand path gestures.
 * Handles coordinate mapping and closest-point detection.
 */

import type { GridLocation, GridMode } from "$shared";
import { inject, injectable } from "inversify";
import { TYPES } from "$lib/shared/inversify/types";
import type { GridPositionPoint, SwipeGesture } from "../../domain";
import type { IHandPathDirectionDetector } from "../contracts/IHandPathDirectionDetector";
import type { ISwipeDetectionService } from "../contracts/ISwipeDetectionService";

@injectable()
export class SwipeDetectionService implements ISwipeDetectionService {
  constructor(
    @inject(TYPES.IHandPathDirectionDetector)
    private handPathDirectionDetector: IHandPathDirectionDetector
  ) {}

  findClosestGridPosition(
    x: number,
    y: number,
    gridPositions: readonly GridPositionPoint[]
  ): GridLocation | null {
    if (gridPositions.length === 0) {
      return null;
    }

    let closestPosition: GridPositionPoint | null = null;
    let minDistance = Infinity;

    for (const position of gridPositions) {
      const distance = Math.sqrt(
        Math.pow(x - position.x, 2) + Math.pow(y - position.y, 2)
      );

      if (distance < minDistance) {
        minDistance = distance;
        closestPosition = position;
      }
    }

    // Only return if within hit radius
    if (closestPosition && minDistance <= closestPosition.radius) {
      return closestPosition.location;
    }

    // If nothing within radius, return closest anyway (always snap)
    return closestPosition?.location || null;
  }

  hasMovedSignificantly(
    startX: number,
    startY: number,
    currentX: number,
    currentY: number,
    threshold: number
  ): boolean {
    const distance = Math.sqrt(
      Math.pow(currentX - startX, 2) + Math.pow(currentY - startY, 2)
    );
    return distance > threshold;
  }

  calculateVelocity(
    startX: number,
    startY: number,
    endX: number,
    endY: number,
    durationMs: number
  ): number {
    if (durationMs === 0) {
      return 0;
    }

    const distance = Math.sqrt(
      Math.pow(endX - startX, 2) + Math.pow(endY - startY, 2)
    );

    return distance / durationMs; // pixels per millisecond
  }

  buildSwipeGesture(
    startLocation: GridLocation,
    endLocation: GridLocation,
    velocity: number,
    duration: number,
    gridMode: GridMode
  ): SwipeGesture {
    const handMotionType = this.handPathDirectionDetector.getHandMotionType(
      startLocation,
      endLocation,
      gridMode
    );

    return {
      startLocation,
      endLocation,
      handMotionType,
      velocity,
      duration,
    };
  }
}
